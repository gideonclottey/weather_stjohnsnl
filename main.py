from pathlib import Path
import glob
import pandas as pd
import matplotlib.pyplot as plt

# loading data with data path 
data_pattern = r"data\*.csv"   # or "data/*.csv" on any OS

def load_data(file_pattern: str, index_col="Date/Time"):
    all_files = glob.glob(file_pattern)
    if not all_files:
        raise FileNotFoundError(f"No files matched: {file_pattern}")

    df_list = []
    for file in all_files:
        df = pd.read_csv(
            file,
            encoding="utf-8-sig",
            parse_dates=[index_col],  # specify the date column explicitly
            index_col=index_col
        )
        df_list.append(df)

    combined_df = pd.concat(df_list).sort_index()
    return combined_df

print("Loading data...")
df = load_data(data_pattern)
print("Data loaded successfully.")
print(df.head(10)) 
print(df.info())
print(df.describe())