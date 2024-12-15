import streamlit as st
from utils2 import responderquery
import torch


def chatbot_ia():
  #input("gato")
  def reiniciarChat():
      """Función que reinicia el chat y borra el historial"""
      st.toast("CHAT INICIADO", icon='🤖')
      # Inicializamos el historial de chat
      if "messages" in st.session_state:
          st.session_state.messages = []
  
  
  
  st.header('Habla con la IA de las Rubricas')
  
  # Menú lateral para configurar parámetros
  with st.sidebar:
      st.subheader('Parámetros')
      parUsarMemoria = st.checkbox("Recordar la conversación", value=True, on_change=reiniciarChat)
  
  # Inicialización del historial de chat si no existe
  if "messages" not in st.session_state:
      st.session_state.messages = []
  
  # Mostrar los mensajes anteriores en el chat
  with st.container():
      for message in st.session_state.messages:
          if message["role"] != "system":  # Omitimos los mensajes del sistema
              with st.chat_message(message["role"]):
                  st.markdown(message["content"])
  
  # Campo para el mensaje del usuario
  prompt = st.chat_input("¿Qué quieres saber?")
  
  if prompt:
      # Mostrar mensaje del usuario
      st.chat_message("user").markdown(prompt)
      
      # Agregar mensaje del usuario al historial
      st.session_state.messages.append({"role": "user", "content": prompt})
  
      # Definir el historial de mensajes a enviar a la función `responderquery`
      if parUsarMemoria:
          # Usar todo el historial de chat
          messages = [
              {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
          ]
      else:
          # Solo enviar el primer y último mensaje (sin memoria)
          messages = [
              {"role": st.session_state.messages[0]["role"], "content": st.session_state.messages[0]["content"]},
              {"role": st.session_state.messages[-1]["role"], "content": st.session_state.messages[-1]["content"]}
          ]
     # input("esto es")    
     # input(messages)
      # Llamar a la función `responderquery` con el historial de mensajes
      respuesta = responderquery(messages)
      
  
      # Mostrar respuesta del asistente en el chat
      with st.chat_message("assistant"):
          st.write(respuesta)
      
      # Agregar respuesta del asistente al historial
      st.session_state.messages.append({"role": "assistant", "content": respuesta})
  