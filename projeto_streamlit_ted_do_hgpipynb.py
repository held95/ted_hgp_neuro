import streamlit as st
import pandas as pd
from datetime import time, timedelta
import io

st.set_page_config(page_title="Editor NCR", layout="wide")

st.title("🧠 Editor de Dados - HOSP NCR (CSV do Colab)")

# URL do CSV hospedado no GitHub ou Colab
CSV_URL = "https://github.com/held95/ted_hgp_neuro/raw/refs/heads/main/HOSP%20NCR%20-%2016-06-25%20a%2015-07-25.csv"

# Função para converter diferentes formatos de horas em float
def converter_para_float(valor):
    try:
        if pd.isnull(valor):
            return 0.0
        if isinstance(valor, timedelta):
            return round(valor.total_seconds() / 3600, 2)
        if isinstance(valor, time):
            return round(valor.hour + valor.minute / 60, 2)
        if isinstance(valor, pd.Timestamp):
            return round(valor.hour + valor.minute / 60, 2)
        valor_str = str(valor).strip().lower().replace("h", ":").replace(".", ":")
        partes = valor_str.split(":")
        if len(partes) == 2:
            horas = int(partes[0])
            minutos = int(partes[1])
            return round(horas + minutos / 60, 2)
        elif len(partes) == 1:
            return float(partes[0])
    except:
        return 0.0
    return 0.0

# Função para converter float de horas em formato HH:MM
def float_para_horas(valor_float):
    total_minutos = int(round(valor_float * 60))
    horas = total_minutos // 60
    minutos = total_minutos % 60
    return f"{horas:02d}:{minutos:02d}"

@st.cache_data
def processar_csv():
    try:
        # Lê o CSV (simulando aba 'PLANTÕES' do Excel)
        df = pd.read_csv(CSV_URL, encoding='latin1', on_bad_lines='skip')

        # Seleciona colunas específicas
        df = df[['Unnamed: 3', 'Unnamed: 4', 'Unnamed: 9']].copy()
        df.columns = ['Nome', 'CRM', 'Horas']
        df = df.dropna(subset=['Nome', 'Horas'])

        # Converte a coluna Horas para float
        df['Horas_float'] = df['Horas'].apply(converter_para_float)

        # Agrupa por Nome e CRM
        agrupado = df.groupby(['Nome', 'CRM'], as_index=False)['Horas_float'].sum()

        # Adiciona coluna final formatada
        agrupado['Total de Horas'] = agrupado['Horas_float'].apply(float_para_horas)

        # Retorna apenas as colunas desejadas
        resultado_final = agrupado[['Nome', 'CRM', 'Total de Horas']]
        return resultado_final
    except Exception as e:
        st.error(f"Erro ao processar CSV: {e}")
        return None

# Processar os dados
resultado = processar_csv()

if resultado is not None:
    st.subheader("📊 Resultado Agrupado por Médico")
    edit_df = st.data_editor(resultado, use_container_width=True, num_rows="dynamic")

    # Permitir download do Excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        edit_df.to_excel(writer, index=False, sheet_name='Resumo')

    st.download_button(
        label="📥 Baixar Excel Editado",
        data=output.getvalue(),
        file_name="resumo_plantao_HOSP_NCR_editado.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.warning("Não foi possível gerar o relatório.")
