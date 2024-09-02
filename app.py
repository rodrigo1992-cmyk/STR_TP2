
import plotly.express as px
import pandas as pd
import streamlit as st
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pydeck as pdk
import math

df_plot = pd.read_csv('Dados\df_sud_lat_long.csv')

st.write('# 12.Mapa Interativo com PyDeck')
st.write('Doenças contagiosas tem maior chance de proliferação em locais com maior densidade populacional. Para este mapa foi feito um ajuste da quantidade de casos dividido pela quantidade de habitantes de cada município, de forma ater uma visão clara do impacto proporcional da pandemia em cada localidade.')

# Reduzindo a escala
df_plot["radius"] = df_plot["casos_por_cem_mil"].apply(lambda count: math.sqrt(count))

layer = pdk.Layer(
    "ScatterplotLayer",
    df_plot,
    pickable=True,
    opacity=0.05,
    stroked=False,
    filled=True,
    radius_scale=50,
    radius_min_pixels=1,
    radius_max_pixels=100,
    line_width_min_pixels=1,
    get_position=['longitude', 'latitude'],
    get_radius=["radius"],
    get_fill_color=[237, 28, 36],
    get_line_color=[0, 0, 0]
)

view_state = pdk.ViewState(latitude=-19.637148, longitude=-44.338077, zoom=4.9, bearing=0, pitch=0)

r = pdk.Deck(layers=[layer], initial_view_state=view_state)
r.to_html("scatterplot_layer.html")

st.pydeck_chart(r)
