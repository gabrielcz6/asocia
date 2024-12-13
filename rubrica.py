import streamlit as st
from db.MongoConnection import MongoConnection
import pandas as pd
import json
from bson.objectid import ObjectId



def rubrica():
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
    if alumno_seleccionado["name"] in opciones_alumnos:
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
                if backend.save_rubric(student=alumno_seleccionado,course=curso_seleccionado,rubric=rubrica, course_id=curso_seleccionado_id, teacher_id=st.session_state["current_user"]["_id"], teacher_name = st.session_state["current_user"]["fullname"]):
                # bd_simulada[alumno_seleccionado["name"]] = rubrica
                    st.success(f"Rúbrica guardada para {alumno_seleccionado["name"]}")
                    print(st.session_state["current_user"])
                    rubricas_del_profe = backend.find_documents("rubrics", {"teacher_id" : st.session_state["current_user"]["_id"]})
                else:
                    st.error(f"Rúbrica no guardada para {alumno_seleccionado["name"]}")
            else:
                st.warning("La rúbrica no puede estar vacía.")
    
    # Mostrar la información final
    if alumno_seleccionado["name"] in bd_simulada:
        st.write(f"Rúbrica para {alumno_seleccionado}, {curso_seleccionado}:")
        st.write(bd_simulada[alumno_seleccionado["name"]])

    if len(rubricas_del_profe) > 0: 
        st.title(f"Histórico de Rúbricas")
        df = pd.DataFrame(rubricas_del_profe)
        #df['student'] = df['student'].apply(json.loads)
        df['student'] = df['student'].apply(lambda x: x['name'])
        df['course'] = df['course'].apply(lambda x: x['name'])


        st.dataframe(df[['teacher_name', 'student','course','rubric']])


def crear_rubrica_v2():
    st.title("Crear Rúbrica V2")

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
    descripcion_rubrica = st.text_area("Descripción de la Rúbrica", height=100)

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
            nombre_criterio = st.text_input(f"Nombre del Criterio {i + 1}", key=f"nombre_criterio_{i}")
            descripcion_criterio = st.text_area(f"Descripción del Criterio {i + 1}", key=f"descripcion_criterio_{i}")

            # Control del número de puntajes
            if f"num_puntajes_{i}" not in st.session_state:
                st.session_state[f"num_puntajes_{i}"] = 1

            num_puntajes = st.number_input(
                f"Número de Puntajes para el Criterio {i + 1}",
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
                        f"Descripción del Puntaje {j + 1}",
                        key=f"puntaje_descripcion_{i}_{j}",
                        height=68
                    )

                with col2:
                    puntaje_valor = st.number_input(
                        f"Valor {j + 1}",
                        min_value=1,
                        key=f"puntaje_valor_{i}_{j}"
                    )

                puntajes.append({
                    "valor": puntaje_valor,
                    "descripcion": puntaje_descripcion
                })

            # Añadir el criterio a la lista de criterios
            criterios.append({
                "nombre": nombre_criterio,
                "descripcion": descripcion_criterio,
                "puntajes": puntajes
            })

    # Botón de guardar (simulando el envío de un formulario)
    if st.button("Guardar Rúbrica"):
        if nombre_rubrica and descripcion_rubrica and all(c["nombre"] for c in criterios):
            # Crear el documento para la base de datos
            nueva_rubrica = {
                "nombre": nombre_rubrica,
                "descripcion": descripcion_rubrica,
                "criterios": criterios,
                "teacher_id": st.session_state["current_user"]["_id"],
                "teacher_name": st.session_state["current_user"]["fullname"]
            }

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

    # Transformar los datos en una lista de diccionarios para la tabla
    # data = []
    # for rubrica in rubricas:
    #     # Extraer solo los parámetros que deseas mostrar
    #     for criterio in rubrica["criterios"]:
    #         data.append({
    #             "Nombre Rúbrica": rubrica["nombre"],
    #             "Descripción Rúbrica": rubrica["descripcion"],
    #             "Nombre Criterio": criterio["nombre"],
    #             "Descripción Criterio": criterio["descripcion"],
    #             "Teacher": rubrica["teacher_name"]
    #         })

    data = []
    for rubrica in rubricas:
        # Agregar solo un registro por rúbrica
        data.append({
            "ID": str(rubrica["_id"]),
            "Nombre Rúbrica": rubrica["nombre"],
            "Descripción Rúbrica": rubrica["descripcion"],
            "Teacher": rubrica["teacher_name"]
        })
    # Crear un DataFrame de pandas
    df = pd.DataFrame(data)

    # Mostrar la tabla en Streamlit
    st.dataframe(df)

    for rubrica in rubricas:
        with st.expander(f"Detalles de '{rubrica['nombre']}'"):
            st.write(f"**Descripción:** {rubrica['descripcion']}")
            st.write(f"**Teacher:** {rubrica['teacher_name']}")

            # Botón para ver los criterios
            if st.button(f"Ver Criterios de '{rubrica['nombre']}'", key=f"ver_criterios_{rubrica['_id']}"):
                mostrar_criterios(rubrica)
                
    # Opcional: Mostrar tabla estática
    # st.table(df)
def mostrar_criterios(rubrica):
    st.subheader(f"Criterios de la Rúbrica '{rubrica['nombre']}'")

    # Crear una lista de diccionarios con los criterios
    data_criterios = []
    for criterio in rubrica["criterios"]:
        data_criterios.append({
            "Nombre Criterio": criterio["nombre"],
            "Descripción Criterio": criterio["descripcion"],
            "Puntajes": ", ".join([f"{p['valor']} ({p['descripcion']})" for p in criterio["puntajes"]])
        })

    # Crear un DataFrame para los criterios
    df_criterios = pd.DataFrame(data_criterios)

    # Mostrar la tabla con los criterios
    st.dataframe(df_criterios)
# Llamar a la función para listar rúbricas

