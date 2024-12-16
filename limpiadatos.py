import pandas as pd
import openpyxl
import unidecode  # Librería para eliminar tildes
import re
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import CharacterTextSplitter
import os


def limpiaryguardarbdrubricas():
     filepath = r'evaluaciones_promedio.xlsx'
     df=pd.read_excel(filepath)
     df.head(10)
     
     #limpiando la bd
     #Eliminar columna nùmeros
     df = df.drop(df.columns[0], axis=1)
     #borra duplicados
     df = df.drop_duplicates()
     #cambiar nan o nulos con cadena ""
     df = df.fillna("")
     #limpiar espacios de mas
     df = df.replace('  ', ' ', regex=True)
     # Primero, convertimos todo el DataFrame a minúsculas
     #df = df.map(lambda x: x.lower() if isinstance(x, str) else x)
     # Luego, eliminamos las tildes utilizando la librería unidecode
     df = df.map(lambda x: unidecode.unidecode(x) if isinstance(x, str) else x)
     #convertir la fecha a un formato mas legible
     df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')  # 'errors="coerce"' convierte los errores en NaT
     df['fecha'] = df['fecha'].dt.strftime('%d-%m-%Y')  # "01-06-2022"
     #convertir columnas a minuscula
     df.columns = df.columns.str.lower()
     # Luego, eliminamos las tildes utilizando la librería unidecode
     df.columns = df.columns.map(lambda x: unidecode.unidecode(x))
     
     # ahora creamos una columna resumen con la data
     
     def crear_resumen(row):
         partes = []
     
         # Añadir partes de la oración solo si tienen contenido
         if pd.notna(row['nombre_rubrica']) and row['nombre_rubrica'] != '':
             partes.append(f" | Nombre Rubrica: {row['nombre_rubrica']}")
             
         if pd.notna(row['descripcion_rubrica']) and row['descripcion_rubrica'] != '':
             partes.append(f" | Descripcion Rubrica:  {row['descripcion_rubrica']}")
             
         if pd.notna(row['curso_name']) and row['curso_name'] != '':
             partes.append(f" | nombre del curso: {row['curso_name']}")
             
         if pd.notna(row['curso_semester']) and row['curso_semester'] != '':
             partes.append(f" | semestre del curso:  {row['curso_semester']}")
             
         if pd.notna(row['curso_ano']) and row['curso_ano'] != '':
             partes.append(f" | año del curso: {row['curso_ano']}")
             
         if pd.notna(row['fecha']) and row['fecha'] != '':
             partes.append(f" | fecha: {row['fecha']}")
             
         if pd.notna(row['alumno_name']) and row['alumno_name'] != '':
             partes.append(f" | nombre del alumno: {row['alumno_name']}")
     
         if pd.notna(row['promedio_puntajes']) and row['promedio_puntajes'] != '':
             partes.append(f" | promedio puntaje: {row['promedio_puntajes']}")
     
         if pd.notna(row['teacher_name']) and row['teacher_name'] != '':
             partes.append(f" | nombre del profesor: {row['teacher_name']}")
     
     
         
     
         # Unir todas las partes de la oración
         resumen = '. '.join(partes) + '.' if partes else 'Información incompleta o no disponible.'
     
         return resumen
     
     # Aplicar la función al dataframe para crear la columna 'resumen'
     df['resumen'] = df.apply(crear_resumen, axis=1)
     
     # Mostrar el dataframe con la nueva columna 'resumen'
     #print(df[['resumen']])
     
     ####################################################
     """
     # Guardar la columna 'resumen' en un archivo .txt
     with open('resumen.txt', 'w') as file:
         for resumen in df['resumen']:
             file.write(resumen + '\n')  # Añadir cada resumen en una nueva línea
     """        
     ###################################################        
     df_transformer=df
     
     model=SentenceTransformer('distiluse-base-multilingual-cased-v2')
     #model=SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')
     #funcion encode
     def get_embeddings_text(texto):
        return model.encode(texto)
     
     #crear los chunkks
     """
text_splitter = CharacterTextSplitter(
    separator=None,
    chunk_size=560,+
    chunk_overlap=50,
    length_function = len,
    is_separator_regex=False,

)
 

def create_chunks(text):
     textchunk = text_splitter.split_text(text)
     return textchunk

df_transformer["chunks"]=df_transformer["resumen"].apply(create_chunks)
"""
     
     df_transformer["chunks"]=df_transformer["resumen"]
     
     # Eliminar comas, puntos y espacios dobles
     df_transformer['chunks'] = df_transformer['chunks'].apply(lambda x: re.sub(r'[.,]', '', x))  # Eliminar comas y puntos
     df_transformer['chunks'] = df_transformer['chunks'].apply(lambda x: re.sub(r'\s+', ' ', x))  # Reemplazar múltiples espacios por uno solo
     df_transformer['chunks'] = df_transformer['chunks'].apply(lambda x: x.strip())  # Eliminar espacios al principio y al final
     
     # Eliminar posibles espacios extras entre líneas
     df_transformer['chunks'] = df_transformer['chunks'].str.strip()
     
     # Eliminar saltos de línea extra entre palabras
     df_transformer['chunks'] = df_transformer['chunks'].str.replace(r'\n+', '\n', regex=True)
     
     # Mostrar el DataFrame después de la eliminación
     df_transformer["chunks"].head(5)
     #reseteando el index
     chunks_df=df_transformer.explode("chunks").reset_index(drop=True)
     #funcion que codifica
     def get_embeddings(texto):
         return model.encode(texto)
     
     #generar y asignar embeddings a cada chunk del dataframe
     chunks_df["embeddings"]=chunks_df["chunks"].apply(lambda x : get_embeddings(x))
     
     # Convertir los embeddings a listas para guardarlos en un archivo
     chunks_df["embeddings"]=chunks_df["embeddings"].apply(lambda x: x.tolist())
     
     #guartdar los embeddings junto a los chunks
     
     chunks_df.to_pickle("chunks_embeddings.pkl")
     
     #print("chunks y embeddings guardados ")