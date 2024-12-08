import streamlit as st


def app():
         
         # Configuración de la página
     #st.set_page_config(page_title="UNFV", page_icon="🎓", layout="wide")
     
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
     col1, col2 = st.columns([1, 3])
     
     with col1:
         st.image("https://www.unfv.edu.pe/images/logo.png", width=150)  # Imagen del logo
     
     with col2:
         st.markdown("""
         <h1 style="color: #FF6600; font-size: 32px;">Universidad Nacional Federico Villarreal</h1>
         """, unsafe_allow_html=True)
     
     # Menú de navegación
     st.markdown("""
         <style>
             .menu {
                 background-color: #FFC300;
                 padding: 10px;
                 text-align: center;
                 font-weight: bold;
                 font-size: 16px;
             }
             .menu a {
                 text-decoration: none;
                 color: black;
                 padding: 10px;
             }
             .menu a:hover {
                 color: #FF6600;
             }
         </style>
         <div class="menu">
             | <a href="#profesor">Plataforma Asocia</a> |
          
     
         </div>
     """, unsafe_allow_html=True)
     
     # Imagen principal
     st.image("https://www.unfv.edu.pe/images/unfv_front.png", caption="UNFV", use_column_width=True)
     
     # Sección de noticias
     st.markdown("### Seleccionar")
     col1, col2, col3 = st.columns(3)
     
     with col1:
         st.image("https://via.placeholder.com/150", caption="Profesor")
         st.write("Descripción de la noticia 1...")
     
     with col2:
         st.image("https://via.placeholder.com/150", caption="Secretaria(o)")
         st.write("Descripción de la noticia 2...")
     
     with col3:
         st.image("https://via.placeholder.com/150", caption="Decano")
         st.write("Descripción de la noticia 3...")
     
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

