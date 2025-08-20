import pandas as pd
import os
os.system('cls' if os.name == 'nt' else 'clear')

df = pd.read_csv("20_Agosto\dataset\Mall_Customers.csv")

print(df.head())
print(df.info())
print('Shape: ', df.shape)


print(df.isnull().sum()) # indica quanti valori nulli ci sono per colonna, isnull() crea un vettore booleano per ogni colonna impostando True se è nullo e False se è avvalorato, applicando .sum() contiamo quanti True(ovvero valori nulli) ci sono in ogni colonna

# K-Means funziona solo su feature numeriche, le mie colonne sono:
# CustomerID,Genre,Age,Annual Income (k$),Spending Score (1-100)
# -Genre è di tipo stringa quindi devo codificarlo, li mappo a 0(femmina) o 1(maschio)
# -customerID è un identificativo e non ha senso per il K-Means, ovvero non da informazioni all'algoritmo
#             sul comportamento che assume il cliente, non aiuta nei raggruppamenti

# mappo il Genre
df['Genre'] = df['Genre'].map({'Male': 1,
                               'Female': 0})

# print(df.loc[:10, 'Genre'])


# ==========================
# SCALATURA DATI
# K-Means è sensibile alle scale: se una variabile ha valori molto più grandi 
# (es. reddito annuale in migliaia), domina sulle altre.
# ===========================

from sklearn.preprocessing import StandardScaler

features = ['Genre', 'Age', 'Annual Income (k$)', 'Spending Score (1-100)']
X = df[features] # prendo un sottoinsieme del df iniziale con le sole colonne che vorrò includere nel clustering

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X) # le features sono state scalate


# ==============
# K-MEANS
# cerchiamo prima il numero ottimale di cluster
# tramite l'elbow method
# ==============
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

wcss = []  # Within-Cluster Sum of Squares, qui dentro memorizzo la somma delle distanze al quadrato tra ogni punto e il centroide del cluster a cui appartiene, questo poi sommato agli altri wcss degli altri cluster, misura quanto i clster sono compatti, più questo valore è basso più i cluster sono "stretti", il WCSS altro non è che la somma delle distanze quadratiche di ciascun punto x_i dal suo centroide c.
for k in range(1, 15): # proviamo diversi numeri di cluster
    kmeans = KMeans(n_clusters=k, init='k-means++', random_state=42) # init='k-means++': inizializzazione “intelligente” dei centroidi, random_state=42: seme fisso per avere sempre gli stessi risultati (riproducibilità)
    kmeans.fit(X_scaled)
    wcss.append(kmeans.inertia_)

plt.plot(range(1, 15), wcss, marker='o') # plotto sull'asse x i vari numeri di cluster, sull'asse y il valore si wcss ottenuto per ogni cluster 
plt.xlabel('Numero di cluster')
plt.ylabel('WCSS')
plt.title('Elbow Method')
plt.show()
"""
Il grafico che ottieni decresce sempre (più cluster = punti più vicini ai centroidi = WCSS più basso).
Ma non vogliamo esagerare: troppi cluster = overfitting.
Il punto giusto è dove la curva inizia ad “appiattirsi”, cioè forma un gomito:
Prima del gomito: aggiungere cluster riduce molto il WCSS.
Dopo il gomito: aggiungere cluster riduce poco il WCSS → non vale la pena.
"""





# dopo aver osservato il grafico scelgo k=11, e quindi effettuo il clustering vero e proprio
kmeans = KMeans(n_clusters=11, init='k-means++', random_state=42)
df['Cluster'] = kmeans.fit_predict(X_scaled) # ogni cliente avrà il suo cluster associato



import matplotlib.pyplot as plt

plt.scatter(df['Annual Income (k$)'], df['Spending Score (1-100)'], c=df['Cluster'], cmap='rainbow')
plt.xlabel('Annual Income (k$)')
plt.ylabel('Spending Score (1-100)')
plt.show()