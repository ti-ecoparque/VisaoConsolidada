import pandas as pd
import numpy as np

def aplicar_estilo_alerta(val):
    """Aplica cores de fundo de acordo com o texto da coluna Status Aprovação."""
    if not isinstance(val, str):
        return ""
    val_upper = val.upper()
    if val_upper in ["A", "APROVADO"]:
        return "background-color: #e2f0d9; color: #385723; font-weight: bold;"
    elif val_upper in ["R", "REPROVADO"]:
        return "background-color: #fce4d6; color: #c00000; font-weight: bold;"
    elif val_upper in ["P", "PENDENTE"]:
        return "background-color: #fff2cc; color: #7f6000; font-weight: bold;"
    return ""

def processar_dataframe_compras(dados_brutos: list) -> pd.DataFrame:
    if not dados_brutos:
        return pd.DataFrame()

    df = pd.DataFrame(dados_brutos)
    
    # Dicionário com a ordem estrita de todas as colunas (incluindo Data Necessidade)
    mapeamento_colunas = {
        # Requisição Mega
        "rm_usuario_solicitante": "Requisitante",
        "rm_numero": "Nr. RM",
        "rm_material": "Material",
        "rm_descricao": "Descrição",
        "rm_qtd_solicitada": "Qt. Sol",
        "rm_data_emissao": "Data RM",
        "rm_data_necessidade": "Data Necessidade",
        
        # Rel do Aprovo
        "app_status_doc": "Status Aprovação",
        "app_nome_aprovador": "Aprovador Ocorrência",
        "app_data_documento": "Dt de Aprovação",
        
        #Pedido de compra do Mega
        "ped_comprador": "Comprador",
        "pc_numero": "Nr. Pedido",
        # Falta data de Entrega 
        "ped_quantidade_comprada": "Qt. Compr.",
       
        # Approval dos Pedidos de Compra 
        
        "ped_situacao": "Situação Pedido",

        "ped_status_descricao": "Status Pedido",
        #"app_data_ocorrencia": "Data Ocorrência", # Ocoorencia Aprovp
        "app_nome_solicitante": "Aprovador RM",   #Rel Aprovo
        
        #"app_nome_aprovador" : "Aprovador App",
        "app_data_ocorrencia": "Dt Ocorrência", # Ocoorencia Aprovp
        #"app_status_doc": "Status App",
        
        "pc_data_entrega": "dt_entrega",
        
        # Status Final 
        "rm_situacao_item": "Status da Baixa"
        
    }

    # CORREÇÃO CRUCIAL: Trocado '...' por 'coluna_banco' para forçar a criação das colunas vazias
    for coluna_banco in mapeamento_colunas.keys():
        if coluna_banco not in df.columns:
            df[coluna_banco] = None

    # Limita o tamanho do texto da descrição para não quebrar o layout da tabela
    if "rm_descricao" in df.columns:
        df["rm_descricao"] = df["rm_descricao"].fillna("None").astype(str).apply(
            lambda x: x[:30] + "..." if len(x) > 30 else x
        )

    # Formatação de todas as colunas de data no padrão brasileiro
    if "rm_data_emissao" in df.columns:
        df["rm_data_emissao"] = pd.to_datetime(df["rm_data_emissao"], errors='coerce').dt.strftime('%d/%m/%Y')
        
    if "rm_data_necessidade" in df.columns:
        df["rm_data_necessidade"] = pd.to_datetime(df["rm_data_necessidade"], errors='coerce').dt.strftime('%d/%m/%Y')
        
    if "app_data_documento" in df.columns:
        df["app_data_documento"] = pd.to_datetime(df["app_data_documento"], errors='coerce').dt.strftime('%d/%m/%Y')
        
    if "app_data_ocorrencia" in df.columns:
        df["app_data_ocorrencia"] = pd.to_datetime(df["app_data_ocorrencia"], errors='coerce').dt.strftime('%d/%m/%Y %H:%M')
        
    # Formata Campos para inteiro
    if "pc_numero" in df.columns:
        df["pc_numero"] = df["pc_numero"].apply(
            lambda x: str(int(float(x))) if pd.notna(x) and str(x).strip() not in ["", "None"] else None)
    
    if "ped_quantidade_comprada" in df.columns:
        df["ped_quantidade_comprada"] = (pd.to_numeric(df["ped_quantidade_comprada"], errors="coerce").fillna(0).astype(int))

    if "rm_qtd_solicitada" in df.columns:
        df["rm_qtd_solicitada"] = (pd.to_numeric(df["rm_qtd_solicitada"], errors="coerce").fillna(0).astype(int))

    
    # Força a ordenação final e substitui todos os nulos por "None" para aparecer na tela
    df_ordenado = df[list(mapeamento_colunas.keys())].copy()
    df_final = df_ordenado.rename(columns=mapeamento_colunas)
    df_final = df_final.replace({np.nan: "None", None: "None"}).astype(str).replace("nan", "None")
    
    return df_final
