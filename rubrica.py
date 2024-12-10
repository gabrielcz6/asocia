import streamlit as st
from db.MongoConnection import MongoConnection
import pandas as pd

def rubrica():
    # Datos de ejemplo: Cursos y alumnos asociados
    backend: MongoConnection = st.session_state.backend
    data = backend.find_courses_by_user(user_id=st.session_state["current_user"]["_id"], include_students=True)

    cursos = {
    course["_id"]: {
        "name": course["name"],
        "semester": course["semester"],
        "year": course["year"],
        "students": course["students"]  # Incluye todos los campos de cada estudiante
    }
    for course in data
}

    opciones_cursos = {course_id: f"{details['name']}"
                   for course_id, details in cursos.items()}
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
    
    curso_seleccionado_id = st.selectbox(
        "Selecciona un curso",
        options=list(opciones_cursos.keys()),
        format_func=lambda x: opciones_cursos[x]
    )
    
    # Paso 1: Selección del curso
    curso_seleccionado = cursos[curso_seleccionado_id]
    # curso_seleccionado = st.selectbox("Selecciona un curso", list(cursos.keys()))
    

    # Paso 2: Filtrar alumnos según el curso elegido
    alumnos_disponibles = curso_seleccionado["students"]

    # Crear un diccionario para asociar cada nombre de estudiante con sus datos completos
    alumnos_dict = {
        student["id"]: student
        for student in alumnos_disponibles
    }

    # Preparar las opciones para el selectbox con un formato legible
    opciones_alumnos = {
        student_id: student["name"]
        for student_id, student in alumnos_dict.items()
    }

    # Mostrar el selectbox con los nombres de los estudiantes
    alumno_seleccionado_id = st.selectbox(
        "Selecciona un alumno",
        options=list(opciones_alumnos.keys()),
        format_func=lambda x: opciones_alumnos[x]
    )

    # Obtener los datos completos del alumno seleccionado
    alumno_seleccionado = alumnos_dict[alumno_seleccionado_id]

    
    # Paso 3: Verificar si hay una rúbrica ya guardada para este alumno en la "BD"
    if alumno_seleccionado["name"] in bd_simulada:
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
                if backend.save_rubric(student=alumno_seleccionado,course=curso_seleccionado,rubric=rubrica, course_id=curso_seleccionado_id):
                # bd_simulada[alumno_seleccionado["name"]] = rubrica
                    st.success(f"Rúbrica guardada para {alumno_seleccionado["name"]}")
                else:
                    st.error(f"Rúbrica no guardada para {alumno_seleccionado["name"]}")
            else:
                st.warning("La rúbrica no puede estar vacía.")
    
    # Mostrar la información final
    if alumno_seleccionado["name"] in bd_simulada:
        st.write(f"Rúbrica para {alumno_seleccionado}, {curso_seleccionado}:")
        st.write(bd_simulada[alumno_seleccionado["name"]])

