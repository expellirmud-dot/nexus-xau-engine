from __future__ import annotations

import argparse
import bisect
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import pandas as pd

from nexus_xau.data.csv_loader import load_ohlc_csv
from nexus_xau.data.resample import resample_ohlc
from nexus_xau.research.outcomes import FirstHit, OutcomeSpec, measure_outcome

PROJECT_POINT_SIZE = 0.01
H1_TARGET_POINTS = 1000.0
HORIZON_H1_BARS = 24
TIMEFRAMES = ("H1", "M30", "M15", "M5")
TF_DELTA = {
    "H1": pd.Timedelta("1h"),
    "M30": pd.Timedelta("30min"),
    "M15": pd.Timedelta("15min"),
    "M5": pd.Timedelta("5min"),
}
LOOKBACK_VARIANTS = {
    "EXACT_COMPLETION": 0,
    "RECENT_1_TF_BAR": 1,
    "RECENT_2_TF_BARS": 2,
}
MIN_HELDOUT_EVENTS = 100
MIN_LEVEL_EVENTS = 20


@dataclass(frozen=True, slots=True)
class Pat2BodyEvent:
    timeframe: str
    side: str
    bar_start: pd.Timestamp
    known_at: pd.Timestamp
    close: float


def _is_bearish(row: pd.Series) -> bool:
    return float(row.close) < float(row.open)


def _is_bullish(row: pd.Series) -> bool:
    return float(row.close) > float(row.open)


def _pat2_body_events(frame: pd.DataFrame, timeframe: str) -> list[Pat2BodyEvent]:
    """Detect the explicit PAT2 BODY-midpoint research variant.

    This is a research proxy, not a canonical full PA detector.
    Consecutive bars must also be truly adjacent so missing periods cannot form
    a synthetic two-candle pattern across a data gap.
    """
    delta = TF_DELTA[timeframe]
    events: list[Pat2BodyEvent] = []
    for i in range(1, len(frame)):
        previous = frame.iloc[i - 1]
        current = frame.iloc[i]
        previous_ts = frame.index[i - 1]
        current_ts = frame.index[i]
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
            Pat2BodyEvent(
                timeframe=timeframe,
                side=side,
                bar_start=current_ts,
                known_at=current_ts + delta,
                close=float(current.close),
            )
        )
    return events


def _event_index(events: list[Pat2BodyEvent]) -> tuple[list[int], list[Pat2BodyEvent]]:
    ordered = sorted(events, key=lambda event: event.known_at)
    return [event.known_at.value for event in ordered], ordered


def _latest_event_at_or_before(
    index_ns: list[int],
    events: list[Pat2BodyEvent],
    anchor_known_at: pd.Timestamp,
) -> Pat2BodyEvent | None:
    pos = bisect.bisect_right(index_ns, anchor_known_at.value) - 1
    if pos < 0:
        return None
    return events[pos]


def _alignment_count(
    *,
    anchor_side: str,
    anchor_known_at: pd.Timestamp,
    indexed_events: dict[str, tuple[list[int], list[Pat2BodyEvent]]],
    lookback_bars: int,
) -> tuple[int, tuple[str, ...]]:
    aligned: list[str] = []
    for timeframe in TIMEFRAMES:
        index_ns, events = indexed_events[timeframe]
        latest = _latest_event_at_or_before(index_ns, events, anchor_known_at)
        if latest is None:
            continue
        age = anchor_known_at - latest.known_at
        max_age = TF_DELTA[timeframe] * lookback_bars
        if lookback_bars == 0:
            fresh = age == pd.Timedelta(0)
        else:
            fresh = pd.Timedelta(0) <= age <= max_age
        if fresh and latest.side == anchor_side:
            aligned.append(timeframe)
    return len(aligned), tuple(aligned)


def _load_failed_dates(metadata_path: str | Path | None) -> set[date]:
    if metadata_path is None:
        return set()
    payload = json.loads(Path(metadata_path).read_text(encoding="utf-8"))
    return {date.fromisoformat(value) for value in payload.get("failed_dates", [])}


def _intersects_failed_date(start: pd.Timestamp, end: pd.Timestamp, failed_dates: set[date]) -> bool:
    if not failed_dates:
        return False
    current = start.normalize()
    final = end.normalize()
    while current <= final:
        if current.date() in failed_dates:
            return True
        current += pd.Timedelta("1D")
    return False


def _split(ts: pd.Timestamp, *, dev_end: pd.Timestamp, val_end: pd.Timestamp) -> str:
    if ts < dev_end:
        return "DEV"
    if ts < val_end:
        return "VAL"
    return "TEST"


def _safe_spearman(frame: pd.DataFrame, x: str, y: str) -> float | None:
    clean = frame[[x, y]].dropna()
    if len(clean) < 3 or clean[x].nunique() < 2 or clean[y].nunique() < 2:
        return None
    ranked_x = clean[x].rank(method="average")
    ranked_y = clean[y].rank(method="average")
    value = ranked_x.corr(ranked_y, method="pearson")
    if pd.isna(value):
        return None
    return float(value)


def _group_summary(group: pd.DataFrame) -> dict[str, float | int | None]:
    resolved = group[group["first_hit"].isin([FirstHit.TARGET_FIRST.value, FirstHit.STOP_FIRST.value])]
    return {
        "events": len(group),
        "resolved_events": len(resolved),
        "target_first_rate_resolved": (
            float((resolved["first_hit"] == FirstHit.TARGET_FIRST.value).mean()) if not resolved.empty else None
        ),
        "target_reach_rate_anywhere": (
            float(group["target_reached_anywhere"].mean()) if not group.empty else None
        ),
        "mfe_median": float(group["mfe_points"].median()) if not group.empty else None,
        "mae_median": float(group["mae_points"].median()) if not group.empty else None,
    }


def _relation_summary(group: pd.DataFrame) -> dict[str, object]:
    resolved = group[group["first_hit"].isin([FirstHit.TARGET_FIRST.value, FirstHit.STOP_FIRST.value])].copy()
    if not resolved.empty:
        resolved["target_first_binary"] = (
            resolved["first_hit"] == FirstHit.TARGET_FIRST.value
        ).astype(int)

    level_counts = group["alignment_count"].value_counts().sort_index().to_dict()
    usable_levels = sum(count >= MIN_LEVEL_EVENTS for count in level_counts.values())
    return {
        "events": len(group),
        "alignment_level_counts": {str(int(level)): int(count) for level, count in level_counts.items()},
        "levels_with_at_least_min_events": usable_levels,
        "spearman_alignment_vs_target_first": (
            _safe_spearman(resolved, "alignment_count", "target_first_binary") if not resolved.empty else None
        ),
        "spearman_alignment_vs_target_reach": _safe_spearman(
            group, "alignment_count", "target_reached_anywhere"
        ),
        "spearman_alignment_vs_mfe": _safe_spearman(group, "alignment_count", "mfe_points"),
        "spearman_alignment_vs_mae": _safe_spearman(group, "alignment_count", "mae_points"),
    }


def _heldout_relation_state(summary: dict[str, object]) -> str:
    if int(summary["events"]) < MIN_HELDOUT_EVENTS or int(summary["levels_with_at_least_min_events"]) < 2:
        return "INSUFFICIENT"

    tf = summary["spearman_alignment_vs_target_first"]
    reach = summary["spearman_alignment_vs_target_reach"]
    mfe = summary["spearman_alignment_vs_mfe"]
    mae = summary["spearman_alignment_vs_mae"]
    if not all(isinstance(value, float) for value in (tf, reach, mfe, mae)):
        return "INSUFFICIENT"

    if tf > 0 and reach >= 0 and mfe >= 0 and mae <= 0:
        return "SUPPORT"
    if tf <= 0 and reach <= 0 and mfe <= 0 and mae >= 0:
        return "OPPOSE"
    return "MIXED"


def run_test(
    *,
    m1_path: str | Path,
    report_path: str | Path,
    events_path: str | Path,
    dev_end: pd.Timestamp,
    val_end: pd.Timestamp,
    metadata_path: str | Path | None = None,
    positive_volume_only: bool = False,
) -> dict[str, object]:
    m1 = load_ohlc_csv(m1_path)
    source_rows = len(m1)
    if positive_volume_only:
        if "volume" not in m1.columns:
            raise ValueError("positive_volume_only requires a volume column")
        m1 = m1[m1["volume"] > 0].copy()
    active_rows = len(m1)
    failed_dates = _load_failed_dates(metadata_path)
    frames = {timeframe: resample_ohlc(m1, timeframe) for timeframe in TIMEFRAMES}
    all_events = {timeframe: _pat2_body_events(frames[timeframe], timeframe) for timeframe in TIMEFRAMES}
    indexed_events = {timeframe: _event_index(events) for timeframe, events in all_events.items()}

    anchors = all_events["H1"]
    rows: list[dict[str, object]] = []
    skipped_failed_window = 0
    skipped_insufficient_future = 0

    h1_frame = frames["H1"]
    for anchor in anchors:
        future_h1 = h1_frame.loc[h1_frame.index >= anchor.known_at]
        if len(future_h1) < HORIZON_H1_BARS:
            skipped_insufficient_future += 1
            continue
        horizon_end = future_h1.index[HORIZON_H1_BARS - 1] + TF_DELTA["H1"] - pd.Timedelta("1min")
        if _intersects_failed_date(anchor.known_at, horizon_end, failed_dates):
            skipped_failed_window += 1
            continue

        outcome = measure_outcome(
            m1,
            OutcomeSpec(
                side=anchor.side,
                reference_price=anchor.close,
                known_at=anchor.known_at,
                horizon_end=horizon_end,
                point_size=PROJECT_POINT_SIZE,
                target_points=H1_TARGET_POINTS,
                stop_points=H1_TARGET_POINTS,
            ),
        )

        for variant, lookback_bars in LOOKBACK_VARIANTS.items():
            count, aligned_tfs = _alignment_count(
                anchor_side=anchor.side,
                anchor_known_at=anchor.known_at,
                indexed_events=indexed_events,
                lookback_bars=lookback_bars,
            )
            rows.append(
                {
                    "split": _split(anchor.known_at, dev_end=dev_end, val_end=val_end),
                    "variant": variant,
                    "anchor_side": anchor.side,
                    "anchor_known_at": anchor.known_at.isoformat(),
                    "reference_price": anchor.close,
                    "alignment_count": count,
                    "aligned_timeframes": ",".join(aligned_tfs),
                    "target_reached_anywhere": outcome.mfe_points >= H1_TARGET_POINTS,
                    "first_hit": outcome.first_hit.value,
                    "mfe_points": outcome.mfe_points,
                    "mae_points": outcome.mae_points,
                    "end_return_points": outcome.end_return_points,
                }
            )

    events = pd.DataFrame(rows)
    Path(events_path).parent.mkdir(parents=True, exist_ok=True)
    events.to_csv(events_path, index=False)

    variant_reports: dict[str, object] = {}
    decisions: dict[str, str] = {}
    for variant in LOOKBACK_VARIANTS:
        variant_rows = events[events["variant"] == variant]
        split_reports: dict[str, object] = {}
        heldout_states: list[str] = []
        for split_name in ("DEV", "VAL", "TEST"):
            group = variant_rows[variant_rows["split"] == split_name]
            relation = _relation_summary(group)
            by_count = {
                str(count): _group_summary(group[group["alignment_count"] == count])
                for count in sorted(group["alignment_count"].unique())
            }
            state = _heldout_relation_state(relation) if split_name in {"VAL", "TEST"} else "DISCOVERY_ONLY"
            split_reports[split_name] = {
                "relation": relation,
                "by_alignment_count": by_count,
                "heldout_relation_state": state,
            }
            if split_name in {"VAL", "TEST"}:
                heldout_states.append(state)

        if heldout_states == ["SUPPORT", "SUPPORT"]:
            decision = "SUPPORTED"
        elif heldout_states == ["OPPOSE", "OPPOSE"]:
            decision = "NOT_SUPPORTED"
        else:
            decision = "INCONCLUSIVE"
        decisions[variant] = decision
        variant_reports[variant] = split_reports

    report: dict[str, object] = {
        "research_question": (
            "For H1 PAT2 BODY research-variant anchors, does a larger count of same-direction "
            "H1/M30/M15/M5 PAT2 BODY alignments associate with better H1 1,000-point forward behavior?"
        ),
        "research_status": "MTF_ALIGNMENT_VARIANT_RELATION_COMPONENT_TEST",
        "source_m1": str(m1_path),
        "source_metadata": str(metadata_path) if metadata_path is not None else None,
        "positive_volume_only": positive_volume_only,
        "source_m1_rows": source_rows,
        "active_m1_rows": active_rows,
        "timeframes": list(TIMEFRAMES),
        "anchor": "H1 PAT2 BODY midpoint-pass research variant; reference price = completed anchor close",
        "alignment_proxy": (
            "On each TF, use the latest PAT2 BODY event at/before the H1 anchor known_at. "
            "Count it aligned only when it is fresh under the variant window and its side matches the H1 anchor."
        ),
        "lookback_variants": LOOKBACK_VARIANTS,
        "outcome_control": {
            "target_points": H1_TARGET_POINTS,
            "point_size": PROJECT_POINT_SIZE,
            "horizon": "next 24 active H1 bars after anchor known_at",
            "adverse_barrier": "symmetric 1,000-point research control, not canonical SL",
            "target_model": "FRESH_TARGET_CONTROL, not inherited remaining-run",
            "horizon_h1_bars": HORIZON_H1_BARS,
        },
        "chronological_split": {
            "DEV": f"before {dev_end.isoformat()}",
            "VAL": f"{dev_end.isoformat()} through before {val_end.isoformat()}",
            "TEST": f"{val_end.isoformat()} onward",
        },
        "closure_rule": (
            "Per lookback variant: SUPPORTED only when VAL and TEST both show positive/non-negative "
            "Spearman relation for target-first, target reach and MFE, and non-positive relation for MAE, "
            f"with >= {MIN_HELDOUT_EVENTS} events and >=2 count levels having >= {MIN_LEVEL_EVENTS} events. "
            "NOT_SUPPORTED only when both held-out splits consistently oppose those core directions; otherwise INCONCLUSIVE."
        ),
        "failed_dates_excluded": sorted(value.isoformat() for value in failed_dates),
        "h1_anchor_events_detected": len(anchors),
        "skipped_anchor_horizons_intersecting_failed_dates": skipped_failed_window,
        "skipped_insufficient_future": skipped_insufficient_future,
        "measured_anchor_events": int(len(events) / len(LOOKBACK_VARIANTS)) if not events.empty else 0,
        "variant_reports": variant_reports,
        "decisions": decisions,
        "limitations": [
            "PAT2 BODY is a research proxy, not the canonical full PA/SIG detector.",
            "PAT1, PAT3, Daily Frame, SW, Location and inherited remaining-run are not included in this first MTF component test.",
            "Outcome performance cannot choose a production minimum aligned-TF count.",
            "A failure of this proxy does not refute the user-direct semantic that more true PA alignment is stronger.",
            "Dukascopy BID is a research feed and remains distinct from the Exness/MT5 execution feed.",
        ],
    }
    Path(report_path).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--m1", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--events", required=True)
    parser.add_argument("--dev-end", required=True, help="UTC ISO boundary, e.g. 2023-02-01")
    parser.add_argument("--val-end", required=True, help="UTC ISO boundary, e.g. 2023-05-01")
    parser.add_argument("--metadata", default=None)
    parser.add_argument("--positive-volume-only", action="store_true")
    args = parser.parse_args()

    dev_end = pd.Timestamp(args.dev_end, tz="UTC")
    val_end = pd.Timestamp(args.val_end, tz="UTC")
    if val_end <= dev_end:
        raise ValueError("val-end must be after dev-end")

    result = run_test(
        m1_path=args.m1,
        report_path=args.report,
        events_path=args.events,
        dev_end=dev_end,
        val_end=val_end,
        metadata_path=args.metadata,
        positive_volume_only=args.positive_volume_only,
    )
    print(json.dumps(result["decisions"], ensure_ascii=False, indent=2))
    print(
        "anchors=",
        result["h1_anchor_events_detected"],
        "measured=",
        result["measured_anchor_events"],
        "skipped_failed=",
        result["skipped_anchor_horizons_intersecting_failed_dates"],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
