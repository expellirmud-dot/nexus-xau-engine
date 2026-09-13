from __future__ import annotations

import json
from collections.abc import Mapping
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from nexus_xau.research.holdout_ledger_v0 import (
    HoldoutLedgerError,
    append_ledger_record,
    validate_activation_lock,
    verify_ledger,
)
from nexus_xau.research.sig_mode2_signal_run_v0 import SigMode2SignalRunEvent

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_ACTIVATION_LOCK = (
    REPO_ROOT / "docs" / "RQ012_V0_HOLDOUT_ACTIVATION_LOCK_2026-09-13.json"
)

ALLOWED_RECORD_TYPES = {
    "NO_EVENT",
    "ELIGIBLE_MODE2_EVENT",
    "AMBIGUOUS_OR_CONFLICT",
    "EXCLUDED_DATA_OR_PROVENANCE",
}

_BLOCKED_KEYS = {
    "result",
    "outcome",
    "score",
    "scoring",
    "target_hit_at",
    "point_check_hit_at",
    "terminal_at",
    "terminal_time",
    "mfe",
    "mfe_ticks",
    "mae",
    "mae_ticks",
    "bars_observed",
    "win",
    "loss",
    "win_rate",
    "loss_rate",
    "expectancy",
    "profit_factor",
    "realized_pnl",
    "pnl",
}
_BLOCKED_OUTCOME_VALUES = {
    "TARGET_FIRST",
    "POINT_CHECK_FIRST",
    "AMBIGUOUS_SAME_BAR",
    "HORIZON_EXHAUSTED",
}


class HoldoutProgressiveRevealError(HoldoutLedgerError):
    pass


def _timestamp(value: Any, *, field: str) -> datetime:
    if isinstance(value, datetime):
        parsed = value
    elif isinstance(value, str) and value.strip():
        try:
            parsed = datetime.fromisoformat(value)
        except ValueError as exc:
            raise HoldoutProgressiveRevealError(
                f"{field} must be a valid ISO timestamp"
            ) from exc
    else:
        raise HoldoutProgressiveRevealError(
            f"{field} must be a timezone-aware ISO timestamp"
        )
    if parsed.tzinfo is None:
        raise HoldoutProgressiveRevealError(f"{field} must be timezone-aware")
    return parsed


def _resolve_repo_path(value: str | Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return REPO_ROOT / path


def load_activation_lock(
    path: str | Path = DEFAULT_ACTIVATION_LOCK,
) -> dict[str, Any]:
    lock_path = Path(path)
    try:
        raw = json.loads(lock_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise HoldoutProgressiveRevealError(
            f"activation lock not found: {lock_path}"
        ) from exc
    except json.JSONDecodeError as exc:
        raise HoldoutProgressiveRevealError("activation lock is invalid JSON") from exc
    if not isinstance(raw, dict):
        raise HoldoutProgressiveRevealError("activation lock must be a JSON object")
    return validate_activation_lock(raw)


def _find_blocked_payload_content(value: Any, *, path: str = "payload") -> str | None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            normalized = str(key).strip().lower()
            if normalized in _BLOCKED_KEYS:
                return f"{path}.{key}"
            blocked = _find_blocked_payload_content(item, path=f"{path}.{key}")
            if blocked is not None:
                return blocked
        return None
    if isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            blocked = _find_blocked_payload_content(item, path=f"{path}[{index}]")
            if blocked is not None:
                return blocked
        return None
    if isinstance(value, str) and value.strip().upper() in _BLOCKED_OUTCOME_VALUES:
        return path
    return None


def _validate_progressive_payload(payload: Mapping[str, Any]) -> None:
    blocked = _find_blocked_payload_content(payload)
    if blocked is not None:
        raise HoldoutProgressiveRevealError(
            f"payload contains prohibited outcome/scoring content at {blocked}"
        )


def _last_checkpoint_time(ledger_path: Path) -> datetime | None:
    status = verify_ledger(ledger_path)
    if status["record_count"] == 0:
        return None
    lines = ledger_path.read_text(encoding="utf-8").splitlines()
    last = json.loads(lines[-1])
    return _timestamp(last["checkpoint_time"], field="previous checkpoint_time")


def _validate_eligible_event(
    *,
    payload: Mapping[str, Any],
    boundary: datetime,
    checkpoint_time: datetime,
    visible_data_until: datetime,
) -> None:
    event_raw = payload.get("event")
    if not isinstance(event_raw, Mapping):
        raise HoldoutProgressiveRevealError(
            "ELIGIBLE_MODE2_EVENT payload must contain one event mapping"
        )
    try:
        event = SigMode2SignalRunEvent.from_mapping(event_raw)
    except (KeyError, TypeError, ValueError) as exc:
        raise HoldoutProgressiveRevealError(
            f"eligible V0.1 event validation failed: {exc}"
        ) from exc

    known_at = event.post_sig_closed_at.to_pydatetime()
    horizon_end = event.horizon_end.to_pydatetime()
    if known_at < boundary:
        raise HoldoutProgressiveRevealError(
            "eligible event post_sig_closed_at is before prospective boundary"
        )
    if checkpoint_time != known_at:
        raise HoldoutProgressiveRevealError(
            "ELIGIBLE_MODE2_EVENT checkpoint_time must equal post_sig_closed_at"
        )
    if visible_data_until != checkpoint_time:
        raise HoldoutProgressiveRevealError(
            "ELIGIBLE_MODE2_EVENT visible_data_until must equal checkpoint_time"
        )
    if horizon_end != known_at + timedelta(days=30):
        raise HoldoutProgressiveRevealError(
            "ELIGIBLE_MODE2_EVENT horizon_end must be exactly 30 calendar days "
            "after post_sig_closed_at"
        )


def holdout_runner_status(
    *,
    activation_lock_path: str | Path = DEFAULT_ACTIVATION_LOCK,
    now: datetime,
) -> dict[str, Any]:
    lock = load_activation_lock(activation_lock_path)
    current = _timestamp(now, field="now")
    boundary = _timestamp(lock["prospective_boundary"], field="prospective_boundary")
    ledger_path = _resolve_repo_path(lock["ledger_path"])
    ledger = verify_ledger(ledger_path)
    return {
        "activation_state": "ACTIVE_COLLECTION_WINDOW"
        if current >= boundary
        else "PRE_ACTIVATION",
        "now": current.isoformat(),
        "prospective_boundary": boundary.isoformat(),
        "outcome_scoring_enabled": lock["outcome_scoring_enabled"],
        "ledger_path": str(ledger_path),
        "ledger_record_count": ledger["record_count"],
        "ledger_final_sha256": ledger["final_sha256"],
    }


def append_progressive_checkpoint(
    *,
    activation_lock_path: str | Path = DEFAULT_ACTIVATION_LOCK,
    now: datetime,
    checkpoint_time: str | datetime,
    visible_data_until: str | datetime,
    record_type: str,
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    lock = load_activation_lock(activation_lock_path)
    current = _timestamp(now, field="now")
    boundary = _timestamp(lock["prospective_boundary"], field="prospective_boundary")
    checkpoint = _timestamp(checkpoint_time, field="checkpoint_time")
    visible_until = _timestamp(visible_data_until, field="visible_data_until")

    if current < boundary:
        raise HoldoutProgressiveRevealError(
            "prospective boundary has not been reached; ledger append is forbidden"
        )
    if checkpoint < boundary:
        raise HoldoutProgressiveRevealError(
            "checkpoint_time is before prospective boundary"
        )
    if checkpoint > current:
        raise HoldoutProgressiveRevealError(
            "checkpoint_time cannot be in the future relative to now"
        )
    if visible_until > checkpoint:
        raise HoldoutProgressiveRevealError(
            "visible_data_until cannot be later than checkpoint_time"
        )

    normalized_type = str(record_type).strip().upper()
    if normalized_type not in ALLOWED_RECORD_TYPES:
        raise HoldoutProgressiveRevealError(
            f"record_type must be one of {sorted(ALLOWED_RECORD_TYPES)}"
        )
    if not isinstance(payload, Mapping):
        raise HoldoutProgressiveRevealError("payload must be a mapping")
    _validate_progressive_payload(payload)

    if normalized_type == "ELIGIBLE_MODE2_EVENT":
        _validate_eligible_event(
            payload=payload,
            boundary=boundary,
            checkpoint_time=checkpoint,
            visible_data_until=visible_until,
        )

    ledger_path = _resolve_repo_path(lock["ledger_path"])
    previous_checkpoint = _last_checkpoint_time(ledger_path)
    if previous_checkpoint is not None and checkpoint < previous_checkpoint:
        raise HoldoutProgressiveRevealError(
            "checkpoint_time moves backward relative to the append-only ledger"
        )

    return append_ledger_record(
        ledger_path,
        checkpoint_time=checkpoint.isoformat(),
        record_created_at=current.isoformat(),
        record_type=normalized_type,
        visible_data_until=visible_until.isoformat(),
        payload=payload,
    )
