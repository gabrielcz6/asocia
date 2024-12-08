from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os
import sys
from dotenv import load_dotenv
load_dotenv()
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


    def export_to_csv(self, collection_name, output_file, max_id=49000) -> None:
        """
        Exporta datos de MongoDB a un archivo CSV excluyendo 'updatedAt'.

        :param collection_name: Nombre de la colección
        :param output_file: Nombre del archivo de salida
        :param max_id: El valor máximo de 'id' a filtrar
        """
        try:
            # Verificar si hay conexión
            if self.db is None:
                raise ConnectionFailure("No hay conexión a la base de datos.")

            # Obtener la colección
            collection = self.db[collection_name]

            # Definir la consulta para filtrar los documentos
            query = {"id": {"$lte": max_id}}

            # Consultar los documentos de la colección
            cursor = collection.find(query)

            # Procesar los datos excluyendo 'updatedAt'
            processed_data = []
            for entry in cursor:
                excel_data = entry.get('data_excel', {})
                result_data = entry.get('result', {})

                combined_data = {
                    "NOMBRE": excel_data.get('nombre', ''),
                    "DISTRITO": excel_data.get('distrito', ''),
                    "TIP. DOCUMENTO": excel_data.get('tip. documento', ''),
                    "NRO. DOCUMENTO": excel_data.get('nro. documento', ''),
                    "NUMBER": result_data.get('number', ''),
                    "NAME": result_data.get('name', ''),
                    "MOTHERS_LASTNAME": result_data.get('mothersLastname', ''),
                    "FATHERS_LASTNAME": result_data.get('fathersLastname', ''),
                    "FULLNAME": result_data.get('fullName', ''),
                    "VERIFICATION_CODE": result_data.get('verificationCode', ''),
                    "GENDER": result_data.get('gender', ''),
                    "BIRTHDATE": result_data.get('birthDate', ''),
                    "MARITAL_STATUS": result_data.get('maritalStatus', ''),
                    "LOCATION": result_data.get('location', ''),
                    "LOCATION_RENIEC": result_data.get('locationReniec', ''),
                    "REGION": result_data.get('region', ''),
                    "PROVINCE": result_data.get('province', ''),
                    "DISTRICT": result_data.get('district', ''),
                    "ADDRESS": result_data.get('address', '')
                }
                processed_data.append(combined_data)

            # Crear un DataFrame y exportar a CSV
            df = pd.DataFrame(processed_data)
            df.to_csv(output_file, index=False)
            print(f"Exportación completada con éxito. Archivo guardado en {output_file}")
        
        except ConnectionFailure as e:
            print(f"Error de conexión: {e}")
        except Exception as e:
            print(f"Se produjo un error durante la exportación: {e}")

    def export_to_excel(self, collection_name, output_file, from_id: int, max_id=49000) -> None:
        """
        Exporta datos de MongoDB a un archivo Excel excluyendo 'updatedAt'.
        
        :param collection_name: Nombre de la colección
        :param output_file: Nombre del archivo de salida
        :param max_id: El valor máximo de 'id' a filtrar
        """
        try:
            # Verificar si hay conexión
            if self.db is None:
                raise Exception("No hay conexión a la base de datos.")

            # Obtener la colección
            collection = self.db[collection_name]

            # Definir la consulta para filtrar los documentos
            # query = {"id": {"$lte": max_id}}
            query = {"id": {"$gte": from_id, "$lte": max_id}}

            # Consultar los documentos de la colección
            cursor = collection.find(query)

            # Procesar los datos excluyendo 'updatedAt' y asegurando el orden correcto
            processed_data = []
            for entry in cursor:
                excel_data = entry.get('data_excel', {})
                result_data = entry.get('result', {})

                combined_data = {
                    "POSICION": entry.get('id', 0) + 1,
                    "NOMBRE": excel_data.get('nombre', ''),
                    "DISTRITO": excel_data.get('distrito', ''),
                    "TIP. DOCUMENTO": excel_data.get('tip. documento', ''),
                    "NRO. DOCUMENTO": excel_data.get('nro. documento', ''),
                    "NUMBER": result_data.get('number', ''),
                    "NAME": result_data.get('name', ''),
                    "MOTHERS_LASTNAME": result_data.get('mothersLastname', ''),
                    "FATHERS_LASTNAME": result_data.get('fathersLastname', ''),
                    "FULLNAME": result_data.get('fullName', ''),
                    "VERIFICATION_CODE": result_data.get('verificationCode', ''),
                    "GENDER": result_data.get('gender', ''),
                    "BIRTHDATE": result_data.get('birthDate', ''),
                    "MARITAL_STATUS": result_data.get('maritalStatus', ''),
                    "LOCATION": result_data.get('location', ''),
                    "LOCATION_RENIEC": result_data.get('locationReniec', ''),
                    "REGION": result_data.get('region', ''),
                    "PROVINCE": result_data.get('province', ''),
                    "DISTRICT": result_data.get('district', ''),
                    "ADDRESS": result_data.get('address', '')
                }
                processed_data.append(combined_data)

            # Crear un DataFrame y exportar a Excel
            df = pd.DataFrame(processed_data)
            # df.to_excel(output_file, index=False)
            with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False)
            print(f"Exportación completada con éxito. Archivo guardado en {output_file}")
        
        except Exception as e:
            print(f"Se produjo un error durante la exportación: {e}")

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
                return {
                    "usuario": user["usuario"],
                    "rol": user["rol"]
                }
            else:
                # Contraseña incorrecta
                print(f"{VERDE}Loggin failed: password{GRIS}\n")
                return None
        else:
            # Usuario no encontrado
            print(f"{VERDE}Loggin failed: user{GRIS}\n")
            return None

# Ejemplo de uso
if __name__ == "__main__":
    # Crear una instancia de la clase
    # mongo_conn = MongoConnection(uri="mongodb://localhost:27017/", db_name="mi_base_de_datos")
    
    # # Conectar a la base de datos
    # mongo_conn.connect()

    # # Insertar un documento
    # documento = {"nombre": "Alice", "edad": 30, "ciudad": "New York"}
    # mongo_conn.insert_document("usuarios", documento)

    # # Consultar documentos
    # resultados = mongo_conn.find_documents("usuarios", {"edad": {"$gt": 25}})
    # for doc in resultados:
    #     print(doc)

    # # Cerrar la conexión
    # mongo_conn.close_connection()


    # mongo_connection = MongoConnection('mongodb://localhost:27017/', 'LDS-Massive')
    # mongo_connection.connect()

    # # Luego puedes exportar los datos
    # mongo_connection.export_to_csv('DNI', 'output.csv')
    mongo_connection = MongoConnection('mongodb://localhost:27017/', 'LDS-Massive')
    mongo_connection.connect()

    # Luego puedes exportar los datos directamente a un archivo Excel
    mongo_connection.export_to_excel('DNI', 'DNI-297869-428000-PROCESADOS.xlsx', from_id=297869, max_id=428001)