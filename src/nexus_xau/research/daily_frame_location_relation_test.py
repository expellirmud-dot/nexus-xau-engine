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


def _median(group: pd.DataFrame, col: str) -> float | None:
    if group.empty:
        return None
    return float(group[col].median())


def _summary(group: pd.DataFrame) -> dict[str, float | int | None]:
    return {
        "events": len(group),
        "target_first_rate_resolved": _target_first_rate(group),
        "target_reach_rate_anywhere": _rate(group, "target_reached_anywhere"),
        "mfe_median": _median(group, "mfe_project_points"),
        "mae_median": _median(group, "mae_project_points"),
    }


def _better(candidate: dict[str, float | int | None], control: dict[str, float | int | None]) -> bool:
    c_tf = candidate["target_first_rate_resolved"]
    k_tf = control["target_first_rate_resolved"]
    c_reach = candidate["target_reach_rate_anywhere"]
    k_reach = control["target_reach_rate_anywhere"]
    if not all(isinstance(v, float) for v in (c_tf, k_tf, c_reach, k_reach)):
        return False
    return bool(c_tf > k_tf and c_reach >= k_reach)


def run_test(
    *,
    m1_path: str | Path,
    hits_path: str | Path,
    outcomes_path: str | Path,
    report_path: str | Path,
    events_path: str | Path,
) -> dict[str, object]:
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
        daily_frame = build_mae_pla_frame_candidates(open_0700)

        if side == "BUY":
            pattern_location_price = float(pattern["low"].min())
            expected_lines = [c.lower_price for c in daily_frame.candidates]
            line = min(expected_lines, key=lambda p: abs(pattern_location_price - p))
            signed_valid_side_points = (pattern_location_price - line) / PROJECT_POINT_SIZE
            expected_location = "SUPPORT"
        elif side == "SELL":
            pattern_location_price = float(pattern["high"].max())
            expected_lines = [c.upper_price for c in daily_frame.candidates]
            line = min(expected_lines, key=lambda p: abs(pattern_location_price - p))
            signed_valid_side_points = (line - pattern_location_price) / PROJECT_POINT_SIZE
            expected_location = "RESISTANCE"
        else:
            continue

        absolute_distance_points = abs(signed_valid_side_points)
        match = outcomes[
            (outcomes["timeframe"] == tf)
            & (outcomes["kind"] == str(hit.kind))
            & (outcomes["side"] == side)
            & (outcomes["pattern_window_end_utc"] == end)
        ]
        if len(match) != 1:
            continue
        out = match.iloc[0]

        rows.append(
            {
                "split": _split(end),
                "timeframe": tf,
                "kind": str(hit.kind),
                "side": side,
                "expected_location": expected_location,
                "pattern_window_start_utc": start.isoformat(),
                "pattern_window_end_utc": end.isoformat(),
                "open_0700_price": open_0700,
                "pattern_location_price": pattern_location_price,
                "daily_frame_line_price": line,
                "signed_valid_side_distance_points": float(signed_valid_side_points),
                "absolute_distance_points": float(absolute_distance_points),
                "target_reached_anywhere": bool(out["target_reached_anywhere"]),
                "symmetric_first_hit": str(out["symmetric_first_hit"]),
                "mfe_project_points": float(out["mfe_project_points"]),
                "mae_project_points": float(out["mae_project_points"]),
            }
        )

    events = pd.DataFrame(rows)
    Path(events_path).parent.mkdir(parents=True, exist_ok=True)

    thresholds: dict[str, dict[str, float]] = {}
    summaries: list[dict[str, object]] = []
    decisions: dict[str, str] = {}

    for tf in SUPPORTED_TFS:
        dev = events[(events["split"] == "DEV") & (events["timeframe"] == tf)]
        if dev.empty:
            continue
        near_max = float(dev["absolute_distance_points"].quantile(0.25))
        far_min = float(dev["absolute_distance_points"].quantile(0.75))
        thresholds[tf] = {
            "dev_q25_near_max_points": near_max,
            "dev_q75_far_min_points": far_min,
        }

        tf_checks: list[bool | None] = []
        for split_name in ("DEV", "VAL", "TEST"):
            g = events[(events["split"] == split_name) & (events["timeframe"] == tf)].copy()
            g["location_relation"] = "MID_CONTROL"
            g.loc[g["absolute_distance_points"] >= far_min, "location_relation"] = "FAR_CONTROL"
            near = g["absolute_distance_points"] <= near_max
            expected_side = g["signed_valid_side_distance_points"] >= 0
            g.loc[near & expected_side, "location_relation"] = "EXPECTED_SIDE_NEAR"
            g.loc[near & ~expected_side, "location_relation"] = "CROSSED_SIDE_NEAR"
            events.loc[g.index, "location_relation"] = g["location_relation"]

            expected = g[g["location_relation"] == "EXPECTED_SIDE_NEAR"]
            crossed = g[g["location_relation"] == "CROSSED_SIDE_NEAR"]
            far = g[g["location_relation"] == "FAR_CONTROL"]
            expected_summary = _summary(expected)
            crossed_summary = _summary(crossed)
            far_summary = _summary(far)

            summaries.append(
                {
                    "timeframe": tf,
                    "split": split_name,
                    "all_events": len(g),
                    "expected_side_near": expected_summary,
                    "crossed_side_near": crossed_summary,
                    "far_control": far_summary,
                }
            )

            if split_name in {"VAL", "TEST"}:
                enough_expected = len(expected) >= 10
                enough_crossed = len(crossed) >= 10
                enough_far = len(far) >= 10
                if not (enough_expected and enough_crossed and enough_far):
                    tf_checks.append(None)
                    continue
                tf_checks.append(
                    _better(expected_summary, crossed_summary)
                    and _better(expected_summary, far_summary)
                )

        if len(tf_checks) != 2:
            decisions[tf] = "INCONCLUSIVE: held-out checks were not both available."
        elif any(value is None for value in tf_checks):
            decisions[tf] = "INCONCLUSIVE: at least one held-out comparison group is below the minimum sample size."
        elif all(tf_checks):
            decisions[tf] = (
                "SUPPORTED: expected-side near-frame candidates outperform both crossed-side near "
                "and far controls on both held-out splits by the frozen two-metric rule."
            )
        elif not any(tf_checks):
            decisions[tf] = (
                "NOT_SUPPORTED: the expected-side near-frame relation does not beat both controls "
                "on either held-out split under the frozen rule."
            )
        else:
            decisions[tf] = "INCONCLUSIVE: held-out splits disagree."

    events.to_csv(events_path, index=False)

    if decisions and all(value.startswith("SUPPORTED") for value in decisions.values()):
        overall = "SUPPORTED_BOTH_TF"
    elif decisions and all(value.startswith("NOT_SUPPORTED") for value in decisions.values()):
        overall = "NOT_SUPPORTED_BOTH_TF"
    else:
        overall = "MIXED_OR_INCONCLUSIVE"

    report: dict[str, object] = {
        "research_question": (
            "Within H1/H4 PAT topology candidates, does direction-correct side relation to the 07:00 "
            "Daily Frame add information beyond simple proximity?"
        ),
        "research_status": "Q2_LOCATION_RELATION_COMPONENT_TEST_NOT_CANONICAL_LOCATION_RULE",
        "source_m1": str(m1_path),
        "source_hits": str(hits_path),
        "source_outcomes": str(outcomes_path),
        "time_mapping": "07:00 Asia/Bangkok = 00:00 UTC",
        "representation": (
            "BUY uses PAT-window low relative to Daily-Frame lower/support line; SELL uses PAT-window high "
            "relative to Daily-Frame upper/resistance line. Positive signed distance means the PAT extreme "
            "remains on the expected/inside side of the line; negative means the extreme crosses beyond it."
        ),
        "bucket_policy": (
            "Near and far cutoffs are DEV q25/q75 of absolute frame distance, frozen before VAL/TEST. "
            "EXPECTED_SIDE_NEAR and CROSSED_SIDE_NEAR are research relations, not canonical touch/invalidation rules."
        ),
        "minimum_group_size": 10,
        "decision_rule": (
            "Per timeframe, SUPPORTED only if EXPECTED_SIDE_NEAR has higher resolved target-first rate "
            "and no-lower target-reach rate than BOTH CROSSED_SIDE_NEAR and FAR_CONTROL on BOTH VAL and TEST."
        ),
        "limitations": [
            "PAT topology candidates are not fully validated PA/SIG labels.",
            "PAT-window wick extremes are used for this Q2 representation; body/touch geometry is not solved.",
            "A small wick penetration can still be valid in the teaching system, so CROSSED_SIDE_NEAR is not called invalid location.",
            "SW and inherited remaining-run state are intentionally excluded.",
            "The symmetric adverse barrier in the source outcome table is a research control, not a canonical SL.",
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--m1", required=True)
    parser.add_argument("--hits", required=True)
    parser.add_argument("--outcomes", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--events", required=True)
    args = parser.parse_args()
    result = run_test(
        m1_path=args.m1,
        hits_path=args.hits,
        outcomes_path=args.outcomes,
        report_path=args.report,
        events_path=args.events,
    )
    print(result["overall_decision"])
    print(json.dumps(result["timeframe_decisions"], ensure_ascii=False, indent=2))
    for row in result["summaries"]:
        if row["split"] in {"VAL", "TEST"}:
            print(json.dumps(row, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
