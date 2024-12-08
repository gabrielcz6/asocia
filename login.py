import streamlit as st


def login_page():
    st.title("Iniciar Sesión")
    
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    
    if st.button("Iniciar sesión"):
        if username == "admin" and password == "admin123":
            st.session_state["logged_in"] = True  # Establecer sesión
            st.session_state["current_page"] = "home"
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos")