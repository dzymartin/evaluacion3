# -*- coding: utf-8 -*-
"""Evaluacion2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1F9yDJhdp56u_kDSo1QoGkZF51wfNGrgp

# **Evaluación N°2 - Mineria de datos**
# Integrantes:  
  - Vanessa Salazar
  - Martín Hidalgo
  - Jonatan Sandoval.

# Business Understanding

***Entendiendo el negocio.***

Australia, conocido por su vasto territorio y diversidad climática, enfrenta desafíos únicos en términos de gestión y predicción de precipitaciones debido a su condición de ser uno de los continentes más secos y llanos del planeta. El país se caracteriza por tener una gran variedad de climas que van desde el tropical en el norte hasta el templado-continental en el sureste y Tasmania. A pesar de esto, casi dos tercios del territorio australiano carecen de corrientes de agua hacia el mar, lo que enfatiza la importancia crítica de la previsión y gestión de la lluvia para actividades agrícolas, industriales y de gestión de recursos naturales.

La disponibilidad de datos meteorológicos detallados de la Oficina de Meteorología de la Commonwealth de Australia nos proporciona una oportunidad invaluable para analizar y comprender mejor los patrones de lluvia en diversas regiones del país. En este contexto, la variable objetivo elegida para nuestro análisis es "Rainfall", que representa la cantidad de lluvia registrada en milímetros. Este análisis no solo nos permitirá entender las tendencias históricas y actuales de precipitaciones, sino que también puede ayudar a predecir futuros eventos de lluvia, lo cual es crucial para la planificación agrícola, la gestión de recursos hídricos, y la mitigación de desastres naturales como inundaciones y sequías.

El objetivo principal de este análisis es desarrollar modelos predictivos y descriptivos que puedan proporcionar información útil sobre las precipitaciones diarias en diferentes ubicaciones de Australia. Esto permitirá a las partes interesadas, como agricultores, urbanistas y responsables de políticas medioambientales, tomar decisiones informadas y planificar con mayor precisión sus actividades.

# Data Understanding
"""

# Se realiza la importación y creacion de alias para las librerias a usar.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.impute import KNNImputer
from sklearn.preprocessing import LabelEncoder
from sklearn import preprocessing
import streamlit as st

from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR, SVC
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from sklearn.mixture import GaussianMixture
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Evaluación.
from sklearn.metrics import accuracy_score, mean_squared_error, mean_absolute_error, r2_score

# Pandas: Manipulación y análisis eficientes de datos tabulares como DataFrames, esencial para limpiar y transformar conjuntos de datos.
# NumPy: Computación numérica rápida y eficiente con matrices multidimensionales, ofrece funciones matemáticas para análisis y procesamiento de datos.
# Matplotlib: Creación de gráficos de alta calidad en 2D, permite trazar visualizaciones estáticas e interactivas con amplias opciones de personalización.
# Seaborn: Librería de visualización basada en Matplotlib, simplifica la creación de gráficos estadísticos atractivos y descriptivos.

#Carga de datos.
# Se utiliza esta función para cargar por pantalla el archivo de origen de datos en formato CSV separado por el carcater ;

# Widget para cargar archivos
uploaded_file = st.file_uploader("Choose a file", type=['txt', 'csv'])

if uploaded_file is not None:
    # Procesamiento del archivo cargado
    st.write("File contents:")
    data_frame = uploaded_file.read()
    st.write(data_frame)

# Indica la cantidad de filas y columnas contenidas en el archivo starcraft_duoc.csv
data_frame.shape

# En este caso podermos indentificar que el archivo cargadoc contiene 3395 filas con 20 columnas

# .Head() nos entrega un resumen de todas las columnas contenidas en el dataframe y los 5 primeros registros que se encuentran en este
data_frame.head()

# Revisión de los tipos de datos del archivo
data_frame.dtypes
# Este código nos muestra el tipo de dato por cada una de las columnas.

# Resumen estadisticos para las columnas numéricas
data_frame.describe()
# Muestra datos estadisticos generales de las columnas que contienen datos.

# Variables numéricas
v_num= data_frame.select_dtypes(include=np.number).columns.to_list()
v_num

#Variables categoricas
v_cat= data_frame.select_dtypes(exclude=np.number).columns.to_list()
v_cat

# Identificar valores nulos
for feature in data_frame.columns:
  print('Total de valores nulos para la columna:', feature, '-->', data_frame[feature].isna().sum())

# Con este código podemos analizar los datos e identificar que campos se encuentran con campos nulos.

"""Como se puede apreciar en el comando anterior, hay muchas columnas con valores nulos, por lo que no es conveniente eliminar los nulos, si no que saldría mejor reemplazar por otros valores"""

# Identificar el porcentaje de datos nulos o faltantes para cada columna identificada con nulos
miss = data_frame.isnull().sum()/len(data_frame)
miss = miss[miss > 0]
miss.sort_values(inplace=True)
miss

# Este código muestra el portecentaje de nulos en relacion al total de datos de la fila.

# Proporción de valores faltantes de columnas, caracteristica representa el nombre de las columnas y count la proporcion de valores faltantes
miss = miss.to_frame()
miss.columns = ['count']
miss.index.names = ['Nombre']
miss['Característica'] = miss.index
#
sns.set(style="whitegrid", color_codes=True)
sns.barplot(x = 'Característica', y = 'count', data=miss)
plt.xticks(rotation = 90)
plt.show()

"""En este gráfico podemos apreciar los porcentaje de valores faltantes que tiene cada columna del dataset weatherAUS. Porcentajes que serán trabajados más adelante, luego de identificar y eliminar valores atípicos y imputar dichos valores faltantes"""

# Datos de la variable 'Humidity3pm'
humidity_values = data_frame['Humidity3pm'].values

sampled_data = data_frame['Humidity3pm'].sample(n=100, random_state=1).values

bins = range(0, 101, 10)  # Crear intervalos de 0-10, 10-20, ..., 90-100
humidity_binned = pd.cut(data_frame['Humidity3pm'], bins=bins, right=False)
humidity_counts = humidity_binned.value_counts().sort_index()

# Crear el gráfico de barras
plt.figure(figsize=(10, 6))
plt.bar(humidity_counts.index.astype(str), humidity_counts.values, width=1.0, edgecolor='black')

# Añadir títulos y etiquetas
plt.title('Gráfico de Barras de Humidity3pm')
plt.xlabel('Índice')
plt.ylabel('Humedad a las 3pm (%)')

# Mostrar el gráfico
plt.show()

"""Podemos ver que el gráfico de distribución de la variable Humidity3pm nos muestra que mayormente hay una humedad del 50-60% a las 3 de la tarde."""

# Datos de la variable 'Humidity3pm'
bins = range(0, 101, 10)  # Crear intervalos de 0-10, 10-20, ..., 90-100
humidity_binned = pd.cut(data_frame['Humidity9am'], bins=bins, right=False)
humidity_counts = humidity_binned.value_counts().sort_index()

# Crear el gráfico de barras
plt.figure(figsize=(10, 6))
plt.bar(humidity_counts.index.astype(str), humidity_counts.values, width=1.0, edgecolor='black')

# Añadir títulos y etiquetas
plt.title('Gráfico de Barras de Humidity9am')
plt.xlabel('Humedad a las 9am (%)')
plt.ylabel('Count')

# Mostrar el gráfico
plt.show()

"""El gráfico de barras de humedad a las 9 de la mañana muestra que la mayoría de los registros se encuentran en el rango de 50% a 80%, lo que indica que es común tener una humedad moderada a alta en ese horario.


Al comparar los gráficos de humedad a las 9am y a las 3pm podemos apreciar una disminución general en los niveles de humedad conforme avanza el día. La humedad es más alta en la mañana y disminuye ligeramente por la tarde. Este patrón es típico en muchas regiones climáticas, donde la humedad es mayor por la mañana debido a la condensación y se reduce durante el día debido al aumento de la temperatura y la evaporación.
"""

sampled_data = data_frame['MaxTemp'].sample(n=100, random_state=1).values

bins = range(0, 101, 10)  # Crear intervalos de 0-10, 10-20, ..., 90-100
humidity_binned = pd.cut(data_frame['MaxTemp'], bins=bins, right=False)
humidity_counts = humidity_binned.value_counts().sort_index()

# Crear el gráfico de barras
plt.figure(figsize=(10, 6))
plt.bar(humidity_counts.index.astype(str), humidity_counts.values, width=1.0, edgecolor='black')
#plt.bar(range(len(sampled_data)), sampled_data, width=1.0, edgecolor='black')

# Añadir títulos y etiquetas
plt.title('Gráfico de Barras de MaxTemp')
plt.xlabel('Máxima temperatura registrada')
plt.ylabel('Count')

# Mostrar el gráfico
plt.show()

"""El gráfico de barras de temperaturas máximas muestra que las temperaturas más comúnmente registradas están entre 10°C y 30°C, con muy pocos casos de temperaturas extremas fuera de este rango. Esto podría ser indicativo de un clima moderado en la región o al menos en las estaciones del año durante las cuales los datos fueron recopilados."""

# Contar la frecuencia de cada categoría
category_counts = data_frame['RainToday'].value_counts()

# Crear el gráfico de barras
plt.figure(figsize=(6, 4))
plt.bar(category_counts.index, category_counts.values, color=['darkblue', 'blue'], edgecolor='black')

# Añadir títulos y etiquetas
plt.title('Gráfico de Barras de Lluvia hoy')
plt.xlabel('Lluvia hoy')
plt.ylabel('Count')

# Mostrar el gráfico
plt.show()

# Contar la frecuencia de cada categoría
category_counts = data_frame['RainTomorrow'].value_counts()

# Crear el gráfico de barras
plt.figure(figsize=(6, 4))
plt.bar(category_counts.index, category_counts.values, color=['darkblue', 'blue'], edgecolor='black')

# Añadir títulos y etiquetas
plt.title('Gráfico de Barras de Lluvia mañana')
plt.xlabel('Lluvia mañana')
plt.ylabel('Count')

# Mostrar el gráfico
plt.show()

"""Al analizar la fecuencia de probabilidades para las variables RainToday y RainTomorrow, podemos inferir que es muy probable que si un día no llueve, al otro tampoco. Claramente en algún momento se rompe este ciclo, pero por lo que vemos en el gráfico no varía si llovió o no (ni hoy, ni mañana)"""

# Guardamos en la variable numeric_data todas las columnas del dataset de starcraft que son de tipo numericas.
v_num = data_frame.select_dtypes(include=[np.number])

#Visualizamos la correlacion entre las columnas.
# El grafico de calor nos puestra la correlación entre los datos. Donde los colores más intensos muestran una correalción mas distante entre
# Los datos y los colores más claros una relación más cercana con los datos.
corr = v_num.corr()
sns.heatmap(corr)

# Extraer las correlaciones específicas con 'Rainfall'
rainfall_correlations = corr['Rainfall'].sort_values(ascending=False)

# Imprimir las correlaciones con 'Rainfall'
print("Correlaciones de 'Rainfall' con otras variables numéricas:")
rainfall_correlations

"""# Data Preparation"""

# Eliminaremos los outliers o 'Valores atípicos' que identifiquemos en nuestra variable objetivo

# Identificando valores atípicos
Q1 = data_frame['Rainfall'].quantile(0.25)
Q3 = data_frame['Rainfall'].quantile(0.75)
IQR = Q3 - Q1

outliers = data_frame[(data_frame['Rainfall'] < (Q1 - 1.5 * IQR)) | (data_frame['Rainfall'] > (Q3 + 1.5 * IQR))]

print("Outliers:")
outliers

"""Este bloque de código fue diseñado para identificar valores atípicos (o outliers) en la columna Rainfall del data set weatherAUS. Se utilizó el método del rango intercuartílico (IQR) para detectar estos valores atípicos."""

# Eliminando valores atípicos
df_sin_outliers = data_frame.drop(outliers.index)
df_sin_outliers.shape

# Imputación de datos (relleno datos faltantes)
# vamos a crear una copia de los datos originales
data_knn = df_sin_outliers.copy()
data_knn = pd.DataFrame(data_knn)
data_knn

# Creamos un objeto de KNN imputer. con 3 vecinos y parámetro weights = uniform.
knn_imputer = KNNImputer(n_neighbors=3, weights="uniform")

# Identificar el porcentaje de datos nulos o faltantes para cada columna identificada con nulos
# ***Al data_frame original, el cual contiene los registros con valores nulos o faltantes, para así luego ver la comparación con el data_frame3.
miss = data_frame.isnull().sum()/len(data_frame)
miss = miss[miss > 0]
miss.sort_values(inplace=True)
miss

data_knn[['Rainfall']] = knn_imputer.fit_transform(data_knn[['Rainfall']])
data_knn

"""En este bloque de código se utiliza una técnica llamada KNN (K-Nearest Neighbors) para imputar o rellenar los valores faltantes en la columna Rainfall del DataFrame llamado data_knn."""

a = data_knn['MinTemp']
b = data_knn['MaxTemp']
c = data_knn['Evaporation']
d = data_knn['Sunshine']
h = data_knn['WindGustSpeed']
i = data_knn['WindSpeed9am']
j = data_knn['WindSpeed3pm']
k = data_knn['Humidity9am']
l = data_knn['Humidity3pm']
m = data_knn['Pressure9am']
n = data_knn['Pressure3pm']
o = data_knn['Cloud9am']
p = data_knn['Cloud3pm']
q = data_knn['Temp9am']
r = data_knn['Temp3pm']

prom_a = a.mean()
prom_b = b.mean()
prom_c = c.mean()
prom_d = d.mean()
prom_h = h.mean()
prom_i = i.mean()
prom_j = j.mean()
prom_k = k.mean()
prom_l = l.mean()
prom_m = m.mean()
prom_n = n.mean()
prom_o = o.mean()
prom_p = p.mean()
prom_q = q.mean()
prom_r = r.mean()

diccionario = {'MinTemp': prom_a, 'MaxTemp': prom_b, 'Evaporation': prom_c, 'Sunshine': prom_d, 'WindGustSpeed': prom_h, 'WindSpeed9am': prom_i, 'WindSpeed3pm': prom_j, 'Humidity9am': prom_k, 'Humidity3pm': prom_l, 'Pressure9am': prom_m, 'Pressure3pm': prom_n, 'Cloud9am': prom_o, 'Cloud3pm': prom_p, 'Temp9am': prom_q, 'Temp3pm': prom_r}

data_frame3 = data_knn.fillna(diccionario)
data_frame3

"""Para el resto de las variables rellenamos sus vacíos con la media de cada variable simplemente."""

# Transformamos las variables categoricas a numéricas utilizando la clase LabelEncoder.

label_encoder = preprocessing.LabelEncoder()

data_frame3['Date'] = label_encoder.fit_transform(data_frame3['Date'])
data_frame3['WindGustDir'] = label_encoder.fit_transform(data_frame3['WindGustDir'])
data_frame3['WindDir9am'] = label_encoder.fit_transform(data_frame3['WindDir9am'])
data_frame3['WindDir3pm'] = label_encoder.fit_transform(data_frame3['WindDir3pm'])
data_frame3['Location'] = label_encoder.fit_transform(data_frame3['Location'])
data_frame3['RainTomorrow'] = label_encoder.fit_transform(data_frame3['RainTomorrow'])
data_frame3['RainToday'] = label_encoder.fit_transform(data_frame3['RainToday'])

# Buscamos nulos en el data_frame luego de realizar las tecnicas de eliminacion de valores atípicos e imputación.
data_frame3.isnull().sum()

# Identificar el porcentaje de datos nulos o faltantes para cada columna identificada con nulos **Al data_frame3, el cual ya no contiene nulos, ni outliers
miss = data_frame3.isnull().sum()/len(data_frame3)
miss = miss[miss > 0]
miss.sort_values(inplace=True)
miss

# Este código muestra el portecentaje de nulos en relacion al total de datos de la fila.

# Proporción de valores faltantes de columnas, caracteristica representa el nombre de las columnas y count la proporcion de valores faltantes

# Luego de imputar todas las variables del data_frame y remover valores atípicos, podemos ver que tenemos 0% de datos faltantes en el siguiente gráfico.

miss = miss.to_frame()
miss.columns = ['count']
miss.index.names = ['Nombre']
miss['Característica'] = miss.index

sns.set(style="whitegrid", color_codes=True)
sns.barplot(x = 'Característica', y = 'count', data=miss)
plt.xticks(rotation = 90)
plt.show()

"""# Modeling"""

# Seleccionar las características (X) y la variable objetivo (y)
X = data_frame3.drop('Rainfall', axis=1)
y = data_frame3['Rainfall']

# Dividir el conjunto de datos en entrenamiento (80%) y prueba (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Verificamos contenido de los conjuntos de datos divididos:
print(f'Valores NaN en X_train:\n{np.isnan(X_train).sum()}')
print(f'Valores NaN en y_train:\n{np.isnan(y_train).sum()}')
print(f'Valores NaN en X_test:\n{np.isnan(X_test).sum()}')
print(f'Valores NaN en y_test:\n{np.isnan(y_test).sum()}')

"""## **Implementación de modelos supervisados**"""

# Regresión Lineal

# Crear y entrenar el modelo de regresión lineal
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)
linear_predictions = linear_model.predict(X_test)

# Calcular métricas de regresión lineal
linear_rmse = np.sqrt(mean_squared_error(y_test, linear_predictions))
linear_mse = mean_squared_error(y_test, linear_predictions)
linear_mae = mean_absolute_error(y_test, linear_predictions)
linear_r2 = r2_score(y_test, linear_predictions)

# Imprimir métricas de regresión lineal
print(f'Regresión Lineal Metrics:')
print(f'RMSE: {linear_rmse}')
print(f'MSE: {linear_mse}')
print(f'MAE: {linear_mae}')
print(f'R^2 Score: {linear_r2}')

# KNN

# Crear y entrenar el modelo de KNN para regresión
knn_model = KNeighborsRegressor()
knn_model.fit(X_train, y_train)
knn_predictions = knn_model.predict(X_test)

# Calcular métricas de KNN
knn_rmse = np.sqrt(mean_squared_error(y_test, knn_predictions))
knn_mse = mean_squared_error(y_test, knn_predictions)
knn_mae = mean_absolute_error(y_test, knn_predictions)
knn_r2 = r2_score(y_test, knn_predictions)

# Imprimir métricas de KNN
print(f'\nKNN Metrics:')
print(f'RMSE: {knn_rmse}')
print(f'MSE: {knn_mse}')
print(f'MAE: {knn_mae}')
print(f'R^2 Score: {knn_r2}')

# Arboles De Decisión

# Crear y entrenar el modelo de árbol de decisión para regresión
tree_model = DecisionTreeRegressor()
tree_model.fit(X_train, y_train)
tree_predictions = tree_model.predict(X_test)

# Calcular métricas de árbol de decisión
tree_rmse = np.sqrt(mean_squared_error(y_test, tree_predictions))
tree_mse = mean_squared_error(y_test, tree_predictions)
tree_mae = mean_absolute_error(y_test, tree_predictions)
tree_r2 = r2_score(y_test, tree_predictions)

# Imprimir métricas de árbol de decisión
print(f'\nÁrbol de Decisión Metrics:')
print(f'RMSE: {tree_rmse}')
print(f'MSE: {tree_mse}')
print(f'MAE: {tree_mae}')
print(f'R^2 Score: {tree_r2}')

# Random Forest

# Crear y entrenar el modelo de bosques aleatorios para regresión
forest_model = RandomForestRegressor()
forest_model.fit(X_train, y_train)
forest_predictions = forest_model.predict(X_test)

# Calcular métricas de bosques aleatorios
forest_rmse = np.sqrt(mean_squared_error(y_test, forest_predictions))
forest_mse = mean_squared_error(y_test, forest_predictions)
forest_mae = mean_absolute_error(y_test, forest_predictions)
forest_r2 = r2_score(y_test, forest_predictions)

# Imprimir métricas de bosques aleatorios
print(f'\nBosques Aleatorios Metrics:')
print(f'RMSE: {forest_rmse}')
print(f'MSE: {forest_mse}')
print(f'MAE: {forest_mae}')
print(f'R^2 Score: {forest_r2}')

"""## **Implementación de modelos no supervisados**"""

# K-MEANS
# Escalar los datos
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_train)

# Crear y entrenar el modelo de K-Means
kmeans_model = KMeans(n_clusters=3, random_state=42)
kmeans_model.fit(X_scaled)

# Obtener los clusters asignados y los centroides
clusters = kmeans_model.labels_
centroids = kmeans_model.cluster_centers_

# Calcular las distancias de los puntos a sus centroides asignados
distances = np.linalg.norm(X_scaled - centroids[clusters], axis=1)

# Obtener las etiquetas de los clusters
kmeans_labels = kmeans_model.labels_

# Calcular MSE, RMSE y MAE
mse = np.mean(distances**2)
rmse = np.sqrt(mse)
mae = np.mean(distances)

# Evaluar los clusters usando Silhouette Score
silhouette_avg = silhouette_score(X_scaled, clusters)

# Imprimir métricas de K-Means
print(f'\nK-Means Metrics:')
print(f'MSE: {mse}')
print(f'RMSE: {rmse}')
print(f'MAE: {mae}')
print(f'Silhouette Score: {silhouette_avg}')
print(f'Cluster Centers:\n {centroids}')

# DBSCAN

# Escalar los datos
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_train)

# Crear y entrenar el modelo de DBSCAN
dbscan_model = DBSCAN(eps=0.5, min_samples=5)
dbscan_model.fit(X_scaled)

# Obtener los clusters asignados y los puntos de ruido
clusters = dbscan_model.labels_
n_clusters = len(set(clusters)) - (1 if -1 in clusters else 0)
n_noise = list(clusters).count(-1)

# Obtener las etiquetas de los clusters
dbscan_labels = dbscan_model.labels_

# Calcular las métricas de evaluación
if n_clusters > 1:
    silhouette_avg = silhouette_score(X_scaled, clusters)
    db_index = davies_bouldin_score(X_scaled, clusters)
    ch_index = calinski_harabasz_score(X_scaled, clusters)
else:
    silhouette_avg = -1
    db_index = -1
    ch_index = -1

# Imprimir métricas de DBSCAN
print(f'\nDBSCAN Metrics:')
print(f'Número de clusters: {n_clusters}')
print(f'Número de puntos ruidosos: {n_noise}')
print(f'Silhouette Score: {silhouette_avg}')
print(f'Davies-Bouldin Index: {db_index}')
print(f'Calinski-Harabasz Index: {ch_index}')

# GMM

# Crear y entrenar el modelo GMM
gmm = GaussianMixture(n_components=5, random_state=42)
gmm.fit(X_scaled)

# Obtener las etiquetas de los clusters
gmm_labels = gmm.predict(X_scaled)

# Calcular métricas de evaluación
gmm_silhouette = silhouette_score(X_scaled, gmm_labels)
gmm_calinski_harabasz = calinski_harabasz_score(X_scaled, gmm_labels)
gmm_davies_bouldin = davies_bouldin_score(X_scaled, gmm_labels)

# Imprimir las métricas de evaluación
print(f'GMM Metrics:')
print(f'Silhouette Score: {gmm_silhouette}')
print(f'Calinski-Harabasz Index: {gmm_calinski_harabasz}')
print(f'Davies-Bouldin Index: {gmm_davies_bouldin}')

"""## Validar modelos supervisados

Para poder ser capaz de determinar el mejor modelo entre los que hemos implementado, compararemos el resultado de las metricas de cada uno de los modelos, las cuales son:

- RMSE (Root Mean Squared Error)
- MSE (Mean Squared Error)
- MAE (Mean Absolute Error)
- R² Score (Coefficient of Determination)

RMSE: El valor más bajo indica mejor ajuste del modelo. Bosques Aleatorios tiene el menor RMSE (0.1903).

MSE: Similar al RMSE, un valor más bajo es mejor. Nuevamente, Bosques Aleatorios tiene el menor MSE (0.0362).

MAE: Valor más bajo es mejor, ya que indica menor error absoluto medio. Bosques Aleatorios tiene el menor MAE (0.1139).

R² Score: Un valor más alto indica mejor ajuste del modelo. El Bosque Aleatorio tiene el mayor R² Score (0.7595).

En conclusión podemos decir que el mejor modelo para este contexto es el del Bosque aleatorio o random forest al comparar el resultado de sus metricas con los demás modelos supervisados
"""

# Instalar Streamlit

#pip install streamlit

# Implementar Random Forest

# Definir variable target
target_column = 'Rainfall'

# Dividir los datos en características (X) y objetivo (y)
X = data_frame3[['Cloud3pm', 'Cloud9am', 'Date', 'Evaporation', 'Humidity3pm']]  # Use actual feature names from your training data
y = data_frame3[target_column]

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar el modelo
forest_model = RandomForestRegressor(random_state=42)
forest_model.fit(X_train, y_train)

# Implementar el panel de control
st.title('Predicción de Precipitaciones con Bosques Aleatorios')

st.sidebar.header('Configuración de Entrada')

def user_input_features():
    cloud3pm = st.sidebar.slider('Cloud3pm', min_value=0.0, max_value=1.0, value=0.5)
    cloud9am = st.sidebar.slider('Cloud9am', min_value=0.0, max_value=1.0, value=0.5)
    date = st.sidebar.slider('Date', min_value=0.0, max_value=1.0, value=0.5)
    evaporation = st.sidebar.slider('Evaporation', min_value=0.0, max_value=1.0, value=0.5)
    humidity3pm = st.sidebar.slider('Humidity3pm', min_value=0.0, max_value=1.0, value=0.5)

    data = {'Cloud3pm': cloud3pm, 'Cloud9am': cloud9am, 'Date': date, 'Evaporation': evaporation, 'Humidity3pm': humidity3pm}
    features = pd.DataFrame(data, index=[0])
    return features

input_df = user_input_features()

# Mostrar las características de entrada
st.subheader('Características de Entrada')
st.write(input_df)

# Realizar predicciones
prediction = forest_model.predict(input_df)

st.subheader('Predicción de Precipitaciones')
st.write(prediction)

# Evaluar el modelo en los datos de prueba

forest_predictions = forest_model.predict(X_test)
forest_rmse = np.sqrt(mean_squared_error(y_test, forest_predictions))
forest_mse = mean_squared_error(y_test, forest_predictions)
forest_mae = mean_absolute_error(y_test, forest_predictions)
forest_r2 = r2_score(y_test, forest_predictions)

# Mostrar métricas de rendimiento
st.subheader('Métricas de Rendimiento del Modelo')
st.write(f'RMSE: {forest_rmse}')
st.write(f'MSE: {forest_mse}')
st.write(f'MAE: {forest_mae}')
st.write(f'R² Score: {forest_r2}')

# Evaluar el modelo en los datos de prueba

forest_predictions = forest_model.predict(X_test)
forest_rmse = np.sqrt(mean_squared_error(y_test, forest_predictions))
forest_mse = mean_squared_error(y_test, forest_predictions)
forest_mae = mean_absolute_error(y_test, forest_predictions)
forest_r2 = r2_score(y_test, forest_predictions)

# Mostrar métricas de rendimiento
st.subheader('Métricas de Rendimiento del Modelo')
st.write(f'RMSE: {forest_rmse}')
st.write(f'MSE: {forest_mse}')
st.write(f'MAE: {forest_mae}')
st.write(f'R² Score: {forest_r2}')

