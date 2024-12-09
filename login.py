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
        backend = MongoConnection()
        backend.connect()
        user = backend.login(user=username, password=password)
        print(user)
        if user != None:
            st.session_state["logged_in"] = True
            st.session_state["user_role"] = user["rol"]  # Asignamos el rol como decano
            st.session_state["current_page"] = "home"
            st.rerun()
        # elif username == "profesor" and password == "profesor123":
        #     st.session_state["logged_in"] = True
        #     st.session_state["user_role"] = "profesor"  # Asignamos el rol como profesor
        #     st.session_state["current_page"] = "home"
        #     st.rerun()
        # elif username == "secretaria" and password == "secretaria123":
        #     st.session_state["logged_in"] = True
        #     st.session_state["user_role"] = "secretaria"  # Asignamos el rol como secretaria
        #     st.session_state["current_page"] = "home"
        #     st.rerun()
        else:
            st.error("Credenciales incorrectas")