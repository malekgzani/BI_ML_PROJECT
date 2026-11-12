import pandas as pd
import numpy as np
import seaborn as sns
import os
from pathlib import Path


# ============================================================
# 1. CONFIGURATION DES DOSSIERS ET DU FICHIER
# ============================================================

RAW_DIR = Path(
    r"C:\Users\malek\OneDrive\Desktop\ESPRIT\3ème IA\PROJET BI\data\raw"
)

PROCESSED_DIR = RAW_DIR.parent / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

FILE_NAME = "olist_order_reviews_dataset.csv"

input_path = RAW_DIR / FILE_NAME
output_path = PROCESSED_DIR / f"{input_path.stem}_cleaned.csv"


# ============================================================
# 2. VÉRIFICATION ET LECTURE DU FICHIER
# ============================================================

if not input_path.exists():
    raise FileNotFoundError(f"Fichier introuvable : {input_path}")

df = pd.read_csv(input_path, encoding="utf-8-sig")

print("Dimensions initiales :", df.shape)

print("\nColonnes initiales :")
print(df.columns.tolist())

print("\nTypes de données initiaux :")
print(df.dtypes)


# ============================================================
# 3. NETTOYAGE DES NOMS DES COLONNES
# ============================================================

df.columns = df.columns.str.replace(r"[^\w]", "", regex=True)

print("\n" + "=" * 70)
print("NETTOYAGE DES NOMS DES COLONNES")
print("=" * 70)

print(df.columns.tolist())


# ============================================================
# 4. NETTOYAGE DES COLONNES TEXTUELLES
# ============================================================

colonnes = [
    "review_id",
    "order_id"
]

for col in colonnes:
    df[col] = df[col].str.strip()
    df[col] = df[col].replace("", pd.NA)
    df[col] = df[col].str.replace(r"[^\w]", "", regex=True)


# ============================================================
# 5. SUPPRESSION DES COLONNES INUTILES
# ============================================================

columns_to_remove = [
    "review_comment_title",
    "review_creation_date",
    "review_answer_timestamp",
    "review_comment_message",
    "review_id"
]

df = df.drop(columns=columns_to_remove)

print("\nColonnes restantes :")
print(df.columns.tolist())


# ============================================================
# 6. SUPPRESSION DES LIGNES ET COLONNES ENTIÈREMENT VIDES
# ============================================================

df = df.dropna(axis=0, how="all")
df = df.dropna(axis=1, how="all")


# ============================================================
# 7. SUPPRESSION DES DOUBLONS EXACTS
# ============================================================

duplicates = df.duplicated().sum()
df = df.drop_duplicates()


# ============================================================
# 8. VÉRIFICATION DES NOTES
# ============================================================

col = "review_score"

invalides = df[
    ~df[col].between(1, 5)
]

print("\nNombre de notes invalides :", len(invalides))


# ============================================================
# 9. CRÉATION DE LA VARIABLE negative_review
# ============================================================

df["negative_review"] = (
    df["review_score"] <= 3
).astype(int)

print("\nRépartition des avis négatifs :")
print(df["negative_review"].value_counts())


# ============================================================
# 10. BILAN DU NETTOYAGE
# ============================================================

print("\n" + "=" * 70)
print("BILAN DU NETTOYAGE")
print("=" * 70)

print("Nettoyage terminé.")

print("\nDoublons supprimés :", duplicates)

print("\nValeurs manquantes par colonne :")
print(df.isna().sum())
print("\nTypes de données finaux :")
print(df.dtypes)
print("\nDimensions finales :", df.shape)


# ============================================================
# 11. EXPORTATION DU FICHIER NETTOYÉ
# ============================================================

df.to_csv(
    output_path,
    index=False,
    encoding="utf-8-sig",
    na_rep="NULL"
)

print("\nCopie enregistrée :", output_path)
print("Le fichier original reste intact.")
