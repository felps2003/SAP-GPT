import json
import pandas as pd
import streamlit as st
import openai
import re


def adicionar_usuario(nome, email, senha):
    """
    Adiciona um novo usuário (email e senha) ao arquivo "db/usuarios.json".

    Args:
        email (str): O email do novo usuário.
        senha (str): A senha do novo usuário.

    """
    with open("db/usuarios.json", "r") as file:
        data = json.load(file)
    with open("db/dataframes.json", "r") as file:
        df = json.load(file)

    novo_usuario = {"Nome": nome,
                    "email": email, 
                    "senha": senha, 
                    "dataframes": 0, 
                    "requests API": 0, 
                    "acessos": 0, 
                    "API": ''}
    
    novo_df_usuario = {"email": email, "dataframes": []}

    data["usuarios"].append(novo_usuario)

    df["bases"].append(novo_df_usuario)

    with open("db/usuarios.json", "w") as file:
        json.dump(data, file)
    with open("db/dataframes.json", "w") as file:
        json.dump(df, file)

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
    with open("db/dataframes.json", "r") as file:
        data = json.load(file)

    for usuario in data["bases"]:
        email_para_teste = str(usuario["email"]).lower()
        email = str(email).lower()
        st.warning(email_para_teste+'/'+email)
        if email_para_teste == email:
            dataframes = usuario.get("dataframes", [])
            novo_dataframe = {
                "id": dataframe_id,
                "colunas": colunas,
                "dados": dados
            }
            dataframes.append(novo_dataframe)
            usuario["dataframes"] = dataframes
            with open("db/dataframes.json", "w") as file:
                json.dump(data,file) 
            with open("db/usuarios.json", "r") as file:
                data = json.load(file)
            for usuario in data["usuarios"]:
                if usuario["email"] == email:
                    usuario["dataframes"] += 1
                    with open("db/usuarios.json", "w") as arquivo:
                        json.dump(data, arquivo)
                    return True
        
    return False


def atualizar_chave_api(nova_chave_api):
    email_alvo = consultar_email_em_log()
    """
    Esta função atualiza a chave 'Token' de um usuário em um arquivo JSON,
    desde que o email desse usuário corresponda ao email alvo.

    :param nova_chave_api: A nova chave 'Token' a ser atribuída.
    """
    with open("db/usuarios.json", 'r') as arquivo:
        data = json.load(arquivo)

    for usuario in data['usuarios']:
        if usuario.get('email') == email_alvo:
            usuario['API'] = nova_chave_api

    with open("db/usuarios.json", 'w') as arquivo:
        json.dump(data, arquivo, indent=4)


def obter_api():
    email_alvo = consultar_email_em_log()
    """
    Esta função busca a chave 'Token' de um usuário com base no email fornecido.

    :param arquivo_json: O caminho para o arquivo JSON.
    :param email_alvo: O email do usuário cuja chave 'Token' será obtida.
    :return: A chave 'Token' do usuário ou None se o email não for encontrado.
    """
    with open("db/usuarios.json", 'r') as arquivo:
        data = json.load(arquivo)

    for usuario in data['usuarios']:
        if usuario.get('email') == email_alvo:
            return usuario.get('API')
        


def return_produtos_df(produto):
    prompt = "Escreva uma descricao para o produto {x}, que contenha detalhes do mesmo.".format(x = produto)
    return {"produto": produto,
            "descricao": get_response(prompt = prompt),}



def get_response(prompt):
    openai.api_key = obter_api()
    model_engine = "text-davinci-003"
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=200,
        temperature = 0.5,
    )
    return response.choices[0].text


def testeEmail(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    return False


