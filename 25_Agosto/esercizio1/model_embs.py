from openai import AzureOpenAI
from dotenv import load_dotenv
import os
import json

# Carica variabili dal file .env
load_dotenv(dotenv_path="C:\\Users\\XS452CF\\OneDrive - EY\\Desktop\\deposito-santo\\.env")

# Recupero variabili ambiente
openai_api_key = os.getenv("AZURE_OPENAI_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")
embedding_deployment = os.getenv("AZURE_OPENAI_EMBEDING_DEPLOYMENT")

# print(openai_api_key)
# print(endpoint)
# print(api_version)
# print(embedding_deployment)


# Configura il client
client = AzureOpenAI(
    api_key=openai_api_key,  
    api_version=api_version,     # importante: dipende dalla versione disponibile
    azure_endpoint=endpoint
)

# Testo da trasformare in embedding
text = "Hello World"

# Calcolo embedding
response = client.embeddings.create(
    model=embedding_deployment,   # il nome del deployment su Azure
    input=text
)

#print("Response modello:", json.dumps(response.model_dump(), indent=2)) # model_dump() converto l'oggetto in un dizionario python, json.dumps() prende un oggetto python (dict, stringa, lista) e lo trasforma in una stringa json, indent=2 Serve a rendere il JSON “leggibile”, cioè con ritorni a capo e spazi per la gerarchia.print("\n\n")
embedding = response.data[0].embedding
print("Dimensione embedding:", len(embedding))
print("Primi 10 valori:", embedding[:10])