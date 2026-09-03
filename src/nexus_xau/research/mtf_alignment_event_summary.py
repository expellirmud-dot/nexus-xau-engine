from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from nexus_xau.research.mtf_alignment_variant_relation_test import (
    LOOKBACK_VARIANTS,
    _group_summary,
    _heldout_relation_state,
    _relation_summary,
)


def summarize_events(*, events_path: str | Path, report_path: str | Path) -> dict[str, object]:
    events = pd.read_csv(events_path)
    required = {
        "split",
        "variant",
        "alignment_count",
        "target_reached_anywhere",
        "first_hit",
        "mfe_points",
        "mae_points",
    }
    missing = required.difference(events.columns)
    if missing:
        raise ValueError(f"events table missing columns: {sorted(missing)}")

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
                str(int(count)): _group_summary(group[group["alignment_count"] == count])
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

    measured_anchors = int(events["anchor_known_at"].nunique()) if "anchor_known_at" in events.columns else None
    report: dict[str, object] = {
        "research_status": "MTF_ALIGNMENT_VARIANT_RELATION_EVENT_TABLE_SUMMARY",
        "source_events": str(events_path),
        "measured_event_rows": len(events),
        "measured_unique_anchors": measured_anchors,
        "variants": list(LOOKBACK_VARIANTS),
        "decisions": decisions,
        "variant_reports": variant_reports,
        "interpretation_guard": [
            "PAT2 BODY is a research proxy, not canonical full PA.",
            "Fresh-target symmetric 1,000-point outcome is a research control, not strategy win rate.",
            "Do not choose a production minimum aligned-TF count from these results alone.",
            "A weak proxy result does not refute the user-direct semantic that more true PA alignment is stronger.",
        ],
    }
    target = Path(report_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--events", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()
    report = summarize_events(events_path=args.events, report_path=args.report)
    print(json.dumps(report["decisions"], ensure_ascii=False, indent=2))
    for variant, splits in report["variant_reports"].items():
        for split_name in ("VAL", "TEST"):
            relation = splits[split_name]["relation"]
            print(
                variant,
                split_name,
                splits[split_name]["heldout_relation_state"],
                json.dumps(relation, ensure_ascii=False),
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
