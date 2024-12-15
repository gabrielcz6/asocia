import datetime
import itertools
import streamlit as st
from db.MongoConnection import MongoConnection
import pandas as pd
import json
import utils.funcionespredefinidadisplay
from bson.objectid import ObjectId



def evaluacion_rubrica():
    # Datos de ejemplo: Cursos y alumnos asociados
    backend: MongoConnection = st.session_state.backend
    data = backend.find_courses_by_user(user_id=st.session_state["current_user"]["_id"], include_students=True)
    rubricas_del_profe = backend.find_documents("rubrics", {"teacher_id" : st.session_state["current_user"]["_id"]})
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


    # Título de la app
    st.title("Evaluar Alumno")
    
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
    # Filtrar las rúbricas asociadas al curso seleccionado
    rubricas_filtradas = [
        rubrica for rubrica in rubricas_del_profe if rubrica["curso"]["id"] == curso_seleccionado_id
    ]

    # Preparar nombres de las rúbricas para el selectbox
    rubrica_nombres = ["Elige una rúbrica"] + [rubrica["nombre"] for rubrica in rubricas_filtradas]

    if "success_message" not in st.session_state:
        st.session_state.success_message = ""

        
    # Dropdown de selección de rúbrica
    selected_rubrica_nombre = st.selectbox(
        "Seleccione la rúbrica a evaluar:",
        rubrica_nombres,
        key="rubrica_dropdown"
    )

    # Mostrar evaluación solo si se selecciona una rúbrica válida
    if selected_rubrica_nombre != "Elige una rúbrica":
        selected_rubrica = next(rubrica for rubrica in rubricas_del_profe if rubrica["nombre"] == selected_rubrica_nombre)

        st.title(f"Evaluación: {selected_rubrica['nombre']}")
        st.write(f"Docente: {selected_rubrica['teacher_name']}")
        st.write(f"Descripción: {selected_rubrica['descripcion']}")

        # Interfaz de evaluación
        resultados = []
        criterios = selected_rubrica["criterios"]
        rows = itertools.zip_longest(*(iter(criterios),) * 2)  # Agrupa los criterios de 2 en 2

        for row in rows:
            cols = st.columns([1, 0.1, 1])  # Ajusta el espacio entre columnas
            for col, criterio in zip([cols[0], cols[2]], row):
                if criterio:  # Asegura que no haya iteraciones nulas
                    with col:
                        st.subheader(criterio["nombre"])
                        puntaje = st.radio(
                            "Seleccione un puntaje:",
                            options=criterio["puntajes"],
                            format_func=lambda x: f"{x['descripcion']} - {x['valor']} pts",
                            key=f"criterio_{criterio['nombre']}",
                        )
                        resultados.append({"criterio": criterio["nombre"], "puntaje": puntaje})

        # Guardar la evaluación
        if st.button("Guardar evaluación"):
            evaluacion = {
                "rubrica": selected_rubrica,
                "curso": curso_seleccionado,
                "fecha_evaluacion": datetime.datetime.now(),
                "teacher_id": selected_rubrica["teacher_id"],
                "teacher_name": selected_rubrica["teacher_name"],
                "alumno": alumno_seleccionado,
                "resultados": resultados,
            }

            result = backend.save_document(collection_name="evaluations", document=evaluacion)

            if result:
                st.success("Evaluación guardada exitosamente.")
                st.session_state.success_message = "Evaluación guardada exitosamente."
                st.rerun()  # Recargar la interfaz
            else:
                st.error("Error al guardar la evaluación.")

    # Mostrar mensaje de éxito si existe
    if st.session_state.success_message:
        st.success(st.session_state.success_message)
        st.session_state.success_message = ""



def crear_rubrica_v2():
    st.title("Crear Rúbrica V2")

    # Inicializar la conexión a MongoDB (Simulación aquí)
    backend: MongoConnection = st.session_state.backend

    # Obtener los cursos del docente
    data = backend.find_courses_by_user(user_id=st.session_state["current_user"]["_id"], include_students=True)
    cursos = {
        course["_id"]: {
            "name": course["name"],
            "semester": course["semester"],
            "year": course["year"],
            "students": course["students"]
        }
        for course in data
    }

    opciones_cursos = {
        course_id: f"{details['name']} - {details['semester']} ({details['year']})"
        for course_id, details in cursos.items()
    }

    # Selección de curso
    st.subheader("Seleccionar Curso")
    curso_seleccionado_id = st.selectbox(
        "Selecciona un curso para asociar a esta rúbrica",
        options=list(opciones_cursos.keys()),
        format_func=lambda x: opciones_cursos[x]
    )   
    curso_seleccionado = cursos[curso_seleccionado_id]

    # Agregar estilos CSS personalizados
    st.markdown(
        """
        <style>
        /* Estilo para inputs numéricos */
        div[data-testid="stNumberInputContainer"] {
            width: 120px !important;
            font-size: 14px;
        }

        /* Estilo para inputs de texto */
        div[data-testid="stTextInput"] input {
            font-size: 14px;
        }

        /* Estilo para text areas */
        div[data-testid="stTextArea"] textarea {
            font-size: 14px;
        }

        /* Estilo para subencabezados */
        h2 {
            color: #1f77b4;
        }

        /* Reducir el margen de los expanders */
        .streamlit-expander {
            margin-bottom: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Inicializar el estado para número de criterios
    if "num_criterios" not in st.session_state:
        st.session_state.num_criterios = 1

    # Control de la rúbrica (nombre y descripción)
    st.subheader("Información de la Rúbrica")
    nombre_rubrica = st.text_input("Nombre de la Rúbrica", max_chars=100)
    descripcion_rubrica = st.text_area("Descripción de la Rúbrica (opcional)", height=100)

    # Control del número de criterios
    st.subheader("Criterios")
    num_criterios = st.number_input(
        "Número de Criterios",
        min_value=1,
        max_value=10,
        step=1,
        value=st.session_state.num_criterios,
        key="num_criterios_input"
    )

    # Si el valor cambia, actualiza el estado
    if num_criterios != st.session_state.num_criterios:
        st.session_state.num_criterios = num_criterios
        st.rerun()

    # Campos para criterios
    criterios = []
    for i in range(int(st.session_state.num_criterios)):
        with st.expander(f"Criterio {i + 1}", expanded=True):
            nombre_criterio = st.text_input(f"Nombre del Criterio", key=f"nombre_criterio_{i}")

            # Control del número de puntajes
            if f"num_puntajes_{i}" not in st.session_state:
                st.session_state[f"num_puntajes_{i}"] = 5

            num_puntajes = st.number_input(
                f"Número de Puntajes para el Criterio",
                min_value=1,
                max_value=10,
                step=1,
                value=st.session_state[f"num_puntajes_{i}"],
                key=f"num_puntajes_input_{i}"
            )

            if num_puntajes != st.session_state[f"num_puntajes_{i}"]:
                st.session_state[f"num_puntajes_{i}"] = num_puntajes
                st.rerun()

            # Campos para puntajes
            puntajes = []
            for j in range(int(st.session_state[f"num_puntajes_{i}"])):
                col1, col2 = st.columns([4, 1])

                with col1:
                    puntaje_descripcion = st.text_area(
                        f"Etiqueta o descripción del Puntaje {j + 1}",
                        key=f"puntaje_descripcion_{i}_{j}",
                        height=68 , # Puedes ajustar la altura inicial según necesites
                        value=utils.funcionespredefinidadisplay.obtener_descripcion_puntaje(j),
                        
                           
                    )

                with col2:
                    puntaje_valor = st.text_input(
                    f"Valor del Puntaje {j + 1}",
                    key=f"puntaje_valor_{i}_{j}",
                    placeholder="Numérico",
                    value=j+1
                )
                
                if puntaje_valor:
                    try:
                        puntaje_valor_float = float(puntaje_valor)  # Convertir a flotante
                        if puntaje_valor_float < 0.0:
                            st.error("El valor debe ser mayor o igual a 0.0.")
                            puntaje_valor_float = None  # Invalidar el valor
                    except ValueError:
                        st.error("Por favor, ingresa un número válido.")
                        puntaje_valor_float = None
                else:
                    puntaje_valor_float = None

                puntajes.append({
                    "valor": puntaje_valor,
                    "descripcion": puntaje_descripcion
                })

            # Añadir el criterio a la lista de criterios
            criterios.append({
                "nombre": nombre_criterio,
                "puntajes": puntajes
            })

    # Botón de guardar (simulando el envío de un formulario)
    if st.button("Guardar Rúbrica"):
        if nombre_rubrica and all(c["nombre"] for c in criterios):
            # Crear el documento para la base de datos
            nueva_rubrica = {
                "nombre": nombre_rubrica,
                "descripcion": descripcion_rubrica,
                "criterios": criterios,
                "teacher_id": st.session_state["current_user"]["_id"],
                "teacher_name": st.session_state["current_user"]["fullname"],
                "curso": {
                    "id": curso_seleccionado_id,
                    "name": curso_seleccionado["name"],
                    "semester": curso_seleccionado["semester"],
                    "year": curso_seleccionado["year"]
                }
            }
            print(nueva_rubrica)
            
            # Guardar en la base de datos
            result = backend.save_document("rubrics", nueva_rubrica)

            if result:
                st.success(f"Rúbrica '{nombre_rubrica}' guardada exitosamente.")
            else:
                st.error("Error al guardar la rúbrica.")
        else:
            st.warning("Por favor, completa todos los campos obligatorios.")
            

def crear_rubrica_generic():
    st.title("Crear Rúbrica para los profesores")

    # Inicializar la conexión a MongoDB (Simulación aquí)
    backend: MongoConnection = st.session_state.backend

    # Agregar estilos CSS personalizados
    st.markdown(
        """
        <style>
        /* Estilo para inputs numéricos */
        div[data-testid="stNumberInputContainer"] {
            width: 120px !important;
            font-size: 14px;
        }

        /* Estilo para inputs de texto */
        div[data-testid="stTextInput"] input {
            font-size: 14px;
        }

        /* Estilo para text areas */
        div[data-testid="stTextArea"] textarea {
            font-size: 14px;
        }

        /* Estilo para subencabezados */
        h2 {
            color: #1f77b4;
        }

        /* Reducir el margen de los expanders */
        .streamlit-expander {
            margin-bottom: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Inicializar el estado para número de criterios
    if "num_criterios" not in st.session_state:
        st.session_state.num_criterios = 1

    # Control de la rúbrica (nombre y descripción)
    st.subheader("Información de la Rúbrica")
    nombre_rubrica = st.text_input("Nombre de la Rúbrica", max_chars=100)
    descripcion_rubrica = st.text_area("Descripción de la Rúbrica (opcional)", height=100)

    # Control del número de criterios
    st.subheader("Criterios")
    num_criterios = st.number_input(
        "Número de Criterios",
        min_value=1,
        max_value=10,
        step=1,
        value=st.session_state.num_criterios,
        key="num_criterios_input"
    )

    # Si el valor cambia, actualiza el estado
    if num_criterios != st.session_state.num_criterios:
        st.session_state.num_criterios = num_criterios
        st.rerun()

    # Campos para criterios
    criterios = []
    for i in range(int(st.session_state.num_criterios)):
        with st.expander(f"Criterio {i + 1}", expanded=True):
            nombre_criterio = st.text_input(f"Nombre del Criterio", key=f"nombre_criterio_{i}")

            # Control del número de puntajes
            if f"num_puntajes_{i}" not in st.session_state:
                st.session_state[f"num_puntajes_{i}"] = 5

            num_puntajes = st.number_input(
                f"Número de Puntajes para el Criterio",
                min_value=1,
                max_value=10,
                step=1,
                value=st.session_state[f"num_puntajes_{i}"],
                key=f"num_puntajes_input_{i}"
            )

            if num_puntajes != st.session_state[f"num_puntajes_{i}"]:
                st.session_state[f"num_puntajes_{i}"] = num_puntajes
                st.rerun()

            # Campos para puntajes
            puntajes = []
            for j in range(int(st.session_state[f"num_puntajes_{i}"])):
                col1, col2 = st.columns([4, 1])

                with col1:
                    puntaje_descripcion = st.text_area(
                        f"Etiqueta o descripción del Puntaje {j + 1}",
                        key=f"puntaje_descripcion_{i}_{j}",
                        height=68 , # Puedes ajustar la altura inicial según necesites
                        value=utils.funcionespredefinidadisplay.obtener_descripcion_puntaje(j),
                        
                           
                    )

                with col2:
                    puntaje_valor = st.text_input(
                    f"Valor del Puntaje {j + 1}",
                    key=f"puntaje_valor_{i}_{j}",
                    placeholder="Numérico",
                    value=j+1
                )
                
                if puntaje_valor:
                    try:
                        puntaje_valor_float = float(puntaje_valor)  # Convertir a flotante
                        if puntaje_valor_float < 0.0:
                            st.error("El valor debe ser mayor o igual a 0.0.")
                            puntaje_valor_float = None  # Invalidar el valor
                    except ValueError:
                        st.error("Por favor, ingresa un número válido.")
                        puntaje_valor_float = None
                else:
                    puntaje_valor_float = None

                puntajes.append({
                    "valor": puntaje_valor,
                    "descripcion": puntaje_descripcion
                })

            # Añadir el criterio a la lista de criterios
            criterios.append({
                "nombre": nombre_criterio,
                "puntajes": puntajes
            })

    # Botón de guardar (simulando el envío de un formulario)
    if st.button("Guardar Rúbrica"):
        if nombre_rubrica and all(c["nombre"] for c in criterios):
            # Crear el documento para la base de datos
            nueva_rubrica = {
                "nombre": nombre_rubrica,
                "descripcion": descripcion_rubrica,
                "criterios": criterios,
                "teacher_id": "",
                "teacher_name": "",
            }
            print(nueva_rubrica)
            
            # Guardar en la base de datos
            result = backend.save_document("rubrics", nueva_rubrica)

            if result:
                st.success(f"Rúbrica '{nombre_rubrica}' guardada exitosamente.")
            else:
                st.error("Error al guardar la rúbrica.")
        else:
            st.warning("Por favor, completa todos los campos obligatorios.")

def listar_rubricas():
    st.title("Listado de Rúbricas")

    # Inicializar la conexión a MongoDB
    backend: MongoConnection = st.session_state.backend

    # Consultar todas las rúbricas de la colección
    rubricas = backend.find_documents("rubrics")

    if not rubricas:
        st.warning("No hay rúbricas disponibles.")
        return

    # Obtener la lista de cursos disponibles
    cursos = list({rubrica["curso"]["name"] for rubrica in rubricas})
    cursos.insert(0, "Elige un curso")

    # Selectbox para filtrar por curso
    curso_seleccionado = st.selectbox("Filtrar por curso", cursos)

    # Filtrar las rúbricas según el curso seleccionado
    if curso_seleccionado != "Elige un curso":
        rubricas_filtradas = [rubrica for rubrica in rubricas if rubrica["curso"]["name"] == curso_seleccionado]
        header = f"Rúbricas del Curso: {curso_seleccionado}"
    else:
        rubricas_filtradas = rubricas
        header = "Todas mis Rúbricas"

    st.header(header)

    for rubrica in rubricas_filtradas:
        if curso_seleccionado == "Elige un curso":
            expander_label = f"Detalles de '{rubrica['nombre']}': rúbrica del curso {rubrica['curso']['name']}"
        else:
            expander_label = f"Detalles de '{rubrica['nombre']}'"
        
        with st.expander(expander_label):
            st.subheader(f"{rubrica['nombre']}")
            st.write(f"**Curso:** {rubrica['curso']['name']}")
            st.write(f"**Descripción:** {rubrica['descripcion']}")

            # Botón para ver los criterios
            if st.button(f"Ver Criterios de '{rubrica['nombre']}'", key=f"ver_criterios_{rubrica['_id']}"):
                mostrar_criterios(rubrica)

                
    # Opcional: Mostrar tabla estática
    # st.table(df)




def mostrar_criterios(rubrica):    
    # Crear tarjetas HTML para los criterios
    for criterio in rubrica["criterios"]:
        puntajes_html = "".join([
            f"<li><strong>{p['descripcion']}</strong>: ({p['valor']} pts)</li>"
            for p in criterio["puntajes"]
        ])
        
        criterio_html = f"""
        <div style='border: 1px solid #ddd; border-radius: 10px; padding: 15px; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);'>
            <h4 style='margin: 0 0 10px; color: #333;'>{criterio['nombre']}:</h4>
            <ul style='padding-left: 20px; color: #555;'>
                {puntajes_html}
            </ul>
        </div>
        """
        
        st.markdown(criterio_html, unsafe_allow_html=True)