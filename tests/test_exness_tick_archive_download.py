from __future__ import annotations

import csv
import io
import zipfile
from pathlib import Path

from nexus_xau.data.exness_tick_archive_download import (
    DownloadValidationRecord,
    append_manifest,
    download_and_validate_month,
    load_manifest,
    month_url,
    validate_zip,
)


def _write_zip(path: Path) -> None:
    rows = [
        ["Exness", "Symbol", "Timestamp", "Bid", "Ask"],
        ["Exness", "XAUUSDm", "2026-08-01T00:00:00.100Z", "100.0", "100.2"],
        ["Exness", "XAUUSDm", "2026-08-01T00:00:00.200Z", "100.1", "100.3"],
    ]
    buf = io.StringIO(newline="")
    writer = csv.writer(buf)
    writer.writerows(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("Exness_XAUUSDm_2026_08.csv", buf.getvalue())


def test_month_url() -> None:
    assert month_url("XAUUSDm", 2026, 8) == (
        "https://ticks.ex2archive.com/ticks/XAUUSDm/2026/08/"
        "Exness_XAUUSDm_2026_08.zip"
    )


def test_validate_zip_streams_and_checks_rows(tmp_path: Path) -> None:
    path = tmp_path / "sample.zip"
    _write_zip(path)
    result = validate_zip(path, symbol="XAUUSDm")
    assert result["zip_integrity"] == "PASS"
    assert result["row_count"] == 2
    assert result["provider_mismatch"] == 0
    assert result["symbol_mismatch"] == 0
    assert result["ask_lt_bid"] == 0
    assert result["timestamp_regression"] == 0


def test_validated_manifest_is_reused_without_network(tmp_path: Path) -> None:
    output_root = tmp_path / "archive"
    target = output_root / "XAUUSDm" / "2026" / "Exness_XAUUSDm_2026_08.zip"
    _write_zip(target)
    validation = validate_zip(target, symbol="XAUUSDm")
    record = DownloadValidationRecord(
        symbol="XAUUSDm",
        year=2026,
        month=8,
        url=month_url("XAUUSDm", 2026, 8),
        local_path=str(target),
        expected_size=target.stat().st_size,
        actual_size=target.stat().st_size,
        sha256="known",
        status="VALIDATED",
        validated_at_utc="2026-09-14T00:00:00+00:00",
        **validation,
    )
    manifest = tmp_path / "manifest.jsonl"
    append_manifest(manifest, record)

    reused = download_and_validate_month(
        symbol="XAUUSDm",
        year=2026,
        month=8,
        output_root=output_root,
        manifest_path=manifest,
        expected_size=target.stat().st_size,
        base_url="https://example.invalid/ticks/",
    )
    assert reused.sha256 == "known"
    assert len(load_manifest(manifest)) == 1
    assert len(manifest.read_text(encoding="utf-8").splitlines()) == 1
