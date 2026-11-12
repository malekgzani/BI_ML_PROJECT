"""
print(closed_deals.head())
print(closed_deals.shape)
print(closed_deals.columns)
print(closed_deals.info()) #permet aussi de voir nbre de valeurs manquantes
#print(closed_deals.describe())
#print(closed_deals.tail())
# Statistiques descriptives
display(reviews.describe(include="all"))
# Nombre de valeurs manquantes par colonne
print(reviews.isnull().sum())

# Séparer les colonnes numériques et catégorielles
numeric_cols = customers.select_dtypes(include=np.number).columns
categorical_cols = customers.select_dtypes(
    include=["object", "category", "string"]
).columns

# Supprimer les colonnes entièrement vides
df = customers.dropna(axis=1, how="all")
print("Data cleaning terminé !")
"""

import pandas as pd
import numpy as np
import seaborn as sns
import os
from pathlib import Path

#Dossiers du projet
RAW_DIR = Path(
    r"C:\Users\malek\OneDrive\Desktop\ESPRIT\3ème IA\PROJET BI\data\raw"
)
PROCESSED_DIR = RAW_DIR.parent / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# Fichier à nettoyer : un seul à la fois
FILE_NAME = "test.csv"

input_path = RAW_DIR / FILE_NAME
output_path = PROCESSED_DIR / f"{input_path.stem}_cleaned.csv"

# Vérifier l'existence du fichier
if not input_path.exists():
    raise FileNotFoundError(f"Fichier introuvable : {input_path}")

"""
#Afficher les lignes autour de X ligne
print("Fichier analysé :", FILE_NAME)
with open(input_path, "r", encoding="utf-8-sig") as f:
    for numero, ligne in enumerate(f, start=1):
        if 68 <= numero <= 75:
            print(f"Ligne {numero} : {ligne.rstrip()!r}")
"""


# Lire le fichier original
df = pd.read_csv(input_path, encoding="utf-8-sig")
print("Dimensions initiales :", df.shape)
print("colonnes initiales :")
print(df.columns.tolist())


#SUPPRESSIION espace sur les cotés + ""
#df.columns = df.columns.str.strip()
#df.columns = df.columns.str.strip().str.strip('"')

#SUPPRESSIION espace au milieu 
#df.columns = df.columns.str.replace(" ", "", regex=False)


# 3. Nettoyer les noms des colonnes
#SUPPRESSIION espace au milieu + caracteres speciaux - noms des colonnes
df.columns= df.columns.str.replace(r"[^\w]", "", regex=True)
print("**************************************SUPPRESSIION espace + caracteres speciaux NOM COLONNE**************************************")
print(df.columns.tolist())


"""
#Supprimer les espaces inutiles et uniformiser les noms. des colonnes 
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(" ", "_")
)
"""

# 3. Nettoyer les colonnes choisies + ajouter NULL (contenu)
colonnes = [
    "product_category_name",
    "product_category_name_english"
]
for col in colonnes:
    #df[col] = df[col].str.replace(" ", "", regex=False)
    df[col] = df[col].str.strip()
    df[col] = df[col].replace("", pd.NA)
    df[col] = df[col].str.replace(r"[^\w]", "", regex=True)

"""
# 5. Nettoyer les espaces dans les colonnes TEXTUELLES
for col in df.select_dtypes(include=["object", "string"]).columns:
    df[col] = df[col].apply(
        lambda x: x.strip() if isinstance(x, str) else x
    )
"""

# 4. Supprimer les lignes et colonnes entièrement vides
df = df.dropna(axis=0, how="all")
df = df.dropna(axis=1, how="all")


"""
# pourcentage de valeur NULL
df.isna().mean().mul(100).round(2)
"""

# 6. Supprimer les doublons exacts
duplicates = df.duplicated().sum()
df = df.drop_duplicates()

# 7. Afficher le bilan du nettoyage
print("******************************************************************************************************************")
print("Nettoyage terminé.")
print("\nDoublons supprimés :", duplicates)
print("\nValeurs manquantes par colonne :")
print(df.isna().sum())
print("\nDimensions finales :", df.shape)
print("Copie enregistrée :", output_path)
print("Le fichier original reste intact.")

# Enregistrer la copie nettoyée
df.to_csv(output_path, index=False, na_rep="NULL",encoding="utf-8-sig")





