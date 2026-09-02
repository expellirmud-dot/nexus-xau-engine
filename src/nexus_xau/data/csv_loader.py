from __future__ import annotations

from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

_REQUIRED = ("timestamp", "open", "high", "low", "close")


def load_ohlc_csv(
    path: str | Path,
    *,
    source_timezone: str | None = None,
) -> pd.DataFrame:
    """Load OHLC CSV into a normalized UTC-indexed dataframe.

    Required columns: timestamp, open, high, low, close.
    If timestamps are naive, source_timezone is mandatory. We refuse to guess.
    """
    frame = pd.read_csv(path)
    missing = [column for column in _REQUIRED if column not in frame.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    ts = pd.to_datetime(frame["timestamp"], errors="raise")
    if ts.dt.tz is None:
        if source_timezone is None:
            raise ValueError(
                "CSV timestamps are timezone-naive; pass source_timezone explicitly"
            )
        ts = ts.dt.tz_localize(ZoneInfo(source_timezone))

    frame = frame.copy()
    frame["timestamp"] = ts.dt.tz_convert("UTC")
    frame = frame.sort_values("timestamp")

    if frame["timestamp"].duplicated().any():
        raise ValueError("Duplicate timestamps found in source data")

    numeric_columns = [c for c in ("open", "high", "low", "close", "volume") if c in frame]
    frame[numeric_columns] = frame[numeric_columns].apply(pd.to_numeric, errors="raise")

    invalid = (
        (frame["high"] < frame[["open", "close", "low"]].max(axis=1))
        | (frame["low"] > frame[["open", "close", "high"]].min(axis=1))
    )
    if invalid.any():
        raise ValueError(f"Invalid OHLC rows found: {int(invalid.sum())}")

    return frame.set_index("timestamp")
