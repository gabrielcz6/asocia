import streamlit as st



def infounfv():
  
  # Configuración de la página
  st.set_page_config(page_title="UNFV", page_icon="🎓", layout="wide")

  # Sección de noticias
  st.markdown("<h3 style='text-align: center;'>Sistema de Rubricas UNFV</h3>", unsafe_allow_html=True)

  
  # Barra superior
  st.markdown("""
      <style>
          .barra-superior {
              background-color: #FF6600;
              padding: 10px;
              text-align: center;
              color: white;
              font-weight: bold;
              font-size: 14px;
          }
      </style>
      <div class="barra-superior">
          📞 Tel: (+51) 748 0888 | ✉️ Correo Institucional | Redes Sociales: Facebook | Twitter | YouTube | Instagram
      </div>
  """, unsafe_allow_html=True)
  
  # Encabezado principal
 # col1 = st.columns(1)
  
  #with col1:
  st.markdown("<div style='text-align: center;'><img src='https://www.unfv.edu.pe/images/logo_unfv.jpg' width='450'></div>", unsafe_allow_html=True)

  st.markdown("<h3 style='text-align: center;'>Acceso Personal</h3>", unsafe_allow_html=True)

  

  
  
  col1, col2, col3 = st.columns(3)
  
    # Columna 1
  with col1:
        if st.button('Ir a Login desde Profesor'):
            st.session_state["logged_in"] = False  # Si no está logueado, redirigir al login
            st.session_state["current_page"] = "login"
            st.rerun()
            st.image("https://via.placeholder.com/150", caption="Profesor")
            st.write("Descripción de la noticia 1...")
  
  # Columna 2
  with col2:
      if st.button('Ir a Login desde Secretaria'):
            st.session_state["logged_in"] = False  # Si no está logueado, redirigir al login
            st.session_state["current_page"] = "login"
            st.rerun()
            st.image("https://via.placeholder.com/150", caption="Secretaria")
            st.write("Descripción de la noticia 1...")
  
  # Columna 3
  with col3:
            if st.button('Ir a Login desde Decano'):
              st.session_state["logged_in"] = False  # Si no está logueado, redirigir al login
              st.session_state["current_page"] = "login"
              st.rerun()
              st.image("https://via.placeholder.com/150", caption="Decano")
              st.write("Descripción de la noticia 1...")
  # Footer
  st.markdown("""
      <style>
          .footer {
              background-color: #FF6600;
              padding: 10px;
              text-align: center;
              color: white;
              font-size: 12px;
          }
      </style>
      <div class="footer">
          © 2024 Universidad Nacional Federico Villarreal | Todos los derechos reservados
      </div>
  """, unsafe_allow_html=True)
  