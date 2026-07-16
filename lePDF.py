import os
import re
import json
import hashlib
from datetime import datetime

import pdfplumber
import streamlit as st
from supabase import create_client

# ==================================================
# CONFIGURAÇÕES
# ==================================================

PASTA_PDFS = r"C:\PDFS"

ARQUIVO_HISTORICO = "historico_pedidos.json"

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

total_inseridos = 0
total_ignorados = 0
total_pdfs_ignorados = 0
total_erros = 0


# ==================================================
# HISTÓRICO JSON
# ==================================================

def carregar_historico():

    if not os.path.exists(ARQUIVO_HISTORICO):
        return {}

    with open(
        ARQUIVO_HISTORICO,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def salvar_historico(historico):

    with open(
        ARQUIVO_HISTORICO,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            historico,
            f,
            indent=4,
            ensure_ascii=False
        )


# ==================================================
# SHA256
# ==================================================

def calcular_sha256(caminho_arquivo):

    sha256 = hashlib.sha256()

    with open(caminho_arquivo, "rb") as f:

        for bloco in iter(
            lambda: f.read(4096),
            b""
        ):
            sha256.update(bloco)

    return sha256.hexdigest()


# ==================================================
# EXTRAÇÃO PDF
# ==================================================

def extrair_dados_pdf(caminho_pdf):

    texto = ""

    with pdfplumber.open(caminho_pdf) as pdf:

        for pagina in pdf.pages:

            texto += pagina.extract_text() or ""
            texto += "\n"

    pedido_match = re.search(
        r"Pedido:\s*(\d+)",
        texto,
        re.IGNORECASE
    )

    if not pedido_match:

        print(
            f"❌ Pedido não encontrado: {caminho_pdf}"
        )

        return None

    pedido = int(
        pedido_match.group(1)
    )

    rms_match = re.search(
        r"RMs?:\s*([\d,\s]+)",
        texto,
        re.IGNORECASE
    )

    if not rms_match:

        print(
            f"❌ RM não encontrada: {caminho_pdf}"
        )

        return None

    rms_texto = rms_match.group(1)

    rms = [

        int(rm.strip())

        for rm in re.split(
            r"[,;]",
            rms_texto
        )

        if rm.strip().isdigit()
    ]

    print("\n========================================")
    print(f"Arquivo : {os.path.basename(caminho_pdf)}")
    print(f"Pedido  : {pedido}")
    print(f"RMs     : {rms}")
    print("========================================")

    return pedido, rms


# ==================================================
# SUPABASE
# ==================================================

def salvar_supabase(pedido, rms):

    global total_inseridos
    global total_ignorados

    for rm in rms:

        existe = (
            supabase
            .table("rm_pc")
            .select("id")
            .eq("rm", rm)
            .eq("pc", pedido)
            .execute()
        )

        if existe.data:

            print(
                f"⏭ RM={rm} PC={pedido} já existe"
            )

            total_ignorados += 1

            continue

        (
            supabase
            .table("rm_pc")
            .insert(
                {
                    "rm": rm,
                    "pc": pedido
                }
            )
            .execute()
        )

        print(
            f"✅ Inserido RM={rm} PC={pedido}"
        )

        total_inseridos += 1


# ==================================================
# PROCESSAMENTO
# ==================================================

historico = carregar_historico()

for arquivo in os.listdir(PASTA_PDFS):

    if not arquivo.lower().endswith(".pdf"):
        continue

    caminho_pdf = os.path.join(
        PASTA_PDFS,
        arquivo
    )

    try:

        sha = calcular_sha256(
            caminho_pdf
        )

        if sha in historico:

            print(
                f"⏭ PDF ignorado (SHA já processado): {arquivo}"
            )

            total_pdfs_ignorados += 1

            continue

        dados = extrair_dados_pdf(
            caminho_pdf
        )

        if not dados:
            continue

        pedido, rms = dados

        salvar_supabase(
            pedido,
            rms
        )

        historico[sha] = {
            "pedido": pedido,
            "rms": rms,
            "arquivo": arquivo,
            "processado_em": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        salvar_historico(
            historico
        )

        print(
            f"💾 Histórico atualizado para {arquivo}"
        )

    except Exception as erro:

        total_erros += 1

        print(
            f"❌ Erro em {arquivo}"
        )

        print(erro)


# ==================================================
# RESUMO
# ==================================================

print("\n")
print("========================================")
print("PROCESSAMENTO FINALIZADO")
print("========================================")
print(f"✅ Registros inseridos : {total_inseridos}")
print(f"⏭ Registros ignorados : {total_ignorados}")
print(f"📄 PDFs ignorados     : {total_pdfs_ignorados}")
print(f"❌ Erros              : {total_erros}")
print("========================================")