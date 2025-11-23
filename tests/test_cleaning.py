import pytest
import pandas as pd
import numpy as np

from data_cleaning import clean_daily_dataframe


def _make_raw_daily_df():
    """Small helper to create a minimal raw daily dataframe like ECCC output."""
    return pd.DataFrame(
        {
            "Date/Time": ["2020-01-01", "2020-01-02"],
            "Max Temp (°C)": [1.0, 2.0],
            "Min Temp (°C)": [-1.0, 0.0],
            "Mean Temp (°C)": [0.0, 1.0],
            "Total Precip (mm)": [0.0, 5.0],
            "Spd of Max Gust (km/h)": [40.0, 60.0],
        }
    )


def test_clean_parses_date_and_adds_helpers():
    """
    clean_daily_dataframe should parse 'Date/Time' into a datetime 'date' column
    and keep the same number of rows.
    """
    df_raw = _make_raw_daily_df()
    out = clean_daily_dataframe(df_raw)

    # row count is preserved
    assert len(out) == len(df_raw)

    # date column exists and is datetime
    assert "date" in out.columns
    assert pd.api.types.is_datetime64_any_dtype(out["date"])

    # helper columns year / month / doy should exist
    for col in ["year", "month", "doy"]:
        assert col in out.columns
        assert out[col].notna().all()


def test_clean_has_expected_numeric_columns():
    """
    Core numeric columns should exist and be numeric after cleaning.
    """
    df_raw = _make_raw_daily_df()
    out = clean_daily_dataframe(df_raw)

    for col in ["tmax_c", "tmin_c", "tmean_c", "precip_mm", "gust_kmh"]:
        assert col in out.columns
        assert pd.api.types.is_numeric_dtype(out[col])


def test_clean_computes_temp_range_and_is_wet_day_correctly():
    """
    temp_range_c should equal tmax_c - tmin_c (non-negative),
    and is_wet_day should be 1 exactly when precip_mm > 0.
    """
    df_raw = _make_raw_daily_df()
    out = clean_daily_dataframe(df_raw)

    assert "temp_range_c" in out.columns
    expected_range = out["tmax_c"] - out["tmin_c"]
    assert np.allclose(out["temp_range_c"], expected_range)
    assert (out["temp_range_c"] >= 0).all()

    
    assert "is_wet_day" in out.columns
    expected_is_wet = (out["precip_mm"] > 0.0).astype(int)
    assert (out["is_wet_day"] == expected_is_wet).all()
