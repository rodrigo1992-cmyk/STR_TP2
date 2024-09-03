
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import seaborn as sns
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pydeck as pdk
import math



#--------------------------EXERCICIO 1--------------------------------
st.write('# 1.Importância da Visualização de Dados')
st.write('*Explique a importância da visualização de dados no contexto de uma pandemia como a COVID-19. Como essas visualizações podem ajudar gestores de saúde pública e a população em geral a tomar decisões informadas?*')
st.write('''A quantidade de aplicações para a visualização de dados no contexto de uma pandemia é vasta. No entanto, podemos destacar algumas abordagens importantes:
- Mapear a evolução da doença, permitindo a observação de acentuações nas curvas de contágio e óbito.
- Comparar o padrão de evolução da doença em diferentes localidades, facilitando a análise de tendências regionais.
- Acompanhar a como diferentes contextos socioeconômicos afetam no padrão de contágio e de óbitos.
- Utilizar dados georreferenciados para criar mapas de calor, permitindo visualizar aglutinações por proximidade e identificar áreas críticas.
''')



#--------------------------EXERCICIO 2--------------------------------

#Agrupando o dataset para que eu tenha apenas um registro por semana e estado
uf = 'RJ'
df = pd.read_csv('dados/covid.csv')
df_plot = df[(df['estado'] == uf)  & df['municipio'].isnull()]
df_plot = df_plot[['semanaAno', 'casosNovos']].groupby(['semanaAno']).sum().reset_index()
df_plot = df_plot.sort_values('semanaAno')

st.write('# 2.Gráfico de Barras com Streamlit')
st.write('*Usando os dados de casos novos de COVID-19 por semana epidemiológica de notificação, crie um gráfico de barras em Streamlit que mostre a evolução semanal dos casos em um determinado estado. Indique o estado escolhido e explique sua escolha.*')
st.write('### Selecionado o estado do RJ por ser o meu estado de residência.')

#Plotando o gráfico
plt.figure(figsize=(12, 4))
plt.title(f'Novos casos de Covid-19 por semana no {uf} [Visão Incremental]')
plt.bar(df_plot['semanaAno'], df_plot['casosNovos'])
plt.ylabel('Casos Novos')
plt.xlabel('Semana Epidemológica')

#Ajustando os rótulos do eixo X para que não fiquem um por cima do outro
x_ticks = plt.gca().get_xticks()
x_labels = df_plot['semanaAno'].unique()
plt.xticks(x_ticks[::4], x_labels[::4], rotation=90, size=6)
st.pyplot(plt)



#--------------------------EXERCICIO 3--------------------------------

#Agrupando o dataset para que eu tenha apenas um registro por semana no Brasil
regiao = 'Brasil'
df_plot = df[df['regiao'] == regiao]
df_plot = df_plot[['semanaAno', 'obitosAcumulado']].groupby(['semanaAno']).max().reset_index()
df_plot = df_plot.sort_values('semanaAno')

st.write('# 3.Gráfico de linha com Streamlit')
st.write('*Crie um gráfico de linha utilizando Streamlit para representar o número de óbitos acumulados por COVID-19 ao longo das semanas epidemiológicas de notificação para todo o Brasil. Explique como a curva de óbitos acumulados pode ser interpretada.*')
st.write('### O gráfico abaixo apresenta o número de óbitos total no Brasil desde o início da pandemia, separados por semana epidemiológica')

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



#--------------------------EXERCICIO 4--------------------------------
ufs = ['MG','RJ','ES']
df_plot = df[(df['estado'].isin(ufs)) & df['municipio'].isnull()]
df_plot = df_plot[['estado', 'mes', 'casosAcumulado']].groupby(['estado', 'mes']).max().reset_index()
df_plot= df_plot.sort_values('mes')

st.write('# 4.Gráfico de Área com Streamlit')
st.write('*Utilizando os dados de casos acumulados por COVID-19, crie um gráfico de área em Streamlit para comparar a evolução dos casos em três estados diferentes. Explique as diferenças observadas entre os estados escolhidos.*')
st.write('### Comparativo entre RJ, ES e MG')
st.write('Se observa uma curva de contágio semelhante entre os estados da região sudeste, apesar de MG apresentar uma aceleração maior no primeiro semestre de 2020. Também é possível observar um pico em janeiro de 2022, após festas de final de ano, e a entrada em um platô a partir de janeiro de 2023.')

#Plotando o gráfico
plt.figure(figsize=(12, 4))
plt.title('Evolução dos casos de COVID-19 na região sudeste (Exceto SP)')
for estado in ufs:
    df_uf = df_plot[df_plot['estado'] == estado]
    plt.fill_between(df_uf['mes'].astype(str), df_uf['casosAcumulado'], label=estado, alpha=0.8)

plt.xticks(rotation=90)
plt.legend(title='Estado')
plt.tight_layout()
st.pyplot(plt)



#--------------------------EXERCICIO 5--------------------------------

df_plot = pd.read_csv('Dados\df_rj_lat_long.csv')
df_plot = df_plot[df_plot['municipio'].notnull()]
df_plot = df_plot.dropna(subset=['latitude', 'longitude'])

#Reduzi o tamanho dos pontos para que não fiquem muito grandes
df_plot['size'] = (df_plot['casosAcumulado'] /  max(df_plot['casosAcumulado'])) * 10000

st.write('# 5.Mapa com Streamlit')
st.write('*Crie um mapa interativo utilizando a função st.map do Streamlit que mostre a distribuição dos casos acumulados de COVID-19 por município em um estado específico. Explique como esse tipo de visualização pode ajudar na análise geográfica da pandemia.*')
st.write("Plotar dados georeferenciados pode auxiliar a observar aglutinações por proximidade.")
st.write("#### Total de Casos de COVID-19")
st.map(df_plot, latitude = 'latitude', longitude = 'longitude', size = 'size')



#--------------------------EXERCICIO 6--------------------------------

#Total de cada estado
df_plot = df[(df['municipio'].isnull()) & (df['estado'].notnull())]

#Selecionando a semana mais recente
semana = max(df_plot['semanaAno'])
df_plot = df_plot[df_plot['semanaAno'] == semana]

#Somar os casos da semana mais recente
df_plot = df_plot[['estado', 'semanaAno','casosNovos','obitosNovos']].groupby(['estado', 'semanaAno']).sum().reset_index()
df_plot = df_plot.sort_values('casosNovos', ascending=False)

st.write('# 6.Visualização com Matplotlib')
st.write('*Utilize a biblioteca Matplotlib para criar um gráfico de barras que mostre a comparação entre os casos novos e os óbitos novos de COVID-19 por estado na semana epidemiológica mais recente disponível. Explique o que os dados sugerem sobre a relação entre casos e óbitos.*')
st.write('Apesar de SP possuir o maior número de casos e de óbitos, não observei uma relação proporcional para os demais estados. Também é possível que os obitos observados sejam referentes aos casos de semanas anteriores.')

#Plotando o gráfico
plt.figure(figsize=(12, 4))
plt.title(f'Comparação de casos e óbitos por estado na semana epidemológica de {semana}')

# Posicionando as barras
x = range(len(df_plot['estado']))
largura = 0.35
barra_casos = plt.bar(x, df_plot['casosNovos'], width=largura, label='Casos Novos', color='blue')
barra_obitos = plt.bar([i + largura for i in x], df_plot['obitosNovos'], width=largura, label='Óbitos Novos', color='red')

# Adicionando rótulos de dados
for barra in barra_casos:
    altura = barra.get_height()
    plt.text(
        x = barra.get_x() + barra.get_width()/2, 
        y = altura, 
        s = altura,
        fontsize=7,
        ha='center', va='bottom'
        )

for barra in barra_obitos:
    altura = barra.get_height()
    plt.text(
        x = barra.get_x() + barra.get_width()/2, 
        y = altura, 
        s = altura,
        fontsize=7,
        ha='center', va='bottom'
        )

# Ajustando os rótulos do eixo X
plt.xticks([i + largura / 2 for i in x], df_plot['estado'], rotation=45)

st.pyplot(plt)



#--------------------------EXERCICIO 7--------------------------------

#Filtrando apenas as regiões desejadas
df_plot = df[df['regiao'].isin(['Norte','Nordeste','Sudeste'])]
#Deixando apenas o total de cada estado
df_plot = df_plot[df_plot['municipio'].isnull()]
#Retirei os valores negativos pois se tratam de correções sobre o calculo acumulado, não existindo notificação negativa.
df_plot = df_plot[df_plot['casosNovos'] >= 0]

#Agregando por região
df_plot = df_plot[['regiao', 'semanaAno','casosNovos']].groupby(['regiao', 'semanaAno']).sum().reset_index()

st.write('# 7.Boxplot com Seaborn')
st.write('*Usando a biblioteca Seaborn, crie um boxplot que compare a distribuição dos casos novos de COVID-19 por semana epidemiológica entre três regiões do Brasil (Norte, Nordeste, Sudeste). Explique as principais diferenças observadas.*')
st.write('Se observa um grande contraste entre o número de casos reportados semanalmente na região Sudeste e as demais regiões. A diferença é tão expressiva que a mediana da região sudeste quase alcança o terceiro quartil do Nordeste e o limite superior da região Norte. Entretanto, esse plot não é adequado para comparar o nível epidêmico em cada região, pois a população das 3 regiões é bem distinta (Sudeste ~84Mi, Nordeste ~54Mi, Norte ~17Mi). Para uma comparação mais adequada deveria ser calculada a proporção de casos em relação à população total de habitantes de cada região, por exemplo, o número de casos a cada mil habitantes.')

#criando um boxplot com seaborn
plt.figure(figsize=(12, 4))
plt.title(f'Distribuição de casos novos por semana epidemiológica nas regiões Norte, Nordeste e Sudeste')
sns.boxplot(data=df_plot, x='casosNovos', y='regiao')
st.pyplot(plt)



#--------------------------EXERCICIO 8--------------------------------

#Agrupando o dataset para que eu tenha apenas um registro por semana e estado
df_plot = df[(df['regiao'] == 'Sudeste') & (df['municipio'].isnull())]
df_plot = df_plot[['estado','semanaAno', 'casosNovos']].groupby(['estado','semanaAno']).sum().reset_index()
df_plot = df_plot.sort_values('semanaAno')

st.write('# 8.Gráfico de Área com Altair')
st.write('*Crie um gráfico de área em Altair para mostrar a evolução dos casos novos de COVID-19 por semana epidemiológica de notificação em uma determinada região do Brasil. Explique a escolha da região e as tendências observadas nos dados.*')
st.write('### Seguindo o padrão dos exercícios anteriores, selecionei o Sudeste por ser a região onde resido')
st.write('Se observa que São Paulo, em parte pelo tamanho de sua população, se manteve com número de contágio semanal bem superior às demais UFs desde o começo da pandemia, inclusive, tendo uma aceleração de contágio mais agravada do que as outras UFs entre o início da pandemia e a semana 33 de 2020. O mesmo comportamento pode ser observado novamente entre a semana 1 (pós festas) e a semana 24 de 2021. Apesar disso, se manteve controlada nas semanas 3 a 6 de 2022, enquanto RJ e MG apresentaram o maior pico histórico, com mais de 160mil novos casos, superando até mesmo a máxima histórica de 120mil casos em SP. Após este pico, todos os UFs entraram em declínio do número de casos, e apesar da diferença populacional, todas se mantiveram em um patamar similar, demonstrando um melhor controle da pandemia no estado de SP em relação às demais UFs.')

#Plotando o gráfico de área com altair
grafico = (
    alt.Chart(df_plot).mark_area().encode(
        x=alt.X('semanaAno:N', 
                axis=alt.Axis(labelOverlap='greedy') #Ajustei para que os rótulos não se sobreponham
                ),
        y=alt.Y('casosNovos:Q', stack=None),
        color=alt.Color('estado:N', legend=alt.Legend(title='Estado')),
        opacity=alt.value(0.7),
        tooltip=['estado:N', 'semanaAno:O', 'casosNovos:Q']
    ).properties(
        title='Novos casos de Covid-19 por semana na região Sudeste',
        width=1000,
        height=400,
    )
)

st.altair_chart(grafico)


#--------------------------EXERCICIO 9--------------------------------

df_plot = df[(df['estado'] == 'RJ') & (df['municipio'].isnull())]

#Tratei os valores negativos pois se tratam de correções sobre o calculo acumulado, não existindo notificação negativa.
df_plot['casosNovos'] = np.where(df_plot['casosNovos'] < 0, 0, df_plot['casosNovos'])
df_plot['data'] = pd.to_datetime(df_plot['data'])
df_plot['trimestre'] = df_plot['data'].dt.to_period('Q').astype(str)

st.write('# 9.Heatmap com Altair')
st.write('*Desenvolva um heatmap em Altair que mostre a correlação entre casos novos, óbitos novos e leitos hospitalares ocupados (caso os dados estejam disponíveis) em um determinado estado. Explique as possíveis correlações observadas.*')
st.write('A base de leitos hospitalares não estava disponível no DataSus, portanto prossegui com uma correlação entre casos e óbitos por mês. Em 2021 é possível observar um agravamento do número de óbitos de acordo com a número de novos casos, situação que já não ocorre mais a partir de janeiro de 2022, momento em que a grande massa da população do Rio de Janeiro já havia recebido a primeira dose de vacina.')

grafico = (
    alt.Chart(df_plot).mark_rect().encode(
        x=alt.X('trimestre:N', sort='ascending'),
        y=alt.Y('casosNovos:O', sort='descending').bin(maxbins=100),
        color='obitosNovos:Q'
    ).properties(
        title='Correlação entre casos e óbitos por quarter no RJ',
        width=600,
        height=400,
    )
)
st.altair_chart(grafico)



#--------------------------EXERCICIO 10--------------------------------


df_plot = df[df['regiao'] != 'Brasil']
df_plot = df_plot[df_plot['municipio'].isnull()]

#Pegando a última data
df_plot = df_plot[df_plot['data'] == max(df_plot['data'])]
df_plot = df_plot[['regiao', 'casosAcumulado']].groupby('regiao').sum().reset_index()

#Criando os rótulos com abreviação da região e percentual
df_plot['perc'] = df_plot['casosAcumulado'] / sum(df_plot['casosAcumulado'])
df_plot['perc'] = (df_plot['perc']*100).round().astype(int).astype(str) + '%'
df_plot['round'] = round(df_plot['casosAcumulado'] / 1000000, 2)

cmap = {
    'Norte': 'N',
    'Nordeste': 'NE',
    'Centro-Oeste': 'CO',
    'Sudeste': 'SE',
    'Sul': 'S'
}

df_plot['regiao'] = df_plot['regiao'].replace(cmap)
df_plot['label'] = df_plot['regiao'] + ': ' + df_plot['round'].astype(str) + 'Mi'
df_plot.sort_values('casosAcumulado', ascending=False, inplace=True)

st.write('# 10.Gráfico de Piza com Plotly')
st.write('*Usando Plotly, crie um gráfico de pizza (pie chart) que mostre a distribuição percentual dos casos acumulados de COVID-19 entre as cinco regiões do Brasil. Explique o que os dados revelam sobre a distribuição geográfica dos casos.*')
st.write('Se observa que a região sudeste concentrou 40% de todos os casos de Covid no Brasil, praticamente o dobro da região sul, a segunda colocada. Se compararmos ao número de habitantes de cada região, o número de casos no Sul é equivalente a 27% de sua população (~30Mi hab.), enquanto no Sudeste é equivalente a 17% (~85Mi hab.) e no Nordeste 14% (55Mi hab.).')


# Criando o gráfico de pizza
fig = px.pie(
    df_plot,
    values='casosAcumulado',
    names='regiao',
    title='Total de casos por região',
    labels={'casosAcumulado': 'Total de Casos', 'regiao': 'Região'},
    hole=False,
    color_discrete_sequence = ['#FF5733', '#33FF57', '#3357FF', '#F1C40F', '#8E44AD'] 
)

fig.update_traces(textinfo='label+percent', textfont_size=10)

st.plotly_chart(fig)


#--------------------------EXERCICIO 11--------------------------------

#Total de cada estado
df_plot = df[(df['municipio'].isnull()) & (df['regiao'].isin(['Sul','Sudeste']))]

#Agrupando e tratando valores negativos
df_plot = df_plot[['regiao', 'semanaAno','casosNovos','obitosNovos']].groupby(['regiao', 'semanaAno']).sum().reset_index()
df_plot['casosNovos'] = np.where(df_plot['casosNovos'] < 0, 0, df_plot['casosNovos'])
df_plot['obitosNovos'] = np.where(df_plot['obitosNovos'] < 0, 0, df_plot['obitosNovos'])
df_plot = df_plot.sort_values('semanaAno', ascending=True)

df_se = df_plot[df_plot['regiao'] == 'Sudeste']
df_su = df_plot[df_plot['regiao'] == 'Sul']

st.write('# 11.Subplots com Plotly')
st.write('*Crie subplots em Plotly que mostrem, lado a lado, gráficos de barras comparando os casos novos e os óbitos novos de COVID-19 por semana epidemiológica em duas diferentes regiões do Brasil. Explique as diferenças observadas entre as regiões.*')
st.write('Em números absolutos de novos casos se observam curvas semelhantes para as regiões sul e sudeste. Para óbitos se observa um patamar elevado para o Sudeste no início da pandemia, que se mantém durante todo o primeiro semestre de 2021, representando aproximadamente o dobro de óbitos por semana em relação à região sul, o mesmo volta a ocorrer no primeiro semestre de 2022. Também se observa que ambas as regiões apresentam os mesmos períodos de picos, com picos de contaminação em outubro 2021 e abril 2022, sendo seguidos por picos de óbitos nos meses seguintes, em dezembro 2021 e julho 2022.')

#Plotando gráfico com Altair
fig = make_subplots(rows=1, cols=2)

#-----------Gráfico 1---------------
#Sudeste
fig.add_trace(
    go.Bar(name='Sudeste', x=df_se["semanaAno"], y=df_se["casosNovos"], yaxis='y', offsetgroup=1),
    row=1, col=1
)
#Sul
fig.add_trace(
    go.Bar(name='Sul', x=df_su["semanaAno"], y=df_su["casosNovos"], yaxis='y', offsetgroup=2),
    row=1, col=1
)

#-----------Gráfico 2---------------
#Sudeste
fig.add_trace(
    go.Bar(name='Sudeste', x=df_se["semanaAno"], y=df_se["obitosNovos"], yaxis='y2', offsetgroup=1),
    row=1, col=2
)
#Sul
fig.add_trace(
    go.Bar(name='Sul', x=df_su["semanaAno"], y=df_su["obitosNovos"], yaxis='y2', offsetgroup=2),
    row=1, col=2
)

fig.update_layout(barmode='group',
                  title_text='Comparativo de Covid-19 entre Sul e Sudeste por semana epidemológica',
                  yaxis_title='Casos',
                  yaxis2_title='Óbitos')

st.plotly_chart(fig)


#--------------------------EXERCICIO 12--------------------------------

df_plot = pd.read_csv('Dados\df_sud_lat_long.csv')

st.write('# 12.Mapa Interativo com PyDeck')
st.write('*Utilize PyDeck para criar um mapa interativo que mostre a densidade populacional ajustada para os casos acumulados de COVID-19 por município em uma determinada região do Brasil. Explique como a densidade populacional pode influenciar a disseminação da COVID-19.*')
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
