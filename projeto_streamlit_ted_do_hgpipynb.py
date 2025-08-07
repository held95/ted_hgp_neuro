import streamlit as st
import pandas as pd

# URL do CSV no GitHub (RAW)
CSV_URL = "https://github.com/held95/ted_hgp_neuro/raw/refs/heads/main/HOSP%20NCR%20-%2016-06-25%20a%2015-07-25.csv"

st.title("🧠 Editor de Dados - HOSP NCR")

@st.cache_data
def carregar_dados():
    try:
        # Tenta ler o CSV com on_bad_lines='skip' (ignora linhas com erro)
        df = pd.read_csv(CSV_URL, encoding='latin1', on_bad_lines='skip')  # pandas >= 1.3.0
        return df
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return None

df = carregar_dados()

if df is not None:
    st.subheader("📝 Visualizar e Editar Dados")
    edit_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")

    st.subheader("📊 Dados Atualizados")
    st.dataframe(edit_df, use_container_width=True)

    csv = edit_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar CSV Atualizado",
        data=csv,
        file_name="dados_editados.csv",
        mime="text/csv"
    )
else:
    st.warning("⚠️ Não foi possível carregar o CSV. Verifique se o arquivo está corretamente formatado.")
