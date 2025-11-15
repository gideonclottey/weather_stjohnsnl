
import numpy as np
import pandas as pd
from scipy.stats import genextreme

def select_extremes(clean: pd.DataFrame, p_low=5.0, p_high=95.0):
    
    if "tmin_c" in clean.columns:
        low_thr = np.nanpercentile(clean["tmin_c"].dropna(), p_low)
        cold = clean.loc[clean["tmin_c"] <= low_thr, "tmin_c"].dropna()
    else:
        cold = pd.Series([], dtype=float)
    if "tmax_c" in clean.columns:
        high_thr = np.nanpercentile(clean["tmax_c"].dropna(), p_high)
        heat = clean.loc[clean["tmax_c"] >= high_thr, "tmax_c"].dropna()
    else:
        heat = pd.Series([], dtype=float)
    return cold, heat

def fit_gev_heat(heat_series: pd.Series):
    
    if len(heat_series) < 10:
        return None
    # scipy genextreme uses shape 'c'; for maxima, fit directly
    c, loc, scale = genextreme.fit(heat_series.dropna())
    return (c, loc, scale)

def fit_gev_cold(cold_series: pd.Series):
    
    if len(cold_series) < 10:
        return None
    neg = -cold_series.dropna()
    c, loc, scale = genextreme.fit(neg)
    # for reporting as temperature threshold, return parameters for the negated domain plus flag
    return (c, loc, scale)

def return_level_gev(c, loc, scale, T):
   
    # Quantile at probability p = 1-1/T
    from scipy.stats import genextreme
    p = 1.0 - 1.0/float(T)
    return genextreme.ppf(p, c, loc=loc, scale=scale)

def pdf_points(c, loc, scale, x):
    from scipy.stats import genextreme
    return genextreme.pdf(x, c, loc=loc, scale=scale)
