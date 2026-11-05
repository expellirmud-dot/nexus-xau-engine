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
