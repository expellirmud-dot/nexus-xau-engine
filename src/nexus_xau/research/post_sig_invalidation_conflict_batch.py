from __future__ import annotations

import argparse
import json
from pathlib import Path

from nexus_xau.research.inherited_origin_context_batch import (
    KNOWN_PERIODS,
    discover_remaining_events_file,
)
from nexus_xau.research.path_remaining_daily_side_mtf_batch import discover_m1_file
from nexus_xau.research.post_sig_invalidation_conflict_scan import run as run_period


def cross_period_decision(period_states: list[str]) -> str:
    conflicts = period_states.count("CONFLICT_OBSERVED")
    evaluable = sum(
        state in {"CONFLICT_OBSERVED", "NO_CONFLICT_OBSERVED"}
        for state in period_states
    )
    if conflicts >= 2:
        return "REPLICATED_SOURCE_PARTIAL_CONFLICT_OBSERVED"
    if conflicts == 1:
        return "SOURCE_PARTIAL_CONFLICT_SINGLE_PERIOD"
    if evaluable > 0:
        return "NO_SOURCE_PARTIAL_CONFLICT_OBSERVED"
    return "NOT_TESTABLE_WITH_CURRENT_EVIDENCE"


def run_known_periods(
    *,
    m1_root: str | Path,
    results_root: str | Path,
    output_root: str | Path,
) -> dict[str, object]:
    output_root = Path(output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    periods: list[dict[str, object]] = []
    states: list[str] = []
    for period in KNOWN_PERIODS:
        m1_path = discover_m1_file(
            m1_root,
            start=period.start,
            end=period.end,
        )
        remaining_path = discover_remaining_events_file(
            results_root,
            start=period.start,
            end=period.end,
        )
        report_path = output_root / f"{period.label}_REPORT.json"
        scan_path = output_root / f"{period.label}_SCAN.csv"
        report = run_period(
            m1_path=m1_path,
            remaining_events_path=remaining_path,
            report_path=report_path,
            scan_path=scan_path,
            period_start=__import__("pandas").Timestamp(period.start, tz="UTC"),
            period_end=__import__("pandas").Timestamp(period.end, tz="UTC"),
        )
        summary = report["summary"]
        state = str(summary["period_state"])
        states.append(state)
        periods.append(
            {
                "label": period.label,
                "start": period.start,
                "end": period.end,
                "m1": str(m1_path),
                "remaining_events": str(remaining_path),
                "report": str(report_path),
                "scan": str(scan_path),
                "summary": summary,
            }
        )

    cross = cross_period_decision(states)
    result: dict[str, object] = {
        "research_status": "POST_SIG_SOURCE_PARTIAL_INVALIDATION_CONFLICT_MULTIPERIOD",
        "periods": periods,
        "period_states": states,
        "cross_period_decision": cross,
        "closure_rule_frozen_before_execution": (
            "conflict in >=2 periods => replicated source-partial conflict; exactly 1 => single-period conflict; "
            "zero conflicts with evaluable evidence => no source-partial conflict observed; otherwise not testable"
        ),
        "guardrails": [
            "No minimum conflict fraction is invented.",
            "No 200-point destruction threshold is used.",
            "This does not perform full origin replacement/re-anchoring.",
            "Outcome performance cannot upgrade source provenance.",
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
        default="results/POST_SIG_INVALIDATION_CONFLICT_SCAN",
    )
    args = parser.parse_args()
    summary = run_known_periods(
        m1_root=args.m1_root,
        results_root=args.results_root,
        output_root=args.output_root,
    )
    for period in summary["periods"]:
        print(period["label"], json.dumps(period["summary"], ensure_ascii=False))
    print(
        "CROSS-PERIOD",
        summary["cross_period_decision"],
        summary["period_states"],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
