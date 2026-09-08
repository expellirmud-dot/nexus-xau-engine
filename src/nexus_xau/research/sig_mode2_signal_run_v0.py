from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

import pandas as pd

from nexus_xau.data.price_grid import PriceGrid

SCHEMA_VERSION = "SIG_MODE2_SIGNAL_RUN_V0.1"


class SignalSide(StrEnum):
    BUY = "BUY"
    SELL = "SELL"


class SignalTimeframe(StrEnum):
    H1 = "H1"
    H4 = "H4"


class LocationLabel(StrEnum):
    VALID_SUPPORT = "VALID_SUPPORT"
    VALID_RESISTANCE = "VALID_RESISTANCE"


class SignalRunResult(StrEnum):
    TARGET_FIRST = "TARGET_FIRST"
    POINT_CHECK_FIRST = "POINT_CHECK_FIRST"
    AMBIGUOUS_SAME_BAR = "AMBIGUOUS_SAME_BAR"
    HORIZON_EXHAUSTED = "HORIZON_EXHAUSTED"


def _timestamp(value: Any, *, field: str) -> pd.Timestamp:
    try:
        ts = pd.Timestamp(value)
    except Exception as exc:  # pragma: no cover - pandas supplies specific parser errors
        raise ValueError(f"{field} must be a valid timestamp") from exc
    if ts.tz is None:
        raise ValueError(f"{field} must be timezone-aware")
    return ts


def _required_text(value: Any, *, field: str) -> str:
    result = str(value).strip()
    if not result:
        raise ValueError(f"{field} is required")
    return result


@dataclass(frozen=True, slots=True)
class SigMode2SignalRunEvent:
    """Pre-outcome-labeled source-compatible Mode-2 SIG instance.

    This is an input contract for signal/run research only. It deliberately does
    not contain a broker entry price, spread, slippage, P&L, or an autonomous PAT
    detector result.
    """

    signal_id: str
    side: SignalSide
    signal_tf: SignalTimeframe
    pa_kind_or_source_label: str
    pa_confirmed_at: pd.Timestamp
    location_label: LocationLabel
    location_label_provenance: str
    post_sig_closed_at: pd.Timestamp
    point_check_price: str
    point_check_price_provenance: str
    run_anchor_price: str
    run_target_price: str
    horizon_end: pd.Timestamp
    parent_context_tf: str
    context_tags: tuple[str, ...]
    source_or_label_provenance: str
    label_known_before_outcome: bool

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> SigMode2SignalRunEvent:
        tags_raw = raw.get("context_tags", ())
        if isinstance(tags_raw, str):
            raise TypeError("context_tags must be a sequence of strings, not one string")
        if not isinstance(tags_raw, Sequence):
            raise TypeError("context_tags must be a sequence")

        try:
            side = SignalSide(str(raw["side"]).upper())
        except (KeyError, ValueError) as exc:
            raise ValueError("side must be BUY or SELL") from exc
        try:
            signal_tf = SignalTimeframe(str(raw["signal_tf"]).upper())
        except (KeyError, ValueError) as exc:
            raise ValueError("signal_tf must be H1 or H4") from exc
        try:
            location_label = LocationLabel(str(raw["location_label"]).upper())
        except (KeyError, ValueError) as exc:
            raise ValueError(
                "location_label must be VALID_SUPPORT or VALID_RESISTANCE"
            ) from exc

        label_flag = raw.get("label_known_before_outcome")
        if label_flag is not True:
            raise ValueError("label_known_before_outcome must be boolean true")

        event = cls(
            signal_id=_required_text(raw.get("signal_id", ""), field="signal_id"),
            side=side,
            signal_tf=signal_tf,
            pa_kind_or_source_label=_required_text(
                raw.get("pa_kind_or_source_label", ""),
                field="pa_kind_or_source_label",
            ),
            pa_confirmed_at=_timestamp(raw.get("pa_confirmed_at"), field="pa_confirmed_at"),
            location_label=location_label,
            location_label_provenance=_required_text(
                raw.get("location_label_provenance", ""),
                field="location_label_provenance",
            ),
            post_sig_closed_at=_timestamp(
                raw.get("post_sig_closed_at"), field="post_sig_closed_at"
            ),
            point_check_price=_required_text(
                raw.get("point_check_price", ""), field="point_check_price"
            ),
            point_check_price_provenance=_required_text(
                raw.get("point_check_price_provenance", ""),
                field="point_check_price_provenance",
            ),
            run_anchor_price=_required_text(
                raw.get("run_anchor_price", ""), field="run_anchor_price"
            ),
            run_target_price=_required_text(
                raw.get("run_target_price", ""), field="run_target_price"
            ),
            horizon_end=_timestamp(raw.get("horizon_end"), field="horizon_end"),
            parent_context_tf=_required_text(
                raw.get("parent_context_tf", ""), field="parent_context_tf"
            ),
            context_tags=tuple(_required_text(tag, field="context_tags item") for tag in tags_raw),
            source_or_label_provenance=_required_text(
                raw.get("source_or_label_provenance", ""),
                field="source_or_label_provenance",
            ),
            label_known_before_outcome=label_flag,
        )
        event.validate_semantics()
        return event

    def validate_semantics(self) -> None:
        if self.pa_confirmed_at > self.post_sig_closed_at:
            raise ValueError("pa_confirmed_at must be <= post_sig_closed_at")
        if self.horizon_end < self.post_sig_closed_at:
            raise ValueError("horizon_end must be >= post_sig_closed_at")
        if not self.label_known_before_outcome:
            raise ValueError("label_known_before_outcome must be true")
        if self.side is SignalSide.BUY and self.location_label is not LocationLabel.VALID_SUPPORT:
            raise ValueError("BUY Mode-2 event requires VALID_SUPPORT location label")
        if self.side is SignalSide.SELL and self.location_label is not LocationLabel.VALID_RESISTANCE:
            raise ValueError("SELL Mode-2 event requires VALID_RESISTANCE location label")


@dataclass(frozen=True, slots=True)
class SigMode2V0Manifest:
    schema_version: str
    dataset_id: str
    tick_size: str
    events: tuple[SigMode2SignalRunEvent, ...]

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> SigMode2V0Manifest:
        version = _required_text(raw.get("schema_version", ""), field="schema_version")
        if version != SCHEMA_VERSION:
            raise ValueError(f"schema_version must equal {SCHEMA_VERSION}")
        dataset_id = _required_text(raw.get("dataset_id", ""), field="dataset_id")
        tick_size = _required_text(raw.get("tick_size", ""), field="tick_size")
        raw_events = raw.get("events")
        if not isinstance(raw_events, Sequence) or isinstance(raw_events, (str, bytes)):
            raise TypeError("events must be a sequence")
        events = tuple(SigMode2SignalRunEvent.from_mapping(item) for item in raw_events)
        if not events:
            raise ValueError("manifest must contain at least one event")
        signal_ids = [event.signal_id for event in events]
        if len(signal_ids) != len(set(signal_ids)):
            raise ValueError("signal_id values must be unique within a manifest")
        PriceGrid.from_tick_size(tick_size)
        return cls(
            schema_version=version,
            dataset_id=dataset_id,
            tick_size=tick_size,
            events=events,
        )


@dataclass(frozen=True, slots=True)
class SigMode2SignalRunOutcome:
    signal_id: str
    side: SignalSide
    signal_tf: SignalTimeframe
    signal_known_at: pd.Timestamp
    horizon_end: pd.Timestamp
    result: SignalRunResult
    terminal_at: pd.Timestamp
    bars_observed: int
    target_hit_at: pd.Timestamp | None
    point_check_hit_at: pd.Timestamp | None
    mfe_ticks: int
    mae_ticks: int
    run_anchor_tick: int
    run_target_tick: int
    point_check_tick: int


def _validate_bars(bars: pd.DataFrame) -> None:
    if not isinstance(bars.index, pd.DatetimeIndex) or bars.index.tz is None:
        raise ValueError("bars must use a timezone-aware DatetimeIndex")
    if not bars.index.is_monotonic_increasing:
        raise ValueError("bars must be sorted oldest to newest")
    required = {"high", "low", "close"}
    missing = required.difference(bars.columns)
    if missing:
        raise ValueError(f"bars missing columns: {sorted(missing)}")


def _validate_event_on_grid(event: SigMode2SignalRunEvent, grid: PriceGrid) -> tuple[int, int, int]:
    event.validate_semantics()
    point_check_tick = grid.tick_index(event.point_check_price)
    run_anchor_tick = grid.tick_index(event.run_anchor_price)
    run_target_tick = grid.tick_index(event.run_target_price)

    if point_check_tick != run_anchor_tick:
        raise ValueError(
            "V0 Mode-2 contract requires point_check_price and run_anchor_price "
            "to be the same normalized post-SIG wick reference"
        )
    if event.side is SignalSide.BUY and run_target_tick <= run_anchor_tick:
        raise ValueError("BUY run_target_price must be above run_anchor_price")
    if event.side is SignalSide.SELL and run_target_tick >= run_anchor_tick:
        raise ValueError("SELL run_target_price must be below run_anchor_price")
    return point_check_tick, run_anchor_tick, run_target_tick


def replay_sig_mode2_signal_run_v0(
    bars: pd.DataFrame,
    *,
    event: SigMode2SignalRunEvent,
    grid: PriceGrid,
) -> SigMode2SignalRunOutcome:
    """Replay one pre-labeled Mode-2 signal/run lifecycle on Bid OHLC bars.

    The replay starts at the source-backed knowledge time ``post_sig_closed_at``.
    Target crossing and literal point-check contact are then evaluated without a
    broker-fill model. If both occur in the same available bar, ordering is
    deliberately left ambiguous.
    """

    _validate_bars(bars)
    point_check_tick, run_anchor_tick, run_target_tick = _validate_event_on_grid(event, grid)

    window = bars.loc[
        (bars.index >= event.post_sig_closed_at) & (bars.index <= event.horizon_end)
    ]
    if window.empty:
        raise ValueError("no eligible bars between post_sig_closed_at and horizon_end")

    mfe_ticks = 0
    mae_ticks = 0
    target_hit_at: pd.Timestamp | None = None
    point_check_hit_at: pd.Timestamp | None = None

    for bars_observed, (timestamp, row) in enumerate(window.iterrows(), start=1):
        high_tick = grid.tick_index(row["high"])
        low_tick = grid.tick_index(row["low"])
        if low_tick > high_tick:
            raise ValueError("bar low must be <= bar high")

        if event.side is SignalSide.BUY:
            favorable = max(high_tick - run_anchor_tick, 0)
            adverse = max(run_anchor_tick - low_tick, 0)
            target_touched = high_tick >= run_target_tick
        else:
            favorable = max(run_anchor_tick - low_tick, 0)
            adverse = max(high_tick - run_anchor_tick, 0)
            target_touched = low_tick <= run_target_tick

        mfe_ticks = max(mfe_ticks, favorable)
        mae_ticks = max(mae_ticks, adverse)
        point_check_touched = low_tick <= point_check_tick <= high_tick

        if target_touched and target_hit_at is None:
            target_hit_at = timestamp
        if point_check_touched and point_check_hit_at is None:
            point_check_hit_at = timestamp

        if target_touched and point_check_touched:
            result = SignalRunResult.AMBIGUOUS_SAME_BAR
            terminal_at = timestamp
            break
        if target_touched:
            result = SignalRunResult.TARGET_FIRST
            terminal_at = timestamp
            break
        if point_check_touched:
            result = SignalRunResult.POINT_CHECK_FIRST
            terminal_at = timestamp
            break
    else:
        result = SignalRunResult.HORIZON_EXHAUSTED
        terminal_at = window.index[-1]
        bars_observed = len(window)

    return SigMode2SignalRunOutcome(
        signal_id=event.signal_id,
        side=event.side,
        signal_tf=event.signal_tf,
        signal_known_at=event.post_sig_closed_at,
        horizon_end=event.horizon_end,
        result=result,
        terminal_at=terminal_at,
        bars_observed=bars_observed,
        target_hit_at=target_hit_at,
        point_check_hit_at=point_check_hit_at,
        mfe_ticks=mfe_ticks,
        mae_ticks=mae_ticks,
        run_anchor_tick=run_anchor_tick,
        run_target_tick=run_target_tick,
        point_check_tick=point_check_tick,
    )


def replay_sig_mode2_manifest_v0(
    bars: pd.DataFrame,
    manifest: SigMode2V0Manifest,
) -> tuple[SigMode2SignalRunOutcome, ...]:
    """Replay all V0 events with one manifest-declared runtime tick grid."""

    grid = PriceGrid.from_tick_size(manifest.tick_size)
    return tuple(
        replay_sig_mode2_signal_run_v0(bars, event=event, grid=grid)
        for event in manifest.events
    )
