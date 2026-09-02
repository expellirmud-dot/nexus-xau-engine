import pandas as pd

from nexus_xau.data.mt5_validate import compare_ohlc_frames


def _frame(values: list[float]) -> pd.DataFrame:
    index = pd.date_range("2026-08-24T00:00:00Z", periods=len(values), freq="5min")
    return pd.DataFrame(
        {
            "open": values,
            "high": [v + 1 for v in values],
            "low": [v - 1 for v in values],
            "close": [v + 0.5 for v in values],
        },
        index=index,
    )


def test_compare_ohlc_frames_exact_match() -> None:
    local = _frame([100.0, 101.0, 102.0])
    result = compare_ohlc_frames(local, local.copy(), timeframe="M5")

    assert result.common_timestamps == 3
    assert result.only_local_timestamps == 0
    assert result.only_mt5_timestamps == 0
    assert result.ohlc_mismatch_rows == 0
    assert result.max_abs_ohlc_diff == 0.0


def test_compare_ohlc_frames_reports_price_and_timestamp_mismatch() -> None:
    local = _frame([100.0, 101.0, 102.0])
    reference = local.copy()
    reference.loc[reference.index[1], "high"] += 0.01
    reference = reference.iloc[1:]

    result = compare_ohlc_frames(local, reference, timeframe="M5")

    assert result.common_timestamps == 2
    assert result.only_local_timestamps == 1
    assert result.only_mt5_timestamps == 0
    assert result.ohlc_mismatch_rows == 1
    assert result.max_abs_ohlc_diff > 0
