import streamlit as st
from bson import ObjectId
import datetime

def assessmentScreen():

    # Rúbricas de ejemplo
    rubricas = [
        {
            "_id": ObjectId("675bdfc9a64c8258ae69516f"),
            "nombre": "Proyecto semana 2",
            "descripcion": "Evaluación del proyecto realizado en la semana 2.",
            "criterios": [
                {
                    "nombre": "Dominio del tema",
                    "puntajes": [
                        {"valor": "2.5", "descripcion": "Realizó"},
                        {"valor": "0", "descripcion": "No realizó"},
                    ],
                },
                {
                    "nombre": "Investigación del tema",
                    "puntajes": [
                        {"valor": "3.5", "descripcion": "Sabe del tema"},
                        {"valor": "0.1", "descripcion": "No sabe"},
                    ],
                },
            ],
            "teacher_id": ObjectId("67550e8e278f66cc36fe9342"),
            "teacher_name": "Espinoza Silverio, Edgar Franklin",
        },
        {
            "_id": ObjectId("675bdfc9a64c8258ae695170"),
            "nombre": "Tarea integradora",
            "descripcion": "Evaluación integral de habilidades.",
            "criterios": [
                {
                    "nombre": "Creatividad",
                    "puntajes": [
                        {"valor": "3", "descripcion": "Altamente creativo"},
                        {"valor": "2", "descripcion": "Moderadamente creativo"},
                        {"valor": "1", "descripcion": "Poco creativo"},
                    ],
                },
                {
                    "nombre": "Resolución de problemas",
                    "puntajes": [
                        {"valor": "3", "descripcion": "Solución completa y precisa"},
                        {"valor": "2", "descripcion": "Solución parcial pero razonable"},
                        {"valor": "1", "descripcion": "Poco o nada resolutivo"},
                    ],
                },
                {
                    "nombre": "Presentación",
                    "puntajes": [
                        {"valor": "3", "descripcion": "Muy bien presentada"},
                        {"valor": "2", "descripcion": "Presentación aceptable"},
                        {"valor": "1", "descripcion": "Presentación deficiente"},
                    ],
                },
            ],
            "teacher_id": ObjectId("67550e8e278f66cc36fe9342"),
            "teacher_name": "Espinoza Silverio, Edgar Franklin",
        },
    ]

    # Selección de rúbrica
    rubrica_nombres = ["Elige una rúbrica"] + [rubrica["nombre"] for rubrica in rubricas]
    selected_rubrica_nombre = st.selectbox("Seleccione la rúbrica a evaluar:", rubrica_nombres)

    # Mostrar evaluación solo si se selecciona una rúbrica válida
    if selected_rubrica_nombre != "Elige una rúbrica":
        selected_rubrica = next(rubrica for rubrica in rubricas if rubrica["nombre"] == selected_rubrica_nombre)

        st.title(f"Evaluación: {selected_rubrica['nombre']}")
        st.write(f"Docente: {selected_rubrica['teacher_name']}")
        st.write(f"Descripción: {selected_rubrica['descripcion']}")

        # Interfaz de evaluación
        resultados = []
        for criterio in selected_rubrica["criterios"]:
            st.subheader(criterio["nombre"])
            puntaje = st.radio(
                "Seleccione un puntaje:",
                options=criterio["puntajes"],
                format_func=lambda x: f"{x['valor']} - {x['descripcion']}",
                key=criterio["nombre"],
            )
            resultados.append({"criterio": criterio["nombre"], "puntaje": puntaje})

        # Guardar la evaluación
        if st.button("Guardar evaluación"):
            evaluacion = {
                "_id": ObjectId(),  # Nuevo ID para la evaluación
                "rubrica_id": selected_rubrica["_id"],
                "rubrica_nombre": selected_rubrica["nombre"],
                "fecha_evaluacion": datetime.datetime.now(),
                "teacher_id": selected_rubrica["teacher_id"],
                "teacher_name": selected_rubrica["teacher_name"],
                "evaluador_id": ObjectId("67550e8e278f66cc36fe9342"),  # Evaluador ficticio
                "alumno_id": ObjectId("202400002700000000000001"),  # Alumno ficticio
                "alumno_nombre": "Juan Pérez",
                "resultados": resultados,
            }
            st.write("Evaluación guardada:")
            st.json(evaluacion)
            # Código para inyectar a MongoDB (por ejemplo, usando pymongo)
            # db.evaluaciones.insert_one(evaluacion)


if __name__ == "__main__":
    assessmentScreen()