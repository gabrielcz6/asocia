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
    st.title("Crear / Editar Rúbrica V2")

    # Inicializar la conexión a MongoDB
    backend: MongoConnection = st.session_state.backend

    # Cargar datos de la rúbrica si estamos en modo edición
    rubrica_a_editar = st.session_state.get("rubrica_a_editar", None)
    edit_mode = st.session_state.get("edit_mode", False)

    # Inicializar campos con datos existentes si es edición
    nombre_rubrica = st.text_input("Nombre de la Rúbrica", value=rubrica_a_editar["nombre"] if rubrica_a_editar else "")
    descripcion_rubrica = st.text_area("Descripción de la Rúbrica", height=100, value=rubrica_a_editar["descripcion"] if rubrica_a_editar else "")

    # Control del número de criterios
    criterios_iniciales = rubrica_a_editar["criterios"] if rubrica_a_editar else []
    num_criterios = len(criterios_iniciales) if criterios_iniciales else 1

    criterios = []
    for i in range(num_criterios):
        criterio_existente = criterios_iniciales[i] if i < len(criterios_iniciales) else {"nombre": "", "descripcion": "", "puntajes": []}

        with st.expander(f"Criterio {i + 1}"):
            nombre_criterio = st.text_input(f"Nombre del Criterio {i + 1}", value=criterio_existente["nombre"], key=f"nombre_criterio_{i}")
            descripcion_criterio = st.text_area(f"Descripción del Criterio {i + 1}", value=criterio_existente["descripcion"], key=f"descripcion_criterio_{i}")

            puntajes = []
            for j, puntaje in enumerate(criterio_existente.get("puntajes", [])):
                puntaje_valor = st.number_input(f"Valor del Puntaje {j + 1}", min_value=1, value=puntaje["valor"], key=f"puntaje_valor_{i}_{j}")
                puntaje_descripcion = st.text_area(f"Descripción del Puntaje {j + 1}", value=puntaje["descripcion"], key=f"puntaje_descripcion_{i}_{j}")
                puntajes.append({"valor": puntaje_valor, "descripcion": puntaje_descripcion})

            criterios.append({"nombre": nombre_criterio, "descripcion": descripcion_criterio, "puntajes": puntajes})

    # Botón para guardar
    if st.button("Guardar Rúbrica"):
        nueva_rubrica = {
            "nombre": nombre_rubrica,
            "descripcion": descripcion_rubrica,
            "criterios": criterios,
            "teacher_id": st.session_state["current_user"]["_id"],
            "teacher_name": st.session_state["current_user"]["fullname"]
        }

        if edit_mode:
            backend.db["rubrics"].update_one({"_id": rubrica_a_editar["_id"]}, {"$set": nueva_rubrica})
            st.success(f"Rúbrica '{nombre_rubrica}' actualizada exitosamente.")
        else:
            backend.save_document("rubrics", nueva_rubrica)
            st.success(f"Rúbrica '{nombre_rubrica}' guardada exitosamente.")

        # Limpiar el estado y volver a la lista de rúbricas
        st.session_state.pop("rubrica_a_editar", None)
        st.session_state.pop("edit_mode", None)
        st.session_state.current_page = "Mis Rubricas"
        st.rerun()



def listar_rubricas():
    st.title("Listado de Rúbricas")

    # Inicializar la conexión a MongoDB
    backend: MongoConnection = st.session_state.backend

    # Consultar todas las rúbricas de la colección
    rubricas = backend.find_documents("rubrics")

    if not rubricas:
        st.warning("No hay rúbricas disponibles.")
        return

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
                        # Botón para editar la rúbrica
            if st.button(f"Editar Rúbrica '{rubrica['nombre']}'", key=f"editar_{rubrica['_id']}"):
                # Guardar los datos de la rúbrica en st.session_state
                st.session_state.rubrica_a_editar = rubrica
                st.session_state.edit_mode = True
                st.session_state.current_page = "Crear Rubrica V2"
                st.rerun()  # Recargar para ir al formulario de edición
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

