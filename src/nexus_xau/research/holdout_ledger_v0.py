from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Mapping
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

ENGINE_SCHEMA_VERSION = "SIG_MODE2_SIGNAL_RUN_V0.1"
ENGINE_FREEZE_COMMIT = "75866d2"
PROTOCOL_FREEZE_COMMIT = "43c29be"
PROTOCOL_VERSION = "RQ011_PRISTINE_V0_HOLDOUT_PROTOCOL@43c29be"
PROTOCOL_FREEZE_TIME = datetime.fromisoformat("2026-09-09T05:34:43+07:00")
LOCK_SCHEMA_VERSION = "HOLDOUT_ACTIVATION_LOCK_V0.1"
LEDGER_GENESIS_SHA256 = "0" * 64
BANGKOK = ZoneInfo("Asia/Bangkok")

_REQUIRED_RECORD_FIELDS = {
    "record_index",
    "checkpoint_time",
    "record_created_at",
    "record_type",
    "visible_data_until",
    "payload",
    "previous_record_sha256",
    "record_sha256",
    "engine_version",
    "protocol_version",
}

_REQUIRED_ENV_FIELDS = {
    "broker_server",
    "symbol",
    "data_side",
    "digits",
    "point",
    "tick_size",
    "source_export_method",
    "timezone_normalization_method",
}


class HoldoutLedgerError(ValueError):
    pass


def _json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_ready(item) for item in value]
    if isinstance(value, float) and not math.isfinite(value):
        raise HoldoutLedgerError("NaN and Infinity are not canonical JSON values")
    return value


def canonical_json_bytes(value: Mapping[str, Any]) -> bytes:
    ready = _json_ready(value)
    try:
        text = json.dumps(
            ready,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise HoldoutLedgerError("value is not canonical-JSON serializable") from exc
    return text.encode("utf-8")


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _timestamp(value: Any, *, field: str) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise HoldoutLedgerError(f"{field} must be a non-empty ISO timestamp")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise HoldoutLedgerError(f"{field} must be a valid ISO timestamp") from exc
    if parsed.tzinfo is None:
        raise HoldoutLedgerError(f"{field} must be timezone-aware")
    return parsed


def _required_text(value: Any, *, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise HoldoutLedgerError(f"{field} must be a non-empty string")
    return value.strip()


def record_sha256(record: Mapping[str, Any]) -> str:
    body = dict(record)
    body.pop("record_sha256", None)
    return _sha256_hex(canonical_json_bytes(body))


def build_ledger_record(
    *,
    record_index: int,
    checkpoint_time: str,
    record_created_at: str,
    record_type: str,
    visible_data_until: str,
    payload: Mapping[str, Any],
    previous_record_sha256: str,
) -> dict[str, Any]:
    if not isinstance(record_index, int) or record_index < 0:
        raise HoldoutLedgerError("record_index must be a non-negative integer")
    _timestamp(checkpoint_time, field="checkpoint_time")
    _timestamp(record_created_at, field="record_created_at")
    _timestamp(visible_data_until, field="visible_data_until")
    _required_text(record_type, field="record_type")
    if not isinstance(payload, Mapping):
        raise HoldoutLedgerError("payload must be a mapping")
    if len(previous_record_sha256) != 64:
        raise HoldoutLedgerError("previous_record_sha256 must be a SHA256 hex digest")

    record: dict[str, Any] = {
        "record_index": record_index,
        "checkpoint_time": checkpoint_time,
        "record_created_at": record_created_at,
        "record_type": record_type,
        "visible_data_until": visible_data_until,
        "payload": dict(payload),
        "previous_record_sha256": previous_record_sha256.lower(),
        "engine_version": ENGINE_SCHEMA_VERSION,
        "protocol_version": PROTOCOL_VERSION,
    }
    record["record_sha256"] = record_sha256(record)
    return record


def _validate_record(
    record: Mapping[str, Any],
    *,
    expected_index: int,
    expected_previous_sha256: str,
) -> None:
    if set(record) != _REQUIRED_RECORD_FIELDS:
        missing = sorted(_REQUIRED_RECORD_FIELDS.difference(record))
        extra = sorted(set(record).difference(_REQUIRED_RECORD_FIELDS))
        raise HoldoutLedgerError(f"record fields mismatch; missing={missing}; extra={extra}")
    if record["record_index"] != expected_index:
        raise HoldoutLedgerError("record_index is not contiguous")
    if record["previous_record_sha256"] != expected_previous_sha256:
        raise HoldoutLedgerError("previous_record_sha256 chain mismatch")
    if record["engine_version"] != ENGINE_SCHEMA_VERSION:
        raise HoldoutLedgerError("engine version drift detected")
    if record["protocol_version"] != PROTOCOL_VERSION:
        raise HoldoutLedgerError("protocol version drift detected")
    _timestamp(record["checkpoint_time"], field="checkpoint_time")
    _timestamp(record["record_created_at"], field="record_created_at")
    _timestamp(record["visible_data_until"], field="visible_data_until")
    _required_text(record["record_type"], field="record_type")
    if not isinstance(record["payload"], Mapping):
        raise HoldoutLedgerError("payload must be a mapping")
    actual_hash = _required_text(record["record_sha256"], field="record_sha256").lower()
    if len(actual_hash) != 64 or any(ch not in "0123456789abcdef" for ch in actual_hash):
        raise HoldoutLedgerError("record_sha256 is not lowercase SHA256 hex")
    expected_hash = record_sha256(record)
    if actual_hash != expected_hash:
        raise HoldoutLedgerError("record_sha256 mismatch")


def verify_ledger(path: str | Path) -> dict[str, Any]:
    ledger_path = Path(path)
    if not ledger_path.exists():
        return {
            "valid": True,
            "empty": True,
            "record_count": 0,
            "final_sha256": None,
        }

    raw = ledger_path.read_bytes()
    if not raw:
        return {
            "valid": True,
            "empty": True,
            "record_count": 0,
            "final_sha256": None,
        }
    if not raw.endswith(b"\n"):
        raise HoldoutLedgerError("ledger must end with a newline")

    previous = LEDGER_GENESIS_SHA256
    count = 0
    for expected_index, raw_line in enumerate(raw.splitlines()):
        if not raw_line:
            raise HoldoutLedgerError("blank ledger lines are not allowed")
        try:
            decoded = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            raise HoldoutLedgerError("invalid JSON record") from exc
        if not isinstance(decoded, dict):
            raise HoldoutLedgerError("each ledger line must be a JSON object")
        canonical_line = canonical_json_bytes(decoded)
        if canonical_line != raw_line:
            raise HoldoutLedgerError("record is not canonically serialized")
        _validate_record(
            decoded,
            expected_index=expected_index,
            expected_previous_sha256=previous,
        )
        previous = decoded["record_sha256"]
        count += 1

    return {
        "valid": True,
        "empty": False,
        "record_count": count,
        "final_sha256": previous,
    }


def append_ledger_record(
    path: str | Path,
    *,
    checkpoint_time: str,
    record_created_at: str,
    record_type: str,
    visible_data_until: str,
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    ledger_path = Path(path)
    status = verify_ledger(ledger_path)
    next_index = int(status["record_count"])
    previous = status["final_sha256"] or LEDGER_GENESIS_SHA256
    record = build_ledger_record(
        record_index=next_index,
        checkpoint_time=checkpoint_time,
        record_created_at=record_created_at,
        record_type=record_type,
        visible_data_until=visible_data_until,
        payload=payload,
        previous_record_sha256=previous,
    )
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with ledger_path.open("ab") as handle:
        handle.write(canonical_json_bytes(record))
        handle.write(b"\n")
    return record


def _validate_environment(environment: Mapping[str, Any]) -> dict[str, Any]:
    missing = sorted(field for field in _REQUIRED_ENV_FIELDS if field not in environment)
    if missing:
        raise HoldoutLedgerError(f"environment metadata missing fields: {missing}")
    normalized = dict(environment)
    for field in _REQUIRED_ENV_FIELDS:
        value = normalized[field]
        if value is None or (isinstance(value, str) and not value.strip()):
            raise HoldoutLedgerError(f"environment field {field} must be non-empty")
    return normalized


def validate_activation_lock(lock: Mapping[str, Any]) -> dict[str, Any]:
    required = {
        "lock_schema_version",
        "engine_schema_version",
        "engine_freeze_commit",
        "protocol_freeze_commit",
        "activation_created_at",
        "prospective_boundary",
        "timezone",
        "outcome_scoring_enabled",
        "ledger_path",
        "environment",
    }
    missing = sorted(required.difference(lock))
    if missing:
        raise HoldoutLedgerError(f"activation lock missing fields: {missing}")
    if lock["lock_schema_version"] != LOCK_SCHEMA_VERSION:
        raise HoldoutLedgerError("activation lock schema version mismatch")
    if lock["engine_schema_version"] != ENGINE_SCHEMA_VERSION:
        raise HoldoutLedgerError("engine schema version mismatch")
    if lock["engine_freeze_commit"] != ENGINE_FREEZE_COMMIT:
        raise HoldoutLedgerError("engine freeze commit mismatch")
    if lock["protocol_freeze_commit"] != PROTOCOL_FREEZE_COMMIT:
        raise HoldoutLedgerError("protocol freeze commit mismatch")
    if lock["timezone"] != "Asia/Bangkok":
        raise HoldoutLedgerError("timezone must be Asia/Bangkok")
    if lock["outcome_scoring_enabled"] is not False:
        raise HoldoutLedgerError("outcome scoring must remain disabled")
    _required_text(lock["ledger_path"], field="ledger_path")
    created = _timestamp(lock["activation_created_at"], field="activation_created_at")
    boundary = _timestamp(lock["prospective_boundary"], field="prospective_boundary")
    boundary_bkk = boundary.astimezone(BANGKOK)
    if (
        boundary_bkk.hour != 7
        or boundary_bkk.minute != 0
        or boundary_bkk.second != 0
        or boundary_bkk.microsecond != 0
    ):
        raise HoldoutLedgerError("prospective boundary must be exactly 07:00 Asia/Bangkok")
    if boundary <= PROTOCOL_FREEZE_TIME:
        raise HoldoutLedgerError("prospective boundary must be after protocol freeze")
    if boundary <= created:
        raise HoldoutLedgerError("prospective boundary must be after activation creation")
    environment = lock["environment"]
    if not isinstance(environment, Mapping):
        raise HoldoutLedgerError("environment must be a mapping")
    _validate_environment(environment)
    return dict(lock)


def create_activation_lock(
    *,
    activation_created_at: str,
    prospective_boundary: str,
    ledger_path: str,
    environment: Mapping[str, Any],
) -> dict[str, Any]:
    lock: dict[str, Any] = {
        "lock_schema_version": LOCK_SCHEMA_VERSION,
        "engine_schema_version": ENGINE_SCHEMA_VERSION,
        "engine_freeze_commit": ENGINE_FREEZE_COMMIT,
        "protocol_freeze_commit": PROTOCOL_FREEZE_COMMIT,
        "activation_created_at": activation_created_at,
        "prospective_boundary": prospective_boundary,
        "timezone": "Asia/Bangkok",
        "outcome_scoring_enabled": False,
        "ledger_path": ledger_path,
        "environment": _validate_environment(environment),
    }
    return validate_activation_lock(lock)


def write_activation_lock(path: str | Path, lock: Mapping[str, Any]) -> None:
    validated = validate_activation_lock(lock)
    output_path = Path(path)
    if output_path.exists():
        raise HoldoutLedgerError("activation lock already exists; overwrite is forbidden")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(canonical_json_bytes(validated) + b"\n")
