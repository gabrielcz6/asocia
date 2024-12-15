import streamlit as st
from db.MongoConnection import MongoConnection
from streamlit.components.v1 import html as st_html

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
        st.subheader("Mis Últimas Publicaciones")

    # Mostrar evaluaciones
    if evaluaciones:
        if curso_seleccionado_id:
            html_posts = generar_posts_rubricas(evaluaciones, showCourse=False)
        else:
            html_posts = generar_posts_rubricas(evaluaciones, showCourse=True)
        st.components.v1.html(html_posts, height=600, scrolling=True)
        # for evaluacion in evaluaciones:
            
        #     st.markdown("---")
    else:
        st.info("No se encontraron evaluaciones.")

from datetime import datetime

from datetime import datetime

from datetime import datetime

def generar_posts_rubricas(evaluaciones, showCourse=True):
    # HTML y estilos para mostrar las rúbricas como posts
    html = """
    <style>
        .post-container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: flex-start;
        }
        .post {
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 15px;
            width: 300px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .post h4 {
            margin: 0 0 10px;
            font-size: 18px;
            color: #333;
        }
        .post p {
            margin: 5px 0;
            font-size: 14px;
            color: #555;
        }
        .post .puntajes {
            margin-top: 10px;
            font-size: 12px;
            color: #777;
        }
        .post .puntajes ul {
            padding-left: 30px;
            margin: 5px 0;
        }
        .post .puntajes ul li {
            margin-bottom: 5px;
        }
    </style>
    <div class="post-container">
    """

    for evaluacion in evaluaciones:
        # Formatear la fecha
        if isinstance(evaluacion['fecha_evaluacion'], datetime):
            fecha_formateada = evaluacion['fecha_evaluacion'].strftime("%d/%m/%Y %H:%M")
        else:
            fecha_formateada = datetime.strptime(evaluacion['fecha_evaluacion'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%d/%m/%Y %H:%M")

        html += f"""
        <div class="post">
            <h4>{evaluacion['rubrica']['nombre'].upper()}</h4>
            <p><strong>Alumno:</strong> {evaluacion['alumno']['name']}</p>
            <p><strong>Fecha:</strong> {fecha_formateada}</p>
        """
        if showCourse:
            html += f"<p><strong>Curso:</strong> {evaluacion['curso']['name']}</p>"

        html += "<div class=\"puntajes\">"
        html += "<strong>Resultados:</strong>"

        for idx, resultado in enumerate(evaluacion["resultados"], start=1):
            html += f"""
                <p><strong>{idx}. {resultado['criterio']}</strong>: {resultado['puntaje']['descripcion']} ({resultado['puntaje']['valor']} pts)</p>
                <p style="margin-left: 20px;"><strong>Posibles puntajes:</strong></p>
                <ul>
            """
            for criterio in evaluacion["rubrica"]["criterios"]:
                if criterio["nombre"] == resultado["criterio"]:
                    for puntaje in criterio["puntajes"]:
                        html += f"<li>{puntaje['descripcion']} ({puntaje['valor']} pts)</li>"
            html += "</ul>"

        html += "</div></div>"

    html += "</div>"
    return html
