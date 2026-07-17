import pandas as pd


def criar_multiindex_compras(df_final):

    ordem_colunas = [
        "Requisitante",
        "Nr. RM",
        "Material",
        "Descrição",
        "Qt. Sol",
        "Data RM",
        "Data Necessidade",

        "Status Aprovação",
        "Dt de Aprovação",
        "Aprovador Ocorrência",
        
        "Comprador",
        "Nr. Pedido",
        "Qt. Compr.",
        
        #"Data Ocorrência",
        #"Aprovador RM",

        "Status Pedido",

        "Situação Pedido",
        
        "Status da Baixa"
    ]

    colunas_multiindex = {

        "Requisitante": (
            "REQUISIÇÃO DE MATERIAL MEGA",
            "Requisitante"
        ),

        "Nr. RM": (
            "REQUISIÇÃO DE MATERIAL MEGA",
            "Nr. RM"
        ),

        "Material": (
            "REQUISIÇÃO DE MATERIAL MEGA",
            "Material"
        ),

        "Descrição": (
            "REQUISIÇÃO DE MATERIAL MEGA",
            "Descrição"
        ),

        "Qt. Sol": (
            "REQUISIÇÃO DE MATERIAL MEGA",
            "Qt. Sol."
        ),

        "Data RM": (
            "REQUISIÇÃO DE MATERIAL MEGA",
            "Data da Requisição"
        ),

        "Data Necessidade": (
            "REQUISIÇÃO DE MATERIAL MEGA",
            "Dt. Necessidade"
        ),
        # Aprovação da RM 
        "Status Aprovação": (
            "APROVAÇÃO DA RM",
            "Status da Aprovação"
        ),

        "Aprovador Ocorrência": (
            "APROVAÇÃO DA RM",
            "Aprovador"
        ),
        
        "Dt de Aprovação": (
            "APROVAÇÃO DA RM",
            "Dt. Aprovação"
        ),

        # Pedido de Compra
         "Comprador": (
            "PEDIDO DE COMPRA MEGA",
            "Comprador"
        ),
        
         "Nr. Pedido": (
            "PEDIDO DE COMPRA MEGA",
            "Nr. PC"
        ),

        "Qt. Compr.": (
            "PEDIDO DE COMPRA MEGA",
            "Qt. Compr."
        ),
        
        ### Falta a data de compra
        
        # Aproval do Pedido de Compra 
        
        #"Data Ocorrência": (
            #"APROVAÇÃO DO PEDIDO - Approval",
            #"Data da Ocorrência"
        #),
        
        "Situação Pedido": (
            "APROVAÇÃO DO PEDIDO",
            "Situação"
        ),
        
        "Status Pedido": (
            "APROVAÇÃO DO PEDIDO",
            "Status da Aprovação"
        ),


        #"Aprovador RM": (
            #"ARRUMAR",
            #"Solicitante"
        #),

                
        "Status da Baixa": (
            "SITUAÇÃO",
            "Status da Baixa"
        )

    }

    df_exibicao = df_final[ordem_colunas].copy()

    df_exibicao.columns = pd.MultiIndex.from_tuples(
        [colunas_multiindex[col] for col in ordem_colunas]
    )

    return df_exibicao


def destacar_rm(df):
    estilos = pd.DataFrame(
        "",
        index=df.index,
        columns=df.columns
    )

    for col in df.columns:
        grupo = col[0]
        campo = col[1]
        # Grupo RM
        if grupo == "REQUISIÇÃO DE MATERIAL MEGA":
            estilos[col] = (
                "background-color:#f2f7f2;"
                "color:#000000;"
            )
        if grupo == "APROVAÇÃO DA RM":
            estilos[col] = (
                "background-color:#e2f0d9;"
                "color:#000000;"
            )    
        if grupo == "PEDIDO DE COMPRA MEGA":
            estilos[col] = (
                "background-color:#fbf2fa;"
                "color:#000000;"
            )  
        
        if grupo == "APROVAÇÃO DO PEDIDO":
            estilos[col] = (
                "background-color:#f3daf1;"
                "color:#000000;"
            )
            
        # Status
        if campo == "Status da Aprovação":
            for idx in df.index:
                valor = str(df.at[idx, col]).upper()
                if valor == "APROVADO":
                    estilos.at[idx, col] = (
                        "background-color:#e2f0d9;"
                        "color:#385723;"
                        "font-weight:bold;"
                    )

                elif valor == "REPROVADO":
                    estilos.at[idx, col] = (
                        "background-color:#fce4d6;"
                        "color:#c00000;"
                        "font-weight:bold;"
                    )
                elif valor == "PENDENTE":
                    estilos.at[idx, col] = (
                        "background-color:#fff2cc;"
                        "color:#7f6000;"
                        "font-weight:bold;"
                    )
        
        
    if campo == "Status da Baixa":

        for idx in df.index:
            valor = str(df.at[idx, col]).upper()
            if valor == "ABERTO":
                estilos.at[idx, col] = (
                    "background-color:#fff2cc;"
                    "color:#7f6000;"
                    "font-weight:bold;"
                )

            elif valor == "BAIXADO":
                estilos.at[idx, col] = (
                    "background-color:#e2f0d9;"
                    "color:#385723;"
                    "font-weight:bold;"
                )

            elif valor == "PENDENTE":
                estilos.at[idx, col] = (
                    "background-color:#fce4d6;"
                    "color:#c00000;"
                    "font-weight:bold;"
                )

            elif valor == "APROVAR ESTOQUE":
                estilos.at[idx, col] = (
                    "background-color:#ddebf7;"
                    "color:#1f4e78;"
                    "font-weight:bold;"
                )            

    return estilos