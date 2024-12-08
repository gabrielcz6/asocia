import streamlit as st


def login_page():
    st.write("### Iniciar sesión")
    
    # Inputs para login (usuario y contraseña)
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    
    if st.button("Iniciar sesión"):
        # Aquí validamos las credenciales, esto puede ser con una base de datos o lógica predefinida
        if username == "decano" and password == "decano123":
            st.session_state["logged_in"] = True
            st.session_state["user_role"] = "decano"  # Asignamos el rol como decano
            st.session_state["current_page"] = "home"
            st.rerun()
        elif username == "profesor" and password == "profesor123":
            st.session_state["logged_in"] = True
            st.session_state["user_role"] = "profesor"  # Asignamos el rol como profesor
            st.session_state["current_page"] = "home"
            st.rerun()
        elif username == "secretaria" and password == "secretaria123":
            st.session_state["logged_in"] = True
            st.session_state["user_role"] = "secretaria"  # Asignamos el rol como secretaria
            st.session_state["current_page"] = "home"
            st.rerun()
        else:
            st.error("Credenciales incorrectas")