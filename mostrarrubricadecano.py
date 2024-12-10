import streamlit as st
import pandas as pd
from db.MongoConnection import MongoConnection



def mostrarrubricadecano():
# Datos simulados
   backend: MongoConnection = st.session_state.backend

   facultades = ['Facultad de Ciencias', 'Facultad de Ingeniería Electrónica e Informática', 'Facultad de Medicina']
   carreras = {
       'Facultad de Ciencias': ['Biología', 'Física', 'Química'],
       'Facultad de Ingeniería Electrónica e Informática': ['Ingeniería de Telecomunicaciones', 'Ingeniería Informática', 'Ingeniería Mecánica'],
       'Facultad de Medicina': ['Medicina', 'Enfermería', 'Odontología']
   }
   cursos = {
       'Biología': ['Biología 101', 'Biología 102'],
       'Física': ['Física 101', 'Física 102'],
       'Ingeniería Informática' : ['Cálculo 1', 'Estructuras 1'],
       'Ingeniería de Telecomunicaciones': ['Anatomía 1', 'Fisiología 1']
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
#    curso = st.selectbox("Selecciona el Curso", cursos[carrera])
   
   # Mostrar los datos de las rúbricas del curso seleccionado
   data = backend.find_documents(collection_name='courses', query= {"faculty" : facultad, "school" : carrera})

   course_names = [course["name"] for course in data]

   # Mostrar el selectbox con los nombres de los cursos
   curso = st.selectbox("Selecciona el Curso", course_names)

   rubrics = []
   print(curso)

   if curso != None:
       rubrics = backend.find_documents(collection_name='rubrics', query= {"course.name" : curso})

   print(rubrics)
       

   if rubrics:
       st.subheader(f"Rúbricas del curso: {curso}")
   
       # Convertir los datos de las rúbricas en un DataFrame para visualización

       rubricas_procesadas = [
        {
            'codigo_curso': rubric['course']['id'],
            'nombre_curso': rubric['course']['name'],
            'docente': str(rubric['teacher_name']),  # Convertimos teacher_id a string
            'periodo': f"{rubric['course']['year']} - Semestre {rubric['course']['semester']}",
            'codigo_alumno': rubric['student']['id'],
            'nombre_alumno': rubric['student']['name'],
            'rubrica' : rubric['rubric']
        }
        for rubric in rubrics
    ]
       rubricas_df = pd.DataFrame(rubricas_procesadas)
   
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
   