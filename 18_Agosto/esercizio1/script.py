def conta_righe(righe : list[str]) -> int: 
    return len(righe)

def conta_parole(righe: list[str]) -> int:
    """Conta il numero totale di parole in una lista di righe."""
    return sum(len(riga.split()) for riga in righe)

import string

def top_parole(file_path: str="prova.txt", top_n: int = 5) -> None:
    """Stampa le top N parole più frequenti in un file usando solo dizionario."""
    # Leggi il file
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Normalizza il testo: minuscolo e rimuove punteggiatura
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Dividi in parole
    parole = text.split()

    # Conta le occorrenze con un dizionario
    conteggio = {}
    for parola in parole:
        if parola in conteggio:
            conteggio[parola] += 1
        else:
            conteggio[parola] = 1

    # Ordina le parole per conteggio decrescente
    top = sorted(conteggio.items(), key=lambda x: x[1], reverse=True)[:top_n]

    # Stampa le top N
    for parola, count in top:
        print(f"{parola}: {count}")


top_parole(top_n=5)





with open("prova.txt", "r", encoding="utf-8") as f:
    righe = f.readlines()

print(f'Righe nel file: {conta_righe(righe)}')
print(f'Parole nel file: {conta_parole(righe)}')


