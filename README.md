# CMSC6950 Final Project | Weather Time-Series (St. John's, NL) | Gideon Clottey (202289192)

This repository contains Python **scripts** to reproduce every figure and table in the CMSC6950 final project report for St. John’s, NL.  
The data come from **Environment and Climate Change Canada (ECCC)** daily station records for St. John’s A (Station 8403603).

All analysis is done in plain `.py` files so the whole workflow can be run from the command line.

---

## Structure

Top-level layout (what you see in VS Code):

- `Data/`  
  Put all raw **daily** ECCC CSV files for St. John’s here  
  (e.g. `stjohns_daily_2020.csv`, `stjohns_daily_2021.csv`, …).

- `outputs/`  
  Created by the scripts. Contains cleaned/aggregated CSVs, text summaries, and all final figures under `outputs/figs/`.

- `data_cleaning.py`  
  - Load ECCC daily CSVs from `Data/`.  
  - Parse `"Date/Time"` to a `date` column.  
  - Coerce temperature, precipitation, and wind columns to numeric.  
  - Create `tmax_c`, `tmin_c`, `tmean_c`, `precip_mm`, `gust_kmh`.  
  - Add helper columns `year`, `month`, `doy`.  
  - Compute `temp_range_c` and a binary `is_wet_day` flag.

- `metrics.py`  
  - Compute a daily **storm index** (0–1 scale) from precipitation and gusts.  
  - Compute **temperature anomalies** relative to a day-of-year baseline.  
  - Build monthly summaries (mean temp, total precip, wet-day counts, etc.).  
  - Build annual mean temperature series for trend analysis.

- `mk_test.py`  
  - Pure-Python **Mann–Kendall** trend test.  
  - Given a 1-D series, returns `S`, `varS`, `Z`, `p`, and a `trend` label (`"increasing"`, `"decreasing"`, or `"no trend"`).

- `eda.py`  
  - Exploratory data analysis.  
  - Descriptive statistics and correlation between temperature, precipitation, and wind.  
  - Simple trend analysis (including Mann–Kendall applied to annual means).

- `extremes.py`  
  - Select hot/cold extremes and very wet days.  
  - Fit GEV distributions to the tails.  
  - Compute return levels (e.g. 5-year events) for hot and cold extremes.

- `sensitivity.py`  
  - Sensitivity analysis: how the number of “extreme” events changes when the percentile threshold moves (e.g. 90th vs 95th).

- `plotting.py`  
  - All “core” figures: time-series plots, histograms, anomaly and storm-index plots, correlation heatmap.

- `plotting_extremes.py`  
  - Figures for the extremes and return-level analysis (GEV fits, return level plots).

- `style.py`  
  - Central Matplotlib style settings (fonts, colors, sizes) so all plots look consistent.

- `correlation.py`, `eda.py`, `extremes.py`, `sensitivity.py`  
  - Helper scripts for specific parts of the analysis. Can be run on their own if you only want subsets of the results.

- `main.py`  
  - **Main driver for the whole project.**  
  - Steps:
    1. Read all daily CSVs in `Data/`.  
    2. Clean and merge them using `data_cleaning.py`.  
    3. Compute metrics and summaries using `metrics.py`.  
    4. Run EDA, trend, extremes, and sensitivity analysis.  
    5. Call plotting functions to generate all figures into `outputs/figs/`.

- `tests/`  
  Unit tests for the analysis code (no plotting tests):
  - `test_cleaning.py` tests `clean_daily_dataframe` (dates, helper columns, temp range, wet-day flag).  
  - `test_metrics.py` tests `compute_storm_index` and `compute_baseline_anomaly`.  
  - `test_mk.py` tests `mann_kendall` on increasing / decreasing / flat / short series.

- `requirements.txt`  
  Python dependencies (NumPy, pandas, Matplotlib, SciPy, pytest, etc.).

---

## Setup and how to run

### 1. Create and activate a virtual environment

From the project root (`WEATHER_STJOHNSNL`):

```bash
python -m venv venv

# Windows PowerShell
.\venv\Scripts\Activate.ps1

# macOS / Linux
# source venv/bin/activate
```

###  2. Install dependencies:

```bash
pip install -r requirements.txt

```

###  3. Run the full pipeline

``` bash
python main.py --input_dir ./Data --output_dir ./outputs

```

### 4. Tests

``` bash
# Run all test files 

pytest -q

# Run specific test file

pytest tests/test_cleaning.py
pytest tests/test_metrics.py
pytest tests/test_mk.py

```