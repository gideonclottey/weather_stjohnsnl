
import pandas as pd
import numpy as np

def extremes_sensitivity(clean: pd.DataFrame, p_lows=(1,2,5,10), p_highs=(90,95,98,99)):
    res = []
    if "tmin_c" in clean.columns:
        for pl in p_lows:
            thr = np.nanpercentile(clean["tmin_c"].dropna(), pl)
            count = int((clean["tmin_c"] <= thr).sum())
            res.append({"type":"cold","percentile":pl,"threshold":float(thr),"count":count})
    if "tmax_c" in clean.columns:
        for ph in p_highs:
            thr = np.nanpercentile(clean["tmax_c"].dropna(), ph)
            count = int((clean["tmax_c"] >= thr).sum())
            res.append({"type":"heat","percentile":ph,"threshold":float(thr),"count":count})
    return pd.DataFrame(res).sort_values(["type","percentile"]).reset_index(drop=True)
