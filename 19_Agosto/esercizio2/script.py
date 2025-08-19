import os
import pandas as pd
import numpy as np

os.system('cls' if os.name == 'nt' else 'clear')

df = pd.read_csv("19_Agosto\dataset\AirQualityUCI.csv", sep=";", decimal=",")

# I valori mancanti nel dataset sono indicati con il "-200"
df = df.replace(-200, np.nan)

# Creo colonna Datetime combinando le 2 colonne Date e Time
df["Datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"], 
                                format="%d/%m/%Y %H.%M.%S", errors="coerce")

# Ordino per data/ora
df = df.sort_values("Datetime").reset_index(drop=True)

print(df.head())
print(df.info())


# Scelta dell'inquinante
pollutant = "NO2(GT)"

# Tengo solo righe con dato valido per l'inquinante e la data/ora, tutte le righe che hanno anche un solo valore mancante per inquinante e/o Datatime verranno rimosse
df = df.dropna(subset=[pollutant, "Datetime"]).copy()

# Media giornaliera del pollutante (per ogni giorno)
df["day"] = df["Datetime"].dt.date # creo colonna giorno
df["daily_mean"] = df.groupby("day")[pollutant].transform("mean") # raggruppo per giorno e calcolo la media giornaliera del valore dell'inquinante 


# Calcolo se ogni valore orario è sopra o sotto la media, 
# ottengo poi una colonna di 0 ed 1, che successivamente
# etichetto: 1 = poor (sopra la media del giorno), 0 = good
df["y"] = (df[pollutant] > df["daily_mean"]).astype(int)
df["quality"] = df["y"].map({0: "good", 1: "poor"})


# Controllo bilanciamento classi
print("Bilanciamento classi:")
print(df["quality"].value_counts(normalize=True).round(3))

print("\nAnteprima:")
print(df[["Datetime", pollutant, "daily_mean", "quality"]].head(10))



from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt

# Definiamo feature da escludere
exclude_cols = ["Date", "Time", "Datetime", "day", "daily_mean", "y", "quality", pollutant]
feature_cols = [c for c in df.columns if c not in exclude_cols]

X = df[feature_cols].select_dtypes(include=[np.number])
y = df["y"]

# Split per train/test set (80% - 20%)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Istanzio e addestro albero di decisione
tree = DecisionTreeClassifier(max_depth=4, min_samples_leaf=50, random_state=42)
tree.fit(X_train, y_train)

# Calcolo predizioni
y_pred = tree.predict(X_test)

print("=== Decision Tree ===")
print(classification_report(y_test, y_pred, digits=3))



from sklearn.ensemble import RandomForestClassifier

# Istanzio e addestro Random Forest usando le stesse feature già trasformate
rf = RandomForestClassifier(
    n_estimators=100,
    max_depth=4,
    min_samples_leaf=50,
    random_state=42,
    n_jobs=-1
)
rf.fit(X_train, y_train)

# Predizioni
y_pred_rf = rf.predict(X_test)

print("=== Random Forest ===")
print(classification_report(y_test, y_pred_rf, digits=3))