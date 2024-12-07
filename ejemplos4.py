import streamlit as st
import pandas as pd
from PIL import Image
from funciones_endpoint import *

# Crear un DataFrame de Pandas

def main():
 
 #

 st.title(get_rubricas(1))
 #########################################
 #textinput
 nombre=st.text_input("ingresa tu nombre")

 st.write(nombre)
 #########################################
#tex area input 
 mensaje=st.text_area("ingresa tu mensaje", height=100)
 st.write(mensaje)

 ########################################
 #inputa para numero
 numero=st.number_input("ingresa un numero", 1.0,25.0)
 st.write(numero)
 ########################################

 cita=st.date_input("selecciona una fecha")
 st.write(cita)

 ########################################

 cita=st.time_input("selecciona una hora")
 st.write(cita)

 ########################################

 color=st.color_picker("selecciona un color")
 st.write(color)
 
if __name__=="__main__": 
 main()


