
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def compute_corr(clean: pd.DataFrame, cols=None):
    if cols is None:
        cols = [c for c in ["tmax_c","tmin_c","tmean_c","precip_mm","gust_kmh","temp_range_c"] if c in clean.columns]
    return clean[cols].corr(method="pearson")

def plot_corr_heatmap(corr: pd.DataFrame, out_path: str):
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6,5))
    im = ax.imshow(corr.values, aspect="auto", origin="upper")
    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.index)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right")
    ax.set_yticklabels(corr.index)
    for i in range(corr.shape[0]):
        for j in range(corr.shape[1]):
            ax.text(j, i, f"{corr.values[i,j]:.2f}", ha="center", va="center", fontsize=8)
    fig.colorbar(im, ax=ax, label="Pearson r")
    ax.set_title("Correlation Matrix Heatmap")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
