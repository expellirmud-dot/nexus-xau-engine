from __future__ import annotations

import csv
import io
import json
import math
import zipfile
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from nexus_xau.data.exness_tick_archive_download import (
    VALIDATOR_VERSION,
    load_manifest,
)
from nexus_xau.replay.tick_reference import (
    DATA_EXCLUDED_ARCHIVE_GAP,
    DATA_EXCLUDED_INCOMPLETE_HORIZON,
    DATA_EXCLUDED_INSUFFICIENT_WARMUP,
    validate_tick_frame,
)

CONTINUITY_STATUS = "KNOWN_GAPS_ENFORCED_FULL_CONTINUITY_NOT_PROVEN"
WINDOW_STATUS_OK = "OK"
WINDOW_STATUS_NO_TICKS = "NO_TICKS_OBSERVED_IN_WINDOW"

DATA_EXCLUDED_ARCHIVE_MONTH_NOT_VALIDATED = "DATA_EXCLUDED_ARCHIVE_MONTH_NOT_VALIDATED"
DATA_EXCLUDED_ARCHIVE_LOCAL_FILE_INVALID = "DATA_EXCLUDED_ARCHIVE_LOCAL_FILE_INVALID"
DATA_EXCLUDED_ARCHIVE_CSV_INVALID = "DATA_EXCLUDED_ARCHIVE_CSV_INVALID"


class ArchiveWindowError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code


@dataclass(frozen=True, slots=True)
class BoundaryGapCandidate:
    gap_id: str
    last_observed_before_gap: pd.Timestamp
    first_observed_after_gap: pd.Timestamp
    status: str


@dataclass(frozen=True, slots=True)
class GapLedger:
    earliest_observed_tick: pd.Timestamp
    latest_observed_tick: pd.Timestamp
    gaps: tuple[BoundaryGapCandidate, ...]
    continuity_status: str


@dataclass(frozen=True, slots=True)
class ArchiveMonthProvenance:
    symbol: str
    year: int
    month: int
    local_path: str
    sha256: str
    actual_size: int
    validator_version: str


@dataclass(frozen=True, slots=True)
class ArchiveWindowResult:
    symbol: str
    requested_start: pd.Timestamp
    requested_end: pd.Timestamp
    frame: pd.DataFrame
    source_months: tuple[ArchiveMonthProvenance, ...]
    status: str
    continuity_status: str


def _utc(value: pd.Timestamp | str) -> pd.Timestamp:
    timestamp = pd.Timestamp(value)
    if timestamp.tz is None:
        raise ValueError("Timestamp must be timezone-aware")
    return timestamp.tz_convert("UTC")


def load_gap_ledger(path: Path) -> GapLedger:
    payload = json.loads(path.read_text(encoding="utf-8"))
    bounds = payload["coverage_boundaries"]
    gaps = tuple(
        BoundaryGapCandidate(
            gap_id=str(item["gap_id"]),
            last_observed_before_gap=_utc(item["last_observed_before_gap"]),
            first_observed_after_gap=_utc(item["first_observed_after_gap"]),
            status=str(item["status"]),
        )
        for item in payload.get("boundary_gap_candidates", [])
    )
    for gap in gaps:
        if gap.first_observed_after_gap <= gap.last_observed_before_gap:
            raise ValueError(f"Gap {gap.gap_id!r} has invalid observed endpoints")
    return GapLedger(
        earliest_observed_tick=_utc(bounds["earliest_observed_tick_utc"]),
        latest_observed_tick=_utc(bounds["latest_observed_tick_utc"]),
        gaps=gaps,
        continuity_status=str(payload.get("continuity_claim") or CONTINUITY_STATUS),
    )


def _month_keys(start: pd.Timestamp, end: pd.Timestamp) -> tuple[tuple[int, int], ...]:
    cursor = pd.Timestamp(year=start.year, month=start.month, day=1, tz="UTC")
    keys: list[tuple[int, int]] = []
    while cursor < end:
        keys.append((cursor.year, cursor.month))
        cursor = cursor + pd.offsets.MonthBegin(1)
    return tuple(keys)


def _check_window_against_gap_ledger(
    start: pd.Timestamp,
    end: pd.Timestamp,
    ledger: GapLedger,
) -> None:
    if start < ledger.earliest_observed_tick:
        raise ArchiveWindowError(
            DATA_EXCLUDED_INSUFFICIENT_WARMUP,
            f"requested start {start.isoformat()} precedes earliest observed tick",
        )
    if end > ledger.latest_observed_tick:
        raise ArchiveWindowError(
            DATA_EXCLUDED_INCOMPLETE_HORIZON,
            f"requested end {end.isoformat()} exceeds latest observed tick",
        )

    for gap in ledger.gaps:
        if start < gap.first_observed_after_gap and end > gap.last_observed_before_gap:
            raise ArchiveWindowError(
                DATA_EXCLUDED_ARCHIVE_GAP,
                f"requested window intersects {gap.gap_id}",
            )


def _resolve_month_record(
    *,
    latest_manifest: dict[tuple[str, int, int], dict[str, object]],
    repo_root: Path,
    symbol: str,
    year: int,
    month: int,
) -> tuple[dict[str, object], Path, ArchiveMonthProvenance]:
    record = latest_manifest.get((symbol, year, month))
    if (
        record is None
        or record.get("status") != "VALIDATED"
        or record.get("validator_version") != VALIDATOR_VERSION
    ):
        raise ArchiveWindowError(
            DATA_EXCLUDED_ARCHIVE_MONTH_NOT_VALIDATED,
            f"{symbol} {year}-{month:02d} lacks a current validated manifest record",
        )

    local_path = Path(str(record["local_path"]))
    resolved = local_path if local_path.is_absolute() else repo_root / local_path
    expected_size = int(record["actual_size"])
    if not resolved.exists() or resolved.stat().st_size != expected_size:
        raise ArchiveWindowError(
            DATA_EXCLUDED_ARCHIVE_LOCAL_FILE_INVALID,
            f"validated local file missing or size-mismatched: {resolved}",
        )

    provenance = ArchiveMonthProvenance(
        symbol=symbol,
        year=year,
        month=month,
        local_path=str(local_path),
        sha256=str(record["sha256"]),
        actual_size=expected_size,
        validator_version=str(record["validator_version"]),
    )
    return record, resolved, provenance


def _read_month_window(
    *,
    path: Path,
    symbol: str,
    year: int,
    month: int,
    sha256: str,
    start: pd.Timestamp,
    end: pd.Timestamp,
) -> list[dict[str, object]]:
    admitted: list[dict[str, object]] = []
    previous_admitted_timestamp: pd.Timestamp | None = None

    with zipfile.ZipFile(path) as archive:
        csv_members = [name for name in archive.namelist() if name.lower().endswith(".csv")]
        if len(csv_members) != 1:
            raise ArchiveWindowError(
                DATA_EXCLUDED_ARCHIVE_CSV_INVALID,
                f"expected exactly one CSV member in {path}, got {csv_members}",
            )

        with archive.open(csv_members[0], "r") as raw:
            text = io.TextIOWrapper(raw, encoding="utf-8-sig", newline="")
            reader = csv.reader(text)
            header = next(reader, None)
            normalized = [cell.strip() for cell in (header or [])]
            if normalized != ["Exness", "Symbol", "Timestamp", "Bid", "Ask"]:
                raise ArchiveWindowError(
                    DATA_EXCLUDED_ARCHIVE_CSV_INVALID,
                    f"unexpected CSV header in {path}: {header}",
                )

            for raw_ordinal, row in enumerate(reader):
                if len(row) != 5:
                    raise ArchiveWindowError(
                        DATA_EXCLUDED_ARCHIVE_CSV_INVALID,
                        f"unexpected row width in {path} at raw ordinal {raw_ordinal}",
                    )
                provider, row_symbol, timestamp, bid_text, ask_text = (
                    cell.strip() for cell in row
                )
                ts = _utc(timestamp)
                if ts >= end:
                    break
                if ts < start:
                    continue

                try:
                    bid = float(bid_text)
                    ask = float(ask_text)
                except ValueError as exc:
                    raise ArchiveWindowError(
                        DATA_EXCLUDED_ARCHIVE_CSV_INVALID,
                        f"non-numeric Bid/Ask in {path} at raw ordinal {raw_ordinal}",
                    ) from exc

                if provider.casefold() != "exness" or row_symbol != symbol:
                    raise ArchiveWindowError(
                        DATA_EXCLUDED_ARCHIVE_CSV_INVALID,
                        f"provider/symbol mismatch in {path} at raw ordinal {raw_ordinal}",
                    )
                if not math.isfinite(bid) or not math.isfinite(ask) or ask < bid:
                    raise ArchiveWindowError(
                        DATA_EXCLUDED_ARCHIVE_CSV_INVALID,
                        f"invalid Bid/Ask in {path} at raw ordinal {raw_ordinal}",
                    )
                if previous_admitted_timestamp is not None and ts < previous_admitted_timestamp:
                    raise ArchiveWindowError(
                        DATA_EXCLUDED_ARCHIVE_CSV_INVALID,
                        f"timestamp regression in {path} at raw ordinal {raw_ordinal}",
                    )
                previous_admitted_timestamp = ts

                admitted.append(
                    {
                        "timestamp": ts,
                        "bid": bid,
                        "ask": ask,
                        "raw_ordinal": raw_ordinal,
                        "source_year": year,
                        "source_month": month,
                        "source_sha256": sha256,
                        "source_local_path": str(path),
                        "source_validator_version": VALIDATOR_VERSION,
                    }
                )

    return admitted


def load_archive_tick_window(
    *,
    repo_root: Path,
    manifest_path: Path,
    gap_ledger_path: Path,
    symbol: str,
    start: pd.Timestamp | str,
    end: pd.Timestamp | str,
) -> ArchiveWindowResult:
    """Stream a validated half-open Bid/Ask archive window with provenance."""

    requested_start = _utc(start)
    requested_end = _utc(end)
    if requested_end <= requested_start:
        raise ValueError("end must be strictly greater than start")

    gap_ledger = load_gap_ledger(gap_ledger_path)
    _check_window_against_gap_ledger(requested_start, requested_end, gap_ledger)

    latest_manifest = load_manifest(manifest_path)
    source_months: list[ArchiveMonthProvenance] = []
    admitted: list[dict[str, object]] = []

    for year, month in _month_keys(requested_start, requested_end):
        _record, resolved, provenance = _resolve_month_record(
            latest_manifest=latest_manifest,
            repo_root=repo_root,
            symbol=symbol,
            year=year,
            month=month,
        )
        source_months.append(provenance)
        admitted.extend(
            _read_month_window(
                path=resolved,
                symbol=symbol,
                year=year,
                month=month,
                sha256=provenance.sha256,
                start=requested_start,
                end=requested_end,
            )
        )

    if admitted:
        frame = pd.DataFrame(admitted).set_index("timestamp")
        frame.index = pd.DatetimeIndex(frame.index)
        validate_tick_frame(frame)
        status = WINDOW_STATUS_OK
    else:
        frame = pd.DataFrame(
            columns=[
                "bid",
                "ask",
                "raw_ordinal",
                "source_year",
                "source_month",
                "source_sha256",
                "source_local_path",
                "source_validator_version",
            ],
            index=pd.DatetimeIndex([], tz="UTC", name="timestamp"),
        )
        status = WINDOW_STATUS_NO_TICKS

    return ArchiveWindowResult(
        symbol=symbol,
        requested_start=requested_start,
        requested_end=requested_end,
        frame=frame,
        source_months=tuple(source_months),
        status=status,
        continuity_status=gap_ledger.continuity_status,
    )
