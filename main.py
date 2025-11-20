
import argparse
from pathlib import Path
import pandas as pd

from data_cleaning import load_raw_csvs, clean_daily_dataframe, save_clean
from metrics import compute_baseline_anomaly, compute_storm_index, compute_monthly_summary, compute_annual_means
from style import apply as apply_style
from plotting import (
    plot_daily_tmean, plot_monthly_mean_with_trend, plot_hist_tmean,
    plot_monthly_precip_intensity, plot_storm_index
)
from eda import descriptive_stats, temperature_skewness, monthly_trend_tests, annual_trend_tests
from mk_test import mann_kendall
from correlation import compute_corr, plot_corr_heatmap
from extremes import select_extremes, fit_gev_heat, fit_gev_cold, return_level_gev
from sensitivity import extremes_sensitivity
from plotting_extremes import plot_heat_extremes_hist, plot_cold_extremes_hist

def run_project_pipeline(input_dir: str, output_dir: str):
    out = Path(output_dir)
    (out / "figs").mkdir(parents=True, exist_ok=True)

    # Plot style
    apply_style()

    # Load & clean
    raw = load_raw_csvs(input_dir)
    clean = clean_daily_dataframe(raw)

    # metrics
    clean = compute_baseline_anomaly(clean, baseline_years=(2020, 2021))
    clean = compute_storm_index(clean)
    monthly = compute_monthly_summary(clean)
    annual = compute_annual_means(clean)

    # Save cleaned data & aggregates
    save_clean(clean, str(out / "stjohns_clean_daily.csv"))
    monthly.to_csv(out / "monthly_summary.csv", index=False)
    annual.to_csv(out / "annual_means.csv", index=False)

    # EDA summaries
    desc = descriptive_stats(clean)
    desc.to_csv(out / "descriptive_stats.csv")
    skewness = temperature_skewness(clean)
    m_tests = monthly_trend_tests(monthly)
    a_tests = annual_trend_tests(annual)

    # Mann–Kendall on annual means
    mk = mann_kendall(annual["annual_mean_temp"].values.tolist())

    with open(out / "eda_summary.txt", "w") as f:
        f.write(f"Daily mean temperature skewness: {skewness:.6f}\n")
        f.write(f"Monthly trend — Kendall tau: {m_tests['kendall_tau']:.6f}, p={m_tests['kendall_p']:.6f}, Theil–Sen slope (°C/month): {m_tests['theilsen_slope_c_per_month']:.6f}\n")
        f.write(f"Annual trend — Kendall tau: {a_tests['kendall_tau']:.6f}, p={a_tests['kendall_p']:.6f}, Theil–Sen slope (°C/year): {a_tests['theilsen_slope_c_per_year']:.6f}\n")
        f.write(f"Mann–Kendall on annual means: S={mk['S']}, Z={mk['Z']:.3f}, p={mk['p']:.4f}, trend={mk['trend']}\n")

    # correlation
    corr = compute_corr(clean)
    corr.to_csv(out / "correlation_matrix.csv")
    plot_corr_heatmap(corr, str(out / "figs" / "corr_heatmap.png"))

    # extremes analysis
    cold, heat = select_extremes(clean, p_low=5.0, p_high=95.0)
    heat_params = fit_gev_heat(heat)
    cold_params = fit_gev_cold(cold)

    plot_heat_extremes_hist(heat, heat_params, str(out / "figs" / "heat_extremes_gev.png"))
    plot_cold_extremes_hist(cold, cold_params, str(out / "figs" / "cold_extremes_gev.png"))

    # Example 5-year return levels 
    with open(out / "extremes_summary.txt", "w") as f:
        if heat_params:
            rl5 = return_level_gev(*heat_params, T=5*365.25)
            f.write(f"Heat extremes (GEV) ~5-year return level Tmax: {rl5:.2f} °C\n")
        else:
            f.write("Heat extremes: insufficient data for GEV fit.\n")
        if cold_params:
            # fit was on negated Tmin; return level for neg domain -> map back with minus sign
            rl5_neg = return_level_gev(*cold_params, T=5*365.25)
            f.write(f"Cold extremes (GEV) ~5-year return level Tmin: {-rl5_neg:.2f} °C\n")
        else:
            f.write("Cold extremes: insufficient data for GEV fit.\n")

    # Plots 
    plot_daily_tmean(clean, str(out / "figs" / "daily_mean_temp.png"))
    plot_monthly_mean_with_trend(monthly, str(out / "figs" / "monthly_mean_theilsen.png"))
    plot_hist_tmean(clean, str(out / "figs" / "hist_tmean.png"))
    plot_monthly_precip_intensity(monthly, str(out / "figs" / "monthly_precip_intensity.png"))
    plot_storm_index(clean, str(out / "figs" / "storm_index.png"))


    # threshold sensitivity table
    sens = extremes_sensitivity(clean)
    sens.to_csv(out / "extremes_sensitivity.csv", index=False)

    return {"output_dir": str(out)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="St. John's NlWeather EDA pipeline (ECCC daily CSVs).")
    parser.add_argument("--input_dir", default="./data", help="Root Folder containing en_climate_daily_*_P1D.csv files")
    parser.add_argument("--output_dir", default="./outputs", help="Where to write cleaned data, tables, and plots")
    args = parser.parse_args()
    results = run_project_pipeline(args.input_dir, args.output_dir)
    print("results are  written under:", results["output_dir"])