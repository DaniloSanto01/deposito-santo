def conta_righe(righe : list[str]) -> int: 
    return len(righe)

def conta_parole(righe: list[str]) -> int:
    """Conta il numero totale di parole in una lista di righe."""
    return sum(len(riga.split()) for riga in righe)

with open("prova.txt", "r", encoding="utf-8") as f:
    righe = f.readlines()

print(f'Righe nel file: {conta_righe(righe)}')
print(f'Parole nel file: {conta_parole(righe)}')
