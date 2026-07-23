from leRM import processar_rms
from lePC import processar_pedidos
from lePDF import processar_pdfs
from leApprovo import processar_approvo
from datetime import datetime

def log(mensagem):
    print(f"[{datetime.now():%d/%m/%Y %H:%M:%S}] {mensagem}")

def main():

    log("Iniciando processamento de RMs")
    processar_rms()

    log("Iniciando processamento de Pedidos")
    processar_pedidos()

    log("Iniciando processamento de PDFs")
    processar_pdfs()
    
    log("Iniciando processamento dos Relatorios do Approval")
    processar_approvo()

    log("Processamento concluído")

    print("=== PROCESSAMENTO CONCLUÍDO ===")

if __name__ == "__main__":
    main()