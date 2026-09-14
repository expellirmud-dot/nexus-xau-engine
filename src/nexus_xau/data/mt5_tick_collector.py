from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import tempfile
import time
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from itertools import pairwise
from pathlib import Path
from typing import Any

COLLECTOR_VERSION = "PHASE1_MT5_FORWARD_COLLECTOR_V0.1"
SCHEMA_VERSION = "1"
READ_ONLY_MODE = "READ_ONLY_DATA_ORDER_SEND_DISABLED"

RAW_TICK_FIELDS = (
    "time",
    "time_msc",
    "bid",
    "ask",
    "last",
    "volume",
    "flags",
    "volume_real",
)


@dataclass(frozen=True)
class TickRow:
    time: int
    time_msc: int
    bid: float
    ask: float
    last: float
    volume: int
    flags: int
    volume_real: float

    @classmethod
    def from_mapping(cls, row: Mapping[str, Any]) -> TickRow:
        return cls(
            time=int(row.get("time", 0)),
            time_msc=int(row.get("time_msc", int(row.get("time", 0)) * 1000)),
            bid=float(row.get("bid", 0.0)),
            ask=float(row.get("ask", 0.0)),
            last=float(row.get("last", 0.0)),
            volume=int(row.get("volume", 0)),
            flags=int(row.get("flags", 0)),
            volume_real=float(row.get("volume_real", 0.0)),
        )

    def fingerprint(self) -> str:
        payload = [
            self.time,
            self.time_msc,
            self.bid,
            self.ask,
            self.last,
            self.volume,
            self.flags,
            self.volume_real,
        ]
        raw = json.dumps(payload, separators=(",", ":"), ensure_ascii=False)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class CollectorState:
    symbol: str
    source_identity: str
    last_committed_time_msc: int
    boundary_multiset: dict[str, int]
    last_successful_commit_utc: str
    runtime_snapshot_id: int | None


@dataclass(frozen=True)
class PersistResult:
    inserted_rows: int
    skipped_boundary_rows: int
    last_committed_time_msc: int
    boundary_multiset: dict[str, int]


def utc_now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="milliseconds")


def atomic_write_json(path: str | Path, payload: Mapping[str, Any]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(
        prefix=f".{target.name}.",
        suffix=".tmp",
        dir=str(target.parent),
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, target)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def init_db(path: str | Path) -> sqlite3.Connection:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(target)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA synchronous=FULL")
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS runtime_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            captured_at_utc TEXT NOT NULL,
            source_identity TEXT NOT NULL,
            payload_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS ticks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            time INTEGER NOT NULL,
            time_msc INTEGER NOT NULL,
            bid REAL NOT NULL,
            ask REAL NOT NULL,
            last REAL NOT NULL,
            volume INTEGER NOT NULL,
            flags INTEGER NOT NULL,
            volume_real REAL NOT NULL,
            runtime_snapshot_id INTEGER,
            collected_at_utc TEXT NOT NULL,
            FOREIGN KEY(runtime_snapshot_id) REFERENCES runtime_snapshots(id)
        );

        CREATE INDEX IF NOT EXISTS idx_ticks_symbol_time_msc
        ON ticks(symbol, time_msc, id);

        CREATE TABLE IF NOT EXISTS collector_state (
            symbol TEXT PRIMARY KEY,
            schema_version TEXT NOT NULL,
            collector_version TEXT NOT NULL,
            source_identity TEXT NOT NULL,
            last_committed_time_msc INTEGER NOT NULL,
            boundary_multiset_json TEXT NOT NULL,
            last_successful_commit_utc TEXT NOT NULL,
            runtime_snapshot_id INTEGER,
            FOREIGN KEY(runtime_snapshot_id) REFERENCES runtime_snapshots(id)
        );

        CREATE TABLE IF NOT EXISTS gaps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            detected_at_utc TEXT NOT NULL,
            requested_start_msc INTEGER NOT NULL,
            requested_end_msc INTEGER NOT NULL,
            source_identity TEXT NOT NULL,
            recovery_attempt_count INTEGER NOT NULL DEFAULT 1,
            returned_first_msc INTEGER,
            returned_last_msc INTEGER,
            mt5_error_code INTEGER,
            mt5_error_message TEXT,
            status TEXT NOT NULL,
            note TEXT
        );
        """
    )
    conn.commit()
    return conn


def save_runtime_snapshot(
    conn: sqlite3.Connection,
    *,
    source_identity: str,
    payload: Mapping[str, Any],
) -> int:
    cursor = conn.execute(
        """
        INSERT INTO runtime_snapshots(captured_at_utc, source_identity, payload_json)
        VALUES (?, ?, ?)
        """,
        (utc_now_iso(), source_identity, json.dumps(payload, ensure_ascii=False, sort_keys=True)),
    )
    conn.commit()
    return int(cursor.lastrowid)


def load_state(conn: sqlite3.Connection, symbol: str) -> CollectorState | None:
    row = conn.execute(
        """
        SELECT symbol, source_identity, last_committed_time_msc,
               boundary_multiset_json, last_successful_commit_utc,
               runtime_snapshot_id
        FROM collector_state
        WHERE symbol = ?
        """,
        (symbol,),
    ).fetchone()
    if row is None:
        return None
    return CollectorState(
        symbol=str(row[0]),
        source_identity=str(row[1]),
        last_committed_time_msc=int(row[2]),
        boundary_multiset={
            str(key): int(value) for key, value in json.loads(str(row[3])).items()
        },
        last_successful_commit_utc=str(row[4]),
        runtime_snapshot_id=None if row[5] is None else int(row[5]),
    )


def initialize_state(
    conn: sqlite3.Connection,
    *,
    symbol: str,
    source_identity: str,
    start_time_msc: int,
    runtime_snapshot_id: int | None,
) -> CollectorState:
    existing = load_state(conn, symbol)
    if existing is not None:
        return existing
    now = utc_now_iso()
    with conn:
        conn.execute(
            """
            INSERT INTO collector_state(
                symbol, schema_version, collector_version, source_identity,
                last_committed_time_msc, boundary_multiset_json,
                last_successful_commit_utc, runtime_snapshot_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                symbol,
                SCHEMA_VERSION,
                COLLECTOR_VERSION,
                source_identity,
                int(start_time_msc),
                "{}",
                now,
                runtime_snapshot_id,
            ),
        )
    state = load_state(conn, symbol)
    if state is None:  # pragma: no cover
        raise RuntimeError("collector state initialization failed")
    return state


def validate_source_identity(
    state: CollectorState,
    source_identity: str,
) -> None:
    if state.source_identity != source_identity:
        raise RuntimeError(
            "BLOCKED_SOURCE_IDENTITY_MISMATCH: "
            f"expected={state.source_identity!r} observed={source_identity!r}"
        )


def normalize_ticks(rows: Iterable[Mapping[str, Any] | TickRow]) -> list[TickRow]:
    result: list[TickRow] = []
    for row in rows:
        result.append(row if isinstance(row, TickRow) else TickRow.from_mapping(row))
    for previous, current in pairwise(result):
        if current.time_msc < previous.time_msc:
            raise ValueError(
                f"non-monotonic tick input: {previous.time_msc} -> {current.time_msc}"
            )
    return result


def _dedupe_restart_boundary(
    ticks: Sequence[TickRow],
    state: CollectorState,
) -> tuple[list[TickRow], int]:
    consumed = Counter()
    kept: list[TickRow] = []
    skipped = 0
    for tick in ticks:
        if tick.time_msc < state.last_committed_time_msc:
            continue
        if tick.time_msc == state.last_committed_time_msc:
            fingerprint = tick.fingerprint()
            already = state.boundary_multiset.get(fingerprint, 0)
            if consumed[fingerprint] < already:
                consumed[fingerprint] += 1
                skipped += 1
                continue
        kept.append(tick)
    return kept, skipped


def persist_tick_batch(
    conn: sqlite3.Connection,
    *,
    symbol: str,
    source_identity: str,
    ticks: Sequence[TickRow],
    runtime_snapshot_id: int | None,
) -> PersistResult:
    state = load_state(conn, symbol)
    if state is None:
        raise RuntimeError("collector state missing; initialize with explicit start time")
    validate_source_identity(state, source_identity)

    normalized = normalize_ticks(ticks)
    kept, skipped = _dedupe_restart_boundary(normalized, state)
    if not kept:
        return PersistResult(
            inserted_rows=0,
            skipped_boundary_rows=skipped,
            last_committed_time_msc=state.last_committed_time_msc,
            boundary_multiset=dict(state.boundary_multiset),
        )

    new_last = max(tick.time_msc for tick in kept)
    if new_last == state.last_committed_time_msc:
        boundary = Counter(state.boundary_multiset)
        boundary.update(
            tick.fingerprint() for tick in kept if tick.time_msc == new_last
        )
    else:
        boundary = Counter(
            tick.fingerprint() for tick in kept if tick.time_msc == new_last
        )

    collected_at = utc_now_iso()
    with conn:
        conn.executemany(
            """
            INSERT INTO ticks(
                symbol, time, time_msc, bid, ask, last, volume, flags,
                volume_real, runtime_snapshot_id, collected_at_utc
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    symbol,
                    tick.time,
                    tick.time_msc,
                    tick.bid,
                    tick.ask,
                    tick.last,
                    tick.volume,
                    tick.flags,
                    tick.volume_real,
                    runtime_snapshot_id,
                    collected_at,
                )
                for tick in kept
            ],
        )
        conn.execute(
            """
            UPDATE collector_state
            SET last_committed_time_msc = ?,
                boundary_multiset_json = ?,
                last_successful_commit_utc = ?,
                runtime_snapshot_id = ?
            WHERE symbol = ?
            """,
            (
                new_last,
                json.dumps(dict(boundary), sort_keys=True),
                collected_at,
                runtime_snapshot_id,
                symbol,
            ),
        )

    return PersistResult(
        inserted_rows=len(kept),
        skipped_boundary_rows=skipped,
        last_committed_time_msc=new_last,
        boundary_multiset=dict(boundary),
    )


def record_gap(
    conn: sqlite3.Connection,
    *,
    requested_start_msc: int,
    requested_end_msc: int,
    source_identity: str,
    status: str,
    returned_first_msc: int | None = None,
    returned_last_msc: int | None = None,
    mt5_error_code: int | None = None,
    mt5_error_message: str | None = None,
    note: str | None = None,
) -> int:
    cursor = conn.execute(
        """
        INSERT INTO gaps(
            detected_at_utc, requested_start_msc, requested_end_msc,
            source_identity, recovery_attempt_count, returned_first_msc,
            returned_last_msc, mt5_error_code, mt5_error_message, status, note
        ) VALUES (?, ?, ?, ?, 1, ?, ?, ?, ?, ?, ?)
        """,
        (
            utc_now_iso(),
            requested_start_msc,
            requested_end_msc,
            source_identity,
            returned_first_msc,
            returned_last_msc,
            mt5_error_code,
            mt5_error_message,
            status,
            note,
        ),
    )
    conn.commit()
    return int(cursor.lastrowid)


def tick_count(conn: sqlite3.Connection, symbol: str) -> int:
    row = conn.execute(
        "SELECT COUNT(*) FROM ticks WHERE symbol = ?",
        (symbol,),
    ).fetchone()
    return 0 if row is None else int(row[0])


def gap_counts(conn: sqlite3.Connection) -> dict[str, int]:
    rows = conn.execute(
        "SELECT status, COUNT(*) FROM gaps GROUP BY status ORDER BY status"
    ).fetchall()
    return {str(status): int(count) for status, count in rows}


def build_status(
    *,
    state_name: str,
    symbol: str,
    source_identity: str,
    latest_tick: TickRow | None,
    rows_committed_session: int,
    last_committed_time_msc: int,
    last_successful_commit_utc: str | None,
    gaps: Mapping[str, int],
    current_backfill: Mapping[str, int] | None = None,
    last_error: str | None = None,
) -> dict[str, Any]:
    return {
        "collector_version": COLLECTOR_VERSION,
        "mode": READ_ONLY_MODE,
        "state": state_name,
        "symbol": symbol,
        "source_identity": source_identity,
        "latest_committed_tick_time_msc": last_committed_time_msc,
        "latest_bid": None if latest_tick is None else latest_tick.bid,
        "latest_ask": None if latest_tick is None else latest_tick.ask,
        "rows_committed_session": rows_committed_session,
        "last_successful_commit_utc": last_successful_commit_utc,
        "current_backfill": current_backfill,
        "gap_counts": dict(gaps),
        "last_error": last_error,
        "updated_at_utc": utc_now_iso(),
    }


def _rows_from_mt5_payload(payload: Any) -> list[TickRow]:
    if payload is None:
        return []
    names = getattr(getattr(payload, "dtype", None), "names", None)
    if names:
        return [
            TickRow.from_mapping({name: row[name] for name in names})
            for row in payload
        ]
    return [TickRow.from_mapping(row) for row in payload]


def source_identity_from_runtime(mt5: Any, symbol: str) -> tuple[str, dict[str, Any]]:
    terminal = mt5.terminal_info()
    account = mt5.account_info()
    spec = mt5.symbol_info(symbol)
    if terminal is None or account is None or spec is None:
        raise RuntimeError("cannot read terminal/account/symbol runtime identity")

    payload = {
        "terminal_build": int(getattr(terminal, "build", 0)),
        "company": str(getattr(account, "company", "")),
        "server": str(getattr(account, "server", "")),
        "trade_mode": int(getattr(account, "trade_mode", -1)),
        "currency": str(getattr(account, "currency", "")),
        "leverage": int(getattr(account, "leverage", 0)),
        "symbol": symbol,
        "digits": int(getattr(spec, "digits", 0)),
        "point": float(getattr(spec, "point", 0.0)),
        "contract_size": float(getattr(spec, "trade_contract_size", 0.0)),
        "volume_min": float(getattr(spec, "volume_min", 0.0)),
        "volume_max": float(getattr(spec, "volume_max", 0.0)),
        "volume_step": float(getattr(spec, "volume_step", 0.0)),
        "trade_exemode": int(getattr(spec, "trade_exemode", -1)),
        "collector_version": COLLECTOR_VERSION,
    }
    identity_basis = {
        key: payload[key]
        for key in (
            "company",
            "server",
            "trade_mode",
            "currency",
            "symbol",
            "digits",
            "point",
            "contract_size",
        )
    }
    source_identity = hashlib.sha256(
        json.dumps(identity_basis, sort_keys=True, separators=(",", ":")).encode(
            "utf-8"
        )
    ).hexdigest()
    payload["source_identity"] = source_identity
    return source_identity, payload


def run_live_collector(
    *,
    mt5: Any,
    symbol: str,
    db_path: str | Path,
    status_path: str | Path,
    explicit_start_msc: int | None,
    duration_seconds: float,
    poll_seconds: float,
    chunk_seconds: int,
) -> dict[str, Any]:
    if poll_seconds <= 0:
        raise ValueError("poll_seconds must be > 0")
    if chunk_seconds <= 0:
        raise ValueError("chunk_seconds must be > 0")
    if duration_seconds < 0:
        raise ValueError("duration_seconds must be >= 0")

    if not mt5.initialize():
        code, message = mt5.last_error()
        raise RuntimeError(f"MT5 initialize failed: {code} {message}")

    conn: sqlite3.Connection | None = None
    latest_tick: TickRow | None = None
    rows_session = 0
    try:
        if not mt5.symbol_select(symbol, True):
            code, message = mt5.last_error()
            raise RuntimeError(f"Cannot select symbol {symbol}: {code} {message}")

        source_identity, snapshot_payload = source_identity_from_runtime(mt5, symbol)
        conn = init_db(db_path)
        snapshot_id = save_runtime_snapshot(
            conn,
            source_identity=source_identity,
            payload=snapshot_payload,
        )
        state = load_state(conn, symbol)
        if state is None:
            if explicit_start_msc is None:
                raise RuntimeError(
                    "INITIAL_START_TIME_REQUIRED: pass an explicit start time for a new store"
                )
            state = initialize_state(
                conn,
                symbol=symbol,
                source_identity=source_identity,
                start_time_msc=explicit_start_msc,
                runtime_snapshot_id=snapshot_id,
            )
        else:
            try:
                validate_source_identity(state, source_identity)
            except RuntimeError as exc:
                atomic_write_json(
                    status_path,
                    build_status(
                        state_name="BLOCKED",
                        symbol=symbol,
                        source_identity=source_identity,
                        latest_tick=None,
                        rows_committed_session=0,
                        last_committed_time_msc=state.last_committed_time_msc,
                        last_successful_commit_utc=state.last_successful_commit_utc,
                        gaps=gap_counts(conn),
                        last_error=str(exc),
                    ),
                )
                raise

        started = time.monotonic()
        first_cycle = True
        while first_cycle or time.monotonic() - started < duration_seconds:
            first_cycle = False
            state = load_state(conn, symbol)
            if state is None:  # pragma: no cover
                raise RuntimeError("collector state disappeared")

            now_tick = mt5.symbol_info_tick(symbol)
            if now_tick is None:
                code, message = mt5.last_error()
                atomic_write_json(
                    status_path,
                    build_status(
                        state_name="ERROR",
                        symbol=symbol,
                        source_identity=source_identity,
                        latest_tick=latest_tick,
                        rows_committed_session=rows_session,
                        last_committed_time_msc=state.last_committed_time_msc,
                        last_successful_commit_utc=state.last_successful_commit_utc,
                        gaps=gap_counts(conn),
                        last_error=f"{code}: {message}",
                    ),
                )
                time.sleep(poll_seconds)
                continue

            acquisition_end_msc = int(getattr(now_tick, "time_msc", 0))
            cursor_msc = state.last_committed_time_msc
            while cursor_msc <= acquisition_end_msc:
                chunk_end_msc = min(
                    acquisition_end_msc,
                    cursor_msc + chunk_seconds * 1000,
                )
                start_dt = datetime.fromtimestamp(cursor_msc / 1000, UTC)
                end_dt = datetime.fromtimestamp(chunk_end_msc / 1000, UTC)
                payload = mt5.copy_ticks_range(
                    symbol,
                    start_dt,
                    end_dt,
                    mt5.COPY_TICKS_ALL,
                )
                if payload is None:
                    code, message = mt5.last_error()
                    record_gap(
                        conn,
                        requested_start_msc=cursor_msc,
                        requested_end_msc=chunk_end_msc,
                        source_identity=source_identity,
                        status="API_ERROR",
                        mt5_error_code=int(code),
                        mt5_error_message=str(message),
                    )
                    atomic_write_json(
                        status_path,
                        build_status(
                            state_name="ERROR",
                            symbol=symbol,
                            source_identity=source_identity,
                            latest_tick=latest_tick,
                            rows_committed_session=rows_session,
                            last_committed_time_msc=state.last_committed_time_msc,
                            last_successful_commit_utc=state.last_successful_commit_utc,
                            gaps=gap_counts(conn),
                            current_backfill={
                                "start_msc": cursor_msc,
                                "end_msc": chunk_end_msc,
                            },
                            last_error=f"{code}: {message}",
                        ),
                    )
                    raise RuntimeError(
                        f"MT5 copy_ticks_range failed: {code} {message}"
                    )

                ticks = _rows_from_mt5_payload(payload)
                if ticks:
                    result = persist_tick_batch(
                        conn,
                        symbol=symbol,
                        source_identity=source_identity,
                        ticks=ticks,
                        runtime_snapshot_id=snapshot_id,
                    )
                    rows_session += result.inserted_rows
                    latest_tick = ticks[-1]
                    state = load_state(conn, symbol)
                    if state is None:  # pragma: no cover
                        raise RuntimeError("collector state disappeared after commit")
                    cursor_msc = max(
                        chunk_end_msc + 1,
                        state.last_committed_time_msc,
                    )
                else:
                    # Zero ticks is an observation, not proof of a data gap.
                    # Advance only the in-memory scan cursor for this cycle.
                    # On restart the durable last-tick boundary is queried again.
                    cursor_msc = chunk_end_msc + 1

                atomic_write_json(
                    status_path,
                    build_status(
                        state_name=(
                            "BACKFILLING"
                            if chunk_end_msc < acquisition_end_msc
                            else "RUNNING"
                        ),
                        symbol=symbol,
                        source_identity=source_identity,
                        latest_tick=latest_tick,
                        rows_committed_session=rows_session,
                        last_committed_time_msc=state.last_committed_time_msc,
                        last_successful_commit_utc=state.last_successful_commit_utc,
                        gaps=gap_counts(conn),
                        current_backfill=(
                            {
                                "start_msc": cursor_msc,
                                "end_msc": acquisition_end_msc,
                            }
                            if chunk_end_msc < acquisition_end_msc
                            else None
                        ),
                    ),
                )

            if time.monotonic() - started >= duration_seconds:
                break
            time.sleep(poll_seconds)

        final_state = load_state(conn, symbol)
        if final_state is None:  # pragma: no cover
            raise RuntimeError("collector state missing at shutdown")
        status = build_status(
            state_name="STOPPED",
            symbol=symbol,
            source_identity=source_identity,
            latest_tick=latest_tick,
            rows_committed_session=rows_session,
            last_committed_time_msc=final_state.last_committed_time_msc,
            last_successful_commit_utc=final_state.last_successful_commit_utc,
            gaps=gap_counts(conn),
        )
        atomic_write_json(status_path, status)
        return status
    finally:
        if conn is not None:
            conn.close()
        mt5.shutdown()
