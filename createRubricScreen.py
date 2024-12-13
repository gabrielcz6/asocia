
from db.MongoConnection import MongoConnection
import streamlit as st
import pandas as pd

# Pantalla para crear un template de rúbrica

def createRubricScreen():
    # backend = st.session_state.backend

    st.title("Creación de Rúbrica")

    # Formulario para crear el template de rúbrica
    rubric_name = st.text_input("Nombre de la Rúbrica", placeholder="Ingrese un nombre para la rúbrica")
    rubric_description = st.text_area("Descripción", placeholder="Ingrese una descripción detallada de la rúbrica")

    # Tabla dinámica para agregar criterios
    st.subheader("Criterios de Evaluación")
    if "criteria" not in st.session_state:
        st.session_state["criteria"] = []

    criteria_container = st.container()

    for idx, criterion in enumerate(st.session_state["criteria"]):
        with criteria_container:
            st.write(f"### Criterio {idx + 1}")
            criterion_name = st.text_input(f"Nombre del criterio {idx + 1}", value=criterion.get("name", ""))
            criterion_description = st.text_area(f"Descripción del criterio {idx + 1}", value=criterion.get("description", ""))

            criterion_scores = st.slider(f"Número de niveles de puntuación para {criterion_name}", 1, 10, value=len(criterion.get("scores", [])))
            scores = []
            for i in range(criterion_scores):
                score_label = st.text_input(f"Etiqueta del nivel {i + 1} para {criterion_name}",
                                            value=criterion.get("scores", [])[i].get("label", "") if len(criterion.get("scores", [])) > i else "")
                scores.append({"label": score_label, "value": i + 1})
            st.session_state["criteria"][idx] = {"name": criterion_name, "description": criterion_description, "scores": scores}

    # Botones para agregar o eliminar criterios fuera del formulario
    if st.button("Agregar Criterio"):
        st.session_state["criteria"].append({"name": "", "description": "", "scores": []})

    if st.button("Eliminar Último Criterio") and st.session_state["criteria"]:
        st.session_state["criteria"].pop()

    # Botón para guardar la rúbrica
    if st.button("Guardar Rúbrica"):
        if rubric_name and st.session_state["criteria"]:
            rubric = {
                "name": rubric_name,
                "description": rubric_description,
                "criteria": st.session_state["criteria"]
            }

            # Guardar en la base de datos
            # backend.create_rubric(rubric)
            st.success("Rúbrica creada exitosamente.")
            st.session_state["criteria"] = []
        else:
            st.error("Por favor, complete todos los campos requeridos.")


def crear_rubrica_v2():
    st.title("Crear Rúbrica V2")
    st.markdown(
        """
        <style>
        /* Cambiar el ancho solo del número de criterios basado en su clave */
        div[data-testid="stNumberInputContainer"] {
            width: 100px !important; /* Ancho personalizado */
            font-size: 14px; /* Cambiar el tamaño del texto (opcional) */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    # Inicializar la conexión a MongoDB (Simulación aquí)
    # backend: MongoConnection = st.session_state.backend
    backend = MongoConnection()

    # Inicializar el estado para número de criterios
    if "num_criterios" not in st.session_state:
        st.session_state.num_criterios = 1

    # Control de la rúbrica (nombre y descripción
    st.subheader("Información de la Rúbrica")
    nombre_rubrica = st.text_input("Nombre de la Rúbrica", max_chars=100)

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
        with st.expander(f"Criterio {i + 1}"):
            nombre_criterio = st.text_input(f"Nombre del Criterio", key=f"nombre_criterio_{i}")
            
            # Control del número de puntajes
            if f"num_puntajes_{i}" not in st.session_state:
                st.session_state[f"num_puntajes_{i}"] = 1
            
            st.markdown(f"<div class='small-number-input'>", unsafe_allow_html=True)
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
                col1, _ = st.columns([4, 1])  # Columna pequeña para el input y una grande vacía
                with col1:
                    puntaje_descripcion = st.text_area(
                        f"Etiqueta o descripción del Puntaje {j + 1}",
                        key=f"puntaje_descripcion_{i}_{j}",
                        height=68  # Puedes ajustar la altura inicial según necesites
                    )
                with _:
                    puntaje_valor = st.text_input(
                    f"Valor del Puntaje {j + 1}",
                    key=f"puntaje_valor_{i}_{j}",
                    placeholder="Numérico"
                )
                # Validar la entrada del usuario
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
            
            criterios.append({
                "nombre": nombre_criterio,
                "puntajes": puntajes
            })

    # Botón de guardar (simulando el envío de un formulario)
    if st.button("Guardar Rúbrica"):
        if nombre_rubrica and all(c["nombre"] for c in criterios):
            # Guardar la rúbrica en MongoDB
            nueva_rubrica = {
                "nombre": nombre_rubrica,
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









# def createRubricScreen():
#     # Ejemplo de datos: lista de diccionarios
    
#     backend: MongoConnection = st.session_state.backend
#     data = backend.find_courses_by_user(st.session_state["current_user"]["_id"])
#     df = pd.DataFrame(data, dtype="object")
#     df.rename(columns={'_id': 'Código', 'name': 'Asignatura', 'semester': 'Semestre', 'year': 'Año'}, inplace=True)
    
    
#     # Renderizar la tabla en Streamlit
#     st.title("Lista de Cursos")
#     st.dataframe(df, hide_index=True)


if __name__ == "__main__":
    # createRubricScreen()
    crear_rubrica_v2()