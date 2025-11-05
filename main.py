from pathlib import Path
import glob
import pandas as pd
import matplotlib.pyplot as plt
from data_cleaning import load_raw_csvs, clean_daily_dataframe, save_clean

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
print(df.shape)


# ploting daily mean temperature if present
if "Mean Temp (°C)" in df.columns:
    ax = df["Mean Temp (°C)"].plot(figsize=(10,4), linewidth=0.6, label="Daily mean (°C)")
    df["Mean Temp (°C)"].rolling(30, min_periods=15).mean().plot(ax=ax, linewidth=1.2, label="30-day rolling")
    ax.set_title("Daily Mean Temperature (°C)")
    ax.set_xlabel("Date"); ax.set_ylabel("Temperature (°C)")
    ax.grid(True, linewidth=0.3); ax.legend()
    plt.tight_layout()
    plt.savefig("first_plot_daily_mean_temp.png")
    plt.close()
    print("Saved plot: first_plot_daily_mean_temp.png")
else:
    print("Column 'Mean Temp (°C)' not found.")
