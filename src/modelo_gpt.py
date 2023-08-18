import openai
from src.functions import *

# Chave Felype - GPT
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