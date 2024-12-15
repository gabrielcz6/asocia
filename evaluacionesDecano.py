import streamlit as st
from db.MongoConnection import MongoConnection
from streamlit.components.v1 import html as st_html

def evaluacionesDecano():
    # Inicializar backend y cargar datos
    backend: MongoConnection = st.session_state.backend
    

    evaluaciones_query = {}

    evaluaciones = backend.find_documents("evaluations", evaluaciones_query)

    # st.divider()

    st.subheader("Últimas Publicaciones")

    # Mostrar evaluaciones
    if evaluaciones:
        html_posts = generar_posts_rubricas(evaluaciones, showCourse=True)
        st.components.v1.html(html_posts, height=600, scrolling=True)
    else:
        st.info("No se encontraron evaluaciones.")


from datetime import datetime

import base64

def generar_posts_rubricas(evaluaciones, showCourse=True):
    # HTML y estilos para mostrar las rúbricas como posts
    html = """
    <style>
        .post-container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
        }
        .post {
            background-color: #FFFFFF; /* Fondo blanco */
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 15px;
            width: 285px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .post-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
        }
        .post-header img {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            object-fit: cover;
        }
        .post-header .teacher-info {
            display: flex;
            flex-direction: column;
        }
        .post-header .teacher-info p {
            margin: 0;
            font-size: 14px;
            color: #555;
        }
        .post h4 {
            margin: 0;
            font-size: 18px;
            color: #333;
            background-color: #f5f5f5; /* Fondo resaltado */
            padding: 5px;
            border-radius: 5px;
        }
        .post p {
            margin: 5px 0;
            font-size: 14px;
            color: #555;
        }
        .azul {
            color: #007BFF; /* Texto resaltado en azul */
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
            /*color: #333;  Color de texto para puntajes */
        }
        .post .puntajes ul li strong {
            /*color: #28A745;  Resaltar en verde los posibles puntajes */
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

        # Convertir la imagen base64 a un formato que el tag <img> pueda renderizar
        teacher_img_src = f"{evaluacion['teacher_img']}" if 'teacher_img' in evaluacion else "https://media.istockphoto.com/id/1300845620/vector/user-icon-flat-isolated-on-white-background-user-symbol-vector-illustration.jpg?s=612x612&w=0&k=20&c=yBeyba0hUkh14_jgv1OKqIH0CCSWU_4ckRkAoy2p73o="

        total_obtenido = 0
        total_maximo = 0

        html += f"""
        <div class="post">
            <div class="post-header">
                <img src="{teacher_img_src}" alt="Foto del profesor">
                <div class="teacher-info">
                    <p style="color: #007BFF;"><strong>{evaluacion['teacher_name']}</strong></p>
                    <p>{fecha_formateada}</p>
                </div>
            </div>
            <h4>{evaluacion['rubrica']['nombre'].upper()}</h4>
            <p><strong>Curso:</strong> {evaluacion['curso']['name']}</p>
            <p><strong>Alumno:</strong> {evaluacion['alumno']['name']}</p>
        """

        html += "<div class=\"puntajes\">"
        html += "<strong>Resultados:</strong>"

        for idx, resultado in enumerate(evaluacion["resultados"], start=1):
            total_obtenido += float(resultado['puntaje']['valor'])
            for criterio in evaluacion["rubrica"]["criterios"]:
                if criterio["nombre"] == resultado["criterio"]:
                    total_maximo += max(float(p["valor"]) for p in criterio["puntajes"])

            html += f"""
                <p><strong>{idx}. {resultado['criterio']}</strong>: <span >{resultado['puntaje']['descripcion']} ({resultado['puntaje']['valor']} pts)</span></p>
                <p style="margin-left: 20px;"><strong>Posibles puntajes:</strong></p>
                <ul>
            """
            for criterio in evaluacion["rubrica"]["criterios"]:
                if criterio["nombre"] == resultado["criterio"]:
                    for puntaje in criterio["puntajes"]:
                        html += f"<li><strong>{puntaje['descripcion']}</strong> ({puntaje['valor']} pts)</li>"
            html += "</ul>"

        html += f"</div><p style='text-align: right;'><strong>Puntuación Final:</strong> <span >{total_obtenido}/{total_maximo} pts</span></p></div>"

    html += "</div>"
    return html
