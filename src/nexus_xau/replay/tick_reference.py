from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import pandas as pd

Side = Literal["BUY", "SELL"]
OutcomeKind = Literal["TARGET_FIRST", "STOP_FIRST", "AMBIGUOUS_SAME_TIMESTAMP", "NEITHER"]

REFERENCE_FILL_STATUS = "REFERENCE_NOT_BROKER_FILL"
SLIPPAGE_STATUS = "UNMODELED_NOT_ASSUMED_ZERO"

DATA_EXCLUDED_ARCHIVE_GAP = "DATA_EXCLUDED_ARCHIVE_GAP"
DATA_EXCLUDED_INSUFFICIENT_WARMUP = "DATA_EXCLUDED_INSUFFICIENT_WARMUP"
DATA_EXCLUDED_INCOMPLETE_HORIZON = "DATA_EXCLUDED_INCOMPLETE_HORIZON"
DATA_EXCLUDED_NO_POST_CONFIRMATION_QUOTE = "DATA_EXCLUDED_NO_POST_CONFIRMATION_QUOTE"


@dataclass(frozen=True, slots=True)
class ReferenceFill:
    timestamp: pd.Timestamp
    side: Side
    price: float
    bid: float
    ask: float
    raw_ordinal: int
    source_id: str
    fill_status: str = REFERENCE_FILL_STATUS
    slippage_status: str = SLIPPAGE_STATUS


@dataclass(frozen=True, slots=True)
class SuppliedLevelOutcome:
    outcome: OutcomeKind
    timestamp: pd.Timestamp | None
    price: float | None
    raw_ordinal: int | None
    source_id: str
    fill_status: str = REFERENCE_FILL_STATUS
    slippage_status: str = SLIPPAGE_STATUS


@dataclass(frozen=True, slots=True)
class GapInterval:
    start: pd.Timestamp
    end: pd.Timestamp
    label: str


def _aware(value: pd.Timestamp | str) -> pd.Timestamp:
    timestamp = pd.Timestamp(value)
    if timestamp.tz is None:
        raise ValueError("Timestamp must be timezone-aware")
    return timestamp


def validate_tick_frame(ticks: pd.DataFrame) -> None:
    """Validate a replay-ready Bid/Ask frame without mutating raw rows."""

    if not isinstance(ticks.index, pd.DatetimeIndex) or ticks.index.tz is None:
        raise ValueError("Replay ticks must use a timezone-aware DatetimeIndex")
    if not ticks.index.is_monotonic_increasing:
        raise ValueError("Replay ticks must be sorted oldest to newest")
    missing = {"bid", "ask"} - set(ticks.columns)
    if missing:
        raise ValueError(f"Replay ticks missing required columns: {sorted(missing)}")
    if ticks[["bid", "ask"]].isna().any().any():
        raise ValueError("Replay ticks contain missing Bid/Ask values")
    if (ticks["ask"] < ticks["bid"]).any():
        raise ValueError("Replay ticks contain Ask < Bid")


def spread(bid: float, ask: float) -> float:
    if ask < bid:
        raise ValueError("Ask must be greater than or equal to Bid")
    return float(ask - bid)


def first_reference_entry(
    ticks: pd.DataFrame,
    *,
    known_at: pd.Timestamp | str,
    side: Side,
    source_id: str,
) -> ReferenceFill:
    """Return the first executable-side quote strictly after confirmation knowledge time."""

    validate_tick_frame(ticks)
    cutoff = _aware(known_at)
    if side not in {"BUY", "SELL"}:
        raise ValueError(f"Unsupported side: {side}")

    positions = [i for i, timestamp in enumerate(ticks.index) if timestamp > cutoff]
    if not positions:
        raise LookupError(DATA_EXCLUDED_NO_POST_CONFIRMATION_QUOTE)

    pos = positions[0]
    row = ticks.iloc[pos]
    bid = float(row["bid"])
    ask = float(row["ask"])
    price = ask if side == "BUY" else bid
    return ReferenceFill(
        timestamp=ticks.index[pos],
        side=side,
        price=price,
        bid=bid,
        ask=ask,
        raw_ordinal=pos,
        source_id=source_id,
    )


def evaluate_supplied_levels(
    ticks: pd.DataFrame,
    *,
    start_after: pd.Timestamp | str,
    side: Side,
    stop_level: float,
    target_level: float,
    source_id: str,
) -> SuppliedLevelOutcome:
    """Evaluate externally supplied stop/target levels without choosing their geometry."""

    validate_tick_frame(ticks)
    cutoff = _aware(start_after)
    if side not in {"BUY", "SELL"}:
        raise ValueError(f"Unsupported side: {side}")
    if side == "BUY" and stop_level >= target_level:
        raise ValueError("BUY supplied stop level must be below supplied target level")
    if side == "SELL" and target_level >= stop_level:
        raise ValueError("SELL supplied target level must be below supplied stop level")

    working = ticks.assign(_raw_ordinal=range(len(ticks)))
    eligible = working.loc[working.index > cutoff]
    for timestamp, group in eligible.groupby(level=0, sort=False):
        if side == "BUY":
            target_mask = group["bid"] >= target_level
            stop_mask = group["bid"] <= stop_level
            executable_column = "bid"
        else:
            target_mask = group["ask"] <= target_level
            stop_mask = group["ask"] >= stop_level
            executable_column = "ask"

        target_hit = bool(target_mask.any())
        stop_hit = bool(stop_mask.any())
        if target_hit and stop_hit:
            return SuppliedLevelOutcome(
                outcome="AMBIGUOUS_SAME_TIMESTAMP",
                timestamp=timestamp,
                price=None,
                raw_ordinal=None,
                source_id=source_id,
            )

        if target_hit:
            first_match = group.loc[target_mask].iloc[0]
            return SuppliedLevelOutcome(
                outcome="TARGET_FIRST",
                timestamp=timestamp,
                price=float(first_match[executable_column]),
                raw_ordinal=int(first_match["_raw_ordinal"]),
                source_id=source_id,
            )

        if stop_hit:
            first_match = group.loc[stop_mask].iloc[0]
            return SuppliedLevelOutcome(
                outcome="STOP_FIRST",
                timestamp=timestamp,
                price=float(first_match[executable_column]),
                raw_ordinal=int(first_match["_raw_ordinal"]),
                source_id=source_id,
            )

    return SuppliedLevelOutcome(
        outcome="NEITHER",
        timestamp=None,
        price=None,
        raw_ordinal=None,
        source_id=source_id,
    )


def window_exclusion_reason(
    *,
    required_start: pd.Timestamp | str,
    required_end: pd.Timestamp | str,
    available_start: pd.Timestamp | str,
    available_end: pd.Timestamp | str,
    gaps: tuple[GapInterval, ...] = (),
) -> str | None:
    """Classify replay-window availability without interpolation."""

    start = _aware(required_start)
    end = _aware(required_end)
    have_start = _aware(available_start)
    have_end = _aware(available_end)
    if end < start:
        raise ValueError("required_end must be greater than or equal to required_start")

    if start < have_start:
        return DATA_EXCLUDED_INSUFFICIENT_WARMUP
    if end > have_end:
        return DATA_EXCLUDED_INCOMPLETE_HORIZON

    for gap in gaps:
        gap_start = _aware(gap.start)
        gap_end = _aware(gap.end)
        if gap_end < gap_start:
            raise ValueError(f"Gap {gap.label!r} has end before start")
        if start < gap_end and end > gap_start:
            return DATA_EXCLUDED_ARCHIVE_GAP

    return None
