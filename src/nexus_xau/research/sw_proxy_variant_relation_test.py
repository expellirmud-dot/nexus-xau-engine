from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

from nexus_xau.data.csv_loader import load_ohlc_csv
from nexus_xau.data.resample import resample_ohlc
from nexus_xau.research.mtf_alignment_variant_relation_test import (
    _group_summary,
    _safe_spearman,
)

WINDOWS = (6, 12, 24)
FEATURES = (
    "oscillation_strength",
    "direction_flip_rate",
    "candle_overlap_rate",
)
MIN_HELDOUT_EVENTS = 100
MIN_QUARTILE_EVENTS = 20


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
        current += pd.Timedelta(days=1)
    return False


def _sw_shape_features(window: pd.DataFrame) -> dict[str, float | None]:
    if len(window) < 2:
        return {feature: None for feature in FEATURES}

    closes = window["close"].to_numpy(dtype=float)
    changes = np.diff(closes)
    path = float(np.abs(changes).sum())
    net = float(abs(closes[-1] - closes[0]))
    oscillation_strength = None if path <= 0 else float(1.0 - (net / path))

    signs = np.sign(changes)
    signs = signs[signs != 0]
    if len(signs) < 2:
        direction_flip_rate = None
    else:
        direction_flip_rate = float((signs[1:] != signs[:-1]).mean())

    overlaps: list[float] = []
    highs = window["high"].to_numpy(dtype=float)
    lows = window["low"].to_numpy(dtype=float)
    for i in range(1, len(window)):
        prior_range = highs[i - 1] - lows[i - 1]
        current_range = highs[i] - lows[i]
        denominator = min(prior_range, current_range)
        if denominator <= 0:
            continue
        overlap = max(0.0, min(highs[i - 1], highs[i]) - max(lows[i - 1], lows[i]))
        overlaps.append(min(1.0, overlap / denominator))
    candle_overlap_rate = float(np.mean(overlaps)) if overlaps else None

    return {
        "oscillation_strength": oscillation_strength,
        "direction_flip_rate": direction_flip_rate,
        "candle_overlap_rate": candle_overlap_rate,
    }


def _quartile_better(high: dict[str, object], low: dict[str, object]) -> bool:
    high_tf = high["target_first_rate_resolved"]
    low_tf = low["target_first_rate_resolved"]
    high_reach = high["target_reach_rate_anywhere"]
    low_reach = low["target_reach_rate_anywhere"]
    if not all(isinstance(value, float) for value in (high_tf, low_tf, high_reach, low_reach)):
        return False
    return bool(high_tf > low_tf and high_reach >= low_reach)


def _quartile_opposes(high: dict[str, object], low: dict[str, object]) -> bool:
    high_tf = high["target_first_rate_resolved"]
    low_tf = low["target_first_rate_resolved"]
    high_reach = high["target_reach_rate_anywhere"]
    low_reach = low["target_reach_rate_anywhere"]
    if not all(isinstance(value, float) for value in (high_tf, low_tf, high_reach, low_reach)):
        return False
    return bool(high_tf < low_tf and high_reach <= low_reach)


def _relation_state(
    *,
    group: pd.DataFrame,
    feature: str,
    low_threshold: float,
    high_threshold: float,
) -> tuple[str, dict[str, object]]:
    clean = group[group[feature].notna()].copy()
    low_group = clean[clean[feature] <= low_threshold]
    high_group = clean[clean[feature] >= high_threshold]

    resolved = clean[clean["first_hit"].isin(["TARGET_FIRST", "STOP_FIRST"])].copy()
    if not resolved.empty:
        resolved["target_first_binary"] = (resolved["first_hit"] == "TARGET_FIRST").astype(int)

    relation = {
        "events": len(clean),
        "low_quartile_events": len(low_group),
        "high_quartile_events": len(high_group),
        "spearman_vs_target_first": (
            _safe_spearman(resolved, feature, "target_first_binary") if not resolved.empty else None
        ),
        "spearman_vs_target_reach": _safe_spearman(clean, feature, "target_reached_anywhere"),
        "spearman_vs_mfe": _safe_spearman(clean, feature, "mfe_points"),
        "spearman_vs_mae": _safe_spearman(clean, feature, "mae_points"),
        "low_quartile": _group_summary(low_group),
        "high_quartile": _group_summary(high_group),
    }

    if (
        len(clean) < MIN_HELDOUT_EVENTS
        or len(low_group) < MIN_QUARTILE_EVENTS
        or len(high_group) < MIN_QUARTILE_EVENTS
    ):
        return "INSUFFICIENT", relation

    tf = relation["spearman_vs_target_first"]
    reach = relation["spearman_vs_target_reach"]
    mfe = relation["spearman_vs_mfe"]
    mae = relation["spearman_vs_mae"]
    if not all(isinstance(value, float) for value in (tf, reach, mfe, mae)):
        return "INSUFFICIENT", relation

    positive = tf > 0 and reach >= 0 and mfe >= 0 and mae <= 0
    negative = tf < 0 and reach <= 0 and mfe <= 0 and mae >= 0
    if positive and _quartile_better(relation["high_quartile"], relation["low_quartile"]):
        return "SUPPORT", relation
    if negative and _quartile_opposes(relation["high_quartile"], relation["low_quartile"]):
        return "OPPOSE", relation
    return "MIXED", relation


def run_test(
    *,
    m1_path: str | Path,
    anchor_events_path: str | Path,
    metadata_path: str | Path | None,
    report_path: str | Path,
    events_path: str | Path,
) -> dict[str, object]:
    m1 = load_ohlc_csv(m1_path)
    if "volume" not in m1.columns:
        raise ValueError("SW proxy experiment requires Dukascopy volume for active-minute filtering")
    source_m1_rows = len(m1)
    active_m1 = m1[m1["volume"] > 0].copy()
    h1 = resample_ohlc(active_m1, "H1")

    anchors = pd.read_csv(anchor_events_path)
    if "variant" in anchors.columns:
        anchors = anchors[anchors["variant"] == "EXACT_COMPLETION"].copy()
    anchors["anchor_known_at"] = pd.to_datetime(anchors["anchor_known_at"], utc=True)
    anchors = anchors.sort_values("anchor_known_at").drop_duplicates(
        subset=["anchor_known_at", "anchor_side"], keep="first"
    )

    failed_dates = _load_failed_dates(metadata_path)
    rows: list[dict[str, object]] = []
    skipped_insufficient_history = 0
    skipped_failed_lookback = 0

    for anchor in anchors.itertuples(index=False):
        known_at = pd.Timestamp(anchor.anchor_known_at)
        first_pat_bar_start = known_at - pd.Timedelta(hours=2)
        pre = h1[h1.index < first_pat_bar_start]

        for window_size in WINDOWS:
            if len(pre) < window_size:
                skipped_insufficient_history += 1
                continue
            history = pre.iloc[-window_size:]
            if _intersects_failed_date(history.index[0], first_pat_bar_start, failed_dates):
                skipped_failed_lookback += 1
                continue

            features = _sw_shape_features(history)
            rows.append(
                {
                    "split": str(anchor.split),
                    "anchor_side": str(anchor.anchor_side),
                    "anchor_known_at": known_at.isoformat(),
                    "window_h1_bars": window_size,
                    "history_start": history.index[0].isoformat(),
                    "history_end": history.index[-1].isoformat(),
                    **features,
                    "target_reached_anywhere": bool(anchor.target_reached_anywhere),
                    "first_hit": str(anchor.first_hit),
                    "mfe_points": float(anchor.mfe_points),
                    "mae_points": float(anchor.mae_points),
                }
            )

    events = pd.DataFrame(rows)
    target_events = Path(events_path)
    target_events.parent.mkdir(parents=True, exist_ok=True)
    events.to_csv(target_events, index=False)

    tests: dict[str, object] = {}
    decisions: dict[str, str] = {}
    for window_size in WINDOWS:
        window_rows = events[events["window_h1_bars"] == window_size]
        for feature in FEATURES:
            key = f"W{window_size}_{feature.upper()}"
            dev = window_rows[(window_rows["split"] == "DEV") & window_rows[feature].notna()]
            if dev.empty:
                decisions[key] = "INCONCLUSIVE"
                tests[key] = {"reason": "no DEV feature values"}
                continue

            low_threshold = float(dev[feature].quantile(0.25))
            high_threshold = float(dev[feature].quantile(0.75))
            split_results: dict[str, object] = {
                "dev_q25_low": low_threshold,
                "dev_q75_high": high_threshold,
            }
            heldout_states: list[str] = []
            for split_name in ("DEV", "VAL", "TEST"):
                group = window_rows[window_rows["split"] == split_name]
                state, relation = _relation_state(
                    group=group,
                    feature=feature,
                    low_threshold=low_threshold,
                    high_threshold=high_threshold,
                )
                split_results[split_name] = {"state": state, **relation}
                if split_name in {"VAL", "TEST"}:
                    heldout_states.append(state)

            if heldout_states == ["SUPPORT", "SUPPORT"]:
                decision = "SUPPORTED_POSITIVE_RELATION"
            elif heldout_states == ["OPPOSE", "OPPOSE"]:
                decision = "NOT_SUPPORTED_POSITIVE_RELATION"
            else:
                decision = "INCONCLUSIVE"
            decisions[key] = decision
            tests[key] = split_results

    report: dict[str, object] = {
        "research_status": "SW_PROXY_VARIANT_RELATION_COMPONENT_TEST_NOT_CANONICAL_SW",
        "research_question": (
            "Before an H1 PAT2 BODY research anchor, do simple oscillation/overlap proxies over "
            "6/12/24 active H1 bars show a stable positive relationship with the H1 1,000-point fresh-target outcome?"
        ),
        "source_m1": str(m1_path),
        "source_anchor_events": str(anchor_events_path),
        "source_metadata": str(metadata_path) if metadata_path is not None else None,
        "source_m1_rows": source_m1_rows,
        "active_positive_volume_m1_rows": len(active_m1),
        "unique_source_anchors": len(anchors),
        "measured_rows": len(events),
        "windows_h1_bars": list(WINDOWS),
        "features": list(FEATURES),
        "pre_anchor_boundary": "strictly before first PAT2 H1 candle: anchor_known_at - 2h",
        "failed_dates_excluded": sorted(value.isoformat() for value in failed_dates),
        "skipped_insufficient_history_window_rows": skipped_insufficient_history,
        "skipped_failed_date_lookback_window_rows": skipped_failed_lookback,
        "decisions": decisions,
        "tests": tests,
        "limitations": [
            "These are threshold-free shape proxies, not the canonical SW frame detector.",
            "No source-labeled SW truth set is used, so this experiment addresses outcome usefulness only.",
            "Exact SW completion, upper/lower frame, breakout and false-break rules remain unresolved.",
            "H1 PAT2 BODY is a research proxy, not a complete canonical SIG detector.",
            "Fresh-target symmetric 1,000-point measurement is a research control, not strategy win rate.",
            "A weak proxy result does not refute the teaching concept of a completed SW frame.",
        ],
    }
    Path(report_path).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--m1", required=True)
    parser.add_argument("--anchors", required=True)
    parser.add_argument("--metadata", default=None)
    parser.add_argument("--report", required=True)
    parser.add_argument("--events", required=True)
    args = parser.parse_args()
    report = run_test(
        m1_path=args.m1,
        anchor_events_path=args.anchors,
        metadata_path=args.metadata,
        report_path=args.report,
        events_path=args.events,
    )
    print(json.dumps(report["decisions"], indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
