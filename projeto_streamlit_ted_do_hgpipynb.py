# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import io

# URL do CSV no GitHub (RAW)
CSV_URL = "https://github.com/held95/ted_hgp_neuro/raw/refs/heads/main/HOSP%20NCR%20-%2016-06-25%20a%2015-07-25.csv"

# Função para carregar dados com codificação apropriada
@st.cache_data
def carregar_dados():
    return pd.read_csv(CSV_URL, encoding='latin1')  # ← CORRIGIDO AQUI

# Título
st.title("🧠 Editor de Dados - HOSP NCR")

# Carregar dados
df = carregar_dados()

# Editor interativo
st.subheader("📝 Visualizar e Editar Dados")
edit_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")

# Mostrar os dados editados
st.subheader("📊 Dados Atualizados")
st.dataframe(edit_df, use_container_width=True)

# Botão para baixar CSV atualizado
csv = edit_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Baixar CSV Atualizado",
    data=csv,
    file_name="dados_editados.csv",
    mime="text/csv"
)
