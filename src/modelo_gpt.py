import openai
from src.functions import *

# Chave Felype - GPT

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

openai.api_key = obter_api()
    
model_engine = "text-davinci-003"

def get_response(prompt):
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=200,
        temperature = 0.5,
    )
    return response.choices[0].text