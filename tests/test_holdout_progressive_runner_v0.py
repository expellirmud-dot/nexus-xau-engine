from datetime import datetime, timedelta
from pathlib import Path

import pytest

from nexus_xau.research.holdout_ledger_v0 import (
    create_activation_lock,
    verify_ledger,
    write_activation_lock,
)
from nexus_xau.research.holdout_progressive_runner_v0 import (
    HoldoutProgressiveRevealError,
    append_progressive_checkpoint,
    holdout_runner_status,
)


def _dt(value: str) -> datetime:
    return datetime.fromisoformat(value)


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


def _activation(tmp_path: Path) -> tuple[Path, Path]:
    ledger = tmp_path / "checkpoints.jsonl"
    lock_path = tmp_path / "activation.json"
    lock = create_activation_lock(
        activation_created_at="2026-09-13T17:10:00+07:00",
        prospective_boundary="2026-09-14T07:00:00+07:00",
        ledger_path=str(ledger),
        environment=_environment(),
    )
    write_activation_lock(lock_path, lock)
    return lock_path, ledger


def _event(known_at: str = "2026-09-14T08:00:00+07:00") -> dict[str, object]:
    known = _dt(known_at)
    return {
        "signal_id": "fixture-H1-001",
        "side": "BUY",
        "signal_tf": "H1",
        "pa_kind_or_source_label": "fixture-pa",
        "pa_confirmed_at": (known - timedelta(hours=1)).isoformat(),
        "location_label": "VALID_SUPPORT",
        "location_label_provenance": "fixture-location",
        "post_sig_closed_at": known.isoformat(),
        "point_check_price": "2500.000",
        "point_check_price_provenance": "fixture-point-check",
        "run_anchor_price": "2500.000",
        "run_target_price": "2510.000",
        "horizon_end": (known + timedelta(days=30)).isoformat(),
        "parent_context_tf": "H4",
        "context_tags": ["fixture"],
        "source_or_label_provenance": "fixture-source",
        "label_known_before_outcome": True,
    }


def test_status_is_pre_activation_and_does_not_create_ledger(tmp_path: Path) -> None:
    lock_path, ledger = _activation(tmp_path)

    status = holdout_runner_status(
        activation_lock_path=lock_path,
        now=_dt("2026-09-13T23:00:00+07:00"),
    )

    assert status["activation_state"] == "PRE_ACTIVATION"
    assert status["outcome_scoring_enabled"] is False
    assert status["ledger_record_count"] == 0
    assert not ledger.exists()


def test_append_is_forbidden_before_boundary(tmp_path: Path) -> None:
    lock_path, ledger = _activation(tmp_path)

    with pytest.raises(HoldoutProgressiveRevealError, match="boundary has not been reached"):
        append_progressive_checkpoint(
            activation_lock_path=lock_path,
            now=_dt("2026-09-14T06:59:59+07:00"),
            checkpoint_time="2026-09-14T07:00:00+07:00",
            visible_data_until="2026-09-14T07:00:00+07:00",
            record_type="NO_EVENT",
            payload={"reason": "none"},
        )

    assert not ledger.exists()


def test_non_event_append_after_boundary_is_chronological(tmp_path: Path) -> None:
    lock_path, ledger = _activation(tmp_path)

    first = append_progressive_checkpoint(
        activation_lock_path=lock_path,
        now=_dt("2026-09-14T09:00:00+07:00"),
        checkpoint_time="2026-09-14T08:00:00+07:00",
        visible_data_until="2026-09-14T08:00:00+07:00",
        record_type="NO_EVENT",
        payload={"reason": "no eligible mode2 event"},
    )
    second = append_progressive_checkpoint(
        activation_lock_path=lock_path,
        now=_dt("2026-09-14T10:00:00+07:00"),
        checkpoint_time="2026-09-14T08:00:00+07:00",
        visible_data_until="2026-09-14T08:00:00+07:00",
        record_type="AMBIGUOUS_OR_CONFLICT",
        payload={"reason": "same decision-time batch"},
    )

    assert first["record_index"] == 0
    assert second["record_index"] == 1
    assert verify_ledger(ledger)["record_count"] == 2


def test_backward_checkpoint_is_rejected(tmp_path: Path) -> None:
    lock_path, _ = _activation(tmp_path)
    append_progressive_checkpoint(
        activation_lock_path=lock_path,
        now=_dt("2026-09-14T10:00:00+07:00"),
        checkpoint_time="2026-09-14T09:00:00+07:00",
        visible_data_until="2026-09-14T09:00:00+07:00",
        record_type="NO_EVENT",
        payload={},
    )

    with pytest.raises(HoldoutProgressiveRevealError, match="moves backward"):
        append_progressive_checkpoint(
            activation_lock_path=lock_path,
            now=_dt("2026-09-14T10:00:00+07:00"),
            checkpoint_time="2026-09-14T08:00:00+07:00",
            visible_data_until="2026-09-14T08:00:00+07:00",
            record_type="NO_EVENT",
            payload={},
        )


@pytest.mark.parametrize(
    "payload",
    [
        {"result": "TARGET_FIRST"},
        {"nested": {"mfe_ticks": 100}},
        {"note": "POINT_CHECK_FIRST"},
    ],
)
def test_outcome_content_is_rejected_recursively(
    tmp_path: Path,
    payload: dict[str, object],
) -> None:
    lock_path, ledger = _activation(tmp_path)

    with pytest.raises(HoldoutProgressiveRevealError, match="prohibited outcome"):
        append_progressive_checkpoint(
            activation_lock_path=lock_path,
            now=_dt("2026-09-14T09:00:00+07:00"),
            checkpoint_time="2026-09-14T08:00:00+07:00",
            visible_data_until="2026-09-14T08:00:00+07:00",
            record_type="NO_EVENT",
            payload=payload,
        )

    assert not ledger.exists()


def test_visible_data_cannot_extend_past_checkpoint(tmp_path: Path) -> None:
    lock_path, _ = _activation(tmp_path)

    with pytest.raises(HoldoutProgressiveRevealError, match="visible_data_until"):
        append_progressive_checkpoint(
            activation_lock_path=lock_path,
            now=_dt("2026-09-14T09:00:00+07:00"),
            checkpoint_time="2026-09-14T08:00:00+07:00",
            visible_data_until="2026-09-14T08:01:00+07:00",
            record_type="NO_EVENT",
            payload={},
        )


def test_eligible_event_requires_exact_blind_checkpoint_and_30_day_horizon(
    tmp_path: Path,
) -> None:
    lock_path, ledger = _activation(tmp_path)
    event = _event()

    record = append_progressive_checkpoint(
        activation_lock_path=lock_path,
        now=_dt("2026-09-14T08:01:00+07:00"),
        checkpoint_time=event["post_sig_closed_at"],
        visible_data_until=event["post_sig_closed_at"],
        record_type="ELIGIBLE_MODE2_EVENT",
        payload={"event": event},
    )

    assert record["record_type"] == "ELIGIBLE_MODE2_EVENT"
    assert verify_ledger(ledger)["record_count"] == 1

    bad_event = _event("2026-09-14T09:00:00+07:00")
    bad_event["horizon_end"] = (
        _dt(str(bad_event["post_sig_closed_at"])) + timedelta(days=29)
    ).isoformat()
    with pytest.raises(HoldoutProgressiveRevealError, match="exactly 30 calendar days"):
        append_progressive_checkpoint(
            activation_lock_path=lock_path,
            now=_dt("2026-09-14T09:01:00+07:00"),
            checkpoint_time=bad_event["post_sig_closed_at"],
            visible_data_until=bad_event["post_sig_closed_at"],
            record_type="ELIGIBLE_MODE2_EVENT",
            payload={"event": bad_event},
        )
