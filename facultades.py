import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Pregrado", page_icon="🎓", layout="wide")

# Título principal
st.markdown("<h1 style='text-align: center; color: #FF6600;'>FACULTADES</h1>", unsafe_allow_html=True)

# Sección: Ciencias de la Empresa
with st.expander("📚 Ciencias de la Empresa"):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.image("https://via.placeholder.com/150", caption="Facultad de Administración", use_column_width=True)
        st.markdown("""
        **Facultad de Administración**
        """)
        st.button("Más Información", key="admin")

    with col2:
        st.image("https://via.placeholder.com/150", caption="Facultad de Ciencias Económicas", use_column_width=True)
        st.markdown("""
        **Facultad de Ciencias Económicas**
        """)
        st.button("Más Información", key="economics")

    with col3:
        st.image("https://via.placeholder.com/150", caption="Facultad de Ciencias Financieras y Contables", use_column_width=True)
        st.markdown("""
        **Facultad de Ciencias Financieras y Contables**
        """)
        st.button("Más Información", key="finance")

# Sección: Ciencias Sociales y Humanas
with st.expander("🌍 Ciencias Sociales y Humanas"):
    st.write("Aquí puedes incluir las facultades de esta categoría.")
    # Añade imágenes y botones según sea necesario.

# Sección: Ingenierías y Ciencias Naturales
with st.expander("🛠️ Ingenierías y Ciencias Naturales"):
    st.write("Aquí puedes incluir las facultades de esta categoría.")
    # Añade imágenes y botones según sea necesario.

# Sección: Ciencias de la Salud
with st.expander("❤️ Ciencias de la Salud"):
    st.write("Aquí puedes incluir las facultades de esta categoría.")
    # Añade imágenes y botones según sea necesario.
