import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def carrega_dados(caminho):
    dados = pd.read_csv(caminho)
    return dados


def grafico_comparativo(dados_2019, dados_2020, causa, estado='BRASIL'):
    
    # Condicional para estado ou geral
    if estado == 'BRASIL':
        # preparação dos dados consolidado
        total_2019 = dados_2019.groupby('tipo_doenca').sum()
        total_2020 = dados_2020.groupby('tipo_doenca').sum()
        
        lista = [int(total_2019.loc[causa]), int(total_2020.loc[causa])]
        dados = pd.DataFrame({'Ano' : [2019, 2020], 'Total' : lista})
    else:
        # preparação dos dados com escolha de estado
        total_2019 = dados_2019.groupby(['uf', 'tipo_doenca']).sum()
        total_2020 = dados_2020.groupby(['uf', 'tipo_doenca']).sum()
        
        lista = [int(total_2019.loc[estado, causa]), int(total_2020.loc[estado, causa])]
        dados = pd.DataFrame({'Ano' : [2019, 2020], 'Total' : lista})

    # formação do gráfico
    fig, ax = plt.subplots()

    ax = sns.barplot(x='Ano', y='Total', data=dados)
    ax.set_title(f'Óbitos por {causa} - {estado}')
   
    return fig


def main():
    obitos_2019 = carrega_dados('dados/obitos-2019.csv')
    obitos_2020 = carrega_dados('dados/obitos-2020.csv')

    tipo_doenca = obitos_2020.tipo_doenca.unique()
    uf = np.append('BRASIL', obitos_2020.uf.unique())
    
    st.title('Análise dos óbitos 2019-2020')
    st.markdown('Este trabalho analisa os dados dos óbitos de **2019** e **2020**')

    opcao_doenca = st.sidebar.selectbox('Selecione a doença respiratória', tipo_doenca)
    opcao_estado = st.sidebar.selectbox('Selecione o estado', uf)

    figura = grafico_comparativo(obitos_2019, obitos_2020, opcao_doenca, opcao_estado)

    st.pyplot(figura)
    

if __name__ == '__main__':
    main()


