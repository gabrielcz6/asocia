import streamlit as st
from streamlit_option_menu import option_menu
import info_unfv, login,miscursos,rubrica,mostrarrubricadecano,crearcurso

# Definimos las diferentes páginas de la app
def home_page():
    info_unfv.infounfv()

def logout_button():
    st.session_state["logged_in"] = False
    st.session_state["current_page"] = "home"
    st.rerun()

# Página de contenido de la MultiApp
def multi_app():
    # Aquí es donde se muestra el menú y las aplicaciones cuando el usuario está autenticado
    with st.sidebar:
        if st.session_state["user_role"] == "decano":
            app = option_menu(
                menu_title='Decano',
                options=['Buscar Rubricas', 'Cerrar Sesion'],
                icons=['house-fill', 'person-circle', 'trophy-fill', 'chat-fill', 'info-circle-fill'],
                menu_icon='chat-text-fill',
                default_index=0,
                styles={
                    "container": {"padding": "5!important", "background-color": 'black'},
                    "icon": {"color": "white", "font-size": "23px"},
                    "nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#02ab21"},
                }
            )
        elif st.session_state["user_role"] == "profesor":
            app = option_menu(
                menu_title='Profesor',
                options=['Mis Cursos', 'Crear Rubrica', 'Cerrar Sesion'],
                icons=['house-fill', 'chat-fill', 'trophy-fill', 'info-circle-fill'],
                menu_icon='chat-text-fill',
                default_index=0,
                styles={
                    "container": {"padding": "5!important", "background-color": 'black'},
                    "icon": {"color": "white", "font-size": "23px"},
                    "nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#02ab21"},
                }
            )
        elif st.session_state["user_role"] == "secretaria":  # Secretaria
            app = option_menu(
                menu_title='Secretaria',
                options=['Crear Curso', 'Cerrar Sesion'],
                icons=['house-fill', 'person-circle', 'info-circle-fill'],
                menu_icon='chat-text-fill',
                default_index=0,
                styles={
                    "container": {"padding": "5!important", "background-color": 'black'},
                    "icon": {"color": "white", "font-size": "23px"},
                    "nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#02ab21"},
                }
            )

    # Aquí se definen las páginas según la opción seleccionada
    if app == "Home":
        st.write("Página principal")
    elif app == "Homedecano":
        st.write("Homedecano")
    elif app == "Homesecretaria":
        st.write("Homesecretaria")
    elif app == "Homeprofesor":
        st.write("Homeprofesor")        
    elif app == "Buscar Rubricas":
        mostrarrubricadecano.mostrarrubricadecano()
    elif app == 'Crear Rubrica':
        rubrica.rubrica()
    elif app == 'Mis Cursos':
        miscursos.miscursos()
    elif app == 'Crear Curso':
        crearcurso.crearcurso()    
    elif app == 'Cerrar Sesion':
        logout_button()

    # Botón para cerrar sesión
    if st.button("Cerrar sesión"):
        logout_button()

# Función para manejar el login y la validación de rol


# Clase MultiApp que gestiona las aplicaciones
class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        # Página de información
        if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
            if "current_page" not in st.session_state or st.session_state["current_page"] == "home":
                home_page()
            elif st.session_state["current_page"] == "login":
                login.login_page()
        else:
            multi_app()

# Inicialización y ejecución de la app
if __name__ == "__main__":
    app = MultiApp()
    app.run()
