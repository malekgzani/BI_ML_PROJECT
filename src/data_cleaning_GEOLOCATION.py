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

FILE_NAME = "olist_geolocation_dataset.csv"

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
# 4. Nettoyage de la colonne textuelle sélectionnée
# ============================================================

colonnes_texte = [
    "geolocation_state"
]

for col in colonnes_texte:
    df[col] = df[col].str.strip()
    df[col] = df[col].replace("", pd.NA)
    df[col] = df[col].str.replace(r"[^\w]", "", regex=True)


# ============================================================
# 5. Suppression de la colonne non conservée
# ============================================================

columns_to_remove = [
    "geolocation_city"
]

df = df.drop(columns=columns_to_remove)

print("\nColonnes restantes :")
print(df.columns.tolist())


# ============================================================
# 6. Suppression des lignes/colonnes vides et des doublons
# ============================================================

df = df.dropna(axis=0, how="all")
df = df.dropna(axis=1, how="all")

duplicates = df.duplicated().sum()
df = df.drop_duplicates()


# ============================================================
# 7. Détection des valeurs atypiques (outliers)
# ============================================================

colonnes_numeriques = [
    "geolocation_lat",
    "geolocation_lng",
    "geolocation_zip_code_prefix"
]

for col in colonnes_numeriques:

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
# 8. Traitement des codes postaux
# ============================================================

# Remplacer les codes postaux égaux à 0 par des valeurs manquantes
df["geolocation_zip_code_prefix"] = (
    df["geolocation_zip_code_prefix"].replace(0, np.nan)
)

# Convertir le code postal en chaîne de caractères
df["geolocation_zip_code_prefix"] = (
    df["geolocation_zip_code_prefix"].astype("str")
)

print("\nTypes après traitement des codes postaux :")
print(df.dtypes)


# ============================================================
# 9. Bilan final du nettoyage
# ============================================================

print("\nNettoyage terminé.")

print("Doublons supprimés :", duplicates)

print("\nValeurs manquantes par colonne :")
print(df.isna().sum())

print("\nDimensions finales :", df.shape)


# ============================================================
# 10. Export du fichier nettoyé
# ============================================================

df.to_csv(
    output_path,
    index=False,
    encoding="utf-8-sig",
    na_rep="NULL"
)

print("\nCopie enregistrée :", output_path)
print("Le fichier original reste intact.")