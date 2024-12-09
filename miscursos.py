import streamlit as st
import pandas as pd
from db.MongoConnection import MongoConnection


def miscursos():
    # Ejemplo de datos: lista de diccionarios
    
    backend: MongoConnection = st.session_state.backend
    data = backend.find_courses_by_user(st.session_state["current_user"]["_id"])
    df = pd.DataFrame(data, dtype="object")
    df.rename(columns={'_id': 'Código', 'name': 'Asignatura', 'semester': 'Semestre', 'year': 'Año'}, inplace=True)
    
    # Convertir la lista de diccionarios en un DataFrame
    # df_cursos = pd.DataFrame(cursos)
    
    # Renderizar la tabla en Streamlit
    st.title("Lista de Cursos")
    st.dataframe(df, hide_index=True)
    