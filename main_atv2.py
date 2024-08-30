
import pandas as pd
import seaborn as sns
import csv
import streamlit as st
import matplotlib.pyplot as plt

df = pd.read_csv(r'/workspaces/STR_TP2/Dados/HIST_PAINEL_COVIDBR_2024_Parte2_24ago2024.csv', delimiter=';', encoding='UTF-8')
df['data'] 
df['data'] = pd.to_datetime(df['data'])
df['mes'] = df['data'].dt.to_period('M')
df_rj = df.groupby('mes')['casosNovos'].sum().reset_index()

plt.figure(figsize=(6, 4))
sns.barplot(x = df_rj['mes'], y = df_rj['casosNovos'])
plt.xticks(rotation=45)
plt.title('Casos Novos de COVID-19 no RJ por Data')
st.pyplot(plt)
