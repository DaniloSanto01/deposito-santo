import pandas as pd
import numpy as np

"""
I dati si riferiscono al carico energetico/domanda di energia elettrica della città Dayton 
(Dayton, Ohio, USA).
"""
df = pd.read_csv("19_Agosto\dataset\DAYTON_hourly.csv")


df['Datetime'] = pd.to_datetime(df['Datetime']) # convertiamo la colonna in Datetime
df['Date'] = df['Datetime'].dt.date # Aggiungo una colonna con la sola data (senza ora) per raggruppare

# Raggruppo per Date e calcolo la media giornaliera sul consumo
df['MediaGiornaliera'] = df.groupby("Date")['DAYTON_MW'].transform('mean')

df['EtichettaGiorn'] = df['DAYTON_MW'] > df['MediaGiornaliera']

# Rendo la colonna più leggibile (Alto/Basso invece di True/False)
df['EtichettaGiorn'] = df['EtichettaGiorn'].map({True: 'Alto consumo (gg)', False: 'Basso consumo (gg)'})
print(df.head(30))




# aggiungo colonna settimana
df['Week'] = df['Datetime'].dt.to_period('W').apply(lambda r: r.start_time)

# calcolo media settimanale
df['MediaSettimanale'] = df.groupby("Week")['DAYTON_MW'].transform('mean')

# faccio il confronto, quindi etichetto ogni ora rispetto la media settimanale
# e poi mappo i ooleani a valori stringa
df['EtichettaSett'] = df['DAYTON_MW'] > df['MediaSettimanale']
df['EtichettaSett'] = df['EtichettaSett'].map({True: 'Alto Consumo (sett)', 
                         False: 'Basso consumo (sett)'})


print("\nEtichette:\n", df[['Datetime', 'DAYTON_MW', 'MediaGiornaliera', 'EtichettaGiorn', 'MediaSettimanale', 'EtichettaSett']].head(50))