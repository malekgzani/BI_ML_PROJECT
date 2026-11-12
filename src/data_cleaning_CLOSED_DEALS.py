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

FILE_NAME = "olist_closed_deals_dataset.csv"

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
# 3. Suppression des colonnes non conservées
# ============================================================

columns_to_remove = [
    "declared_product_catalog_size",
    "declared_monthly_revenue",
    "has_company",
    "has_gtin",
    "average_stock",
    "mql_id",
    "sdr_id",
    "sr_id",
    "lead_type",
    "won_date"
]

df = df.drop(columns=columns_to_remove)

print("\nColonnes restantes après suppression :")
print(df.columns.tolist())


# ============================================================
# 4. Nettoyage des noms de colonnes
# ============================================================

df.columns = df.columns.str.replace(r"[^\w]", "", regex=True)

print("\nColonnes après nettoyage des noms :")
print(df.columns.tolist())


# ============================================================
# 5. Nettoyage des colonnes textuelles sélectionnées
# ============================================================

colonnes_texte = [
    "seller_id",
    "business_segment",
    "lead_behaviour_profile",
    "business_type",
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
# 7. Nettoyage et vérification de la date
# ============================================================

"""df["won_date"] = df["won_date"].str.strip()
df["won_date"] = df["won_date"].replace("", pd.NA)
df["won_date"] = pd.to_datetime(df["won_date"], errors="coerce")

print("\nDate minimale :", df["won_date"].min())
print("Date maximale :", df["won_date"].max())"""


# ============================================================
#  Remplacer les valeurs NULL par UNKNOWN 
# ============================================================

categorical_columns = [
    'business_segment',
    'lead_behaviour_profile',
    'business_type'
]

for col in categorical_columns:
    df[col] = df[col].fillna('Unknown')

# ============================================================
# 8. Bilan final du nettoyage
# ============================================================

print("\nTypes finaux :")
print(df.dtypes)

print("\nNettoyage terminé.")
print("Doublons supprimés :", duplicates)
print("\nValeurs manquantes par colonne :")
print(df.isna().sum())
print("\nDimensions finales :", df.shape)


# ============================================================
# 9. Export du fichier nettoyé
# ============================================================

df.to_csv(
    output_path,
    index=False,
    encoding="utf-8-sig",
    na_rep="NULL",
)

print("\nCopie enregistrée :", output_path)
print("Le fichier original reste intact.")
