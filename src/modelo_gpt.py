import openai

# Chave Felype - GPT
openai.api_key = "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"
model_engine = "text-davinci-003"

def gpt(prompt):
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=200,
        temperature = 0.5,
    )
    return response.choices[0].text