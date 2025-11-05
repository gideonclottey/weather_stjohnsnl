
from pathlib import Path
import glob
import pandas as pd
import numpy as np

ECCC_KEEP_MAP = {
    "Max Temp (°C)": "tmax_c",
    "Min Temp (°C)": "tmin_c",
    "Mean Temp (°C)": "tmean_c",
    "Total Precip (mm)": "precip_mm",
    "Total Snow (cm)": "snow_cm",
    "Spd of Max Gust (km/h)": "gust_kmh",
}

def load_raw_csvs(input_dir: str):
    #loading all csv files and combining into a single dataframe
    csvs = sorted(glob.glob(str(Path(input_dir) / "en_climate_daily_*_P1D.csv")))
    if not csvs:
        raise FileNotFoundError(f"No ECCC daily CSVs found in {input_dir}")
    frames = []
    for p in csvs:
        df = pd.read_csv(p)
        df["source_file"] = Path(p).name
        frames.append(df)
    raw = pd.concat(frames, ignore_index=True)
    return raw

def clean_daily_dataframe(raw: pd.DataFrame):
    # perform cleaning operations on raw dataframe
    df = raw.copy()
    # Parse date
    if "Date/Time" not in df.columns:
        raise KeyError("Expected 'Date/Time' column in ECCC CSVs")
    df["date"] = pd.to_datetime(df["Date/Time"], errors="coerce")
    df = df.sort_values("date")
    # rename core numeric columns
    keep_cols = ["date"] + [c for c in ECCC_KEEP_MAP.keys() if c in df.columns]
    df = df[keep_cols].rename(columns=ECCC_KEEP_MAP)
    # coerce to numeric
    for c in ["tmax_c","tmin_c","tmean_c","precip_mm","snow_cm","gust_kmh"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    # derive range and wet day flag
    if "tmax_c" in df.columns and "tmin_c" in df.columns:
        df["temp_range_c"] = df["tmax_c"] - df["tmin_c"]
    else:
        df["temp_range_c"] = np.nan
    if "precip_mm" in df.columns:
        df["is_wet_day"] = (df["precip_mm"] > 0).astype(int)
    else:
        df["is_wet_day"] = 0
    #droping rows that are entirely NaN on key measures
    key_cols = [c for c in ["tmax_c","tmin_c","tmean_c","precip_mm","snow_cm","gust_kmh"] if c in df.columns]
    if key_cols:
        df = df.dropna(how="all", subset=key_cols)
    #  year/month helpers
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["doy"] = df["date"].dt.dayofyear
    return df

def save_clean(df: pd.DataFrame, out_csv: str) -> None:
    Path(out_csv).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_csv, index=False)