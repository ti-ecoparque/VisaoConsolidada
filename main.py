from leRM import processar_rms
from lePC import processar_pedidos
from lePDF import processar_pdfs
from leApprovo import processar_approvo
from datetime import datetime
import time


#Ação       C:\Users\ti\AppData\Local\Microsoft\WindowsApps\python.exe
#Agrumento "C:\Users\ti\OneDrive - ECOPARQUE BAIRROS INTEGRADOS LTDA\PY\api_ecoparque365\api_lista_materiais.py"
#Iniciar    C:\Users\ti\OneDrive - ECOPARQUE BAIRROS INTEGRADOS LTDA\PY\api_ecoparque365

def log(mensagem):
    texto = f"[{datetime.now():%d/%m/%Y %H:%M:%S}] {mensagem}"

    print(texto)

    with open("execucao.log", "a", encoding="utf-8") as f:
        f.write(texto + "\n")

def main():

    log("-----------Iniciando processamento de RMs-----------")
    processar_rms()
    log("-----------Fim processamento de RMs-----------")


    log("-----------Iniciando processamento de Pedidos-----------")
    processar_pedidos()
    log("-----------Fim processamento de Pedidos-----------")


    log("-----------Iniciando processamento de PDFs-----------")
    processar_pdfs()
    log("-----------Fim processamento de PDFs-----------")


    log("Iniciando processamento dos Relatorios do Approval")
    processar_approvo()
    log("-----------Fim processamento dos Relatorios do Approval-----------")


    log("**********Processamento concluído************")

    print("=== PROCESSAMENTO CONCLUÍDO ===")
    print("Janela será fechada em 30 segundos...")

    time.sleep(45)

if __name__ == "__main__":
    main()