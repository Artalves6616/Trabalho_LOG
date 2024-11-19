import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# Carregar dados do arquivo Excel
caminho = "/Users/arthuralves/Desktop/LOGG_projeto/LOGCP_-_base_tickets_manutencao_historico.xlsx"
df = pd.read_excel(caminho)
print(df)

# Selecionar colunas relevantes
colunas = ["des_assunto", "des_tipo_servico", "des_condominio", "des_status", "dat_criacao", "dat_resolucao", "des_atendimento", "cod_uf", "des_status_etapa"]
df = df[colunas]


# Filtrar por status não deletado
df = df[df["des_status"] != "deleted"]

# Função para gerar gráficos e estatísticas para a UF selecionada
def gerar_graficos(df, uf):
    # Filtrar dados para a UF selecionada e converter as datas corretamente
    df_uf = df[(df["cod_uf"] == uf) & (~df["dat_resolucao"].isnull())]
    df_uf["dat_criacao"] = pd.to_datetime(df_uf["dat_criacao"], errors="coerce")
    df_uf["dat_resolucao"] = pd.to_datetime(df_uf["dat_resolucao"], errors="coerce")

    # Remover linhas com datas inválidas (NaT)
    df_uf = df_uf.dropna(subset=["dat_criacao", "dat_resolucao"])

    # Calcular o tempo de resolução em segundos e converter para horas
    tempo_resolucao = (df_uf["dat_resolucao"] - df_uf["dat_criacao"]).dt.total_seconds() / 3600
    media = tempo_resolucao.mean()
    desvio = tempo_resolucao.std()
    cv = desvio / media

    # Exibir os resultados
    st.write(f"*{uf} - Média de tempo de resolução (horas):* {media:.2f}")
    st.write(f"*{uf} - Desvio padrão de tempo de resolução (horas):* {desvio:.2f}")
    st.write(f"*{uf} - Coeficiente de variação:* {cv:.2f}")

    # Gerando o histograma do tempo de resolução
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(tempo_resolucao, kde=True, bins=30, color='blue', ax=ax)
    ax.set_title(f'Distribuição do Tempo de Resolução dos Chamados ({uf})')
    ax.set_xlabel('Tempo de Resolução (Horas)')
    ax.set_ylabel('Frequência')
    ax.grid(True)
    st.pyplot(fig)

    # Gerando o boxplot do tempo de resolução
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x=tempo_resolucao, color='lightblue', ax=ax)
    ax.set_title(f'Boxplot do Tempo de Resolução dos Chamados ({uf})')
    ax.set_xlabel('Tempo de Resolução (Horas)')
    ax.grid(True)
    st.pyplot(fig)

# Opções de seleção de UF
ufs_disponiveis = df["cod_uf"].dropna().unique()
uf_selecionada = st.selectbox("Selecione o Estado (UF):", ufs_disponiveis)

# Gerar gráficos para a UF selecionada
if uf_selecionada:
    gerar_graficos(df, uf_selecionada)

# Gráfico de barras com tempo médio de resolução por UF
st.write("## Tempo Médio de Resolução por UF")
df["dat_criacao"] = pd.to_datetime(df["dat_criacao"], errors="coerce")
df["dat_resolucao"] = pd.to_datetime(df["dat_resolucao"], errors="coerce")
df = df.dropna(subset=["dat_criacao", "dat_resolucao"])

# Calcula o tempo de resolução em horas e agrupa por UF
df["tempo_resolucao_horas"] = (df["dat_resolucao"] - df["dat_criacao"]).dt.total_seconds() / 3600
tempo_medio_por_uf = df.groupby("cod_uf")["tempo_resolucao_horas"].mean()

# Gerar gráfico de barras
fig, ax = plt.subplots(figsize=(12, 6))
tempo_medio_por_uf.plot(kind='bar', color='skyblue', ax=ax)
ax.set_title("Tempo Médio de Resolução por UF")
ax.set_xlabel("UF")
ax.set_ylabel("Tempo Médio de Resolução (Horas)")
ax.grid(axis='y')
st.pyplot(fig)

# Exibir contagem dos serviços mais frequentes (des_assunto)
st.write("## Tipos de Serviços Realizados Mais Frequentes")

# Calcular os 10 tipos de serviço mais realizados
top_n = 10  # Define o número de serviços mais frequentes para exibir
servicos_mais_frequentes = df["des_assunto"].value_counts().nlargest(top_n)

# Gerar gráfico de barras para os serviços mais frequentes
fig, ax = plt.subplots(figsize=(12, 6))
servicos_mais_frequentes.plot(kind='bar', color='lightcoral', ax=ax)
ax.set_title("Top 10 Tipos de Serviços Realizados")
ax.set_xlabel("Tipo de Serviço")
ax.set_ylabel("Quantidade")
ax.grid(axis='y')
st.pyplot(fig)


