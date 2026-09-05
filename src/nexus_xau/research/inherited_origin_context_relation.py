from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from nexus_xau.research.mtf_alignment_variant_relation_test import H1_TARGET_POINTS

MIN_GROUP = 10

REQUIRED_REMAINING_COLUMNS = {
    "state",
    "cutoff_utc",
    "candidate_known_at",
    "side",
    "origin_anchor_known_at",
    "remaining_at_entry_points",
    "fresh_target_reached_anywhere",
    "fresh_first_hit",
    "fresh_mfe_points",
    "fresh_mae_points",
    "path_remaining_reached",
    "path_remaining_first_hit",
    "origin_level_reached",
    "origin_level_first_hit",
}

REQUIRED_DAILY_COLUMNS = {
    "candidate_known_at",
    "side",
    "signed_valid_side_distance_points",
}


def _normalize_bool(value: object) -> bool | None:
    if isinstance(value, bool):
        return value
    if value is None or pd.isna(value):
        return None
    text = str(value).strip().lower()
    if text in {"true", "1", "yes"}:
        return True
    if text in {"false", "0", "no"}:
        return False
    raise ValueError(f"Cannot normalize boolean value: {value!r}")


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


def _fixed_outcome_summary(group: pd.DataFrame) -> dict[str, float | int | None]:
    resolved = group[group["fresh_first_hit"].isin(["TARGET_FIRST", "STOP_FIRST"])]
    return {
        "events": len(group),
        "resolved_events": len(resolved),
        "target_first_rate_resolved": (
            float((resolved["fresh_first_hit"] == "TARGET_FIRST").mean())
            if not resolved.empty
            else None
        ),
        "fresh_1000_reach_rate": (
            float(group["fresh_target_reached_anywhere"].mean()) if not group.empty else None
        ),
        "fresh_mfe_median": (
            float(group["fresh_mfe_points"].median()) if not group.empty else None
        ),
        "fresh_mae_median": (
            float(group["fresh_mae_points"].median()) if not group.empty else None
        ),
    }


def _secondary_target_summary(group: pd.DataFrame) -> dict[str, float | int | None]:
    path_resolved = group[
        group["path_remaining_first_hit"].isin(["TARGET_FIRST", "STOP_FIRST"])
    ]
    level_resolved = group[
        group["origin_level_first_hit"].isin(["TARGET_FIRST", "STOP_FIRST"])
    ]
    return {
        "events": len(group),
        "path_remaining_reach_rate": (
            float(group["path_remaining_reached"].mean()) if not group.empty else None
        ),
        "path_remaining_target_first_rate_resolved": (
            float((path_resolved["path_remaining_first_hit"] == "TARGET_FIRST").mean())
            if not path_resolved.empty
            else None
        ),
        "origin_level_reach_rate": (
            float(group["origin_level_reached"].mean()) if not group.empty else None
        ),
        "origin_level_target_first_rate_resolved": (
            float((level_resolved["origin_level_first_hit"] == "TARGET_FIRST").mean())
            if not level_resolved.empty
            else None
        ),
    }


def _relation_summary(group: pd.DataFrame, feature: str) -> dict[str, object]:
    resolved = group[group["fresh_first_hit"].isin(["TARGET_FIRST", "STOP_FIRST"])].copy()
    if not resolved.empty:
        resolved["target_first_binary"] = (
            resolved["fresh_first_hit"] == "TARGET_FIRST"
        ).astype(int)

    return {
        "events": len(group),
        "distinct_feature_values": int(group[feature].nunique(dropna=True)),
        "feature_min": float(group[feature].min()) if not group.empty else None,
        "feature_median": float(group[feature].median()) if not group.empty else None,
        "feature_max": float(group[feature].max()) if not group.empty else None,
        "spearman_vs_fixed_target_first": (
            _safe_spearman(resolved, feature, "target_first_binary")
            if not resolved.empty
            else None
        ),
        "spearman_vs_fixed_reach": _safe_spearman(
            group,
            feature,
            "fresh_target_reached_anywhere",
        ),
        "spearman_vs_fresh_mfe": _safe_spearman(group, feature, "fresh_mfe_points"),
        "spearman_vs_fresh_mae": _safe_spearman(group, feature, "fresh_mae_points"),
    }


def _relation_values(summary: dict[str, object]) -> tuple[float, float, float, float] | None:
    values = (
        summary["spearman_vs_fixed_target_first"],
        summary["spearman_vs_fixed_reach"],
        summary["spearman_vs_fresh_mfe"],
        summary["spearman_vs_fresh_mae"],
    )
    if not all(isinstance(value, float) for value in values):
        return None
    return values  # type: ignore[return-value]


def age_relation_state(summary: dict[str, object]) -> str:
    if int(summary["events"]) < MIN_GROUP:
        return "INSUFFICIENT"
    if int(summary["distinct_feature_values"]) < 2:
        return "INDISTINGUISHABLE"
    values = _relation_values(summary)
    if values is None:
        return "INDISTINGUISHABLE"
    target_first, reach, mfe, mae = values
    if target_first < 0 and reach <= 0 and mfe <= 0 and mae >= 0:
        return "YOUNGER_ORIGIN_FAVORED"
    if target_first > 0 and reach >= 0 and mfe >= 0 and mae <= 0:
        return "OLDER_ORIGIN_FAVORED"
    return "MIXED"


def consumed_relation_state(summary: dict[str, object]) -> str:
    if int(summary["events"]) < MIN_GROUP:
        return "INSUFFICIENT"
    if int(summary["distinct_feature_values"]) < 2:
        return "INDISTINGUISHABLE"
    values = _relation_values(summary)
    if values is None:
        return "INDISTINGUISHABLE"
    target_first, reach, mfe, mae = values
    if target_first > 0 and reach >= 0 and mfe >= 0 and mae <= 0:
        return "MORE_CONSUMED_FAVORED"
    if target_first < 0 and reach <= 0 and mfe <= 0 and mae >= 0:
        return "LESS_CONSUMED_FAVORED"
    return "MIXED"


def cycle_relation_state(previous: dict[str, object], older: dict[str, object]) -> str:
    if int(previous["events"]) < MIN_GROUP or int(older["events"]) < MIN_GROUP:
        return "INSUFFICIENT"
    keys = (
        "target_first_rate_resolved",
        "fresh_1000_reach_rate",
        "fresh_mfe_median",
        "fresh_mae_median",
    )
    values = [previous[key] for key in keys] + [older[key] for key in keys]
    if not all(isinstance(value, float) for value in values):
        return "INSUFFICIENT"

    previous_favored = (
        previous["target_first_rate_resolved"] > older["target_first_rate_resolved"]
        and previous["fresh_1000_reach_rate"] >= older["fresh_1000_reach_rate"]
        and previous["fresh_mfe_median"] >= older["fresh_mfe_median"]
        and previous["fresh_mae_median"] <= older["fresh_mae_median"]
    )
    older_favored = (
        previous["target_first_rate_resolved"] < older["target_first_rate_resolved"]
        and previous["fresh_1000_reach_rate"] <= older["fresh_1000_reach_rate"]
        and previous["fresh_mfe_median"] <= older["fresh_mfe_median"]
        and previous["fresh_mae_median"] >= older["fresh_mae_median"]
    )
    if previous_favored:
        return "PREVIOUS_24H_FAVORED"
    if older_favored:
        return "OLDER_CYCLE_FAVORED"
    return "MIXED"


def build_context_events(
    *,
    remaining_events: pd.DataFrame,
    daily_events: pd.DataFrame,
) -> pd.DataFrame:
    missing_remaining = REQUIRED_REMAINING_COLUMNS.difference(remaining_events.columns)
    if missing_remaining:
        raise ValueError(f"remaining events missing columns: {sorted(missing_remaining)}")
    missing_daily = REQUIRED_DAILY_COLUMNS.difference(daily_events.columns)
    if missing_daily:
        raise ValueError(f"daily events missing columns: {sorted(missing_daily)}")

    remaining = remaining_events.copy()
    daily = daily_events.copy()
    for frame in (remaining, daily):
        frame["candidate_known_at"] = pd.to_datetime(frame["candidate_known_at"], utc=True)
        frame["side"] = frame["side"].astype(str).str.upper()

    remaining = remaining[remaining["state"] == "INHERITED_REMAINING_RUN"].copy()
    remaining["cutoff_utc"] = pd.to_datetime(remaining["cutoff_utc"], utc=True)
    remaining["origin_anchor_known_at"] = pd.to_datetime(
        remaining["origin_anchor_known_at"],
        utc=True,
    )

    daily = daily[
        ["candidate_known_at", "side", "signed_valid_side_distance_points"]
    ].drop_duplicates(subset=["candidate_known_at", "side"], keep="first")

    merged = remaining.merge(
        daily,
        on=["candidate_known_at", "side"],
        how="inner",
        validate="many_to_one",
    )
    if merged.empty:
        return merged

    for column in (
        "fresh_target_reached_anywhere",
        "path_remaining_reached",
        "origin_level_reached",
    ):
        merged[column] = merged[column].map(_normalize_bool)

    merged = merged[
        merged["fresh_target_reached_anywhere"].notna()
        & merged["origin_anchor_known_at"].notna()
        & merged["remaining_at_entry_points"].notna()
    ].copy()

    age = merged["candidate_known_at"] - merged["origin_anchor_known_at"]
    merged["origin_age_hours"] = age.dt.total_seconds() / 3600.0
    if (merged["origin_age_hours"] < 0).any():
        raise ValueError("origin_anchor_known_at occurs after candidate_known_at")

    merged["consumed_run_ratio_at_entry"] = (
        H1_TARGET_POINTS - merged["remaining_at_entry_points"].astype(float)
    ) / H1_TARGET_POINTS

    cycle_start = merged["cutoff_utc"] - pd.Timedelta(hours=24)
    if (merged["origin_anchor_known_at"] > merged["cutoff_utc"]).any():
        raise ValueError("origin_anchor_known_at occurs after cutoff_utc")
    merged["origin_cycle_group"] = "OLDER_THAN_PREVIOUS_24H"
    merged.loc[
        merged["origin_anchor_known_at"] > cycle_start,
        "origin_cycle_group",
    ] = "PREVIOUS_24H_CYCLE"

    merged["frame_side"] = "CROSSED_SIDE"
    merged.loc[
        merged["signed_valid_side_distance_points"].astype(float) >= 0,
        "frame_side",
    ] = "EXPECTED_SIDE"
    return merged


def summarize_context_events(events: pd.DataFrame) -> dict[str, object]:
    side_reports: dict[str, object] = {}
    for frame_side in ("EXPECTED_SIDE", "CROSSED_SIDE"):
        group = events[events["frame_side"] == frame_side].copy()
        age_summary = _relation_summary(group, "origin_age_hours")
        consumed_summary = _relation_summary(group, "consumed_run_ratio_at_entry")
        side_reports[frame_side] = {
            "events": len(group),
            "fixed_outcomes": _fixed_outcome_summary(group),
            "secondary_targets": _secondary_target_summary(group),
            "origin_age": {
                "relation": age_summary,
                "state": age_relation_state(age_summary),
            },
            "consumed_run_ratio_at_entry": {
                "relation": consumed_summary,
                "state": consumed_relation_state(consumed_summary),
            },
        }

    expected = events[events["frame_side"] == "EXPECTED_SIDE"].copy()
    previous = expected[expected["origin_cycle_group"] == "PREVIOUS_24H_CYCLE"]
    older = expected[expected["origin_cycle_group"] == "OLDER_THAN_PREVIOUS_24H"]
    previous_summary = _fixed_outcome_summary(previous)
    older_summary = _fixed_outcome_summary(older)
    return {
        "side_reports": side_reports,
        "expected_side_cycle_comparison": {
            "PREVIOUS_24H_CYCLE": previous_summary,
            "OLDER_THAN_PREVIOUS_24H": older_summary,
            "state": cycle_relation_state(previous_summary, older_summary),
        },
    }


def _slice_period(
    frame: pd.DataFrame,
    *,
    start: pd.Timestamp | None,
    end: pd.Timestamp | None,
) -> pd.DataFrame:
    if start is None and end is None:
        return frame
    if start is None or end is None:
        raise ValueError("period_start and period_end must be supplied together")
    start = pd.Timestamp(start)
    end = pd.Timestamp(end)
    if start.tzinfo is None or end.tzinfo is None:
        raise ValueError("period bounds must be timezone-aware")
    start = start.tz_convert("UTC")
    end = end.tz_convert("UTC")
    known_at = pd.to_datetime(frame["candidate_known_at"], utc=True)
    return frame[(known_at >= start) & (known_at < end + pd.Timedelta(days=1))].copy()


def run(
    *,
    remaining_events_path: str | Path,
    daily_events_path: str | Path,
    report_path: str | Path,
    events_path: str | Path,
    period_start: pd.Timestamp | None = None,
    period_end: pd.Timestamp | None = None,
) -> dict[str, object]:
    remaining = pd.read_csv(remaining_events_path)
    daily = pd.read_csv(daily_events_path)
    remaining = _slice_period(remaining, start=period_start, end=period_end)
    daily = _slice_period(daily, start=period_start, end=period_end)
    events = build_context_events(remaining_events=remaining, daily_events=daily)

    target_events = Path(events_path)
    target_events.parent.mkdir(parents=True, exist_ok=True)
    events.to_csv(target_events, index=False)

    summary = summarize_context_events(events)
    report: dict[str, object] = {
        "research_status": "INHERITED_ORIGIN_CONTEXT_X_DAILY_FRAME_SIDE_RELATION",
        "source_remaining_events": str(remaining_events_path),
        "source_daily_events": str(daily_events_path),
        "period_start": period_start.isoformat() if period_start is not None else None,
        "period_end": period_end.isoformat() if period_end is not None else None,
        "joined_inherited_events": len(events),
        "minimum_group": MIN_GROUP,
        "primary_outcome_lane": (
            "Fixed fresh H1 1000-point control: target-first, reach, MFE, MAE. "
            "This avoids mechanically rewarding larger consumed-run ratio through a smaller PATH_REMAINING target."
        ),
        "derived_features": {
            "origin_age_hours": "candidate_known_at - origin_anchor_known_at",
            "consumed_run_ratio_at_entry": (
                f"({H1_TARGET_POINTS} - remaining_at_entry_points) / {H1_TARGET_POINTS}"
            ),
            "origin_cycle_group": (
                "PREVIOUS_24H_CYCLE when origin_anchor_known_at > cutoff_utc - 24h; otherwise older."
            ),
        },
        "summary": summary,
        "guardrails": [
            "No age or consumed-run production threshold is selected.",
            "The 24-hour group is a preparation-cycle research representation, not a canonical expiry rule.",
            "PATH_REMAINING and ORIGIN_TARGET_LEVEL remain secondary comparators.",
            "Historical outcomes cannot identify instructor intent.",
            "Fresh target-first is not strategy win rate.",
        ],
    }
    Path(report_path).write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return report


def _parse_bound(value: str | None) -> pd.Timestamp | None:
    if value is None:
        return None
    timestamp = pd.Timestamp(value)
    if timestamp.tzinfo is None:
        timestamp = timestamp.tz_localize("UTC")
    return timestamp.tz_convert("UTC")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--remaining-events", required=True)
    parser.add_argument("--daily-events", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--events", required=True)
    parser.add_argument("--period-start", default=None)
    parser.add_argument("--period-end", default=None)
    args = parser.parse_args()
    report = run(
        remaining_events_path=args.remaining_events,
        daily_events_path=args.daily_events,
        report_path=args.report,
        events_path=args.events,
        period_start=_parse_bound(args.period_start),
        period_end=_parse_bound(args.period_end),
    )
    expected = report["summary"]["side_reports"]["EXPECTED_SIDE"]
    print("EXPECTED_SIDE origin_age", expected["origin_age"]["state"])
    print(
        "EXPECTED_SIDE consumed_run_ratio_at_entry",
        expected["consumed_run_ratio_at_entry"]["state"],
    )
    print(
        "EXPECTED_SIDE origin_cycle_group",
        report["summary"]["expected_side_cycle_comparison"]["state"],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
