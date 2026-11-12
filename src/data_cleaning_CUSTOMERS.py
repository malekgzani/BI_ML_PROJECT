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

FILE_NAME = "olist_customers_dataset.csv"

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
# Vérification des deux identifiants avant nettoyage
# ============================================================

colonnes_id = [
    'customer  _id@                     ',
    ' "customer_unique_id"              '
]

for col in colonnes_id:
    print(f"\nColonne : {repr(col)}")

    if col not in df.columns:
        print("ERREUR : colonne introuvable.")
        continue

    print("Valeurs uniques :", df[col].is_unique)
    print("Valeurs nulles :", df[col].isna().sum())
    print("Nombre de doublons :", df[col].duplicated().sum())

    if df[col].is_unique and df[col].notna().all():
        print("Résultat : candidate à une clé primaire (PK).")
    else:
        print("Résultat : ne peut pas être une PK seule.")


# ============================================================
# 3. Nettoyage des noms de colonnes
# ============================================================

df.columns = df.columns.str.replace(r"[^\w]", "", regex=True)

print("\nColonnes après nettoyage des noms :")
print(df.columns.tolist())


# ============================================================
# 4. Suppression des colonnes non conservées
# ============================================================

columns_to_remove = [
    "customer_unique_id",
    "customer_city",
]

df = df.drop(columns=columns_to_remove)

print("\nColonnes restantes :")
print(df.columns.tolist())


# ============================================================
# 5. Nettoyage des colonnes sélectionnées
# ============================================================

colonnes_texte = [
    "customer_id",
    "customer_zip_code_prefix",
    "customer_state",
]

for col in colonnes_texte:
    df[col] = df[col].str.strip()
    df[col] = df[col].replace("", pd.NA)
    df[col] = df[col].str.replace(r"[^\w]", "", regex=True)




# ============================================================
# 6. Suppression des lignes/colonnes vides et des doublons
# ============================================================

df = df.dropna(axis=0, how="all")
df = df.dropna(axis=1, how="all")

duplicates = df.duplicated().sum()
df = df.drop_duplicates()


# ============================================================
# 7. Bilan final du nettoyage
# ============================================================

print("\nNettoyage terminé.")
print("Doublons supprimés :", duplicates)
print("\nValeurs manquantes par colonne :")
print(df.isna().sum())
print("\nDimensions finales :", df.shape)
print("\nTypes finaux :")
print(df.dtypes)


# ============================================================
# 8. Export du fichier nettoyé
# ============================================================

df.to_csv(
    output_path,
    index=False,
    encoding="utf-8-sig",
    na_rep="NULL",
)

print("\nCopie enregistrée :", output_path)
print("Le fichier original reste intact.")
