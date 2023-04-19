import openai

# Chave Felype - GPT
with open("util/api_key.txt", "r") as file:
    openai.api_key = file.read()
    
model_engine = "text-davinci-003"

def get_response(prompt):
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=200,
        temperature = 0.5,
    )
    return response.choices[0].text