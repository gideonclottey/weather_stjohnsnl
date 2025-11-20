
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.stats import genextreme

def plot_heat_extremes_hist(heat_series, params, out_path: str):
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(6,4))
    data = heat_series.dropna().values
    plt.hist(data, bins=20, density=True, alpha=0.6)
    if params is not None:
        c, loc, scale = params
        xs = np.linspace(min(data), max(data), 200)
        ys = genextreme.pdf(xs, c, loc=loc, scale=scale)
        plt.plot(xs, ys)
    plt.title("Extreme Heat (Tmax ≥ 95th percentile) — GEV fit")
    plt.xlabel("Tmax (°C)"); plt.ylabel("Density")
    plt.tight_layout(); plt.savefig(out_path, dpi=150); plt.close()

def plot_cold_extremes_hist(cold_series, params, out_path: str):
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(6,4))
    data = cold_series.dropna().values
    plt.hist(data, bins=20, density=True, alpha=0.6)
    if params is not None:
        c, loc, scale = params
        xs = np.linspace(min(data), max(data), 200)
        # Fit was on negated Tmin; map PDF accordingly: f_Tmin(t) = f_neg(-t)
        neg_xs = -xs
        ys = genextreme.pdf(neg_xs, c, loc=loc, scale=scale)
        plt.plot(xs, ys)
    plt.title("Extreme Cold (Tmin ≤ 5th percentile) — GEV fit")
    plt.xlabel("Tmin (°C)"); plt.ylabel("Density")
    plt.tight_layout(); plt.savefig(out_path, dpi=150); plt.close()
