import streamlit as st
import pandas as pd
from PIL import Image

# Crear un DataFrame de Pandas


def main():
 st.title("Curso de Streamlit")
 img=Image.open("imagen.jpg")

##########################################
#imagen desde aca los datos
 st.image(img,use_column_width=True)
###########################################
#imagen aleatoria de internet
 st.image("https://picsum.photos/800")
###########################################
#poner un vide
if __name__=="__main__": 
 main()