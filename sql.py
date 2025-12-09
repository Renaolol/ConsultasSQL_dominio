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
def get_empregados (empresa):
    conn=conecta_banco()
    cursor=conn.cursor()
    query="""
        SELECT
        e.nome, e.salario, e.data_nascimento
        FROM
        bethadba.foempregados e
        LEFT JOIN bethadba.forescisoes r
        ON e.codi_emp = r.codi_emp AND e.i_empregados =r.i_empregados 
        WHERE e.codi_emp = ? AND r.demissao IS NULL 
        ORDER BY e.salario DESC
        """
    cursor.execute(query,(empresa))
    empregados=cursor.fetchall()
    conn.close()
    return empregados
#Fim Funções
st.set_page_config(layout='wide',page_icon='icone.ico',page_title="B.I Gcont")
st.logo("horizontal4.png")
st.title('B.I Gcont')
st.subheader('Autor: André Griebeler')
cod=st.sidebar.number_input('Insira o código da empresa:',width=300,step=0)
dt_init=st.sidebar.date_input('Insira a data Inicial',format='DD/MM/YYYY',width=300)
dt_end=st.sidebar.date_input('Insira a data final',format='DD/MM/YYYY',width=300)
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