import streamlit as st
import pandas as pd
import numpy as np 
import urllib.request

st.title('Datos Hidrometereológicos del Gobierno Regional Piura')


from PIL import Image
image = Image.open('Hidro.jpg')
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
aux = dt

# lista_x = []
# a = list(dt['FECHA_MUESTRA'])
# for i in a:
#   lista_x.append((str(i))[:4] + '-' + (str(i))[4:6] + '-' + (str(i))[6:])


##con el texto justificado :3
st.markdown("""<div style="text-align: justify;">
	Este dataset muestra los datos hidrometereológicos registrados de las presas, 
	estaciones hidrológicas e hidrométricas de la región de Piura. 
	La importancia de conocer datos hidrometereológicos se refleja en la prevención
	de desastres naturales.
	\n\nTener en cuenta que, de la base de datos que rescatamos, no tenemos información de
	la capacidad máxima del caudal que tiene como máximo una determinada cuenca.
	Los datos se muestra está para el uso a disposición para analizar de manera 
	independiente cada una.
	\n\n- **Base de Datos:** _última actualización: 2022-11-06_
	</div>
	https://www.datosabiertos.gob.pe/node/10105/
	
	""",unsafe_allow_html=True)


st.header('Dataset Hidrometereológico')  #MODIFICACIÓN
st.dataframe(dt) #MODIFICACIÓN 

st.header('Resumen del dataset')
dt = dt.drop( ##eliminamos columnas de las que no nos pueden beneficiar 
	#	para la visualización del resumen total
	columns=['FECHA_CORTE', 'FECHA_MUESTRA', 'UNIDAD_MEDIDA', 'DEPARTAMENTO', 'UBIGEO'], axis=1)
st.dataframe(dt.describe())

st.markdown("""<div style="text-align: justify;"> 
	Para la tabla anterior refleja un total de los datos en el que fueron captados 
	en diferentes cuencas de la región mencionada (Piura).
	
	\n_count_: es un total o sumatoria de las cuencas
	\n_mean_: media o promedio de los datos obtenidos 
	\n_std_: representa mi desviación estándar 
	\n_min_: el valor mínimo de todas las observaciones de la región
	\n_25%_: El percentil 25 o cuartil 1 
	\n_50%_: El percentil 50 o cuartil 2
	\n_75%_: El percentil 75 o cuartil 3
	\n\tLos percentiles son porcentajes en la ocurrencia de los datos \nmenor que o igual a este valor.
	\n_max_: el valor máximo de todas las observaciones de la región
	</div>
	""",unsafe_allow_html=True)



st.header('Estadistica Hidrometereológica del tipo de estación')

#selectbox de tipo de estaciones 
lista_tipo_estacion = []
for elem in dt['TIPO_ESTACION'].unique():
  lista_tipo_estacion.append(elem)

op1 = st.selectbox('- Seleccione el tipo de estación', tuple(sorted(lista_tipo_estacion)))
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
## separamos las fechas por un 


for i in range(0, 4):
	graf = pd.DataFrame(df_provincia , columns=[datos_hidro[i]])
	st.subheader('Grafico de ' + datos_hidro[i])#(st.caption('Grafico de ' + datos_hidro[i]))
	st.line_chart(graf)#################################################################
	st.caption('x = índice de la fila del dataframe o dataset\n		y = valor obtenido en la observación')
#
grupo = dt.groupby(dt.PROVINCIA)
provincia = grupo.get_group(op2)


cont_distrito = provincia.iloc[:,5:].max()



st.subheader("Datos hidrometereológicos del distrito seleccionado - Resume") 
#####################
column_ , column__ = st.columns(2)
with column_:
	
    st.write('valores máximos y mínimos captados')
# with column__:
	
#     st.write('valores mínimos captados')
#	se cambió pq te fusionó ambas tablitas de max y min
###################


# with column1:
	
#     st.dataframe(cont_distrito)
# with column2:
	
#     st.dataframe(provincia.iloc[:,5:].min())


aus = pd.DataFrame({'Max': provincia.iloc[:,5:].max(), 'Min': provincia.iloc[:,5:].min()})
st.write(aus)

# st.write('los datos mecionados del maximo corresponden a: \nMáximo\n', dt.loc[dt ['CAUDAL07H']  == aus["CAUDAL07H"]["max"]],
# dt.loc[dt ['']  == aus["CAUDAL07H"]["max"]]
# )
st.markdown("""
En los estadísticos siguientes, se muestra según la selección por el usuario (en la lista de opciones anterior),
\n_count_: es un total o sumatoria de las observaciones de la cuenca anteriormente seleccionada
\n_mean_: media o promedio de los datos obtenidos 
\n_std_: variabilidad de mis observaciones respecto a la media de los datos obtenidos en la cuenca
\n_min_: el valor mínimo de todas las observaciones de la cuenca según mis variables que se muestran en el encabezado
\n_25%_ De la ocurrencia de mis datos es menor al valor mostrado
\n_50%_ De la ocurrencia de mis datos es menor al valor mostrado
\n_75%_: De la ocurrencia de mis datos es menor al valor mostrado
\n\tlos porcentajes son mis percentiles o cuartiles 1,2,3 respectivamente.
\n_max_: el valor máximo de todas las observaciones de la cuenca según las variables que se muestran en el encabezado

"""
)

st.write(provincia.iloc[:,5:].describe())

st.subheader("Gráficos interactivos")
st.bar_chart(cont_distrito.describe())
#S

op_multi = st.multiselect(
    "Seleccione las provincias que desea comparar", 
    options= dt["PROVINCIA"].unique()
    )

x = dt.set_index("PROVINCIA")
y = x.loc[op_multi]

st.dataframe(y)
z = x.loc[op_multi,"PROMEDIO24H"]

st.bar_chart(z)

st.write("""Caudal: es el volumen de agua por unidad de tiempo que pasa por una sección de un
cauce. _Las unidades en las que se mide es en """)
st.latex("m/s^3")
st.write(
"""\n
- Las observaciones han sido obtenidas en diferentes fechas
- El caudal ha sido tomado cada 7 horas
- El promedio es referente al cauda durante 24 horas
- Maximo valor del caudal en el periodo de 24 horas
- Precipitación en 24 horas
""")




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

