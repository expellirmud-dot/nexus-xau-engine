from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path

import numpy as np
import pandas as pd

from nexus_xau.data.csv_loader import load_ohlc_csv
from nexus_xau.data.resample import resample_ohlc
from nexus_xau.engine.mae_pla_frame import build_mae_pla_frame_candidates

PROJECT_POINT_SIZE = 0.01
H4_RUN_POINTS = 1500.0
H4_DELTA = timedelta(hours=4)
M5_DELTA = timedelta(minutes=5)


@dataclass(frozen=True, slots=True)
class Pat2Event:
    timeframe: str
    side: str
    previous_bar_start: pd.Timestamp
    pattern_bar_start: pd.Timestamp
    known_at: pd.Timestamp
    close: float
    pattern_low: float
    pattern_high: float


@dataclass(frozen=True, slots=True)
class H4Origin:
    origin_id: str
    side: str
    pattern_known_at: pd.Timestamp
    origin_known_at: pd.Timestamp
    anchor_price: float


@dataclass(frozen=True, slots=True)
class BoundaryHit:
    target_at: pd.Timestamp | None
    point_check_at: pd.Timestamp | None
    first_hit: str


def _bullish(row: pd.Series) -> bool:
    return float(row.close) > float(row.open)


def _bearish(row: pd.Series) -> bool:
    return float(row.close) < float(row.open)


def detect_pat2_full_range(frame: pd.DataFrame, timeframe: str) -> list[Pat2Event]:
    """Detect the frozen V2 PAT2 FULL-RANGE research representation."""
    delta = {"H4": H4_DELTA, "M5": M5_DELTA}[timeframe]
    events: list[Pat2Event] = []
    for i in range(1, len(frame)):
        previous = frame.iloc[i - 1]
        current = frame.iloc[i]
        previous_ts = pd.Timestamp(frame.index[i - 1])
        current_ts = pd.Timestamp(frame.index[i])
        if current_ts - previous_ts != delta:
            continue

        midpoint = (float(previous.high) + float(previous.low)) / 2.0
        side: str | None = None
        if _bearish(previous) and _bullish(current) and float(current.close) > midpoint:
            side = "BUY"
        elif _bullish(previous) and _bearish(current) and float(current.close) < midpoint:
            side = "SELL"
        if side is None:
            continue

        events.append(
            Pat2Event(
                timeframe=timeframe,
                side=side,
                previous_bar_start=previous_ts,
                pattern_bar_start=current_ts,
                known_at=current_ts + delta,
                close=float(current.close),
                pattern_low=min(float(previous.low), float(current.low)),
                pattern_high=max(float(previous.high), float(current.high)),
            )
        )
    return events


def build_h4_origins(frame: pd.DataFrame, events: list[Pat2Event]) -> list[H4Origin]:
    """Map H4 PAT2 events to the frozen adjacent post-SIG research anchor."""
    origins: list[H4Origin] = []
    for event in events:
        post_sig_start = event.known_at
        if post_sig_start not in frame.index:
            continue
        post_sig = frame.loc[post_sig_start]
        origin_known_at = post_sig_start + H4_DELTA
        anchor = float(post_sig.low if event.side == "BUY" else post_sig.high)
        origins.append(
            H4Origin(
                origin_id=(
                    f"H4:{event.side}:"
                    f"{origin_known_at.isoformat().replace('+00:00', 'Z')}"
                ),
                side=event.side,
                pattern_known_at=event.known_at,
                origin_known_at=origin_known_at,
                anchor_price=anchor,
            )
        )
    return origins


def _sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_metadata(path: str | Path | None) -> dict[str, object]:
    if path is None:
        return {}
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _first_true_at(index: pd.DatetimeIndex, mask: np.ndarray) -> pd.Timestamp | None:
    if mask.size == 0 or not bool(mask.any()):
        return None
    return pd.Timestamp(index[int(mask.argmax())])


def boundary_hit(
    *,
    path: pd.DataFrame,
    side: str,
    target_price: float,
    point_check_price: float,
) -> BoundaryHit:
    if path.empty:
        return BoundaryHit(None, None, "NEITHER_BY_NEXT_0700")

    highs = path["high"].to_numpy(dtype=float, copy=False)
    lows = path["low"].to_numpy(dtype=float, copy=False)
    if side == "BUY":
        target_mask = highs >= target_price
    elif side == "SELL":
        target_mask = lows <= target_price
    else:
        raise ValueError(f"unsupported side: {side}")

    point_mask = (lows <= point_check_price) & (highs >= point_check_price)
    target_at = _first_true_at(path.index, target_mask)
    point_at = _first_true_at(path.index, point_mask)

    if target_at is None and point_at is None:
        first = "NEITHER_BY_NEXT_0700"
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


def favorable_consumed_points(
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
    if side == "BUY":
        favorable = float(path["high"].max()) - anchor
    elif side == "SELL":
        favorable = anchor - float(path["low"].min())
    else:
        raise ValueError(f"unsupported side: {side}")
    return max(0.0, favorable / PROJECT_POINT_SIZE)


def first_point_check_touch(
    *,
    active_m1: pd.DataFrame,
    anchor: float,
    start: pd.Timestamp,
    end: pd.Timestamp | None = None,
) -> pd.Timestamp | None:
    path = active_m1.loc[active_m1.index >= start]
    if end is not None:
        path = path.loc[path.index < end]
    if path.empty:
        return None
    mask = (path["low"].to_numpy(dtype=float) <= anchor) & (
        path["high"].to_numpy(dtype=float) >= anchor
    )
    return _first_true_at(path.index, mask)


def origin_state_at(
    *,
    active_m1: pd.DataFrame,
    origin: H4Origin,
    at: pd.Timestamp,
) -> tuple[str, float, float, pd.Timestamp | None]:
    path = active_m1.loc[
        (active_m1.index >= origin.origin_known_at) & (active_m1.index < at)
    ]
    target_price = (
        origin.anchor_price + H4_RUN_POINTS * PROJECT_POINT_SIZE
        if origin.side == "BUY"
        else origin.anchor_price - H4_RUN_POINTS * PROJECT_POINT_SIZE
    )
    hit = boundary_hit(
        path=path,
        side=origin.side,
        target_price=target_price,
        point_check_price=origin.anchor_price,
    )
    consumed = favorable_consumed_points(
        active_m1=active_m1,
        side=origin.side,
        anchor=origin.anchor_price,
        start=origin.origin_known_at,
        end=at,
    )
    remaining = max(0.0, H4_RUN_POINTS - consumed)

    if hit.first_hit == "TARGET_FIRST":
        return "RUN_COMPLETE", consumed, remaining, hit.point_check_at
    if hit.first_hit == "POINT_CHECK_FIRST":
        return "POINT_CHECK_DESTROYED", consumed, remaining, hit.point_check_at
    if hit.first_hit == "AMBIGUOUS_SAME_BAR":
        return "AMBIGUOUS_TERMINAL_SAME_BAR", consumed, remaining, hit.point_check_at
    return "ACTIVE", consumed, remaining, None


def _frame_relation(
    *, event: Pat2Event, lower: float, upper: float
) -> tuple[str, float]:
    if event.side == "BUY":
        signed = (event.pattern_low - lower) / PROJECT_POINT_SIZE
    else:
        signed = (upper - event.pattern_high) / PROJECT_POINT_SIZE
    return (
        "EXPECTED_SIDE_RESEARCH_PROXY" if signed >= 0 else "CROSSED_SIDE_RESEARCH_PROXY",
        float(signed),
    )


def _cutoffs(active_m1: pd.DataFrame) -> list[pd.Timestamp]:
    mask = (
        (active_m1.index.hour == 0)
        & (active_m1.index.minute == 0)
        & (active_m1.index.second == 0)
    )
    return [pd.Timestamp(x) for x in active_m1.index[mask].sort_values().unique()]


def _day_frame_row(
    *, cutoff: pd.Timestamp, active_m1: pd.DataFrame
) -> dict[str, object]:
    price = float(active_m1.loc[cutoff, "open"])
    frame = build_mae_pla_frame_candidates(price)
    refs = [float(x.reference_price) for x in frame.candidates]
    uppers = [float(x.upper_price) for x in frame.candidates]
    lowers = [float(x.lower_price) for x in frame.candidates]
    unique = len(refs) == 1
    return {
        "day_id": cutoff.strftime("%Y-%m-%d"),
        "cutoff_utc": cutoff.isoformat(),
        "cutoff_thailand": cutoff.tz_convert("Asia/Bangkok").isoformat(),
        "price_at_cutoff": price,
        "daily_frame_candidate_count": len(refs),
        "daily_frame_reference_candidates": json.dumps(refs),
        "daily_frame_upper_candidates": json.dumps(uppers),
        "daily_frame_lower_candidates": json.dumps(lowers),
        "daily_frame_reference": refs[0] if unique else None,
        "daily_frame_upper": uppers[0] if unique else None,
        "daily_frame_lower": lowers[0] if unique else None,
        "daily_frame_tie_ambiguous": not unique,
    }


def _first_m5_confirmation(
    *,
    events: list[Pat2Event],
    side: str,
    cutoff: pd.Timestamp,
    next_cutoff: pd.Timestamp,
) -> Pat2Event | None:
    candidates = [
        e
        for e in events
        if e.side == side and cutoff < e.known_at < next_cutoff
    ]
    if not candidates:
        return None
    return min(candidates, key=lambda e: e.known_at)


def action_state_for_candidate(
    *, same_side_origin_count: int, opposite_side_origin_count: int
) -> str:
    if same_side_origin_count > 1 or opposite_side_origin_count > 0:
        return "PASS_CONFLICT_UNRESOLVED"
    return "PASS_SOURCE_GEOMETRY_UNRESOLVED"


def _target_price_from_confirmation(
    *, side: str, confirmation_close: float, remaining_points: float
) -> float:
    distance = remaining_points * PROJECT_POINT_SIZE
    if side == "BUY":
        return confirmation_close + distance
    return confirmation_close - distance


def build_minimal_v2(
    *,
    m1_path: str | Path,
    metadata_path: str | Path | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, object]]:
    m1 = load_ohlc_csv(m1_path)
    active_m1 = m1[m1["volume"] > 0].copy() if "volume" in m1.columns else m1.copy()
    if active_m1.empty:
        raise ValueError("no active M1 rows")

    metadata = _load_metadata(metadata_path)
    h4 = resample_ohlc(active_m1, "H4")
    m5 = resample_ohlc(active_m1, "M5")
    h4_events = detect_pat2_full_range(h4, "H4")
    m5_events = detect_pat2_full_range(m5, "M5")
    origins = build_h4_origins(h4, h4_events)
    cutoffs = _cutoffs(active_m1)

    day_rows: list[dict[str, object]] = []
    origin_rows: list[dict[str, object]] = []
    event_rows: list[dict[str, object]] = []

    for i, cutoff in enumerate(cutoffs):
        day = _day_frame_row(cutoff=cutoff, active_m1=active_m1)
        next_cutoff = cutoffs[i + 1] if i + 1 < len(cutoffs) else None
        known_origins = [o for o in origins if o.origin_known_at <= cutoff]
        eligible: list[tuple[H4Origin, float, float]] = []

        for origin in known_origins:
            state, consumed, remaining, touch = origin_state_at(
                active_m1=active_m1,
                origin=origin,
                at=cutoff,
            )
            if state != "ACTIVE":
                continue
            eligible.append((origin, consumed, remaining))
            origin_rows.append(
                {
                    "day_id": day["day_id"],
                    "cutoff_utc": day["cutoff_utc"],
                    "origin_id": origin.origin_id,
                    "origin_side": origin.side,
                    "origin_known_at": origin.origin_known_at.isoformat(),
                    "origin_anchor_price": origin.anchor_price,
                    "origin_detector": "H4_PAT2_FULL_RANGE_POST_SIG_PROXY_V2",
                    "origin_source_class": "RESEARCH_REPRESENTATION",
                    "origin_state_0700": state,
                    "consumed_points_at_0700": consumed,
                    "consumed_ratio_at_0700": consumed / H4_RUN_POINTS,
                    "remaining_points_at_0700": remaining,
                    "point_check_touch_before_0700": (
                        touch.isoformat() if touch is not None else None
                    ),
                }
            )

        day["eligible_h4_origin_count"] = len(eligible)
        day["eligible_h4_buy_count"] = sum(1 for o, _, _ in eligible if o.side == "BUY")
        day["eligible_h4_sell_count"] = sum(1 for o, _, _ in eligible if o.side == "SELL")

        if bool(day["daily_frame_tie_ambiguous"]):
            day["research_day_state"] = "PASS_FRAME_TIE"
            day["action_day_state"] = "PASS_FRAME_TIE"
            day_rows.append(day)
            continue

        if not eligible:
            day["research_day_state"] = "PASS_NO_H4_ORIGIN"
            day["action_day_state"] = "PASS_NO_H4_ORIGIN"
            day_rows.append(day)
            continue

        if next_cutoff is None:
            day["research_day_state"] = "PASS_DATA_QUALITY"
            day["action_day_state"] = "PASS_DATA_QUALITY"
            day_rows.append(day)
            continue

        day_candidate_count = 0
        terminal_reasons: list[str] = []
        for origin, consumed_0700, remaining_0700 in eligible:
            confirmation = _first_m5_confirmation(
                events=m5_events,
                side=origin.side,
                cutoff=cutoff,
                next_cutoff=next_cutoff,
            )
            base: dict[str, object] = {
                "day_id": day["day_id"],
                "cutoff_utc": day["cutoff_utc"],
                "next_cutoff_utc": next_cutoff.isoformat(),
                "origin_id": origin.origin_id,
                "side": origin.side,
                "origin_known_at": origin.origin_known_at.isoformat(),
                "origin_anchor_price": origin.anchor_price,
                "consumed_points_at_0700": consumed_0700,
                "consumed_ratio_at_0700": consumed_0700 / H4_RUN_POINTS,
                "remaining_points_at_0700": remaining_0700,
                "same_side_eligible_origin_count": sum(
                    1 for other, _, _ in eligible if other.side == origin.side
                ),
                "opposite_side_eligible_origin_count": sum(
                    1 for other, _, _ in eligible if other.side != origin.side
                ),
                "daily_frame_tie_ambiguous": False,
            }
            if confirmation is None:
                base["candidate_state"] = "PASS_NO_M5_PAT2_CONFIRMATION"
                base["action_state"] = "PASS_NO_M5_PAT2_CONFIRMATION"
                terminal_reasons.append("PASS_NO_M5_PAT2_CONFIRMATION")
                event_rows.append(base)
                continue

            pre_state, _, _, pre_touch = origin_state_at(
                active_m1=active_m1,
                origin=origin,
                at=confirmation.known_at,
            )
            base.update(
                {
                    "confirmation_event_id": (
                        f"M5:{confirmation.side}:"
                        f"{confirmation.known_at.isoformat().replace('+00:00', 'Z')}"
                    ),
                    "confirmation_known_at": confirmation.known_at.isoformat(),
                    "confirmation_close": confirmation.close,
                    "confirmation_pattern_low": confirmation.pattern_low,
                    "confirmation_pattern_high": confirmation.pattern_high,
                    "preconfirmation_origin_state": pre_state,
                    "preconfirmation_point_check_touch_at": (
                        pre_touch.isoformat() if pre_touch is not None else None
                    ),
                }
            )
            if pre_state == "POINT_CHECK_DESTROYED":
                base["candidate_state"] = "PASS_ORIGIN_DESTROYED_BEFORE_CONFIRMATION"
                base["action_state"] = "PASS_ORIGIN_DESTROYED_BEFORE_CONFIRMATION"
                terminal_reasons.append("PASS_ORIGIN_DESTROYED_BEFORE_CONFIRMATION")
                event_rows.append(base)
                continue
            if pre_state == "RUN_COMPLETE":
                base["candidate_state"] = "PASS_RUN_COMPLETED_BEFORE_CONFIRMATION"
                base["action_state"] = "PASS_RUN_COMPLETED_BEFORE_CONFIRMATION"
                terminal_reasons.append("PASS_RUN_COMPLETED_BEFORE_CONFIRMATION")
                event_rows.append(base)
                continue
            if pre_state == "AMBIGUOUS_TERMINAL_SAME_BAR":
                base["candidate_state"] = "PASS_UNKNOWN_STATE"
                base["action_state"] = "PASS_UNKNOWN_STATE"
                terminal_reasons.append("PASS_UNKNOWN_STATE")
                event_rows.append(base)
                continue

            consumed_confirmation = favorable_consumed_points(
                active_m1=active_m1,
                side=origin.side,
                anchor=origin.anchor_price,
                start=origin.origin_known_at,
                end=confirmation.known_at,
            )
            remaining_confirmation = H4_RUN_POINTS - consumed_confirmation
            if remaining_confirmation <= 0:
                base["candidate_state"] = "PASS_RUN_COMPLETED_BEFORE_CONFIRMATION"
                base["action_state"] = "PASS_RUN_COMPLETED_BEFORE_CONFIRMATION"
                terminal_reasons.append("PASS_RUN_COMPLETED_BEFORE_CONFIRMATION")
                event_rows.append(base)
                continue

            frame_relation, frame_distance = _frame_relation(
                event=confirmation,
                lower=float(day["daily_frame_lower"]),
                upper=float(day["daily_frame_upper"]),
            )
            target_price = _target_price_from_confirmation(
                side=origin.side,
                confirmation_close=confirmation.close,
                remaining_points=remaining_confirmation,
            )
            post = active_m1.loc[
                (active_m1.index >= confirmation.known_at)
                & (active_m1.index < next_cutoff)
            ]
            hit = boundary_hit(
                path=post,
                side=origin.side,
                target_price=target_price,
                point_check_price=origin.anchor_price,
            )
            same_side_count = int(base["same_side_eligible_origin_count"])
            opposite_count = int(base["opposite_side_eligible_origin_count"])
            action_state = action_state_for_candidate(
                same_side_origin_count=same_side_count,
                opposite_side_origin_count=opposite_count,
            )

            base.update(
                {
                    "candidate_state": "RESEARCH_CANDIDATE",
                    "action_state": action_state,
                    "location_qualification_state": "UNKNOWN",
                    "frame_relation_research_proxy": frame_relation,
                    "signed_frame_distance_points": frame_distance,
                    "confirmation_reference": "M5_PAT2_CLOSE_RESEARCH_CONVENTION",
                    "consumed_points_at_confirmation": consumed_confirmation,
                    "remaining_points_at_confirmation": remaining_confirmation,
                    "path_remaining_target_price": target_price,
                    "path_remaining_first_hit": hit.first_hit,
                    "path_remaining_target_at": (
                        hit.target_at.isoformat() if hit.target_at is not None else None
                    ),
                    "path_remaining_point_check_at": (
                        hit.point_check_at.isoformat()
                        if hit.point_check_at is not None
                        else None
                    ),
                }
            )
            event_rows.append(base)
            day_candidate_count += 1

        if day_candidate_count > 0:
            day["research_day_state"] = "RESEARCH_CANDIDATE"
            candidate_actions = [
                str(row["action_state"])
                for row in event_rows
                if row.get("day_id") == day["day_id"]
                and row.get("candidate_state") == "RESEARCH_CANDIDATE"
            ]
            day["action_day_state"] = (
                "PASS_CONFLICT_UNRESOLVED"
                if "PASS_CONFLICT_UNRESOLVED" in candidate_actions
                else "PASS_SOURCE_GEOMETRY_UNRESOLVED"
            )
        elif terminal_reasons:
            day["research_day_state"] = terminal_reasons[0]
            day["action_day_state"] = terminal_reasons[0]
        else:
            day["research_day_state"] = "PASS_UNKNOWN_STATE"
            day["action_day_state"] = "PASS_UNKNOWN_STATE"
        day_rows.append(day)

    days_df = pd.DataFrame(day_rows)
    origins_df = pd.DataFrame(origin_rows)
    events_df = pd.DataFrame(event_rows)

    report: dict[str, object] = {
        "version": "0700_MINIMAL_V2.0",
        "research_status": "FROZEN_SPEC_IMPLEMENTATION_SIGNAL_RUN_ONLY",
        "source_m1": str(m1_path),
        "source_metadata": str(metadata_path) if metadata_path else None,
        "source_sha256": metadata.get("sha256") or _sha256(m1_path),
        "time_mapping": "07:00 Asia/Bangkok = 00:00 UTC",
        "rows": {
            "days": len(days_df),
            "eligible_origin_rows": len(origins_df),
            "event_rows": len(events_df),
        },
        "detectors": {
            "origin": "H4_PAT2_FULL_RANGE_POST_SIG_PROXY_V2",
            "confirmation": "M5_PAT2_FULL_RANGE_SOURCE_CLOSED",
            "pat2_midpoint": "(prior.high + prior.low) / 2",
            "strict_midpoint_pass": True,
        },
        "nominal_h4_run_points": H4_RUN_POINTS,
        "location_action_state": "FAIL_CLOSED_UNKNOWN_UNLESS_EXTERNAL_SOURCE_COMPATIBLE_LABEL",
        "guards": [
            "No consumed-ratio threshold is applied.",
            "PAT3/H1/D1 origins are excluded.",
            "Research location proxy is not canonical location qualification.",
            "Action lane fails closed on unresolved location geometry and unresolved origin conflict.",
            "No broker fill, spread, slippage, trade P&L, or system Win Rate is computed.",
            "Same-bar target and point-check is AMBIGUOUS_SAME_BAR.",
            "Next-07:00 horizon is a research accounting convention, not source expiry.",
            "This module does not rewrite historical V1/Q1-Q4 results.",
        ],
    }
    return days_df, origins_df, events_df, report


def summarize_report(
    days: pd.DataFrame,
    events: pd.DataFrame,
    report: dict[str, object],
) -> dict[str, object]:
    out = dict(report)
    if not days.empty:
        out["day_state_counts"] = {
            str(k): int(v)
            for k, v in days["research_day_state"].value_counts().to_dict().items()
        }
        out["action_day_state_counts"] = {
            str(k): int(v)
            for k, v in days["action_day_state"].value_counts().to_dict().items()
        }
    if not events.empty:
        out["candidate_state_counts"] = {
            str(k): int(v)
            for k, v in events["candidate_state"].value_counts().to_dict().items()
        }
        scored = events[events["candidate_state"].eq("RESEARCH_CANDIDATE")]
        out["research_candidate_rows"] = len(scored)
        if not scored.empty:
            out["path_remaining_first_hit_counts"] = {
                str(k): int(v)
                for k, v in scored["path_remaining_first_hit"].value_counts().to_dict().items()
            }
    return out


def run(
    *,
    m1_path: str | Path,
    metadata_path: str | Path | None,
    output_root: str | Path,
) -> dict[str, object]:
    days, origins, events, report = build_minimal_v2(
        m1_path=m1_path,
        metadata_path=metadata_path,
    )
    report = summarize_report(days, events, report)
    root = Path(output_root)
    root.mkdir(parents=True, exist_ok=True)
    days.to_csv(root / "0700_v2_day_state.csv", index=False)
    origins.to_csv(root / "0700_v2_origin_context.csv", index=False)
    events.to_csv(root / "0700_v2_research_events.csv", index=False)
    (root / "REPORT.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--m1", required=True)
    parser.add_argument("--metadata", default=None)
    parser.add_argument("--output-root", required=True)
    args = parser.parse_args()
    report = run(
        m1_path=args.m1,
        metadata_path=args.metadata,
        output_root=args.output_root,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
