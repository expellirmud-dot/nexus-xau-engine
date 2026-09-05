from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from nexus_xau.research.inherited_origin_context_relation import (
    REQUIRED_DAILY_COLUMNS,
    REQUIRED_REMAINING_COLUMNS,
)
from nexus_xau.research.inherited_origin_context_relation import (
    run as run_period,
)


@dataclass(frozen=True, slots=True)
class PeriodSpec:
    label: str
    start: str
    end: str


KNOWN_PERIODS = (
    PeriodSpec("DISCOVERY_2022_09_TO_2023_03", "2022-09-01", "2023-03-31"),
    PeriodSpec("LATER_2024_09_TO_2024_11", "2024-09-01", "2024-11-30"),
    PeriodSpec("LATER_2025_09_TO_2025_11", "2025-09-01", "2025-11-30"),
)


def _utc_day(value: str) -> pd.Timestamp:
    return pd.Timestamp(value, tz="UTC")


def _candidate_stats(
    path: Path,
    *,
    required_columns: set[str],
    excluded_columns: set[str],
    start: pd.Timestamp,
    end: pd.Timestamp,
) -> tuple[int, int] | None:
    try:
        header = pd.read_csv(path, nrows=0)
    except (OSError, UnicodeDecodeError, pd.errors.EmptyDataError):
        return None
    columns = set(header.columns)
    if not required_columns.issubset(columns):
        return None
    if excluded_columns.intersection(columns):
        return None

    try:
        raw = pd.read_csv(path, usecols=["candidate_known_at"])
    except (ValueError, OSError, pd.errors.EmptyDataError):
        return None
    known_at = pd.to_datetime(raw["candidate_known_at"], utc=True, errors="coerce").dropna()
    if known_at.empty:
        return None

    end_exclusive = end + pd.Timedelta(days=1)
    inside = int(((known_at >= start) & (known_at < end_exclusive)).sum())
    if inside == 0:
        return None
    outside = int(len(known_at) - inside)
    return inside, outside


def _discover_table(
    root: str | Path,
    *,
    required_columns: set[str],
    excluded_columns: set[str],
    start: str,
    end: str,
    label: str,
) -> Path:
    root = Path(root)
    target_start = _utc_day(start)
    target_end = _utc_day(end)
    candidates: list[tuple[int, int, str, Path]] = []
    for path in root.rglob("*.csv"):
        stats = _candidate_stats(
            path,
            required_columns=required_columns,
            excluded_columns=excluded_columns,
            start=target_start,
            end=target_end,
        )
        if stats is None:
            continue
        inside, outside = stats
        candidates.append((outside, -inside, str(path), path))

    if not candidates:
        raise FileNotFoundError(
            f"No {label} CSV under {root} contains events for {start} through {end}."
        )
    candidates.sort(key=lambda item: (item[0], item[1], item[2]))
    return candidates[0][3]


def discover_remaining_events_file(
    root: str | Path,
    *,
    start: str,
    end: str,
) -> Path:
    return _discover_table(
        root,
        required_columns=set(REQUIRED_REMAINING_COLUMNS),
        excluded_columns={"origin_age_hours", "frame_side"},
        start=start,
        end=end,
        label="Remaining-Run parent event",
    )


def discover_daily_events_file(
    root: str | Path,
    *,
    start: str,
    end: str,
) -> Path:
    return _discover_table(
        root,
        required_columns=set(REQUIRED_DAILY_COLUMNS),
        excluded_columns={"alignment_count", "variant", "origin_age_hours"},
        start=start,
        end=end,
        label="Daily-Frame interaction parent event",
    )


def replicated_direction(
    states: list[str],
    *,
    direction_a: str,
    direction_b: str,
) -> str:
    count_a = states.count(direction_a)
    count_b = states.count(direction_b)
    if count_a >= 2 and count_b == 0:
        return f"REPLICATED_RESEARCH_RELATION::{direction_a}"
    if count_b >= 2 and count_a == 0:
        return f"REPLICATED_RESEARCH_RELATION::{direction_b}"
    if count_a > 0 and count_b > 0:
        return "NOT_STABLE_ACROSS_PERIODS"
    return "INCONCLUSIVE"


def run_known_periods(
    *,
    results_root: str | Path,
    output_root: str | Path,
) -> dict[str, object]:
    output_root = Path(output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    periods: list[dict[str, object]] = []
    for period in KNOWN_PERIODS:
        remaining_path = discover_remaining_events_file(
            results_root,
            start=period.start,
            end=period.end,
        )
        daily_path = discover_daily_events_file(
            results_root,
            start=period.start,
            end=period.end,
        )
        report_path = output_root / f"{period.label}_REPORT.json"
        events_path = output_root / f"{period.label}_EVENTS.csv"
        report = run_period(
            remaining_events_path=remaining_path,
            daily_events_path=daily_path,
            report_path=report_path,
            events_path=events_path,
            period_start=_utc_day(period.start),
            period_end=_utc_day(period.end),
        )
        expected = report["summary"]["side_reports"]["EXPECTED_SIDE"]
        cycle = report["summary"]["expected_side_cycle_comparison"]
        states = {
            "origin_age": expected["origin_age"]["state"],
            "consumed_run_ratio_at_entry": expected["consumed_run_ratio_at_entry"]["state"],
            "origin_cycle_group": cycle["state"],
        }
        periods.append(
            {
                "label": period.label,
                "start": period.start,
                "end": period.end,
                "remaining_events": str(remaining_path),
                "daily_events": str(daily_path),
                "report": str(report_path),
                "events": str(events_path),
                "expected_side_states": states,
            }
        )

    age_states = [str(period["expected_side_states"]["origin_age"]) for period in periods]
    consumed_states = [
        str(period["expected_side_states"]["consumed_run_ratio_at_entry"])
        for period in periods
    ]
    cycle_states = [
        str(period["expected_side_states"]["origin_cycle_group"])
        for period in periods
    ]

    cross = {
        "origin_age": {
            "period_states": age_states,
            "decision": replicated_direction(
                age_states,
                direction_a="YOUNGER_ORIGIN_FAVORED",
                direction_b="OLDER_ORIGIN_FAVORED",
            ),
        },
        "consumed_run_ratio_at_entry": {
            "period_states": consumed_states,
            "decision": replicated_direction(
                consumed_states,
                direction_a="MORE_CONSUMED_FAVORED",
                direction_b="LESS_CONSUMED_FAVORED",
            ),
        },
        "origin_cycle_group": {
            "period_states": cycle_states,
            "decision": replicated_direction(
                cycle_states,
                direction_a="PREVIOUS_24H_FAVORED",
                direction_b="OLDER_CYCLE_FAVORED",
            ),
        },
    }

    summary: dict[str, object] = {
        "research_status": "INHERITED_ORIGIN_CONTEXT_X_DAILY_SIDE_MULTIPERIOD",
        "periods": periods,
        "cross_period": cross,
        "closure_rule_frozen_before_execution": (
            "Same directional state in >=2 periods with no opposite state -> replicated research relation; "
            "both opposite directions observed -> not stable; otherwise inconclusive."
        ),
        "primary_outcomes": "fixed fresh H1 1000-point control",
        "guardrails": [
            "No age or consumed-run threshold is selected.",
            "24-hour cycle grouping is not a canonical expiry rule.",
            "PATH_REMAINING and ORIGIN_TARGET_LEVEL remain secondary comparators.",
            "Historical outcomes cannot identify instructor intent.",
        ],
    }
    summary_path = output_root / "CROSS_PERIOD_SUMMARY.json"
    summary_path.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-root", default="results")
    parser.add_argument(
        "--output-root",
        default="results/INHERITED_ORIGIN_CONTEXT_RELATION",
    )
    args = parser.parse_args()
    summary = run_known_periods(
        results_root=args.results_root,
        output_root=args.output_root,
    )
    for period in summary["periods"]:
        print(period["label"], json.dumps(period["expected_side_states"], ensure_ascii=False))
    print("CROSS-PERIOD")
    for feature, result in summary["cross_period"].items():
        print(feature, result["decision"], result["period_states"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
