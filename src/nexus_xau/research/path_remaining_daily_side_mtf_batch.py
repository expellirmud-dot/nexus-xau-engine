from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from nexus_xau.research.mtf_alignment_variant_relation_test import LOOKBACK_VARIANTS
from nexus_xau.research.path_remaining_daily_side_mtf_relation_v2 import (
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

REQUIRED_INTERACTION_COLUMNS = {
    "candidate_known_at",
    "side",
    "signed_valid_side_distance_points",
    "path_remaining_reached",
    "path_remaining_first_hit",
    "fresh_mfe_points",
    "fresh_mae_points",
}

_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")


def _utc_day(value: str) -> pd.Timestamp:
    return pd.Timestamp(value, tz="UTC")


def _filename_bounds(path: Path) -> tuple[pd.Timestamp, pd.Timestamp] | None:
    dates = _DATE_RE.findall(path.name)
    if len(dates) < 2:
        return None
    parsed = sorted(_utc_day(value) for value in dates)
    end_of_last_day = parsed[-1] + pd.Timedelta("1D") - pd.Timedelta("1min")
    return parsed[0], end_of_last_day


def _csv_timestamp_bounds(path: Path) -> tuple[pd.Timestamp, pd.Timestamp] | None:
    try:
        timestamps = pd.read_csv(path, usecols=["timestamp"])["timestamp"]
    except (ValueError, KeyError, OSError, pd.errors.EmptyDataError):
        return None
    if timestamps.empty:
        return None
    parsed = pd.to_datetime(timestamps, utc=True, errors="coerce").dropna()
    if parsed.empty:
        return None
    return pd.Timestamp(parsed.iloc[0]), pd.Timestamp(parsed.iloc[-1])


def discover_m1_file(root: str | Path, *, start: str, end: str) -> Path:
    root = Path(root)
    target_start = _utc_day(start)
    target_end = _utc_day(end) + pd.Timedelta("1D") - pd.Timedelta("1min")
    candidates: list[tuple[float, Path]] = []

    for path in root.rglob("*.csv"):
        name = path.name.upper()
        if "XAUUSD" not in name or "M1" not in name or "BID" not in name:
            continue
        bounds = _filename_bounds(path)
        if bounds is None:
            bounds = _csv_timestamp_bounds(path)
        if bounds is None:
            continue
        first, last = bounds
        if first <= target_start and last >= target_end:
            coverage_seconds = float((last - first).total_seconds())
            candidates.append((coverage_seconds, path))

    if not candidates:
        raise FileNotFoundError(
            f"No XAUUSD BID M1 CSV under {root} covers {start} through {end}."
        )
    candidates.sort(key=lambda item: (item[0], str(item[1])))
    return candidates[0][1]


def _interaction_candidate_stats(
    path: Path,
    *,
    start: pd.Timestamp,
    end: pd.Timestamp,
) -> tuple[int, int] | None:
    try:
        header = pd.read_csv(path, nrows=0)
    except (OSError, pd.errors.EmptyDataError, UnicodeDecodeError):
        return None
    columns = set(header.columns)
    if not REQUIRED_INTERACTION_COLUMNS.issubset(columns):
        return None
    # Exclude already-enriched MTF outputs so the parent interaction table is used.
    if "alignment_count" in columns or "variant" in columns:
        return None

    try:
        raw = pd.read_csv(path, usecols=["candidate_known_at"])
    except (ValueError, OSError, pd.errors.EmptyDataError):
        return None
    known_at = pd.to_datetime(
        raw["candidate_known_at"],
        utc=True,
        errors="coerce",
    ).dropna()
    if known_at.empty:
        return None
    end_exclusive = end + pd.Timedelta("1D")
    inside = int(((known_at >= start) & (known_at < end_exclusive)).sum())
    if inside == 0:
        return None
    outside = int(len(known_at) - inside)
    return inside, outside


def discover_interaction_events_file(
    root: str | Path,
    *,
    start: str,
    end: str,
) -> Path:
    root = Path(root)
    target_start = _utc_day(start)
    target_end = _utc_day(end)
    candidates: list[tuple[int, int, str, Path]] = []

    for path in root.rglob("*.csv"):
        stats = _interaction_candidate_stats(
            path,
            start=target_start,
            end=target_end,
        )
        if stats is None:
            continue
        inside, outside = stats
        # Prefer the table with the least unrelated period data, then the most
        # in-period events. Filename is only a deterministic tie-breaker.
        candidates.append((outside, -inside, str(path), path))

    if not candidates:
        raise FileNotFoundError(
            f"No parent Daily-Frame/PATH_REMAINING interaction event CSV under {root} "
            f"contains {start} through {end}."
        )
    candidates.sort(key=lambda item: (item[0], item[1], item[2]))
    return candidates[0][3]


def cross_period_decision(period_states: list[str]) -> str:
    side = period_states.count("SIDE_CONDITIONAL_SUPPORT")
    general = period_states.count("GENERAL_MTF_SUPPORT_NOT_SIDE_SPECIFIC")
    oppose = period_states.count("EXPECTED_SIDE_OPPOSE")

    if side >= 2 and general == 0 and oppose == 0:
        return "SUPPORTED_SIDE_CONDITIONAL_REPLICATION"
    if general >= 2 and side == 0 and oppose == 0:
        return "SUPPORTED_GENERAL_MTF_NOT_SIDE_SPECIFIC"
    if side + general >= 2 and oppose == 0:
        return "SUPPORTED_MTF_RELATION_SPECIFICITY_MIXED"
    if oppose >= 2:
        return "NOT_SUPPORTED_EXPECTED_SIDE"
    return "INCONCLUSIVE"


def run_known_periods(
    *,
    data_root: str | Path,
    results_root: str | Path,
    output_root: str | Path,
) -> dict[str, object]:
    output_root = Path(output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    period_outputs: list[dict[str, object]] = []
    for period in KNOWN_PERIODS:
        m1_path = discover_m1_file(data_root, start=period.start, end=period.end)
        interaction_path = discover_interaction_events_file(
            results_root,
            start=period.start,
            end=period.end,
        )
        report_path = output_root / f"{period.label}_REPORT.json"
        events_path = output_root / f"{period.label}_EVENTS.csv"
        report = run_period(
            m1_path=m1_path,
            interaction_events_path=interaction_path,
            report_path=report_path,
            enriched_events_path=events_path,
            positive_volume_only=True,
            period_start=_utc_day(period.start),
            period_end=_utc_day(period.end),
        )
        period_outputs.append(
            {
                "label": period.label,
                "start": period.start,
                "end": period.end,
                "m1": str(m1_path),
                "interaction_events": str(interaction_path),
                "report": str(report_path),
                "events": str(events_path),
                "period_states": report["period_states"],
            }
        )

    cross_variant: dict[str, object] = {}
    for variant in LOOKBACK_VARIANTS:
        states = [str(period["period_states"][variant]) for period in period_outputs]
        cross_variant[variant] = {
            "period_states": states,
            "decision": cross_period_decision(states),
        }

    summary: dict[str, object] = {
        "research_status": "PATH_REMAINING_X_DAILY_SIDE_X_GRADED_MTF_V2_MULTIPERIOD",
        "periods": period_outputs,
        "cross_period_by_variant": cross_variant,
        "closure_rule_frozen_before_execution": {
            "side_conditional_replication": (
                ">=2 SIDE_CONDITIONAL_SUPPORT periods, no GENERAL and no EXPECTED_SIDE_OPPOSE"
            ),
            "general_replication": (
                ">=2 GENERAL_MTF_SUPPORT_NOT_SIDE_SPECIFIC periods, no SIDE and no OPPOSE"
            ),
            "mtf_supported_specificity_mixed": (
                ">=2 total SIDE/GENERAL support periods and no EXPECTED_SIDE_OPPOSE"
            ),
            "not_supported": ">=2 EXPECTED_SIDE_OPPOSE periods",
            "otherwise": "INCONCLUSIVE",
        },
        "interpretation_guard": [
            (
                "These periods have prior project use; this is replication/interaction "
                "evidence, not untouched final holdout confirmation."
            ),
            "No aligned-TF production minimum is selected.",
            "PAT2 BODY and PATH_REMAINING remain research representations.",
            "Outcome cannot identify the instructor's canonical freshness rule.",
            "No strategy win rate is produced.",
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
    parser.add_argument("--data-root", default="data/raw/dukascopy")
    parser.add_argument("--results-root", default="results")
    parser.add_argument(
        "--output-root",
        default="results/PATH_REMAINING_DAILY_SIDE_MTF_V2",
    )
    args = parser.parse_args()
    summary = run_known_periods(
        data_root=args.data_root,
        results_root=args.results_root,
        output_root=args.output_root,
    )
    for period in summary["periods"]:
        print(period["label"], json.dumps(period["period_states"], ensure_ascii=False))
    print("CROSS-PERIOD")
    for variant, result in summary["cross_period_by_variant"].items():
        print(variant, result["decision"], result["period_states"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
