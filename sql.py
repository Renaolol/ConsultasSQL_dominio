import pyodbc
from pprint import pprint
import streamlit as st
import pandas as pd
CONEXAO = "DSN=ContabilPBI;UID=PBI;PWD=Pbi"
#Conexão com o banco de dados
def conecta_banco():
    return pyodbc.connect(CONEXAO)

#Funções
def get_saidas(empresa:int, data_inicial, data_final):
    conn=conecta_banco()
    cursor=conn.cursor()
    query="""
        SELECT 
        s.nume_sai, c.nomr_cli, s.vcon_sai, s.ddoc_sai
        FROM
        bethadba.efsaidas s
        LEFT JOIN bethadba.efclientes c
        ON s.codi_emp = c.codi_emp AND
        s.codi_cli = c.codi_cli
        WHERE s.codi_emp = ? AND s.ddoc_sai >= ? AND s.ddoc_sai <= ?
        """
    cursor.execute(query,(empresa,data_inicial,data_final))
    saidas=cursor.fetchall()
    conn.close()
    return saidas
def get_entradas(empresa,data_inicial,data_final):
    conn=conecta_banco()
    cursor=conn.cursor()
    query= """
        SELECT
        e.nume_ent, f.nomr_for, e.vcon_ent, e.ddoc_ent
        FROM 
        bethadba.efentradas e
        LEFT JOIN bethadba.effornece f
        ON e.codi_emp = f.codi_emp AND e.codi_for = f.codi_for
        WHERE e.codi_emp = ? AND e.ddoc_ent >= ? AND e.ddoc_ent <= ? 
        """
    cursor.execute(query,(empresa,data_inicial,data_final))
    entradas=cursor.fetchall()
    conn.close()
    return entradas
def formata_valor(valor):
    return f'R$ {valor:,.2f}'.replace(",","X").replace(".",",").replace("X",".")

#Fim Funções
st.set_page_config(layout='wide')


st.title('B.i gcont')
st.subheader('Autor André Griebeler')
col1,col2,col3=st.columns(3)
with col1:
    cod=st.number_input('Insira o código da empresa:',width=300,step=0)
with col2:   
    dt_init=st.date_input('Insira a data Inicial',format='DD/MM/YYYY',width=300)
with col3:
    dt_end=st.date_input('Insira a data final',format='DD/MM/YYYY',width=300)
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
soma_saidas = float(saidas_df["Valor"].sum())
soma_entradas = float(entradas_df["Valor"].sum())
colun1, colun2=st.columns(2) 
with colun1: 
    cliente = st.text_input("Insira o nome do cliente a pesquisar: ").lower()
    saidas_df_fil = saidas_df[saidas_df["Clientes"].str.lower().str.contains(cliente)]
    st.subheader("Relatório das Saídas")
    st.dataframe(saidas_df_fil)
    st.metric('Soma das Saídas',formata_valor(soma_saidas))
with colun2: 
    st.subheader("Relatório das Entradas")
    st.dataframe(entradas_df)
    st.metric('Soma das Entradas',formata_valor(soma_entradas))