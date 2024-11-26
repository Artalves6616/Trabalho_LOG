import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Título da aplicação
st.title("Análise de Dados Financeiros - LOGG3")

# Carregar os dados diretamente do arquivo
file_path = "financeiro_LOGG3.csv"  # Insira o nome do arquivo corretamente se estiver na mesma pasta
finance_data = pd.read_csv(file_path)

# Exibir os primeiros dados da planilha
st.write("Visualizando os primeiros dados da planilha:")
st.dataframe(finance_data.head())

# Ordenar o período e verificar colunas numéricas
finance_data['periodo'] = pd.Categorical(finance_data['periodo'], ordered=True)
finance_data.sort_values('periodo', inplace=True)
numeric_columns = finance_data.select_dtypes(include=['float64', 'int64']).columns

# Selecionar a coluna para análise
selected_columns = st.multiselect("Selecione as colunas para visualização:", numeric_columns)

# Plotar gráficos
if selected_columns:
    for column in selected_columns:
        fig, ax = plt.subplots()
        ax.plot(finance_data['periodo'], finance_data[column], marker='o', label=column)
        ax.set_title(f"Evolução de {column}")
        ax.set_xlabel("Período")
        ax.set_ylabel(column)
        ax.legend()
        plt.xticks(rotation=45)
        st.pyplot(fig)
    
    # Calcular variação percentual e exibir gráfico
    if st.checkbox("Mostrar variação percentual"):
        for column in selected_columns:
            finance_data[f'{column}_var'] = finance_data[column].pct_change() * 100
            fig, ax = plt.subplots()
            ax.bar(finance_data['periodo'], finance_data[f'{column}_var'], color='skyblue')
            ax.set_title(f"Variação Percentual de {column}")
            ax.set_xlabel("Período")
            ax.set_ylabel(f"Variação (%)")
            plt.xticks(rotation=45)
            st.pyplot(fig)

