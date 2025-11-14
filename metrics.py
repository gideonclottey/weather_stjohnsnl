
import numpy as np
import pandas as pd

def compute_baseline_anomaly(clean: pd.DataFrame, baseline_years=(2020, 2021)):
    """Add tmean anomaly relative to a day-of-year climatology over baseline_years."""
    df = clean.copy()
    if "tmean_c" not in df.columns:
        df["tmean_anom_c"] = np.nan
        return df
    base = df[(df["year"] >= baseline_years[0]) & (df["year"] <= baseline_years[1])].copy()
    clim = base.groupby("doy")["tmean_c"].mean()
    df["tmean_anom_c"] = df["tmean_c"] - df["doy"].map(clim)
    return df

def minmax(s: pd.Series):
    s = s.copy()
    if s.max() == s.min():
        return pd.Series(np.zeros(len(s)), index=s.index)
    return (s - s.min()) / (s.max() - s.min())

def compute_storm_index(clean: pd.DataFrame, w_gust=0.6, w_precip=0.4):
  
    df = clean.copy()
    gust = df.get("gust_kmh", pd.Series(np.zeros(len(df)), index=df.index)).fillna(0)
    precip = df.get("precip_mm", pd.Series(np.zeros(len(df)), index=df.index)).fillna(0)
    df["storm_index"] = w_gust*minmax(gust) + w_precip*minmax(precip)
    return df

def compute_monthly_summary(clean: pd.DataFrame):
    """Monthly aggregates, mean temp, total precip, wet days, max gust, mean temp range, precip intensity."""
    monthly = clean.groupby(["year","month"]).agg(
        mean_temp=("tmean_c","mean"),
        total_precip=("precip_mm","sum"),
        wet_days=("is_wet_day","sum"),
        gust_max=("gust_kmh","max"),
        temp_range_mean=("temp_range_c","mean"),
    ).reset_index()
    monthly["precip_intensity_mm_per_wetday"] = monthly["total_precip"] / monthly["wet_days"].replace({0:np.nan})
    return monthly

def compute_annual_means(clean: pd.DataFrame):
    ann = clean.groupby(clean["date"].dt.year)["tmean_c"].mean().reset_index()
    ann.columns = ["year","annual_mean_temp"]
    return ann
