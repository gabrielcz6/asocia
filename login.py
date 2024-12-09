import streamlit as st
from db.MongoConnection import MongoConnection


def login_page():

    st.write("### Iniciar sesión")
    
    # Inputs para login (usuario y contraseña)
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    #ENDPOINT 1 recuperar dni del usuario y contraseña que esta logeando
    #st.session_state["id"]
    
    if st.button("Iniciar sesión"):
        # Aquí validamos las credenciales, esto puede ser con una base de datos o lógica predefinida
        if "mongo_backend" not in st.session_state:
            backend = MongoConnection()
            backend.connect()
            st.session_state.backend = backend
        # backend = MongoConnection()
        # backend.connect()
        user = st.session_state.backend.login(user=username, password=password)
        if user != None:
            st.session_state["logged_in"] = True
            st.session_state["user_role"] = user["rol"]  # Asignamos el rol como decano
            st.session_state["current_page"] = "home"
            st.session_state["current_user"] = user
            st.rerun()
        else:
            st.error("Credenciales incorrectas")