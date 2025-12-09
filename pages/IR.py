import streamlit as st
tabela_ir={'Cabecalho':['Limite mínimo','Limite máximo','Alíquota','Dedução'],
           'faixa1':[0,2428.80,0,0],
           'faixa2':[2428.81,2826.65,7.5,182.16],
           'faixa3':[2826.66,3751.05,15.00,394.16],
           'faixa4':[3751.06,4664.68,22.5,675.49],
           'faixa5':[4664.68,0.0,27.5,908.73]}
imposto_renda = 0

salario=st.number_input('Insira um Valor de Salário:')
if salario <= tabela_ir['faixa1'][1]:
    imposto_renda = 0
elif salario <= tabela_ir['faixa2'][1]: 
    aliquota = tabela_ir['faixa2'][2]
    parcela_dedutivel = tabela_ir['faixa2'][3]
    imposto_renda = (salario*(aliquota/100))-parcela_dedutivel
elif salario <= tabela_ir['faixa3'][1]:
    aliquota = tabela_ir ['faixa3'][2]
    parcela_dedutivel = tabela_ir['faixa3'][3]
    imposto_renda = (salario*(aliquota/100))-parcela_dedutivel
elif salario <= tabela_ir['faixa4'][1]:
    aliquota = tabela_ir ['faixa4'][2]
    parcela_dedutivel = tabela_ir['faixa4'][3]
    imposto_renda = (salario*(aliquota/100))-parcela_dedutivel
else:
    aliquota = tabela_ir ['faixa5'][2]
    parcela_dedutivel = tabela_ir['faixa5'][3]
    imposto_renda = (salario*(aliquota/100))-parcela_dedutivel
st.text(imposto_renda)
salario_liquido=salario-imposto_renda
st.text(f'Salário Liquido é igual a: R$ {salario_liquido}')