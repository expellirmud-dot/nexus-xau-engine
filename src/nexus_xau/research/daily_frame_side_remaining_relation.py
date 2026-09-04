from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

MIN_GROUP = 10


def _summary(group: pd.DataFrame) -> dict[str, float | int | None]:
    resolved = group[group["path_remaining_first_hit"].isin(["TARGET_FIRST", "STOP_FIRST"])]
    return {
        "events": len(group),
        "resolved_events": len(resolved),
        "target_first_rate_resolved": (
            float((resolved["path_remaining_first_hit"] == "TARGET_FIRST").mean())
            if not resolved.empty
            else None
        ),
        "target_reach_rate": float(group["path_remaining_reached"].mean()) if not group.empty else None,
        "fresh_mfe_median": (
            float(group["fresh_mfe_points"].median()) if not group.empty else None
        ),
        "fresh_mae_median": (
            float(group["fresh_mae_points"].median()) if not group.empty else None
        ),
    }


def _state(expected: dict[str, object], crossed: dict[str, object]) -> str:
    if int(expected["events"]) < MIN_GROUP or int(crossed["events"]) < MIN_GROUP:
        return "INSUFFICIENT"
    etf = expected["target_first_rate_resolved"]
    ctf = crossed["target_first_rate_resolved"]
    er = expected["target_reach_rate"]
    cr = crossed["target_reach_rate"]
    if not all(isinstance(v, float) for v in (etf, ctf, er, cr)):
        return "INSUFFICIENT"
    if etf > ctf and er >= cr:
        return "SUPPORT"
    if etf < ctf and er <= cr:
        return "OPPOSE"
    return "MIXED"


def run(*, interaction_events_path: str | Path, report_path: str | Path) -> dict[str, object]:
    events = pd.read_csv(interaction_events_path)
    expected = events[events["signed_valid_side_distance_points"] >= 0]
    crossed = events[events["signed_valid_side_distance_points"] < 0]
    expected_summary = _summary(expected)
    crossed_summary = _summary(crossed)
    report: dict[str, object] = {
        "research_status": "DAILY_FRAME_DIRECTIONAL_SIDE_X_PATH_REMAINING_EXPLORATORY",
        "source_interaction_events": str(interaction_events_path),
        "groups": {
            "EXPECTED_SIDE": expected_summary,
            "CROSSED_SIDE": crossed_summary,
        },
        "period_state": _state(expected_summary, crossed_summary),
        "minimum_group": MIN_GROUP,
        "guard": (
            "Generated after the <=200 interaction showed later-period sample scarcity. "
            "This is exploratory diagnostic evidence, not fresh confirmation and not a canonical penetration rule."
        ),
    }
    Path(report_path).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--interaction-events", required=True)
    p.add_argument("--report", required=True)
    a = p.parse_args()
    result = run(interaction_events_path=a.interaction_events, report_path=a.report)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
