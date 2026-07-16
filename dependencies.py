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
        LEFT JOIN
            bethadba.efclientes c
        ON
            s.codi_emp = c.codi_emp 
        AND
            s.codi_cli = c.codi_cli
        WHERE 
            s.codi_emp = ? AND s.ddoc_sai >= ? AND s.ddoc_sai <= ?
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
def get_impostos (empresa,data_inicial,data_final):
    conn=conecta_banco()
    cursor=conn.cursor()
    query="""
        SELECT
        e.CODI_EMP, e.CODI_IMP, e.NOME_IMP, s.sdev_sim, s.data_sim, s.scre_sim
        FROM
        bethadba.EFIMPOSTO e 
        LEFT JOIN bethadba.efsdoimp s
        ON e.CODI_EMP = s.codi_emp AND e.CODI_IMP = s.codi_imp 
        WHERE e.CODI_EMP = ? AND (s.sdev_sim >0 OR s.scre_sim >0) AND s.data_sim >= ? AND s.data_sim <= ?
        """
    cursor.execute(query,(empresa,data_inicial,data_final))
    impostos=cursor.fetchall()
    conn.close()
    return impostos
    
def get_empresas (codigo):
    conn=conecta_banco()
    cursor=conn.cursor()
    query="""
        SELECT
        NOME
        FROM bethadba.PRVCLIENTES
        WHERE CODIGO = ? 
        """
    cursor.execute(query,(codigo))
    empresa=cursor.fetchall()
    conn.close()
    return empresa

def get_cadastro (codigo):
    conn=conecta_banco()
    cursor=conn.cursor()
    query="""
        SELECT
        cgce_emp, cida_emp, ende_emp, ramo_emp, fone_emp, email_emp
        FROM 
        bethadba.geempre
        WHERE codi_emp = ?
        """
    cursor.execute(query,(codigo))
    empresa=cursor.fetchall()
    conn.close()
    return empresa