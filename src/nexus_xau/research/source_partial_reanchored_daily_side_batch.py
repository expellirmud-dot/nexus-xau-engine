from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from nexus_xau.research.daily_frame_remaining_run_interaction import (
    run as run_daily_interaction,
)
from nexus_xau.research.daily_frame_side_remaining_relation import run as run_daily_side
from nexus_xau.research.inherited_origin_context_batch import KNOWN_PERIODS, _discover_table
from nexus_xau.research.path_remaining_daily_side_mtf_batch import discover_m1_file
from nexus_xau.research.source_partial_reanchored_remaining_run import (
    REQUIRED_PARENT_COLUMNS,
    run as run_reanchor,
)


def discover_parent_remaining_events(
    root: str | Path,
    *,
    start: str,
    end: str,
) -> Path:
    return _discover_table(
        root,
        required_columns=set(REQUIRED_PARENT_COLUMNS),
        excluded_columns={
            "origin_age_hours",
            "frame_side",
            "reanchor_impact",
            "source_partial_selected",
        },
        start=start,
        end=end,
        label="legacy Remaining-Run parent event",
    )


def cross_period_decision(states: list[str]) -> str:
    support = states.count("SUPPORT")
    oppose = states.count("OPPOSE")
    if support >= 2 and oppose == 0:
        return "SUPPORTED_AFTER_SOURCE_PARTIAL_REANCHOR"
    if oppose >= 2:
        return "NOT_SUPPORTED_AFTER_SOURCE_PARTIAL_REANCHOR"
    if support > 0 and oppose > 0:
        return "NOT_STABLE_AFTER_SOURCE_PARTIAL_REANCHOR"
    return "INCONCLUSIVE_AFTER_SOURCE_PARTIAL_REANCHOR"


def _utc_day(value: str) -> pd.Timestamp:
    return pd.Timestamp(value, tz="UTC")


def run_known_periods(
    *,
    m1_root: str | Path,
    results_root: str | Path,
    output_root: str | Path,
) -> dict[str, object]:
    output_root = Path(output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    periods: list[dict[str, object]] = []
    side_states: list[str] = []
    for period in KNOWN_PERIODS:
        m1_path = discover_m1_file(m1_root, start=period.start, end=period.end)
        parent_path = discover_parent_remaining_events(
            results_root,
            start=period.start,
            end=period.end,
        )

        reanchor_report_path = output_root / f"{period.label}_REANCHORED_REPORT.json"
        reanchor_events_path = output_root / f"{period.label}_REANCHORED_EVENTS.csv"
        reanchor_report = run_reanchor(
            m1_path=m1_path,
            parent_events_path=parent_path,
            report_path=reanchor_report_path,
            events_path=reanchor_events_path,
            period_start=_utc_day(period.start),
            period_end=_utc_day(period.end),
        )

        daily_report_path = output_root / f"{period.label}_DAILY_INTERACTION_REPORT.json"
        daily_events_path = output_root / f"{period.label}_DAILY_INTERACTION_EVENTS.csv"
        run_daily_interaction(
            m1_path=m1_path,
            remaining_events_path=reanchor_events_path,
            report_path=daily_report_path,
            events_path=daily_events_path,
        )

        side_report_path = output_root / f"{period.label}_DAILY_SIDE_REPORT.json"
        side_report = run_daily_side(
            interaction_events_path=daily_events_path,
            report_path=side_report_path,
        )
        side_state = str(side_report["period_state"])
        side_states.append(side_state)

        periods.append(
            {
                "label": period.label,
                "start": period.start,
                "end": period.end,
                "m1": str(m1_path),
                "legacy_parent_events": str(parent_path),
                "reanchored_report": str(reanchor_report_path),
                "reanchored_events": str(reanchor_events_path),
                "daily_interaction_report": str(daily_report_path),
                "daily_interaction_events": str(daily_events_path),
                "daily_side_report": str(side_report_path),
                "reanchor_summary": reanchor_report["summary"],
                "daily_side_state": side_state,
                "daily_side_groups": side_report["groups"],
            }
        )

    result: dict[str, object] = {
        "research_status": "SOURCE_PARTIAL_REANCHORED_DAILY_SIDE_MULTIPERIOD",
        "periods": periods,
        "daily_side_period_states": side_states,
        "cross_period_decision": cross_period_decision(side_states),
        "closure_rule_frozen_before_execution": (
            ">=2 SUPPORT and no OPPOSE -> supported after source-partial re-anchor; "
            ">=2 OPPOSE -> not supported; SUPPORT+OPPOSE -> not stable; otherwise inconclusive"
        ),
        "guardrails": [
            "Legacy results remain preserved as historical checkpoints.",
            "No 200-point destruction buffer is used.",
            "No age or expiry threshold is introduced.",
            "H1 PAT2 BODY and PATH_REMAINING remain research representations.",
            "Historical outcomes cannot identify instructor intent.",
        ],
    }
    (output_root / "CROSS_PERIOD_SUMMARY.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--m1-root", default="data/raw/dukascopy")
    parser.add_argument("--results-root", default="results")
    parser.add_argument(
        "--output-root",
        default="results/SOURCE_PARTIAL_REANCHORED_REMAINING_RUN",
    )
    args = parser.parse_args()
    summary = run_known_periods(
        m1_root=args.m1_root,
        results_root=args.results_root,
        output_root=args.output_root,
    )
    for period in summary["periods"]:
        print(
            period["label"],
            "REANCHOR",
            json.dumps(period["reanchor_summary"], ensure_ascii=False),
        )
        print(
            period["label"],
            "DAILY_SIDE",
            period["daily_side_state"],
            json.dumps(period["daily_side_groups"], ensure_ascii=False),
        )
    print(
        "CROSS-PERIOD",
        summary["cross_period_decision"],
        summary["daily_side_period_states"],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
