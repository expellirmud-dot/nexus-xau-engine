from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

import pandas as pd


class FirstHit(StrEnum):
    TARGET_FIRST = "TARGET_FIRST"
    STOP_FIRST = "STOP_FIRST"
    AMBIGUOUS_SAME_BAR = "AMBIGUOUS_SAME_BAR"
    NEITHER = "NEITHER"


@dataclass(frozen=True, slots=True)
class OutcomeSpec:
    side: str
    reference_price: float
    known_at: pd.Timestamp
    horizon_end: pd.Timestamp
    point_size: float
    target_points: float | None = None
    stop_points: float | None = None


@dataclass(frozen=True, slots=True)
class EventOutcome:
    side: str
    reference_price: float
    known_at: pd.Timestamp
    horizon_end: pd.Timestamp
    bars_observed: int
    mfe_points: float
    mae_points: float
    end_return_points: float
    target_hit_at: pd.Timestamp | None
    stop_hit_at: pd.Timestamp | None
    first_hit: FirstHit


def _validate_bars(bars: pd.DataFrame) -> None:
    if not isinstance(bars.index, pd.DatetimeIndex) or bars.index.tz is None:
        raise ValueError("bars must use a timezone-aware DatetimeIndex")
    if not bars.index.is_monotonic_increasing:
        raise ValueError("bars must be sorted oldest to newest")
    required = {"high", "low", "close"}
    missing = required.difference(bars.columns)
    if missing:
        raise ValueError(f"bars missing columns: {sorted(missing)}")


def _directional_points(*, side: str, price: float, reference: float, point_size: float) -> float:
    if side == "BUY":
        return (price - reference) / point_size
    if side == "SELL":
        return (reference - price) / point_size
    raise ValueError(f"unsupported side: {side}")


def measure_outcome(bars: pd.DataFrame, spec: OutcomeSpec) -> EventOutcome:
    """Measure forward price behavior using only bars visible after ``known_at``.

    ``reference_price`` may come from a previously completed/confirmed object,
    while ``known_at`` records when that reference became knowable without
    look-ahead. Bars with timestamps before ``known_at`` are never used.

    If target and stop are both touched inside the same OHLC bar, the order is
    unknowable without lower-level/tick data and is reported as AMBIGUOUS.
    """

    _validate_bars(bars)
    if spec.point_size <= 0:
        raise ValueError("point_size must be > 0")
    if spec.horizon_end < spec.known_at:
        raise ValueError("horizon_end must be >= known_at")
    if spec.target_points is not None and spec.target_points <= 0:
        raise ValueError("target_points must be > 0 when supplied")
    if spec.stop_points is not None and spec.stop_points <= 0:
        raise ValueError("stop_points must be > 0 when supplied")

    side = spec.side.upper()
    if side not in {"BUY", "SELL"}:
        raise ValueError(f"unsupported side: {spec.side}")

    window = bars.loc[(bars.index >= spec.known_at) & (bars.index <= spec.horizon_end)]
    if window.empty:
        raise ValueError("no forward bars in requested outcome window")

    if side == "BUY":
        favorable_prices = window["high"]
        adverse_prices = window["low"]
    else:
        favorable_prices = window["low"]
        adverse_prices = window["high"]

    mfe_points = max(
        _directional_points(
            side=side,
            price=float(favorable_prices.max() if side == "BUY" else favorable_prices.min()),
            reference=spec.reference_price,
            point_size=spec.point_size,
        ),
        0.0,
    )
    mae_points = max(
        -_directional_points(
            side=side,
            price=float(adverse_prices.min() if side == "BUY" else adverse_prices.max()),
            reference=spec.reference_price,
            point_size=spec.point_size,
        ),
        0.0,
    )
    end_return_points = _directional_points(
        side=side,
        price=float(window.iloc[-1]["close"]),
        reference=spec.reference_price,
        point_size=spec.point_size,
    )

    target_hit_at: pd.Timestamp | None = None
    stop_hit_at: pd.Timestamp | None = None
    first_hit = FirstHit.NEITHER

    for timestamp, row in window.iterrows():
        if side == "BUY":
            target_touched = (
                spec.target_points is not None
                and float(row["high"]) >= spec.reference_price + spec.target_points * spec.point_size
            )
            stop_touched = (
                spec.stop_points is not None
                and float(row["low"]) <= spec.reference_price - spec.stop_points * spec.point_size
            )
        else:
            target_touched = (
                spec.target_points is not None
                and float(row["low"]) <= spec.reference_price - spec.target_points * spec.point_size
            )
            stop_touched = (
                spec.stop_points is not None
                and float(row["high"]) >= spec.reference_price + spec.stop_points * spec.point_size
            )

        if target_touched and target_hit_at is None:
            target_hit_at = timestamp
        if stop_touched and stop_hit_at is None:
            stop_hit_at = timestamp

        if target_touched and stop_touched:
            first_hit = FirstHit.AMBIGUOUS_SAME_BAR
            break
        if target_touched:
            first_hit = FirstHit.TARGET_FIRST
            break
        if stop_touched:
            first_hit = FirstHit.STOP_FIRST
            break

    return EventOutcome(
        side=side,
        reference_price=spec.reference_price,
        known_at=spec.known_at,
        horizon_end=spec.horizon_end,
        bars_observed=len(window),
        mfe_points=float(mfe_points),
        mae_points=float(mae_points),
        end_return_points=float(end_return_points),
        target_hit_at=target_hit_at,
        stop_hit_at=stop_hit_at,
        first_hit=first_hit,
    )
