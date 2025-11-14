
import pandas as pd
from scipy.stats import skew, kendalltau, theilslopes

def descriptive_stats(clean: pd.DataFrame) -> pd.DataFrame:
    cols = [c for c in ["tmax_c","tmin_c","tmean_c","temp_range_c","precip_mm","snow_cm","gust_kmh","storm_index"] if c in clean.columns]
    return clean[cols].describe().T

def temperature_skewness(clean: pd.DataFrame) -> float:
    return float(skew(clean["tmean_c"].dropna()))

def monthly_trend_tests(monthly: pd.DataFrame):
    m = monthly.copy()
    m["t"] = (m["year"] - m["year"].min())*12 + (m["month"]-1)
    tau, pval = kendalltau(m["t"], m["mean_temp"])
    slope, intercept, _, _ = theilslopes(m["mean_temp"], m["t"], 0.95)
    return {"kendall_tau": float(tau), "kendall_p": float(pval), "theilsen_slope_c_per_month": float(slope)}

def annual_trend_tests(annual: pd.DataFrame):
    a = annual.copy()
    a["t"] = a["year"] - a["year"].min()
    tau, pval = kendalltau(a["t"], a["annual_mean_temp"])
    slope, intercept, _, _ = theilslopes(a["annual_mean_temp"], a["t"], 0.95)
    return {"kendall_tau": float(tau), "kendall_p": float(pval), "theilsen_slope_c_per_year": float(slope)}
