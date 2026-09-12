from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from nexus_xau.data.csv_loader import load_ohlc_csv

PROJECT_POINT_SIZE = 0.01
ELIGIBLE_TFS = ("H1", "H4")
VARIANT_ANY = "FIRST_ANY_PA_PROXY"
VARIANT_EXPECTED = "FIRST_EXPECTED_SIDE_PA_PROXY"
VARIANTS = (VARIANT_ANY, VARIANT_EXPECTED)


@dataclass(frozen=True, slots=True)
class BoundaryHit:
    target_at: pd.Timestamp | None
    point_check_at: pd.Timestamp | None
    first_hit: str


def _as_bool(series: pd.Series) -> pd.Series:
    if series.dtype == bool:
        return series
    mapping = {
        "true": True,
        "false": False,
        "1": True,
        "0": False,
        "yes": True,
        "no": False,
    }
    lowered = series.astype(str).str.strip().str.lower()
    mapped = lowered.map(mapping)
    if mapped.isna().any():
        bad = sorted(set(series[mapped.isna()].astype(str)))
        raise ValueError(f"Cannot normalize boolean values: {bad[:5]}")
    return mapped.astype(bool)


def _first_true_at(index: pd.DatetimeIndex, mask: np.ndarray) -> pd.Timestamp | None:
    if mask.size == 0 or not bool(mask.any()):
        return None
    return pd.Timestamp(index[int(mask.argmax())])


def _boundary_hit(
    *,
    path: pd.DataFrame,
    side: str,
    target_price: float,
    point_check_price: float,
) -> BoundaryHit:
    if path.empty:
        return BoundaryHit(None, None, "NEITHER")

    highs = path["high"].to_numpy(dtype=float, copy=False)
    lows = path["low"].to_numpy(dtype=float, copy=False)
    side = side.upper()
    if side == "BUY":
        target_mask = highs >= target_price
    elif side == "SELL":
        target_mask = lows <= target_price
    else:
        raise ValueError(f"Unsupported side: {side}")

    point_mask = (lows <= point_check_price) & (highs >= point_check_price)
    target_at = _first_true_at(path.index, target_mask)
    point_at = _first_true_at(path.index, point_mask)

    if target_at is None and point_at is None:
        first = "NEITHER"
    elif point_at is None:
        first = "TARGET_FIRST"
    elif target_at is None:
        first = "POINT_CHECK_FIRST"
    elif target_at == point_at:
        first = "AMBIGUOUS_SAME_BAR"
    elif target_at < point_at:
        first = "TARGET_FIRST"
    else:
        first = "POINT_CHECK_FIRST"
    return BoundaryHit(target_at, point_at, first)


def _absolute_origin_target(*, side: str, anchor: float, nominal_points: float) -> float:
    distance = nominal_points * PROJECT_POINT_SIZE
    if side.upper() == "BUY":
        return anchor + distance
    if side.upper() == "SELL":
        return anchor - distance
    raise ValueError(f"Unsupported side: {side}")


def _favorable_consumed(
    *,
    active_m1: pd.DataFrame,
    side: str,
    anchor: float,
    start: pd.Timestamp,
    end: pd.Timestamp,
) -> float:
    path = active_m1.loc[(active_m1.index >= start) & (active_m1.index < end)]
    if path.empty:
        return 0.0
    if side.upper() == "BUY":
        favorable = float(path["high"].max()) - anchor
    else:
        favorable = anchor - float(path["low"].min())
    return max(0.0, favorable / PROJECT_POINT_SIZE)


def _preconfirmation_terminal(
    *,
    active_m1: pd.DataFrame,
    side: str,
    anchor: float,
    nominal_points: float,
    cutoff: pd.Timestamp,
    confirmation_known_at: pd.Timestamp,
) -> BoundaryHit:
    path = active_m1.loc[
        (active_m1.index >= cutoff) & (active_m1.index < confirmation_known_at)
    ]
    target_price = _absolute_origin_target(
        side=side,
        anchor=anchor,
        nominal_points=nominal_points,
    )
    return _boundary_hit(
        path=path,
        side=side,
        target_price=target_price,
        point_check_price=anchor,
    )


def _preconfirmation_state(hit: BoundaryHit) -> str:
    if hit.first_hit == "TARGET_FIRST":
        return "ORIGIN_COMPLETED_BEFORE_CONFIRMATION"
    if hit.first_hit == "POINT_CHECK_FIRST":
        return "POINT_CHECK_DESTROYED_BEFORE_CONFIRMATION"
    if hit.first_hit == "AMBIGUOUS_SAME_BAR":
        return "AMBIGUOUS_PRECONFIRMATION_TERMINAL_SAME_BAR"
    return "ACTIVE_AT_CONFIRMATION"


def _mfe_mae(
    *,
    path: pd.DataFrame,
    side: str,
    reference_price: float,
) -> tuple[float | None, float | None]:
    if path.empty:
        return None, None
    if side.upper() == "BUY":
        mfe = (float(path["high"].max()) - reference_price) / PROJECT_POINT_SIZE
        mae = (reference_price - float(path["low"].min())) / PROJECT_POINT_SIZE
    else:
        mfe = (reference_price - float(path["low"].min())) / PROJECT_POINT_SIZE
        mae = (float(path["high"].max()) - reference_price) / PROJECT_POINT_SIZE
    return max(0.0, mfe), max(0.0, mae)


def _minutes_from(start: pd.Timestamp, event: pd.Timestamp | None) -> float | None:
    if event is None:
        return None
    return (event - start).total_seconds() / 60.0


def _select_confirmation(
    *,
    events: pd.DataFrame,
    variant: str,
) -> pd.Series | None:
    if events.empty:
        return None
    ordered = events.sort_values(["event_known_at", "event_tf", "event_id"])
    if variant == VARIANT_EXPECTED:
        ordered = ordered[ordered["frame_side"] == "EXPECTED_SIDE"]
    elif variant != VARIANT_ANY:
        raise ValueError(f"Unknown confirmation variant: {variant}")
    if ordered.empty:
        return None
    return ordered.iloc[0]


def _next_cutoff_map(day_state: pd.DataFrame) -> dict[str, pd.Timestamp | None]:
    ordered = day_state.copy()
    ordered["cutoff_utc"] = pd.to_datetime(ordered["cutoff_utc"], utc=True)
    ordered = ordered.sort_values("cutoff_utc")
    values = list(ordered["cutoff_utc"])
    result: dict[str, pd.Timestamp | None] = {}
    for index, row in ordered.reset_index(drop=True).iterrows():
        result[str(row["day_id"])] = values[index + 1] if index + 1 < len(values) else None
    return result


def build_q1_events(
    *,
    active_m1: pd.DataFrame,
    day_state: pd.DataFrame,
    origins: pd.DataFrame,
    confirmations: pd.DataFrame,
) -> pd.DataFrame:
    origins = origins.copy()
    origins["source_partial_survival_proxy"] = _as_bool(
        origins["source_partial_survival_proxy"]
    )
    origins = origins[
        origins["origin_tf"].isin(ELIGIBLE_TFS)
        & origins["source_partial_survival_proxy"]
        & origins["origin_validity_state"].eq(
            "INCOMPLETE_NOMINAL_RUN_RESEARCH_PROXY"
        )
    ].copy()
    if origins.empty:
        return pd.DataFrame()

    for column in ("cutoff_utc", "origin_known_at"):
        origins[column] = pd.to_datetime(origins[column], utc=True)

    confirmations = confirmations.copy()
    confirmations["event_known_at"] = pd.to_datetime(
        confirmations["event_known_at"], utc=True
    )
    next_cutoffs = _next_cutoff_map(day_state)

    confirmation_groups = {
        (str(day), str(side)): group.copy()
        for (day, side), group in confirmations.groupby(["day_id", "event_side"])
    }
    origins_by_day = {
        str(day): group.copy()
        for day, group in origins.groupby("day_id")
    }

    rows: list[dict[str, object]] = []
    for (day_id, side), context in origins.groupby(["day_id", "origin_side"]):
        day_id = str(day_id)
        side = str(side)
        all_day = origins_by_day[day_id]
        opposite = all_day[all_day["origin_side"] != side]
        context_tf_set = ",".join(sorted(set(context["origin_tf"])))
        context_id = f"{day_id}:{side}"
        candidate_events = confirmation_groups.get((day_id, side), pd.DataFrame())
        next_cutoff = next_cutoffs.get(day_id)

        for variant in VARIANTS:
            confirmation = _select_confirmation(
                events=candidate_events,
                variant=variant,
            )
            for origin in context.itertuples(index=False):
                base: dict[str, object] = {
                    "context_id": context_id,
                    "day_id": day_id,
                    "side": side,
                    "variant": variant,
                    "context_origin_count": len(context),
                    "context_origin_tf_set": context_tf_set,
                    "opposite_side_origin_count": len(opposite),
                    "direction_conflict_present": len(opposite) > 0,
                    "origin_id": str(origin.origin_id),
                    "origin_tf": str(origin.origin_tf),
                    "origin_known_at": pd.Timestamp(origin.origin_known_at).isoformat(),
                    "origin_anchor_price": float(origin.origin_anchor_price),
                    "nominal_run_points": float(origin.nominal_run_points),
                    "origin_age_hours_at_0700": float(origin.origin_age_hours),
                    "consumed_ratio_at_0700": float(origin.consumed_ratio_at_0700),
                    "remaining_points_at_0700": float(origin.remaining_points_at_0700),
                    "next_cutoff_utc": (
                        next_cutoff.isoformat() if next_cutoff is not None else None
                    ),
                }

                if confirmation is None:
                    base["candidate_state"] = "NO_CONFIRMATION_BEFORE_NEXT_0700"
                    rows.append(base)
                    continue

                known_at = pd.Timestamp(confirmation["event_known_at"])
                candidate_close = float(confirmation["pattern_close"])
                base.update(
                    {
                        "confirmation_event_id": str(confirmation["event_id"]),
                        "confirmation_event_tf": str(confirmation["event_tf"]),
                        "confirmation_known_at": known_at.isoformat(),
                        "confirmation_close": candidate_close,
                        "confirmation_frame_side": str(confirmation["frame_side"]),
                        "confirmation_signed_frame_distance_points": (
                            float(
                                confirmation[
                                    "signed_distance_to_valid_frame_side_points"
                                ]
                            )
                            if not pd.isna(
                                confirmation[
                                    "signed_distance_to_valid_frame_side_points"
                                ]
                            )
                            else None
                        ),
                        "alignment_count_exact": int(
                            confirmation["alignment_count_exact"]
                        ),
                        "aligned_tf_set_exact": str(
                            confirmation["aligned_tf_set_exact"]
                        ),
                    }
                )

                if next_cutoff is None:
                    base["candidate_state"] = "RIGHT_CENSORED_NO_NEXT_0700"
                    rows.append(base)
                    continue

                cutoff = pd.Timestamp(origin.cutoff_utc)
                anchor = float(origin.origin_anchor_price)
                nominal = float(origin.nominal_run_points)
                pre_hit = _preconfirmation_terminal(
                    active_m1=active_m1,
                    side=side,
                    anchor=anchor,
                    nominal_points=nominal,
                    cutoff=cutoff,
                    confirmation_known_at=known_at,
                )
                pre_state = _preconfirmation_state(pre_hit)
                base.update(
                    {
                        "preconfirmation_state": pre_state,
                        "preconfirmation_target_at": (
                            pre_hit.target_at.isoformat()
                            if pre_hit.target_at is not None
                            else None
                        ),
                        "preconfirmation_point_check_at": (
                            pre_hit.point_check_at.isoformat()
                            if pre_hit.point_check_at is not None
                            else None
                        ),
                    }
                )
                if pre_state != "ACTIVE_AT_CONFIRMATION":
                    base["candidate_state"] = pre_state
                    rows.append(base)
                    continue

                consumed = _favorable_consumed(
                    active_m1=active_m1,
                    side=side,
                    anchor=anchor,
                    start=pd.Timestamp(origin.origin_known_at),
                    end=known_at,
                )
                remaining = nominal - consumed
                if remaining <= 0:
                    base["candidate_state"] = "ORIGIN_COMPLETED_BEFORE_CONFIRMATION"
                    rows.append(base)
                    continue

                origin_target_price = _absolute_origin_target(
                    side=side,
                    anchor=anchor,
                    nominal_points=nominal,
                )
                if side == "BUY":
                    path_target_price = candidate_close + remaining * PROJECT_POINT_SIZE
                    origin_target_distance = (
                        origin_target_price - candidate_close
                    ) / PROJECT_POINT_SIZE
                else:
                    path_target_price = candidate_close - remaining * PROJECT_POINT_SIZE
                    origin_target_distance = (
                        candidate_close - origin_target_price
                    ) / PROJECT_POINT_SIZE

                post_path = active_m1.loc[
                    (active_m1.index >= known_at)
                    & (active_m1.index < next_cutoff)
                ]
                path_hit = _boundary_hit(
                    path=post_path,
                    side=side,
                    target_price=path_target_price,
                    point_check_price=anchor,
                )
                origin_hit = _boundary_hit(
                    path=post_path,
                    side=side,
                    target_price=origin_target_price,
                    point_check_price=anchor,
                )
                mfe, mae = _mfe_mae(
                    path=post_path,
                    side=side,
                    reference_price=candidate_close,
                )

                base.update(
                    {
                        "candidate_state": "SCORED",
                        "consumed_points_before_confirmation": consumed,
                        "remaining_points_at_confirmation": remaining,
                        "origin_target_price": origin_target_price,
                        "origin_target_distance_at_confirmation_points": (
                            origin_target_distance
                        ),
                        "path_remaining_target_price": path_target_price,
                        "post_confirmation_mfe_points": mfe,
                        "post_confirmation_mae_points": mae,
                        "path_remaining_first_hit": path_hit.first_hit.replace(
                            "NEITHER", "NEITHER_BEFORE_NEXT_0700"
                        ),
                        "path_remaining_target_at": (
                            path_hit.target_at.isoformat()
                            if path_hit.target_at is not None
                            else None
                        ),
                        "path_remaining_point_check_at": (
                            path_hit.point_check_at.isoformat()
                            if path_hit.point_check_at is not None
                            else None
                        ),
                        "path_remaining_time_to_target_minutes": _minutes_from(
                            known_at, path_hit.target_at
                        ),
                        "path_remaining_time_to_point_check_minutes": _minutes_from(
                            known_at, path_hit.point_check_at
                        ),
                        "origin_level_first_hit": origin_hit.first_hit.replace(
                            "NEITHER", "NEITHER_BEFORE_NEXT_0700"
                        ),
                        "origin_level_target_at": (
                            origin_hit.target_at.isoformat()
                            if origin_hit.target_at is not None
                            else None
                        ),
                        "origin_level_point_check_at": (
                            origin_hit.point_check_at.isoformat()
                            if origin_hit.point_check_at is not None
                            else None
                        ),
                        "origin_level_time_to_target_minutes": _minutes_from(
                            known_at, origin_hit.target_at
                        ),
                        "origin_level_time_to_point_check_minutes": _minutes_from(
                            known_at, origin_hit.point_check_at
                        ),
                    }
                )
                rows.append(base)

    events = pd.DataFrame(rows)
    if events.empty:
        return events
    return events.sort_values(
        ["day_id", "side", "variant", "origin_tf", "origin_id"]
    ).reset_index(drop=True)


def _category_counts(series: pd.Series) -> dict[str, int]:
    return {
        str(key): int(value)
        for key, value in series.value_counts(dropna=False).to_dict().items()
    }


def _scored_summary(group: pd.DataFrame, column: str) -> dict[str, object]:
    if group.empty:
        return {"origin_rows": 0, "contexts": 0, "first_hit_counts": {}}
    return {
        "origin_rows": len(group),
        "contexts": int(group["context_id"].nunique()),
        "first_hit_counts": _category_counts(group[column]),
        "mfe_median": (
            float(group["post_confirmation_mfe_points"].median())
            if group["post_confirmation_mfe_points"].notna().any()
            else None
        ),
        "mae_median": (
            float(group["post_confirmation_mae_points"].median())
            if group["post_confirmation_mae_points"].notna().any()
            else None
        ),
    }


def _group_summaries(scored: pd.DataFrame) -> dict[str, object]:
    dimensions = (
        "origin_tf",
        "context_origin_tf_set",
        "direction_conflict_present",
        "confirmation_frame_side",
        "confirmation_event_tf",
        "alignment_count_exact",
    )
    out: dict[str, object] = {}
    for dimension in dimensions:
        rows: dict[str, object] = {}
        for value, group in scored.groupby(dimension, dropna=False):
            rows[str(value)] = {
                "origin_rows": len(group),
                "contexts": int(group["context_id"].nunique()),
                "path_remaining": _category_counts(
                    group["path_remaining_first_hit"]
                ),
                "origin_level": _category_counts(group["origin_level_first_hit"]),
                "mfe_median": float(group["post_confirmation_mfe_points"].median()),
                "mae_median": float(group["post_confirmation_mae_points"].median()),
            }
        out[dimension] = rows
    return out


def summarize_q1(events: pd.DataFrame) -> dict[str, object]:
    if events.empty:
        return {"rows": 0, "contexts": 0}
    variants: dict[str, object] = {}
    for variant, group in events.groupby("variant"):
        scored = group[group["candidate_state"] == "SCORED"].copy()
        variants[str(variant)] = {
            "origin_rows": len(group),
            "contexts": int(group["context_id"].nunique()),
            "candidate_state_counts": _category_counts(group["candidate_state"]),
            "scored_rows": len(scored),
            "scored_contexts": int(scored["context_id"].nunique()),
            "path_remaining": _scored_summary(
                scored, "path_remaining_first_hit"
            ),
            "origin_level": _scored_summary(scored, "origin_level_first_hit"),
            "groups": _group_summaries(scored),
        }
    return {
        "rows": len(events),
        "contexts": int(events["context_id"].nunique()),
        "origins": int(events["origin_id"].nunique()),
        "variants": variants,
    }


def run(
    *,
    m1_path: str | Path,
    day_state_path: str | Path,
    origin_candidates_path: str | Path,
    confirmation_events_path: str | Path,
    output_root: str | Path,
) -> dict[str, object]:
    m1 = load_ohlc_csv(m1_path)
    active = m1[m1["volume"] > 0].copy() if "volume" in m1.columns else m1.copy()
    day_state = pd.read_csv(day_state_path)
    origins = pd.read_csv(origin_candidates_path)
    confirmations = pd.read_csv(confirmation_events_path)

    events = build_q1_events(
        active_m1=active,
        day_state=day_state,
        origins=origins,
        confirmations=confirmations,
    )
    summary = summarize_q1(events)
    report: dict[str, object] = {
        "research_status": "0700_Q1_ORIGIN_CONTEXT_DISCOVERY_DESCRIPTIVE_ONLY",
        "source_m1": str(m1_path),
        "source_day_state": str(day_state_path),
        "source_origin_candidates": str(origin_candidates_path),
        "source_confirmation_events": str(confirmation_events_path),
        "confirmation_variants": list(VARIANTS),
        "horizon": "selected confirmation known_at -> next active 07:00 Thailand boundary",
        "target_representations": [
            "PATH_REMAINING_AT_CONFIRMATION",
            "ORIGIN_TARGET_LEVEL",
        ],
        "point_check_boundary": "proxy origin anchor literal M1 range contact",
        "summary": summary,
        "guards": [
            "Discovery only; no production rule or threshold is selected.",
            "PAT2 BODY and origin anchors remain research proxies.",
            "Rows sharing day_id+side context are not independent trials.",
            "D1 is excluded from scoring because exact D run distance is unresolved.",
            "No broker fill, spread, slippage, P&L, trade Win/Loss, or system Win rate is computed.",
            "Same-bar target/point-check ordering remains AMBIGUOUS_SAME_BAR.",
            "Pre-confirmation completion/destruction is retained rather than silently excluded.",
            "Historical outcome differences cannot identify instructor intent.",
        ],
    }

    root = Path(output_root)
    root.mkdir(parents=True, exist_ok=True)
    events.to_csv(root / "Q1_ORIGIN_CONTEXT_EVENTS.csv", index=False)
    (root / "REPORT.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--m1", required=True)
    parser.add_argument("--day-state", required=True)
    parser.add_argument("--origins", required=True)
    parser.add_argument("--confirmations", required=True)
    parser.add_argument("--output-root", required=True)
    args = parser.parse_args()
    report = run(
        m1_path=args.m1,
        day_state_path=args.day_state,
        origin_candidates_path=args.origins,
        confirmation_events_path=args.confirmations,
        output_root=args.output_root,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
