
import streamlit as st
import pandas as pd
import numpy as np 
import urllib.request

#Nikolai#
excel_file = '11122022_bd_hdro_piura.csv'   #Nombre archivo a importar 
sheet_name = '11122022_bd_hdro_piura'   #la hoja de excel que voy a importar

df = pd.read_excel(excel_file, #importo el archivo excel
                   sheet_name = sheet_name, #le digo cual hoja necesito
                   usecols = 'A:O', #Columnas que quiero usar
                   header =0) #desde que fila debe empezar a tomarme la informacion *Empieza a contar desde 0*

df_CUENTA = df.groupby(['CT'], as_index = False)['CUENTA'].count()  #hago un tipo de TABLA DINAMICA para agrupar los datos

df_CUENTA2 = df_CUENTA

st.dataframe(df) #de esta forma nos va a mostrar el dataframe en Streamlit
st.write(df_CUENTA2) #este nos sirve cuando no tenemos dataframe 



#Crear un grafico de torta (pie chart)
pie_chart = px.pie(df_CUENTA2, #tomo el dataframe2
                   title = 'TIPOS DE CUENTA', #El titulo
                   values = 'CUENTA',##columna
                   names = 'CT') ## para verlo por EPS --> Colores

st.plotly_chart(pie_chart) # de esta forma se va a mostrar el dataframe en Streamlit








st.title('Datos Hidrometereológicos del Gobierno Regional Piura')

#id = 1alnmXxvcOvu3o3UxL_41YwNmdLczgN1u

@st.experimental_memo 
def download_data():
	url = 'https://www.datosabiertos.gob.pe/node/10105/download'
	filename = 'datos_piura.csv'
	urllib.request.urlretrieve(url, filename)
	df = pd.read_csv(filename)
	return df 

dt = download_data()

st.markdown('''
	Este dataset muestra los datos hidrometereológicos registrados de las presas, estaciones hidrológicas e hidrométricas.
	- **Base de Datos:** (https://www.datosabiertos.gob.pe/node/10105/download)''')

st.header('Dataset Hidrometereológico')
st.dataframe(dt)

st.header('Resumen del dataset')
dt = dt.drop(columns=['FECHA_CORTE', 'FECHA_MUESTRA', 'UNIDAD_MEDIDA', 'DEPARTAMENTO', 'UBIGEO'], axis=1)
st.dataframe(dt.describe())

st.header('Estadistica Hidrometereológica del tipo de estacion')

#selectbox de tipo de estaciones 
lista_tipo_estacion = []
for elem in dt['TIPO_ESTACION'].unique():
  lista_tipo_estacion.append(elem)

op1 = st.selectbox('- Seleccione el tipo de estacion', tuple(sorted(lista_tipo_estacion)))
st.write('Tipo de estacion seleccionada:', op1.capitalize())

#grafico del tipo de estaciones
df_tipo = dt[dt['TIPO_ESTACION'] == op1]

graf1 = pd.DataFrame(
    df_tipo,
    columns=['CAUDAL07H', 'PROMEDIO24H', 'MAXIMA24H', 'PRECIP24H'])
st.line_chart(graf1)

st.header('Grafico de provincia por dato Hidrometereológico')

#selectbox de provincias
lista_provincia = []
for elem in dt['PROVINCIA'].unique():
  lista_provincia.append(elem)

op2 = st.selectbox('- Seleccione la provincia', tuple(sorted(lista_provincia)))

#selectbox de distritos
lista_distrito = []
for elem in dt['DISTRITO'].unique():
  lista_distrito.append(elem)

op3 = st.selectbox('- Seleccione el distrito', tuple(sorted(lista_distrito)))
st.write('Distrito seleccionada:', op3)


df_provincia = dt[dt['PROVINCIA'] == op2]
df_distrito = dt[dt['DISTRITO'] == op3]

datos_hidro = ['CAUDAL07H', 'PROMEDIO24H', 'MAXIMA24H', 'PRECIP24H']
columnas = [df_provincia, df_distrito]

for j in range(0,2):
	for i in range(0, 4):
		graf = pd.DataFrame(columnas[j], columns=[datos_hidro[i]])
		st.caption('Grafico de ' + datos_hidro[i])
		st.line_chart(graf)
		
		
op_multi = st.multiselect(
    "Seleccione las provincias que desea comparar", 
    options= dt["PROVINCIA"].unique()
    )

x = dt.set_index("PROVINCIA")
y = x.loc[op_multi]

st.dataframe(y)
z = x.loc[op_multi,"CAUDAL07H"]

st.bar_chart(z)







