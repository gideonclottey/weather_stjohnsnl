
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def plot_daily_tmean(clean: pd.DataFrame, out_path: str):
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(10,4))
    plt.plot(clean["date"], clean["tmean_c"])
    plt.title("Daily Mean Temperature (°C) — Station series")
    plt.xlabel("Date"); plt.ylabel("Mean Temp (°C)")
    plt.tight_layout(); plt.savefig(out_path, dpi=150); plt.close()

def plot_monthly_mean_with_trend(monthly: pd.DataFrame, out_path: str):
    from scipy.stats import theilslopes
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    m = monthly.copy()
    m["t"] = (m["year"] - m["year"].min())*12 + (m["month"]-1)
    slope, intercept, _, _ = theilslopes(m["mean_temp"], m["t"], 0.95)
    trend = intercept + slope*m["t"]
    x = pd.to_datetime(m[["year","month"]].assign(day=1))
    plt.figure(figsize=(10,4))
    plt.plot(x, m["mean_temp"])
    plt.plot(x, trend)
    plt.title("Monthly Mean Temperature with Theil–Sen Trend")
    plt.xlabel("Month"); plt.ylabel("Mean Temp (°C)")
    plt.tight_layout(); plt.savefig(out_path, dpi=150); plt.close()

def plot_hist_tmean(clean: pd.DataFrame, out_path: str):
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(6,4))
    plt.hist(clean["tmean_c"].dropna(), bins=40)
    plt.title("Distribution of Daily Mean Temperature (°C)")
    plt.xlabel("Mean Temp (°C)"); plt.ylabel("Count")
    plt.tight_layout(); plt.savefig(out_path, dpi=150); plt.close()

def plot_monthly_precip_intensity(monthly: pd.DataFrame, out_path: str):
    x = pd.to_datetime(monthly[["year","month"]].assign(day=1))
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(10,4))
    plt.plot(x, monthly["precip_intensity_mm_per_wetday"])
    plt.title("Monthly Precipitation Intensity (mm per wet day)")
    plt.xlabel("Month"); plt.ylabel("mm per wet day")
    plt.tight_layout(); plt.savefig(out_path, dpi=150); plt.close()

def plot_storm_index(clean: pd.DataFrame, out_path: str, window: int = 14):
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(10,4))
    plt.plot(clean["date"], clean["storm_index"].rolling(window, min_periods=1).mean())
    plt.title(f"Storm Index — {window}-day Rolling Mean")
    plt.xlabel("Date"); plt.ylabel("Index (0–1)")
    plt.tight_layout(); plt.savefig(out_path, dpi=150); plt.close()
