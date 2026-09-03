from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

PROXIMITY_POINTS = 200.0
MIN_GROUP_SIZE = 20
SUPPORTED_TFS = ("H1", "H4")


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


def _better(near: dict[str, float | int | None], far: dict[str, float | int | None]) -> bool:
    n_tf = near["target_first_rate_resolved"]
    f_tf = far["target_first_rate_resolved"]
    n_reach = near["target_reach_rate_anywhere"]
    f_reach = far["target_reach_rate_anywhere"]
    if not all(isinstance(v, float) for v in (n_tf, f_tf, n_reach, f_reach)):
        return False
    return bool(n_tf > f_tf and n_reach >= f_reach)


def run_test(
    *, event_table_path: str | Path,
    report_path: str | Path,
) -> dict[str, object]:
    events = pd.read_csv(event_table_path)
    events = events[events["timeframe"].isin(SUPPORTED_TFS)].copy()
    summaries: list[dict[str, object]] = []
    decisions: dict[str, str] = {}

    for tf in SUPPORTED_TFS:
        checks: list[bool | None] = []
        for split_name in ("DEV", "VAL", "TEST"):
            g = events[(events["timeframe"] == tf) & (events["split"] == split_name)]
            near = g[g["absolute_distance_points"] <= PROXIMITY_POINTS]
            beyond = g[g["absolute_distance_points"] > PROXIMITY_POINTS]
            near_summary = _summary(near)
            beyond_summary = _summary(beyond)
            summaries.append(
                {
                    "timeframe": tf,
                    "split": split_name,
                    "all_events": len(g),
                    "within_200_points": near_summary,
                    "beyond_200_points": beyond_summary,
                }
            )
            if split_name in {"VAL", "TEST"}:
                if len(near) < MIN_GROUP_SIZE or len(beyond) < MIN_GROUP_SIZE:
                    checks.append(None)
                else:
                    checks.append(_better(near_summary, beyond_summary))

        if len(checks) != 2 or any(value is None for value in checks):
            decisions[tf] = "INCONCLUSIVE: at least one held-out group is below minimum sample size."
        elif all(checks):
            decisions[tf] = (
                "SUPPORTED: candidates within the source-backed 200-point Daily-Frame proximity "
                "outperform beyond-200 controls on both held-out splits by the frozen two-metric rule."
            )
        elif not any(checks):
            decisions[tf] = (
                "NOT_SUPPORTED: the <=200-point proximity rule does not improve both frozen metrics "
                "on either held-out split."
            )
        else:
            decisions[tf] = "INCONCLUSIVE: held-out splits disagree."

    if decisions and all(value.startswith("SUPPORTED") for value in decisions.values()):
        overall = "SUPPORTED_BOTH_TF"
    elif decisions and all(value.startswith("NOT_SUPPORTED") for value in decisions.values()):
        overall = "NOT_SUPPORTED_BOTH_TF"
    else:
        overall = "MIXED_OR_INCONCLUSIVE"

    report: dict[str, object] = {
        "research_question": (
            "Does the source-backed Daily-Frame entry proximity condition of <=200 project points "
            "improve H1/H4 PAT topology outcome behavior versus candidates beyond 200 points?"
        ),
        "research_status": "Q2B_SOURCE_BACKED_200PT_COMPONENT_TEST_NOT_SYSTEM_BACKTEST",
        "source_event_table": str(event_table_path),
        "proximity_points": PROXIMITY_POINTS,
        "minimum_group_size": MIN_GROUP_SIZE,
        "decision_rule": (
            "SUPPORTED per timeframe only if <=200 has higher resolved target-first rate and no-lower "
            "target-reach rate than >200 on BOTH VAL and TEST."
        ),
        "limitations": [
            "The <=200 rule is evidenced for the demonstrated Daily-Frame entry setup, not proven universal across all setup families.",
            "Underlying PAT events are topology candidates, not fully validated SIG labels.",
            "SW and inherited remaining-run state are excluded.",
            "This does not establish strategy win rate or a canonical SL.",
        ],
        "summaries": summaries,
        "timeframe_decisions": decisions,
        "overall_decision": overall,
    }
    Path(report_path).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--events", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()
    result = run_test(event_table_path=args.events, report_path=args.report)
    print(result["overall_decision"])
    print(json.dumps(result["timeframe_decisions"], ensure_ascii=False, indent=2))
    for row in result["summaries"]:
        if row["split"] in {"VAL", "TEST"}:
            print(json.dumps(row, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
