import streamlit as st
import pandas as pd
import numpy as np 
import urllib.request



# id= 1wdbF1i-8jdePmWt1Hf7p6DuZJpaUE3Je
@st.experimental_memo 
def download_data():
	#https://drive.google.com/uc?id=YOURFILEID
	url =  "https://drive.google.com/uc?id=1wdbF1i-8jdePmWt1Hf7p6DuZJpaUE3Je"
	output= 'data.xls'
	gdown.download(url,output,quiet = False)
	





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

st.header('Gráficos por distrito según dato Hidrometereológico')

#selectbox de provincias
lista_provincia = []
for elem in dt['PROVINCIA'].unique():
  lista_provincia.append(elem)

#op2 = st.selectbox('- Seleccione la provincia', tuple(sorted(lista_provincia)))

#selectbox de distritos
lista_distrito = []
for elem in dt['DISTRITO'].unique():
  lista_distrito.append(elem)

op3 = st.selectbox('- Seleccione el distrito', tuple(sorted(lista_distrito)))
st.write('Distrito seleccionada:', op3)


#df_provincia = dt[dt['PROVINCIA'] == op2]
df_distrito = dt[dt['DISTRITO'] == op3]

datos_hidro = ['CAUDAL07H', 'PROMEDIO24H', 'MAXIMA24H', 'PRECIP24H']

for i in range(0, 4):
	graf = pd.DataFrame(df_distrito , columns=[datos_hidro[i]])
	st.caption('Grafico de ' + datos_hidro[i])
	st.line_chart(graf)

#
grupo = dt.groupby(dt.PROVINCIA)
provincia = grupo.get_group(op3)

cont_distrito = provincia.iloc[:,5:]

st.subheader("Datos hidrológicos del distrito seleccionado") 
st.dataframe(cont_distrito)

st.subheader("Gráficos interactivos")
st.bar_chart(cont_distrito.mean())
#

op_multi = st.multiselect(
    "Seleccione las provincias que desea comparar", 
    options= dt["PROVINCIA"].unique()
    )

x = dt.set_index("PROVINCIA")
y = x.loc[op_multi]

st.dataframe(y)
z = x.loc[op_multi,"PROMEDIO24H"]

st.bar_chart(z)
