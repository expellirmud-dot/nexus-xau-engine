"""Decision-neutral 07:00 route availability observer.

Contract: docs/0700_ROUTE_PROBE_AUTOMATION_CONTRACT_V0_1_2026-11-05.md

This script records WHICH route exposes data and WHETHER new owner files
appeared. It does not compute a State Packet, does not rebuild M1, does not
validate archives, does not decide the input route, and does not touch any
research authority. See contract section 3.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import os
import sys
import tempfile
import time
import zipfile
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

from nexus_xau.data.exness_tick_archive import (
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


def boundary_minute_bounds(day: date) -> tuple[str, str]:
    start = datetime(day.year, day.month, day.day, tzinfo=UTC)
    return (
        start.strftime("%Y-%m-%d %H:%M"),
        (start + timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M"),
    )


def _tick_minute(raw: str) -> str:
    text = raw.strip()
    head = text[:16]
    if len(head) != 16 or head[10] != " " or head[13] != ":":
        raise ValueError(f"ARCHIVE_CSV_ROW_INVALID: unparseable timestamp {raw!r}")
    return head


def count_boundary_ticks(zip_path: Path, day: date, symbol: str = DEFAULT_SYMBOL) -> int:
    """Count rows of ``symbol`` whose timestamp falls in the boundary minute.

    Deliberately not ``nexus_xau.replay.archive_window._read_month_window``: that
    helper runs replay admission and the gap ledger, which contract section 3
    forbids inside the observer. A malformed row raises instead of being skipped,
    so a silent format change cannot read as an empty minute.
    """
    lower, upper = boundary_minute_bounds(day)
    with zipfile.ZipFile(zip_path) as archive:
        csv_members = [name for name in archive.namelist() if name.lower().endswith(".csv")]
        if len(csv_members) != 1:
            raise ValueError(f"ARCHIVE_CSV_AMBIGUOUS: {csv_members}")
        with archive.open(csv_members[0], "r") as raw:
            text = io.TextIOWrapper(raw, encoding="utf-8-sig", newline="")
            reader = csv.reader(text)
            header = next(reader, None)
            normalized = [cell.strip() for cell in (header or [])]
            if normalized != ["Exness", "Symbol", "Timestamp", "Bid", "Ask"]:
                raise ValueError(f"ARCHIVE_CSV_HEADER_INVALID: {header}")
            count = 0
            for row in reader:
                if len(row) != 5:
                    raise ValueError(f"ARCHIVE_CSV_ROW_INVALID: {row}")
                if row[1].strip() != symbol:
                    continue
                if lower <= _tick_minute(row[2]) < upper:
                    count += 1
            return count


def scan_inbox(directory: Path, previous_newest: str | None) -> tuple[str, str | None, int]:
    """Report whether the owner inbox gained a file since the last run.

    Only top-level files count; dated subdirectories are intake structure, not
    new source material.
    """
    if not directory.is_dir():
        return ("DIR_MISSING", None, 0)
    newest: str | None = None
    count = 0
    for child in sorted(directory.iterdir()):
        if not child.is_file():
            continue
        count += 1
        modified = iso_utc(datetime.fromtimestamp(child.stat().st_mtime, tz=UTC))
        if newest is None or modified > newest:
            newest = modified
    if newest is None:
        return ("NO_NEW_FILES", None, 0)
    if previous_newest is None or newest > previous_newest:
        return ("NEW_FILES", newest, count)
    return ("NO_NEW_FILES", newest, count)


SUSPEND_AFTER_CONSECUTIVE_ERRORS = 3
TRANSITION_FIELDS = ("daily_route", "month_route", "inbox")
STATUS_OK = "OK"


@dataclass(frozen=True)
class ProbeConfig:
    symbol: str
    checkpoint_day: date
    cadence_minutes: int
    watch_dir: Path
    inbox_dir: Path
    cache_dir: Path
    timeout_seconds: float
    force: bool


def fetch_listing(url: str, timeout_seconds: float) -> list[ArchiveEntry]:
    return fetch_directory(url, timeout_seconds=timeout_seconds)


def download_zip(url: str, target: Path, timeout_seconds: float) -> Path:
    target.parent.mkdir(parents=True, exist_ok=True)
    request = Request(url, headers={"User-Agent": USER_AGENT})
    temporary = target.with_suffix(".part")
    with urlopen(request, timeout=timeout_seconds) as response, temporary.open("wb") as handle:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            handle.write(chunk)
    os.replace(temporary, target)
    return target


def month_zip_cache_path(config: ProbeConfig, zip_name: str) -> Path:
    return config.cache_dir / config.symbol / f"{config.checkpoint_day.year:04d}" / zip_name


def _state_string(state: dict[str, object], key: str) -> str | None:
    value = state.get(key)
    return value if isinstance(value, str) and value else None


def _empty_observation(config: ProbeConfig, now: datetime, status: str) -> dict[str, object]:
    return {
        "at_utc": iso_utc(now),
        "status": status,
        "symbol": config.symbol,
        "checkpoint_day": config.checkpoint_day.isoformat(),
        "daily_route": NOT_PROBED,
        "month_route": NOT_PROBED,
        "inbox": NOT_PROBED,
        "boundary_minute_tick_count": None,
        "forced": config.force,
        "error_class": None,
        "elapsed_ms": 0,
        "retry_count": 0,
        "next_run_at": iso_utc(now + timedelta(minutes=config.cadence_minutes)),
    }


def _fetch_with_retry(url: str, timeout_seconds: float, fetcher):
    """One attempt, one retry, never more (contract section 7.2)."""
    try:
        return fetcher(url, timeout_seconds), 0, None
    except (ArchiveAcquisitionError, URLError, OSError):
        try:
            return fetcher(url, timeout_seconds), 1, None
        except (ArchiveAcquisitionError, URLError, OSError) as second:
            return [], 1, type(second).__name__


def transition_hints(
    previous: dict[str, object] | None, observation: dict[str, object]
) -> list[str]:
    if previous is None:
        return []
    hints: list[str] = []
    for field in TRANSITION_FIELDS:
        before = previous.get(field)
        after = observation.get(field)
        if not (isinstance(before, str) and isinstance(after, str)):
            continue
        # NOT_PROBED records that a run stopped before reaching the check; it is
        # not a statement about the route, so it must never read as a flip.
        if before == NOT_PROBED or after == NOT_PROBED or before == after:
            continue
        hints.append(f"MATERIAL_TRANSITION: {field} {before} -> {after}")
    return hints


def next_error_streak(state: dict[str, object], observation: dict[str, object]) -> int:
    if observation.get("error_class"):
        previous = state.get("error_streak")
        return (previous if isinstance(previous, int) else 0) + 1
    return 0


def _probe_listing(
    config: ProbeConfig,
    state: dict[str, object],
    observation: dict[str, object],
    listing_fetcher,
    zip_downloader,
) -> None:
    entries, retries, error_class = _fetch_with_retry(
        month_directory_url(config.symbol, config.checkpoint_day),
        config.timeout_seconds,
        listing_fetcher,
    )
    observation["retry_count"] = retries
    if error_class is not None:
        # A transport failure is never an absence claim (contract section 7.3).
        observation["daily_route"] = validate_status("daily_route", "LISTING_UNREADABLE")
        observation["month_route"] = validate_status("month_route", "LISTING_UNREADABLE")
        observation["error_class"] = error_class
        return

    facts = classify_listing(entries, config.symbol, config.checkpoint_day)
    observation["daily_route"] = validate_status("daily_route", daily_route_status(facts))
    fingerprint = fingerprint_of(facts.month_zip)
    previous_fingerprint = _state_string(state, "month_zip_fingerprint")
    observation["month_route"] = validate_status(
        "month_route", month_zip_status(facts, fingerprint, previous_fingerprint)
    )
    if facts.month_zip is None or fingerprint is None:
        return
    state["month_zip_fingerprint"] = fingerprint
    if observation["month_route"] != "PRESENT_CHANGED":
        return

    try:
        downloaded = zip_downloader(
            month_zip_url(config.symbol, config.checkpoint_day),
            month_zip_cache_path(config, facts.month_zip.name),
            config.timeout_seconds,
        )
        observation["boundary_minute_tick_count"] = count_boundary_ticks(
            downloaded, config.checkpoint_day, config.symbol
        )
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        observation["error_class"] = type(exc).__name__


def run_probe(
    config: ProbeConfig,
    *,
    now: datetime,
    listing_fetcher,
    zip_downloader,
) -> dict[str, object]:
    started = time.monotonic()
    state_path = config.watch_dir / "state.json"
    log_path = config.watch_dir / "observations.ndjson"
    state = load_state(state_path)
    due = compute_due(state, now, config.cadence_minutes)

    # Suspension is checked before force: a routine call must not re-ignite a
    # suspended observer, and resuming means a human editing state.json.
    if due == STATUS_SUSPENDED:
        observation = _empty_observation(config, now, STATUS_SUSPENDED)
        observation["error_class"] = STATUS_SUSPENDED
        observation["next_run_at"] = (
            _state_string(state, "next_run_at") or observation["next_run_at"]
        )
        append_observation(log_path, observation)
        return observation

    if due == STATUS_NOT_YET_DUE and not config.force:
        observation = _empty_observation(config, now, STATUS_NOT_YET_DUE)
        observation["next_run_at"] = (
            _state_string(state, "next_run_at") or observation["next_run_at"]
        )
        append_observation(log_path, observation)
        return observation

    observation = _empty_observation(config, now, STATUS_DUE)
    _probe_listing(config, state, observation, listing_fetcher, zip_downloader)
    # The inbox is scanned even when the market probe failed: the two facts stay
    # independent, and a dead archive route must not blind the source lane.
    inbox_status, inbox_newest, inbox_count = scan_inbox(
        config.inbox_dir, _state_string(state, "inbox_newest")
    )
    observation["inbox"] = validate_status("inbox", inbox_status)
    if inbox_newest is not None:
        state["inbox_newest"] = inbox_newest
    if inbox_count:
        observation["inbox_file_count"] = inbox_count

    observation["elapsed_ms"] = int((time.monotonic() - started) * 1000)
    streak = next_error_streak(state, observation)
    state["error_streak"] = streak
    state["status"] = (
        STATUS_SUSPENDED if streak >= SUSPEND_AFTER_CONSECUTIVE_ERRORS else STATUS_OK
    )
    state["last_run_at"] = observation["at_utc"]
    state["next_run_at"] = observation["next_run_at"]
    save_state(state_path, state)
    append_observation(log_path, observation)
    return observation


DEFAULT_CACHE_DIR = Path("data/raw/exness_tick_history/current_month_probe")
ZONE = "Asia/Bangkok"


def _resolve_checkpoint_day(raw: str | None) -> date:
    if raw:
        return date.fromisoformat(raw)
    return datetime.now(ZoneInfo(ZONE)).date()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Decision-neutral 07:00 route availability observer (contract V0.1)."
    )
    parser.add_argument("--once", action="store_true", required=True)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--cadence-minutes", type=int, default=DEFAULT_CADENCE_MINUTES)
    parser.add_argument("--symbol", default=DEFAULT_SYMBOL)
    parser.add_argument("--checkpoint-day", default=None)
    parser.add_argument("--watch-dir", type=Path, default=DEFAULT_WATCH_DIR)
    parser.add_argument("--inbox", type=Path, default=DEFAULT_INBOX_DIR)
    parser.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE_DIR)
    parser.add_argument("--timeout-seconds", type=float, default=30.0)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    watch_dir: Path = args.watch_dir
    if args.cadence_minutes <= 0:
        print("PROBE_BLOCKED: cadence_minutes must be > 0", file=sys.stderr)
        return 2
    if args.timeout_seconds <= 0:
        print("PROBE_BLOCKED: timeout_seconds must be > 0", file=sys.stderr)
        return 2
    # state.json is read a second time here, deliberately: this veto must happen
    # before any network call and before run_probe appends an observation line,
    # so a corrupt state produces no record at all.
    try:
        load_state(watch_dir / "state.json")
        checkpoint_day = _resolve_checkpoint_day(args.checkpoint_day)
    except ValueError as exc:
        print(f"PROBE_BLOCKED: {exc}", file=sys.stderr)
        return 2

    config = ProbeConfig(
        symbol=args.symbol,
        checkpoint_day=checkpoint_day,
        cadence_minutes=args.cadence_minutes,
        watch_dir=watch_dir,
        inbox_dir=args.inbox,
        cache_dir=args.cache_dir,
        timeout_seconds=args.timeout_seconds,
        force=args.force,
    )
    observation = run_probe(
        config,
        now=datetime.now(UTC),
        listing_fetcher=fetch_listing,
        zip_downloader=download_zip,
    )

    prior = read_observations(watch_dir / "observations.ndjson")[:-1]
    for hint in transition_hints(prior[-1] if prior else None, observation):
        print(hint)
    print(
        "status={status} daily_route={daily_route} month_route={month_route} "
        "inbox={inbox} boundary_minute_tick_count={boundary_minute_tick_count} "
        "error_class={error_class} next_run_at={next_run_at}".format(**observation)
    )
    return 1 if observation["error_class"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
