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

FILE_NAME = "olist_products_dataset.csv"

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

print("\nInformations générales :")
df.info()

print("\nAperçu des données :")
print(df.head())


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
    "product_id",
    "product_category_name"
]

for col in colonnes:
    df[col] = df[col].str.strip()
    df[col] = df[col].replace("", pd.NA)
    df[col] = df[col].str.replace(r"[^\w]", "", regex=True)


# ============================================================
# 5. SUPPRESSION DES COLONNES INUTILES
# ============================================================

columns_to_remove = [
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm",
    "product_name_lenght"
]

df = df.drop(columns=columns_to_remove)

print("\nColonnes restantes :")
print(df.columns.tolist())

print("\nAperçu des données :")
print(df.head())


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
# 8. CONVERSION DE product_photos_qty
# ============================================================

df["product_photos_qty"] = df["product_photos_qty"].replace(
    r"^\s*$",
    np.nan,
    regex=True
)

df["product_photos_qty"] = pd.to_numeric(
    df["product_photos_qty"],
    errors="coerce"
).astype("Int64")


# ============================================================
# 9. DÉTECTION DES VALEURS ABERRANTES
# ============================================================

colonnes = [
    "product_photos_qty"
]

for col in colonnes:
    serie = pd.to_numeric(df[col], errors="coerce").dropna()

    Q1 = serie.quantile(0.25)
    Q3 = serie.quantile(0.75)
    IQR = Q3 - Q1

    limite_inf = Q1 - 1.5 * IQR
    limite_sup = Q3 + 1.5 * IQR

    outliers = serie[
        (serie < limite_inf) |
        (serie > limite_sup)
    ]

    print(f"\nColonne : {col}")

    print("Valeurs négatives :")
    print(df[df[col] < 0])

    print("Valeur minimale :", df[col].min())
    print("Valeur maximale :", df[col].max())
    print("Limite inférieure :", limite_inf)
    print("Limite supérieure :", limite_sup)
    print("Nombre d'outliers :", len(outliers))
    print(
        "Pourcentage :",
        round(len(outliers) / len(serie) * 100, 2),
        "%"
    )


# ============================================================
# Remplacer NULL par UNKNOWN 
# ============================================================
"""categorical_columns = [
    "product_category_name",
]

for col in categorical_columns:
        df[col] = df[col].fillna('Unknown')"""
    
df["product_category_name"] = df["product_category_name"].fillna('Unknown')
df["product_photos_qty"] = df["product_photos_qty"].fillna(0).astype(int)
df["product_description_lenght"] = (df["product_description_lenght"]
    .replace(r'^\s*$', 0, regex=True)
    .fillna(0)
    .astype(int)
)
# ============================================================
# 10. TYPES DE DONNÉES
# ============================================================

print("\nTypes de données :")
print(df.dtypes)


# ============================================================
# 11. BILAN DU NETTOYAGE
# ============================================================

print("\n" + "=" * 70)
print("BILAN DU NETTOYAGE")
print("=" * 70)

print("Nettoyage terminé.")

print("\nDoublons supprimés :", duplicates)

print("\nValeurs manquantes par colonne :")
print(df.isna().sum())

print("\nDimensions finales :", df.shape)


# ============================================================
# 12. EXPORTATION DU FICHIER NETTOYÉ
# ============================================================

df.to_csv(
    output_path,
    index=False,
    encoding="utf-8-sig",
    na_rep="NULL"
)

print("\nCopie enregistrée :", output_path)
print("Le fichier original reste intact.")
