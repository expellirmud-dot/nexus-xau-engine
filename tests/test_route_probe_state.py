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
