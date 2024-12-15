import streamlit as st
from db.MongoConnection import MongoConnection

def evaluacionesScreen():
    # Inicializar backend y cargar datos
    backend: MongoConnection = st.session_state.backend
    data = backend.find_courses_by_user(
        user_id=st.session_state["current_user"]["_id"], include_students=True
    )
    
    # Crear diccionario de cursos
    cursos = {
        course["_id"]: {
            "name": course["name"],
            "semester": course["semester"],
            "year": course["year"],
            "students": course["students"],  # Incluye todos los campos de cada estudiante
        }
        for course in data
    }

    # Preparar opciones del dropdown de cursos
    opciones_cursos = {"": "Seleccione un curso"} | {
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

    # Consultar evaluaciones según el curso seleccionado
    evaluaciones_query = {}
    curso_seleccionado = None
    if curso_seleccionado_id:  # Si se selecciona un curso válido
        curso_seleccionado = cursos[curso_seleccionado_id]
        evaluaciones_query["curso.name"] = curso_seleccionado["name"]
        alumnos_disponibles = curso_seleccionado["students"]
    else:  # Si no se selecciona un curso, mostrar todos los datos
        alumnos_disponibles = []

    # Crear diccionario de alumnos si se seleccionó un curso
    alumnos_dict = {student["id"]: student for student in alumnos_disponibles}

    # Mostrar dropdown de alumnos solo si hay un curso seleccionado
    alumno_seleccionado_id = ""
    if curso_seleccionado_id:
        opciones_alumnos = {"": "Elige un alumno"} | {
            student_id: student["name"] for student_id, student in alumnos_dict.items()
        }
        alumno_seleccionado_id = st.selectbox(
            "Selecciona un alumno",
            options=list(opciones_alumnos.keys()),
            format_func=lambda x: opciones_alumnos[x],
        )

    # Filtrar evaluaciones por alumno si corresponde
    if alumno_seleccionado_id:
        evaluaciones_query["alumno.id"] = alumno_seleccionado_id

    # Consultar las evaluaciones en la base de datos
    evaluaciones = backend.find_documents("evaluations", evaluaciones_query)

    st.divider()

    # Cambiar el encabezado dinámicamente según la selección
    if alumno_seleccionado_id:
        # No mostrar título si se seleccionó un alumno
        pass
    elif curso_seleccionado_id:
        st.subheader(f"Evaluaciones del Curso: {curso_seleccionado['name']}")
    else:
        st.subheader("Últimas Publicaciones!!")

    # Mostrar evaluaciones
    if evaluaciones:
        for evaluacion in evaluaciones:
            st.write(f"**Fecha:** {evaluacion['fecha_evaluacion']}")
            if not curso_seleccionado_id:  # Mostrar el curso solo si no se seleccionó uno
                st.write(f"**Curso:** {evaluacion['curso']['name']}")
            st.write(f"**Alumno:** {evaluacion['alumno']['name']}")
            st.write(f"**Rúbrica:** {evaluacion['rubrica']['nombre']}")
            st.write("**Resultados:**")
            for resultado in evaluacion["resultados"]:
                st.write(
                    f"- **{resultado['criterio']}**: {resultado['puntaje']['descripcion']} ({resultado['puntaje']['valor']} pts)"
                )
                puntajes_posibles = evaluacion["rubrica"]["criterios"]
                for criterio in puntajes_posibles:
                    if criterio["nombre"] == resultado["criterio"]:
                        st.write("  **Puntajes posibles:**")
                        for puntaje in criterio["puntajes"]:
                            st.write(
                                f"    - {puntaje['descripcion']} ({puntaje['valor']} pts)"
                            )
            st.markdown("---")
    else:
        st.info("No se encontraron evaluaciones.")
