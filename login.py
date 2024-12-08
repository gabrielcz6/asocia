import streamlit as st


def loginsistema():
 

# Usuarios y contraseñas almacenados en un diccionario
 users = {
    "admin": "admin123",
    "user1": "password1",
    "user2": "password2",
 }

# Estado de sesión para el inicio de sesión
 if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

 def login(username, password):
    """Función para verificar credenciales."""
    if username in users and users[username] == password:
        st.session_state.authenticated = True
        st.success(f"Bienvenido, {username}!")
    else:
        st.error("Credenciales incorrectas.")

 def logout():
    """Cerrar sesión."""
    st.session_state.authenticated = False
    st.experimental_rerun()

# UI del Login
 if not st.session_state.authenticated:
    st.title("Sistema de Login")
    
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    
    if st.button("Iniciar sesión"):
        login(username, password)
 else:
    st.title("Página principal")
    st.write("¡Has iniciado sesión correctamente!")
    st.button("Cerrar sesión", on_click=logout)


if __name__=="__main__": 
 loginsistema()