from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from nexus_xau.data.mt5_collector_dashboard import (
    DASHBOARD_HTML,
    read_dashboard_status,
)


def _make_db(path: Path) -> None:
    conn = sqlite3.connect(path)
    try:
        conn.execute(
            """
            CREATE TABLE ticks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                time_msc INTEGER NOT NULL
            )
            """
        )
        conn.executemany(
            "INSERT INTO ticks(symbol, time_msc) VALUES (?, ?)",
            [("XAUUSDm", 1), ("XAUUSDm", 2), ("XAUUSDm", 3)],
        )
        conn.commit()
    finally:
        conn.close()


def test_read_dashboard_status_combines_json_and_db(tmp_path: Path) -> None:
    status = tmp_path / "status.json"
    db = tmp_path / "ticks.sqlite3"
    status.write_text(
        json.dumps(
            {
                "state": "RUNNING",
                "mode": "READ_ONLY_DATA_ORDER_SEND_DISABLED",
                "rows_committed_session": 7,
            }
        ),
        encoding="utf-8",
    )
    _make_db(db)

    payload = read_dashboard_status(status, db)

    assert payload["state"] == "RUNNING"
    assert payload["total_ticks"] == 3
    assert payload["dashboard_read_only"] is True


def test_missing_status_file_is_explicit(tmp_path: Path) -> None:
    payload = read_dashboard_status(
        tmp_path / "missing.json",
        tmp_path / "missing.sqlite3",
    )

    assert payload["state"] == "NO_STATUS_FILE"
    assert payload["total_ticks"] == 0
    assert payload["dashboard_read_only"] is True


def test_dashboard_has_no_execution_controls() -> None:
    lower = DASHBOARD_HTML.lower()
    assert "no trading/execution controls" in lower
    assert "buy" not in lower
    assert "sell" not in lower
