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
#poner un video
 with open ("video.mp4","rb") as video_file:
   
   st.video(video_file.read(),start_time=10)
###########################################
with open ("audio.mp3","rb") as audio_file:
   
   st.audio(audio_file.read())


if __name__=="__main__": 
 main()