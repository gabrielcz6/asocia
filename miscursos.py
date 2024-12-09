import streamlit as st
import pandas as pd


def miscursos():
    # Ejemplo de datos: lista de diccionarios
    cursos = [
        {"nombre_curso": "Matemáticas 101", "semestre": "1er Semestre", "codigo_curso": "MAT101"},
        {"nombre_curso": "Física 202", "semestre": "2do Semestre", "codigo_curso": "FIS202"},
        {"nombre_curso": "Química 303", "semestre": "3er Semestre", "codigo_curso": "QUI303"},
        {"nombre_curso": "Programación 404", "semestre": "4to Semestre", "codigo_curso": "PRO404"},
    ]
    
    # Convertir la lista de diccionarios en un DataFrame
    df_cursos = pd.DataFrame(cursos)
    
    # Renderizar la tabla en Streamlit
    st.title("Lista de Cursos")
    st.dataframe(df_cursos)
    