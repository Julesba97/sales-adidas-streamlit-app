import pandas as pd
from pathlib import Path


def prepare_data(data_path:Path) -> pd.DataFrame:
    df = pd.read_excel(data_path)
    #Supprimer les lignes 1 à 3
    df = df.drop(df.index[0:3])

    #Supprimer la premiere colonne
    df = df.iloc[:, 1:]
    #Remettre la première ligne en tant qu'en-tête
    new_header = df.iloc[0]
    df = df[1:]
    df.columns = new_header
    #Réinitialiser l'index si nécessaire
    df = df.reset_index(drop=True).copy()

    def get_gender(x):
        if(x[0]=='M'):
            return 'Male'
        else:
            return 'Female'
        
    df[df.columns[7:-1]] = df[df.columns[7:-1]].astype(float)
    df["Invoice Date"] = pd.to_datetime(df["Invoice Date"])

    df['Gender'] = df['Product'].apply(lambda x : get_gender(x))
    df["Year"] = df["Invoice Date"].dt.year
    df["Month Name"] = df["Invoice Date"].dt.month_name()
    df["Month"] = df["Invoice Date"].dt.month
    df["Quarter"] = df["Invoice Date"].dt.quarter
    
    return df

data_path = Path("./data/raw/Adidas US Sales Datasets.xlsx")
df = prepare_data(data_path=data_path)

df.to_csv("./data/processed/sales_adidas.csv", index=False)