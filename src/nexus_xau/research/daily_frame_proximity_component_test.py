from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from nexus_xau.data.csv_loader import load_ohlc_csv
from nexus_xau.data.resample import resample_ohlc
from nexus_xau.engine.mae_pla_frame import build_mae_pla_frame_candidates

PROJECT_POINT_SIZE = 0.01
SUPPORTED_TFS = ("H1", "H4")


def _split(ts: pd.Timestamp) -> str:
    if ts < pd.Timestamp("2026-07-01", tz="UTC"):
        return "DEV"
    if ts < pd.Timestamp("2026-08-01", tz="UTC"):
        return "VAL"
    return "TEST"


def _rate(group: pd.DataFrame, col: str) -> float | None:
    if group.empty:
        return None
    return float(group[col].mean())


def _target_first_rate(group: pd.DataFrame) -> float | None:
    resolved = group[group["symmetric_first_hit"].isin(["TARGET_FIRST", "STOP_FIRST"])]
    if resolved.empty:
        return None
    return float((resolved["symmetric_first_hit"] == "TARGET_FIRST").mean())


def run_test(*, m1_path: str | Path, hits_path: str | Path, outcomes_path: str | Path,
             report_path: str | Path, events_path: str | Path) -> dict[str, object]:
    m1 = load_ohlc_csv(m1_path)
    hits = pd.read_csv(hits_path)
    hits = hits[hits["timeframe"].isin(SUPPORTED_TFS)].copy()
    hits["window_start_utc"] = pd.to_datetime(hits["window_start_utc"], utc=True)
    hits["window_end_utc"] = pd.to_datetime(hits["window_end_utc"], utc=True)

    outcomes = pd.read_csv(outcomes_path)
    outcomes = outcomes[outcomes["timeframe"].isin(SUPPORTED_TFS)].copy()
    outcomes["pattern_window_end_utc"] = pd.to_datetime(outcomes["pattern_window_end_utc"], utc=True)

    frames = {tf: resample_ohlc(m1, tf) for tf in SUPPORTED_TFS}
    rows: list[dict[str, object]] = []

    for hit in hits.itertuples(index=False):
        tf = str(hit.timeframe)
        side = str(hit.side).upper()
        start = pd.Timestamp(hit.window_start_utc)
        end = pd.Timestamp(hit.window_end_utc)
        frame = frames[tf]
        pattern = frame.loc[(frame.index >= start) & (frame.index <= end)]
        if pattern.empty:
            continue

        day_start = end.normalize()
        if day_start not in m1.index:
            continue
        open_0700 = float(m1.loc[day_start, "open"])
        candidate_set = build_mae_pla_frame_candidates(open_0700)

        if side == "BUY":
            pattern_location_price = float(pattern["low"].min())
            frame_prices = [c.lower_price for c in candidate_set.candidates]
        elif side == "SELL":
            pattern_location_price = float(pattern["high"].max())
            frame_prices = [c.upper_price for c in candidate_set.candidates]
        else:
            continue

        nearest_frame_price = min(frame_prices, key=lambda p: abs(pattern_location_price - p))
        distance_points = abs(pattern_location_price - nearest_frame_price) / PROJECT_POINT_SIZE

        match = outcomes[
            (outcomes["timeframe"] == tf)
            & (outcomes["kind"] == str(hit.kind))
            & (outcomes["side"] == side)
            & (outcomes["pattern_window_end_utc"] == end)
        ]
        if len(match) != 1:
            continue
        out = match.iloc[0]

        rows.append({
            "split": _split(end),
            "timeframe": tf,
            "kind": str(hit.kind),
            "side": side,
            "pattern_window_start_utc": start.isoformat(),
            "pattern_window_end_utc": end.isoformat(),
            "open_0700_price": open_0700,
            "pattern_location_price": pattern_location_price,
            "expected_daily_frame_price": nearest_frame_price,
            "distance_to_expected_daily_frame_points": float(distance_points),
            "target_reached_anywhere": bool(out["target_reached_anywhere"]),
            "symmetric_first_hit": str(out["symmetric_first_hit"]),
            "mfe_project_points": float(out["mfe_project_points"]),
            "mae_project_points": float(out["mae_project_points"]),
        })

    events = pd.DataFrame(rows)
    Path(events_path).parent.mkdir(parents=True, exist_ok=True)
    events.to_csv(events_path, index=False)

    thresholds: dict[str, dict[str, float]] = {}
    summaries: list[dict[str, object]] = []
    decisions: dict[str, str] = {}

    for tf in SUPPORTED_TFS:
        dev = events[(events["split"] == "DEV") & (events["timeframe"] == tf)]
        if dev.empty:
            continue
        q25 = float(dev["distance_to_expected_daily_frame_points"].quantile(0.25))
        q75 = float(dev["distance_to_expected_daily_frame_points"].quantile(0.75))
        thresholds[tf] = {"dev_q25_near_max_points": q25, "dev_q75_far_min_points": q75}

        split_checks: list[tuple[bool, bool]] = []
        for split_name in ("DEV", "VAL", "TEST"):
            g = events[(events["split"] == split_name) & (events["timeframe"] == tf)]
            near = g[g["distance_to_expected_daily_frame_points"] <= q25]
            far = g[g["distance_to_expected_daily_frame_points"] >= q75]
            near_tf = _target_first_rate(near)
            far_tf = _target_first_rate(far)
            near_reach = _rate(near, "target_reached_anywhere")
            far_reach = _rate(far, "target_reached_anywhere")
            summaries.append({
                "timeframe": tf,
                "split": split_name,
                "events": len(g),
                "near_events": len(near),
                "far_events": len(far),
                "near_target_first_rate_resolved": near_tf,
                "far_target_first_rate_resolved": far_tf,
                "near_target_reach_rate_anywhere": near_reach,
                "far_target_reach_rate_anywhere": far_reach,
                "near_mfe_median": float(near["mfe_project_points"].median()) if not near.empty else None,
                "far_mfe_median": float(far["mfe_project_points"].median()) if not far.empty else None,
                "near_mae_median": float(near["mae_project_points"].median()) if not near.empty else None,
                "far_mae_median": float(far["mae_project_points"].median()) if not far.empty else None,
            })
            if split_name in {"VAL", "TEST"}:
                tf_better = near_tf is not None and far_tf is not None and near_tf > far_tf
                reach_better = near_reach is not None and far_reach is not None and near_reach >= far_reach
                split_checks.append((tf_better, reach_better))

        if len(split_checks) == 2 and all(a and b for a, b in split_checks):
            decisions[tf] = "SUPPORTED: closer-to-daily-frame candidates outperform far candidates on both held-out splits by pre-registered directional criteria."
        elif len(split_checks) == 2 and all((not a) and (not b) for a, b in split_checks):
            decisions[tf] = "NOT_SUPPORTED: closer-to-daily-frame candidates do not outperform far candidates on either held-out split."
        else:
            decisions[tf] = "INCONCLUSIVE_OR_MIXED: held-out splits/metrics do not agree."

    overall = (
        "SUPPORTED_BOTH_TF" if decisions and all(v.startswith("SUPPORTED") for v in decisions.values())
        else "NOT_SUPPORTED_BOTH_TF" if decisions and all(v.startswith("NOT_SUPPORTED") for v in decisions.values())
        else "MIXED_OR_INCONCLUSIVE"
    )

    report = {
        "research_question": "Does proximity to the direction-correct 07:00 Daily Frame add measurable directional information to H1/H4 PAT topology candidates?",
        "research_status": "COMPONENT_TEST_NOT_SYSTEM_BACKTEST",
        "source_m1": str(m1_path),
        "source_hits": str(hits_path),
        "source_outcomes": str(outcomes_path),
        "time_mapping": "07:00 Asia/Bangkok = 00:00 UTC (project-owner confirmed interpretation)",
        "location_measure": "BUY uses PAT-window low distance to Daily-Frame lower/support line; SELL uses PAT-window high distance to Daily-Frame upper/resistance line.",
        "threshold_policy": "Near/far cutoffs are DEV q25/q75 only, then frozen and applied to VAL/TEST. They are analysis buckets, not trading thresholds.",
        "decision_rule": "Per timeframe: SUPPORTED only if near has higher symmetric target-first rate and no-lower target-reach rate than far on BOTH VAL and TEST. Mixed results => inconclusive.",
        "limitations": [
            "PAT topology candidates are not fully validated SIG labels.",
            "SW state and remaining-run state are intentionally excluded from this first component test.",
            "Symmetric first-hit uses equal favorable/adverse barriers and is not a canonical SL/win-rate definition.",
            "This test answers only whether Daily-Frame proximity adds information to the candidate set."
        ],
        "measured_events": len(events),
        "thresholds_from_dev": thresholds,
        "summaries": summaries,
        "timeframe_decisions": decisions,
        "overall_decision": overall,
    }
    Path(report_path).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--m1", required=True)
    p.add_argument("--hits", required=True)
    p.add_argument("--outcomes", required=True)
    p.add_argument("--report", required=True)
    p.add_argument("--events", required=True)
    args = p.parse_args()
    result = run_test(m1_path=args.m1, hits_path=args.hits, outcomes_path=args.outcomes,
                      report_path=args.report, events_path=args.events)
    print(result["overall_decision"])
    print(json.dumps(result["timeframe_decisions"], ensure_ascii=False, indent=2))
    for row in result["summaries"]:
        if row["split"] in {"VAL", "TEST"}:
            print(row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
