import streamlit as st
import pandas as pd
import numpy as np 
import urllib.request

st.title('Datos Hidrometereológicos del Gobierno Regional Piura')

#id = 1alnmXxvcOvu3o3UxL_41YwNmdLczgN1u

@st.experimental_memo 
def download_data():
	url = 'https://www.datosabiertos.gob.pe/node/10105/download'
	filename = 'datos_piura.csv'
	#https://drive.google.com/uc?id=1alnmXxvcOvu3o3UxL_41YwNmdLczgN1u
	#url = 'https://drive.google.com/uc?id=1alnmXxvcOvu3o3UxL_41YwNmdLczgN1u'
	#gdown.download(url, filename, quiet=False)
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

#selectbox de tipo de estaciones 
lista_tipo_estacion = []
for elem in dt['TIPO_ESTACION'].unique():
  lista_tipo_estacion.append(elem)

st.header('Seleccione los siguientes apartados para determinar el grafico')
#mostrar las opciones
op1 = st.selectbox('- Seleccione el tipo de estacion', tuple(sorted(lista_tipo_estacion)))
st.write('Tipo de estacion seleccionada:', op1.capitalize())

#selectbox de provincia
lista_provincia = []
for item in dt['PROVINCIA'].unique():
	lista_provincia.append(item)

op2 = st.selectbox('- Seleccione la provincia', tuple(sorted(lista_provincia)))
st.write('Provincia seleccionada:', op2)

#selectbox de distrito
lista_distrito = []	
for comp in dt['DISTRITO'].unique():
	lista_distrito.append(comp)

op3 = st.selectbox('- Seleccion el distrito', tuple(sorted(lista_distrito)))
st.write('Distrito seleccionado:', op3)

#agrupar la respuesta de los selectbox
df_total = dt[dt['TIPO_ESTACION'] == op1]
df_provincia = df_total[df_total['PROVINCIA'] == op2]
df_agrupado = df_total[df_total['DISTRITO'] == op3]

#Graficos

#grafico de lineas

st.subheader('Grafico de Lineas')
graf1 = pd.DataFrame(
    df_agrupado,
    columns=['CAUDAL07H', 'PROMEDIO24H', 'MAXIMA24H', 'PRECIP24H'])
st.line_chart(graf1)

#grafico de barras
st.subheader('Grafico de barras')
graf2 = pd.DataFrame(
    df_agrupado,
    columns=['CAUDAL07H', 'PROMEDIO24H', 'MAXIMA24H', 'PRECIP24H'])
st.bar_chart(graf2)