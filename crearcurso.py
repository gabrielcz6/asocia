
import streamlit as st
import pandas as pd

def crearcurso():
  

   # Simulación de bases de datos (esto puede ser reemplazado por una consulta real a la BD)
   # Aquí estamos simulando los datos con pandas. 
   # En un caso real, usarías consultas a la base de datos.
   
   # Datos de ejemplo (normalmente obtendrás esto desde tu BD)
   cursos_bd = pd.DataFrame({
       'id': [1, 2, 3],
       'nombre': ['Matemáticas', 'Física', 'Historia']
   })
   
   semestres_bd = pd.DataFrame({
       'id': [1, 2],
       'semestre': ['2024-I', '2024-II']
   })
   
   profesores_bd = pd.DataFrame({
       'id': [1, 2, 3],
       'nombre': ['Juan Pérez', 'Ana López', 'Carlos Gómez']
   })
   
   # Título de la aplicación
   st.title('Crear Nuevo Curso')
   
   # Campo de código de curso
   codigo_curso = st.text_input("Código del curso")
   
   # Campo de selección de nombre del curso (con opción para registrar nuevo curso)
   curso_opciones = cursos_bd['nombre'].tolist() + ['Registrar nuevo curso']
   curso_seleccionado = st.selectbox('Nombre del Curso', curso_opciones)
   
   # Si seleccionan "Registrar nuevo curso", pedir el nombre del curso
   if curso_seleccionado == 'Registrar nuevo curso':
       nuevo_curso = st.text_input("Nuevo nombre del curso")
       if nuevo_curso:
           # Aquí puedes agregar el código para registrar el nuevo curso en la BD.
           st.write(f'Curso "{nuevo_curso}" registrado con éxito.')
           # Se añade a la lista de cursos (esto es solo un ejemplo para reflejar el comportamiento)
           cursos_bd = cursos_bd.append({'id': len(cursos_bd) + 1, 'nombre': nuevo_curso}, ignore_index=True)
   else:
       nuevo_curso = curso_seleccionado
   
   # Campo de semestre
   semestre_opciones = semestres_bd['semestre'].tolist()
   semestre_seleccionado = st.selectbox('Semestre', semestre_opciones)
   
   # Campo de profesor
   profesor_opciones = profesores_bd['nombre'].tolist()
   profesor_seleccionado = st.selectbox('Profesor', profesor_opciones)
   
   # Botón para guardar
   if st.button('Guardar Curso'):
       if not codigo_curso or not nuevo_curso or not semestre_seleccionado or not profesor_seleccionado:
           st.error("Todos los campos son obligatorios.")
       else:
           # Aquí debes agregar el código para guardar estos datos en tu base de datos.
           st.success(f'Curso "{nuevo_curso}" ({codigo_curso}) creado con éxito para el semestre {semestre_seleccionado}, impartido por {profesor_seleccionado}.')
   