import os
import re
import json
import hashlib
from datetime import datetime
import shutil

import pdfplumber
import streamlit as st
from supabase import create_client


PASTA_PDFS = os.path.join(
    os.path.expanduser("~"),
    "ECOPARQUE BAIRROS INTEGRADOS LTDA",
    "ECOPARQUE MATRIZ - 10_MEGA",
    "PDF"
)

PASTA_LIDOS = os.path.join(
    os.path.expanduser("~"),
    "ECOPARQUE BAIRROS INTEGRADOS LTDA",
    "ECOPARQUE MATRIZ - 10_MEGA",
    "PDF",
    "lidos"
)

ARQUIVO_HISTORICO = "historico_pedidos.json"

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL,SUPABASE_KEY)

# HISTÓRICO JSON
def carregar_historico():
    if not os.path.exists(ARQUIVO_HISTORICO):
        return {}
    with open(ARQUIVO_HISTORICO,"r",encoding="utf-8") as f:
        return json.load(f)

def salvar_historico(historico):
    with open(ARQUIVO_HISTORICO,"w",encoding="utf-8") as f:
        json.dump(historico,f,indent=4,ensure_ascii=False)

# SHA256
def calcular_sha256(caminho_arquivo):
    sha256 = hashlib.sha256()
    with open(caminho_arquivo, "rb") as f:
        for bloco in iter(lambda: f.read(4096),b""):
            sha256.update(bloco)
    return sha256.hexdigest()

# EXTRAÇÃO PDF
def converter_data(data_str):
    """
    Converte de dd/mm/yyyy para yyyy-mm-dd
    """
    try:
        data_limpa = data_str.strip()
        return datetime.strptime(data_limpa, "%d/%m/%Y").strftime("%Y-%m-%d")
    except:
        return None

def extrair_dados_pdf(caminho_pdf):
    texto = ""
    with pdfplumber.open(caminho_pdf) as pdf:

        for pagina in pdf.pages:
            texto += pagina.extract_text() or ""
            texto += "\n"

    pedido_match = re.search(r"Pedido:\s*(\d+)",texto,re.IGNORECASE)
    
    if not pedido_match:
        print(f"❌ Pedido não encontrado: {caminho_pdf}")
        return None

    pedido = int(
        pedido_match.group(1)
    )

    rms_match = re.search(r"RMs?:\s*([\d,\s]+)",texto,re.IGNORECASE)

    if not rms_match:
        print(f"❌ RM não encontrada: {caminho_pdf}")
        return None

    rms_texto = rms_match.group(1)
    rms = [
        int(rm.strip())
        for rm in re.split(r"[,;]",rms_texto)
        if rm.strip().isdigit()
    ]
    
    entrega = None
    try:
        match_entrega = re.search(
            r"Dt\s*\.*\s*Entrega\s*\.*\s*:\s*(\d{2}/\d{2}/\d{4})",
            texto,
            re.IGNORECASE
        )

        if match_entrega:
            entrega = converter_data(
                match_entrega.group(1)
        )

    except Exception:
        entrega = None

    print("\n========================================")
    print(f"Arquivo : {os.path.basename(caminho_pdf)}")
    print(f"Pedido  : {pedido}")
    print(f"RMs     : {rms}")
    print(f"Entrega : {entrega}")
    print("========================================")
    
    # print(texto) Mostrar tudo que tem no PDF
    
    return pedido, rms, entrega

# SUPABASE
def salvar_supabase(pedido, rms, entrega):

    global total_inseridos
    global total_ignorados

    for rm in rms:
        
        existe = (
            supabase.table("rm_pc")
            .select("id")
            .eq("rm", rm)
            .eq("pc", pedido)
            .limit(1)
            .execute()
        )

        if existe.data:
            print(f"⏭ RM={rm} PC={pedido} já existe")
            total_ignorados += 1
            continue
        (
            supabase.table("rm_pc").insert(
                {
                    "rm": rm,
                    "pc": pedido,
                    "data_entrega": entrega
                }
            ).execute()
        )

        print(f"✅ Inserido RM={rm} PC={pedido} Entrega={entrega}")
        total_inseridos += 1


# PROCESSAMENTO
def processar_pdfs():

    global total_inseridos
    global total_ignorados
    global total_pdfs_ignorados
    global total_erros

    total_inseridos = 0
    total_ignorados = 0
    total_pdfs_ignorados = 0
    total_erros = 0

    historico = carregar_historico()

    for arquivo in os.listdir(PASTA_PDFS):

        if not arquivo.lower().endswith(".pdf"):
            continue

        caminho_pdf = os.path.join(PASTA_PDFS, arquivo)

        try:
            sha = calcular_sha256(caminho_pdf)

            if sha in historico:
                print(f"⏭ PDF ignorado (SHA já processado): {arquivo}")
                total_pdfs_ignorados += 1
                continue

            dados = extrair_dados_pdf(caminho_pdf)

            if not dados:
                continue

            pedido, rms, entrega = dados

            salvar_supabase(pedido, rms, entrega)

            historico[sha] = {
                "pedido": pedido,
                "rms": rms,
                "entrega": entrega,
                "arquivo": arquivo,
                "processado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            salvar_historico(historico)
            
            print(f"💾 Histórico atualizado para {arquivo}")
            mover_para_lidos(caminho_pdf)

        except Exception as erro:

            total_erros += 1

            print(f"❌ Erro em {arquivo}")
            print(erro)

    print()
    print("========================================")
    print("PROCESSAMENTO FINALIZADO")
    print("========================================")
    print(f"✅ Registros inseridos : {total_inseridos}")
    print(f"⏭ Registros ignorados : {total_ignorados}")
    print(f"📄 PDFs ignorados     : {total_pdfs_ignorados}")
    print(f"❌ Erros              : {total_erros}")
    print("========================================")
    

def mover_para_lidos(caminho_pdf):

    os.makedirs(PASTA_LIDOS, exist_ok=True)

    destino = os.path.join(
        PASTA_LIDOS,
        os.path.basename(caminho_pdf)
    )

    shutil.move(caminho_pdf, destino)

    print(
        f"📁 PDF movido para lidos: "
        f"{os.path.basename(caminho_pdf)}"
    )

if __name__ == "__main__":
    processar_pdfs()
    