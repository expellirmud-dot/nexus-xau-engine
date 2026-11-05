"""Decision-neutral 07:00 route availability observer.

Contract: docs/0700_ROUTE_PROBE_AUTOMATION_CONTRACT_V0_1_2026-11-05.md

This script records WHICH route exposes data and WHETHER new owner files
appeared. It does not compute a State Packet, does not rebuild M1, does not
validate archives, does not decide the input route, and does not touch any
research authority. See contract section 3.
"""

from __future__ import annotations

import json
import os
import tempfile
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path

from nexus_xau.data.exness_tick_archive import (  # noqa: F401  (used from Task 4)
    USER_AGENT,
    ArchiveAcquisitionError,
    ArchiveEntry,
    fetch_directory,
)

DAILY_ALLOWED = frozenset({"PRESENT", "ABSENT", "LISTING_UNREADABLE", "NOT_PROBED"})
MONTH_ALLOWED = frozenset(
    {"PRESENT_CHANGED", "PRESENT_UNCHANGED", "ABSENT", "LISTING_UNREADABLE", "NOT_PROBED"}
)
INBOX_ALLOWED = frozenset({"NO_NEW_FILES", "NEW_FILES", "DIR_MISSING", "NOT_PROBED"})

NOT_PROBED = "NOT_PROBED"
STATUS_DUE = "DUE"
STATUS_NOT_YET_DUE = "NOT_YET_DUE"
STATUS_SUSPENDED = "SUSPENDED"

DEFAULT_CADENCE_MINUTES = 30
DEFAULT_SYMBOL = "XAUUSDm"
DEFAULT_WATCH_DIR = Path("D:/tools/nexus-0700-watch")
DEFAULT_INBOX_DIR = Path("D:/tools/nexus-video-evidence/_incoming")


def iso_utc(value: datetime) -> str:
    if value.tzinfo is None:
        raise ValueError("datetime must be timezone-aware")
    return value.astimezone(UTC).isoformat(timespec="seconds")


def load_state(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError, OSError) as exc:
        raise ValueError(f"STATE_FILE_UNREADABLE: {path}: {exc}") from exc
    if not isinstance(payload, dict):
        # State-file content has the wrong shape; this is a data problem in the
        # watch directory, not a caller passing the wrong argument type.
        raise ValueError(f"STATE_FILE_UNREADABLE: {path} must contain an object")  # noqa: TRY004
    return payload


def save_state(path: Path, state: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, tmp_name = tempfile.mkstemp(dir=path.parent, prefix=".state-", suffix=".tmp")
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(state, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def _parse_iso(value: object) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None else None


def compute_due(state: dict[str, object], now: datetime, cadence_minutes: int) -> str:
    if state.get("status") == STATUS_SUSPENDED:
        return STATUS_SUSPENDED
    next_run = _parse_iso(state.get("next_run_at"))
    if next_run is None:
        return STATUS_DUE
    return STATUS_DUE if now >= next_run else STATUS_NOT_YET_DUE


def append_observation(path: Path, observation: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(observation, ensure_ascii=False, sort_keys=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")


def read_observations(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    records: list[dict[str, object]] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip():
            continue
        try:
            payload = json.loads(raw_line)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            records.append(payload)
    return records


BASE_URL = "https://ticks.ex2archive.com/ticks"


@dataclass(frozen=True)
class ListingFacts:
    day_directory_present: bool
    month_zip: ArchiveEntry | None


def month_directory_url(symbol: str, day: date) -> str:
    return f"{BASE_URL}/{symbol}/{day.year:04d}/{day.month:02d}/"


def day_directory_url(symbol: str, day: date) -> str:
    return f"{BASE_URL}/{symbol}/{day.year:04d}/{day.month:02d}/{day.day:02d}/"


def month_zip_name(symbol: str, day: date) -> str:
    return f"Exness_{symbol}_{day.year:04d}_{day.month:02d}.zip"


def month_zip_url(symbol: str, day: date) -> str:
    return month_directory_url(symbol, day) + month_zip_name(symbol, day)


def day_zip_url(symbol: str, day: date) -> str:
    return day_directory_url(symbol, day) + (
        f"Exness_{symbol}_{day.year:04d}_{day.month:02d}_{day.day:02d}.zip"
    )


def classify_listing(
    entries: list[ArchiveEntry],
    symbol: str,
    day: date,
) -> ListingFacts:
    named = {entry.name: entry for entry in entries}
    return ListingFacts(
        day_directory_present=f"{day.day:02d}" in named,
        month_zip=named.get(month_zip_name(symbol, day)),
    )


def daily_route_status(facts: ListingFacts) -> str:
    return "PRESENT" if facts.day_directory_present else "ABSENT"


def fingerprint_of(entry: ArchiveEntry | None) -> str | None:
    if entry is None or entry.size is None or not entry.mtime:
        return None
    return f"{entry.size}:{entry.mtime}"


def month_zip_status(
    facts: ListingFacts,
    fingerprint: str | None,
    previous: str | None,
) -> str:
    if facts.month_zip is None:
        return "ABSENT"
    if fingerprint is None or previous is None:
        return "PRESENT_CHANGED"
    return "PRESENT_UNCHANGED" if fingerprint == previous else "PRESENT_CHANGED"


def validate_status(field: str, value: str) -> str:
    allowed = {
        "daily_route": DAILY_ALLOWED,
        "month_route": MONTH_ALLOWED,
        "inbox": INBOX_ALLOWED,
    }.get(field)
    if allowed is None or value not in allowed:
        raise ValueError(f"VOCABULARY: {field}={value!r} is not an allowed status")
    return value
