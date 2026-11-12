import pandas as pd

closed_deals = pd.read_csv(r"C:\Users\malek\OneDrive\Desktop\ESPRIT\3ème IA\PROJET BI\data\raw\olist_closed_deals_dataset.csv")


"""
print(closed_deals.head())
print(closed_deals.shape)
print(closed_deals.columns)
print(closed_deals.info()) #permet aussi de voir nbre de valeurs manquantes
#print(closed_deals.describe())
#print(closed_deals.tail())
"""


print(closed_deals.info())