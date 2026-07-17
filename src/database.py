import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def conectar_supabase() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["API_KEY"]
    return create_client(url, key)

def buscar_dados_view(filtros: dict) -> list:
    supabase = conectar_supabase()
    query = supabase.from_("vw_visao_consolidada").select("*")

    # Aplicação de filtros direto na API
    if filtros.get("rm_numero"):
        query = query.eq("rm_numero", filtros["rm_numero"])
    if filtros.get("pc_numero"):
        query = query.eq("pc_numero", filtros["pc_numero"])
    if filtros.get("ped_comprador"):
        query = query.ilike("ped_comprador", f"%{filtros['ped_comprador']}%")
    if filtros.get("rm_usuario_solicitante"):
        query = query.ilike("rm_usuario_solicitante", f"%{filtros['rm_usuario_solicitante']}%")
    if filtros.get("ped_status_descricao") and filtros["ped_status_descricao"] != "Todos":
        query = query.eq("ped_status_descricao", filtros["ped_status_descricao"])
    if filtros.get("app_status_doc") and filtros["app_status_doc"] != "Todos":
        status_map = {"Aprovado": "A", "Reprovado": "R", "Pendente": "P"}
        query = query.eq("app_status_doc", status_map[filtros["app_status_doc"]])
    if filtros.get("data_inicio"):
        query = query.gte("rm_data_emissao", filtros["data_inicio"].isoformat())
    if filtros.get("data_fim"):
        query = query.lte("rm_data_emissao", filtros["data_fim"].isoformat())

    # Paginação em lotes para superar o teto de 1000 registros do PostgREST
    todos_dados = []
    offset = 0
    tamanho_lote = 1000

    while True:
        resposta = query.range(offset, offset + tamanho_lote - 1).execute()
        if not resposta.data:
            break
        todos_dados.extend(resposta.data)
        if len(resposta.data) < tamanho_lote:
            break
        offset += tamanho_lote
    return todos_dados
