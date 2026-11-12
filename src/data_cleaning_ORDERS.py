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

FILE_NAME = "olist_orders_dataset.csv"

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
    "customer_id",
    "order_id",
    "order_status",
]

for col in colonnes_texte:
    df[col] = df[col].str.strip()
    df[col] = df[col].replace("", pd.NA)
    df[col] = df[col].str.replace(r"[^\w]", "", regex=True)


# ============================================================
# 5. Nettoyage et conversion des dates
# ============================================================

colonnes_dates = [
    "order_approved_at",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]

for col in colonnes_dates:
    df[col] = df[col].str.strip()
    df[col] = df[col].replace("", pd.NA)
    df[col] = pd.to_datetime(df[col], errors="coerce")


# ============================================================
# 6. Suppression des colonnes non conservées
# ============================================================

columns_to_remove = [
    "order_purchase_timestamp",
    "order_delivered_carrier_date",
    "order_status",
]

df = df.drop(columns=columns_to_remove)

print("\nColonnes restantes :")
print(df.columns.tolist())


# ============================================================
# 7. Suppression des lignes/colonnes vides et des doublons
# ============================================================

df = df.dropna(axis=0, how="all")
df = df.dropna(axis=1, how="all")

duplicates = df.duplicated().sum()
df = df.drop_duplicates()


# ============================================================
# 8. Vérification des plages de dates
# ============================================================

print("\nDate minimale d'approbation :", df["order_approved_at"].min())
print("Date maximale d'approbation :", df["order_approved_at"].max())

print("\nDate minimale de livraison client :",
      df["order_delivered_customer_date"].min())
print("Date maximale de livraison client :",
      df["order_delivered_customer_date"].max())

print("\nDate minimale de livraison estimée :",
      df["order_estimated_delivery_date"].min())
print("Date maximale de livraison estimée :",
      df["order_estimated_delivery_date"].max())


# ============================================================
# 9. Filtrage des commandes conservées
# ============================================================
df = df.dropna(subset=["order_approved_at"]).copy()
df = df.dropna(subset=["order_delivered_customer_date"]).copy()


# ============================================================
# 10. Bilan final du nettoyage
# ============================================================

print("\nTypes finaux :")
print(df.dtypes)

print("\nNettoyage terminé.")
print("Doublons supprimés :", duplicates)
print("\nValeurs manquantes par colonne :")
print(df.isna().sum())
print("\nDimensions finales :", df.shape)


# ============================================================
# 11. Export du fichier nettoyé
# ============================================================

df.to_csv(
    output_path,
    index=False,
    encoding="utf-8-sig",
    na_rep="NULL",
)

print("\nCopie enregistrée :", output_path)
print("Le fichier original reste intact.")
