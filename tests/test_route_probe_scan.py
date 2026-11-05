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
