from __future__ import annotations

import pandas as pd

from nexus_xau.replay.tick_reference import validate_tick_frame

BAR_REPRESENTATION = "ARCHIVE_BID_M1_V0.1"

_REQUIRED_PROVENANCE = {
    "raw_ordinal",
    "source_year",
    "source_month",
    "source_sha256",
    "source_local_path",
    "source_validator_version",
}


def _utc(value: pd.Timestamp | str) -> pd.Timestamp:
    timestamp = pd.Timestamp(value)
    if timestamp.tz is None:
        raise ValueError("Timestamp must be timezone-aware")
    return timestamp.tz_convert("UTC")
def _require_minute_aligned(timestamp: pd.Timestamp, *, name: str) -> None:
    if timestamp != timestamp.floor("min"):
        raise ValueError(f"{name} must be aligned to an exact UTC minute boundary")


def _validate_provenance(ticks: pd.DataFrame) -> None:
    missing = _REQUIRED_PROVENANCE - set(ticks.columns)
    if missing:
        raise ValueError(f"Archive ticks missing provenance columns: {sorted(missing)}")


def _single_value(group: pd.DataFrame, column: str) -> object:
    values = group[column].drop_duplicates()
    if len(values) != 1:
        raise ValueError(f"M1 bar contains mixed provenance for {column}")
    return values.iloc[0]


def build_archive_bid_m1(
    ticks: pd.DataFrame,
    *,
    requested_start: pd.Timestamp | str,
    requested_end: pd.Timestamp | str,
) -> pd.DataFrame:
    """Build deterministic M1 OHLC bars from validated archive Bid ticks."""
    start = _utc(requested_start)
    end = _utc(requested_end)
    _require_minute_aligned(start, name="requested_start")
    _require_minute_aligned(end, name="requested_end")
    if end <= start:
        raise ValueError("requested_end must be strictly greater than requested_start")

    validate_tick_frame(ticks)
    _validate_provenance(ticks)

    if len(ticks) and (ticks.index[0] < start or ticks.index[-1] >= end):
        raise ValueError("Tick frame contains rows outside requested half-open window")

    columns = [
        "open",
        "high",
        "low",
        "close",
        "archive_tick_count",
        "source_year",
        "source_month",
        "source_sha256",
        "source_local_path",
        "source_validator_version",
        "first_raw_ordinal",
        "last_raw_ordinal",
        "bar_representation",
    ]
    if ticks.empty:
        return pd.DataFrame(
            columns=columns,
            index=pd.DatetimeIndex([], tz="UTC", name="timestamp"),
        )

    rows: list[dict[str, object]] = []
    labels: list[pd.Timestamp] = []

    grouped = ticks.groupby(
        pd.Grouper(freq="1min", origin="start_day", label="left", closed="left"),
        sort=True,
    )

    for timestamp, group in grouped:
        if group.empty:
            continue

        labels.append(pd.Timestamp(timestamp))
        rows.append(
            {
                "open": float(group.iloc[0]["bid"]),
                "high": float(group["bid"].max()),
                "low": float(group["bid"].min()),
                "close": float(group.iloc[-1]["bid"]),
                "archive_tick_count": len(group),
                "source_year": int(_single_value(group, "source_year")),
                "source_month": int(_single_value(group, "source_month")),
                "source_sha256": str(_single_value(group, "source_sha256")),
                "source_local_path": str(_single_value(group, "source_local_path")),
                "source_validator_version": str(
                    _single_value(group, "source_validator_version")
                ),
                "first_raw_ordinal": int(group.iloc[0]["raw_ordinal"]),
                "last_raw_ordinal": int(group.iloc[-1]["raw_ordinal"]),
                "bar_representation": BAR_REPRESENTATION,
            }
        )

    result = pd.DataFrame(rows, index=pd.DatetimeIndex(labels, name="timestamp"))
    return result[columns]
