import json
import pandas as pd
import streamlit as st


def adicionar_usuario(email, senha):
    """
    Adiciona um novo usuário (email e senha) ao arquivo "db/usuarios.json".

    Args:
        email (str): O email do novo usuário.
        senha (str): A senha do novo usuário.

    """
    with open("db/usuarios.json", "r") as file:
        data = json.load(file)

    novo_usuario = {"email": email, "senha": senha, "dataframes": []}
    data["usuarios"].append(novo_usuario)

    with open("db/usuarios.json", "w") as file:
        json.dump(data, file)


def consultar_usuario(email, senha):
    """
    Consulta se o usuário com o email e senha fornecidos existe no arquivo "db/usuarios.json".

    Args:
        email (str): O email do usuário a ser consultado.
        senha (str): A senha do usuário a ser consultado.

    Returns:
        bool: True se o usuário for encontrado com o email e senha corretos, False caso contrário.

    """
    with open("db/usuarios.json", "r") as file:
        data = json.load(file)

    for usuario in data["usuarios"]:
        if usuario["email"] == email and usuario["senha"] == senha:
            return True

    return False


def registrar_email_em_log(email):
    """
    Registra o email no arquivo de log "log.txt", sobrescrevendo o email se já estiver presente.

    Args:
        email (str): O email a ser registrado no arquivo de log.

    """
    with open("util/log.txt", "w") as file:
        file.write(email)
        


def consultar_email_em_log():
    """
    Consulta se o email fornecido está presente no arquivo de log "log.txt".

    Args:
        email (str): O email a ser consultado no arquivo de log.

    Returns:
        bool: True se o email for encontrado no arquivo de log, False caso contrário.

    """
    with open("util/log.txt", "r") as file:
        linhas = file.readlines()
    return linhas[0]


def ler_dataframe_e_converter(df, sheet_name=None):
    """
    Lê um arquivo CSV ou Excel e retorna as listas de colunas e dados.

    Args:
        caminho_arquivo (str): Caminho para o arquivo CSV ou Excel.
        sheet_name (str, optional): Nome da planilha no arquivo Excel, caso aplicável.
                                    Padrão é None (usado apenas para arquivos Excel).

    Returns:
        tuple: Uma tupla contendo as listas de colunas (lista) e dados (lista).

    """
    

    colunas = df.columns.tolist()
    dados = df.values.tolist()

    return colunas, dados

    


def adicionar_dataframe_para_email(email, dataframe_id, colunas, dados):
    """
    Procura o email da pessoa dentro do JSON e adiciona um novo dataframe
    à lista de dataframes correspondente ao email encontrado.

    Args:
        email (str): O email da pessoa para o qual o dataframe será adicionado.
        dataframe_id (str): O nome do dataframe a ser adicionado.
        colunas (list): Lista contendo o nome das colunas do dataframe.
        dados (list): Lista de listas contendo os dados do dataframe.

    Returns:
        bool: True se o email for encontrado e o dataframe for adicionado,
              False se o email não for encontrado.

    """
    with open("db/usuarios.json", "r") as file:
        data = json.load(file)

    for usuario in data["usuarios"]:
        email_para_teste = str(usuario["email"]).lower()
        email = str(email).lower()
        try:
            dataframes = usuario.get("dataframes", [])
            novo_dataframe = {
                "id": dataframe_id,
                "colunas": colunas,
                "dados": dados
            }
            dataframes.append(novo_dataframe)
            usuario["dataframes"] = dataframes
            with open("db/usuarios.json", "w") as file:
                json.dump(data, file)
            return True
        except:
            return False


