import json
from pathlib import Path

import pytest

from nexus_xau.research.holdout_ledger_v0 import (
    ENGINE_FREEZE_COMMIT,
    ENGINE_SCHEMA_VERSION,
    LOCK_SCHEMA_VERSION,
    PROTOCOL_FREEZE_COMMIT,
    HoldoutLedgerError,
    append_ledger_record,
    canonical_json_bytes,
    create_activation_lock,
    validate_activation_lock,
    verify_ledger,
    write_activation_lock,
)


def _environment() -> dict[str, object]:
    return {
        "broker_server": "fixture-server",
        "symbol": "XAUUSDm",
        "data_side": "Bid OHLC",
        "digits": 3,
        "point": "0.001",
        "tick_size": "0.001",
        "source_export_method": "fixture-export",
        "timezone_normalization_method": "UTC aware timestamps",
    }


def _append(path: Path, suffix: str) -> dict[str, object]:
    return append_ledger_record(
        path,
        checkpoint_time=f"2026-09-14T0{suffix}:00:00+00:00",
        record_created_at=f"2026-09-14T0{suffix}:01:00+00:00",
        record_type="NO_EVENT",
        visible_data_until=f"2026-09-14T0{suffix}:00:00+00:00",
        payload={"checkpoint": suffix},
    )


def _lock() -> dict[str, object]:
    return create_activation_lock(
        activation_created_at="2026-09-13T17:10:00+07:00",
        prospective_boundary="2026-09-14T07:00:00+07:00",
        ledger_path="results/holdout/v0/checkpoints.jsonl",
        environment=_environment(),
    )


def test_valid_genesis_and_append_chain(tmp_path: Path) -> None:
    ledger = tmp_path / "ledger.jsonl"

    first = _append(ledger, "1")
    second = _append(ledger, "2")
    status = verify_ledger(ledger)

    assert first["record_index"] == 0
    assert second["record_index"] == 1
    assert second["previous_record_sha256"] == first["record_sha256"]
    assert status == {
        "valid": True,
        "empty": False,
        "record_count": 2,
        "final_sha256": second["record_sha256"],
    }


def test_tamper_detection_fails_closed(tmp_path: Path) -> None:
    ledger = tmp_path / "ledger.jsonl"
    _append(ledger, "1")

    raw = ledger.read_text(encoding="utf-8")
    ledger.write_text(raw.replace('"checkpoint":"1"', '"checkpoint":"tampered"'), encoding="utf-8")

    with pytest.raises(HoldoutLedgerError, match="record_sha256 mismatch"):
        verify_ledger(ledger)


def test_duplicate_or_reordered_index_is_rejected(tmp_path: Path) -> None:
    ledger = tmp_path / "ledger.jsonl"
    _append(ledger, "1")
    _append(ledger, "2")
    lines = ledger.read_bytes().splitlines()

    ledger.write_bytes(lines[1] + b"\n" + lines[0] + b"\n")
    with pytest.raises(HoldoutLedgerError, match="record_index is not contiguous"):
        verify_ledger(ledger)


def test_previous_hash_mismatch_is_rejected(tmp_path: Path) -> None:
    ledger = tmp_path / "ledger.jsonl"
    _append(ledger, "1")
    _append(ledger, "2")

    records = [json.loads(line) for line in ledger.read_text(encoding="utf-8").splitlines()]
    records[1]["previous_record_sha256"] = "f" * 64
    body = dict(records[1])
    body.pop("record_sha256")
    import hashlib

    records[1]["record_sha256"] = hashlib.sha256(canonical_json_bytes(body)).hexdigest()
    ledger.write_bytes(
        b"\n".join(canonical_json_bytes(record) for record in records) + b"\n"
    )

    with pytest.raises(HoldoutLedgerError, match="previous_record_sha256 chain mismatch"):
        verify_ledger(ledger)


def test_noncanonical_record_is_rejected(tmp_path: Path) -> None:
    ledger = tmp_path / "ledger.jsonl"
    record = _append(ledger, "1")
    ledger.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")

    with pytest.raises(HoldoutLedgerError, match="invalid JSON record|canonically serialized"):
        verify_ledger(ledger)


def test_valid_activation_lock_is_unscored_and_exact() -> None:
    lock = _lock()

    assert lock["lock_schema_version"] == LOCK_SCHEMA_VERSION
    assert lock["engine_schema_version"] == ENGINE_SCHEMA_VERSION
    assert lock["engine_freeze_commit"] == ENGINE_FREEZE_COMMIT
    assert lock["protocol_freeze_commit"] == PROTOCOL_FREEZE_COMMIT
    assert lock["outcome_scoring_enabled"] is False
    assert validate_activation_lock(lock) == lock


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("engine_freeze_commit", "deadbee", "engine freeze commit mismatch"),
        ("protocol_freeze_commit", "deadbee", "protocol freeze commit mismatch"),
        ("outcome_scoring_enabled", True, "outcome scoring must remain disabled"),
        (
            "prospective_boundary",
            "2026-09-14T07:01:00+07:00",
            "exactly 07:00 Asia/Bangkok",
        ),
    ],
)
def test_activation_lock_rejects_identity_scoring_and_boundary(
    field: str,
    value: object,
    message: str,
) -> None:
    lock = _lock()
    lock[field] = value

    with pytest.raises(HoldoutLedgerError, match=message):
        validate_activation_lock(lock)


def test_activation_lock_requires_environment_metadata() -> None:
    environment = _environment()
    environment.pop("tick_size")

    with pytest.raises(HoldoutLedgerError, match="tick_size"):
        create_activation_lock(
            activation_created_at="2026-09-13T17:10:00+07:00",
            prospective_boundary="2026-09-14T07:00:00+07:00",
            ledger_path="results/holdout/v0/checkpoints.jsonl",
            environment=environment,
        )


def test_activation_lock_boundary_must_be_future_of_creation() -> None:
    with pytest.raises(HoldoutLedgerError, match="after activation creation"):
        create_activation_lock(
            activation_created_at="2026-09-14T08:00:00+07:00",
            prospective_boundary="2026-09-14T07:00:00+07:00",
            ledger_path="results/holdout/v0/checkpoints.jsonl",
            environment=_environment(),
        )


def test_activation_lock_file_is_write_once(tmp_path: Path) -> None:
    path = tmp_path / "activation.json"
    lock = _lock()

    write_activation_lock(path, lock)
    stored = json.loads(path.read_text(encoding="utf-8"))
    assert stored == lock

    with pytest.raises(HoldoutLedgerError, match="overwrite is forbidden"):
        write_activation_lock(path, lock)
