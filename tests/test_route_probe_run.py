from __future__ import annotations

import csv
import json
import os
import zipfile
from datetime import UTC, date, datetime, timedelta
from io import StringIO
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

import exness_0700_route_probe as probe
from exness_0700_route_probe import (
    MONTH_ALLOWED,
    NOT_PROBED,
    SUSPEND_AFTER_CONSECUTIVE_ERRORS,
    ProbeConfig,
    _resolve_checkpoint_day,
    build_parser,
    load_state,
    main,
    prior_baseline,
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
def test_main_live_round_prints_status(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    code = main(["--once", "--force", "--watch-dir", str(tmp_path), "--inbox", str(tmp_path)])
    printed = capsys.readouterr().out
    assert code in (0, 1)
    assert "status=" in printed
    assert "next_run_at=" in printed
    assert (tmp_path / "observations.ndjson").exists()


def test_not_probed_is_never_a_material_transition(tmp_path: Path) -> None:
    """A skipped round says nothing about the world, so it cannot be a flip.

    The first live round exposed this: a NOT_YET_DUE run printed
    `daily_route PRESENT -> NOT_PROBED`, which reads like the route disappeared.
    """
    probed = {"daily_route": "PRESENT", "month_route": "PRESENT_CHANGED", "inbox": "NO_NEW_FILES"}
    skipped = {
        "daily_route": NOT_PROBED,
        "month_route": NOT_PROBED,
        "inbox": NOT_PROBED,
    }
    assert transition_hints(probed, skipped) == []
    assert transition_hints(skipped, probed) == []
    # A real flip still reports, even when the neighbour field stayed unprobed.
    after = dict(skipped, daily_route="ABSENT")
    assert transition_hints(probed, after) == ["MATERIAL_TRANSITION: daily_route PRESENT -> ABSENT"]


def test_gate_blocked_round_does_not_blind_the_next_round(tmp_path: Path) -> None:
    """A round that never probed must not become the comparison baseline.

    The second live round exposed this: the 12:32Z NOT_YET_DUE line was the last
    NDJSON record, so the first scheduled round compared against NOT_PROBED and
    printed no hint even though month_route really had moved
    PRESENT_CHANGED -> PRESENT_UNCHANGED. A peek that got gated silently blinded
    the observer for the next round.
    """
    probed = {
        "checkpoint_day": "2026-11-05",
        "daily_route": "PRESENT",
        "month_route": "PRESENT_CHANGED",
        "inbox": "NEW_FILES",
    }
    blocked = {
        "checkpoint_day": "2026-11-05",
        "daily_route": NOT_PROBED,
        "month_route": NOT_PROBED,
        "inbox": NOT_PROBED,
    }
    current = {
        "checkpoint_day": "2026-11-05",
        "daily_route": "PRESENT",
        "month_route": "PRESENT_UNCHANGED",
        "inbox": "NEW_FILES",
    }

    hints = transition_hints(prior_baseline([probed, blocked], "2026-11-05"), current)
    assert hints == ["MATERIAL_TRANSITION: month_route PRESENT_CHANGED -> PRESENT_UNCHANGED"]


def test_baseline_takes_the_newest_probed_value_for_each_field_separately() -> None:
    """Fields rotate independently, so the baseline is per field, not per row."""
    first = {
        "checkpoint_day": "2026-11-05",
        "daily_route": "PRESENT",
        "month_route": "PRESENT_CHANGED",
        "inbox": "NO_NEW_FILES",
    }
    second = {
        "checkpoint_day": "2026-11-05",
        "daily_route": NOT_PROBED,
        "month_route": "ABSENT",
        "inbox": NOT_PROBED,
    }

    assert prior_baseline([first, second], "2026-11-05") == {
        "daily_route": "PRESENT",
        "month_route": "ABSENT",
        "inbox": "NO_NEW_FILES",
    }


def test_baseline_never_crosses_a_checkpoint_day_rollover() -> None:
    """Day 05 PRESENT against day 06 ABSENT is a different question, not a flip.

    The checkpoint day is the Bangkok calendar date, so it changes every day at
    07:00 and the new day's directory legitimately does not exist yet for a
    while. Comparing across that boundary would make the observer report a route
    disappearance each morning and have the automation commit it.
    """
    yesterday = {
        "checkpoint_day": "2026-11-05",
        "daily_route": "PRESENT",
        "month_route": "PRESENT_UNCHANGED",
        "inbox": "NO_NEW_FILES",
    }
    current = {
        "checkpoint_day": "2026-11-06",
        "daily_route": "ABSENT",
        "month_route": "PRESENT_UNCHANGED",
        "inbox": "NO_NEW_FILES",
    }

    assert prior_baseline([yesterday], "2026-11-06") is None
    assert transition_hints(prior_baseline([yesterday], "2026-11-06"), current) == []
    # Same day still compares normally.
    assert prior_baseline([yesterday], "2026-11-05") == {
        "daily_route": "PRESENT",
        "month_route": "PRESENT_UNCHANGED",
        "inbox": "NO_NEW_FILES",
    }


def test_baseline_is_none_when_no_prior_round_ever_probed() -> None:
    """Only gate-blocked history means there is nothing to compare against yet."""
    blocked = {
        "checkpoint_day": "2026-11-05",
        "daily_route": NOT_PROBED,
        "month_route": NOT_PROBED,
        "inbox": NOT_PROBED,
    }
    current = {"daily_route": "PRESENT", "month_route": "PRESENT_CHANGED", "inbox": "NEW_FILES"}

    assert prior_baseline([blocked], "2026-11-05") is None
    assert prior_baseline([], "2026-11-05") is None
    assert transition_hints(prior_baseline([blocked], "2026-11-05"), current) == []


def test_main_promotes_a_flip_that_follows_a_gate_blocked_round(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The wiring, not just the helper: main must compare against prior_baseline.

    Reverting main to `prior[-1]` makes this fail, because the last NDJSON line
    is the gate-blocked round and its NOT_PROBED values swallow the daily flip.
    """
    day = _resolve_checkpoint_day(None).isoformat()
    seeded = [
        {"checkpoint_day": day, "daily_route": "PRESENT", "month_route": "PRESENT_CHANGED",
         "inbox": "NO_NEW_FILES"},
        {"checkpoint_day": day, "daily_route": NOT_PROBED, "month_route": NOT_PROBED,
         "inbox": NOT_PROBED},
    ]
    lines = "\n".join(json.dumps(record) for record in seeded)
    (tmp_path / "observations.ndjson").write_text(lines + "\n", encoding="utf-8")
    monkeypatch.setattr(probe, "fetch_listing", static_listing_fetcher(month_only_listing()))
    monkeypatch.setattr(probe, "download_zip", downloader_for([]))

    code = main(["--once", "--force", "--watch-dir", str(tmp_path), "--inbox", str(tmp_path)])
    printed = capsys.readouterr().out

    assert code == 0
    assert "MATERIAL_TRANSITION: daily_route PRESENT -> ABSENT" in printed
