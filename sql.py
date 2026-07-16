import pyodbc
from pprint import pprint
import streamlit as st
import pandas as pd
from dependencies import *

st.set_page_config(layout='wide',page_icon='icone.ico',page_title="B.I Gcont")
st.logo("horizontal4.png")

cod=st.sidebar.number_input('Insira o código da empresa:',width=300,step=0)
dt_init=st.sidebar.date_input('Insira a data Inicial',format='DD/MM/YYYY',width=300)
dt_end=st.sidebar.date_input('Insira a data final',format='DD/MM/YYYY',width=300)
nome_empresa= get_empresas(cod)
col_titulo,col_autor=st.columns(2)
with col_titulo:
    st.title('B.I Gcont')
with col_autor:
    st.title('Autor: André Griebeler')
try:    
    st.subheader(nome_empresa[0][0])
except:
    st.info("Insira o código da empresa") 
      
cadastro_empresa=get_cadastro(cod)
col_cadastro1,col_cadastro2, col_cadastro3 =st.columns(3)
with col_cadastro1:
    st.write(f'CNPJ: *{cadastro_empresa[0][0]}*')
    st.write(f'Endereço: *{cadastro_empresa[0][2]}*')
with col_cadastro2:
    st.write(f'Telefone: *{cadastro_empresa[0][4]}*')
    st.write(f'e-mail: *{cadastro_empresa[0][5]}*')
with col_cadastro3:
    st.write(f'Ramo: *{cadastro_empresa[0][3]}*')
    
saidas=get_saidas(cod,dt_init, dt_end)
saidas_list = []
for x in saidas:
    saidas_list.append([x[0],x[1],x[2],x[3].strftime("%d/%m/%Y")])
saidas_df=pd.DataFrame(saidas_list,columns=["Documentos","Clientes","Valor","Data"])
entradas=get_entradas(cod,dt_init, dt_end)
entrads_list = []
for x in entradas: 
    entrads_list.append([x[0],x[1],x[2],x[3].strftime("%d/%m/%Y")])
entradas_df=pd.DataFrame(entrads_list,columns=["Documentos","Fornecedores","Valor","Data"])


colun1, colun2=st.columns(2)
with colun1: 
    st.subheader("Relatório das Saídas")
    cliente = st.text_input("Insira o nome do cliente a pesquisar: ",width=350).lower()
    saidas_df_fil = saidas_df[saidas_df["Clientes"].str.lower().str.contains(cliente)]
    soma_saidas = float(saidas_df_fil["Valor"].sum())
    saidas_df_fil["Valor"]=saidas_df_fil["Valor"].apply(formata_valor)
    st.dataframe(saidas_df_fil)

    st.metric('Soma das Saídas',formata_valor(soma_saidas))
with colun2: 
    st.subheader("Relatório das Entradas")
    fornecedores = st.text_input("Insira o nome do fornecedor a pesquisar: ",width=350).lower()
    entradas_df_fil = entradas_df[entradas_df["Fornecedores"].str.lower().str.contains(fornecedores)]
    soma_entradas = float(entradas_df_fil["Valor"].sum())
    entradas_df_fil["Valor"]=entradas_df_fil["Valor"].apply(formata_valor)
    st.dataframe(entradas_df_fil)
    st.metric('Soma das Entradas',formata_valor(soma_entradas))
st.divider() 
st.subheader ('Empregados:')
col_empregados1, col_empregados2 = st.columns(2)
with col_empregados1:
    try:
        empregados= get_empregados(cod)
        empregados_list=[]
        for x in empregados:
            empregados_list.append([x[0],x[1],x[2].strftime("%d/%m/%Y")])
        empregados_df = pd.DataFrame (empregados_list, columns= ['Nome','Salário','Data de Nascimento'])
        empregados_df_bar = empregados_df.copy()
        empregados_df_bar["Salário"] = empregados_df_bar["Salário"].astype(float)
        maior_salario = empregados_df.loc[empregados_df["Salário"].idxmax(),"Nome"]
        st.metric("Maior Salário",maior_salario)
        empregados_df["Salário"]=empregados_df["Salário"].apply(formata_valor)
        st.dataframe(empregados_df)
    except Exception as e:
        st.info(f"Insira o código da empresa")
with col_empregados2:
    st.subheader("Gráfico dos empregados")
    st.bar_chart(empregados_df_bar,x="Nome",y="Salário",color="#Fad32b")
st.divider()    