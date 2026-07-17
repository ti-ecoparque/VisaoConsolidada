import streamlit as st

def configurar_layout():
    """Configura o título e a largura total da página."""
    st.set_page_config(page_title="Visão Compras", layout="wide")

def checar_autenticacao():
    """Valida se o usuário está logado. Se não estiver, exibe a tela de login."""
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False

    if not st.session_state.autenticado:
        st.title("🔑 Acesso ao Sistema")
        usuario_correto = st.secrets["credentials"]["username"]
        senha_correta = st.secrets["credentials"]["password"]
        
        with st.form("form_login"):
            usuario_input = st.text_input("Usuário")
            senha_input = st.text_input("Senha", type="password")
            botao_entrar = st.form_submit_button("Entrar")
            if botao_entrar:
                if usuario_input == usuario_correto and senha_input == senha_correta:
                    st.session_state.autenticado = True
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos.")
        st.stop() # Interrompe a execução do restante da página se não logado
