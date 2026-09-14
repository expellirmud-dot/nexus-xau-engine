from pathlib import Path

from nexus_xau.data.exness_tick_archive import (
    ArchiveAcquisitionError,
    ArchiveEntry,
    ArchiveMonthRecord,
    append_record,
    expected_month_filename,
    load_existing_records,
    parse_directory_payload,
    scan_exness_archive_coverage,
)


def test_parse_directory_payload_and_expected_filename() -> None:
    entries = parse_directory_payload(
        '[{"name":"01","type":"directory","mtime":"x"},'
        '{"name":"file.zip","type":"file","size":123}]'
    )

    assert entries == [
        ArchiveEntry(name="01", type="directory", mtime="x", size=None),
        ArchiveEntry(name="file.zip", type="file", mtime=None, size=123),
    ]
    assert expected_month_filename("XAUUSDm", 2022, 9) == (
        "Exness_XAUUSDm_2022_09.zip"
    )


def test_scan_maps_available_and_missing_months(tmp_path: Path) -> None:
    output = tmp_path / "coverage.jsonl"
    base = "https://example.invalid/ticks/"

    def loader(url: str) -> list[ArchiveEntry]:
        if url == f"{base}XAUUSDm/":
            return [ArchiveEntry("2022", "directory")]
        if url == f"{base}XAUUSDm/2022/":
            return [
                ArchiveEntry("09", "directory"),
                ArchiveEntry("10", "directory"),
            ]
        if url == f"{base}XAUUSDm/2022/09/":
            return [
                ArchiveEntry(
                    "Exness_XAUUSDm_2022_09.zip",
                    "file",
                    "mtime",
                    22115588,
                )
            ]
        if url == f"{base}XAUUSDm/2022/10/":
            return [ArchiveEntry("unexpected.zip", "file", "mtime", 100)]
        raise AssertionError(url)

    result = scan_exness_archive_coverage(
        symbol="XAUUSDm",
        start_year=2022,
        end_year=2022,
        months=[8, 9, 10],
        output_jsonl=output,
        base_url=base,
        directory_loader=loader,
    )

    assert result["summary"]["status_counts"] == {
        "AVAILABLE": 1,
        "EXPECTED_FILE_MISSING": 1,
        "MONTH_DIRECTORY_MISSING": 1,
    }
    records = load_existing_records(output)
    assert len(records) == 3
    september = next(record for record in records if record.month == 9)
    assert september.file_size == 22115588


def test_scan_resume_skips_terminal_record_and_retries_error(tmp_path: Path) -> None:
    output = tmp_path / "coverage.jsonl"
    base = "https://example.invalid/ticks/"
    append_record(
        output,
        ArchiveMonthRecord(
            symbol="XAUUSDm",
            year=2022,
            month=9,
            directory_url=f"{base}XAUUSDm/2022/09/",
            expected_filename="Exness_XAUUSDm_2022_09.zip",
            status="AVAILABLE",
            file_name="Exness_XAUUSDm_2022_09.zip",
            file_size=1,
            file_mtime="old",
            observed_at_utc="2026-09-14T00:00:00+00:00",
            evidence_basis="TEST",
        ),
    )
    append_record(
        output,
        ArchiveMonthRecord(
            symbol="XAUUSDm",
            year=2022,
            month=10,
            directory_url=f"{base}XAUUSDm/2022/10/",
            expected_filename="Exness_XAUUSDm_2022_10.zip",
            status="ERROR",
            file_name=None,
            file_size=None,
            file_mtime=None,
            observed_at_utc="2026-09-14T00:00:00+00:00",
            evidence_basis="TEST",
            error_message="transient",
        ),
    )

    calls: list[str] = []

    def loader(url: str) -> list[ArchiveEntry]:
        calls.append(url)
        if url == f"{base}XAUUSDm/":
            return [ArchiveEntry("2022", "directory")]
        if url == f"{base}XAUUSDm/2022/":
            return [
                ArchiveEntry("09", "directory"),
                ArchiveEntry("10", "directory"),
            ]
        if url == f"{base}XAUUSDm/2022/10/":
            return [
                ArchiveEntry(
                    "Exness_XAUUSDm_2022_10.zip",
                    "file",
                    "new",
                    2,
                )
            ]
        raise AssertionError(url)

    result = scan_exness_archive_coverage(
        symbol="XAUUSDm",
        start_year=2022,
        end_year=2022,
        months=[9, 10],
        output_jsonl=output,
        base_url=base,
        directory_loader=loader,
    )

    assert f"{base}XAUUSDm/2022/09/" not in calls
    assert result["summary"]["status_counts"] == {"AVAILABLE": 2}
    records = load_existing_records(output)
    assert len(records) == 3
    assert records[-1].month == 10
    assert records[-1].status == "AVAILABLE"


def test_symbol_listing_error_is_persisted_and_retryable(tmp_path: Path) -> None:
    output = tmp_path / "coverage.jsonl"

    def loader(_url: str) -> list[ArchiveEntry]:
        raise ArchiveAcquisitionError("TimeoutError: network")

    result = scan_exness_archive_coverage(
        symbol="XAUUSDm",
        start_year=2022,
        end_year=2022,
        months=[9],
        output_jsonl=output,
        directory_loader=loader,
    )

    assert result["summary"]["status_counts"] == {"ERROR": 1}
    record = load_existing_records(output)[0]
    assert record.evidence_basis == "SYMBOL_DIRECTORY_LISTING_ERROR"
    assert "TimeoutError" in (record.error_message or "")
