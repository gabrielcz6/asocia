import streamlit as st
from db.MongoConnection import MongoConnection
import pandas as pd

def rubrica():
    # Datos de ejemplo: Cursos y alumnos asociados
    backend: MongoConnection = st.session_state.backend
    data = backend.find_courses_by_user(user_id=st.session_state["current_user"]["_id"], include_students=True)
    print("printando data del be", data)
    # df = pd.DataFrame(data, dtype="object")
    # df.rename(columns={'_id': 'Código', 'name': 'Asignatura', 'semester': 'Semestre', 'year': 'Año'}, inplace=True)
    
    # cursos = {
    #     "Matemáticas": ["Juan Pérez", "Ana Gómez", "Carlos López"],
    #     "Ciencias": ["María Rodríguez", "Luis Torres", "Pablo Sánchez"],
    #     "Literatura": ["Laura Fernández", "Ricardo Pérez", "Claudia Díaz"]
    # }

    cursos = {}
    for course in data:
        course_name = course["name"]
        students_names = [student["name"] for student in course["students"]]
        cursos[course_name] = students_names
    
    print("printeando luego de acomodar", cursos)
    # Simulación de una base de datos con las rúbricas almacenadas
    # (Este diccionario simula los datos que podrían venir de una BD)
    bd_simulada = {
        "Juan Pérez": "Rúbrica de ejemplo para Juan Pérez.",
        "María Rodríguez": "Rúbrica de ejemplo para María Rodríguez.",
        "Laura Fernández": "Rúbrica de ejemplo para Laura Fernández."
    }

    # Función para predecir el nombre del alumno según lo que se escribe
    def filtrar_alumnos(alumnos, query):
        return [alumno for alumno in alumnos if query.lower() in alumno.lower()]
    
    # Título de la app
    st.title("Creación de Rúbrica para Alumnos")
    
    # Paso 1: Selección del curso
    curso_seleccionado = st.selectbox("Selecciona un curso", list(cursos.keys()))
    
    # Paso 2: Filtrar alumnos según el curso elegido
    alumnos_disponibles = cursos[curso_seleccionado]
    
    # Mostramos los alumnos filtrados en un desplegable
    alumno_seleccionado = st.selectbox("Selecciona un alumno", alumnos_disponibles)
    
    # Paso 3: Verificar si hay una rúbrica ya guardada para este alumno en la "BD"
    if alumno_seleccionado in bd_simulada:
        rubrica_actual = bd_simulada[alumno_seleccionado]
        # Inicializamos un estado de edición
        if 'editarrubrica' not in st.session_state:
            st.session_state.editarrubrica = False
        
        # Si estamos en modo edición, mostramos un text_area editable, si no, mostramos solo lectura
        if st.session_state.editarrubrica:
            rubrica = st.text_area("Edita la rúbrica para el alumno seleccionado", value=rubrica_actual, height=200)
        else:
            st.text_area("Rúbrica actual (solo lectura)", value=rubrica_actual, height=200, disabled=True)
        
        # Botón para editar la rúbrica
        if not st.session_state.editarrubrica:
            if st.button("Editar Rúbrica"):
                st.session_state.editarrubrica = True
                st.rerun()  # Recargar la página para habilitar la edición
        else:
            # Botón para guardar la rúbrica editada
            if st.button("Guardar Rúbrica"):
                if rubrica.strip():  # Verificamos que no esté vacía
                    bd_simulada[alumno_seleccionado] = rubrica
                    st.session_state.editarrubrica = False  # Deshabilitar edición después de guardar
                    st.success(f"Rúbrica guardada para {alumno_seleccionado}")
                    st.rerun() 
                else:
                    st.warning("La rúbrica no puede estar vacía.")
                    st.rerun() 
    else:
        rubrica = st.text_area("Escribe la rúbrica para el alumno seleccionado", height=200)
        
        # Botón para guardar la nueva rúbrica
        if st.button("Guardar Rúbrica"):
            if rubrica.strip():  # Verificamos que no esté vacía
                bd_simulada[alumno_seleccionado] = rubrica
                st.success(f"Rúbrica guardada para {alumno_seleccionado}")
            else:
                st.warning("La rúbrica no puede estar vacía.")
    
    # Mostrar la información final
    if alumno_seleccionado in bd_simulada:
        st.write(f"Rúbrica para {alumno_seleccionado}:")
        st.write(bd_simulada[alumno_seleccionado])

