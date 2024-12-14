import streamlit as st
from db.MongoConnection import MongoConnection


def evaluacionesScreen():
    # Inicializar backend y cargar datos
    backend: MongoConnection = st.session_state.backend
    data = backend.find_courses_by_user(
        user_id=st.session_state["current_user"]["_id"], include_students=True
    )
    cursos = {
        course["_id"]: {
            "name": course["name"],
            "semester": course["semester"],
            "year": course["year"],
            "students": course["students"],  # Incluye todos los campos de cada estudiante
        }
        for course in data
    }
    opciones_cursos = {
        course_id: f"{details['name']}" for course_id, details in cursos.items()
    }

    # Título de la app
    st.title("Revisa tus Evaluaciones Realizadas")

    # Paso 1: Selección del curso
    curso_seleccionado_id = st.selectbox(
        "Selecciona un curso",
        options=list(opciones_cursos.keys()),
        format_func=lambda x: opciones_cursos[x],
    )
    curso_seleccionado = cursos[curso_seleccionado_id]

    # Filtrar alumnos según el curso seleccionado
    alumnos_disponibles = curso_seleccionado["students"]

    # Crear un diccionario para asociar cada nombre de estudiante con sus datos completos
    alumnos_dict = {student["id"]: student for student in alumnos_disponibles}

    # Preparar las opciones del dropdown de alumnos
    opciones_alumnos = {"": "Elige un alumno"} | {
        student_id: student["name"] for student_id, student in alumnos_dict.items()
    }

    # Mostrar el selectbox para seleccionar un alumno
    alumno_seleccionado_id = st.selectbox(
        "Selecciona un alumno", options=list(opciones_alumnos.keys()), format_func=lambda x: opciones_alumnos[x]
    )

    # Consultar evaluaciones de la base de datos
    evaluaciones_query = {"curso.name": curso_seleccionado["name"]}
    if alumno_seleccionado_id:  # Filtrar por alumno seleccionado si aplica
        evaluaciones_query["alumno.id"] = alumno_seleccionado_id

    evaluaciones = backend.find_documents("evaluations", evaluaciones_query)

    # Mostrar evaluaciones
    st.subheader("Evaluaciones Realizadas")
    if evaluaciones:
        for evaluacion in evaluaciones:
            st.write(f"**Fecha:** {evaluacion['fecha_evaluacion']}")
            st.write(f"**Alumno:** {evaluacion['alumno']['name']}")
            st.write(f"**Rúbrica:** {evaluacion['rubrica']['nombre']}")
            st.write("**Resultados:**")
            for resultado in evaluacion["resultados"]:
                st.write(
                    f"- **{resultado['criterio']}**: {resultado['puntaje']['descripcion']} ({resultado['puntaje']['valor']} pts)"
                )
            st.markdown("---")
    else:
        st.info("No se encontraron evaluaciones.")
