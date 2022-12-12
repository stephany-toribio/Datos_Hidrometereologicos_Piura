import streamlit as st
import pandas as pd
import numpy as np 
import urllib.request

st.title('Datos Hidrometereológicos del Gobierno Regional Piura')


from PIL import Image
image = Image.open('contaminacion.jpeg')
st.image(image, caption='Distribución de las estaciones en el Proyecto Especial Chira Piura', use_column_width=True)


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
	El norte del país se encuentra instalado el Proyecto Especial Chira Piura, que se encarga de la administración de los recursos hídricos 
	provenientes de los Valles del Chira y Piura, el fin de esto es el abastecimiento de agua para el sector agrícola que se desarrolla en la zona.
	Ellos cuentan con 27 estaciones o puntos de toma del caudal de los ríos en cuestión y las precipitaciones que sobre estos influyen, 
	por lo que el presente proyecto pretende sistematizar esta información para brindar gráficas que permitan comprender de manera más amigable 
	el comportamiento de los ríos Chira y Piura, a fin de lograr una toma de decisiones más eficiente por parte de las personas implicadas en el sector agrícola.
	Este dataset muestra los datos hidrometereológicos registrados de las presas, estaciones hidrológicas e hidrométricas.
	- **Base de Datos:** (https://www.datosabiertos.gob.pe/node/10105/download)''')



st.header('Dataset Hidrometereológico')
st.dataframe(dt)

st.header('Resumen del dataset')
dt = dt.drop(columns=['UNIDAD_MEDIDA', 'DEPARTAMENTO', 'UBIGEO'], axis=1)
st.dataframe(dt.describe())

st.header('Estadistica Hidrometereológica del tipo de estacion')
 

op1 = st.selectbox('- Seleccione el tipo de estacion', sorted(dt['TIPO_ESTACION'].unique()))
st.write('Tipo de estacion seleccionada:', op1.capitalize())

df_tipo = dt[dt['TIPO_ESTACION'] == op1]

st.line_chart(pd.DataFrame(
    df_tipo,
    columns=['CAUDAL07H', 'PROMEDIO24H', 'MAXIMA24H', 'PRECIP24H']))

st.header('Data Hidrometereológica del distrito seleccionado')


op2 = st.selectbox('- Seleccione el distrito', sorted(dt['DISTRITO'].unique()))
st.write('Distrito seleccionado: ', op2)

grupo = dt.groupby(dt.DISTRITO)
distrito = grupo.get_group(op2)

cont_distrito = distrito.iloc[:,5:]

st.dataframe(cont_distrito)

st.write(pd.DataFrame({'Max': distrito.iloc[:,5:].max(), 'Min': distrito.iloc[:,5:].min()}))

st.subheader("- Gráficos interactivos")
st.bar_chart(cont_distrito.mean())

df_distrito = dt[dt['DISTRITO'] == op2]

datos_hidro = ['CAUDAL07H', 'PROMEDIO24H', 'MAXIMA24H', 'PRECIP24H']

for i in range(0, 4):
	graf = pd.DataFrame(df_distrito , columns=[datos_hidro[i]])
	st.caption('Grafico de ' + datos_hidro[i])
	st.line_chart(graf)

st.header('Filtro de data Hidrometereológica por distrito')

op_multi = st.multiselect(
    "- Distritos", 
    options= dt["DISTRITO"].unique()
    )

op_dato = st.selectbox('- Dato Hidrometereológico', sorted(datos_hidro))

x = dt.set_index("DISTRITO")
y = x.loc[op_multi]

st.dataframe(y)
z = x.loc[op_multi, op_dato]

st.bar_chart(z)


@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

csv = convert_df(y)

st.download_button(
    label="Download",
    data=csv,
    file_name='Descargar archivo.csv',
    mime='text/csv',
)


st.write("""Notas: 
""")
st.write(
"""\n
- Las observaciones han sido obtenidas en diferentes fechas
- El caudal ha sido tomado a las 7 horas
- El promedio es referente al cauda durante 24 horas
- Maximo valor del caudal en el periodo de 24 horas
- Precipitación en 24 horas
""")



