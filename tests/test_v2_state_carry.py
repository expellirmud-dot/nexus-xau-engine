from __future__ import annotations

import json
from dataclasses import replace
from datetime import timedelta

import pandas as pd
import pytest

from nexus_xau.replay.v2_integration import DATA_EXCLUDED_ORIGIN_HISTORY_UNSEEDED
from nexus_xau.replay.v2_state_carry import (
    BRIDGE_CONTINUITY_STATUS,
    COMPLETE_SEED_ASSERTION,
    COMPLETE_SEED_EVIDENCE_CONTRACT,
    COMPLETE_SEED_VERIFICATION_STATUS,
    HANDOFF_GAP_POLICY,
    SEED_COMPLETE,
    SEED_SYNTHETIC_COMPLETE,
    SEED_UNKNOWN_PREHISTORY,
    CarriedH4Origin,
    V2OriginStateCarry,
    V2StateCarryError,
    checkpoint_document,
    checkpoint_from_document,
    checkpoint_sha256,
    create_checkpoint,
    create_complete_checkpoint,
    load_complete_seed_evidence,
    read_checkpoint_json,
    run_continuation,
    write_checkpoint_json,
)
from nexus_xau.research.minimal_v2_0700 import build_minimal_v2_from_frame, origin_state_at

SOURCE_FAMILY = "SYNTHETIC_TEST"
SYMBOL = "XAUUSD"
REPRESENTATION = "SYNTHETIC_M1_OHLC"
INTEGRATION_VERSION = "SYNTHETIC_V2_INPUT_V0.1"
CHECKPOINT = pd.Timestamp("2026-01-02T00:00:00Z")
SOURCE_PROVENANCE = {
    "fixture": "v2-state-carry-parity-v0.1",
    "source_version": "SYNTHETIC_FIXTURE_V0.1",
}


def _expand_h4_bar(
    start: str,
    *,
    open_price: float,
    high_price: float,
    low_price: float,
    close_price: float,
) -> pd.DataFrame:
    index = pd.date_range(start, periods=240, freq="1min")
    prices = [open_price + (close_price - open_price) * i / 239.0 for i in range(240)]
    prices[60] = high_price
    prices[120] = low_price
    prices[-1] = close_price
    return pd.DataFrame(
        {"open": prices, "high": prices, "low": prices, "close": prices},
        index=index,
    )


def _synthetic_m1() -> pd.DataFrame:
    specs = [
        ("2026-01-01T00:00:00Z", 110.0, 112.0, 99.0, 100.0),
        ("2026-01-01T04:00:00Z", 100.0, 112.0, 100.0, 108.0),
        ("2026-01-01T08:00:00Z", 108.0, 111.0, 101.0, 109.0),
        ("2026-01-01T12:00:00Z", 109.0, 113.0, 108.0, 112.0),
        ("2026-01-01T16:00:00Z", 112.0, 113.0, 108.0, 109.0),
        ("2026-01-01T20:00:00Z", 109.0, 114.0, 108.0, 112.0),
        ("2026-01-02T00:00:00Z", 112.0, 114.0, 109.0, 113.0),
        ("2026-01-02T04:00:00Z", 113.0, 115.0, 110.0, 114.0),
        ("2026-01-02T08:00:00Z", 114.0, 116.2, 111.0, 115.0),
        ("2026-01-02T12:00:00Z", 115.0, 117.0, 112.0, 116.0),
        ("2026-01-02T16:00:00Z", 116.0, 118.0, 113.0, 117.0),
        ("2026-01-02T20:00:00Z", 117.0, 119.0, 114.0, 118.0),
        ("2026-01-03T00:00:00Z", 118.0, 120.0, 115.0, 119.0),
    ]
    frames = [
        _expand_h4_bar(
            start,
            open_price=open_price,
            high_price=high_price,
            low_price=low_price,
            close_price=close_price,
        )
        for start, open_price, high_price, low_price, close_price in specs
    ]
    return pd.concat(frames).sort_index()

def _checkpoint(
    m1: pd.DataFrame,
    *,
    seed: str = SEED_SYNTHETIC_COMPLETE,
) -> V2OriginStateCarry:
    return create_checkpoint(
        m1=m1,
        checkpoint_at=CHECKPOINT,
        seed_completeness=seed,  # type: ignore[arg-type]
        source_family=SOURCE_FAMILY,
        symbol=SYMBOL,
        m1_representation=REPRESENTATION,
        integration_representation_version=INTEGRATION_VERSION,
        source_provenance=SOURCE_PROVENANCE,
    )


def _post_checkpoint(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.loc[frame.index >= CHECKPOINT].copy()


def _run(
    checkpoint: V2OriginStateCarry,
    frame: pd.DataFrame,
    *,
    source_family: str = SOURCE_FAMILY,
    integration_version: str = INTEGRATION_VERSION,
    allow_synthetic_complete: bool = True,
):
    return run_continuation(
        checkpoint=checkpoint,
        continuation_m1=_post_checkpoint(frame),
        source_family=source_family,
        symbol=SYMBOL,
        m1_representation=REPRESENTATION,
        integration_representation_version=integration_version,
        handoff_gap_policy=HANDOFF_GAP_POLICY,
        allow_synthetic_complete=allow_synthetic_complete,
    )


def _with_straddling_m5_buy(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    before = pd.date_range("2026-01-01T23:55:00Z", periods=5, freq="1min")
    after = pd.date_range("2026-01-02T00:00:00Z", periods=5, freq="1min")
    for index, prices in (
        (before, [114.0, 113.5, 113.0, 112.5, 112.0]),
        (after, [112.0, 112.6, 113.2, 113.8, 114.1]),
    ):
        for timestamp, price in zip(index, prices, strict=True):
            out.loc[timestamp, ["open", "high", "low", "close"]] = price
    return out


def _normalize_for_compare(frame: pd.DataFrame) -> pd.DataFrame:
    if frame.empty:
        return frame.reset_index(drop=True)
    return frame.sort_values(list(frame.columns), kind="stable").reset_index(drop=True)


def _old_buy_origin(checkpoint: V2OriginStateCarry) -> CarriedH4Origin:
    return next(
        origin
        for origin in checkpoint.active_origins
        if origin.origin_id == "H4:BUY:2026-01-01T12:00:00Z"
    )


def _write_complete_seed_evidence(
    tmp_path,
    *,
    source_family: str = "TEST_COMPLETE_SOURCE",
    integration_version: str = "TEST_COMPLETE_INPUT_V0.1",
):
    path = tmp_path / "complete_seed_evidence.json"
    payload = {
        "contract": COMPLETE_SEED_EVIDENCE_CONTRACT,
        "assertion": COMPLETE_SEED_ASSERTION,
        "verification_status": COMPLETE_SEED_VERIFICATION_STATUS,
        "independence_basis": (
            "Controlled test evidence independently declares all active origins represented."
        ),
        "checkpoint_at": CHECKPOINT.isoformat(),
        "source_family": source_family,
        "symbol": SYMBOL,
        "m1_representation": REPRESENTATION,
        "integration_representation_version": integration_version,
    }
    path.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")
    return path

def test_checkpoint_json_roundtrip_and_digest() -> None:
    checkpoint = _checkpoint(_synthetic_m1())
    document = checkpoint_document(checkpoint)
    restored = checkpoint_from_document(json.loads(json.dumps(document)))
    assert checkpoint_sha256(restored) == checkpoint_sha256(checkpoint)
    assert restored.seed_completeness == SEED_SYNTHETIC_COMPLETE
    assert restored.bridge_provenance.continuity_status == BRIDGE_CONTINUITY_STATUS
    assert len(restored.active_origins) >= 1


def test_checkpoint_atomic_file_roundtrip(tmp_path) -> None:
    checkpoint = _checkpoint(_synthetic_m1())
    target = tmp_path / "carry.json"
    written_digest = write_checkpoint_json(checkpoint, target)
    restored = read_checkpoint_json(target)
    assert written_digest == checkpoint_sha256(checkpoint)
    assert checkpoint_sha256(restored) == written_digest
    assert not (tmp_path / "carry.json.tmp").exists()


def test_checkpoint_digest_mutation_is_rejected() -> None:
    document = checkpoint_document(_checkpoint(_synthetic_m1()))
    document["prior_checkpoint_sha256"] = "0" * 64
    with pytest.raises(V2StateCarryError) as exc:
        checkpoint_from_document(document)
    assert exc.value.code == "CARRY_DIGEST_MISMATCH"


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("contract", "OTHER", "CARRY_CONTRACT_MISMATCH"),
        ("v2_version", "OTHER", "CARRY_V2_VERSION_MISMATCH"),
    ],
)
def test_checkpoint_semantic_version_mismatch_is_rejected(field, value, code) -> None:
    document = checkpoint_document(_checkpoint(_synthetic_m1()))
    document[field] = value
    with pytest.raises(V2StateCarryError) as exc:
        checkpoint_from_document(document)
    assert exc.value.code == code


def test_bridge_provenance_mismatch_is_rejected() -> None:
    checkpoint = _checkpoint(_synthetic_m1())
    bad = replace(
        checkpoint,
        bridge_provenance=replace(
            checkpoint.bridge_provenance,
            source_family="OTHER_FEED",
        ),
    )
    with pytest.raises(V2StateCarryError) as exc:
        checkpoint_document(bad)
    assert exc.value.code == "CARRY_BRIDGE_PROVENANCE_MISMATCH"


def test_bridge_payload_digest_mismatch_is_rejected() -> None:
    checkpoint = _checkpoint(_synthetic_m1())
    mutated_bridge = checkpoint.bridge_m1.copy()
    mutated_bridge.loc[
        mutated_bridge.index[0], ["open", "high", "low", "close"]
    ] += 0.01
    bad = replace(checkpoint, bridge_m1=mutated_bridge)
    with pytest.raises(V2StateCarryError) as exc:
        checkpoint_document(bad)
    assert exc.value.code == "CARRY_BRIDGE_DIGEST_MISMATCH"


def test_bridge_internal_m1_hole_is_rejected() -> None:
    frame = _synthetic_m1().drop(pd.Timestamp("2026-01-01T20:15:00Z"))
    with pytest.raises(V2StateCarryError) as exc:
        _checkpoint(frame)
    assert exc.value.code == "CARRY_BRIDGE_CONTINUITY_GAP"

def test_complete_seed_cannot_use_ordinary_checkpoint_api() -> None:
    with pytest.raises(V2StateCarryError) as exc:
        create_checkpoint(
            m1=_synthetic_m1(),
            checkpoint_at=CHECKPOINT,
            seed_completeness=SEED_COMPLETE,
            source_family="TEST_COMPLETE_SOURCE",
            symbol=SYMBOL,
            m1_representation=REPRESENTATION,
            integration_representation_version="TEST_COMPLETE_INPUT_V0.1",
            source_provenance={"fixture": "bounded-history-is-not-evidence"},
        )
    assert exc.value.code == "CARRY_COMPLETE_REQUIRES_EVIDENCE_API"


def test_complete_seed_requires_independent_evidence_file(tmp_path) -> None:
    evidence = load_complete_seed_evidence(_write_complete_seed_evidence(tmp_path))
    checkpoint = create_complete_checkpoint(
        m1=_synthetic_m1(),
        checkpoint_at=CHECKPOINT,
        source_family="TEST_COMPLETE_SOURCE",
        symbol=SYMBOL,
        m1_representation=REPRESENTATION,
        integration_representation_version="TEST_COMPLETE_INPUT_V0.1",
        source_provenance={"fixture": "complete-evidence-gate"},
        complete_seed_evidence=evidence,
    )
    assert checkpoint.seed_completeness == SEED_COMPLETE
    assert checkpoint.complete_seed_evidence is not None
    assert checkpoint.complete_seed_evidence.evidence_ref == str(
        _write_complete_seed_evidence(tmp_path).resolve()
    )


def test_complete_seed_evidence_identity_mismatch_is_rejected(tmp_path) -> None:
    evidence_path = _write_complete_seed_evidence(
        tmp_path,
        source_family="OTHER_COMPLETE_SOURCE",
    )
    evidence = load_complete_seed_evidence(evidence_path)
    with pytest.raises(V2StateCarryError) as exc:
        create_complete_checkpoint(
            m1=_synthetic_m1(),
            checkpoint_at=CHECKPOINT,
            source_family="TEST_COMPLETE_SOURCE",
            symbol=SYMBOL,
            m1_representation=REPRESENTATION,
            integration_representation_version="TEST_COMPLETE_INPUT_V0.1",
            source_provenance={"fixture": "identity-mismatch"},
            complete_seed_evidence=evidence,
        )
    assert exc.value.code == "CARRY_COMPLETE_EVIDENCE_IDENTITY_MISMATCH"


def test_unknown_prehistory_cannot_promote_by_forward_continuation() -> None:
    frame = _synthetic_m1()
    checkpoint = _checkpoint(frame, seed=SEED_UNKNOWN_PREHISTORY)
    with pytest.raises(V2StateCarryError) as exc:
        _run(checkpoint, frame)
    assert exc.value.code == DATA_EXCLUDED_ORIGIN_HISTORY_UNSEEDED


def test_handoff_hole_is_rejected_without_fabrication() -> None:
    frame = _synthetic_m1()
    continuation = _post_checkpoint(frame).drop(CHECKPOINT)
    with pytest.raises(V2StateCarryError) as exc:
        run_continuation(
            checkpoint=_checkpoint(frame),
            continuation_m1=continuation,
            source_family=SOURCE_FAMILY,
            symbol=SYMBOL,
            m1_representation=REPRESENTATION,
            integration_representation_version=INTEGRATION_VERSION,
            handoff_gap_policy=HANDOFF_GAP_POLICY,
            allow_synthetic_complete=True,
        )
    assert exc.value.code == "CARRY_HANDOFF_GAP"


def test_handoff_gap_policy_mismatch_is_rejected() -> None:
    frame = _synthetic_m1()
    with pytest.raises(V2StateCarryError) as exc:
        run_continuation(
            checkpoint=_checkpoint(frame),
            continuation_m1=_post_checkpoint(frame),
            source_family=SOURCE_FAMILY,
            symbol=SYMBOL,
            m1_representation=REPRESENTATION,
            integration_representation_version=INTEGRATION_VERSION,
            handoff_gap_policy="ALLOW_FILL",
            allow_synthetic_complete=True,
        )
    assert exc.value.code == "CARRY_HANDOFF_POLICY_MISMATCH"


def test_synthetic_checkpoint_requires_explicit_fixture_opt_in() -> None:
    frame = _synthetic_m1()
    with pytest.raises(V2StateCarryError) as exc:
        _run(_checkpoint(frame), frame, allow_synthetic_complete=False)
    assert exc.value.code == "CARRY_SYNTHETIC_ONLY"


def test_source_family_transition_is_rejected() -> None:
    frame = _synthetic_m1()
    with pytest.raises(V2StateCarryError) as exc:
        _run(_checkpoint(frame), frame, source_family="OTHER_FEED")
    assert exc.value.code == "CARRY_SOURCE_FAMILY_MISMATCH"


def test_integration_representation_version_mismatch_is_rejected() -> None:
    frame = _synthetic_m1()
    with pytest.raises(V2StateCarryError) as exc:
        _run(_checkpoint(frame), frame, integration_version="OTHER_INTEGRATION")
    assert exc.value.code == "CARRY_INTEGRATION_VERSION_MISMATCH"

def test_synthetic_split_replay_matches_unsplit_post_checkpoint_state() -> None:
    frame = _synthetic_m1()
    full_days, full_origins, full_events, _ = build_minimal_v2_from_frame(
        m1=frame,
        source_descriptor="SYNTHETIC:UNSPLIT",
    )
    split_days, split_origins, split_events, split_report = _run(_checkpoint(frame), frame)
    expected_days = full_days.loc[
        pd.to_datetime(full_days["cutoff_utc"], utc=True) >= CHECKPOINT
    ].copy()
    expected_origins = full_origins.loc[
        pd.to_datetime(full_origins["cutoff_utc"], utc=True) >= CHECKPOINT
    ].copy()
    expected_events = full_events.loc[
        pd.to_datetime(full_events["cutoff_utc"], utc=True) >= CHECKPOINT
    ].copy()
    pd.testing.assert_frame_equal(
        _normalize_for_compare(split_days),
        _normalize_for_compare(expected_days),
        check_dtype=False,
    )
    pd.testing.assert_frame_equal(
        _normalize_for_compare(split_origins),
        _normalize_for_compare(expected_origins),
        check_dtype=False,
    )
    pd.testing.assert_frame_equal(
        _normalize_for_compare(split_events),
        _normalize_for_compare(expected_events),
        check_dtype=False,
    )
    assert split_report["seed_completeness"] == SEED_SYNTHETIC_COMPLETE
    assert split_report["detector_bridge_hours"] == 8


def test_h4_pat_origin_straddling_checkpoint_matches_unsplit() -> None:
    frame = _synthetic_m1()
    _, full_origins, _, _ = build_minimal_v2_from_frame(
        m1=frame,
        source_descriptor="SYNTHETIC:H4-STRADDLE",
    )
    _, split_origins, _, _ = _run(_checkpoint(frame), frame)
    origin_id = "H4:BUY:2026-01-02T04:00:00Z"
    full = full_origins.loc[full_origins["origin_id"] == origin_id].reset_index(drop=True)
    split = split_origins.loc[split_origins["origin_id"] == origin_id].reset_index(drop=True)
    assert not full.empty
    pd.testing.assert_frame_equal(split, full, check_dtype=False)


def test_m5_confirmation_straddling_checkpoint_matches_unsplit() -> None:
    frame = _with_straddling_m5_buy(_synthetic_m1())
    _, _, full_events, _ = build_minimal_v2_from_frame(
        m1=frame,
        source_descriptor="SYNTHETIC:M5-STRADDLE",
    )
    _, _, split_events, _ = _run(_checkpoint(frame), frame)
    expected = full_events.loc[
        pd.to_datetime(full_events["cutoff_utc"], utc=True) >= CHECKPOINT
    ].copy()
    pd.testing.assert_frame_equal(
        _normalize_for_compare(split_events),
        _normalize_for_compare(expected),
        check_dtype=False,
    )
    confirmations = pd.to_datetime(
        split_events["confirmation_known_at"], utc=True, errors="coerce"
    )
    assert (confirmations == CHECKPOINT + timedelta(minutes=5)).any()


def test_carried_origin_target_completion_after_restart() -> None:
    frame = _synthetic_m1()
    checkpoint = _checkpoint(frame)
    carried = _old_buy_origin(checkpoint)
    state, consumed, remaining, touch = origin_state_at(
        active_m1=_post_checkpoint(frame),
        origin=carried.as_origin(),
        at=pd.Timestamp("2026-01-03T00:00:00Z"),
    )
    assert state == "RUN_COMPLETE"
    assert consumed >= 1500.0
    assert remaining == 0.0
    assert touch is None


def test_carried_origin_point_check_after_restart() -> None:
    frame = _synthetic_m1()
    timestamp = pd.Timestamp("2026-01-02T00:30:00Z")
    frame.loc[timestamp, ["open", "high", "low", "close"]] = [105.0, 110.0, 101.0, 105.0]
    checkpoint = _checkpoint(frame)
    state, _, _, touch = origin_state_at(
        active_m1=_post_checkpoint(frame),
        origin=_old_buy_origin(checkpoint).as_origin(),
        at=pd.Timestamp("2026-01-03T00:00:00Z"),
    )
    assert state == "POINT_CHECK_DESTROYED"
    assert touch == timestamp


def test_carried_origin_same_bar_terminal_remains_ambiguous() -> None:
    frame = _synthetic_m1()
    timestamp = pd.Timestamp("2026-01-02T00:30:00Z")
    frame.loc[timestamp, ["open", "high", "low", "close"]] = [110.0, 116.0, 101.0, 110.0]
    checkpoint = _checkpoint(frame)
    state, _, remaining, touch = origin_state_at(
        active_m1=_post_checkpoint(frame),
        origin=_old_buy_origin(checkpoint).as_origin(),
        at=pd.Timestamp("2026-01-03T00:00:00Z"),
    )
    assert state == "AMBIGUOUS_TERMINAL_SAME_BAR"
    assert remaining == 0.0
    assert touch == timestamp

def test_multiple_same_side_and_opposite_origins_survive_independently() -> None:
    frame = _synthetic_m1()
    base = _checkpoint(frame)
    known_at = pd.Timestamp("2026-01-01T12:00:00Z")
    checkpoint = replace(
        base,
        active_origins=(
            CarriedH4Origin("MANUAL:BUY:A", "BUY", known_at, known_at, 101.0, 1400.0),
            CarriedH4Origin("MANUAL:BUY:B", "BUY", known_at, known_at, 102.0, 1300.0),
            CarriedH4Origin("MANUAL:SELL:A", "SELL", known_at, known_at, 120.0, 1250.0),
        ),
    )
    _, origins, _, _ = _run(checkpoint, frame)
    at_checkpoint = origins.loc[origins["cutoff_utc"] == CHECKPOINT.isoformat()]
    consumed = dict(
        zip(
            at_checkpoint["origin_id"],
            at_checkpoint["consumed_points_at_0700"],
            strict=True,
        )
    )
    assert consumed["MANUAL:BUY:A"] == 1400.0
    assert consumed["MANUAL:BUY:B"] == 1300.0
    assert consumed["MANUAL:SELL:A"] == 1250.0


def test_consumed_progress_preserves_floor_and_updates_by_future_maximum() -> None:
    frame = _synthetic_m1()
    base = _checkpoint(frame)
    known_at = pd.Timestamp("2026-01-01T12:00:00Z")
    origin = CarriedH4Origin(
        "MANUAL:PROGRESS",
        "BUY",
        known_at,
        known_at,
        105.0,
        1000.0,
    )
    checkpoint = replace(base, active_origins=(origin,))
    _, origins, _, _ = _run(checkpoint, frame)

    at_checkpoint = origins.loc[
        (origins["origin_id"] == origin.origin_id)
        & (origins["cutoff_utc"] == CHECKPOINT.isoformat())
    ].iloc[0]
    later = origins.loc[
        (origins["origin_id"] == origin.origin_id)
        & (pd.to_datetime(origins["cutoff_utc"], utc=True) > CHECKPOINT)
    ].iloc[0]

    assert float(at_checkpoint["consumed_points_at_0700"]) == 1000.0
    assert float(later["consumed_points_at_0700"]) > 1000.0
    assert float(later["consumed_points_at_0700"]) < 1500.0


def test_no_economic_or_execution_fields_introduced_by_carry_layer() -> None:
    frame = _synthetic_m1()
    checkpoint = _checkpoint(frame)
    days, origins, events, report = _run(checkpoint, frame)
    document = checkpoint_document(checkpoint)
    forbidden_tokens = (
        "pnl",
        "p&l",
        "win_rate",
        "win rate",
        "expectancy",
        "broker_fill",
        "broker-fill",
        "order_send",
        "order-send",
        "profitability",
    )
    names: list[str] = []
    names.extend(str(key).lower() for key in document)
    names.extend(str(key).lower() for key in report)
    for output in (days, origins, events):
        names.extend(str(column).lower() for column in output.columns)
    assert not [
        name
        for name in names
        if any(token in name for token in forbidden_tokens)
    ]

def test_bridge_source_provenance_digest_mismatch_is_rejected() -> None:
    checkpoint = _checkpoint(_synthetic_m1())
    bad = replace(
        checkpoint,
        source_provenance={"fixture": "changed-after-bridge-freeze"},
    )
    with pytest.raises(V2StateCarryError) as exc:
        checkpoint_document(bad)
    assert exc.value.code == "CARRY_BRIDGE_PROVENANCE_MISMATCH"


def test_direct_complete_checkpoint_without_evidence_is_rejected() -> None:
    checkpoint = replace(_checkpoint(_synthetic_m1()), seed_completeness=SEED_COMPLETE)
    with pytest.raises(V2StateCarryError) as exc:
        checkpoint_document(checkpoint)
    assert exc.value.code == "CARRY_COMPLETE_EVIDENCE_REQUIRED"


def test_complete_seed_evidence_file_mutation_is_rejected(tmp_path) -> None:
    evidence_path = _write_complete_seed_evidence(tmp_path)
    evidence = load_complete_seed_evidence(evidence_path)
    checkpoint = create_complete_checkpoint(
        m1=_synthetic_m1(),
        checkpoint_at=CHECKPOINT,
        source_family="TEST_COMPLETE_SOURCE",
        symbol=SYMBOL,
        m1_representation=REPRESENTATION,
        integration_representation_version="TEST_COMPLETE_INPUT_V0.1",
        source_provenance={"fixture": "evidence-tamper"},
        complete_seed_evidence=evidence,
    )
    evidence_path.write_text("{}", encoding="utf-8")
    with pytest.raises(V2StateCarryError) as exc:
        checkpoint_document(checkpoint)
    assert exc.value.code == "CARRY_COMPLETE_EVIDENCE_DIGEST_MISMATCH"