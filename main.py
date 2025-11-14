from pathlib import Path
import glob
import pandas as pd
import matplotlib.pyplot as plt
import argparse
from data_cleaning import load_raw_csvs, clean_daily_dataframe, save_clean
from eda import descriptive_stats, temperature_skewness, monthly_trend_tests, annual_trend_tests
from metrics import compute_baseline_anomaly, compute_storm_index, compute_monthly_summary, compute_annual_means
from style import apply as apply_style
from mannkendall import mann_kendall



def run_project_pipeline(input_dir: str, output_dir: str):
    out = Path(output_dir)
    (out / "figs").mkdir(parents=True, exist_ok=True)
    
    # ploting style
    apply_style()

    # loading clean data
    raw = load_raw_csvs(input_dir)
    clean = clean_daily_dataframe(raw)

    
    # metrics computation
    clean = compute_baseline_anomaly(clean, baseline_years=(2020, 2021))
    clean = compute_storm_index(clean)
    monthly = compute_monthly_summary(clean)
    annual = compute_annual_means(clean)

    # Save cleaned data and aggregates
    save_clean(clean, str(out / "stjohns_clean_daily.csv"))
    monthly.to_csv(out / "monthly_summary.csv", index=False)
    annual.to_csv(out / "annual_means.csv", index=False)

    # eda summaries
    desc = descriptive_stats(clean)
    desc.to_csv(out / "descriptive_stats.csv")
    skewness = temperature_skewness(clean)
    m_tests = monthly_trend_tests(monthly)
    a_tests = annual_trend_tests(annual)

     # Mann–Kendall on annual means 
    mk = mann_kendall(annual["annual_mean_temp"].values.tolist())

    return {"output_dir": str(out)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="St. John's NlWeather EDA pipeline (ECCC daily CSVs).")
    parser.add_argument("--input_dir", default="./data", help="Root Folder containing en_climate_daily_*_P1D.csv files")
    parser.add_argument("--output_dir", default="./outputs", help="Where to write cleaned data, tables, and plots")
    args = parser.parse_args()
    results = run_project_pipeline(args.input_dir, args.output_dir)
    print("results are  written under:", results["output_dir"])