
from geopy.geocoders import Nominatim
import time
import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt

df = pd.read_csv(r'/workspaces/STR_TP2/Dados/HIST_PAINEL_COVIDBR_2024_Parte2_24ago2024.csv', delimiter=';', encoding='UTF-8')
df['data'] = pd.to_datetime(df['data'])
df['mes'] = df['data'].dt.to_period('M').astype(str)

df_plot = df[(df['mes'] == max(df['mes'])) & (df['estado'] == 'RJ')]
df_plot = df_plot.groupby(['estado','municipio'])['casosAcumulado'].sum().reset_index()

geolocator = Nominatim(user_agent="geoapiExercises")

def get_lat_long(municipio, estado):
    location = geolocator.geocode(f"{municipio}, {estado}, Brasil")
    if location:
        return location.latitude, location.longitude
    return None, None

latitudes = []
longitudes = []

for index, row in df.iterrows():
    time.sleep(1)
    lat, long = get_lat_long(row['municipio'], row['estado'])
    latitudes.append(lat)
    longitudes.append(long)

df_plot['latitude'] = latitudes
df_plot['longitude'] = longitudes


df_plot = df_plot.dropna(subset=['latitude', 'longitude'])

st.title("Distribuição de Casos Acumulados de COVID-19")
st.map(df[['latitude', 'longitude']])
