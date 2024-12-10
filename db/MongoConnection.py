from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson import ObjectId
import os
import sys
#from dotenv import load_dotenv
#load_dotenv()
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.Theme import VERDE
from utils.Theme import GRIS
from utils.Theme import ROJO
from utils.Theme import AZUL
from utils.Theme import BLANCO

class MongoConnection:
    def __init__(self, uri=os.getenv("MONGO_HOST"), db_name="asocia"):
        self.uri = uri
        self.db_name = db_name
        self.client = None
        self.db = None

    def reload(self):
        import importlib
        import db.MongoConnection
        importlib.reload(db.MongoConnection)
        for name, method in db.MongoConnection.MongoConnection.__dict__.items():
            if callable(method):
                setattr(self, name, method.__get__(self, self.__class__))
        print("MongoConnection reloaded")

    def connect(self) -> None:
        """Establece la conexión con MongoDB."""
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.db_name]
            print(f"{VERDE}Conectado a la base de datos: {self.db_name}{GRIS}\n")
        except ConnectionFailure as e:
            print(f"No se pudo conectar a MongoDB: {e}")
            raise

    def create_unique_index(self, collection_name, field_name):
        """Crea un índice único en el campo especificado de la colección."""
        if self.db == None:
            raise ConnectionFailure(f"{ROJO}No está conectado a la base de datos.{GRIS}")
        collection = self.db[collection_name]
        # Crear índice único
        collection.create_index([(field_name, 1)], unique=True)
        print(f"{AZUL}Índice único creado en el campo: {VERDE}{field_name}{GRIS}")

    def insert_document(self, collection_name, document):
        """Inserta un documento en la colección especificada."""
        try:
            if self.db == None:
                raise ConnectionFailure(f"{ROJO}No está conectado a la base de datos.{GRIS}")
            collection = self.db[collection_name]
            result = collection.insert_one(document)
            print(f"{AZUL}Documento insertado con ID: {VERDE}{result.inserted_id}{GRIS}")
        except KeyboardInterrupt:
            raise Exception("Interrupción por el usuario, revise si se guardo correctamente la última data")

    def find_documents(self, collection_name, query={}):
        """Consulta documentos en la colección especificada."""
        print("debug")
        if self.db == None:
            raise ConnectionFailure("No está conectado a la base de datos.")
        collection = self.db[collection_name]
        results = collection.find(query)
        return list(results)
    

    def update_document(self, collection_name, docNumber, update_fields):
        """
        Actualiza un documento en la colección especificada basado en 'docNumber' 
        y agrega los nuevos campos pasados en 'update_fields'.
        
        Parameters:
        - collection_name: Nombre de la colección en la que se actualizará el documento.
        - docNumber: Número de documento (criterio de búsqueda).
        - update_fields: Diccionario con los campos a actualizar.
        """
        if self.db is None:
            raise ConnectionFailure("No está conectado a la base de datos.")
        
        collection = self.db[collection_name]
        
        # Definir el criterio de búsqueda (filtro) en base al número de documento
        query = {"docNumber": docNumber}
        
        # Actualizar los campos en base a los valores proporcionados
        update = {"$set": update_fields}
        
        # Realizar la actualización del documento
        result = collection.update_one(query, update)
        
        if result.matched_count > 0:
            # print(f"{AZUL}MongoManager: {BLANCO}Documento con 'docNumber' {docNumber} {VERDE}actualizado correctamente.{GRIS}")
            pass
        else:
            print(f"No se encontró ningún documento con 'docNumber' {docNumber}.")
            raise Exception("No se encontró registro")

    def close_connection(self):
        """Cierra la conexión con MongoDB."""
        if self.client:
            self.client.close()
            print("Conexión cerrada.")

    def login(self, user, password):
        """
        Autentica un usuario verificando su nombre de usuario y contraseña.

        :param collection_name: Nombre de la colección donde están los usuarios.
        :param usuario: Nombre de usuario.
        :param password: Contraseña del usuario.
        :return: Diccionario con los datos del usuario si el login es exitoso, None si falla.
        """
        # Acceder a la colección
        collection = self.db["users"]

        # Buscar el usuario en la colección
        user = collection.find_one({"usuario": user})

        if user:
            # Verificar contraseña
            if user["password"] == password:
                print(f"{VERDE}Loggin success{GRIS}\n")
                return user
                # return {
                #     "usuario": user["usuario"],
                #     "rol": user["rol"]
                # }
            else:
                # Contraseña incorrecta
                print(f"{VERDE}Loggin failed: password{GRIS}\n")
                return None
        else:
            # Usuario no encontrado
            print(f"{VERDE}Loggin failed: user{GRIS}\n")
            return None
        
    def find_courses_by_user(self, user_id: str, include_students: bool = False):
        """
        Find all courses associated with a specific user, including the year from the user_course collection.
        Optionally include students associated with each course.
        
        :param user_id: The ObjectId of the user as a string.
        :param include_students: Boolean indicating whether to include student information.
        :return: A list of dictionaries, each containing course details, the year, and optionally the students.
        """
        user_course_collection = self.db["user_course"]
        course_collection = self.db["courses"]  # Assuming you have a "courses" collection for course details.

        # Find all course IDs and years associated with the user
        user_courses = list(user_course_collection.find({"user_id": user_id}, {"course_id": 1, "year": 1, "students": 1, "_id": 0}))

        # Extract course IDs and map them to their respective years (and optionally students)
        course_year_mapping = {uc["course_id"]: {"year": uc["year"], "students": uc.get("students", [])} for uc in user_courses}
        course_ids = list(course_year_mapping.keys())

        # Fetch the detailed course information from the courses collection
        courses = list(course_collection.find({"_id": {"$in": course_ids}}))

        # Add the year (and optionally students) to each course result
        for course in courses:
            course_details = course_year_mapping[course["_id"]]
            course["year"] = course_details["year"]
            if include_students:
                course["students"] = course_details["students"]

        return courses
    

    def save_rubric(self, student, course, rubric, course_id):
        """
        Guarda una rúbrica en la colección `rubrics`.
        
        :param student: Diccionario con los datos del estudiante seleccionado.
        :param course: Diccionario con los datos del curso seleccionado.
        :param rubric: String o estructura que representa la rúbrica actual.
        :return: El resultado de la operación de inserción.
        """
        try: 
            rubrics_collection = self.db["rubrics"]  # Conectar a la colección `rubrics`
            
            # Crear el documento a guardar
            rubric_document = {
                "student": student,
                "course": {
                    "id": course_id,
                    "name": course["name"],
                    "year": course["year"],
                    "semester": course["semester"]
                },
                "rubric": rubric
            }

            # Guardar el documento en la colección
            result = rubrics_collection.insert_one(rubric_document)
            return result.inserted_id 
        except:
            return False

# Ejemplo de uso
if __name__ == "__main__":
    mongo = MongoConnection('mongodb://localhost:27017/', 'asocia')
    mongo.connect()
    print(mongo.find_courses_by_user(ObjectId("67550e8e278f66cc36fe9342"), include_students=True))