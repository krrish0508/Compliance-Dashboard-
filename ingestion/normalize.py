import pandas as pd

def normalize_data(file):
    df = pd.read_csv(file)
    return df