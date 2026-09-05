from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from nexus_xau.data.csv_loader import load_ohlc_csv
from nexus_xau.data.resample import resample_ohlc
from nexus_xau.research.mtf_alignment_variant_relation_test import (
    H1_TARGET_POINTS,
    PROJECT_POINT_SIZE,
    TF_DELTA,
)
from nexus_xau.research.outcomes import OutcomeSpec, measure_outcome
from nexus_xau.research.remaining_run_state_relation_test import (
    OriginRun,
    _build_origins,
    _consumed_points,
)

HORIZON_H1_BARS = 24

REQUIRED_PARENT_COLUMNS = {
    "cutoff_utc",
    "candidate_known_at",
    "candidate_close",
    "side",
    "state",
    "origin_anchor_known_at",
    "origin_anchor_price",
    "fresh_target_reached_anywhere",
    "fresh_first_hit",
    "fresh_mfe_points",
    "fresh_mae_points",
}


def _origin_destroyed_before(
    active_m1: pd.DataFrame,
    origin: OriginRun,
    end: pd.Timestamp,
) -> bool | None:
    path = active_m1.loc[
        (active_m1.index >= origin.anchor_known_at) & (active_m1.index < end)
    ]
    if path.empty:
        return None
    if origin.side == "BUY":
        return bool((path["low"].astype(float) < origin.anchor_price).any())
    return bool((path["high"].astype(float) > origin.anchor_price).any())


def select_source_partial_origin(
    *,
    active_m1: pd.DataFrame,
    origins: list[OriginRun],
    side: str,
    cutoff_utc: pd.Timestamp,
    candidate_known_at: pd.Timestamp,
) -> OriginRun | None:
    side = side.upper()
    eligible = [
        origin
        for origin in origins
        if origin.side == side and origin.anchor_known_at <= cutoff_utc
    ]
    for origin in reversed(eligible):
        consumed_cutoff = _consumed_points(active_m1, origin, cutoff_utc)
        consumed_entry = _consumed_points(active_m1, origin, candidate_known_at)
        if consumed_cutoff >= H1_TARGET_POINTS or consumed_entry >= H1_TARGET_POINTS:
            continue
        destroyed = _origin_destroyed_before(active_m1, origin, candidate_known_at)
        if destroyed is None or destroyed:
            continue
        return origin
    return None


def _impact_label(
    *,
    old_state: str,
    old_anchor_known_at: pd.Timestamp | None,
    new_origin: OriginRun | None,
) -> str:
    was_inherited = old_state == "INHERITED_REMAINING_RUN"
    if was_inherited and new_origin is None:
        return "DROPPED_NO_VALID_ORIGIN"
    if not was_inherited and new_origin is None:
        return "REMAINS_NO_ACTIVE_ORIGIN"
    if not was_inherited and new_origin is not None:
        return "GAINED_VALID_ORIGIN"
    if old_anchor_known_at is not None and new_origin is not None:
        if new_origin.anchor_known_at == old_anchor_known_at:
            return "SAME_ORIGIN_STILL_VALID"
        if new_origin.anchor_known_at < old_anchor_known_at:
            return "REANCHORED_TO_OLDER_VALID_ORIGIN"
    return "REANCHORED_TO_OTHER_VALID_ORIGIN"


def _horizon_end(h1: pd.DataFrame, candidate_known_at: pd.Timestamp) -> pd.Timestamp | None:
    future = h1.loc[h1.index >= candidate_known_at]
    if len(future) < HORIZON_H1_BARS:
        return None
    return future.index[HORIZON_H1_BARS - 1] + TF_DELTA["H1"] - pd.Timedelta(minutes=1)


def rebuild_events(
    *,
    m1: pd.DataFrame,
    parent_events: pd.DataFrame,
) -> pd.DataFrame:
    missing = REQUIRED_PARENT_COLUMNS.difference(parent_events.columns)
    if missing:
        raise ValueError(f"parent remaining-run events missing columns: {sorted(missing)}")

    active = m1[m1["volume"] > 0].copy() if "volume" in m1.columns else m1.copy()
    h1 = resample_ohlc(active, "H1")
    origins = _build_origins(h1)

    parent = parent_events.copy()
    parent["cutoff_utc"] = pd.to_datetime(parent["cutoff_utc"], utc=True)
    parent["candidate_known_at"] = pd.to_datetime(parent["candidate_known_at"], utc=True)
    parent["origin_anchor_known_at"] = pd.to_datetime(
        parent["origin_anchor_known_at"],
        utc=True,
        errors="coerce",
    )

    rows: list[dict[str, object]] = []
    for row in parent.itertuples(index=False):
        cutoff = pd.Timestamp(row.cutoff_utc)
        candidate_known_at = pd.Timestamp(row.candidate_known_at)
        side = str(row.side).upper()
        horizon_end = _horizon_end(h1, candidate_known_at)
        if horizon_end is None:
            continue

        selected = select_source_partial_origin(
            active_m1=active,
            origins=origins,
            side=side,
            cutoff_utc=cutoff,
            candidate_known_at=candidate_known_at,
        )
        old_anchor = (
            pd.Timestamp(row.origin_anchor_known_at)
            if not pd.isna(row.origin_anchor_known_at)
            else None
        )
        impact = _impact_label(
            old_state=str(row.state),
            old_anchor_known_at=old_anchor,
            new_origin=selected,
        )

        out: dict[str, object] = {
            "cutoff_utc": cutoff.isoformat(),
            "side": side,
            "candidate_known_at": candidate_known_at.isoformat(),
            "candidate_close": float(row.candidate_close),
            "state": (
                "INHERITED_REMAINING_RUN"
                if selected is not None
                else "NO_ACTIVE_INHERITED_RUN"
            ),
            "fresh_target_reached_anywhere": row.fresh_target_reached_anywhere,
            "fresh_first_hit": str(row.fresh_first_hit),
            "fresh_mfe_points": float(row.fresh_mfe_points),
            "fresh_mae_points": float(row.fresh_mae_points),
            "legacy_state": str(row.state),
            "legacy_origin_anchor_known_at": (
                old_anchor.isoformat() if old_anchor is not None else None
            ),
            "legacy_origin_anchor_price": (
                float(row.origin_anchor_price)
                if not pd.isna(row.origin_anchor_price)
                else None
            ),
            "reanchor_impact": impact,
            "source_partial_selected": selected is not None,
            "origin_anchor_known_at": (
                selected.anchor_known_at.isoformat() if selected is not None else None
            ),
            "origin_anchor_price": selected.anchor_price if selected is not None else None,
            "remaining_at_cutoff_points": None,
            "remaining_at_entry_points": None,
            "origin_level_distance_at_entry_points": None,
            "path_remaining_reached": None,
            "path_remaining_first_hit": None,
            "origin_level_reached": None,
            "origin_level_first_hit": None,
        }

        if selected is not None:
            consumed_cutoff = _consumed_points(active, selected, cutoff)
            consumed_entry = _consumed_points(active, selected, candidate_known_at)
            remaining_cutoff = H1_TARGET_POINTS - consumed_cutoff
            path_remaining = max(PROJECT_POINT_SIZE, H1_TARGET_POINTS - consumed_entry)
            origin_target_price = selected.anchor_price + (
                H1_TARGET_POINTS * PROJECT_POINT_SIZE
                if side == "BUY"
                else -H1_TARGET_POINTS * PROJECT_POINT_SIZE
            )
            level_distance = (
                (origin_target_price - float(row.candidate_close))
                if side == "BUY"
                else (float(row.candidate_close) - origin_target_price)
            ) / PROJECT_POINT_SIZE
            level_distance = max(PROJECT_POINT_SIZE, level_distance)

            path_out = measure_outcome(
                active,
                OutcomeSpec(
                    side=side,
                    reference_price=float(row.candidate_close),
                    known_at=candidate_known_at,
                    horizon_end=horizon_end,
                    point_size=PROJECT_POINT_SIZE,
                    target_points=path_remaining,
                    stop_points=H1_TARGET_POINTS,
                ),
            )
            level_out = measure_outcome(
                active,
                OutcomeSpec(
                    side=side,
                    reference_price=float(row.candidate_close),
                    known_at=candidate_known_at,
                    horizon_end=horizon_end,
                    point_size=PROJECT_POINT_SIZE,
                    target_points=level_distance,
                    stop_points=H1_TARGET_POINTS,
                ),
            )
            out.update(
                {
                    "remaining_at_cutoff_points": remaining_cutoff,
                    "remaining_at_entry_points": path_remaining,
                    "origin_level_distance_at_entry_points": level_distance,
                    "path_remaining_reached": path_out.mfe_points >= path_remaining,
                    "path_remaining_first_hit": path_out.first_hit.value,
                    "origin_level_reached": level_out.mfe_points >= level_distance,
                    "origin_level_first_hit": level_out.first_hit.value,
                }
            )
        rows.append(out)

    return pd.DataFrame(rows)


def summarize_rebuild(events: pd.DataFrame) -> dict[str, object]:
    if events.empty:
        return {
            "candidate_events": 0,
            "legacy_inherited_events": 0,
            "reanchored_inherited_events": 0,
            "impact_counts": {},
        }
    return {
        "candidate_events": len(events),
        "legacy_inherited_events": int(
            (events["legacy_state"] == "INHERITED_REMAINING_RUN").sum()
        ),
        "reanchored_inherited_events": int(
            (events["state"] == "INHERITED_REMAINING_RUN").sum()
        ),
        "impact_counts": {
            str(key): int(value)
            for key, value in events["reanchor_impact"].value_counts().to_dict().items()
        },
    }


def _slice_period(
    events: pd.DataFrame,
    *,
    start: pd.Timestamp | None,
    end: pd.Timestamp | None,
) -> pd.DataFrame:
    if start is None and end is None:
        return events
    if start is None or end is None:
        raise ValueError("period_start and period_end must be supplied together")
    start = pd.Timestamp(start)
    end = pd.Timestamp(end)
    if start.tzinfo is None or end.tzinfo is None:
        raise ValueError("period bounds must be timezone-aware")
    known_at = pd.to_datetime(events["candidate_known_at"], utc=True)
    return events[
        (known_at >= start.tz_convert("UTC"))
        & (known_at < end.tz_convert("UTC") + pd.Timedelta(days=1))
    ].copy()


def run(
    *,
    m1_path: str | Path,
    parent_events_path: str | Path,
    report_path: str | Path,
    events_path: str | Path,
    period_start: pd.Timestamp | None = None,
    period_end: pd.Timestamp | None = None,
) -> dict[str, object]:
    m1 = load_ohlc_csv(m1_path)
    parent = pd.read_csv(parent_events_path)
    parent = _slice_period(parent, start=period_start, end=period_end)
    events = rebuild_events(m1=m1, parent_events=parent)

    target_events = Path(events_path)
    target_events.parent.mkdir(parents=True, exist_ok=True)
    events.to_csv(target_events, index=False)

    report: dict[str, object] = {
        "research_status": "SOURCE_PARTIAL_REANCHORED_REMAINING_RUN",
        "source_m1": str(m1_path),
        "source_parent_events": str(parent_events_path),
        "period_start": period_start.isoformat() if period_start is not None else None,
        "period_end": period_end.isoformat() if period_end is not None else None,
        "selection_rule": (
            "latest same-direction pre-cutoff H1 PAT2-BODY origin with nominal 1000-point run incomplete "
            "at cutoff and candidate, and no strict post-SIG destruction before candidate"
        ),
        "strict_destruction": {
            "BUY": "later Low < origin anchor",
            "SELL": "later High > origin anchor",
            "equality": "not destroyed in this frozen research representation",
            "buffer": "none",
        },
        "summary": summarize_rebuild(events),
        "guardrails": [
            "H1 PAT2 BODY remains a research proxy.",
            "SELL destruction is a directional-mirror research representation.",
            "No age, expiry, consumed-run, or distance threshold is introduced.",
            "The approximately 200-point transcript example is not used as a universal buffer.",
            "This is not a strategy win-rate test.",
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
    parser.add_argument("--parent-events", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--events", required=True)
    parser.add_argument("--period-start", default=None)
    parser.add_argument("--period-end", default=None)
    args = parser.parse_args()
    report = run(
        m1_path=args.m1,
        parent_events_path=args.parent_events,
        report_path=args.report,
        events_path=args.events,
        period_start=_parse_bound(args.period_start),
        period_end=_parse_bound(args.period_end),
    )
    print(json.dumps(report["summary"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
