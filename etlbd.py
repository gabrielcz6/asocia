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



def etlbd():
  backend = MongoConnection()
  backend.connect()
  
  
  client = MongoClient('mongodb://localhost:27017/')
  db = client['asocia']
  evaluations_collection = db['evaluations']
  a = evaluations_collection.find()  # Buscar documentos en la colección "evaluations"
  
  
  
  
  
  
  # Aplanamos el documento, separando los valores anidados en columnas
  def flatten_document(doc):
      total_obtenido = 0  # Inicializar variables
      total_maximo = 0
      for idx, resultado in enumerate(doc["resultados"], start=1):
              total_obtenido += float(resultado['puntaje']['valor'])
              for criterio in doc["rubrica"]["criterios"]:
                  if criterio["nombre"] == resultado["criterio"]:
                      total_maximo += max(float(p["valor"]) for p in criterio["puntajes"])
      promedio=total_obtenido/total_maximo
  
      flat_doc = {
          'rubrica_id':  str(doc['_id']),
          'nombre_rubrica': doc['rubrica']['nombre'],
          'descripcion_rubrica' : doc['rubrica']['descripcion'],
          'teacher_id': str(doc['teacher_id']),
          'teacher_name': doc['teacher_name'],
          'curso_name': doc['curso']['name'],
          'curso_semester': doc['curso']['semester'],
          'curso_año': doc['curso']['year'],
          'fecha': doc['fecha_evaluacion'],
          'alumno_id' : doc['alumno']['id'],
          'alumno_name': doc['alumno']['name'],
          'promedio_puntajes' : promedio,
          
          #'fecha_evaluacion': datetime.datetime(2024, 12, 15, 2, 33, 32, 360000)
      }
       # Si 'fecha_evaluacion' es datetime, formateamos a 'YYYY-MM-DD HH:MM:SS'
      if isinstance(flat_doc['fecha'], datetime.datetime):
          flat_doc['fecha'] = flat_doc['fecha'].strftime('%Y-%m-%d %H:%M:%S')
      else:
          # Si 'fecha_evaluacion' es string, lo convertimos a datetime y luego formateamos
          flat_doc['fecha'] = pd.to_datetime(flat_doc['fecha']).strftime('%Y-%m-%d %H:%M:%S')
  
      return flat_doc
      
                      
      
  
  
  
  
  #print(a)
  
  results = list(a)  # 'a' es el cursor
  # Aplanamos todos los documentos
  flattened_documents = [flatten_document(doc) for doc in results]
  
  # Convertimos todos los documentos a DataFrame
  df = pd.DataFrame(flattened_documents)
  
  # Convertir columnas con ObjectId a string explícitamente
  for col in df.columns:
      # Verificamos si la columna contiene ObjectId y la convertimos a string
      if df[col].apply(lambda x: isinstance(x, ObjectId)).any():
          df[col] = df[col].apply(str)
  
  # Mostrar DataFrame en Streamlit
  #st.write(df)
  
  # Guardar el DataFrame como un archivo Excel
  excel_file = 'evaluaciones_promedio.xlsx'
  df.to_excel(excel_file, index=False)
  
  # Mostrar un mensaje indicando que el archivo fue guardado
  # st.success(f"El archivo Excel ha sido guardado como {excel_file}")