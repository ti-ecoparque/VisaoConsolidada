import streamlit as st
import datetime
from src.config import configurar_layout, checar_autenticacao
from src.database import buscar_dados_view
from src.processing import processar_dataframe_compras

from src.components.grid import criar_multiindex_compras
from src.components.styles import aplicar_estilo_grid



from src.components.grid import (
    criar_multiindex_compras,
    destacar_rm
)

from src.components.styles import aplicar_estilo_grid



# Inicialização e Proteção de Rota
configurar_layout()
checar_autenticacao()

# Barra lateral de controle
if st.sidebar.button("Sair / Logout"):
    st.session_state.autenticado = False
    st.rerun()

# Cabeçalhos do painel
#st.title("🛒 Painel Visão Compras")
st.subheader("🛒 Filtros de Monitoramento")

# Definição das datas padrão
data_hoje = datetime.date.today()
trinta_dias_atras = data_hoje - datetime.timedelta(days=30)

# Bloco Visual 1: Construção dos Inputs na Interface
c1, c2, c3, c4 = st.columns(4)
filtro_rm = c1.text_input("Número da RM:")
filtro_pc = c2.text_input("Número do Pedido (PC):")
filtro_comprador = c3.text_input("Comprador (Pedido):")
filtro_req = c4.text_input("Requisitante do Material:")

c5, c6, c7, c8 = st.columns(4)
filtro_sit = c5.selectbox("Situação do Pedido:", ["Todos", "Pendente", "Aprovado", "Reprovado"])
filtro_status = c6.selectbox("Status do Documento (App):", ["Todos", "Aprovado", "Reprovado", "Pendente"])
data_ini = c7.date_input("Data Emissão RM (Início):", value=trinta_dias_atras, format="DD/MM/YYYY")
data_fim = c8.date_input("Data Emissão RM (Fim):", value=data_hoje, format="DD/MM/YYYY")

# Validação do filtro numérico do Pedido de Compra
if filtro_pc and not filtro_pc.isdigit():
    st.warning("Por favor, digite apenas números no campo de Pedido (PC).")
    st.stop()

# Junta os valores capturados em um dicionário de filtros estruturado
dicionario_filtros = {
    "rm_numero": filtro_rm,
    "pc_numero": int(filtro_pc) if filtro_pc else None,
    "ped_comprador": filtro_comprador,
    "rm_usuario_solicitante": filtro_req,
    "ped_status_descricao": filtro_sit,
    "app_status_doc": filtro_status,
    "data_inicio": data_ini,
    "data_fim": data_fim
}

# Bloco 2: Execução das Regras e Consulta
with st.spinner("Buscando dados na View consolidada..."):
    try:
        dados_banco = buscar_dados_view(dicionario_filtros)
        df_final = processar_dataframe_compras(dados_banco)
        #st.write(df_final.columns.tolist())

    except Exception as e:
        st.error("Erro no processamento de dados do aplicativo:")
        st.code(str(e))
        st.stop()

# Bloco Visual 3: Renderização da Tabela de Resultados Estilizada
if not df_final.empty:

    st.write(f"**{len(df_final)}** registros encontrados.")

    st.markdown(
        aplicar_estilo_grid(),
        unsafe_allow_html=True
    )

    df_exibicao = criar_multiindex_compras(df_final)

    df_estilizado = (
        df_exibicao.style
        .apply(destacar_rm, axis=None)
    )

    st.dataframe(
        df_estilizado,
        width="stretch",
        hide_index=True
    )

else:
    st.warning(
        "Nenhum dado encontrado para os filtros selecionados."
    )