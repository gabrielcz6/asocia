import streamlit as st
import pandas as pd
from db.MongoConnection import MongoConnection





def mostrarrubricadecano():
    # Inicializar la conexión a MongoDB
    backend: MongoConnection = st.session_state.backend

    # Facultades y carreras simuladas
    facultades = [
        'Facultad de Ciencias',
        'Facultad de Ingeniería Electrónica e Informática',
        'Facultad de Medicina'
    ]

    carreras = {
        'Facultad de Ciencias': ['Biología', 'Física', 'Química'],
        'Facultad de Ingeniería Electrónica e Informática': [
            'Ingeniería de Telecomunicaciones',
            'Ingeniería Informática',
            'Ingeniería Mecánica'
        ],
        'Facultad de Medicina': ['Medicina', 'Enfermería', 'Odontología']
    }

    # Interfaz de Streamlit
    st.title("Sistema de Rúbricas - Decano")

    # Selección de Facultad
    # Selección de Facultad
    facultad = st.selectbox("Selecciona la Facultad", facultades)
    if not facultad:
        st.warning("Por favor, selecciona una facultad.")
        return
    print(f"Facultad seleccionada: {facultad}")

    # Selección de Carrera
    # Selección de Carrera
    carrera = st.selectbox("Selecciona la Carrera", carreras[facultad])
    if not carrera:
        st.warning("Por favor, selecciona una carrera.")
        return
    print(f"Carrera seleccionada: {carrera}")

    # Obtener los cursos disponibles para la carrera seleccionada
    # Obtener los cursos disponibles para la carrera seleccionada
    data = backend.find_documents(collection_name='courses', query={"faculty": facultad, "school": carrera})
    if not data:
        st.warning("No se encontraron cursos disponibles para la carrera seleccionada.")
        return    print(f"Datos de cursos encontrados: {data}")

    # Obtener los nombres de los cursos
    course_names = {course["_id"]: course["name"] for course in data}
    print(f"Nombres de los cursos: {course_names}")

    # Selección de Curso
    curso_seleccionado_id = st.selectbox("Selecciona el Curso", list(course_names.keys()), format_func=lambda x: course_names[x])
    curso_seleccionado = course_names[curso_seleccionado_id]
    print(f"Curso seleccionado: {curso_seleccionado}")

    # Filtrar rúbricas por el curso seleccionado
    rubrics = backend.find_documents(
        collection_name='rubrics',
        query={"curso.id": curso_seleccionado_id}
    )
    print(f"Consulta de rúbricas para el curso '{curso_seleccionado}': {rubrics}")

    # Verificar si hay rúbricas disponibles
    if rubrics:
        st.subheader(f"Rúbricas del curso: {curso_seleccionado}")

        # Obtener evaluaciones asociadas a la rúbrica seleccionada
        evaluaciones = backend.find_documents(
            collection_name='evaluations',
            query={"rubrica.curso.id": curso_seleccionado_id}
        )
        print(f"Evaluaciones encontradas: {evaluaciones}")

        # Listar alumnos que tienen evaluaciones con esta rúbrica
        alumnos = {"": "Seleccionar un alumno"} | {
            eval['alumno']['id']: eval['alumno']['name'] for eval in evaluaciones
        }
        print(f"Alumnos con evaluaciones: {alumnos}")

        # Seleccionar un alumno
        alumno_seleccionado_id = st.selectbox(
            "Selecciona un alumno",
            options=list(alumnos.keys()),
            format_func=lambda x: alumnos[x]
        )
        print(f"Alumno seleccionado ID: {alumno_seleccionado_id}")

        # Filtrar las evaluaciones basadas en el alumno seleccionado
        if alumno_seleccionado_id == "todos" or alumno_seleccionado_id == "":
            evaluaciones_a_mostrar = evaluaciones
        else:
            evaluaciones_a_mostrar = [eval for eval in evaluaciones if eval['alumno']['id'] == alumno_seleccionado_id]

        # Mostrar evaluaciones con el mismo estilo que evaluacionesScreen
        if evaluaciones_a_mostrar:
            html_posts = generar_posts_rubricas(evaluaciones_a_mostrar, showCourse=True)
            st.components.v1.html(html_posts, height=600, scrolling=True)
        else:
            st.warning("No se encontraron evaluaciones para la selección actual.")
    else:
        st.warning("No se encontraron rúbricas asociadas a este curso.")




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



def mostrarrubricadecano2():
    # Inicializar la conexión a MongoDB
    backend: MongoConnection = st.session_state.backend

    # Facultades y carreras simuladas
    facultades = [
        'Facultad de Ciencias',
        'Facultad de Ingeniería Electrónica e Informática',
        'Facultad de Medicina'
    ]

    carreras = {
        'Facultad de Ciencias': ['Biología', 'Física', 'Química'],
        'Facultad de Ingeniería Electrónica e Informática': [
            'Ingeniería de Telecomunicaciones',
            'Ingeniería Informática',
            'Ingeniería Mecánica'
        ],
        'Facultad de Medicina': ['Medicina', 'Enfermería', 'Odontología']
    }

    # Interfaz de Streamlit
    st.title("Sistema de Rúbricas - Decano")

    # Selección de Facultad
    facultad = st.selectbox("Selecciona la Facultad", facultades)
    if not facultad:
        st.warning("Por favor, selecciona una facultad.")
        return

    # Selección de Carrera
    carrera = st.selectbox("Selecciona la Carrera", carreras[facultad])
    if not carrera:
        st.warning("Por favor, selecciona una carrera.")
        return

    # Obtener los cursos disponibles para la carrera seleccionada
    data = backend.find_documents(collection_name='courses', query={"faculty": facultad, "school": carrera})
    if not data:
        st.warning("No se encontraron cursos disponibles para la carrera seleccionada.")
        return

    # Obtener los nombres de los cursos
    course_names = {course["_id"]: course["name"] for course in data}

    # Selección de Curso
    curso_seleccionado_id = st.selectbox("Selecciona el Curso", list(course_names.keys()), format_func=lambda x: course_names[x])
    curso_seleccionado = course_names[curso_seleccionado_id]

    # Filtrar rúbricas por el curso seleccionado
    rubrics = backend.find_documents(
        collection_name='rubrics',
        query={"curso.id": curso_seleccionado_id}
    )

    if not rubrics:
        st.warning("No se encontraron rúbricas asociadas a este curso.")
        return

    # Obtener evaluaciones asociadas a las rúbricas seleccionadas
    evaluaciones = backend.find_documents(
        collection_name='evaluations',
        query={"rubrica.curso.id": curso_seleccionado_id}
    )

    if not evaluaciones:
        st.warning("No se encontraron evaluaciones para este curso.")
        return

    # Calcular estadísticas para cada rúbrica
    rubrica_stats = []
    for rubrica in rubrics:
        rubrica_id = rubrica["_id"]
        rubrica_nombre = rubrica["nombre"]

        # Filtrar evaluaciones para esta rúbrica
        evals_rubrica = [eval for eval in evaluaciones if eval['rubrica']['_id'] == rubrica_id]

        total_alumnos = len(evals_rubrica)
        aprobados = sum(1 for eval in evals_rubrica if all(int(resultado['puntaje']['valor']) >= 3 for resultado in eval['resultados']))
        desaprobados = total_alumnos - aprobados

        rubrica_stats.append({
            "Rúbrica": rubrica_nombre,
            "Total de Alumnos Evaluados": total_alumnos,
            "Aprobados": aprobados,
            "Desaprobados": desaprobados
        })

    # Convertir estadísticas a un DataFrame
    df_rubrica_stats = pd.DataFrame(rubrica_stats)

    # Mostrar las estadísticas en una tabla
    st.subheader(f"Resumen de Rúbricas para el Curso: {curso_seleccionado}")
    st.dataframe(df_rubrica_stats)

