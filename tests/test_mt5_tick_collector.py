from __future__ import annotations

import json
from pathlib import Path

import pytest

from nexus_xau.data.mt5_tick_collector import (
    READ_ONLY_MODE,
    TickRow,
    atomic_write_json,
    gap_counts,
    init_db,
    initialize_state,
    load_state,
    persist_tick_batch,
    record_gap,
    tick_count,
    validate_source_identity,
)


def _tick(msc: int, bid: float = 4300.0, ask: float = 4300.2) -> TickRow:
    return TickRow(
        time=msc // 1000,
        time_msc=msc,
        bid=bid,
        ask=ask,
        last=0.0,
        volume=0,
        flags=6,
        volume_real=0.0,
    )


def test_schema_and_state_creation(tmp_path: Path) -> None:
    db = tmp_path / "ticks.sqlite3"
    conn = init_db(db)
    try:
        state = initialize_state(
            conn,
            symbol="XAUUSDm",
            source_identity="source-a",
            start_time_msc=1000,
            runtime_snapshot_id=None,
        )
        assert state.last_committed_time_msc == 1000
        assert state.boundary_multiset == {}
        assert tick_count(conn, "XAUUSDm") == 0
    finally:
        conn.close()


def test_repeated_identical_rows_are_preserved(tmp_path: Path) -> None:
    conn = init_db(tmp_path / "ticks.sqlite3")
    try:
        initialize_state(
            conn,
            symbol="XAUUSDm",
            source_identity="source-a",
            start_time_msc=1000,
            runtime_snapshot_id=None,
        )
        duplicate = _tick(2000)
        result = persist_tick_batch(
            conn,
            symbol="XAUUSDm",
            source_identity="source-a",
            ticks=[duplicate, duplicate],
            runtime_snapshot_id=None,
        )
        assert result.inserted_rows == 2
        assert tick_count(conn, "XAUUSDm") == 2
        assert list(result.boundary_multiset.values()) == [2]
    finally:
        conn.close()


def test_restart_boundary_is_multiplicity_aware(tmp_path: Path) -> None:
    conn = init_db(tmp_path / "ticks.sqlite3")
    try:
        initialize_state(
            conn,
            symbol="XAUUSDm",
            source_identity="source-a",
            start_time_msc=1000,
            runtime_snapshot_id=None,
        )
        same = _tick(2000)
        persist_tick_batch(
            conn,
            symbol="XAUUSDm",
            source_identity="source-a",
            ticks=[same, same],
            runtime_snapshot_id=None,
        )

        result = persist_tick_batch(
            conn,
            symbol="XAUUSDm",
            source_identity="source-a",
            ticks=[same, same, same, _tick(2001)],
            runtime_snapshot_id=None,
        )

        assert result.skipped_boundary_rows == 2
        assert result.inserted_rows == 2
        assert tick_count(conn, "XAUUSDm") == 4
        state = load_state(conn, "XAUUSDm")
        assert state is not None
        assert state.last_committed_time_msc == 2001
    finally:
        conn.close()


def test_non_monotonic_input_is_rejected(tmp_path: Path) -> None:
    conn = init_db(tmp_path / "ticks.sqlite3")
    try:
        initialize_state(
            conn,
            symbol="XAUUSDm",
            source_identity="source-a",
            start_time_msc=1000,
            runtime_snapshot_id=None,
        )
        with pytest.raises(ValueError, match="non-monotonic"):
            persist_tick_batch(
                conn,
                symbol="XAUUSDm",
                source_identity="source-a",
                ticks=[_tick(2001), _tick(2000)],
                runtime_snapshot_id=None,
            )
    finally:
        conn.close()


def test_source_identity_mismatch_blocks_merge(tmp_path: Path) -> None:
    conn = init_db(tmp_path / "ticks.sqlite3")
    try:
        state = initialize_state(
            conn,
            symbol="XAUUSDm",
            source_identity="source-a",
            start_time_msc=1000,
            runtime_snapshot_id=None,
        )
        with pytest.raises(RuntimeError, match="BLOCKED_SOURCE_IDENTITY_MISMATCH"):
            validate_source_identity(state, "source-b")
    finally:
        conn.close()


def test_gap_ledger_persists_status(tmp_path: Path) -> None:
    conn = init_db(tmp_path / "ticks.sqlite3")
    try:
        record_gap(
            conn,
            requested_start_msc=1000,
            requested_end_msc=2000,
            source_identity="source-a",
            status="API_ERROR",
            mt5_error_code=-1,
            mt5_error_message="test",
        )
        assert gap_counts(conn) == {"API_ERROR": 1}
    finally:
        conn.close()


def test_atomic_status_write(tmp_path: Path) -> None:
    path = tmp_path / "status.json"
    payload = {"mode": READ_ONLY_MODE, "state": "RUNNING"}
    atomic_write_json(path, payload)
    assert json.loads(path.read_text(encoding="utf-8")) == payload


def test_module_contains_no_order_send_call() -> None:
    module_path = (
        Path(__file__).parents[1]
        / "src"
        / "nexus_xau"
        / "data"
        / "mt5_tick_collector.py"
    )
    text = module_path.read_text(encoding="utf-8")
    forbidden = "order" + "_send("
    assert forbidden not in text
