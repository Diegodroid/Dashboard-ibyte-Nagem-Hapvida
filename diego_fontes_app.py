import pandas as pd 
import numpy as np 
import plotly.express as px 
import streamlit as st
import datetime
from st_pages import Page, show_pages, add_page_title

#### CARREGAR O DADO ####
df_hapvida=pd.read_csv('RECLAMEAQUI_HAPVIDA.csv')
df_ibyte=pd.read_csv('RECLAMEAQUI_IBYTE.csv')
df_nagem=pd.read_csv('RECLAMEAQUI_NAGEM.csv')

                     
## DATETIME ####
df_hapvida['TEMPO']=pd.to_datetime(df_hapvida['TEMPO'])
df_ibyte['TEMPO']=pd.to_datetime(df_hapvida['TEMPO'])
df_nagem['TEMPO']=pd.to_datetime(df_hapvida['TEMPO'])

#CONTAGEM DE RECLAMACOES 
casos_hapvida = df_hapvida['ID'].nunique()
casos_ibyte = df_ibyte['ID'].nunique()
casos_nagem = df_nagem['ID'].nunique()

#SEPARANDO POR ESTADO HAPVIDA
estado_lista=[]
for i in range(len(df_hapvida)):
    estado_lista.append(df_hapvida['LOCAL'].iloc[i][-2:])
df_hapvida['ESTADO']=estado_lista

#SEPARANDO POR ESTADO IBYTE
estado_lista=[]
for i in range(len(df_ibyte)):
    estado_lista.append(df_ibyte['LOCAL'].iloc[i][-2:])
df_ibyte['ESTADO']=estado_lista
#SEPARANDO POR ESTADO NAGEM
estado_lista=[]
for i in range(len(df_nagem)):
    estado_lista.append(df_nagem['LOCAL'].iloc[i][-2:])
df_nagem['ESTADO']=estado_lista

#SEPARANDO AS CIDADES HAPVIDA
df_hapvida['CIDADE'] = df_hapvida['LOCAL'].str.extract(r'([^\-]+)')

#SEPARANDO AS CIDADES IBYTE
df_ibyte['CIDADE'] = df_ibyte['LOCAL'].str.extract(r'([^\-]+)')

#SEPARANDO AS CIDADES NAGEM
df_nagem['CIDADE'] = df_nagem['LOCAL'].str.extract(r'([^\-]+)')

#LISTAR AS CIDADES 
lista_de_cidades_hapvida = df_hapvida['CIDADE'].unique()
lista_de_cidades_ibyte = df_ibyte['CIDADE'].unique()
lista_de_cidades_nagem = df_nagem['CIDADE'].unique()

#LISTAR OS ESTADOS 
lista_de_estados_hapvida = df_hapvida['ESTADO'].unique()
lista_de_estados_ibyte = df_ibyte['ESTADO'].unique()
lista_de_estados_nagem = df_nagem['ESTADO'].unique()

# Cidade com a maior ocorrência
ocorrencias_por_cidade_hapvida = df_hapvida['CIDADE'].value_counts()
cidade_maior_ocorrencia_hapvida = ocorrencias_por_cidade_hapvida.idxmax()


ocorrencias_por_cidade_ibyte = df_ibyte['CIDADE'].value_counts()
cidade_maior_ocorrencia_ibyte = ocorrencias_por_cidade_ibyte.idxmax()

ocorrencias_por_cidade_nagem = df_nagem ['CIDADE'].value_counts()
cidade_maior_ocorrencia_nagem = ocorrencias_por_cidade_nagem.idxmax()


# Estado com a maior ocorrência
ocorrencias_por_estado_hapvida = df_hapvida['ESTADO'].value_counts()
estado_maior_ocorrencia_hapvida = ocorrencias_por_estado_hapvida.idxmax()

ocorrencias_por_estado_ibyte = df_ibyte['ESTADO'].value_counts()
estado_maior_ocorrencia_ibyte = ocorrencias_por_estado_ibyte.idxmax()

ocorrencias_por_estado_nagem = df_nagem ['ESTADO'].value_counts()
estado_maior_ocorrencia_nagem = ocorrencias_por_estado_nagem.idxmax()

#STATUS OCORRENCIA 
status_hapvida = df_hapvida.STATUS.value_counts()
status_ibyte = df_ibyte.STATUS.value_counts()
status_nagem = df_nagem.STATUS.value_counts()

# Criando uma tabela com as informações
table_data = {
    'Status': ['Não respondida', 'Respondida', 'Resolvido', 'Em réplica', 'Não resolvido'],
    'Hapvida': [status_hapvida.get(status, 0) for status in ['Não respondida', 'Respondida', 'Resolvido', 'Em réplica', 'Não resolvido']],
    'Ibyte': [status_ibyte.get(status, 0) for status in ['Não respondida', 'Respondida', 'Resolvido', 'Em réplica', 'Não resolvido']],
    'Nagem': [status_nagem.get(status, 0) for status in ['Não respondida', 'Respondida', 'Resolvido', 'Em réplica', 'Não resolvido']]
}

df_table = pd.DataFrame(table_data)


# Optional -- adds the title and icon to the current page
add_page_title("Panorama Geral de Reclamações")
st.write('Quantidade de reclamações por loja')


col1, col2, col3= st.columns(3)
col1.metric(label="Reclamações Hapvida", value=casos_hapvida)
col2.metric(label="Reclamações Ibyte", value=casos_ibyte)
col3.metric(label="Reclamações Nagem", value=casos_nagem)


col1, col2, col3= st.columns(3)
col1.metric(label="Estado com maior Reclamaçao da Hapvida:", value=estado_maior_ocorrencia_hapvida)
col2.metric(label="Estado com maior Reclamaçao da Ibyte", value=estado_maior_ocorrencia_ibyte)
col3.metric(label="Estado com maior Reclamaçao da Nagem", value=estado_maior_ocorrencia_nagem)

col1, col2, col3= st.columns(3)
col1.metric(label="Cidade com maior Reclamaçao da Hapvida:", value=cidade_maior_ocorrencia_hapvida)
col2.metric(label="Cidade com maior Reclamaçao da Ibyte", value=cidade_maior_ocorrencia_ibyte)
col3.metric(label="Cidade com maior Reclamaçao da Nagem", value=cidade_maior_ocorrencia_nagem)


st.write('Status das reclamações por loja')
# Exibindo a tabela
st.table(df_table)


# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page("diego_fontes_app.py", "Panorama Geral"),
        Page("hapvida.py", "Hapvida"),
        Page("ibytepy.py", "Ibyte"),
        Page("nagem.py", "Nagem"),
        #Page("hapvida.py", "Page 2", ":books:"),
    ]
)
