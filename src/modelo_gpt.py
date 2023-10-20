import openai
from src.functions import *

# Chave Felype - GPT

# openai.api_key = "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"
# openai.api_key = "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"

# openai.api_key = "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"

openai.api_key = "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"


model_engine = "text-davinci-003"

def get_response(prompt):
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=200,
        temperature = 0.5,
    )
    return response.choices[0].text