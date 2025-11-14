from pathlib import Path
import glob
import pandas as pd
import matplotlib.pyplot as plt
import argparse
from data_cleaning import load_raw_csvs, clean_daily_dataframe, save_clean
from eda import descriptive_stats, temperature_skewness, monthly_trend_tests, annual_trend_tests
from style import apply as apply_style


def run_project_pipeline(input_dir: str, output_dir: str):
    out = Path(output_dir)
    (out / "figs").mkdir(parents=True, exist_ok=True)
    
    # ploting style
    apply_style()

    # loading clean data
    raw = load_raw_csvs(input_dir)
    clean = clean_daily_dataframe(raw)

    



    return {"output_dir": str(out)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="St. John's NlWeather EDA pipeline (ECCC daily CSVs).")
    parser.add_argument("--input_dir", default="./data", help="Root Folder containing en_climate_daily_*_P1D.csv files")
    parser.add_argument("--output_dir", default="./outputs", help="Where to write cleaned data, tables, and plots")
    args = parser.parse_args()
    results = run_project_pipeline(args.input_dir, args.output_dir)
    print("results are  written under:", results["output_dir"])