import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from openai import RateLimitError
"""
tenacity è una libreria Python che serve a gestire i retry automatici di funzioni che possono fallire, senza dover scrivere tu manualmente tutti i cicli di tentativi, sleep, e gestione degli errori.

🔹 A cosa serve concretamente:
- Immagina di fare richieste a un'API (come Azure OpenAI), ma a volte ricevi errori temporanei:
- 429 Too Many Requests → superato il rate limit
- TimeoutError → richiesta impiega troppo tempo
- ConnectionError → problemi di rete

Senza tenacity dovresti scrivere qualcosa tipo:
        success = False
        for i in range(5):
            try:
                response = client.chat.completions.create(...)
                success = True
                break
            except RateLimitError:
                time.sleep(2 ** i)  # intervallo esponenziale
        if not success:
            print("Fallito dopo 5 tentativi")
    
Con tenacity, tutto questo diventa molto più pulito:
        from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
        from openai.error import RateLimitError

        @retry(
            retry=retry_if_exception_type(RateLimitError),
            wait=wait_exponential(min=2, max=30),
            stop=stop_after_attempt(5)
        )
        def get_haiku():
            return client.chat.completions.create(...).choices[0].message.content

-La funzione ritenta automaticamente se riceve un errore specifico (RateLimitError).
-Gestisce quanto tempo aspettare tra i retry (wait_exponential).
-Interrompe i retry dopo un certo numero di tentativi (stop_after_attempt).

🔹 Vantaggi:
    -Codice pulito → niente cicli manuali con try/except e sleep.
    -Flessibile → puoi decidere su quali errori ritentare, quanti tentativi, intervallo tra retry.
    -Robusto → riduce la probabilità che il tuo script fallisca per problemi temporanei o rate limit.
"""

# Carica variabili dal file .env
load_dotenv(dotenv_path=".env")

# Recupero variabili ambiente
openai_api_key = os.getenv("AZURE_OPENAI_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# Creo client Azure OpenAI
client = AzureOpenAI(
    api_key=openai_api_key,
    api_version=api_version,
    azure_endpoint=endpoint
)

# Decoratore retry
"""
Spiegazione di cosa fa:
- @retry(...) → indica che la funzione get_haiku verrà rilanciata automaticamente se si verifica un errore specifico.
- retry_if_exception_type(RateLimitError) → ritenta solo se l’errore è un Rate Limit (429).
- wait_exponential(min=2, max=30) → ogni retry aspetta un intervallo esponenziale:
    primo retry → 2s
    secondo retry → 4s
    terzo retry → 8s
    … fino a max 30s
- stop_after_attempt(5) → si ferma dopo 5 tentativi se non riesce a ottenere risposta.
"""
@retry(
    retry=retry_if_exception_type(RateLimitError),  # ritenta solo se è un RateLimitError (429)
    wait=wait_exponential(min=2, max=30),         # intervallo esponenziale tra retry: 2s → 4s → 8s ... max 30s
    stop=stop_after_attempt(5)                     # massimo 5 tentativi
)
def get_response():
    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "Sei un assistente utile."},
            {"role": "user", "content": "Scrivimi un haiku sugli sviluppatori Python."}
        ],
        max_tokens=200,
        temperature=0.2
    )
    return response.choices[0].message.content

# Chiamata alla funzione con retry automatico
print(get_response())
