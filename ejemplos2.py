import streamlit as st
import pandas as pd
data = {
    'Nombre': ['Elefante', 'León', 'Tigre', 'Jirafa', 'Oso', 'Cebra', 'Zebra', 'Águila', 'Cocodrilo', 'Ballena'],
    'Especie': ['Elefante africano', 'Pantera leo', 'Panthera tigris', 'Giraffa camelopardalis', 'Ursidae', 'Equus zebra', 'Equus zebra', 'Aquila chrysaetos', 'Crocodylus porosus', 'Balaenoptera musculus'],
    'Continente': ['África', 'África', 'Asia', 'África', 'América del Norte', 'África', 'África', 'América del Norte', 'Asia', 'Océano'],
    'Dieta': ['Herbívoro', 'Carnívoro', 'Carnívoro', 'Herbívoro', 'Omnívoro', 'Herbívoro', 'Herbívoro', 'Carnívoro', 'Carnívoro', 'Carnívoro'],
    'Longevidad (años)': [60, 14, 15, 25, 20, 30, 30, 20, 70, 90],
    'Estado de conservación': ['Vulnerable', 'Casi amenazado', 'En peligro de extinción', 'Preocupación menor', 'Casi amenazado', 'Preocupación menor', 'Preocupación menor', 'Preocupación menor', 'Vulnerable', 'Preocupación menor']
}

# Crear un DataFrame de Pandas
df = pd.DataFrame(data)
df2 = df.sample(n=3,random_state=42)
def main():

 st.title("CURSO STREAMLIT")
 st.header("Dataframe: ")

 #para mostrar resaltado los maximos
 #st.dataframe(df2.style.highlight_max(axis=0))
 
 #mostar primeras 5 filas
 #st.write(df.head(5))

 #imprimir formato jsom
 st.json({"clave":"valor"})
###################################
 #CON ESTO SE CREA CODIGO

 #codigo="""def saludar():
  #             print("hola")
   #            """
 #st.code(codigo,language="python")
#####################################
 
 #codigo para select box con accion write
 opcion=st.selectbox("elije tu fruta favorita", 
                     ["manzana","pera","sandia","durazno"]
                     )
 st.write(f"Tu fruta favorita es: {opcion}")
#####################################
#seleccionar mas de 1 opcion en un desplegable
 opciones = st.multiselect(
   "Selecciona tus colores favoritos",
   ["rojo","verde","azul","amarillo","negro"]

 )
######################################
#slider horizontal!!!

nivel=st.slider(
     "selecciona tu edad",
     min_value=0,
     max_value=100,
     value=25,
     step=1

)
#################################

st.write("Tu nivel de satisfaccion es: ", nivel)

##################################

nivel = st.select_slider(
 "Selecciona tu nivel ed satistaccion",
 options=["muy bajo","bajo","alto","muy alto"],
 value="bajo"
)
st.write("tu nivel de satisfaccion es: "+nivel)

######################################



####################################
 #st.table(df) - tabla

if __name__=="__main__": 
 main()