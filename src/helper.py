import pandas as pd

def load_data(data_path) -> pd.DataFrame:
    return pd.read_csv(data_path)