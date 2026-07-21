import pandas as pd


def criar_multiindex_compras(df_final):

    ordem_colunas = [
        #RM MEGA
        "Requisitante",
        "Nr. RM",
        "Material",
        "Descrição",
        "Qt. Sol",
        "Data RM",
        "Data Necessidade",

        # Status RM Approvals
        "Status Aprovação",
        "Dt de Aprovação",
        "Aprovador Ocorrência",
        
        # Pedido de compra MEGA
        "Comprador",
        "Nr. Pedido",
        "Qt. Compr.",
        "dt_entrega",
        
        #"Data Ocorrência",
        #"Aprovador RM",

        "Status Pedido",

        
        "Status Aprovação Pedido",
        "Dt Aprovação Pedido",
        "Aprovador Pedido",

        #"Situação Pedido",

        "Status da Baixa",
        "Prazo Entrega",

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
            "Dt. Requisição"
        ),

        "Data Necessidade": (
            "REQUISIÇÃO DE MATERIAL MEGA",
            "Dt. Necessidade"
        ),
        # Aprovação da RM 
        "Status Aprovação": (
            "APROVAÇÃO DA RM",
            "Status"
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
        
        
        "dt_entrega": (
            "PEDIDO DE COMPRA MEGA",
            "Dt. Entrega"
        ),
        

        
        ### Falta a data de compra
        
        # Aproval do Pedido de Compra 
        
        #"Data Ocorrência": (
            #"APROVAÇÃO DO PEDIDO - Approval",
            #"Data da Ocorrência"
        #),
        
        
        "Status Aprovação Pedido": (
            "APROVAÇÃO DO PEDIDO",
            "Status"
        ),

        "Dt Aprovação Pedido": (
            "APROVAÇÃO DO PEDIDO",
            "Dt. Aprovação"
        ),

        "Aprovador Pedido": (
            "APROVAÇÃO DO PEDIDO",
            "Aprovador"
        ),

        
        ##### Aqui
        #"Situação Pedido": (
         #   "APROVAÇÃO DO PEDIDO",
          #  "Situação"
       #),
        
       # "Status Pedido": (
        #   "APROVAÇÃO DO PEDIDO",
        #),


        "Aprovador RM": (
            "ARRUMAR",
            "Solicitante"
        ),

                
        "Status da Baixa": (
            "SITUAÇÃO",
            "Status da Baixa"
        ),
        
        
        "Prazo Entrega": (
            "SITUAÇÃO",
            "Prazo Entrega"
        ),


    }
    
    print(df_final.columns.tolist())
    df_exibicao = df_final[ordem_colunas].copy()

    
    
    for col in ordem_colunas:

        if col not in colunas_multiindex:

            raise Exception(
                f"Coluna '{col}' não encontrada em colunas_multiindex"
            )


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
        if campo == "Status":
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