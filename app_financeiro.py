import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Título do aplicativo
st.title("Análise de Dados Financeiros - LOGG3")

# Upload do arquivo CSV
uploaded_file = st.file_uploader("Faça upload do arquivo financeiro (CSV)", type="csv")

if uploaded_file:
    # Carregar dados
    finance_data = pd.read_csv(uploaded_file)
    
    # Ordenar períodos, se necessário
    finance_data['periodo'] = pd.Categorical(finance_data['periodo'], ordered=True)
    finance_data.sort_values('periodo', inplace=True)

    # Exibir os primeiros dados
    st.write("Primeiros dados da planilha:")
    st.dataframe(finance_data.head())

    # Identificar colunas numéricas
    numeric_columns = finance_data.select_dtypes(include=['float64', 'int64']).columns

    # Selecionar colunas para análise
    selected_columns = st.multiselect("Selecione as colunas para gerar gráficos:", numeric_columns)

    # Gerar gráficos
    if selected_columns:
        st.subheader("Gráficos de Evolução Financeira")
        for column in selected_columns:
            fig, ax = plt.subplots()
            ax.plot(finance_data['periodo'], finance_data[column], marker='o', label=column)
            ax.set_title(f"Evolução de {column}")
            ax.set_xlabel("Período")
            ax.set_ylabel(column)
            ax.legend()
            plt.xticks(rotation=45)
            st.pyplot(fig)
        
        # Mostrar variação percentual
        if st.checkbox("Mostrar variação percentual entre períodos"):
            st.subheader("Gráficos de Variação Percentual")
            for column in selected_columns:
                finance_data[f'{column}_var'] = finance_data[column].pct_change() * 100
                fig, ax = plt.subplots()
                ax.bar(finance_data['periodo'], finance_data[f'{column}_var'], color='skyblue')
                ax.set_title(f"Variação Percentual de {column}")
                ax.set_xlabel("Período")
                ax.set_ylabel("Variação (%)")
                plt.xticks(rotation=45)
                st.pyplot(fig)



