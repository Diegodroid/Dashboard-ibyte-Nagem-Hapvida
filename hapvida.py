import pandas as pd 
import numpy as np 
import plotly.express as px 
import streamlit as st
import datetime
import json
from urllib.request import urlopen
from pathlib import Path
from st_pages import Page, show_pages, add_page_title
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
# Download NLTK stopwords data
import nltk
nltk.download('stopwords')
nltk.download('punkt')

# Load data
df_hapvida = pd.read_csv('RECLAMEAQUI_HAPVIDA.csv')

# Convert 'TEMPO' column to datetime format
df_hapvida['TEMPO'] = pd.to_datetime(df_hapvida['TEMPO'])

# Extract 'ESTADO' and 'CIDADE' from 'LOCAL' column
df_hapvida['ESTADO'] = df_hapvida['LOCAL'].str[-2:]
df_hapvida['CIDADE'] = df_hapvida['LOCAL'].str.extract(r'([^\-]+)')

# Unique values for filters
cidades = ['Todos'] + list(df_hapvida['CIDADE'].unique())
estados = ['Todos'] + list(df_hapvida['ESTADO'].unique())
status_options = ['Todos'] + list(df_hapvida['STATUS'].unique())
categoria_options = ['Todos'] + list(df_hapvida['CATEGORIA'].unique())

# Sidebar filters
st.sidebar.title('Filtros')
cidade_selecionada = st.sidebar.selectbox('Selecione a cidade:', cidades)
estado_selecionado = st.sidebar.selectbox('Selecione o estado:', estados)
status_selecionado = st.sidebar.selectbox('Selecione o status:', status_options)
categoria_selecionada = st.sidebar.selectbox('Selecione a categoria:', categoria_options)

# Adicionar filtro de tamanho para a coluna 'DESCRICAO'
# Calcular o tamanho máximo da coluna 'DESCRICAO'
min_size, max_size_selected = st.sidebar.slider(
    'Selecione a faixa de tamanho da coluna "DESCRICAO":',
    0, int(df_hapvida['DESCRICAO'].str.len().max()), (0, int(df_hapvida['DESCRICAO'].str.len().max()))
)# Filter data based on selected options
df_filtered = df_hapvida.copy()

if cidade_selecionada != 'Todos':
    df_filtered = df_filtered[df_filtered['CIDADE'] == cidade_selecionada]

if estado_selecionado != 'Todos':
    df_filtered = df_filtered[df_filtered['ESTADO'] == estado_selecionado]

if status_selecionado != 'Todos':
    df_filtered = df_filtered[df_filtered['STATUS'] == status_selecionado]

if categoria_selecionada != 'Todos':
    df_filtered = df_filtered[df_filtered['CATEGORIA'] == categoria_selecionada]

# Filtrar por tamanho da coluna 'DESCRICAO'
df_filtered = df_filtered[(df_filtered['DESCRICAO'].str.len() >= min_size) & (df_filtered['DESCRICAO'].str.len() <= max_size_selected)]

# Display filtered data
st.title('Dados Filtrados')
st.write(df_filtered)

# Plot the interactive bar chart for 'STATUS' by city
ocorrencias_por_status_cidade = df_filtered['STATUS'].value_counts().reset_index()
ocorrencias_por_status_cidade.columns = ['Status', 'Quantidade']
fig_status_cidade = px.bar(ocorrencias_por_status_cidade, x='Status', y='Quantidade',
                            title=f'Quantidade de Reclamações por Status em {cidade_selecionada}',
                            labels={'Quantidade': 'Quantidade de Reclamações', 'Status': 'Status'},
                            text='Quantidade')

st.plotly_chart(fig_status_cidade)

# Plot the top 10 cities with the most complaints
ocorrencias_por_cidade = df_filtered['CIDADE'].value_counts().reset_index().head(10)
ocorrencias_por_cidade.columns = ['Cidade', 'Quantidade']
fig_top_cidades = px.bar(ocorrencias_por_cidade, x='Cidade', y='Quantidade',
                         title='Top 10 Cidades com Mais Reclamações',
                         labels={'Quantidade': 'Quantidade de Reclamações', 'Cidade': 'Cidade'},
                         text='Quantidade')

st.plotly_chart(fig_top_cidades)

# Display table for the top 10 cities
st.table(ocorrencias_por_cidade)


# Plot the top 10 states with the most complaints
ocorrencias_por_estado = df_filtered['ESTADO'].value_counts().reset_index().head(10)
ocorrencias_por_estado.columns = ['ESTADO', 'Quantidade']
fig_top_estados = px.bar(ocorrencias_por_estado, x='ESTADO', y='Quantidade',
                          title='Top 10 Estados com Mais Reclamações',
                          labels={'Quantidade': 'Quantidade de Reclamações', 'ESTADO': 'ESTADO'},
                          text='Quantidade')

st.plotly_chart(fig_top_estados)

# Display table for the top 10 states
st.table(ocorrencias_por_estado)

# Time series plot
df_filtered.set_index('TEMPO', inplace=True)
time_series = df_filtered.resample('D').size()
fig_time_series = px.line(time_series, x=time_series.index, y=time_series.values, labels={'y': 'Number of Observations'})
st.title("Número de Observações ao Longo do Tempo")
st.plotly_chart(fig_time_series)

# Plot the interactive bar chart for 'CATEGORIA' by city
ocorrencias_por_categoria_cidade = df_filtered['CATEGORIA'].value_counts().reset_index()
ocorrencias_por_categoria_cidade.columns = ['Categoria', 'Quantidade']
fig_categoria_cidade = px.bar(ocorrencias_por_categoria_cidade, x='Categoria', y='Quantidade',
                               title=f'Quantidade de Reclamações por Categoria em {cidade_selecionada}',
                               labels={'Quantidade': 'Quantidade de Reclamações', 'Categoria': 'Categoria'},
                               text='Quantidade')

st.plotly_chart(fig_categoria_cidade)


# Exibir tabela com as top 10 cidades
st.table(ocorrencias_por_cidade)

# Função para gerar a nuvem de palavras
def generate_wordcloud(tokens):
    wordcloud = WordCloud(width=800, height=400, random_state=21, max_font_size=110, background_color='white')
    wordcloud.generate_from_frequencies(Counter(tokens))
    return wordcloud

# Filtrar as palavras-chave mais comuns
filtered_tokens = [word for word in word_tokenize(df_filtered['DESCRICAO'].str.cat(sep=' ')) if word.lower() not in stopwords.words('portuguese')]

# Exibir a nuvem de palavras no Streamlit
st.title('Nuvem de Palavras Mais Usadas na Descrição')
wordcloud = generate_wordcloud(filtered_tokens)
st.image(wordcloud.to_image(), use_container_width=True)

# Exibir as top 10 palavras em uma tabela
top_10_palavras = Counter(filtered_tokens).most_common(10)
st.title('Top 10 Palavras Mais Usadas na Descrição')
st.write(pd.DataFrame(top_10_palavras, columns=['Palavra', 'Quantidade']))

# Exibir histograma de distribuição do tamanho das palavras
st.title('Distribuição do Tamanho das Palavras na Descrição')
histogram_data = [len(word) for word in filtered_tokens]
fig_histogram = px.histogram(x=histogram_data, nbins=20, labels={'x': 'Tamanho da Palavra', 'y': 'Quantidade'})
st.plotly_chart(fig_histogram)
