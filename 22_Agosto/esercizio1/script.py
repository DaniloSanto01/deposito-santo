import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Carica variabili dal file .env
load_dotenv(dotenv_path=".env")

# Recupero variabili ambiente
openai_api_key = os.getenv("AZURE_OPENAI_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# print(openai_api_key)
# print(endpoint)
# print(api_version)
# print(deployment)

# Creo client Azure OpenAI
client = AzureOpenAI(
    api_key=openai_api_key,
    api_version=api_version,
    azure_endpoint=endpoint
)

# Eseguo una richiesta al modello
response = client.chat.completions.create(
    model=deployment,  # qui va il nome del deployment, non "gpt-4"
    messages=[
        {"role": "system", "content": "Sei un assistente utile."},
        {"role": "user", "content": "Scrivimi un haiku sugli sviluppatori Python."}
    ],
    max_tokens=200,
    temperature=2
)

# Stampo la risposta
print(response.choices[0].message.content)
