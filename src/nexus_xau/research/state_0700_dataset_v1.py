from __future__ import annotations

import argparse
import bisect
import hashlib
import json
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path

import numpy as np
import pandas as pd

from nexus_xau.data.csv_loader import load_ohlc_csv
from nexus_xau.data.resample import resample_ohlc
from nexus_xau.engine.mae_pla_frame import build_mae_pla_frame_candidates

PROJECT_POINT_SIZE = 0.01
ORIGIN_TFS = ("H1", "H4", "D1")
CONFIRM_TFS = ("H1", "M30", "M15", "M5")
TF_DELTA = {
    "M5": timedelta(minutes=5),
    "M15": timedelta(minutes=15),
    "M30": timedelta(minutes=30),
    "H1": timedelta(hours=1),
    "H4": timedelta(hours=4),
    "D1": timedelta(days=1),
}
NOMINAL_RUN_POINTS: dict[str, float | None] = {
    "H1": 1000.0,
    "H4": 1500.0,
    "D1": None,
}
LOOKBACK_VARIANTS = {
    "EXACT": 0,
    "RECENT_1_TF_BAR": 1,
    "RECENT_2_TF_BARS": 2,
}


@dataclass(frozen=True, slots=True)
class ProxyPaEvent:
    timeframe: str
    side: str
    previous_bar_start: pd.Timestamp
    pattern_bar_start: pd.Timestamp
    known_at: pd.Timestamp
    close: float
    pattern_low: float
    pattern_high: float


@dataclass(frozen=True, slots=True)
class ProxyOrigin:
    origin_id: str
    timeframe: str
    side: str
    pattern_known_at: pd.Timestamp
    origin_known_at: pd.Timestamp
    anchor_price: float
    nominal_run_points: float | None


def _is_bearish(row: pd.Series) -> bool:
    return float(row.close) < float(row.open)


def _is_bullish(row: pd.Series) -> bool:
    return float(row.close) > float(row.open)


def _proxy_pa_events(frame: pd.DataFrame, timeframe: str) -> list[ProxyPaEvent]:
    """Build the frozen PAT2-BODY midpoint-pass research proxy.

    This is intentionally a research representation, not a canonical PA/PAT detector.
    """
    delta = TF_DELTA[timeframe]
    events: list[ProxyPaEvent] = []
    for i in range(1, len(frame)):
        previous = frame.iloc[i - 1]
        current = frame.iloc[i]
        previous_ts = pd.Timestamp(frame.index[i - 1])
        current_ts = pd.Timestamp(frame.index[i])
        if current_ts - previous_ts != delta:
            continue

        midpoint = (float(previous.open) + float(previous.close)) / 2.0
        side: str | None = None
        if _is_bearish(previous) and _is_bullish(current) and float(current.close) > midpoint:
            side = "BUY"
        elif _is_bullish(previous) and _is_bearish(current) and float(current.close) < midpoint:
            side = "SELL"
        if side is None:
            continue

        events.append(
            ProxyPaEvent(
                timeframe=timeframe,
                side=side,
                previous_bar_start=previous_ts,
                pattern_bar_start=current_ts,
                known_at=current_ts + delta,
                close=float(current.close),
                pattern_low=min(float(previous.low), float(current.low)),
                pattern_high=max(float(previous.high), float(current.high)),
            )
        )
    return events


def _build_proxy_origins(
    frame: pd.DataFrame,
    *,
    timeframe: str,
    pa_events: list[ProxyPaEvent],
) -> list[ProxyOrigin]:
    """Map a proxy PA to its adjacent post-SIG candle reference.

    The mapping is retained as a research proxy. No winner/priority is selected.
    """
    delta = TF_DELTA[timeframe]
    nominal = NOMINAL_RUN_POINTS[timeframe]
    origins: list[ProxyOrigin] = []
    for event in pa_events:
        post_sig_start = event.known_at
        if post_sig_start not in frame.index:
            continue
        post_sig = frame.loc[post_sig_start]
        origin_known_at = post_sig_start + delta
        anchor = float(post_sig.low if event.side == "BUY" else post_sig.high)
        origin_id = (
            f"{timeframe}:{event.side}:"
            f"{origin_known_at.isoformat().replace('+00:00', 'Z')}"
        )
        origins.append(
            ProxyOrigin(
                origin_id=origin_id,
                timeframe=timeframe,
                side=event.side,
                pattern_known_at=event.known_at,
                origin_known_at=origin_known_at,
                anchor_price=anchor,
                nominal_run_points=nominal,
            )
        )
    return origins


def _latest_completed_snapshot(
    frame: pd.DataFrame,
    *,
    cutoff: pd.Timestamp,
    timeframe: str,
) -> tuple[pd.Series | None, pd.Series | None, pd.Timestamp | None]:
    delta = TF_DELTA[timeframe]
    eligible = frame.index[frame.index + delta <= cutoff]
    if len(eligible) == 0:
        return None, None, None
    current_start = pd.Timestamp(eligible[-1])
    current = frame.loc[current_start]
    previous_start = current_start - delta
    previous = frame.loc[previous_start] if previous_start in frame.index else None
    return current, previous, current_start


def _bar_features(
    *,
    prefix: str,
    current: pd.Series | None,
    previous: pd.Series | None,
    bar_start: pd.Timestamp | None,
) -> dict[str, object]:
    names = {
        f"{prefix}_bar_start": None,
        f"{prefix}_open": None,
        f"{prefix}_high": None,
        f"{prefix}_low": None,
        f"{prefix}_close": None,
        f"{prefix}_range_points": None,
        f"{prefix}_body_size_points": None,
        f"{prefix}_upper_wick_points": None,
        f"{prefix}_lower_wick_points": None,
        f"{prefix}_body_fraction_of_range": None,
        f"{prefix}_close_fraction_of_range": None,
        f"{prefix}_close_vs_previous_body_mid_points": None,
        f"{prefix}_close_vs_previous_range_mid_points": None,
        f"{prefix}_close_vs_current_body_mid_points": None,
        f"{prefix}_close_vs_current_range_mid_points": None,
    }
    if current is None or bar_start is None:
        return names

    open_price = float(current.open)
    high = float(current.high)
    low = float(current.low)
    close = float(current.close)
    range_price = high - low
    body = abs(close - open_price)
    upper_wick = high - max(open_price, close)
    lower_wick = min(open_price, close) - low

    names.update(
        {
            f"{prefix}_bar_start": bar_start.isoformat(),
            f"{prefix}_open": open_price,
            f"{prefix}_high": high,
            f"{prefix}_low": low,
            f"{prefix}_close": close,
            f"{prefix}_range_points": range_price / PROJECT_POINT_SIZE,
            f"{prefix}_body_size_points": body / PROJECT_POINT_SIZE,
            f"{prefix}_upper_wick_points": upper_wick / PROJECT_POINT_SIZE,
            f"{prefix}_lower_wick_points": lower_wick / PROJECT_POINT_SIZE,
            f"{prefix}_body_fraction_of_range": body / range_price if range_price > 0 else None,
            f"{prefix}_close_fraction_of_range": (
                (close - low) / range_price if range_price > 0 else None
            ),
            f"{prefix}_close_vs_current_body_mid_points": (
                close - ((open_price + close) / 2.0)
            )
            / PROJECT_POINT_SIZE,
            f"{prefix}_close_vs_current_range_mid_points": (
                close - ((high + low) / 2.0)
            )
            / PROJECT_POINT_SIZE,
        }
    )

    if previous is not None:
        previous_body_mid = (float(previous.open) + float(previous.close)) / 2.0
        previous_range_mid = (float(previous.high) + float(previous.low)) / 2.0
        names[f"{prefix}_close_vs_previous_body_mid_points"] = (
            close - previous_body_mid
        ) / PROJECT_POINT_SIZE
        names[f"{prefix}_close_vs_previous_range_mid_points"] = (
            close - previous_range_mid
        ) / PROJECT_POINT_SIZE
    return names


def _build_day_states(
    *,
    active_m1: pd.DataFrame,
    frames: dict[str, pd.DataFrame],
    data_source: str,
    complete_cache_range: bool | None,
    source_sha256: str | None,
) -> pd.DataFrame:
    exact_cutoff = (
        (active_m1.index.hour == 0)
        & (active_m1.index.minute == 0)
        & (active_m1.index.second == 0)
    )
    cutoffs = pd.DatetimeIndex(active_m1.index[exact_cutoff]).sort_values().unique()
    rows: list[dict[str, object]] = []

    for cutoff in cutoffs:
        cutoff = pd.Timestamp(cutoff)
        open_0700 = float(active_m1.loc[cutoff, "open"])
        frame_set = build_mae_pla_frame_candidates(open_0700)
        references = [float(item.reference_price) for item in frame_set.candidates]
        uppers = [float(item.upper_price) for item in frame_set.candidates]
        lowers = [float(item.lower_price) for item in frame_set.candidates]
        unique_frame = len(frame_set.candidates) == 1

        row: dict[str, object] = {
            "day_id": cutoff.strftime("%Y-%m-%d"),
            "cutoff_utc": cutoff.isoformat(),
            "cutoff_thailand": cutoff.tz_convert("Asia/Bangkok").isoformat(),
            "data_source": data_source,
            "data_quality_state": (
                "CACHE_COMPLETE_RANGE"
                if complete_cache_range is True
                else "CACHE_COMPLETENESS_NOT_ASSERTED"
            ),
            "source_sha256": source_sha256,
            "price_at_cutoff": open_0700,
            "daily_frame_candidate_count": len(frame_set.candidates),
            "daily_frame_reference_candidates": json.dumps(references),
            "daily_frame_upper_candidates": json.dumps(uppers),
            "daily_frame_lower_candidates": json.dumps(lowers),
            "daily_frame_reference": references[0] if unique_frame else None,
            "daily_frame_upper": uppers[0] if unique_frame else None,
            "daily_frame_lower": lowers[0] if unique_frame else None,
            "daily_frame_tie_ambiguous": not unique_frame,
            "origin_history_left_censored": True,
        }

        for timeframe, prefix in (("H1", "h1"), ("H4", "h4"), ("D1", "d1")):
            current, previous, start = _latest_completed_snapshot(
                frames[timeframe],
                cutoff=cutoff,
                timeframe=timeframe,
            )
            row.update(
                _bar_features(
                    prefix=prefix,
                    current=current,
                    previous=previous,
                    bar_start=start,
                )
            )
        rows.append(row)

    return pd.DataFrame(rows)


def _favorable_consumed_points(
    *,
    index: pd.DatetimeIndex,
    highs: np.ndarray,
    lows: np.ndarray,
    origin: ProxyOrigin,
    cutoff: pd.Timestamp,
) -> float:
    start = int(index.searchsorted(origin.origin_known_at, side="left"))
    end = int(index.searchsorted(cutoff, side="left"))
    if end <= start:
        return 0.0
    if origin.side == "BUY":
        favorable = float(np.max(highs[start:end])) - origin.anchor_price
    else:
        favorable = origin.anchor_price - float(np.min(lows[start:end]))
    return max(0.0, favorable / PROJECT_POINT_SIZE)


def _first_point_check_touch(
    *,
    index: pd.DatetimeIndex,
    highs: np.ndarray,
    lows: np.ndarray,
    origin: ProxyOrigin,
) -> pd.Timestamp | None:
    """Return the first literal M1 range contact with the proxy point-check.

    This applies the source-backed literal-contact concept to a research-proxy anchor.
    It does not upgrade the proxy origin into a canonical SIG.
    """
    start = int(index.searchsorted(origin.origin_known_at, side="left"))
    if start >= len(index):
        return None
    mask = (lows[start:] <= origin.anchor_price) & (highs[start:] >= origin.anchor_price)
    hits = np.flatnonzero(mask)
    if hits.size == 0:
        return None
    return pd.Timestamp(index[start + int(hits[0])])


def _point_check_cutoff_state(
    *,
    first_touch_at: pd.Timestamp | None,
    cutoff: pd.Timestamp,
) -> tuple[str, bool, pd.Timestamp | None]:
    """Expose point-check state using only information known strictly before cutoff."""
    if first_touch_at is not None and first_touch_at < cutoff:
        return "TOUCHED_BEFORE_0700", False, first_touch_at
    return "UNTOUCHED_BEFORE_0700", True, None


def _build_origin_candidates(
    *,
    active_m1: pd.DataFrame,
    day_states: pd.DataFrame,
    frames: dict[str, pd.DataFrame],
    origin_pa_events: dict[str, list[ProxyPaEvent]],
) -> pd.DataFrame:
    if day_states.empty:
        return pd.DataFrame()

    cutoffs = [pd.Timestamp(value) for value in day_states["cutoff_utc"]]
    cutoff_ns = [value.value for value in cutoffs]
    index = active_m1.index
    highs = active_m1["high"].to_numpy(dtype=float, copy=False)
    lows = active_m1["low"].to_numpy(dtype=float, copy=False)
    rows: list[dict[str, object]] = []

    for timeframe in ORIGIN_TFS:
        origins = _build_proxy_origins(
            frames[timeframe],
            timeframe=timeframe,
            pa_events=origin_pa_events[timeframe],
        )
        for origin in origins:
            first_touch_at = (
                _first_point_check_touch(
                    index=index,
                    highs=highs,
                    lows=lows,
                    origin=origin,
                )
                if origin.nominal_run_points is not None
                else None
            )
            first_pos = bisect.bisect_left(cutoff_ns, origin.origin_known_at.value)
            for cutoff in cutoffs[first_pos:]:
                if origin.nominal_run_points is None:
                    consumed: float | None = None
                    remaining: float | None = None
                    ratio: float | None = None
                    validity = "UNRESOLVED_TARGET_DISTANCE"
                    point_check_state = "NOT_EVALUATED_D1_V1"
                    source_partial_survival = False
                    visible_touch_at = None
                else:
                    consumed = _favorable_consumed_points(
                        index=index,
                        highs=highs,
                        lows=lows,
                        origin=origin,
                        cutoff=cutoff,
                    )
                    if consumed >= origin.nominal_run_points:
                        break
                    remaining = origin.nominal_run_points - consumed
                    ratio = consumed / origin.nominal_run_points
                    validity = "INCOMPLETE_NOMINAL_RUN_RESEARCH_PROXY"
                    (
                        point_check_state,
                        source_partial_survival,
                        visible_touch_at,
                    ) = _point_check_cutoff_state(
                        first_touch_at=first_touch_at,
                        cutoff=cutoff,
                    )

                rows.append(
                    {
                        "day_id": cutoff.strftime("%Y-%m-%d"),
                        "cutoff_utc": cutoff.isoformat(),
                        "origin_id": origin.origin_id,
                        "origin_tf": origin.timeframe,
                        "origin_side": origin.side,
                        "pattern_known_at": origin.pattern_known_at.isoformat(),
                        "origin_known_at": origin.origin_known_at.isoformat(),
                        "origin_anchor_price": origin.anchor_price,
                        "origin_source_class": "RESEARCH_REPRESENTATION",
                        "origin_detector": "PAT2_BODY_MIDPOINT_PROXY",
                        "origin_validity_state": validity,
                        "origin_target_definition": (
                            f"NOMINAL_{int(origin.nominal_run_points)}_PROJECT_POINTS"
                            if origin.nominal_run_points is not None
                            else "UNRESOLVED_D1_RUN_DISTANCE"
                        ),
                        "nominal_run_points": origin.nominal_run_points,
                        "consumed_points_at_0700": consumed,
                        "consumed_ratio_at_0700": ratio,
                        "remaining_points_at_0700": remaining,
                        "origin_age_hours": (
                            cutoff - origin.origin_known_at
                        ).total_seconds()
                        / 3600.0,
                        "point_check_first_touch_before_cutoff_at": (
                            visible_touch_at.isoformat()
                            if visible_touch_at is not None
                            else None
                        ),
                        "point_check_state": point_check_state,
                        "source_partial_survival_proxy": source_partial_survival,
                        "invalidation_reason": (
                            "SOURCE_LITERAL_TOUCH_APPLIED_TO_RESEARCH_PROXY_ANCHOR"
                            if origin.nominal_run_points is not None
                            else "D1_POINT_CHECK_NOT_EVALUATED_V1"
                        ),
                    }
                )

    origins = pd.DataFrame(rows)
    if origins.empty:
        return origins

    origins["is_measurable_incomplete"] = origins["origin_tf"].isin(["H1", "H4"])
    origins["is_unresolved_d1"] = origins["origin_tf"].eq("D1")

    for day_id, group in origins.groupby("day_id"):
        measurable = group[group["is_measurable_incomplete"]]
        for side in ("BUY", "SELL"):
            same = measurable[measurable["origin_side"] == side]
            opposite = measurable[measurable["origin_side"] != side]
            d1_same = group[
                group["is_unresolved_d1"] & group["origin_side"].eq(side)
            ]
            indexer = group.index[group["origin_side"].eq(side)]
            origins.loc[indexer, "measurable_same_side_origin_count"] = len(same)
            origins.loc[indexer, "measurable_same_side_origin_tf_set"] = ",".join(
                sorted(set(same["origin_tf"]))
            )
            origins.loc[indexer, "measurable_opposite_side_origin_count"] = len(opposite)
            origins.loc[indexer, "unresolved_d1_same_side_count"] = len(d1_same)
            origins.loc[indexer, "measurable_origin_conflict_state"] = (
                "OPPOSITE_SIDE_MEASURABLE_ORIGIN_PRESENT"
                if len(opposite) > 0
                else "NO_OPPOSITE_SIDE_MEASURABLE_ORIGIN"
            )

    return origins


def _event_index(
    events: list[ProxyPaEvent],
) -> tuple[list[int], list[ProxyPaEvent]]:
    ordered = sorted(events, key=lambda event: event.known_at)
    return [event.known_at.value for event in ordered], ordered


def _alignment_snapshot(
    *,
    anchor_side: str,
    anchor_known_at: pd.Timestamp,
    indexed_events: dict[str, tuple[list[int], list[ProxyPaEvent]]],
    lookback_bars: int,
) -> tuple[int, tuple[str, ...]]:
    aligned: list[str] = []
    for timeframe in CONFIRM_TFS:
        index_ns, events = indexed_events[timeframe]
        pos = bisect.bisect_right(index_ns, anchor_known_at.value) - 1
        if pos < 0:
            continue
        latest = events[pos]
        age = anchor_known_at - latest.known_at
        max_age = TF_DELTA[timeframe] * lookback_bars
        if lookback_bars == 0:
            fresh = age == timedelta(0)
        else:
            fresh = timedelta(0) <= age <= max_age
        if fresh and latest.side == anchor_side:
            aligned.append(timeframe)
    return len(aligned), tuple(aligned)


def _frame_relation(
    *,
    event: ProxyPaEvent,
    day_row: pd.Series,
) -> tuple[str, float | None]:
    if bool(day_row["daily_frame_tie_ambiguous"]):
        return "AMBIGUOUS_FRAME_TIE", None

    if event.side == "BUY":
        line = float(day_row["daily_frame_lower"])
        signed = (event.pattern_low - line) / PROJECT_POINT_SIZE
    else:
        line = float(day_row["daily_frame_upper"])
        signed = (line - event.pattern_high) / PROJECT_POINT_SIZE
    return ("EXPECTED_SIDE" if signed >= 0 else "CROSSED_SIDE"), float(signed)


def _build_confirmation_events(
    *,
    day_states: pd.DataFrame,
    confirm_events: dict[str, list[ProxyPaEvent]],
    origin_candidates: pd.DataFrame,
) -> pd.DataFrame:
    if day_states.empty:
        return pd.DataFrame()

    days = {
        str(row.day_id): row
        for row in day_states.itertuples(index=False)
    }
    day_rows = {
        str(row["day_id"]): row
        for _, row in day_states.iterrows()
    }
    indexed = {
        timeframe: _event_index(confirm_events[timeframe])
        for timeframe in CONFIRM_TFS
    }

    origin_by_day: dict[str, pd.DataFrame] = {}
    if not origin_candidates.empty:
        origin_by_day = {
            str(day_id): group.copy()
            for day_id, group in origin_candidates.groupby("day_id")
        }

    rows: list[dict[str, object]] = []
    for timeframe in CONFIRM_TFS:
        for event in confirm_events[timeframe]:
            cutoff = event.known_at.normalize()
            if event.known_at == cutoff:
                continue
            day_id = cutoff.strftime("%Y-%m-%d")
            if day_id not in days:
                continue
            if event.known_at >= cutoff + timedelta(days=1):
                continue

            day_row = day_rows[day_id]
            frame_side, signed_distance = _frame_relation(
                event=event,
                day_row=day_row,
            )
            context = origin_by_day.get(day_id, pd.DataFrame())
            if context.empty:
                same_measurable = context
                opposite_measurable = context
                same_surviving = context
                same_d1 = context
            else:
                measurable = context[context["is_measurable_incomplete"]]
                same_measurable = measurable[measurable["origin_side"] == event.side]
                opposite_measurable = measurable[measurable["origin_side"] != event.side]
                same_surviving = same_measurable[
                    same_measurable["source_partial_survival_proxy"].astype(bool)
                ]
                same_d1 = context[
                    context["is_unresolved_d1"]
                    & context["origin_side"].eq(event.side)
                ]

            row: dict[str, object] = {
                "day_id": day_id,
                "context_id": f"{day_id}:{event.side}",
                "event_id": (
                    f"{timeframe}:{event.side}:"
                    f"{event.known_at.isoformat().replace('+00:00', 'Z')}"
                ),
                "event_tf": timeframe,
                "event_side": event.side,
                "event_known_at": event.known_at.isoformat(),
                "minutes_since_0700": (
                    event.known_at - cutoff
                ).total_seconds()
                / 60.0,
                "pattern_bar_start": event.pattern_bar_start.isoformat(),
                "pattern_close": event.close,
                "pattern_low": event.pattern_low,
                "pattern_high": event.pattern_high,
                "frame_side": frame_side,
                "signed_distance_to_valid_frame_side_points": signed_distance,
                "same_side_measurable_incomplete_origin_count": len(same_measurable),
                "opposite_side_measurable_incomplete_origin_count": len(
                    opposite_measurable
                ),
                "same_side_source_partial_surviving_origin_count": len(same_surviving),
                "same_side_unresolved_d1_origin_count": len(same_d1),
                "same_side_measurable_origin_ids": json.dumps(
                    list(same_measurable.get("origin_id", pd.Series(dtype=str)))
                ),
                "m1_brake_state": "UNRESOLVED_NOT_COMPUTED_V1",
                "m5_brake_state": "UNRESOLVED_NOT_COMPUTED_V1",
                "retest_state": "UNRESOLVED_NOT_COMPUTED_V1",
                "frame_stand_state": "UNRESOLVED_NOT_COMPUTED_V1",
                "structure_confirm_state": "UNRESOLVED_NOT_COMPUTED_V1",
            }

            exact_count, exact_tfs = _alignment_snapshot(
                anchor_side=event.side,
                anchor_known_at=event.known_at,
                indexed_events=indexed,
                lookback_bars=0,
            )
            row["alignment_count_exact"] = exact_count
            row["aligned_tf_set_exact"] = ",".join(exact_tfs)
            for tf in CONFIRM_TFS:
                row[f"{tf.lower()}_pa_proxy_exact"] = tf in exact_tfs

            for label, bars in LOOKBACK_VARIANTS.items():
                if label == "EXACT":
                    continue
                count, tfs = _alignment_snapshot(
                    anchor_side=event.side,
                    anchor_known_at=event.known_at,
                    indexed_events=indexed,
                    lookback_bars=bars,
                )
                suffix = label.lower()
                row[f"alignment_count_{suffix}"] = count
                row[f"aligned_tf_set_{suffix}"] = ",".join(tfs)

            rows.append(row)

    events = pd.DataFrame(rows)
    if events.empty:
        return events
    events = events.sort_values(["event_known_at", "event_tf", "event_side"]).reset_index(
        drop=True
    )
    events["event_sequence_index"] = (
        events.groupby("day_id").cumcount() + 1
    )
    return events


def _sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_metadata(path: str | Path | None) -> dict[str, object]:
    if path is None:
        return {}
    return json.loads(Path(path).read_text(encoding="utf-8"))


def build_dataset(
    *,
    m1_path: str | Path,
    metadata_path: str | Path | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, object]]:
    m1 = load_ohlc_csv(m1_path)
    if "volume" in m1.columns:
        active_m1 = m1[m1["volume"] > 0].copy()
    else:
        active_m1 = m1.copy()
    if active_m1.empty:
        raise ValueError("no active M1 rows")

    metadata = _load_metadata(metadata_path)
    frames = {
        timeframe: resample_ohlc(active_m1, timeframe)
        for timeframe in ("M5", "M15", "M30", "H1", "H4", "D1")
    }
    pa_events = {
        timeframe: _proxy_pa_events(frames[timeframe], timeframe)
        for timeframe in ("M5", "M15", "M30", "H1", "H4", "D1")
    }

    day_states = _build_day_states(
        active_m1=active_m1,
        frames=frames,
        data_source=str(metadata.get("source", Path(m1_path).name)),
        complete_cache_range=(
            bool(metadata["complete_cache_range"])
            if "complete_cache_range" in metadata
            else None
        ),
        source_sha256=str(metadata.get("sha256") or _sha256(m1_path)),
    )
    origins = _build_origin_candidates(
        active_m1=active_m1,
        day_states=day_states,
        frames=frames,
        origin_pa_events={tf: pa_events[tf] for tf in ORIGIN_TFS},
    )

    if not day_states.empty:
        measurable_counts = (
            origins[origins.get("is_measurable_incomplete", False)]
            .groupby("day_id")
            .size()
            if not origins.empty
            else pd.Series(dtype=int)
        )
        surviving_counts = (
            origins[
                origins.get("is_measurable_incomplete", False)
                & origins.get("source_partial_survival_proxy", False)
            ]
            .groupby("day_id")
            .size()
            if not origins.empty
            else pd.Series(dtype=int)
        )
        d1_counts = (
            origins[origins.get("is_unresolved_d1", False)]
            .groupby("day_id")
            .size()
            if not origins.empty
            else pd.Series(dtype=int)
        )
        day_states["measurable_incomplete_origin_count"] = (
            day_states["day_id"].map(measurable_counts).fillna(0).astype(int)
        )
        day_states["source_partial_surviving_origin_count"] = (
            day_states["day_id"].map(surviving_counts).fillna(0).astype(int)
        )
        day_states["unresolved_d1_origin_count"] = (
            day_states["day_id"].map(d1_counts).fillna(0).astype(int)
        )

    confirmation = _build_confirmation_events(
        day_states=day_states,
        confirm_events={tf: pa_events[tf] for tf in CONFIRM_TFS},
        origin_candidates=origins,
    )

    report: dict[str, object] = {
        "research_status": "0700_STATE_DATASET_V1_EXPLORATORY_FEATURE_ONLY",
        "source_m1": str(m1_path),
        "source_metadata": str(metadata_path) if metadata_path else None,
        "source_sha256": metadata.get("sha256") or _sha256(m1_path),
        "time_mapping": "07:00 Asia/Bangkok = 00:00 UTC",
        "rows": {
            "day_state": len(day_states),
            "origin_candidates": len(origins),
            "confirmation_events": len(confirmation),
        },
        "proxy_event_counts": {
            timeframe: len(pa_events[timeframe])
            for timeframe in ("M5", "M15", "M30", "H1", "H4", "D1")
        },
        "nominal_run_points": NOMINAL_RUN_POINTS,
        "guards": [
            "Feature-only dataset: no P&L, trade Win/Loss, or outcome optimization is performed.",
            "PAT2 BODY midpoint pass is a research proxy, not canonical PA/PAT.",
            "H1=1000 and H4=1500 are retained as source-supported run distances; D1 run distance remains unresolved.",
            "No origin winner/priority is selected.",
            "No age/expiry threshold is introduced.",
            "Literal point-check contact is measured on H1/H4 proxy anchors as a separate source-partial survival feature; rows are not deleted by it.",
            "M1/M5 brake, retest, frame-standing and structure-confirmation numeric gates remain unresolved and are not computed.",
            "Daily Frame snap ties remain ambiguous rather than silently resolved.",
            "Origin history is left-censored at the beginning of the supplied dataset.",
            "This exploratory dataset is separate from the unopened V0.1 prospective holdout.",
        ],
    }
    return day_states, origins, confirmation, report


def run(
    *,
    m1_path: str | Path,
    metadata_path: str | Path | None,
    output_root: str | Path,
) -> dict[str, object]:
    day_states, origins, confirmation, report = build_dataset(
        m1_path=m1_path,
        metadata_path=metadata_path,
    )
    root = Path(output_root)
    root.mkdir(parents=True, exist_ok=True)
    day_states.to_csv(root / "0700_day_state.csv", index=False)
    origins.to_csv(root / "0700_origin_candidates.csv", index=False)
    confirmation.to_csv(root / "0700_confirmation_events.csv", index=False)
    (root / "REPORT.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--m1", required=True)
    parser.add_argument("--metadata", default=None)
    parser.add_argument("--output-root", required=True)
    args = parser.parse_args()
    report = run(
        m1_path=args.m1,
        metadata_path=args.metadata,
        output_root=args.output_root,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
