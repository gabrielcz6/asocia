import streamlit as st
import pandas as pd



def mostrarrubricadecano():

# Datos simulados
   facultades = ['Facultad de Ciencias', 'Facultad de Ingeniería', 'Facultad de Medicina']
   carreras = {
       'Facultad de Ciencias': ['Biología', 'Física', 'Química'],
       'Facultad de Ingeniería': ['Ingeniería Civil', 'Ingeniería de Sistemas', 'Ingeniería Mecánica'],
       'Facultad de Medicina': ['Medicina', 'Enfermería', 'Odontología']
   }
   cursos = {
       'Biología': ['Biología 101', 'Biología 102'],
       'Física': ['Física 101', 'Física 102'],
       'Ingeniería Civil': ['Cálculo 1', 'Estructuras 1'],
       'Medicina': ['Anatomía 1', 'Fisiología 1']
   }
   rubricas = {
       'Biología 101': [
           {'codigo_curso': 'BIO101', 'nombre_curso': 'Biología 101', 'docente': 'Dr. Pérez', 'periodo': '2024-1', 'codigo_alumno': 'A001', 'nombre_alumno': 'Juan Pérez', 'rubrica': 'Informe sobre células: Evaluación Final'},
           {'codigo_curso': 'BIO101', 'nombre_curso': 'Biología 101', 'docente': 'Dr. Pérez', 'periodo': '2024-1', 'codigo_alumno': 'A002', 'nombre_alumno': 'Ana López', 'rubrica': 'Informe sobre células: Evaluación Final'}
       ],
       'Física 101': [
           {'codigo_curso': 'FIS101', 'nombre_curso': 'Física 101', 'docente': 'Dr. García', 'periodo': '2024-1', 'codigo_alumno': 'A003', 'nombre_alumno': 'Carlos González', 'rubrica': 'Examen Final: Física Teórica'},
           {'codigo_curso': 'FIS101', 'nombre_curso': 'Física 101', 'docente': 'Dr. García', 'periodo': '2024-1', 'codigo_alumno': 'A004', 'nombre_alumno': 'Laura Martínez', 'rubrica': 'Examen Final: Física Teórica'}
       ]
   }
   
   # Interfaz de Streamlit
   st.title("Sistema de Rúbricas - Decano")
   
   # Selección de Facultad
   facultad = st.selectbox("Selecciona la Facultad", facultades)
   
   # Selección de Carrera (dependiendo de la Facultad seleccionada)
   carrera = st.selectbox("Selecciona la Carrera", carreras[facultad])
   
   # Selección de Curso (dependiendo de la Carrera seleccionada)
   curso = st.selectbox("Selecciona el Curso", cursos[carrera])
   
   # Mostrar los datos de las rúbricas del curso seleccionado
   if curso in rubricas:
       st.subheader(f"Rúbricas del curso: {curso}")
   
       # Convertir los datos de las rúbricas en un DataFrame para visualización
       rubricas_df = pd.DataFrame(rubricas[curso])
   
       # Mostrar la tabla sin la columna de rúbricas, solo con los datos clave
       st.dataframe(rubricas_df[['codigo_curso', 'nombre_curso', 'docente', 'periodo', 'codigo_alumno', 'nombre_alumno']])
   
       # Al hacer clic en el botón de lupa, mostrar los detalles de la rúbrica
       for index, row in rubricas_df.iterrows():
           if st.button(f"🔍 Ver rúbrica de {row['nombre_alumno']}", key=row['codigo_alumno']):
               st.subheader(f"Detalles de la Rúbrica para {row['nombre_alumno']}")
               st.write(f"**Código del curso**: {row['codigo_curso']}")
               st.write(f"**Nombre del curso**: {row['nombre_curso']}")
               st.write(f"**Docente**: {row['docente']}")
               st.write(f"**Periodo**: {row['periodo']}")
               st.write(f"**Código del alumno**: {row['codigo_alumno']}")
               st.write(f"**Nombre del alumno**: {row['nombre_alumno']}")
               st.write(f"**Rúbrica**: {row['rubrica']}")
   else:
       st.write("No hay rúbricas disponibles para este curso.")
   