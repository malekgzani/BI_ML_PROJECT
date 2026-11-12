import pandas as pd
import numpy as np
import seaborn as sns
import os
from pathlib import Path


# ============================================================
# 1. Configuration des chemins et du fichier
# ============================================================

RAW_DIR = Path(
    r"C:\Users\malek\OneDrive\Desktop\ESPRIT\3ème IA\PROJET BI\data\raw"
)
PROCESSED_DIR = RAW_DIR.parent / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

FILE_NAME = "product_category_name_translation.csv"

input_path = RAW_DIR / FILE_NAME
output_path = PROCESSED_DIR / f"{input_path.stem}_cleaned.csv"


# ============================================================
# 2. Vérification et lecture du fichier
# ============================================================

if not input_path.exists():
    raise FileNotFoundError(f"Fichier introuvable : {input_path}")

df = pd.read_csv(input_path, encoding="utf-8-sig")

print("Dimensions initiales :", df.shape)
print("\nColonnes initiales :")
print(df.columns.tolist())
print("\nTypes initiaux :")
print(df.dtypes)


# ============================================================
# 3. Nettoyage des noms de colonnes
# ============================================================

df.columns = df.columns.str.replace(r"[^\w]", "", regex=True)

print("\nColonnes après nettoyage des noms :")
print(df.columns.tolist())


# ============================================================
# 4. Nettoyage des colonnes textuelles sélectionnées
# ============================================================

colonnes_texte = [
    "product_category_name",
    "product_category_name_english",
]

for col in colonnes_texte:
    df[col] = df[col].str.strip()
    df[col] = df[col].replace("", pd.NA)
    df[col] = df[col].str.replace(r"[^\w]", "", regex=True)


# ============================================================
# 5. Suppression des doublons exacts
# ============================================================

duplicates = df.duplicated().sum()
df = df.drop_duplicates()


# ============================================================
# 6. Bilan final du nettoyage
# ============================================================

print("\nNettoyage terminé.")
print("Doublons supprimés :", duplicates)
print("\nValeurs manquantes par colonne :")
print(df.isna().sum())
print("\nDimensions finales :", df.shape)


# ============================================================
# 7. Export du fichier nettoyé
# ============================================================

df.to_csv(
    output_path,
    index=False,
    encoding="utf-8-sig",
    na_rep="NULL",
)

print("\nCopie enregistrée :", output_path)
print("Le fichier original reste intact.")
