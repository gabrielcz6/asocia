import itertools
import streamlit as st
from db.MongoConnection import MongoConnection
import pandas as pd
import json
import utils.funcionespredefinidadisplay
from pymongo import MongoClient
import pandas as pd
import datetime
from bson import ObjectId


# Función para calcular el promedio de puntajes
def calculate_average(doc):
    # Recorremos los resultados y extraemos los puntajes
    puntajes = []
    for result in doc['resultados']:
        valor = result['puntaje']['valor']
        if valor.isdigit():  # Aseguramos que el valor sea numérico
            puntajes.append(int(valor))
    
    if puntajes:
        # Calculamos el promedio de los puntajes
        promedio = sum(puntajes) / len(puntajes)
    else:
        promedio = None
    
    return promedio


backend = MongoConnection()
backend.connect()


client = MongoClient('mongodb://localhost:27017/')
db = client['asocia']
evaluations_collection = db['evaluations']
a = evaluations_collection.find()  # Buscar documentos en la colección "evaluations"

print(a)
results = list(a)  # 'a' es el cursor
#for doc in results:
#    print(doc)

  # Aplanamos el documento
data = (results[0])
print(data)
# Función para aplanar el documento
def flatten_document_with_average(doc):
    data = []
    promedio = calculate_average(doc)  # Calculamos el promedio
    data.append({
        'id_rubrica': doc['rubrica']['_id'],
        'nombre_rubrica': doc['rubrica']['nombre'],
        'teacher_id': doc['teacher_id'],
        'teacher_name': doc['teacher_name'],
        'curso_name': doc['curso']['name'],
        'curso_semester': doc['curso']['semester'],
        'curso_año': doc['curso']['year'],
        'fecha': doc['fecha_evaluacion'].strftime('%Y-%m-%d %H:%M:%S'),
        'alumno_id': doc['alumno']['id'],
        'alumno_name': doc['alumno']['name'],
        'promedio_puntajes': promedio
    })
    return data

# Aplanar los resultados y almacenar en un DataFrame
flattened_data = flatten_document_with_average(data)

df = pd.DataFrame(flattened_data)

# Guardar el DataFrame en un archivo Excel
excel_filename = "evaluaciones_promedio.xlsx"
df.to_excel(excel_filename, index=False)

print(f"El archivo Excel ha sido guardado como {excel_filename}")

