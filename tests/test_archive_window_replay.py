import hashlib
import json
import zipfile
from pathlib import Path

import pandas as pd
import pytest

from nexus_xau.data.exness_tick_archive_download import VALIDATOR_VERSION
from nexus_xau.replay.archive_window import (
    CONTINUITY_STATUS,
    DATA_EXCLUDED_ARCHIVE_LOCAL_FILE_INVALID,
    DATA_EXCLUDED_ARCHIVE_MONTH_NOT_VALIDATED,
    WINDOW_STATUS_NO_TICKS,
    WINDOW_STATUS_OK,
    ArchiveWindowError,
    load_archive_tick_window,
)
from nexus_xau.replay.tick_reference import (
    DATA_EXCLUDED_ARCHIVE_GAP,
    DATA_EXCLUDED_INCOMPLETE_HORIZON,
    DATA_EXCLUDED_INSUFFICIENT_WARMUP,
)

HEADER = "Exness,Symbol,Timestamp,Bid,Ask\n"


def _write_month(
    root: Path,
    *,
    year: int,
    month: int,
    rows: list[tuple[str, float, float]],
    symbol: str = "XAUUSDm",
    header: str = HEADER,
) -> tuple[Path, dict[str, object]]:
    rel = Path("data") / f"{year}-{month:02d}.zip"
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    member = f"Exness_{symbol}_{year}_{month:02d}.csv"
    payload = header + "".join(
        f"exness,{symbol},{timestamp},{bid},{ask}\n" for timestamp, bid, ask in rows
    )
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(member, payload)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    record = {
        "symbol": symbol,
        "year": year,
        "month": month,
        "local_path": str(rel),
        "actual_size": path.stat().st_size,
        "sha256": digest,
        "status": "VALIDATED",
        "validator_version": VALIDATOR_VERSION,
    }
    return path, record


def _write_manifest(path: Path, records: list[dict[str, object]]) -> None:
    path.write_text(
        "".join(json.dumps(record) + "\n" for record in records),
        encoding="utf-8",
    )


def _write_gap_ledger(
    path: Path,
    *,
    earliest: str = "2026-01-01T00:00:00Z",
    latest: str = "2026-03-01T00:00:00Z",
    gap: tuple[str, str] | None = None,
) -> None:
    candidates = []
    if gap is not None:
        candidates.append(
            {
                "gap_id": "gap-1",
                "status": "UNRESOLVED_BOUNDARY_GAP_CANDIDATE",
                "last_observed_before_gap": gap[0],
                "first_observed_after_gap": gap[1],
            }
        )
    path.write_text(
        json.dumps(
            {
                "coverage_boundaries": {
                    "earliest_observed_tick_utc": earliest,
                    "latest_observed_tick_utc": latest,
                },
                "continuity_claim": CONTINUITY_STATUS,
                "boundary_gap_candidates": candidates,
            }
        ),
        encoding="utf-8",
    )


def _load(
    root: Path,
    manifest: Path,
    ledger: Path,
    start: str,
    end: str,
):
    return load_archive_tick_window(
        repo_root=root,
        manifest_path=manifest,
        gap_ledger_path=ledger,
        symbol="XAUUSDm",
        start=start,
        end=end,
    )


def test_half_open_window_includes_start_and_excludes_end(tmp_path: Path) -> None:
    _, record = _write_month(
        tmp_path,
        year=2026,
        month=1,
        rows=[
            ("2026-01-01T00:00:00Z", 100.0, 100.2),
            ("2026-01-01T00:00:01Z", 100.1, 100.3),
            ("2026-01-01T00:00:02Z", 100.2, 100.4),
        ],
    )
    manifest = tmp_path / "manifest.jsonl"
    ledger = tmp_path / "gaps.json"
    _write_manifest(manifest, [record])
    _write_gap_ledger(ledger)

    result = _load(
        tmp_path,
        manifest,
        ledger,
        "2026-01-01T00:00:00Z",
        "2026-01-01T00:00:02Z",
    )
    assert result.status == WINDOW_STATUS_OK
    assert list(result.frame.index) == [
        pd.Timestamp("2026-01-01T00:00:00Z"),
        pd.Timestamp("2026-01-01T00:00:01Z"),
    ]


def test_multi_month_window_selects_each_intersecting_month(tmp_path: Path) -> None:
    _, jan = _write_month(
        tmp_path,
        year=2026,
        month=1,
        rows=[("2026-01-31T23:59:59Z", 100.0, 100.2)],
    )
    _, feb = _write_month(
        tmp_path,
        year=2026,
        month=2,
        rows=[("2026-02-01T00:00:00Z", 100.1, 100.3)],
    )
    manifest = tmp_path / "manifest.jsonl"
    ledger = tmp_path / "gaps.json"
    _write_manifest(manifest, [jan, feb])
    _write_gap_ledger(ledger)

    result = _load(
        tmp_path,
        manifest,
        ledger,
        "2026-01-31T23:59:59Z",
        "2026-02-01T00:00:01Z",
    )
    assert [(m.year, m.month) for m in result.source_months] == [(2026, 1), (2026, 2)]
    assert len(result.frame) == 2


@pytest.mark.parametrize("current", [False, True])
def test_missing_or_noncurrent_manifest_month_is_excluded(
    tmp_path: Path, current: bool
) -> None:
    _, record = _write_month(
        tmp_path,
        year=2026,
        month=1,
        rows=[("2026-01-01T00:00:00Z", 100.0, 100.2)],
    )
    if current:
        record["validator_version"] = "OLD_VALIDATOR"
        records = [record]
    else:
        records = []
    manifest = tmp_path / "manifest.jsonl"
    ledger = tmp_path / "gaps.json"
    _write_manifest(manifest, records)
    _write_gap_ledger(ledger)

    with pytest.raises(ArchiveWindowError) as exc:
        _load(
            tmp_path,
            manifest,
            ledger,
            "2026-01-01T00:00:00Z",
            "2026-01-01T00:00:01Z",
        )
    assert exc.value.code == DATA_EXCLUDED_ARCHIVE_MONTH_NOT_VALIDATED


def test_raw_ordinal_preserves_position_before_requested_start(tmp_path: Path) -> None:
    _, record = _write_month(
        tmp_path,
        year=2026,
        month=1,
        rows=[
            ("2026-01-01T00:00:00Z", 100.0, 100.2),
            ("2026-01-01T00:00:01Z", 100.1, 100.3),
        ],
    )
    manifest = tmp_path / "manifest.jsonl"
    ledger = tmp_path / "gaps.json"
    _write_manifest(manifest, [record])
    _write_gap_ledger(ledger)

    result = _load(
        tmp_path,
        manifest,
        ledger,
        "2026-01-01T00:00:01Z",
        "2026-01-01T00:00:02Z",
    )
    assert result.frame.iloc[0]["raw_ordinal"] == 1


def test_duplicate_and_equal_timestamp_rows_are_preserved(tmp_path: Path) -> None:
    _, record = _write_month(
        tmp_path,
        year=2026,
        month=1,
        rows=[
            ("2026-01-01T00:00:00Z", 100.0, 100.2),
            ("2026-01-01T00:00:00Z", 100.0, 100.2),
            ("2026-01-01T00:00:00Z", 100.1, 100.3),
        ],
    )
    manifest = tmp_path / "manifest.jsonl"
    ledger = tmp_path / "gaps.json"
    _write_manifest(manifest, [record])
    _write_gap_ledger(ledger)

    result = _load(
        tmp_path,
        manifest,
        ledger,
        "2026-01-01T00:00:00Z",
        "2026-01-01T00:00:01Z",
    )
    assert len(result.frame) == 3
    assert list(result.frame["raw_ordinal"]) == [0, 1, 2]
    assert result.frame.index.has_duplicates


def test_known_open_gap_intersection_is_excluded_but_endpoints_are_eligible(
    tmp_path: Path,
) -> None:
    _, record = _write_month(
        tmp_path,
        year=2026,
        month=1,
        rows=[
            ("2026-01-01T00:00:00Z", 100.0, 100.2),
            ("2026-01-01T00:00:10Z", 100.1, 100.3),
        ],
    )
    manifest = tmp_path / "manifest.jsonl"
    ledger = tmp_path / "gaps.json"
    _write_manifest(manifest, [record])
    _write_gap_ledger(
        ledger,
        gap=("2026-01-01T00:00:04Z", "2026-01-01T00:00:06Z"),
    )

    with pytest.raises(ArchiveWindowError) as exc:
        _load(
            tmp_path,
            manifest,
            ledger,
            "2026-01-01T00:00:03Z",
            "2026-01-01T00:00:05Z",
        )
    assert exc.value.code == DATA_EXCLUDED_ARCHIVE_GAP

    left = _load(
        tmp_path,
        manifest,
        ledger,
        "2026-01-01T00:00:00Z",
        "2026-01-01T00:00:04Z",
    )
    assert left.status == WINDOW_STATUS_OK

    right = _load(
        tmp_path,
        manifest,
        ledger,
        "2026-01-01T00:00:06Z",
        "2026-01-01T00:00:11Z",
    )
    assert right.status == WINDOW_STATUS_OK


def test_coverage_boundaries_fail_closed(tmp_path: Path) -> None:
    _, record = _write_month(
        tmp_path,
        year=2026,
        month=1,
        rows=[("2026-01-01T00:00:00Z", 100.0, 100.2)],
    )
    manifest = tmp_path / "manifest.jsonl"
    ledger = tmp_path / "gaps.json"
    _write_manifest(manifest, [record])
    _write_gap_ledger(
        ledger,
        earliest="2026-01-01T00:00:00Z",
        latest="2026-01-31T23:59:59Z",
    )

    with pytest.raises(ArchiveWindowError) as early:
        _load(
            tmp_path,
            manifest,
            ledger,
            "2025-12-31T23:59:59Z",
            "2026-01-01T00:00:00Z",
        )
    assert early.value.code == DATA_EXCLUDED_INSUFFICIENT_WARMUP

    with pytest.raises(ArchiveWindowError) as late:
        _load(
            tmp_path,
            manifest,
            ledger,
            "2026-01-31T23:59:58Z",
            "2026-02-01T00:00:00Z",
        )
    assert late.value.code == DATA_EXCLUDED_INCOMPLETE_HORIZON


def test_empty_structurally_eligible_window_is_explicit(tmp_path: Path) -> None:
    _, record = _write_month(
        tmp_path,
        year=2026,
        month=1,
        rows=[("2026-01-01T00:00:00Z", 100.0, 100.2)],
    )
    manifest = tmp_path / "manifest.jsonl"
    ledger = tmp_path / "gaps.json"
    _write_manifest(manifest, [record])
    _write_gap_ledger(ledger)

    result = _load(
        tmp_path,
        manifest,
        ledger,
        "2026-01-01T00:01:00Z",
        "2026-01-01T00:02:00Z",
    )
    assert result.status == WINDOW_STATUS_NO_TICKS
    assert result.frame.empty
    assert result.continuity_status == CONTINUITY_STATUS


def test_manifest_sha_and_month_provenance_survive_output(tmp_path: Path) -> None:
    _, record = _write_month(
        tmp_path,
        year=2026,
        month=1,
        rows=[("2026-01-01T00:00:00Z", 100.0, 100.2)],
    )
    manifest = tmp_path / "manifest.jsonl"
    ledger = tmp_path / "gaps.json"
    _write_manifest(manifest, [record])
    _write_gap_ledger(ledger)

    result = _load(
        tmp_path,
        manifest,
        ledger,
        "2026-01-01T00:00:00Z",
        "2026-01-01T00:00:01Z",
    )
    assert result.frame.iloc[0]["source_sha256"] == record["sha256"]
    assert result.frame.iloc[0]["source_year"] == 2026
    assert result.frame.iloc[0]["source_month"] == 1
    assert result.source_months[0].sha256 == record["sha256"]


def test_local_size_mismatch_is_excluded(tmp_path: Path) -> None:
    path, record = _write_month(
        tmp_path,
        year=2026,
        month=1,
        rows=[("2026-01-01T00:00:00Z", 100.0, 100.2)],
    )
    record["actual_size"] = path.stat().st_size + 1
    manifest = tmp_path / "manifest.jsonl"
    ledger = tmp_path / "gaps.json"
    _write_manifest(manifest, [record])
    _write_gap_ledger(ledger)

    with pytest.raises(ArchiveWindowError) as exc:
        _load(
            tmp_path,
            manifest,
            ledger,
            "2026-01-01T00:00:00Z",
            "2026-01-01T00:00:01Z",
        )
    assert exc.value.code == DATA_EXCLUDED_ARCHIVE_LOCAL_FILE_INVALID
