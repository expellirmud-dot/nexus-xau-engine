from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import pandas as pd

from nexus_xau.data.csv_loader import load_ohlc_csv
from nexus_xau.data.resample import resample_ohlc
from nexus_xau.research.mtf_alignment_variant_relation_test import (
    H1_TARGET_POINTS,
    PROJECT_POINT_SIZE,
    TF_DELTA,
    _group_summary,
    _pat2_body_events,
)
from nexus_xau.research.outcomes import OutcomeSpec, measure_outcome

MIN_GROUP = 30


@dataclass(frozen=True, slots=True)
class OriginRun:
    side: str
    pattern_known_at: pd.Timestamp
    anchor_known_at: pd.Timestamp
    anchor_price: float


def _load_missing_dates(path: str | Path | None) -> set[date]:
    if path is None:
        return set()
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    values = payload.get("missing_cache_dates", payload.get("failed_dates", []))
    return {date.fromisoformat(value) for value in values}


def _intersects_missing(start: pd.Timestamp, end: pd.Timestamp, missing: set[date]) -> bool:
    current = start.normalize()
    final = end.normalize()
    while current <= final:
        if current.date() in missing:
            return True
        current += pd.Timedelta(days=1)
    return False


def _build_origins(h1: pd.DataFrame) -> list[OriginRun]:
    events = _pat2_body_events(h1, "H1")
    origins: list[OriginRun] = []
    for event in events:
        post_start = event.known_at
        if post_start not in h1.index:
            continue
        post = h1.loc[post_start]
        anchor_price = float(post.low if event.side == "BUY" else post.high)
        origins.append(
            OriginRun(
                side=event.side,
                pattern_known_at=event.known_at,
                anchor_known_at=post_start + TF_DELTA["H1"],
                anchor_price=anchor_price,
            )
        )
    return origins


def _consumed_points(active_m1: pd.DataFrame, origin: OriginRun, end: pd.Timestamp) -> float:
    path = active_m1.loc[(active_m1.index >= origin.anchor_known_at) & (active_m1.index < end)]
    if path.empty:
        return 0.0
    if origin.side == "BUY":
        return max(0.0, (float(path.high.max()) - origin.anchor_price) / PROJECT_POINT_SIZE)
    return max(0.0, (origin.anchor_price - float(path.low.min())) / PROJECT_POINT_SIZE)


def _first_candidate_by_day_side(events: list, start: pd.Timestamp, end: pd.Timestamp) -> dict[str, object]:
    found: dict[str, object] = {}
    for event in events:
        if not (start < event.known_at <= end):
            continue
        if event.side not in found:
            found[event.side] = event
    return found


def _decision(inherited: dict[str, object], control: dict[str, object]) -> str:
    if int(inherited["events"]) < MIN_GROUP or int(control["events"]) < MIN_GROUP:
        return "INCONCLUSIVE_INSUFFICIENT"
    keys = ["target_first_rate_resolved", "target_reach_rate_anywhere", "mfe_median", "mae_median"]
    vals = [inherited[k] for k in keys] + [control[k] for k in keys]
    if not all(isinstance(v, float) for v in vals):
        return "INCONCLUSIVE_INSUFFICIENT"
    support = (
        inherited["target_first_rate_resolved"] > control["target_first_rate_resolved"]
        and inherited["target_reach_rate_anywhere"] >= control["target_reach_rate_anywhere"]
        and inherited["mfe_median"] >= control["mfe_median"]
        and inherited["mae_median"] <= control["mae_median"]
    )
    oppose = (
        inherited["target_first_rate_resolved"] < control["target_first_rate_resolved"]
        and inherited["target_reach_rate_anywhere"] <= control["target_reach_rate_anywhere"]
        and inherited["mfe_median"] <= control["mfe_median"]
        and inherited["mae_median"] >= control["mae_median"]
    )
    if support:
        return "SUPPORTED"
    if oppose:
        return "NOT_SUPPORTED"
    return "INCONCLUSIVE_MIXED"


def run(*, m1_path: str | Path, metadata_path: str | Path | None, report_path: str | Path, events_path: str | Path) -> dict[str, object]:
    m1 = load_ohlc_csv(m1_path)
    active = m1[m1["volume"] > 0].copy()
    h1 = resample_ohlc(active, "H1")
    pat_events = _pat2_body_events(h1, "H1")
    origins = _build_origins(h1)
    missing = _load_missing_dates(metadata_path)
    rows: list[dict[str, object]] = []

    if h1.empty:
        raise ValueError("no active H1 bars")
    cutoff = h1.index.min().normalize()
    final = h1.index.max().normalize()
    while cutoff <= final:
        day_end = cutoff + pd.Timedelta(days=1)
        candidates = _first_candidate_by_day_side(pat_events, cutoff, day_end)
        for side, candidate_obj in candidates.items():
            candidate = candidate_obj
            future_h1 = h1.loc[h1.index >= candidate.known_at]
            if len(future_h1) < 24:
                continue
            horizon_end = future_h1.index[23] + TF_DELTA["H1"] - pd.Timedelta(minutes=1)
            if _intersects_missing(cutoff, horizon_end, missing):
                continue

            eligible = [o for o in origins if o.side == side and o.anchor_known_at <= cutoff]
            active_origin: OriginRun | None = None
            remaining_at_cutoff: float | None = None
            for origin in reversed(eligible):
                if _intersects_missing(origin.anchor_known_at, candidate.known_at, missing):
                    continue
                consumed_cutoff = _consumed_points(active, origin, cutoff)
                consumed_entry = _consumed_points(active, origin, candidate.known_at)
                if consumed_cutoff < H1_TARGET_POINTS and consumed_entry < H1_TARGET_POINTS:
                    active_origin = origin
                    remaining_at_cutoff = H1_TARGET_POINTS - consumed_cutoff
                    break

            fresh = measure_outcome(
                active,
                OutcomeSpec(
                    side=side,
                    reference_price=candidate.close,
                    known_at=candidate.known_at,
                    horizon_end=horizon_end,
                    point_size=PROJECT_POINT_SIZE,
                    target_points=H1_TARGET_POINTS,
                    stop_points=H1_TARGET_POINTS,
                ),
            )
            row: dict[str, object] = {
                "cutoff_utc": cutoff.isoformat(),
                "side": side,
                "candidate_known_at": candidate.known_at.isoformat(),
                "candidate_close": candidate.close,
                "state": "INHERITED_REMAINING_RUN" if active_origin else "NO_ACTIVE_INHERITED_RUN",
                "fresh_target_reached_anywhere": fresh.mfe_points >= H1_TARGET_POINTS,
                "fresh_first_hit": fresh.first_hit.value,
                "fresh_mfe_points": fresh.mfe_points,
                "fresh_mae_points": fresh.mae_points,
                "origin_anchor_known_at": active_origin.anchor_known_at.isoformat() if active_origin else None,
                "origin_anchor_price": active_origin.anchor_price if active_origin else None,
                "remaining_at_cutoff_points": remaining_at_cutoff,
            }
            if active_origin is not None:
                consumed_entry = _consumed_points(active, active_origin, candidate.known_at)
                path_remaining = H1_TARGET_POINTS - consumed_entry
                origin_target_price = active_origin.anchor_price + (H1_TARGET_POINTS * PROJECT_POINT_SIZE if side == "BUY" else -H1_TARGET_POINTS * PROJECT_POINT_SIZE)
                level_distance = ((origin_target_price - candidate.close) if side == "BUY" else (candidate.close - origin_target_price)) / PROJECT_POINT_SIZE
                path_remaining = max(PROJECT_POINT_SIZE, path_remaining)
                level_distance = max(PROJECT_POINT_SIZE, level_distance)
                path_out = measure_outcome(active, OutcomeSpec(side=side, reference_price=candidate.close, known_at=candidate.known_at, horizon_end=horizon_end, point_size=PROJECT_POINT_SIZE, target_points=path_remaining, stop_points=H1_TARGET_POINTS))
                level_out = measure_outcome(active, OutcomeSpec(side=side, reference_price=candidate.close, known_at=candidate.known_at, horizon_end=horizon_end, point_size=PROJECT_POINT_SIZE, target_points=level_distance, stop_points=H1_TARGET_POINTS))
                row.update({
                    "remaining_at_entry_points": path_remaining,
                    "origin_level_distance_at_entry_points": level_distance,
                    "path_remaining_reached": path_out.mfe_points >= path_remaining,
                    "path_remaining_first_hit": path_out.first_hit.value,
                    "origin_level_reached": level_out.mfe_points >= level_distance,
                    "origin_level_first_hit": level_out.first_hit.value,
                })
            rows.append(row)
        cutoff = day_end

    events = pd.DataFrame(rows)
    Path(events_path).parent.mkdir(parents=True, exist_ok=True)
    events.to_csv(events_path, index=False)
    inherited_rows = events[events["state"] == "INHERITED_REMAINING_RUN"].copy()
    control_rows = events[events["state"] == "NO_ACTIVE_INHERITED_RUN"].copy()
    rename = {"fresh_first_hit": "first_hit", "fresh_target_reached_anywhere": "target_reached_anywhere", "fresh_mfe_points": "mfe_points", "fresh_mae_points": "mae_points"}
    inherited_summary = _group_summary(inherited_rows.rename(columns=rename))
    control_summary = _group_summary(control_rows.rename(columns=rename))
    decision = _decision(inherited_summary, control_summary)

    path_reach = float(inherited_rows["path_remaining_reached"].mean()) if not inherited_rows.empty else None
    level_reach = float(inherited_rows["origin_level_reached"].mean()) if not inherited_rows.empty else None
    report = {
        "research_status": "H1_INHERITED_REMAINING_RUN_STATE_COMPONENT_TEST",
        "source_m1": str(m1_path),
        "source_metadata": str(metadata_path) if metadata_path else None,
        "time_mapping": "07:00 Asia/Bangkok = 00:00 UTC",
        "origin_proxy": "H1 PAT2 BODY research variant; PAT2 post-SIG anchor uses next adjacent H1 candle (#3), BUY=Low SELL=High",
        "daily_candidate_policy": "first post-cutoff H1 PAT2 BODY candidate per side per UTC day",
        "active_state": "latest same-direction pre-cutoff origin whose nominal H1 1000-point run is incomplete at both cutoff and candidate time",
        "decision_rule": "SUPPORTED only if inherited state beats no-active control on fresh-1000 target-first, reach and median MFE while median MAE is no higher; reverse all four => NOT_SUPPORTED; otherwise INCONCLUSIVE.",
        "decision": decision,
        "inherited_fresh1000": inherited_summary,
        "no_active_control_fresh1000": control_summary,
        "inherited_target_representation_descriptive": {
            "path_remaining_mean_reach": path_reach,
            "origin_target_level_mean_reach": level_reach,
            "guard": "Outcome differences cannot identify teacher intent between target representations."
        },
        "events": len(events),
        "inherited_events": len(inherited_rows),
        "control_events": len(control_rows),
        "limitations": [
            "PAT2 BODY is a research proxy, not canonical PA/SIG.",
            "Exact post-SIG destruction/invalidation rule is not applied.",
            "If multiple same-direction active origins exist, the latest eligible origin is used as a declared research variant.",
            "Daily Frame location is intentionally excluded from this first state-only component test.",
            "Fresh 1000-point symmetric adverse barrier is a research control, not canonical SL."
        ]
    }
    Path(report_path).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--m1", required=True)
    p.add_argument("--metadata", default=None)
    p.add_argument("--report", required=True)
    p.add_argument("--events", required=True)
    a = p.parse_args()
    report = run(m1_path=a.m1, metadata_path=a.metadata, report_path=a.report, events_path=a.events)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
