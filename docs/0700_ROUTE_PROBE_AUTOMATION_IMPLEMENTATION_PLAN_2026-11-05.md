# 07:00 Route Probe Automation — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a decision-neutral observer that records, on a 30-minute cadence owned by its own state file, which Exness archive route exposes 07:00 boundary-minute data and whether new owner source files appeared.

**Architecture:** One CLI script, `scripts/exness_0700_route_probe.py`, composed of pure interpretation functions plus two injected I/O boundaries (a remote listing fetcher and a ZIP downloader). Each run appends exactly one line to an append-only NDJSON log outside the repository and rewrites `state.json` atomically with the next due time. The repository holds only the contract, the code, the tests, and human-promoted transition entries — never probe output.

**Tech Stack:** Python 3.12 (repo `.venv`), stdlib only (`argparse`, `dataclasses`, `zipfile`, `csv`, `json`, `io`, `os`, `sys`, `time`, `tempfile`, `urllib`, `zoneinfo`), pytest 8, ruff 0.9. Reuses `nexus_xau.data.exness_tick_archive` (`USER_AGENT`, `ArchiveEntry`, `ArchiveAcquisitionError`, `fetch_directory`) and the URL conventions of `scripts/exness_intraday_state_packet_0700.py`.

**Spec:** `docs/0700_ROUTE_PROBE_AUTOMATION_CONTRACT_V0_1_2026-11-05.md` — read it before touching code. Every rule below traces to a contract section.

## Global Constraints

Verbatim from the contract; every task inherits them.

- Status values are a closed vocabulary: `PRESENT`, `ABSENT`, `LISTING_UNREADABLE`, `NOT_PROBED`, `PRESENT_CHANGED`, `PRESENT_UNCHANGED`, `NO_NEW_FILES`, `NEW_FILES`, `DIR_MISSING`. No other literal may appear in those fields (contract §6).
- `NOT_PROBED` appears only when the run ended before reaching that check; it is never a synonym for `ABSENT` (§6).
- Absence may be asserted only when the listing was successfully read; transport or parse failure is `LISTING_UNREADABLE` (§7.3).
- No `0700_STATE_PACKET_H4_V0` computation, no M1 rebuild, no archive validator run on downloaded bytes (§3).
- At most one month-directory listing, one day-path check (only when the month listing shows a day directory), and one ZIP fetch per run; one retry maximum; an unchanged ZIP fingerprint skips download and scan (§7.2).
- No authentication, no credential reads, no MT5 calls, no headers or response bodies logged (§7.1).
- No writes to `docs/CANONICAL_CLAIM_REGISTER_2026-09-03.json`, `docs/0700_WORKSTREAM_STATE.json`, `research_queue/QUEUE.json`, `research_findings/FINDINGS.json`; `docs/CURRENT_RESEARCH_STATE.json` gains one pointer key only, in Task 6 (§3).
- The probe never writes or commits `docs/0700_ROUTE_PROBE_LOG.md`; it only prints a `MATERIAL_TRANSITION` hint (§5).
- Watch directory default `D:/tools/nexus-0700-watch`; owner inbox default `D:/tools/nexus-video-evidence/_incoming`; ZIP cache `data/raw/exness_tick_history/current_month_probe/` (already gitignored by `data/raw/*`).
- Cadence default 30 minutes via `--cadence-minutes`; `--once` before `next_run_at` must exit `NOT_YET_DUE` with zero network calls (§4).
- Three consecutive error runs set `status: "SUSPENDED"` in `state.json` and stop probing until a human clears the flag; `--force` does not override suspension (§7.6).
- The test suite is offline: no network in pytest, ever (§8).
- Verification gate per task: `.venv\Scripts\python.exe -m pytest <test files> -v`, then `.venv\Scripts\python.exe -m ruff check <files>`.

## File Structure

| file | responsibility | action |
|---|---|---|
| `scripts/exness_0700_route_probe.py` | the whole observer: vocabulary, pure interpreters, I/O boundaries, CLI | create |
| `tests/test_route_probe_state.py` | state load/save, due gate, NDJSON append integrity | create |
| `tests/test_route_probe_listing.py` | listing classification and fingerprint decisions | create |
| `tests/test_route_probe_scan.py` | boundary-minute counting and inbox scan | create |
| `tests/test_route_probe_run.py` | orchestration: short-circuit, retry, suspension, hints, CLI | create |
| `pyproject.toml` | make `scripts/` importable from tests | modify (Task 1) |
| `docs/0700_ROUTE_PROBE_LOG.md` | promoted transitions + the one live round | create (Task 6) |
| `TOOLS.md` | reuse-before-build registry entry for the probe | modify (Task 6) |
| `docs/CURRENT_RESEARCH_STATE.json` | one resume-visible pointer to the lane | modify (Task 6) |

Why four test files instead of one: each maps to one unit boundary (state, listing, scan, orchestration), so a reviewer can reject one contract clause without approving or rejecting its neighbour.

---

### Task 1: Vocabulary, state store, and the due gate

**Files:**
- Create: `scripts/exness_0700_route_probe.py`
- Test: `tests/test_route_probe_state.py`
- Modify: `pyproject.toml` (`[tool.pytest.ini_options]`)

**Interfaces:**
- Consumes: nothing (first task).
- Produces: `DAILY_ALLOWED: frozenset[str]`, `MONTH_ALLOWED: frozenset[str]`, `INBOX_ALLOWED: frozenset[str]`, `NOT_PROBED = "NOT_PROBED"`, `STATUS_DUE = "DUE"`, `STATUS_NOT_YET_DUE = "NOT_YET_DUE"`, `STATUS_SUSPENDED = "SUSPENDED"`, `DEFAULT_CADENCE_MINUTES = 30`, `DEFAULT_SYMBOL = "XAUUSDm"`, `DEFAULT_WATCH_DIR: Path`, `DEFAULT_INBOX_DIR: Path`, `iso_utc(value: datetime) -> str`, `load_state(path: Path) -> dict[str, object]`, `save_state(path: Path, state: dict[str, object]) -> None`, `compute_due(state: dict[str, object], now: datetime, cadence_minutes: int) -> str`, `append_observation(path: Path, observation: dict[str, object]) -> None`, `read_observations(path: Path) -> list[dict[str, object]]`.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_route_probe_state.py`:

```python
from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from exness_0700_route_probe import (
    DAILY_ALLOWED,
    INBOX_ALLOWED,
    MONTH_ALLOWED,
    NOT_PROBED,
    STATUS_DUE,
    STATUS_NOT_YET_DUE,
    STATUS_SUSPENDED,
    append_observation,
    compute_due,
    iso_utc,
    load_state,
    read_observations,
    save_state,
)

NOW = datetime(2026, 11, 5, 12, 0, 0, tzinfo=UTC)


def test_closed_vocabularies_are_exact_sets() -> None:
    assert DAILY_ALLOWED == frozenset({"PRESENT", "ABSENT", "LISTING_UNREADABLE", NOT_PROBED})
    assert MONTH_ALLOWED == frozenset(
        {"PRESENT_CHANGED", "PRESENT_UNCHANGED", "ABSENT", "LISTING_UNREADABLE", NOT_PROBED}
    )
    assert INBOX_ALLOWED == frozenset({"NO_NEW_FILES", "NEW_FILES", "DIR_MISSING", NOT_PROBED})


def test_missing_state_file_reads_as_empty_dict(tmp_path: Path) -> None:
    assert load_state(tmp_path / "state.json") == {}


def test_save_state_round_trips_and_creates_parent(tmp_path: Path) -> None:
    target = tmp_path / "watch" / "state.json"
    save_state(target, {"next_run_at": iso_utc(NOW)})
    assert load_state(target) == {"next_run_at": iso_utc(NOW)}
    assert not list((tmp_path / "watch").glob(".state-*"))


def test_corrupt_state_file_raises_instead_of_silently_resetting(tmp_path: Path) -> None:
    target = tmp_path / "state.json"
    target.write_text("{not json", encoding="utf-8")
    with pytest.raises(ValueError, match="STATE_FILE_UNREADABLE"):
        load_state(target)


def test_state_file_holding_a_list_is_rejected(tmp_path: Path) -> None:
    target = tmp_path / "state.json"
    target.write_text("[]", encoding="utf-8")
    with pytest.raises(ValueError, match="STATE_FILE_UNREADABLE"):
        load_state(target)


def test_no_previous_run_is_due() -> None:
    assert compute_due({}, NOW, 30) == STATUS_DUE


def test_future_next_run_is_not_due() -> None:
    state = {"next_run_at": iso_utc(NOW + timedelta(minutes=22))}
    assert compute_due(state, NOW, 30) == STATUS_NOT_YET_DUE


def test_past_next_run_is_due() -> None:
    state = {"next_run_at": iso_utc(NOW - timedelta(seconds=1))}
    assert compute_due(state, NOW, 30) == STATUS_DUE


def test_unparseable_next_run_is_treated_as_due() -> None:
    assert compute_due({"next_run_at": "not-a-time"}, NOW, 30) == STATUS_DUE


def test_suspended_state_is_never_due_even_when_past() -> None:
    state = {"status": STATUS_SUSPENDED, "next_run_at": iso_utc(NOW - timedelta(hours=5))}
    assert compute_due(state, NOW, 30) == STATUS_SUSPENDED


def test_append_observation_writes_one_line_per_run(tmp_path: Path) -> None:
    target = tmp_path / "observations.ndjson"
    append_observation(target, {"at_utc": iso_utc(NOW), "daily_route": "ABSENT"})
    append_observation(target, {"at_utc": iso_utc(NOW + timedelta(minutes=30))})
    lines = target.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert json.loads(lines[0])["daily_route"] == "ABSENT"
    assert json.loads(lines[1])["at_utc"] == iso_utc(NOW + timedelta(minutes=30))


def test_read_observations_skips_blank_and_malformed_lines_without_rewriting(
    tmp_path: Path,
) -> None:
    target = tmp_path / "observations.ndjson"
    good = {"at_utc": iso_utc(NOW)}
    target.write_text(
        "\n".join([json.dumps(good), "{broken", "", json.dumps(good)]) + "\n",
        encoding="utf-8",
    )
    before = target.read_text(encoding="utf-8")
    assert read_observations(target) == [good, good]
    assert target.read_text(encoding="utf-8") == before


def test_read_observations_on_missing_file_is_empty(tmp_path: Path) -> None:
    assert read_observations(tmp_path / "absent.ndjson") == []
```

- [ ] **Step 2: Run the tests and verify they fail**

Run: `.venv\Scripts\python.exe -m pytest tests/test_route_probe_state.py -v`
Expected: collection error `ModuleNotFoundError: No module named 'exness_0700_route_probe'`.

- [ ] **Step 3: Make the script importable from tests**

In `pyproject.toml`, change the existing line inside `[tool.pytest.ini_options]` from `pythonpath = ["src"]` to:

```toml
pythonpath = ["src", "scripts"]
```

- [ ] **Step 4: Write the minimal implementation**

Create `scripts/exness_0700_route_probe.py`. The module docstring must name the contract so a future reader cannot mistake this for a calculator:

```python
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
from datetime import UTC, datetime
from pathlib import Path

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
        raise ValueError(f"STATE_FILE_UNREADABLE: {path} must contain an object")
    return payload


def save_state(path: Path, state: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=path.parent,
        prefix=".state-",
        suffix=".tmp",
        delete=False,
    )
    try:
        with handle:
            json.dump(state, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(handle.name, path)
    finally:
        if os.path.exists(handle.name):
            os.unlink(handle.name)


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
```

- [ ] **Step 5: Run the tests and verify they pass**

Run: `.venv\Scripts\python.exe -m pytest tests/test_route_probe_state.py -v`
Expected: 13 passed.

Run: `.venv\Scripts\python.exe -m ruff check scripts/exness_0700_route_probe.py tests/test_route_probe_state.py`
Expected: `All checks passed!`

- [ ] **Step 6: Commit**

```bash
git add scripts/exness_0700_route_probe.py tests/test_route_probe_state.py pyproject.toml
git commit -m "probe: add route observer state store and due gate"
```

---

### Task 2: Listing interpretation, month fingerprint, and vocabulary guard

**Files:**
- Modify: `scripts/exness_0700_route_probe.py`
- Test: `tests/test_route_probe_listing.py`

**Interfaces:**
- Consumes: `DAILY_ALLOWED`, `MONTH_ALLOWED`, `INBOX_ALLOWED`, `NOT_PROBED` from Task 1; `nexus_xau.data.exness_tick_archive.ArchiveEntry`.
- Produces: `BASE_URL = "https://ticks.ex2archive.com/ticks"`, `month_directory_url(symbol: str, day: date) -> str`, `month_zip_name(symbol: str, day: date) -> str`, `month_zip_url(symbol: str, day: date) -> str`, `day_directory_url(symbol: str, day: date) -> str`, `day_zip_url(symbol: str, day: date) -> str`, `ListingFacts` (frozen dataclass: `day_directory_present: bool`, `month_zip: ArchiveEntry | None`), `classify_listing(entries: list[ArchiveEntry], symbol: str, day: date) -> ListingFacts`, `daily_route_status(facts: ListingFacts) -> str`, `fingerprint_of(entry: ArchiveEntry | None) -> str | None`, `month_zip_status(facts: ListingFacts, fingerprint: str | None, previous: str | None) -> str`, `validate_status(field: str, value: str) -> str`.

One month listing answers both existence questions, which is why `classify_listing` takes the month entries: it detects the day subdirectory (`name == "05"`) and the month ZIP entry in the same JSON payload that `fetch_directory` already parses. The day path is only probed further when `day_directory_present` is true, keeping the run inside the contract's one-listing budget.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_route_probe_listing.py`:

```python
from __future__ import annotations

from datetime import date

import pytest

from exness_0700_route_probe import (
    classify_listing,
    daily_route_status,
    day_directory_url,
    day_zip_url,
    fingerprint_of,
    month_directory_url,
    month_zip_status,
    month_zip_url,
    validate_status,
)
from nexus_xau.data.exness_tick_archive import ArchiveEntry

DAY = date(2026, 11, 5)
MONTH_ZIP = "Exness_XAUUSDm_2026_11.zip"


def test_urls_follow_the_existing_archive_layout() -> None:
    assert month_directory_url("XAUUSDm", DAY) == (
        "https://ticks.ex2archive.com/ticks/XAUUSDm/2026/11/"
    )
    assert month_zip_url("XAUUSDm", DAY) == (
        "https://ticks.ex2archive.com/ticks/XAUUSDm/2026/11/" + MONTH_ZIP
    )
    assert day_directory_url("XAUUSDm", DAY) == (
        "https://ticks.ex2archive.com/ticks/XAUUSDm/2026/11/05/"
    )
    assert day_zip_url("XAUUSDm", DAY) == (
        "https://ticks.ex2archive.com/ticks/XAUUSDm/2026/11/05/"
        "Exness_XAUUSDm_2026_11_05.zip"
    )


def test_day_directory_present_reads_as_present() -> None:
    facts = classify_listing(
        [
            ArchiveEntry(name="05", type="directory"),
            ArchiveEntry(name=MONTH_ZIP, type="file", size=1, mtime="x"),
        ],
        "XAUUSDm",
        DAY,
    )
    assert facts.day_directory_present is True
    assert facts.month_zip is not None
    assert daily_route_status(facts) == "PRESENT"


def test_month_listing_without_day_directory_reads_as_absent() -> None:
    facts = classify_listing(
        [ArchiveEntry(name=MONTH_ZIP, type="file", size=10, mtime="m")], "XAUUSDm", DAY
    )
    assert facts.day_directory_present is False
    assert daily_route_status(facts) == "ABSENT"


def test_empty_but_readable_listing_reads_as_absent_not_unreadable() -> None:
    facts = classify_listing([], "XAUUSDm", DAY)
    assert daily_route_status(facts) == "ABSENT"
    assert facts.month_zip is None


def test_entry_named_like_but_not_the_day_directory_is_not_a_day_directory() -> None:
    facts = classify_listing([ArchiveEntry(name="05x", type="directory")], "XAUUSDm", DAY)
    assert facts.day_directory_present is False


def test_fingerprint_uses_size_and_mtime() -> None:
    facts = classify_listing(
        [ArchiveEntry(name=MONTH_ZIP, type="file", size=42, mtime="T")], "XAUUSDm", DAY
    )
    assert fingerprint_of(facts.month_zip) == "42:T"


def test_entry_without_size_or_mtime_fingerprints_as_none() -> None:
    facts = classify_listing(
        [ArchiveEntry(name=MONTH_ZIP, type="file", size=None, mtime=None)], "XAUUSDm", DAY
    )
    assert fingerprint_of(facts.month_zip) is None
    assert month_zip_status(facts, None, "42:T") == "PRESENT_CHANGED"


def test_missing_month_zip_is_absent_regardless_of_previous() -> None:
    facts = classify_listing([ArchiveEntry(name="05", type="directory")], "XAUUSDm", DAY)
    assert month_zip_status(facts, None, None) == "ABSENT"


def test_first_seen_fingerprint_is_changed() -> None:
    facts = classify_listing(
        [ArchiveEntry(name=MONTH_ZIP, type="file", size=42, mtime="T")], "XAUUSDm", DAY
    )
    assert month_zip_status(facts, "42:T", None) == "PRESENT_CHANGED"


def test_identical_fingerprint_is_unchanged() -> None:
    facts = classify_listing(
        [ArchiveEntry(name=MONTH_ZIP, type="file", size=42, mtime="T")], "XAUUSDm", DAY
    )
    assert month_zip_status(facts, "42:T", "42:T") == "PRESENT_UNCHANGED"


def test_different_fingerprint_is_changed() -> None:
    facts = classify_listing(
        [ArchiveEntry(name=MONTH_ZIP, type="file", size=43, mtime="T")], "XAUUSDm", DAY
    )
    assert month_zip_status(facts, "43:T", "42:T") == "PRESENT_CHANGED"


def test_validate_status_accepts_only_the_closed_vocabulary() -> None:
    assert validate_status("daily_route", "PRESENT") == "PRESENT"
    assert validate_status("month_route", "PRESENT_UNCHANGED") == "PRESENT_UNCHANGED"
    assert validate_status("inbox", "NOT_PROBED") == "NOT_PROBED"


def test_validate_status_rejects_invented_status_values() -> None:
    with pytest.raises(ValueError, match="VOCABULARY"):
        validate_status("daily_route", "PRESENT_BUT_MAYBE")
    with pytest.raises(ValueError, match="VOCABULARY"):
        validate_status("inbox", "MAYBE_NEW")
    with pytest.raises(ValueError, match="VOCABULARY"):
        validate_status("unknown_field", "PRESENT")
```

- [ ] **Step 2: Run the tests and verify they fail**

Run: `.venv\Scripts\python.exe -m pytest tests/test_route_probe_listing.py -v`
Expected: `ImportError: cannot import name 'classify_listing'`.

- [ ] **Step 3: Write the implementation**

In `scripts/exness_0700_route_probe.py`, extend the stdlib datetime import to `from datetime import UTC, date, datetime`, add `from dataclasses import dataclass`, then append:

```python
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
```

`ArchiveEntry` is imported from the existing package, never redefined. Add this import block above `BASE_URL`, mirroring how `scripts/exness_intraday_state_packet_0700.py` imports from the same module:

```python
from nexus_xau.data.exness_tick_archive import (
    USER_AGENT,
    ArchiveAcquisitionError,
    ArchiveEntry,
    fetch_directory,
)
```

`USER_AGENT`, `ArchiveAcquisitionError`, and `fetch_directory` stay unused until Task 4. In this step write the block as:

```python
from nexus_xau.data.exness_tick_archive import (  # noqa: F401  (used from Task 4)
    USER_AGENT,
    ArchiveAcquisitionError,
    ArchiveEntry,
    fetch_directory,
)
```

and drop the `# noqa` comment in Task 4 Step 3 once every name is live.

- [ ] **Step 4: Run the tests and verify they pass**

Run: `.venv\Scripts\python.exe -m pytest tests/test_route_probe_listing.py tests/test_route_probe_state.py -v`
Expected: 26 passed.

Run: `.venv\Scripts\python.exe -m ruff check scripts/exness_0700_route_probe.py tests/test_route_probe_listing.py`
Expected: `All checks passed!`

- [ ] **Step 5: Commit**

```bash
git add scripts/exness_0700_route_probe.py tests/test_route_probe_listing.py
git commit -m "probe: classify archive listing and month fingerprint"
```

---

### Task 3: Boundary-minute count and owner inbox scan

**Files:**
- Modify: `scripts/exness_0700_route_probe.py`
- Test: `tests/test_route_probe_scan.py`

**Interfaces:**
- Consumes: `DEFAULT_SYMBOL`, `iso_utc` from Task 1; `date`/`datetime`/`timedelta`/`UTC` as extended in Task 2.
- Produces: `boundary_minute_bounds(day: date) -> tuple[str, str]`, `count_boundary_ticks(zip_path: Path, day: date, symbol: str = DEFAULT_SYMBOL) -> int`, `scan_inbox(directory: Path, previous_newest: str | None) -> tuple[str, str | None, int]` returning `(status, newest_mtime_iso, file_count)`.

Why this scan is not `_read_month_window`: `nexus_xau.replay.archive_window._read_month_window` runs the replay admission and gap-ledger contract, which is exactly the validator work contract §3 forbids inside the observer. The count is an independent CSV minute-window match over rows of the declared symbol and nothing else.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_route_probe_scan.py`:

```python
from __future__ import annotations

import csv
import zipfile
from datetime import date
from io import StringIO
from pathlib import Path

import pytest

from exness_0700_route_probe import (
    boundary_minute_bounds,
    count_boundary_ticks,
    scan_inbox,
)

DAY = date(2026, 11, 5)
HEADER = ["Exness", "Symbol", "Timestamp", "Bid", "Ask"]


def write_zip(tmp_path: Path, rows: list[list[str]], member: str = "ticks.csv") -> Path:
    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(HEADER)
    writer.writerows(rows)
    target = tmp_path / "month.zip"
    with zipfile.ZipFile(target, "w") as archive:
        archive.writestr(member, buffer.getvalue())
    return target


def test_boundary_minute_is_the_single_00_00_utc_minute() -> None:
    assert boundary_minute_bounds(DAY) == ("2026-11-05 00:00", "2026-11-05 00:01")


def test_ticks_inside_the_minute_are_counted(tmp_path: Path) -> None:
    zip_path = write_zip(
        tmp_path,
        [
            ["Exness", "XAUUSDm", "2026-11-05 00:00:00.017", "4108.073", "4108.173"],
            ["Exness", "XAUUSDm", "2026-11-05 00:00:59.999", "4108.074", "4108.174"],
            ["Exness", "XAUUSDm", "2026-11-05 00:01:00.001", "4108.075", "4108.175"],
            ["Exness", "XAUUSDm", "2026-11-04 23:59:59.000", "4108.070", "4108.170"],
        ],
    )
    assert count_boundary_ticks(zip_path, DAY) == 2


def test_wrong_symbol_and_wrong_minute_do_not_count(tmp_path: Path) -> None:
    zip_path = write_zip(
        tmp_path,
        [
            ["Exness", "XAUUSD", "2026-11-05 00:00:10.000", "1", "2"],
            ["Exness", "XAUUSDm", "2026-11-05 00:02:10.000", "1", "2"],
        ],
    )
    assert count_boundary_ticks(zip_path, DAY) == 0


def test_symbol_is_configurable(tmp_path: Path) -> None:
    zip_path = write_zip(
        tmp_path, [["Exness", "XAUUSDc", "2026-11-05 00:00:10.000", "1", "2"]]
    )
    assert count_boundary_ticks(zip_path, DAY, "XAUUSDc") == 1
    assert count_boundary_ticks(zip_path, DAY) == 0


def test_zip_without_exactly_one_csv_is_an_error_not_zero(tmp_path: Path) -> None:
    target = tmp_path / "two.zip"
    with zipfile.ZipFile(target, "w") as archive:
        archive.writestr("a.csv", "x")
        archive.writestr("b.csv", "y")
    with pytest.raises(ValueError, match="ARCHIVE_CSV_AMBIGUOUS"):
        count_boundary_ticks(target, DAY)


def test_unexpected_header_is_reported_not_silently_skipped(tmp_path: Path) -> None:
    target = tmp_path / "bad_header.zip"
    with zipfile.ZipFile(target, "w") as archive:
        archive.writestr("ticks.csv", "something,else\n")
    with pytest.raises(ValueError, match="ARCHIVE_CSV_HEADER_INVALID"):
        count_boundary_ticks(target, DAY)


def test_malformed_timestamp_is_reported_not_silently_skipped(tmp_path: Path) -> None:
    zip_path = write_zip(tmp_path, [["Exness", "XAUUSDm", "not-a-time", "1", "2"]])
    with pytest.raises(ValueError, match="ARCHIVE_CSV_ROW_INVALID"):
        count_boundary_ticks(zip_path, DAY)


def test_row_with_wrong_column_count_is_reported(tmp_path: Path) -> None:
    zip_path = write_zip(tmp_path, [["Exness", "XAUUSDm", "2026-11-05 00:00:01.000", "1"]])
    with pytest.raises(ValueError, match="ARCHIVE_CSV_ROW_INVALID"):
        count_boundary_ticks(zip_path, DAY)


def test_missing_inbox_directory_reports_dir_missing(tmp_path: Path) -> None:
    assert scan_inbox(tmp_path / "nope", None) == ("DIR_MISSING", None, 0)


def test_empty_inbox_is_no_new_files(tmp_path: Path) -> None:
    assert scan_inbox(tmp_path, None) == ("NO_NEW_FILES", None, 0)


def test_new_file_changes_status_to_new_files(tmp_path: Path) -> None:
    (tmp_path / "VID_3.txt").write_text("x", encoding="utf-8")
    status, newest, count = scan_inbox(tmp_path, None)
    assert status == "NEW_FILES"
    assert count == 1
    assert newest is not None
    assert scan_inbox(tmp_path, newest)[0] == "NO_NEW_FILES"


def test_file_older_than_previous_newest_is_no_new_files(tmp_path: Path) -> None:
    (tmp_path / "VID_3.txt").write_text("x", encoding="utf-8")
    future = "2037-01-01T00:00:00+00:00"
    assert scan_inbox(tmp_path, future)[0] == "NO_NEW_FILES"


def test_subdirectories_are_not_counted_as_source_files(tmp_path: Path) -> None:
    (tmp_path / "2026-09-12").mkdir()
    assert scan_inbox(tmp_path, None) == ("NO_NEW_FILES", None, 0)
```

- [ ] **Step 2: Run the tests and verify they fail**

Run: `.venv\Scripts\python.exe -m pytest tests/test_route_probe_scan.py -v`
Expected: `ImportError: cannot import name 'boundary_minute_bounds'`.

- [ ] **Step 3: Write the implementation**

In `scripts/exness_0700_route_probe.py`, add `import csv`, `import io`, `import zipfile` to the stdlib import block, then append:

```python
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
```

- [ ] **Step 4: Run the tests and verify they pass**

Run: `.venv\Scripts\python.exe -m pytest tests/test_route_probe_scan.py tests/test_route_probe_listing.py tests/test_route_probe_state.py -v`
Expected: 39 passed.

Run: `.venv\Scripts\python.exe -m ruff check scripts/exness_0700_route_probe.py tests/test_route_probe_scan.py`
Expected: `All checks passed!`

- [ ] **Step 5: Commit**

```bash
git add scripts/exness_0700_route_probe.py tests/test_route_probe_scan.py
git commit -m "probe: count boundary-minute ticks and scan owner inbox"
```

---

### Task 4: Orchestration with injected I/O, bounded traffic, retry, and suspension

**Files:**
- Modify: `scripts/exness_0700_route_probe.py`
- Test: `tests/test_route_probe_run.py`

**Interfaces:**
- Consumes: Tasks 1–3 (`classify_listing`, `daily_route_status`, `month_zip_status`, `fingerprint_of`, `validate_status`, `count_boundary_ticks`, `scan_inbox`, `compute_due`, `load_state`, `save_state`, `append_observation`, `iso_utc`, `NOT_PROBED`, `STATUS_*`) and `fetch_directory` / `USER_AGENT` / `ArchiveAcquisitionError` / `ArchiveEntry`.
- Produces: `ProbeConfig` frozen dataclass (`symbol: str`, `checkpoint_day: date`, `cadence_minutes: int`, `watch_dir: Path`, `inbox_dir: Path`, `cache_dir: Path`, `timeout_seconds: float`, `force: bool`), `SUSPEND_AFTER_CONSECUTIVE_ERRORS = 3`, `TRANSITION_FIELDS: tuple[str, str, str]`, `STATUS_OK = "OK"`, `fetch_listing(url: str, timeout_seconds: float) -> list[ArchiveEntry]`, `download_zip(url: str, target: Path, timeout_seconds: float) -> Path`, `month_zip_cache_path(config: ProbeConfig, zip_name: str) -> Path`, `run_probe(config: ProbeConfig, *, now: datetime, listing_fetcher, zip_downloader) -> dict[str, object]`, `transition_hints(previous: dict[str, object] | None, observation: dict[str, object]) -> list[str]`, `next_error_streak(state: dict[str, object], observation: dict[str, object]) -> int`.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_route_probe_run.py`:

```python
from __future__ import annotations

import csv
import zipfile
from datetime import UTC, date, datetime, timedelta
from io import StringIO
from pathlib import Path

import pytest

from exness_0700_route_probe import (
    MONTH_ALLOWED,
    SUSPEND_AFTER_CONSECUTIVE_ERRORS,
    ProbeConfig,
    load_state,
    run_probe,
    save_state,
    transition_hints,
)
from nexus_xau.data.exness_tick_archive import ArchiveAcquisitionError, ArchiveEntry

NOW = datetime(2026, 11, 5, 12, 0, 0, tzinfo=UTC)
DAY = date(2026, 11, 5)
MONTH_ZIP = "Exness_XAUUSDm_2026_11.zip"
HEADER = ["Exness", "Symbol", "Timestamp", "Bid", "Ask"]


def iso(value: datetime) -> str:
    return value.astimezone(UTC).isoformat(timespec="seconds")


def make_config(tmp_path: Path, *, force: bool = False) -> ProbeConfig:
    return ProbeConfig(
        symbol="XAUUSDm",
        checkpoint_day=DAY,
        cadence_minutes=30,
        watch_dir=tmp_path / "watch",
        inbox_dir=tmp_path / "inbox",
        cache_dir=tmp_path / "cache",
        timeout_seconds=5.0,
        force=force,
    )


def seed_state(config: ProbeConfig, **values: object) -> None:
    config.watch_dir.mkdir(parents=True, exist_ok=True)
    save_state(config.watch_dir / "state.json", dict(values))


def month_only_listing() -> list[ArchiveEntry]:
    return [ArchiveEntry(name=MONTH_ZIP, type="file", size=100, mtime="M1")]


def listing_with_day_directory() -> list[ArchiveEntry]:
    return [
        ArchiveEntry(name="05", type="directory"),
        ArchiveEntry(name=MONTH_ZIP, type="file", size=100, mtime="M1"),
    ]


def write_boundary_zip(target: Path, timestamps: list[str]) -> Path:
    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(HEADER)
    for stamp in timestamps:
        writer.writerow(["Exness", "XAUUSDm", stamp, "4108.073", "4108.173"])
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w") as archive:
        archive.writestr("ticks.csv", buffer.getvalue())
    return target


def downloader_for(timestamps: list[str]):
    def download(url: str, target: Path, timeout_seconds: float) -> Path:
        return write_boundary_zip(target, timestamps)

    return download


def forbidden_downloader(url: str, target: Path, timeout_seconds: float) -> Path:
    raise AssertionError(f"zip must not be downloaded: {url}")


def forbidden_fetcher(url: str, timeout_seconds: float) -> list[ArchiveEntry]:
    raise AssertionError(f"no network call allowed: {url}")


def static_listing_fetcher(entries: list[ArchiveEntry]):
    def fetch(url: str, timeout_seconds: float) -> list[ArchiveEntry]:
        return entries

    return fetch


def test_not_yet_due_short_circuits_with_zero_calls(tmp_path: Path) -> None:
    config = make_config(tmp_path)
    seed_state(config, next_run_at=iso(NOW + timedelta(minutes=10)))
    observation = run_probe(
        config,
        now=NOW,
        listing_fetcher=forbidden_fetcher,
        zip_downloader=forbidden_downloader,
    )
    assert observation["status"] == "NOT_YET_DUE"
    assert observation["daily_route"] == "NOT_PROBED"
    assert observation["month_route"] == "NOT_PROBED"
    assert observation["inbox"] == "NOT_PROBED"
    assert observation["boundary_minute_tick_count"] is None
    assert observation["next_run_at"] == iso(NOW + timedelta(minutes=10))


def test_first_run_downloads_counts_and_sets_next_run(tmp_path: Path) -> None:
    config = make_config(tmp_path)
    observation = run_probe(
        config,
        now=NOW,
        listing_fetcher=static_listing_fetcher(month_only_listing()),
        zip_downloader=downloader_for(["2026-11-05 00:00:00.017", "2026-11-05 03:00:00.000"]),
    )
    assert observation["status"] == "DUE"
    assert observation["daily_route"] == "ABSENT"
    assert observation["month_route"] == "PRESENT_CHANGED"
    assert observation["boundary_minute_tick_count"] == 1
    assert observation["error_class"] is None
    assert observation["retry_count"] == 0
    assert observation["next_run_at"] == iso(NOW + timedelta(minutes=30))
    state = load_state(config.watch_dir / "state.json")
    assert state["month_zip_fingerprint"] == "100:M1"
    assert state["last_run_at"] == iso(NOW)
    assert state["status"] == "OK"


def test_unchanged_fingerprint_skips_download(tmp_path: Path) -> None:
    config = make_config(tmp_path)
    seed_state(
        config,
        month_zip_fingerprint="100:M1",
        next_run_at=iso(NOW - timedelta(minutes=1)),
    )
    observation = run_probe(
        config,
        now=NOW,
        listing_fetcher=static_listing_fetcher(month_only_listing()),
        zip_downloader=forbidden_downloader,
    )
    assert observation["month_route"] == "PRESENT_UNCHANGED"
    assert observation["boundary_minute_tick_count"] is None


def test_day_directory_present_reads_as_present(tmp_path: Path) -> None:
    observation = run_probe(
        make_config(tmp_path),
        now=NOW,
        listing_fetcher=static_listing_fetcher(listing_with_day_directory()),
        zip_downloader=downloader_for([]),
    )
    assert observation["daily_route"] == "PRESENT"


def test_one_retry_then_success_is_recorded(tmp_path: Path) -> None:
    attempts: list[str] = []

    def flaky(url: str, timeout_seconds: float) -> list[ArchiveEntry]:
        attempts.append(url)
        if len(attempts) == 1:
            raise ArchiveAcquisitionError("simulated transient")
        return month_only_listing()

    observation = run_probe(
        make_config(tmp_path),
        now=NOW,
        listing_fetcher=flaky,
        zip_downloader=downloader_for([]),
    )
    assert len(attempts) == 2
    assert observation["retry_count"] == 1
    assert observation["error_class"] is None
    assert observation["daily_route"] == "ABSENT"


def test_two_failures_produce_error_observation_without_absence_claim(tmp_path: Path) -> None:
    def dead(url: str, timeout_seconds: float) -> list[ArchiveEntry]:
        raise ArchiveAcquisitionError("persistent")

    observation = run_probe(
        make_config(tmp_path),
        now=NOW,
        listing_fetcher=dead,
        zip_downloader=forbidden_downloader,
    )
    assert observation["error_class"] == "ArchiveAcquisitionError"
    assert observation["daily_route"] == "LISTING_UNREADABLE"
    assert observation["month_route"] == "LISTING_UNREADABLE"
    assert observation["inbox"] == "DIR_MISSING"
    assert observation["boundary_minute_tick_count"] is None


def test_three_consecutive_errors_suspend_and_stop_fetching(tmp_path: Path) -> None:
    config = make_config(tmp_path)

    def dead(url: str, timeout_seconds: float) -> list[ArchiveEntry]:
        raise ArchiveAcquisitionError("persistent")

    for index in range(SUSPEND_AFTER_CONSECUTIVE_ERRORS):
        run_probe(
            config,
            now=NOW + timedelta(minutes=31 * index),
            listing_fetcher=dead,
            zip_downloader=forbidden_downloader,
        )
    state = load_state(config.watch_dir / "state.json")
    assert state["error_streak"] == SUSPEND_AFTER_CONSECUTIVE_ERRORS
    assert state["status"] == "SUSPENDED"

    observation = run_probe(
        config,
        now=NOW + timedelta(hours=4),
        listing_fetcher=forbidden_fetcher,
        zip_downloader=forbidden_downloader,
    )
    assert observation["status"] == "SUSPENDED"


def test_force_does_not_override_suspension(tmp_path: Path) -> None:
    config = make_config(tmp_path, force=True)
    seed_state(config, status="SUSPENDED", error_streak=3)
    observation = run_probe(
        config,
        now=NOW,
        listing_fetcher=forbidden_fetcher,
        zip_downloader=forbidden_downloader,
    )
    assert observation["status"] == "SUSPENDED"


def test_successful_run_clears_the_error_streak(tmp_path: Path) -> None:
    config = make_config(tmp_path)
    seed_state(config, error_streak=2, status="OK")
    run_probe(
        config,
        now=NOW,
        listing_fetcher=static_listing_fetcher(month_only_listing()),
        zip_downloader=downloader_for([]),
    )
    assert load_state(config.watch_dir / "state.json")["error_streak"] == 0


def test_inbox_new_files_flip_and_transition_hints(tmp_path: Path) -> None:
    config = make_config(tmp_path)
    config.inbox_dir.mkdir(parents=True)
    (config.inbox_dir / "VID_3.txt").write_text("x", encoding="utf-8")
    observation = run_probe(
        config,
        now=NOW,
        listing_fetcher=static_listing_fetcher(listing_with_day_directory()),
        zip_downloader=downloader_for([]),
    )
    assert observation["inbox"] == "NEW_FILES"
    assert transition_hints(None, observation) == []
    hints = transition_hints(
        {"daily_route": "ABSENT", "month_route": "PRESENT_UNCHANGED", "inbox": "NO_NEW_FILES"},
        observation,
    )
    assert "MATERIAL_TRANSITION: daily_route ABSENT -> PRESENT" in hints
    assert "MATERIAL_TRANSITION: month_route PRESENT_UNCHANGED -> PRESENT_CHANGED" in hints
    assert "MATERIAL_TRANSITION: inbox NO_NEW_FILES -> NEW_FILES" in hints


def test_every_run_appends_exactly_one_observation_line(tmp_path: Path) -> None:
    config = make_config(tmp_path)
    for index in range(3):
        run_probe(
            config,
            now=NOW + timedelta(minutes=31 * index),
            listing_fetcher=static_listing_fetcher(month_only_listing()),
            zip_downloader=downloader_for([]),
        )
    lines = (config.watch_dir / "observations.ndjson").read_text(encoding="utf-8").splitlines()
    assert len(lines) == 3


def test_status_fields_are_always_in_vocabulary(tmp_path: Path) -> None:
    observation = run_probe(
        make_config(tmp_path),
        now=NOW,
        listing_fetcher=static_listing_fetcher(month_only_listing()),
        zip_downloader=downloader_for([]),
    )
    assert observation["month_route"] in MONTH_ALLOWED
    assert set(observation) >= {
        "at_utc",
        "status",
        "symbol",
        "checkpoint_day",
        "daily_route",
        "month_route",
        "inbox",
        "boundary_minute_tick_count",
        "forced",
        "error_class",
        "elapsed_ms",
        "retry_count",
        "next_run_at",
    }


def test_corrupt_zip_becomes_error_class_without_stopping_inbox_check(tmp_path: Path) -> None:
    config = make_config(tmp_path)
    config.inbox_dir.mkdir(parents=True)
    (config.inbox_dir / "VID_3.txt").write_text("x", encoding="utf-8")

    def broken(url: str, target: Path, timeout_seconds: float) -> Path:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b"not a zip")
        return target

    observation = run_probe(
        config,
        now=NOW,
        listing_fetcher=static_listing_fetcher(month_only_listing()),
        zip_downloader=broken,
    )
    assert observation["error_class"] == "BadZipFile"
    assert observation["boundary_minute_tick_count"] is None
    assert observation["inbox"] == "NEW_FILES"
```

- [ ] **Step 2: Run the tests and verify they fail**

Run: `.venv\Scripts\python.exe -m pytest tests/test_route_probe_run.py -v`
Expected: `ImportError: cannot import name 'run_probe'`.

- [ ] **Step 3: Write the orchestration**

In `scripts/exness_0700_route_probe.py`, add `import time` and `from urllib.error import URLError` plus `from urllib.request import Request, urlopen` to the import block, remove the Task 2 `# noqa` comment, then append:

```python
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
    with urlopen(request, timeout=timeout_seconds) as response:
        with temporary.open("wb") as handle:
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
        if isinstance(before, str) and isinstance(after, str) and before != after:
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
```

Two ordering rules the implementer must honour, both from the contract: the suspended short-circuit is checked **before** `force`, because a suspended observer must not be re-ignited by a routine call — resuming means a human editing `status` in `state.json` (§7.6); and the inbox check runs even after a listing or ZIP failure, because a failed market probe must not blind the source lane (§7.3 keeps them independent facts).

- [ ] **Step 4: Run the tests and verify they pass**

Run: `.venv\Scripts\python.exe -m pytest tests/test_route_probe_run.py -v`
Expected: 13 passed.

Run: `.venv\Scripts\python.exe -m ruff check scripts/exness_0700_route_probe.py tests/test_route_probe_run.py`
Expected: `All checks passed!`

- [ ] **Step 5: Commit**

```bash
git add scripts/exness_0700_route_probe.py tests/test_route_probe_run.py
git commit -m "probe: orchestrate one bounded probe round with retry and suspension"
```

---

### Task 5: CLI, printed contract, and exit codes

**Files:**
- Modify: `scripts/exness_0700_route_probe.py`
- Test: `tests/test_route_probe_run.py`

**Interfaces:**
- Consumes: everything from Tasks 1–4.
- Produces: `DEFAULT_CACHE_DIR: Path`, `ZONE = "Asia/Bangkok"`, `_resolve_checkpoint_day(raw: str | None) -> date`, `build_parser() -> argparse.ArgumentParser`, `main(argv: list[str] | None = None) -> int` returning `0` for a clean observation, `1` for a run that recorded an `error_class`, `2` for a blocked run that produced no observation.

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_route_probe_run.py`:

```python
def test_parser_defaults_match_the_contract(tmp_path: Path) -> None:
    args = build_parser().parse_args(["--once", "--watch-dir", str(tmp_path)])
    assert args.once is True
    assert args.cadence_minutes == 30
    assert args.symbol == "XAUUSDm"
    assert args.force is False
    assert args.checkpoint_day is None
    assert args.timeout_seconds == 30.0


def test_parser_requires_the_once_flag(tmp_path: Path) -> None:
    with pytest.raises(SystemExit):
        build_parser().parse_args(["--watch-dir", str(tmp_path)])


def test_checkpoint_day_is_parsed_as_iso_date() -> None:
    assert _resolve_checkpoint_day("2026-11-05") == date(2026, 11, 5)


def test_checkpoint_day_defaults_to_thailand_today() -> None:
    assert _resolve_checkpoint_day(None) == datetime.now(ZoneInfo("Asia/Bangkok")).date()


def test_main_returns_two_and_writes_nothing_when_state_is_corrupt(tmp_path: Path) -> None:
    (tmp_path / "state.json").write_text("{broken", encoding="utf-8")
    assert main(["--once", "--watch-dir", str(tmp_path)]) == 2
    assert not (tmp_path / "observations.ndjson").exists()


def test_main_returns_two_for_non_positive_cadence(tmp_path: Path) -> None:
    assert main(["--once", "--watch-dir", str(tmp_path), "--cadence-minutes", "0"]) == 2


def test_main_returns_two_for_non_positive_timeout(tmp_path: Path) -> None:
    assert main(["--once", "--watch-dir", str(tmp_path), "--timeout-seconds", "0"]) == 2


@pytest.mark.skipif(
    os.environ.get("NEXUS_PROBE_ALLOW_NETWORK") != "1",
    reason="offline by contract section 8; the single live round runs in Task 6 Step 1",
)
def test_main_live_round_prints_status(tmp_path: Path, capsys) -> None:
    code = main(["--once", "--force", "--watch-dir", str(tmp_path), "--inbox", str(tmp_path)])
    printed = capsys.readouterr().out
    assert code in (0, 1)
    assert "status=" in printed
    assert "next_run_at=" in printed
    assert (tmp_path / "observations.ndjson").exists()
```

Add to the top of `tests/test_route_probe_run.py`: `import os`, `from zoneinfo import ZoneInfo`, and extend the existing `exness_0700_route_probe` import list with `build_parser`, `main`, `_resolve_checkpoint_day`.

- [ ] **Step 2: Run the tests and verify they fail**

Run: `.venv\Scripts\python.exe -m pytest tests/test_route_probe_run.py -v`
Expected: `ImportError: cannot import name 'build_parser'`.

- [ ] **Step 3: Write the CLI**

In `scripts/exness_0700_route_probe.py`, add `import argparse`, `import sys`, `from zoneinfo import ZoneInfo` to the import block, then append:

```python
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
```

`load_state` is read twice on a real run — once in `main` to veto a corrupt state before any network call, once inside `run_probe` as the authoritative read of the transaction. Keep both; the veto must not move inside `run_probe`, because `run_probe` appends an observation line and a corrupt state must produce none.

- [ ] **Step 4: Run the whole offline suite**

Run: `.venv\Scripts\python.exe -m pytest tests/test_route_probe_state.py tests/test_route_probe_listing.py tests/test_route_probe_scan.py tests/test_route_probe_run.py -v`
Expected: all passed, with `test_main_live_round_prints_status` reported as skipped.

Run: `.venv\Scripts\python.exe -m pytest tests -q`
Expected: the pre-existing suite still passes — the probe must add no import-time side effects. If an unrelated pre-existing failure appears, record it verbatim in the commit message rather than "fixing" it inside this lane.

Run: `.venv\Scripts\python.exe -m ruff check scripts/exness_0700_route_probe.py tests/test_route_probe_state.py tests/test_route_probe_listing.py tests/test_route_probe_scan.py tests/test_route_probe_run.py`
Expected: `All checks passed!`

- [ ] **Step 5: Verify no side effects on research authority**

Run: `git status --short`
Expected: only `scripts/exness_0700_route_probe.py`, the four `tests/test_route_probe_*.py` files, and `pyproject.toml`. `docs/CANONICAL_CLAIM_REGISTER_2026-09-03.json`, `docs/CURRENT_RESEARCH_STATE.json`, `docs/0700_WORKSTREAM_STATE.json`, `research_queue/QUEUE.json`, and `research_findings/FINDINGS.json` must not appear.

Run: `.venv\Scripts\python.exe scripts/research_preflight.py 2>&1 | grep NEXUS_RESEARCH_PREFLIGHT`
Expected: `NEXUS_RESEARCH_PREFLIGHT=PASS`.

- [ ] **Step 6: Commit**

```bash
git add scripts/exness_0700_route_probe.py tests/test_route_probe_run.py
git commit -m "probe: add CLI with due gate, transition hints, and exit codes"
```

---

### Task 6: One live round, documentation, tooling registration, and durable job

**Files:**
- Create: `docs/0700_ROUTE_PROBE_LOG.md`
- Modify: `TOOLS.md`
- Modify: `docs/CURRENT_RESEARCH_STATE.json` (one pointer key plus `updated_at`)

**Interfaces:**
- Consumes: the finished CLI from Task 5.
- Produces: the first real observation, the TOOLS.md entry, the supervisor job id, and the resume-visible pointer.

- [ ] **Step 1: Create the watch directory and run one live forced round**

```bash
mkdir -p /d/tools/nexus-0700-watch
.venv\Scripts\python.exe scripts/exness_0700_route_probe.py --once --force \
  --checkpoint-day 2026-11-05 --watch-dir "D:/tools/nexus-0700-watch"
```

Expected: exit 0 or 1, one `status=DUE ...` line printed, and `D:/tools/nexus-0700-watch/observations.ndjson` holding exactly one line. Record the printed values verbatim in the log document — they are Source Facts about the provider layout at that timestamp, not conclusions, and they are the first independent re-observation of the 2026-11-05 recheck finding.

- [ ] **Step 2: Verify the due gate blocks a second immediate call**

```bash
.venv\Scripts\python.exe scripts/exness_0700_route_probe.py --once \
  --watch-dir "D:/tools/nexus-0700-watch"
```

Expected: `status=NOT_YET_DUE` with `daily_route`, `month_route`, and `inbox` all `NOT_PROBED`, and no new bytes in the ZIP cache. This is contract acceptance criterion 2; if a request reached the network, the gate is broken — stop and fix before continuing.

- [ ] **Step 3: Create `docs/0700_ROUTE_PROBE_LOG.md`**

Required sections, in this order:

1. `Purpose` — one line plus the contract link plus the sentence "existence evidence only; never route authority".
2. `Vocabulary` — copy the contract §6 table verbatim.
3. `Rounds` — one block per promoted transition with `at_utc`, the three statuses, `boundary_minute_tick_count`, `error_class`, and the exact command line used. The Step 1 live round is the first block.
4. `Standing notes` — restate contract §11 (no OS scheduler means freshness on demand, not unattended polling) and the rule that a non-zero tick count does not mean the checkpoint is satisfied.
5. `How to promote` — the two-line procedure: run the probe, then copy the printed `MATERIAL_TRANSITION` line into `Rounds`.

- [ ] **Step 4: Register the tool in `TOOLS.md`**

Add a `### 07:00 Route Probe` entry under `## Registered tools` containing: canonical role (decision-neutral availability observer, not a calculator), the invocation command, the three paths (watch dir, inbox, cache), exit codes 0/1/2, a pointer to the contract's closed vocabulary, the hard boundary sentence "no State Packet, no M1 rebuild, no archive validation, no scoring, no order send, no credentials", and the contract document path. The reuse-before-build rule at the top of `TOOLS.md` makes this entry the thing that stops a later session from writing a second poller.

- [ ] **Step 5: Register the durable job**

```bash
py -3 D:/tools/nexus-durable-work/supervisor.py register \
  --job-id XAU-0700-ROUTE-PROBE-20261105 \
  --title "07:00 route availability observer" \
  --purpose DECISION_NEUTRAL_PROBE \
  --status WAITING \
  --repo D:/nexus-xau-engine-repo \
  --next-action "run scripts/exness_0700_route_probe.py --once when now >= next_run_at" \
  --checkpoint "docs/0700_ROUTE_PROBE_AUTOMATION_CONTRACT_V0_1_2026-11-05.md"
```

Then verify the lane is visible cold:

```bash
py -3 D:/tools/nexus-project-continuity/continuity.py resume --project xau
```

Expected: the capsule reports the probe job in live durable state, not only the repository pointer. If it reports `STALE_PROJECT_POINTER`, reconcile the live job before anything else, per AGENTS.md Tier 0.

- [ ] **Step 6: Add the resume pointer and validate**

In `docs/CURRENT_RESEARCH_STATE.json`, add one top-level key `route_probe_observer_2026_11_05` with `status: "IMPLEMENTED_OFFLINE_TESTED_FIRST_LIVE_ROUND_RECORDED"`, `contract`, `plan`, `tool`, `watch_dir`, `durable_job: "XAU-0700-ROUTE-PROBE-20261105"`, `observation_log`, and a `prohibited` sentence repeating contract §3. Set `updated_at` to the actual local timestamp at commit time — never a guessed future time. Edit no other key.

```bash
.venv\Scripts\python.exe -m pytest tests -q
.venv\Scripts\python.exe scripts/research_preflight.py 2>&1 | grep NEXUS_RESEARCH_PREFLIGHT
git diff --check
git status --short
```

Expected: suite green, `PASS`, clean whitespace, and no `data/`, `*.ndjson`, `*.zip`, or media path staged.

- [ ] **Step 7: Commit and push**

```bash
git add docs/0700_ROUTE_PROBE_LOG.md TOOLS.md docs/CURRENT_RESEARCH_STATE.json \
  docs/0700_ROUTE_PROBE_AUTOMATION_CONTRACT_V0_1_2026-11-05.md \
  docs/0700_ROUTE_PROBE_AUTOMATION_IMPLEMENTATION_PLAN_2026-11-05.md
git commit -m "probe: register route observer tooling and durable job"
git push origin main
```

---

## Self-Review Record

Contract coverage (requirement → task):

- §2 three observations → Tasks 2, 3, 4. §3 non-scope → Global Constraints, Task 3's `_read_month_window` rationale, Task 5 Step 5, Task 6 Step 4.
- §4 cadence owned by the state file, `--once` / `--force` semantics → Task 1 `compute_due`, Task 4 short-circuits, Task 5 flags.
- §5 components and reuse list → File Structure; log document, `TOOLS.md`, registration in Task 6.
- §6 closed vocabulary and the `NOT_PROBED` rule → Task 1 constants, Task 2 `validate_status`, Task 4 `validate_status` on every status assignment, Task 6 Step 2.
- §7 rails: read-only network (Task 4 `download_zip` using the shared `USER_AGENT`, nothing logged from headers), bounded traffic (Task 2's single-listing design, Task 4's fingerprint skip and `_fetch_with_retry` one retry), fail-closed (Task 4 error path yields `LISTING_UNREADABLE`, never `ABSENT`), no secrets/media in git (Task 5 Step 5, Task 6 Step 6), atomic writes (Task 1 `save_state`, Task 4 `download_zip` through `.part`), self-limiting (Task 4 `next_error_streak` plus the suspended-before-`force` ordering).
- §8 tests → Tasks 1–5, all offline; the live round exists only in Task 6 Step 1.
- §9 registration after the script exists → Task 6 Step 5.
- §10 acceptance criteria → Task 6 Steps 1–7.
- §11 limitation → restated in the log document (Task 6 Step 3) so it travels with the tool.

Placeholder scan: no TBD/TODO remains; every code step carries its code; every command carries an expected result.

Type consistency across tasks: `ProbeConfig` fields match the Task 5 construction; `run_probe(config, *, now, listing_fetcher, zip_downloader)` is the single call shape used by Tasks 4, 5, and 6; `count_boundary_ticks(zip_path, day, symbol)` keeps the symbol parameter introduced in Task 3; `scan_inbox` returns the three-tuple consumed in Task 4; `iso_utc` (Task 1) is the only formatter in production code, with the test-local `iso` mirroring it for expectations.
