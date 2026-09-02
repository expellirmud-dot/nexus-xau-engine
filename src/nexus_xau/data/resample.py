from __future__ import annotations

import pandas as pd

_RULES = {
    "M5": "5min",
    "H1": "1h",
    "H4": "4h",
    "D1": "1D",
}


def resample_ohlc(
    m1: pd.DataFrame,
    timeframe: str,
    *,
    origin: str = "start_day",
    offset: str | pd.Timedelta | None = None,
) -> pd.DataFrame:
    """Build a higher timeframe from M1 bars.

    Boundary alignment is configurable because project evidence has unresolved
    server/Thai-time semantics for some H4/D1 rules. Do not silently hard-code
    a broker-session offset here.
    """
    if timeframe not in _RULES:
        raise ValueError(f"Unsupported timeframe: {timeframe}")
    if not isinstance(m1.index, pd.DatetimeIndex) or m1.index.tz is None:
        raise ValueError("Input index must be a timezone-aware DatetimeIndex")

    agg: dict[str, str] = {
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
    }
    if "volume" in m1.columns:
        agg["volume"] = "sum"

    result = m1.resample(
        _RULES[timeframe],
        origin=origin,
        offset=offset,
        label="left",
        closed="left",
    ).agg(agg)

    return result.dropna(subset=["open", "high", "low", "close"])
