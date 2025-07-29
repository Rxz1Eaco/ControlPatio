import pandas as pd
import streamlit as st
import os

# ========== CONFIGURAÇÃO INICIAL ==========
st.set_page_config(layout='wide')
st.markdown("<h1 style='text-align: center; color: white;'>📊 Gestão de Pátio Interno - São Luís</h1>", unsafe_allow_html=True)

# ========== CAMINHO DO CSV ==========
CAMINHO_CSV = 'registros.csv'

# ========== FUNÇÕES ==========
def salvar_csv():
    st.session_state.registros.to_csv(CAMINHO_CSV, index=False)

def carregar_csv():
    if os.path.exists(CAMINHO_CSV):
        return pd.read_csv(CAMINHO_CSV)
    else:
        return pd.DataFrame(columns=['Dia', 'Mês', 'Quadra', 'Fila', 'Posicao', 'Placa', 'N° Chassi', 'N° Motor', 'Status'])

# ========== CARREGAR DADOS NA SESSION ==========
if 'registros' not in st.session_state:
    st.session_state.registros = carregar_csv()

df = st.session_state.registros


# ========== INSERIR NOVO REGISTRO COM st.form ==========
with st.expander("➕ Inserir Novo Registro"):
    with st.form(key="form_add"):
        col1, col2, col3 = st.columns(3)
        with col1:
            dia = st.text_input("Dia")
            quadra = st.text_input("Quadra")
            placa = st.text_input("Placa")
        with col2:
            mes = st.text_input("Mês")
            fila = st.text_input("Fila")
            chassi = st.text_input("N° Chassi")
        with col3:
            posicao = st.text_input("Posição")
            motor = st.text_input("N° Motor")
            status = st.selectbox("Status", [
                "Pronta para Aluguel",
                "Em Manutenção",
                "Aguardando Pendência",
                "BO Roubo",
                "Em Trânsito",
                "Recebida",
                "Apreendida",
                "Suporte Rua"
            ])
        submit_add = st.form_submit_button("Adicionar")

    if submit_add:
        novo_registro = {
            'Dia': dia,
            'Mês': mes,
            'Quadra': quadra,
            'Fila': fila,
            'Posicao': posicao,
            'Placa': placa,
            'N° Chassi': chassi,
            'N° Motor': motor,
            'Status': status
        }
        st.session_state.registros = pd.concat(
            [st.session_state.registros, pd.DataFrame([novo_registro])],
            ignore_index=True
        )
        salvar_csv()
        st.success("✅ Registro adicionado com sucesso!")

# ========== ALTERAÇÃO DE STATUS ==========
with st.expander("🔄 Alteração Registro"):
    col10, col11, col12 = st.columns(3)
    with col10:
        placa_alterada = st.text_input('Digite a Placa para editar:')
    with col11:
        nova_quadra = st.text_input('Nova Quadra:')
    with col12:
        nova_fila = st.text_input('Nova Fila:')

    col13, col14 = st.columns(2)
    with col13:
        nova_posicao = st.text_input('Nova Posição:')
    with col14:
        novo_status = st.text_input('Novo Status:')

    if st.button('Alterar'):
        df = st.session_state.registros
        index_match = df[df['Placa'] == placa_alterada].index

        if not index_match.empty:
            i = index_match[0]
            if nova_quadra:
                df.at[i, 'Quadra'] = nova_quadra
            if nova_fila:
                df.at[i, 'Fila'] = nova_fila
            if nova_posicao:
                df.at[i, 'Posicao'] = nova_posicao
            if novo_status:
                df.at[i, 'Status'] = novo_status

            st.session_state.registros = df
            salvar_csv()
            st.success('✅ Registro alterado com sucesso!')
        else:
            st.warning('❌ Placa não encontrada.')

# ========== EXCLUIR REGISTRO ==========
with st.expander("🗑️ Excluir Registro"):
    with st.form(key="form_delete"):
        placa_excluir = st.text_input('Digite a Placa para excluir:')
        submit_delete = st.form_submit_button('Excluir')

    if submit_delete:
        df = st.session_state.registros
        index_match = df[df['Placa'] == placa_excluir].index
        if not index_match.empty:
            st.session_state.registros = df.drop(index_match).reset_index(drop=True)
            salvar_csv()
            st.success(f"🗑️ Registro da placa **{placa_excluir}** excluído com sucesso!")
        else:
            st.warning('❌ Placa não encontrada.')



st.markdown("<h1 style='text-align: center; color: white;'>📊 Dashboard Gestão de Pátio Interno - São Luís</h1>", unsafe_allow_html=True)
# ========== FUNÇÃO PARA OS CARDS ==========
def card(titulo, valor, cor_valor, icone="", bg="#1e1e1e"):
    st.markdown(f"""
        <div style="
            background-color: {bg};
            padding: 20px;
            border-radius: 15px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
            text-align: center;
            height: 130px;
            margin-bottom: 10px;
        ">
            <div style="color:white; font-size:16px; margin-bottom:5px;">{icone} {titulo}</div>
            <div style="color:{cor_valor}; font-size:32px; font-weight:bold;">{valor}</div>
        </div>
    """, unsafe_allow_html=True)

# ======= DASHBOARD COM OS CARDS - POSICIONADO ANTES DA TABELA =======
total_motos = len(df)
status_contagem = df['Status'].value_counts().to_dict()

def get_status_count(nome_status):
    return status_contagem.get(nome_status, 0)

col1, col2, col3 = st.columns(3)
with col1:
    card("Total Motos", total_motos, "white", "✅")
with col2:
    card("Prontas para Aluguel", get_status_count("Pronta para Aluguel"), "#00FF7F", "🟢")
with col3:
    card("Em Manutenção", get_status_count("Em Manutenção"), "#FF4500", "🔴")

col4, col5, col6 = st.columns(3)
with col4:
    card("Aguardando Pendências", get_status_count("Aguardando Pendência"), "#32CD32", "⏱️")
with col5:
    card("BO Roubo", get_status_count("BO Roubo"), "#FFA500", "🟠")
with col6:
    card("Em Trânsito", get_status_count("Em Trânsito"), "#00FF7F", "📈")

col7, col8, col9 = st.columns(3)
with col7:
    card("Recebidas", get_status_count("Recebida"), "#1E90FF", "👥")
with col8:
    card("Apreendida", get_status_count("Apreendida"), "#1E90FF", "📂")
with col9:
    card("Moto Suporte de Rua", get_status_count("Suporte Rua"), "#00FF7F", "🧾")

st.markdown("---")  # divisor visual

# ======= EXIBIR TABELA DE REGISTROS ATUAIS (APÓS O DASHBOARD) =======
st.subheader("📋 Registros Atuais")
st.dataframe(st.session_state.registros, use_container_width=True)
