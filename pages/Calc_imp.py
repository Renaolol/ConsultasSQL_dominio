import streamlit as st
valor_da_nota = float (st.number_input('Insira o Valor da Nota Fiscal',width=350))
regime=st.radio('Selecione o Regime Tributário',['Simples Nacional','Lucro Real','Lucro Presumido'],horizontal=True)

aliquota=0.00
if regime=='Simples Nacional':
    aliquota_simples=st.number_input('Adicione a Alíquota Simples Nacional')
    aliquota=aliquota_simples
elif regime=='Lucro Real':
    icms=st.number_input('Adicione a Alíquota ICMS')
    aliquota=icms+7.6+1.65
else:
    icms=st.number_input('Adicione a Alíquota ICMS Lucro Presumido')
    aliquota=icms+0.65+3.0

st.metric('Valor dos Impostos',((aliquota/100)*valor_da_nota))