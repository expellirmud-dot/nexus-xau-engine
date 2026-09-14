from __future__ import annotations

import json
from pathlib import Path

import pytest

import nexus_xau.data.mt5_tick_collector as collector_module
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
    run_live_collector,
    tick_count,
    validate_source_identity,
    write_status_json,
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


class _Obj:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class _EmptyTickMT5:
    COPY_TICKS_ALL = 0

    def initialize(self):
        return True

    def shutdown(self):
        return None

    def symbol_select(self, symbol, selected):
        return True

    def last_error(self):
        return (1, "Success")

    def terminal_info(self):
        return _Obj(build=6182)

    def account_info(self):
        return _Obj(
            company="Exness Technologies Ltd",
            server="Demo",
            trade_mode=0,
            currency="USD",
            leverage=500,
        )

    def symbol_info(self, symbol):
        return _Obj(
            digits=3,
            point=0.001,
            trade_contract_size=100.0,
            volume_min=0.01,
            volume_max=200.0,
            volume_step=0.01,
            trade_exemode=2,
        )

    def symbol_info_tick(self, symbol):
        return _Obj(time_msc=2000, bid=4300.0, ask=4300.2)

    def copy_ticks_range(self, symbol, start_dt, end_dt, mode):
        return []


def test_zero_tick_live_observation_does_not_create_gap(tmp_path: Path) -> None:
    db = tmp_path / "ticks.sqlite3"
    status = tmp_path / "status.json"
    result = run_live_collector(
        mt5=_EmptyTickMT5(),
        symbol="XAUUSDm",
        db_path=db,
        status_path=status,
        explicit_start_msc=1000,
        duration_seconds=0,
        poll_seconds=0.01,
        chunk_seconds=1,
    )
    conn = init_db(db)
    try:
        assert gap_counts(conn) == {}
    finally:
        conn.close()
    assert result["mode"] == READ_ONLY_MODE


class _ChangedSourceMT5(_EmptyTickMT5):
    def account_info(self):
        return _Obj(
            company="Different Broker",
            server="Demo",
            trade_mode=0,
            currency="USD",
            leverage=500,
        )


class _ApiErrorMT5(_EmptyTickMT5):
    def last_error(self):
        return (-7, "copy failed")

    def copy_ticks_range(self, symbol, start_dt, end_dt, mode):
        return None


def test_live_source_mismatch_writes_blocked_status(tmp_path: Path) -> None:
    db = tmp_path / "ticks.sqlite3"
    status = tmp_path / "status.json"
    run_live_collector(
        mt5=_EmptyTickMT5(),
        symbol="XAUUSDm",
        db_path=db,
        status_path=status,
        explicit_start_msc=1000,
        duration_seconds=0,
        poll_seconds=0.01,
        chunk_seconds=1,
    )

    with pytest.raises(RuntimeError, match="BLOCKED_SOURCE_IDENTITY_MISMATCH"):
        run_live_collector(
            mt5=_ChangedSourceMT5(),
            symbol="XAUUSDm",
            db_path=db,
            status_path=status,
            explicit_start_msc=None,
            duration_seconds=0,
            poll_seconds=0.01,
            chunk_seconds=1,
        )

    payload = json.loads(status.read_text(encoding="utf-8"))
    assert payload["state"] == "BLOCKED"
    assert "BLOCKED_SOURCE_IDENTITY_MISMATCH" in payload["last_error"]


def test_live_api_error_persists_gap_and_error_status(tmp_path: Path) -> None:
    db = tmp_path / "ticks.sqlite3"
    status = tmp_path / "status.json"

    with pytest.raises(RuntimeError, match="MT5 copy_ticks_range failed"):
        run_live_collector(
            mt5=_ApiErrorMT5(),
            symbol="XAUUSDm",
            db_path=db,
            status_path=status,
            explicit_start_msc=1000,
            duration_seconds=0,
            poll_seconds=0.01,
            chunk_seconds=1,
        )

    conn = init_db(db)
    try:
        assert gap_counts(conn) == {"API_ERROR": 1}
    finally:
        conn.close()

    payload = json.loads(status.read_text(encoding="utf-8"))
    assert payload["state"] == "ERROR"
    assert "copy failed" in payload["last_error"]


def test_atomic_status_write_retries_windows_replace_contention(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    path = tmp_path / "status.json"
    real_replace = collector_module.os.replace
    attempts = {"count": 0}

    def flaky_replace(src, dst):
        attempts["count"] += 1
        if attempts["count"] < 4:
            raise PermissionError("simulated Windows reader lock")
        return real_replace(src, dst)

    monkeypatch.setattr(collector_module.os, "replace", flaky_replace)
    collector_module.atomic_write_json(path, {"state": "RUNNING"})

    assert attempts["count"] == 4
    assert json.loads(path.read_text(encoding="utf-8"))["state"] == "RUNNING"


def test_status_write_failure_is_nonfatal(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def always_locked(src, dst):
        raise PermissionError("locked")

    monkeypatch.setattr(collector_module.os, "replace", always_locked)
    assert write_status_json(tmp_path / "status.json", {"state": "RUNNING"}) is False
