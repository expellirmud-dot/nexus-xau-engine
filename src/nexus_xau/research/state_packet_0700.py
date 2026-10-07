from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import pandas as pd

from nexus_xau.data.resample import resample_ohlc
from nexus_xau.engine.mae_pla_frame import build_mae_pla_frame_candidates
from nexus_xau.replay.v2_integration import DATA_EXCLUDED_ORIGIN_HISTORY_UNSEEDED
from nexus_xau.research.minimal_v2_0700 import (
    H4_RUN_POINTS,
    _normalize_m1_frame,
    boundary_hit,
    build_h4_origins,
    detect_pat2_full_range,
    favorable_consumed_points,
    fixed_origin_target_price,
)

PACKET_VERSION = "0700_STATE_PACKET_H4_V0"
SCOPE = "H4_ORIGIN_STATE_AT_0700_ONLY"

INIT_SOURCE_PURE = "SOURCE_PURE"
INIT_OPERATIONAL_EXPLICIT_EPOCH = "OPERATIONAL_EXPLICIT_EPOCH"
INITIALIZATION_MODES = {
    INIT_SOURCE_PURE,
    INIT_OPERATIONAL_EXPLICIT_EPOCH,
}

COMPLETE_WITHIN_OPERATIONAL_EPOCH = "COMPLETE_WITHIN_DECLARED_OPERATIONAL_EPOCH"
UNKNOWN_PREHISTORY = "UNKNOWN_PREHISTORY"

THAILAND = ZoneInfo("Asia/Bangkok")


class StatePacketError(ValueError):
    pass


def _utc(value: pd.Timestamp | str) -> pd.Timestamp:
    timestamp = pd.Timestamp(value)
    if timestamp.tz is None:
        raise StatePacketError("timestamp must be timezone-aware")
    return timestamp.tz_convert("UTC")


def _require_0700_checkpoint(checkpoint: pd.Timestamp) -> None:
    thailand = checkpoint.tz_convert(THAILAND)
    if (
        thailand.hour != 7
        or thailand.minute != 0
        or thailand.second != 0
        or thailand.microsecond != 0
    ):
        raise StatePacketError(
            "checkpoint must map exactly to 07:00:00 Asia/Bangkok"
        )


def _require_h4_aligned_epoch(epoch: pd.Timestamp) -> None:
    if epoch != epoch.floor("4h"):
        raise StatePacketError(
            "operational initialization epoch must be aligned to a UTC H4 boundary"
        )


def _frame_sha256(frame: pd.DataFrame) -> str:
    canonical = frame.copy()
    canonical.index = canonical.index.tz_convert("UTC")
    columns = [
        column
        for column in ("open", "high", "low", "close", "volume")
        if column in canonical.columns
    ]
    rows: list[list[Any]] = []
    for timestamp, row in canonical[columns].iterrows():
        rows.append(
            [
                pd.Timestamp(timestamp).isoformat(),
                *[
                    (
                        value.item()
                        if hasattr(value, "item")
                        else value
                    )
                    for value in row.tolist()
                ],
            ]
        )
    payload = json.dumps(
        {"columns": columns, "rows": rows},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _gap_stats(frame: pd.DataFrame) -> dict[str, object]:
    if len(frame.index) < 2:
        return {
            "observed_gap_count_gt_1m": 0,
            "max_observed_gap_minutes": 0.0,
            "gap_interpretation": (
                "INFORMATIONAL_ONLY_MARKET_CLOSURES_AND_NO_TICK_MINUTES_NOT_DISTINGUISHED"
            ),
        }
    deltas = frame.index.to_series().diff().dropna()
    gaps = deltas[deltas > pd.Timedelta("1min")]
    max_gap = gaps.max() if not gaps.empty else pd.Timedelta(0)
    return {
        "observed_gap_count_gt_1m": len(gaps),
        "max_observed_gap_minutes": float(max_gap.total_seconds() / 60.0),
        "gap_interpretation": (
            "INFORMATIONAL_ONLY_MARKET_CLOSURES_AND_NO_TICK_MINUTES_NOT_DISTINGUISHED"
        ),
    }


def _daily_frame_context(
    frame: pd.DataFrame,
    checkpoint: pd.Timestamp,
) -> dict[str, object]:
    if checkpoint not in frame.index:
        return {
            "authority": "RESEARCH_REPRESENTATION",
            "status": "UNKNOWN_BOUNDARY_PRICE_UNOBSERVED",
            "price_at_checkpoint": None,
            "candidate_count": 0,
            "reference_candidates": [],
            "upper_candidates": [],
            "lower_candidates": [],
            "reference": None,
            "upper": None,
            "lower": None,
            "tie_ambiguous": None,
            "action_qualification_state": "UNKNOWN",
        }

    row = frame.loc[checkpoint]
    price = float(row["open"])
    candidates = build_mae_pla_frame_candidates(price)
    refs = [float(candidate.reference_price) for candidate in candidates.candidates]
    uppers = [float(candidate.upper_price) for candidate in candidates.candidates]
    lowers = [float(candidate.lower_price) for candidate in candidates.candidates]
    unique = len(refs) == 1
    return {
        "authority": "RESEARCH_REPRESENTATION",
        "boundary_price_authority": "RUNTIME_OBSERVATION_AT_CHECKPOINT",
        "status": "KNOWN_CONTEXT_RESEARCH_REPRESENTATION",
        "price_at_checkpoint": price,
        "candidate_count": len(refs),
        "reference_candidates": refs,
        "upper_candidates": uppers,
        "lower_candidates": lowers,
        "reference": refs[0] if unique else None,
        "upper": uppers[0] if unique else None,
        "lower": lowers[0] if unique else None,
        "tie_ambiguous": not unique,
        "action_qualification_state": "UNKNOWN_SOURCE_GEOMETRY_NOT_UNIVERSAL",
    }


def _origin_lifecycle_rows(
    pre_checkpoint: pd.DataFrame,
    epoch: pd.Timestamp,
    checkpoint: pd.Timestamp,
) -> list[dict[str, object]]:
    h4 = resample_ohlc(pre_checkpoint.loc[pre_checkpoint.index >= epoch], "H4")
    events = detect_pat2_full_range(h4, "H4")
    origins = build_h4_origins(h4, events)

    rows: list[dict[str, object]] = []
    for origin in origins:
        if origin.origin_known_at > checkpoint:
            continue

        target_price = fixed_origin_target_price(
            side=origin.side,
            anchor_price=origin.anchor_price,
        )
        path = pre_checkpoint.loc[
            (pre_checkpoint.index >= origin.origin_known_at)
            & (pre_checkpoint.index < checkpoint)
        ]
        hit = boundary_hit(
            path=path,
            side=origin.side,
            target_price=target_price,
            point_check_price=origin.anchor_price,
        )
        if hit.first_hit == "TARGET_FIRST":
            lifecycle = "RUN_COMPLETE"
            terminal_at = hit.target_at
        elif hit.first_hit == "POINT_CHECK_FIRST":
            lifecycle = "POINT_CHECK_DESTROYED"
            terminal_at = hit.point_check_at
        elif hit.first_hit == "AMBIGUOUS_SAME_BAR":
            lifecycle = "AMBIGUOUS_TERMINAL_SAME_BAR"
            terminal_at = hit.target_at or hit.point_check_at
        else:
            lifecycle = "ACTIVE"
            terminal_at = None

        progress_end = checkpoint
        if terminal_at is not None:
            progress_end = min(checkpoint, terminal_at + pd.Timedelta("1min"))
        consumed = favorable_consumed_points(
            active_m1=pre_checkpoint,
            side=origin.side,
            anchor=origin.anchor_price,
            start=origin.origin_known_at,
            end=progress_end,
        )
        if lifecycle in {"RUN_COMPLETE", "AMBIGUOUS_TERMINAL_SAME_BAR"}:
            consumed = H4_RUN_POINTS
        remaining = max(0.0, H4_RUN_POINTS - consumed)

        rows.append(
            {
                "authority": "DERIVED_CALCULATION_FROM_SOURCE_BACKED_GEOMETRY",
                "origin_id": origin.origin_id,
                "side": origin.side,
                "pattern_known_at": origin.pattern_known_at.isoformat(),
                "origin_known_at": origin.origin_known_at.isoformat(),
                "anchor_price": origin.anchor_price,
                "fixed_origin_target_price": target_price,
                "target_representation": "FIXED_ORIGIN_TARGET_V2_1",
                "lifecycle_state_0700": lifecycle,
                "consumed_points_at_0700": consumed,
                "consumed_measurement_basis": (
                    "FROZEN_AT_TERMINAL"
                    if terminal_at is not None
                    else "OBSERVED_THROUGH_CHECKPOINT"
                ),
                "remaining_nominal_points_at_0700": remaining,
                "target_at_before_0700": (
                    hit.target_at.isoformat() if hit.target_at is not None else None
                ),
                "point_check_at_before_0700": (
                    hit.point_check_at.isoformat()
                    if hit.point_check_at is not None
                    else None
                ),
                "terminal_at": (
                    terminal_at.isoformat() if terminal_at is not None else None
                ),
                "terminal_ordering": (
                    "NONE_BEFORE_CHECKPOINT"
                    if hit.first_hit == "NEITHER_BY_NEXT_0700"
                    else hit.first_hit
                ),
            }
        )

    rows.sort(key=lambda item: (str(item["origin_known_at"]), str(item["origin_id"])))
    return rows


def _origin_summary(
    origin_rows: list[dict[str, object]],
) -> tuple[dict[str, object], dict[str, object]]:
    active = [
        row for row in origin_rows if row["lifecycle_state_0700"] == "ACTIVE"
    ]
    active_buy = [row for row in active if row["side"] == "BUY"]
    active_sell = [row for row in active if row["side"] == "SELL"]
    same_side_multiple = len(active_buy) > 1 or len(active_sell) > 1
    opposite_sides = bool(active_buy and active_sell)
    conflict = same_side_multiple or opposite_sides

    lifecycle_counts: dict[str, int] = {}
    for row in origin_rows:
        key = str(row["lifecycle_state_0700"])
        lifecycle_counts[key] = lifecycle_counts.get(key, 0) + 1

    summary = {
        "authority": "DERIVED_CALCULATION",
        "observed_origin_count": len(origin_rows),
        "active_origin_count": len(active),
        "active_buy_count": len(active_buy),
        "active_sell_count": len(active_sell),
        "lifecycle_counts": lifecycle_counts,
        "active_origin_ids": [str(row["origin_id"]) for row in active],
    }
    conflict_state = {
        "authority": "DERIVED_CALCULATION_WITH_SOURCE_RESOLVER_UNKNOWN",
        "same_side_multiple": same_side_multiple,
        "opposite_sides_present": opposite_sides,
        "conflict_present": conflict,
        "action_resolution": (
            "PASS_CONFLICT_UNRESOLVED" if conflict else "NO_ORIGIN_CONFLICT"
        ),
    }
    return summary, conflict_state


def _unknowns(
    *,
    initialization_mode: str,
    conflict_present: bool,
) -> list[dict[str, object]]:
    values: list[dict[str, object]] = []
    if initialization_mode == INIT_SOURCE_PURE:
        values.append(
            {
                "id": "U-P1-08-ORIGIN-SEED-REOPEN",
                "epistemic_class": "STRUCTURAL_UNKNOWN",
                "blocking_axis": "BLOCKING_CANONICAL_SOURCE_PURE_STATE",
                "packet_effect": "PASS_INITIALIZATION_UNKNOWN",
                "reason": DATA_EXCLUDED_ORIGIN_HISTORY_UNSEEDED,
            }
        )
    else:
        values.append(
            {
                "id": "OPERATIONAL-EPOCH-BOUNDARY",
                "epistemic_class": "PROJECT_ENGINEERING_CONVENTION",
                "blocking_axis": "NON_BLOCKING_OPERATIONAL_STATE",
                "packet_effect": "STATE_VALID_ONLY_WITHIN_DECLARED_EPOCH",
                "reason": (
                    "Origins before the declared operational epoch are outside the "
                    "operational universe and are not claimed absent historically."
                ),
            }
        )

    values.extend(
        [
            {
                "id": "LOWER-TF-CONFIRMATION-ROUTING",
                "epistemic_class": "STRUCTURAL_UNKNOWN",
                "blocking_axis": "REQUIRED_LATER_FOR_SOURCE_FAITHFUL_ACTION",
                "packet_effect": "NON_BLOCKING_0700_SNAPSHOT",
                "reason": "Source says M1 or M5; exact universal routing is not closed.",
            },
            {
                "id": "DAILY-FRAME-ACTION-QUALIFICATION",
                "epistemic_class": "STRUCTURAL_UNKNOWN",
                "blocking_axis": "REQUIRED_LATER_FOR_ACTION_GATE",
                "packet_effect": "CONTEXT_VISIBLE_ACTION_QUALIFICATION_UNKNOWN",
                "reason": (
                    "Daily Frame context representation exists, but exact universal "
                    "action geometry is not source-closed."
                ),
            },
        ]
    )
    if conflict_present:
        values.append(
            {
                "id": "MULTIPLE-ORIGIN-WINNER",
                "epistemic_class": "STRUCTURAL_UNKNOWN",
                "blocking_axis": "BLOCKING_SINGLE_ACTION_DIRECTION",
                "packet_effect": "PASS_CONFLICT_UNRESOLVED",
                "reason": "No universal source-backed origin winner is closed.",
            }
        )

    values.append(
        {
            "id": "EXECUTION-ECONOMICS-GROUP",
            "epistemic_class": "DOWNSTREAM_UNKNOWNS",
            "blocking_axis": "NON_BLOCKING_0700_STATE_REQUIRED_LATER",
            "packet_effect": "NONE_ON_STATE_CALCULATION",
            "reason": (
                "Stop-price routing, fill/slippage, historical costs, sizing, risk "
                "cap, P&L and expectancy remain outside this state packet."
            ),
        }
    )
    return values


def build_state_packet(
    *,
    m1: pd.DataFrame,
    checkpoint_at: pd.Timestamp | str,
    initialization_mode: str,
    initialization_epoch: pd.Timestamp | str,
    source_identity: dict[str, object],
    generated_at_utc: pd.Timestamp | str | None = None,
) -> dict[str, object]:
    if initialization_mode not in INITIALIZATION_MODES:
        raise StatePacketError(
            f"unsupported initialization_mode: {initialization_mode}"
        )

    checkpoint = _utc(checkpoint_at)
    epoch = _utc(initialization_epoch)
    _require_0700_checkpoint(checkpoint)
    if epoch >= checkpoint:
        raise StatePacketError("initialization_epoch must be before checkpoint")
    if initialization_mode == INIT_OPERATIONAL_EXPLICIT_EPOCH:
        _require_h4_aligned_epoch(epoch)

    if not isinstance(m1.index, pd.DatetimeIndex) or m1.index.tz is None:
        raise StatePacketError("M1 input index must be timezone-aware")
    raw = m1.copy(deep=True)
    raw.index = raw.index.tz_convert("UTC")
    raw = raw.loc[raw.index <= checkpoint].sort_index(kind="stable")
    if raw.index.duplicated().any():
        raise StatePacketError("duplicate M1 timestamps found through checkpoint")

    state_columns = [
        column
        for column in ("open", "high", "low", "close", "volume")
        if column in raw.columns
    ]
    raw = raw[state_columns]
    boundary_observed = checkpoint in raw.index
    pre_raw = raw.loc[raw.index < checkpoint].copy()
    pre_frame = _normalize_m1_frame(pre_raw)

    if boundary_observed:
        boundary_row = raw.loc[[checkpoint]].copy()
        boundary_open = float(boundary_row.iloc[0]["open"])
        for column in ("open", "high", "low", "close"):
            boundary_row.loc[checkpoint, column] = boundary_open
        if "volume" in boundary_row.columns:
            boundary_row.loc[checkpoint, "volume"] = 0.0
        boundary_frame = _normalize_m1_frame(boundary_row)
        frame = pd.concat([pre_frame, boundary_frame]).sort_index(kind="stable")
    else:
        frame = pre_frame

    if frame.empty:
        raise StatePacketError("M1 frame is empty through checkpoint")

    used = frame.loc[(frame.index >= epoch) & (frame.index <= checkpoint)].copy()
    pre_checkpoint = frame.loc[
        (frame.index >= epoch) & (frame.index < checkpoint)
    ].copy()

    epoch_observed = epoch in frame.index
    boundary_observed = checkpoint in frame.index
    has_pre_checkpoint = not pre_checkpoint.empty
    structural_data_ok = has_pre_checkpoint and boundary_observed
    if initialization_mode == INIT_OPERATIONAL_EXPLICIT_EPOCH:
        structural_data_ok = structural_data_ok and epoch_observed

    data_health: dict[str, object] = {
        "authority": "RUNTIME_OBSERVATION_AND_ENGINEERING_VALIDATION",
        "calculation_eligibility": (
            "PASS_OBSERVED_M1_INPUT" if structural_data_ok else "FAIL_CLOSED"
        ),
        "input_start_utc": frame.index.min().isoformat(),
        "input_end_utc": frame.index.max().isoformat(),
        "used_start_utc": (
            used.index.min().isoformat() if not used.empty else None
        ),
        "used_end_utc": used.index.max().isoformat() if not used.empty else None,
        "input_row_count": len(frame),
        "used_row_count_through_checkpoint": len(used),
        "epoch_bar_observed": bool(epoch_observed),
        "checkpoint_bar_observed": bool(boundary_observed),
        "checkpoint_boundary_semantics": (
            "OPEN_ONLY_HLCV_SANITIZED_NOT_KNOWABLE_AT_BOUNDARY"
        ),
        "pre_checkpoint_rows_observed": bool(has_pre_checkpoint),
        "input_sha256_through_checkpoint": _frame_sha256(used),
        "continuity_claim": (
            "OBSERVED_M1_BAR_WINDOW_ONLY_NO_TICK_COMPLETENESS_OR_FILL_CLAIM"
        ),
        **_gap_stats(used),
    }

    daily_frame = _daily_frame_context(frame, checkpoint)
    origin_rows = (
        _origin_lifecycle_rows(pre_checkpoint, epoch, checkpoint)
        if has_pre_checkpoint
        else []
    )
    origin_summary, conflict = _origin_summary(origin_rows)
    active_origin_rows = [
        row for row in origin_rows if row["lifecycle_state_0700"] == "ACTIVE"
    ]

    if initialization_mode == INIT_SOURCE_PURE:
        initialization = {
            "authority": "SOURCE_FAITHFUL_FAIL_CLOSED",
            "mode": INIT_SOURCE_PURE,
            "epoch_utc": epoch.isoformat(),
            "origin_set_completeness": UNKNOWN_PREHISTORY,
            "canonical_state_eligibility": "FAIL_CLOSED",
            "reason": DATA_EXCLUDED_ORIGIN_HISTORY_UNSEEDED,
        }
    else:
        initialization = {
            "authority": "OWNER_DIRECT_PROJECT_ENGINEERING_CONVENTION",
            "mode": INIT_OPERATIONAL_EXPLICIT_EPOCH,
            "epoch_utc": epoch.isoformat(),
            "origin_set_completeness": COMPLETE_WITHIN_OPERATIONAL_EPOCH,
            "canonical_state_eligibility": (
                "OPERATIONAL_ONLY_NOT_SOURCE_PURE_CANONICAL"
            ),
            "historical_absence_claim": False,
            "lifecycle_rule_changed": False,
        }

    if data_health["calculation_eligibility"] != "PASS_OBSERVED_M1_INPUT":
        state_0700 = "UNKNOWN"
        confidence = "DATA_INSUFFICIENT_FAIL_CLOSED"
        post_0700 = "PASS_DATA_UNKNOWN"
    elif initialization_mode == INIT_SOURCE_PURE:
        state_0700 = "UNKNOWN"
        confidence = "FAIL_CLOSED_CANONICAL_UNKNOWN_PREHISTORY"
        post_0700 = "PASS_INITIALIZATION_UNKNOWN"
    else:
        buy_count = int(origin_summary["active_buy_count"])
        sell_count = int(origin_summary["active_sell_count"])
        if buy_count and not sell_count:
            state_0700 = "BULLISH_CONTEXT"
        elif sell_count and not buy_count:
            state_0700 = "BEARISH_CONTEXT"
        elif buy_count and sell_count:
            state_0700 = "MIXED"
        else:
            state_0700 = "NO_ACTIVE_ORIGIN"

        confidence = "DETERMINISTIC_WITHIN_DECLARED_OPERATIONAL_EPOCH"
        if int(origin_summary["active_origin_count"]) == 0:
            post_0700 = "PASS_NO_ACTIVE_ORIGIN"
        elif bool(conflict["conflict_present"]):
            post_0700 = "PASS_CONFLICT_UNRESOLVED"
        elif daily_frame.get("tie_ambiguous") is True:
            post_0700 = "PASS_FRAME_TIE"
        else:
            post_0700 = "WAIT_POST_0700_CONFIRMATION"

    generated = (
        _utc(generated_at_utc)
        if generated_at_utc is not None
        else pd.Timestamp(datetime.now(UTC))
    )

    packet = {
        "packet_version": PACKET_VERSION,
        "scope": SCOPE,
        "checkpoint_utc": checkpoint.isoformat(),
        "checkpoint_thailand": checkpoint.tz_convert(THAILAND).isoformat(),
        "generated_at_utc": generated.isoformat(),
        "source_identity": {
            "authority": "RUNTIME_OR_PROVIDED_PROVENANCE",
            **dict(source_identity),
        },
        "data_health": data_health,
        "initialization": initialization,
        "daily_frame": daily_frame,
        "origin_summary": origin_summary,
        "active_h4_origins": active_origin_rows,
        "observed_h4_origins": origin_rows,
        "conflict": conflict,
        "state_0700": state_0700,
        "calculation_confidence": confidence,
        "post_0700_requirement": post_0700,
        "confirmation_routing": {
            "authority": "SOURCE_PARTIAL_PROJECT_SCOPE",
            "source_statement": "M1_OR_M5_REVERSAL",
            "exact_universal_routing": "UNKNOWN",
            "existing_research_lane": "M5_PAT2_ONLY",
        },
        "unknowns": _unknowns(
            initialization_mode=initialization_mode,
            conflict_present=bool(conflict["conflict_present"]),
        ),
        "guards": {
            "historical_outcome_scoring": "NOT_PERFORMED_BY_PACKET",
            "protected_holdout_scoring": "DISABLED",
            "economic_scoring": "DISABLED",
            "profitability_expectancy_claims": "DISABLED",
            "automatic_order_send": "DISABLED",
            "broker_fill_inference": "DISABLED",
            "h1_d1_origin_promotion": "DISABLED_IN_V0",
        },
    }
    return packet


def write_state_packet_json(
    packet: dict[str, object],
    path: str | Path,
) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(target.suffix + ".tmp")
    serialized = json.dumps(
        packet,
        ensure_ascii=False,
        sort_keys=True,
        indent=2,
    ) + "\n"
    temporary.write_text(serialized, encoding="utf-8")
    try:
        temporary.replace(target)
    except PermissionError as exc:
        raise StatePacketError(
            f"STATE_PACKET_OUTPUT_LOCKED: cannot replace {target}"
        ) from exc
    return target
