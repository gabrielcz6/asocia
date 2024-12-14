import streamlit as st
from bson import ObjectId
import datetime

def assessmentScreen():
    # Rúbrica de ejemplo
    rubrica = {
        "_id": ObjectId("675bdfc9a64c8258ae69516f"),
        "nombre": "Proyecto semana 2",
        "descripcion": "",
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
    }

    # Interfaz de evaluación
    st.title(f"Evaluación: {rubrica['nombre']}")
    st.write(f"Docente: {rubrica['teacher_name']}")
    st.write(f"Descripción: {rubrica['descripcion']}")

    resultados = []
    for criterio in rubrica["criterios"]:
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
            "rubrica_id": rubrica["_id"],
            "rubrica_nombre": rubrica["nombre"],
            "fecha_evaluacion": datetime.datetime.now(),
            "teacher_id": rubrica["teacher_id"],
            "teacher_name": rubrica["teacher_name"],
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