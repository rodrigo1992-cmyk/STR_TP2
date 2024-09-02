import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

#Agrupando o dataset para que eu tenha apenas um registro por semana no Brasil
regiao = 'Brasil'
df_plot = pd.read_csv('dados/covid.csv')
df_plot = df_plot[df_plot['regiao'] == regiao]
df_plot = df_plot[['semanaAno', 'obitosAcumulado']].groupby(['semanaAno']).max().reset_index()
df_plot.sort_values('semanaAno')


st.write('### O abaixo gráfico apresenta o número de óbitos total no Brasil, desde o início da pandemia, separados por semana epidemiológica')

#Plotando o gráfico
plt.figure(figsize=(12, 4))
plt.title(f'Óbitos de Covid-19 no Brasil por Semana Epidemológica  [Visão Acumulada]')
sns.lineplot(x = df_plot['semanaAno'], y = df_plot['obitosAcumulado'])
plt.ylabel('Óbitos')
plt.xlabel('Semana Epidemológica')

#Ajustando os rótulos do eixo X para que não fiquem um por cima do outro
x_ticks = plt.gca().get_xticks()
x_labels = df_plot['semanaAno'].unique()
plt.xticks(x_ticks[::4], x_labels[::4], rotation=90, size=6)
st.pyplot(plt)
