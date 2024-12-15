import streamlit as st
from streamlit_option_menu import option_menu
from evaluacionesScreen import evaluacionesScreen
import info_unfv, login,miscursos,rubrica,mostrarrubricadecano,crearcurso
from utils.roles import Roles

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
        st.sidebar.image(image="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBwgHBg8IBw0KFRMUDRwVFxEXGRcZGRkfFRgWGCAjHx8YICkhJCYlGxQWIz0tMTU3Li46GB8zRDU4NygwLisBCgoKDQ0NFQ0QGislHSYrKystNzctKy03Ny0rKysrNysrKzcrKysrNzcrKy0rNy0tLSsrKysrKysrKysrKysrK//AABEIAMMAwwMBIgACEQEDEQH/xAAbAAEAAgMBAQAAAAAAAAAAAAAAAwYEBQcCAf/EADcQAAEEAQMDAgQFAQcFAAAAAAEAAgMRBAUSIQYTMUFRIjJSkQcUYXGBIxUWM0JTobFFYnbD8P/EABYBAQEBAAAAAAAAAAAAAAAAAAABAv/EABsRAQACAwEBAAAAAAAAAAAAAAABEQISURMx/9oADAMBAAIRAxEAPwDuCIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIlogIiWgIiWgIiWgIlogIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIEQEREBERBqNd1lmkBrpexRY51vfs+UsFDg2Tv8eeCq0z8RYjA90kELXtk29vulxNmgQWsIr9+eCOSFseudNyNUYyDEMW4Y8r6cwPva6HhoPgm6B8+R6rlEmc78wxso4DWDjbZ7ZaG3Vm7u/e3cE1YdFk/EWJsbCMdhc6QsLO4QW7SBfxMA9fT2pWbQNZZrMTpYuzQrlj945vgmhRBBB/5XEDkSSSvZC3yD5IHDnP3WKB5BNnjijXBrqn4bZH5jAld3GupzRYj7dfMSCPUgnz637goLkiIgIiICIiAiIgIiICInqgIiICIEQECBEBERAREQUv8RXyMhidG/Nb/TkswgE+Yj8V+G2Bz7gD1pc01rJEmpCY7bOP/UAHwkuI+JpH+U7t49gQKocdL/EeGaXHiGOzLcRFIT2nhhABisuvy0cfD6mvZcyAmmzIoHvJb2aAAG0hznHgg1VvcRxxuA9KQY0G+XIcA5jW9n1B+VpJN0K2/DZ55sgeAus/hyZDgydz895bXeADqp1ba8t9j68/suWU8Z0rC54Z2uaBIIa4H1Pq5rPcE8cXx1foDHkxsWZksU7DbSWveJPqFggmga4Hp/uQsEWoRyatLpzWv3RwskJ4oiUyAVzdgxH7j+MWLqHTXwOmyJoogJ5I/wCq5rLMEhjcRZ8WB9x7rF1CGfD112o4UuDcmMyJ8Uzyz/DdI5rmloP+o4EVzQ5HKi0fQHY+Ti5jpYXlhyXvcAaL8qRsnweeBTh71XuUG2GrYfeazuw7XRh7ZN8e129wY2vis2SADVGwLvhS5Go4WLuOTkY7Nlbtzmjbu+W7PF0a91XcbpMtx3QZkkew4T4SW3bS6Z0ocCa+WwR7FqjHTeVkYcGW/IikyBlunkc172MkLmGKmuZ8TdrNoB/7SK5KCwy6zpcULJpcvDax/wAjjIwB1ED4STRouA/kL4/W9O2TdnIxnuijc90bZI9wDLu7IAoirJAHqVqdK6bkw86DLkMNsdO9zQ6R/wAU/bqnSEkkBhs8WSTQsrA/uzmPbPhxz4rGnFmj7bXve252kNOyQExAEg01xB8VSDf6n1Dpumx3kSxb6b/RDmdw7yAKbfI5v+CVlHVdOGZ+SOTi93dXb3t33V1tu7rlV/K6czzj5GHA7DLJ8iOVz37tzTH2gQAAQ7/BFGxV+DS+T9N6lPnNkfLDtbqTcgHc8AtEgdt7bQGbg3jcS4ki+LsBuZNf05mow6fHNE+SSYx7WOaS0tjfIdwBscRkfuQF617WINDwfzmUyZze41lMG53xkNHFgmrvjn9FpdO0XKgycLF7mCWYc737gT3Xh8crPibVNNygk3zV8eDtdZii1KOGKGaAFmbFJ8w57T2uIFepAr+UE39s4hy4oGOsSYjshsoI2bGGMeb9e6D7cHle4NY0zIifLBlYjmsFvcHtIaDzyQaHg+fZVmbpwtz5pdLzMVsUmJLFFE4NcI5JnxOdtBsbSWXtrguPFEAen9K5888uRLLEC6OGmufLMN2PN3viLwPhd4oAAeaJQWOLV8KeSMYssMge9zd7HxkAtaXH/NZ4HgWRdnjlfYdY0udr3Q5eG4MbbyJGHaPd1HjwfPstNn6BnarN3cw4sdmQERWSBJA6EHeQC5wLr8CgAPS1j6h01qGp4fYyXYTCzT5MZmzdTu7sFuBA2tAjHwi/PnhBYotY0yaGSaHKxHNj+dwewht+NxBoWoTruAeycaWOUS5PZBjc1wDi1z/io8cMP68jha/WdCy8rOlycGSFu6CBgaR/ozSSHmjtsPABAJBF1wFh4vTuRj6k3IyZoAXZ7Jw0yPe7+nC+IgOk5cbe03wK4rjkLgiIgIiICIiCnfiHLPFDF+XLRuje11i7DnQj2Nc7T/C5nlRBmosk37C5hd4DA0uJNC+Ko2PQAgCqXR/xLlbDjQ73MFtcPir64TxZHoD+q5vqTZMuaNmONr34raJsN+SOneOByOB4J9kHvTWMfqM0zXgujduaS1rgdpaOfI+UuPj2PFWOodAy5E2FI7JcCQ1jRQqg3c0DwL+U8/quWaeHYvdblOaXMi5cPl8O5t37n14r2oLp/wCHUjZNMeWkcO9KrmSY+nBsEG/W0FM/EbEbm/iZBC7Afl3pwP5cSGImnS87hyK816rL1XqvN0CSDQdFix8YRacJjHIJZjvd8QiBbZ4Lq3Hj9RQu45+BokHVceu5mVsnbjdsML2hu0l/NEX5cfWuFrtf03pzW9RbqA1KWCXs9p0kEzWF7Cb2usH1/wDuBU2hqMM5+Q0Wqdaa7q0WNg6VDixul0p+ROJd3gGRha31HLCRf1N5oG9XofVmZovSOj6Xp7oI3TMme6eRj3hrWTS1TYwSbII8ccfuLVrGgdJas7HdNnyNdDD2tzZwHPYbtr3Gybt3rzuPvxG7p3pUabiYeNqUsbsXf2shkrGygSuc5wJAoglx9P8Ak22x6vnnxrX9edQ5Wmab+ShxW5GRlSQPD2vDNzdm1wBNgfGCfPghfJeosjp/WtbzMmDEdPBhY257Q8dx72RN5s1tDneKBoebW+bpfTA/Il2oPccOUyMc6Zri4uIJ3lwJr4R4oL1laZ0pl5udlZWWxxzImslaZGbQIw0AtoWCNoPk8hNsennnxBi671RpWkZOp9RR4D424QmjdESDucBTHA81z59K8n0i6U6q16bX8bT+oG4RGXg/mYnRBw2ggna7cfpB/wBufb7pHT3SWm94zZ75zJjdgmeZjtsf0toChwP2rilL03ovSvT+d+dh1B8rxF22GaZr+2y72soCh/xz7m22PTzz41vVmW3pP8RG64aDMnTZGu/V8Ddw/k7Ih/K02g4v9laf06Z4YXyZWoOmL3btzd5j2lpaQLLA088forr1dh9MdWYkeNqWZGAyTeHRyMDuQRXxAijYP8Be8/H6azZ8GV+ZG38m8Oia17K4DRTrBJFNHsm2PTzz45t09/0b/wAhm/8ASrJB17rDepsfGkl02WKbP7BbC2UhgcQG/wBUgNcebI58HxfG0xOn+ksQYwjz3HsZjshtyx8uftsGmjj4B+vnlY2F0p0lhywOj1PI2wZYnijM0ZYwgg0BXgkC/Xgc+bbY9PPPjCxOs+qZ+ntQ11w04RY7nRsG125zxJGLq62hjyPNkr1nda9R4ONgw5rtOjly7mEoZK9sUWxrmgtbZc4ncDxQ4/cbqHSOloenMnQW539KeUyOJkj3guLSaNV5YPT3XvV9O6a1PHxGDUHRPxWbYp4pWNkA2hvmiDYaPT39zbbHp558aX+/WsZPT2LOH6fBM7IfFJvZK5ztgaQYomgudYeP249+NbF1Bk9SZ/TubnNYJBqM0btoIB29miASSOCOPcHx4ViyNB6YljxNuq5TZMYu2zjIb3D3Pm3OIPkccVVle9K6Z6Wx5sRmFmyOOPlvmib3IzbpQwEGhZHwD9eTyVNsennnxfURFpgREQEREFE/FNpfhQtoeHeTQFPhPP2XNM3R9VwpIXarkFrZ4A8GJxDdo4bZcKBrn2oD+Or9f40uRHAI4p3j4rDGF/rGRYAP0k/wqHrGj5mdrOAIoNabGGxtmJheW0C26LQCKaXCq423ZJKDS6foeq6iJ5sCdu3Hja7+qTtLXF/yloI4ppPHNg2OAuo/hlGYtIdG6uD6Hzb5D/uSVR+m9JzcHIzGZuPrTtzS2Nxhk27QHeQQSb+EVQ/cronQuPJj4kjHxTM+Lw5hZ6vJqwL8g/ygsjoo3m3Naf3AXzsRfQz7BSopULcouxF9DPsE7EX0M+wUqJUFyi7EX0M+wTsRfQz7BSolQXKLsRfQz7BOxF9DPsFKiVBcouxF9DPsE7EX0M+wUqJUFyi7EX0M+wTsRfQz7BSolQXKLsRfQz7BOxF9DPsFKiVBco+xD9DPsEbDE02Gt+wUiJUFyIiBVBERAREQEREBERAREQEREBERAREQEREBERAREQEREBAiICIiAiIgIiICIiAiIgIgRAREQEREBEQICIiAiIgIiICIiAiIgIiICIiAiIgIiIAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQERAgInKICIiAiIgBERAREQECIgIURAREQEREAIiICIiAiIgeiBEQEHlEQEREBERACBEQEREH/9k=", 
                         width=300)

        if st.session_state["user_role"] == Roles.DECANO.value:
            # backend.find_courses_by_user()
            app = option_menu(
                menu_title='Decano',
                options=['Buscar Rubricas','Reporte Rubrica' ,'Cerrar Sesion'],
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
        elif st.session_state["user_role"] == Roles.PROFESOR.value:
            app = option_menu(
                menu_title=st.session_state["current_user"]["fullname"],
                options=['Mis Cursos', 'Crear Rúbricas', 'Mis Rúbricas', 'Evaluar Estudiantes', 'Ver Evaluaciones', 'Cerrar Sesion'],
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
        elif st.session_state["user_role"] == Roles.SECRETARIA.value:  # Secretaria
            app = option_menu(
                menu_title='Secretaria',
                options=['Crear Nueva Rubrica', 'Cerrar Sesion'],
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
    elif app == "Reporte Rubrica":
        mostrarrubricadecano.mostrarrubricadecano2()
    elif app == 'Evaluar Estudiantes':
        rubrica.evaluacion_rubrica()
    elif app == 'Ver Evaluaciones':
        evaluacionesScreen()
    elif app == 'Crear Rúbricas':
         rubrica.crear_rubrica_v2()
    elif app == 'Mis Rúbricas':
         rubrica.listar_rubricas()
    elif app == 'Mis Cursos':
        miscursos.miscursos()
    elif app == 'Crear Nueva Rubrica':
        rubrica.crear_rubrica_generic()    
    elif app == 'Cerrar Sesion':
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
