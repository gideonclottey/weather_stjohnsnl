import pytest
import numpy as np

from mk_test import mann_kendall


def test_mann_kendall_increasing_trend():
    """
    A strictly increasing series should be classified as an increasing trend
    with a small p-value (significant at 5% level)
    """
    x = np.arange(10, dtype=float)  # 0, 1, ..., 9
    res = mann_kendall(x)

    assert res["trend"] == "increasing"
    assert res["p"] < 0.05


def test_mann_kendall_decreasing_trend():
    """
    A strictly decreasing series should be classified as a decreasing trend
    with a small p-value (significant at 5% level)
    """
    x = np.arange(10, dtype=float)[::-1]  # 9, 8, ..., 0
    res = mann_kendall(x)

    assert res["trend"] == "decreasing"
    assert res["p"] < 0.05


def test_mann_kendall_constant_series_no_trend():
    """
    A perfectly flat series should have no trend and a non-significant p-value.
    """
    x = np.ones(10, dtype=float)
    res = mann_kendall(x)

    assert res["trend"] == "no trend"
    assert res["p"] >= 0.05


def test_mann_kendall_short_series_returns_no_trend():
    """
    For a very short series (n < 8), the implementation is expected
    to fall back to 'no trend'
    """
    x = np.arange(5, dtype=float)
    res = mann_kendall(x)

    assert res["trend"] == "no trend"
