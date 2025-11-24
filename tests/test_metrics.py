import pytest
import pandas as pd
import numpy as np

from metrics import compute_storm_index, compute_baseline_anomaly


@pytest.mark.parametrize(
    "precip, gust",
    [
        ([0.0, 5.0, 10.0], [10.0, 50.0, 100.0]),
        ([0.0, 0.0, 20.0], [0.0, 30.0, 60.0]),
    ],
)
def test_storm_index_bounds(precip, gust):
  
    df = pd.DataFrame({"precip_mm": precip, "gust_kmh": gust})
    out = compute_storm_index(df)

    assert "storm_index" in out.columns
    assert (out["storm_index"] >= 0).all()
    assert (out["storm_index"] <= 1).all()


def test_storm_index_monotone_for_stronger_events():
  
    df = pd.DataFrame(
        {
            "precip_mm": [0.0, 5.0, 10.0],
            "gust_kmh": [10.0, 50.0, 100.0],
        }
    )
    out = compute_storm_index(df)

    s = out["storm_index"].values
    # index should not go down as intensity clearly increases
    assert s[1] >= s[0]
    assert s[2] >= s[1]


def test_anomaly_baseline_single_year_zero_anomaly():
    
    dates = pd.date_range("2020-01-01", periods=10, freq="D")
    df = pd.DataFrame({"date": dates, "tmean_c": np.linspace(0.0, 9.0, 10)})

    df["year"] = df["date"].dt.year
    df["doy"] = df["date"].dt.dayofyear

    out = compute_baseline_anomaly(df, baseline_years=(2020, 2020))

    assert "tmean_anom_c" in out.columns
    assert len(out) == len(df)
    # with only 2020 as baseline, anomalies should be exactly zero
    assert np.allclose(out["tmean_anom_c"], 0.0)


def test_anomaly_baseline_keeps_original_columns():
    
    dates = pd.date_range("2020-01-01", periods=5, freq="D")
    df = pd.DataFrame({"date": dates, "tmean_c": np.linspace(0.0, 4.0, 5)})
    df["year"] = df["date"].dt.year
    df["doy"] = df["date"].dt.dayofyear

    out = compute_baseline_anomaly(df, baseline_years=(2020, 2020))

    # original columns are still there
    for col in ["date", "tmean_c", "year", "doy"]:
        assert col in out.columns

    # and the anomaly column has no missing values
    assert out["tmean_anom_c"].notna().all()
