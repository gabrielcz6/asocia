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

backend = MongoConnection()
backend.connect()


client = MongoClient('mongodb://localhost:27017/')
db = client['asocia']
evaluations_collection = db['evaluations']
a = evaluations_collection.find()  # Buscar documentos en la colección "evaluations"






# Aplanamos el documento, separando los valores anidados en columnas
def flatten_document(doc):
    flat_doc = {
        '_id': doc['_id'],
        'fechaEvaluacion': doc['fechaEvaluacion'],
        'usuarioEvaluadorID': doc['usuarioEvaluadorID'],
        'alumnoID': doc['alumnoID'],
        'rubrica_id': doc['rubrica']['_id'],
        'rubrica_nombre': doc['rubrica']['nombre']
    }
    
    # Procesar los criterios de la rubrica (pueden tener varias entradas)
    criterios = doc['rubrica']['criterios']
    for i, criterio in enumerate(criterios, 1):
        flat_doc[f'criterio_{i}_id'] = criterio['_id']
        flat_doc[f'criterio_{i}_nombre'] = criterio['nombre']
        flat_doc[f'criterio_{i}_puntaje_valor'] = criterio['puntajeOtorgado']['valor']
        flat_doc[f'criterio_{i}_puntaje_etiqueta'] = criterio['puntajeOtorgado']['etiqueta']
    
    return flat_doc



print(a)
results = list(a)  # 'a' es el cursor
for doc in results:
    print(doc)

# Aplanamos el documento
flattened_document = flatten_document(results[0])

# Convertimos a DataFrame
df = pd.DataFrame([flattened_document])

# Mostramos el DataFrame
print(df.head(10))

# Guardar el DataFrame como un archivo Excel
excel_file = 'evaluations_data.xlsx'
df.to_excel(excel_file, index=False)

# Mostrar un mensaje indicando que el archivo fue guardado
st.success(f"El archivo Excel ha sido guardado como {excel_file}")

# Opcional: Mostrar el DataFrame en Streamlit
st.write(df)
