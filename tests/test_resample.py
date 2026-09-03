import pandas as pd

from nexus_xau.data.resample import resample_ohlc


def test_resample_five_m1_bars_to_one_m5_bar() -> None:
    index = pd.date_range("2026-01-01T00:00:00Z", periods=5, freq="1min")
    m1 = pd.DataFrame(
        {
            "open": [10, 11, 12, 13, 14],
            "high": [12, 13, 14, 15, 16],
            "low": [9, 10, 11, 12, 13],
            "close": [11, 12, 13, 14, 15],
        },
        index=index,
    )

    m5 = resample_ohlc(m1, "M5")

    assert len(m5) == 1
    assert m5.iloc[0]["open"] == 10
    assert m5.iloc[0]["high"] == 16
    assert m5.iloc[0]["low"] == 9
    assert m5.iloc[0]["close"] == 15


def test_resample_supports_m15_and_m30_for_mtf_research() -> None:
    index = pd.date_range("2026-01-01T00:00:00Z", periods=60, freq="1min")
    m1 = pd.DataFrame(
        {
            "open": range(60),
            "high": [value + 2 for value in range(60)],
            "low": [value - 1 for value in range(60)],
            "close": [value + 1 for value in range(60)],
        },
        index=index,
    )

    m15 = resample_ohlc(m1, "M15")
    m30 = resample_ohlc(m1, "M30")

    assert len(m15) == 4
    assert len(m30) == 2
    assert m15.index[1] == pd.Timestamp("2026-01-01T00:15:00Z")
    assert m30.index[1] == pd.Timestamp("2026-01-01T00:30:00Z")
