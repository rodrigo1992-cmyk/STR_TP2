
import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt

df = pd.read_csv(r'/workspaces/STR_TP2/Dados/HIST_PAINEL_COVIDBR_2024_Parte2_24ago2024.csv', delimiter=';', encoding='UTF-8')
df['data'] = pd.to_datetime(df['data'])
df['mes'] = df['data'].dt.to_period('M').astype(str)
df_plot = df.groupby('mes')['casosNovos'].sum().reset_index()

st.write('### Casos Novos de COVID-19 no RJ por Mês')
st.write('Selecionado o estado do RJ por ser o meu local de residência')

plt.figure(figsize=(6, 4))
sns.barplot(x = df_plot['mes'], y = df_plot['casosNovos'])
plt.xticks(rotation=45)
st.pyplot(plt)
