from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from nexus_xau.data.csv_loader import load_ohlc_csv
from nexus_xau.research.mtf_alignment_variant_relation_test import LOOKBACK_VARIANTS, TIMEFRAMES
from nexus_xau.research.path_remaining_daily_side_mtf_relation import (
    enrich_events_with_mtf_alignment,
)

# Inherit the already-frozen parent Daily-Frame-side minimum instead of inventing
# a new 40-event gate for this conditional relation test.
MIN_SIDE_EVENTS = 10


def _safe_spearman(frame: pd.DataFrame, x: str, y: str) -> float | None:
    clean = frame[[x, y]].dropna()
    if len(clean) < 3 or clean[x].nunique() < 2 or clean[y].nunique() < 2:
        return None
    ranked_x = clean[x].rank(method="average")
    ranked_y = clean[y].rank(method="average")
    value = ranked_x.corr(ranked_y, method="pearson")
    if pd.isna(value):
        return None
    return float(value)


def _outcome_summary(group: pd.DataFrame) -> dict[str, float | int | None]:
    resolved = group[group["path_remaining_first_hit"].isin(["TARGET_FIRST", "STOP_FIRST"])]
    return {
        "events": len(group),
        "resolved_events": len(resolved),
        "target_first_rate_resolved": (
            float((resolved["path_remaining_first_hit"] == "TARGET_FIRST").mean())
            if not resolved.empty
            else None
        ),
        "path_remaining_reach_rate": (
            float(group["path_remaining_reached"].mean()) if not group.empty else None
        ),
        "fresh_mfe_median": (
            float(group["fresh_mfe_points"].median()) if not group.empty else None
        ),
        "fresh_mae_median": (
            float(group["fresh_mae_points"].median()) if not group.empty else None
        ),
    }


def _relation_summary(group: pd.DataFrame) -> dict[str, object]:
    resolved = group[
        group["path_remaining_first_hit"].isin(["TARGET_FIRST", "STOP_FIRST"])
    ].copy()
    if not resolved.empty:
        resolved["target_first_binary"] = (
            resolved["path_remaining_first_hit"] == "TARGET_FIRST"
        ).astype(int)

    level_counts = group["alignment_count"].value_counts().sort_index().to_dict()
    return {
        "events": len(group),
        "alignment_level_counts": {
            str(int(level)): int(count) for level, count in level_counts.items()
        },
        "distinct_alignment_levels": len(level_counts),
        "spearman_alignment_vs_target_first": (
            _safe_spearman(resolved, "alignment_count", "target_first_binary")
            if not resolved.empty
            else None
        ),
        "spearman_alignment_vs_path_remaining_reach": _safe_spearman(
            group,
            "alignment_count",
            "path_remaining_reached",
        ),
        "spearman_alignment_vs_fresh_mfe": _safe_spearman(
            group,
            "alignment_count",
            "fresh_mfe_points",
        ),
        "spearman_alignment_vs_fresh_mae": _safe_spearman(
            group,
            "alignment_count",
            "fresh_mae_points",
        ),
    }


def _side_relation_state(summary: dict[str, object]) -> str:
    if int(summary["events"]) < MIN_SIDE_EVENTS:
        return "INSUFFICIENT"
    if int(summary["distinct_alignment_levels"]) < 2:
        return "INDISTINGUISHABLE"

    target_first = summary["spearman_alignment_vs_target_first"]
    reach = summary["spearman_alignment_vs_path_remaining_reach"]
    mfe = summary["spearman_alignment_vs_fresh_mfe"]
    mae = summary["spearman_alignment_vs_fresh_mae"]
    if not all(isinstance(value, float) for value in (target_first, reach, mfe, mae)):
        return "INDISTINGUISHABLE"

    if target_first > 0 and reach >= 0 and mfe >= 0 and mae <= 0:
        return "SUPPORT"
    if target_first <= 0 and reach <= 0 and mfe <= 0 and mae >= 0:
        return "OPPOSE"
    return "MIXED"


def _period_state(expected_state: str, crossed_state: str) -> str:
    if expected_state == "SUPPORT" and crossed_state == "SUPPORT":
        return "GENERAL_MTF_SUPPORT_NOT_SIDE_SPECIFIC"
    if expected_state == "SUPPORT":
        return "SIDE_CONDITIONAL_SUPPORT"
    if expected_state == "OPPOSE":
        return "EXPECTED_SIDE_OPPOSE"
    if expected_state == "INDISTINGUISHABLE":
        return "EXPECTED_SIDE_INDISTINGUISHABLE"
    return "INCONCLUSIVE"


def summarize_enriched_events(events: pd.DataFrame) -> dict[str, object]:
    required = {
        "variant",
        "frame_side",
        "alignment_count",
        "aligned_timeframes",
        "path_remaining_reached",
        "path_remaining_first_hit",
        "fresh_mfe_points",
        "fresh_mae_points",
    }
    missing = required.difference(events.columns)
    if missing:
        raise ValueError(f"enriched events missing columns: {sorted(missing)}")

    variant_reports: dict[str, object] = {}
    period_states: dict[str, str] = {}

    for variant in LOOKBACK_VARIANTS:
        variant_rows = events[events["variant"] == variant]
        side_reports: dict[str, object] = {}
        side_states: dict[str, str] = {}

        for frame_side in ("EXPECTED_SIDE", "CROSSED_SIDE"):
            group = variant_rows[variant_rows["frame_side"] == frame_side]
            relation = _relation_summary(group)
            state = _side_relation_state(relation)
            by_count = {
                str(int(count)): _outcome_summary(
                    group[group["alignment_count"] == count]
                )
                for count in sorted(group["alignment_count"].unique())
            }
            aligned_set_counts = (
                group["aligned_timeframes"].fillna("").value_counts().to_dict()
            )
            side_reports[frame_side] = {
                "relation": relation,
                "by_alignment_count": by_count,
                "aligned_tf_set_counts": {
                    str(name): int(count) for name, count in aligned_set_counts.items()
                },
                "relation_state": state,
            }
            side_states[frame_side] = state

        period_state = _period_state(
            side_states["EXPECTED_SIDE"],
            side_states["CROSSED_SIDE"],
        )
        period_states[variant] = period_state
        variant_reports[variant] = {
            "sides": side_reports,
            "period_interaction_state": period_state,
        }

    return {
        "period_states": period_states,
        "variant_reports": variant_reports,
    }


def _slice_period(
    m1: pd.DataFrame,
    interaction: pd.DataFrame,
    *,
    period_start: pd.Timestamp | None,
    period_end: pd.Timestamp | None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    if period_start is None and period_end is None:
        return m1, interaction
    if period_start is None or period_end is None:
        raise ValueError("period_start and period_end must be supplied together")

    start = pd.Timestamp(period_start)
    end = pd.Timestamp(period_end)
    if start.tzinfo is None or end.tzinfo is None:
        raise ValueError("period bounds must be timezone-aware")
    start = start.tz_convert("UTC")
    end = end.tz_convert("UTC")
    if end < start:
        raise ValueError("period_end must be >= period_start")

    # Alignment freshness needs only short history; one day is deliberately
    # conservative and does not use future outcome information.
    m1_start = start - pd.Timedelta("1D")
    m1_end_exclusive = end + pd.Timedelta("1D")
    m1_slice = m1[(m1.index >= m1_start) & (m1.index < m1_end_exclusive)].copy()

    known_at = pd.to_datetime(interaction["candidate_known_at"], utc=True)
    interaction_slice = interaction[
        (known_at >= start) & (known_at < end + pd.Timedelta("1D"))
    ].copy()
    return m1_slice, interaction_slice


def run(
    *,
    m1_path: str | Path,
    interaction_events_path: str | Path,
    report_path: str | Path,
    enriched_events_path: str | Path,
    positive_volume_only: bool = True,
    period_start: pd.Timestamp | None = None,
    period_end: pd.Timestamp | None = None,
) -> dict[str, object]:
    m1 = load_ohlc_csv(m1_path)
    source_rows = len(m1)
    if positive_volume_only:
        if "volume" not in m1.columns:
            raise ValueError("positive_volume_only requires a volume column")
        m1 = m1[m1["volume"] > 0].copy()

    interaction = pd.read_csv(interaction_events_path)
    interaction["candidate_known_at"] = pd.to_datetime(
        interaction["candidate_known_at"],
        utc=True,
    )
    m1, interaction = _slice_period(
        m1,
        interaction,
        period_start=period_start,
        period_end=period_end,
    )
    active_rows = len(m1)

    enriched = enrich_events_with_mtf_alignment(
        m1=m1,
        interaction_events=interaction,
    )
    target_events = Path(enriched_events_path)
    target_events.parent.mkdir(parents=True, exist_ok=True)
    enriched.to_csv(target_events, index=False)

    summary = summarize_enriched_events(enriched)
    report: dict[str, object] = {
        "research_question": (
            "Within inherited PATH_REMAINING events, after conditioning on Daily Frame "
            "EXPECTED_SIDE vs CROSSED_SIDE, does increasing same-direction H1/M30/M15/M5 "
            "PAT2-BODY proxy alignment relate to better remaining-run behavior?"
        ),
        "research_status": "PATH_REMAINING_X_DAILY_FRAME_SIDE_X_GRADED_MTF_RELATION_V2",
        "supersedes_implementation_only": (
            "V1 sufficiency gates 40 events/side and 10 events/alignment-level; no empirical "
            "MTF-interaction outcome was inspected before this V2 correction."
        ),
        "source_m1": str(m1_path),
        "source_interaction_events": str(interaction_events_path),
        "source_m1_rows": source_rows,
        "active_m1_rows": active_rows,
        "positive_volume_only": positive_volume_only,
        "period_start": period_start.isoformat() if period_start is not None else None,
        "period_end": period_end.isoformat() if period_end is not None else None,
        "measured_interaction_events": int(interaction["candidate_known_at"].nunique()),
        "enriched_rows": len(enriched),
        "timeframes": list(TIMEFRAMES),
        "lookback_variants": LOOKBACK_VARIANTS,
        "minimum_side_events": MIN_SIDE_EVENTS,
        "alignment_level_rule": (
            "At least two observed alignment-count levels; no invented per-level count threshold."
        ),
        "sufficiency_basis": (
            "MIN_SIDE_EVENTS=10 inherits the parent Daily-Frame-side checkpoint. Spearman is "
            "treated as a graded relation across observed counts rather than thresholding each count bin."
        ),
        "representation": {
            "daily_frame_side": (
                "EXPECTED_SIDE when signed_valid_side_distance_points >= 0; otherwise CROSSED_SIDE"
            ),
            "alignment": (
                "Count same-direction PAT2-BODY research proxy events across H1/M30/M15/M5 "
                "known at/before candidate_known_at under each frozen freshness variant."
            ),
            "target": "existing PATH_REMAINING outcome fields from the prior interaction event table",
        },
        "period_states": summary["period_states"],
        "variant_reports": summary["variant_reports"],
        "closure_guard": [
            "This is a graded relation test; it does not select a hard aligned-TF gate.",
            "PAT2 BODY is a research proxy, not canonical full PA.",
            "PATH_REMAINING is a research representation, not a proven teacher formula.",
            "Historical outcome performance cannot choose the instructor's canonical freshness rule.",
            "Target-first rate here is not strategy win rate.",
            "CROSSED_SIDE is descriptive and is not automatically invalid.",
        ],
    }

    target_report = Path(report_path)
    target_report.parent.mkdir(parents=True, exist_ok=True)
    target_report.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return report


def _parse_bound(value: str | None) -> pd.Timestamp | None:
    if value is None:
        return None
    ts = pd.Timestamp(value)
    if ts.tzinfo is None:
        ts = ts.tz_localize("UTC")
    return ts.tz_convert("UTC")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--m1", required=True)
    parser.add_argument("--interaction-events", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--events", required=True)
    parser.add_argument("--period-start", default=None)
    parser.add_argument("--period-end", default=None)
    parser.add_argument(
        "--include-zero-volume",
        action="store_true",
        help="Do not apply the project's usual positive-volume-only research filter.",
    )
    args = parser.parse_args()
    report = run(
        m1_path=args.m1,
        interaction_events_path=args.interaction_events,
        report_path=args.report,
        enriched_events_path=args.events,
        positive_volume_only=not args.include_zero_volume,
        period_start=_parse_bound(args.period_start),
        period_end=_parse_bound(args.period_end),
    )
    print(json.dumps(report["period_states"], ensure_ascii=False, indent=2))
    for variant, detail in report["variant_reports"].items():
        print(variant, detail["period_interaction_state"])
        for frame_side, side_detail in detail["sides"].items():
            print(
                " ",
                frame_side,
                side_detail["relation_state"],
                json.dumps(side_detail["relation"], ensure_ascii=False),
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
