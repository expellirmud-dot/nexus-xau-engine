from __future__ import annotations

import json
import os
from collections import Counter
from collections.abc import Callable, Iterable
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import quote
from urllib.request import Request, urlopen

BASE_URL = "https://ticks.ex2archive.com/ticks/"
USER_AGENT = "NEXUS-XAU-Research/0.1"

TERMINAL_STATUSES = {
    "AVAILABLE",
    "YEAR_DIRECTORY_MISSING",
    "MONTH_DIRECTORY_MISSING",
    "EXPECTED_FILE_MISSING",
}


@dataclass(frozen=True)
class ArchiveEntry:
    name: str
    type: str
    mtime: str | None = None
    size: int | None = None


@dataclass(frozen=True)
class ArchiveMonthRecord:
    symbol: str
    year: int
    month: int
    directory_url: str
    expected_filename: str
    status: str
    file_name: str | None
    file_size: int | None
    file_mtime: str | None
    observed_at_utc: str
    evidence_basis: str
    error_message: str | None = None


class ArchiveAcquisitionError(RuntimeError):
    """Expected network or remote-payload acquisition failure."""


DirectoryLoader = Callable[[str], list[ArchiveEntry]]


def _directory_url(base_url: str, *parts: str) -> str:
    base = base_url.rstrip("/") + "/"
    encoded = "/".join(quote(part.strip("/"), safe="") for part in parts)
    return f"{base}{encoded}/" if encoded else base


def expected_month_filename(symbol: str, year: int, month: int) -> str:
    if not 1 <= month <= 12:
        raise ValueError("month must be 1..12")
    return f"Exness_{symbol}_{year}_{month:02d}.zip"


def parse_directory_payload(raw: bytes | str) -> list[ArchiveEntry]:
    text = raw.decode("utf-8") if isinstance(raw, bytes) else raw
    payload = json.loads(text)
    if not isinstance(payload, list):
        raise TypeError("archive directory payload must be a JSON array")

    entries: list[ArchiveEntry] = []
    for item in payload:
        if not isinstance(item, dict):
            raise TypeError("archive directory entry must be an object")
        name = item.get("name")
        entry_type = item.get("type")
        if not isinstance(name, str) or not name:
            raise ValueError("archive directory entry has invalid name")
        if entry_type not in {"file", "directory"}:
            raise ValueError("archive directory entry has invalid type")

        size = item.get("size")
        if size is not None and (not isinstance(size, int) or size < 0):
            raise ValueError("archive directory entry has invalid size")
        mtime = item.get("mtime")
        if mtime is not None and not isinstance(mtime, str):
            raise ValueError("archive directory entry has invalid mtime")

        entries.append(
            ArchiveEntry(
                name=name,
                type=entry_type,
                mtime=mtime,
                size=size,
            )
        )
    return entries


def fetch_directory(
    url: str,
    *,
    timeout_seconds: float = 30.0,
) -> list[ArchiveEntry]:
    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be > 0")
    request = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            return parse_directory_payload(response.read())
    except (OSError, TypeError, ValueError) as exc:
        raise ArchiveAcquisitionError(f"{type(exc).__name__}: {exc}") from exc


def _record_key(record: ArchiveMonthRecord) -> tuple[str, int, int]:
    return (record.symbol, record.year, record.month)


def load_existing_records(path: str | Path) -> list[ArchiveMonthRecord]:
    target = Path(path)
    if not target.exists():
        return []

    records: list[ArchiveMonthRecord] = []
    for line in target.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        records.append(ArchiveMonthRecord(**json.loads(line)))
    return records


def append_record(path: str | Path, record: ArchiveMonthRecord) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(asdict(record), ensure_ascii=False) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def latest_records_by_month(
    records: Iterable[ArchiveMonthRecord],
) -> dict[tuple[str, int, int], ArchiveMonthRecord]:
    latest: dict[tuple[str, int, int], ArchiveMonthRecord] = {}
    for record in records:
        latest[_record_key(record)] = record
    return latest


def _now_utc() -> str:
    return datetime.now(UTC).isoformat()


def _missing_record(
    *,
    symbol: str,
    year: int,
    month: int,
    base_url: str,
    status: str,
    evidence_basis: str,
) -> ArchiveMonthRecord:
    return ArchiveMonthRecord(
        symbol=symbol,
        year=year,
        month=month,
        directory_url=_directory_url(base_url, symbol, str(year), f"{month:02d}"),
        expected_filename=expected_month_filename(symbol, year, month),
        status=status,
        file_name=None,
        file_size=None,
        file_mtime=None,
        observed_at_utc=_now_utc(),
        evidence_basis=evidence_basis,
    )


def _error_record(
    *,
    symbol: str,
    year: int,
    month: int,
    base_url: str,
    evidence_basis: str,
    error: Exception,
) -> ArchiveMonthRecord:
    return ArchiveMonthRecord(
        symbol=symbol,
        year=year,
        month=month,
        directory_url=_directory_url(base_url, symbol, str(year), f"{month:02d}"),
        expected_filename=expected_month_filename(symbol, year, month),
        status="ERROR",
        file_name=None,
        file_size=None,
        file_mtime=None,
        observed_at_utc=_now_utc(),
        evidence_basis=evidence_basis,
        error_message=f"{type(error).__name__}: {error}",
    )


def summarize_records(
    records: Iterable[ArchiveMonthRecord],
    *,
    symbol: str,
    start_year: int,
    end_year: int,
    months: Iterable[int],
) -> dict[str, Any]:
    month_set = set(months)
    latest = latest_records_by_month(records)
    selected = [
        record
        for (record_symbol, year, month), record in latest.items()
        if record_symbol == symbol
        and start_year <= year <= end_year
        and month in month_set
    ]
    counts = Counter(record.status for record in selected)
    available = [record for record in selected if record.status == "AVAILABLE"]
    return {
        "latest_records": len(selected),
        "status_counts": dict(sorted(counts.items())),
        "available_months": len(available),
        "available_bytes": sum(record.file_size or 0 for record in available),
        "earliest_available_month": (
            min(f"{record.year:04d}-{record.month:02d}" for record in available)
            if available
            else None
        ),
        "latest_available_month": (
            max(f"{record.year:04d}-{record.month:02d}" for record in available)
            if available
            else None
        ),
        "error_months": sorted(
            f"{record.year:04d}-{record.month:02d}"
            for record in selected
            if record.status == "ERROR"
        ),
    }


def scan_exness_archive_coverage(
    *,
    symbol: str,
    start_year: int,
    end_year: int,
    output_jsonl: str | Path,
    months: Iterable[int] | None = None,
    base_url: str = BASE_URL,
    timeout_seconds: float = 30.0,
    directory_loader: DirectoryLoader | None = None,
) -> dict[str, Any]:
    if not symbol:
        raise ValueError("symbol is required")
    if end_year < start_year:
        raise ValueError("end_year must be on or after start_year")

    selected_months = (
        list(range(1, 13))
        if months is None
        else sorted({int(month) for month in months})
    )
    if not selected_months or any(month < 1 or month > 12 for month in selected_months):
        raise ValueError("months must contain values in 1..12")

    loader = directory_loader or (
        lambda url: fetch_directory(url, timeout_seconds=timeout_seconds)
    )

    records = load_existing_records(output_jsonl)
    latest = latest_records_by_month(records)

    def is_complete(year: int, month: int) -> bool:
        existing = latest.get((symbol, year, month))
        return existing is not None and existing.status in TERMINAL_STATUSES

    def persist(record: ArchiveMonthRecord) -> None:
        append_record(output_jsonl, record)
        records.append(record)
        latest[_record_key(record)] = record

    symbol_url = _directory_url(base_url, symbol)
    try:
        symbol_entries = loader(symbol_url)
    except ArchiveAcquisitionError as exc:
        for year in range(start_year, end_year + 1):
            for month in selected_months:
                if is_complete(year, month):
                    continue
                persist(
                    _error_record(
                        symbol=symbol,
                        year=year,
                        month=month,
                        base_url=base_url,
                        evidence_basis="SYMBOL_DIRECTORY_LISTING_ERROR",
                        error=exc,
                    )
                )
        return _coverage_result(
            records=records,
            symbol=symbol,
            start_year=start_year,
            end_year=end_year,
            months=selected_months,
            output_jsonl=output_jsonl,
            base_url=base_url,
        )

    listed_years = {
        int(entry.name)
        for entry in symbol_entries
        if entry.type == "directory"
        and len(entry.name) == 4
        and entry.name.isdigit()
    }

    for year in range(start_year, end_year + 1):
        pending = [month for month in selected_months if not is_complete(year, month)]
        if not pending:
            continue

        if year not in listed_years:
            for month in pending:
                persist(
                    _missing_record(
                        symbol=symbol,
                        year=year,
                        month=month,
                        base_url=base_url,
                        status="YEAR_DIRECTORY_MISSING",
                        evidence_basis="SYMBOL_DIRECTORY_LISTING",
                    )
                )
            continue

        year_url = _directory_url(base_url, symbol, str(year))
        try:
            year_entries = loader(year_url)
        except ArchiveAcquisitionError as exc:
            for month in pending:
                persist(
                    _error_record(
                        symbol=symbol,
                        year=year,
                        month=month,
                        base_url=base_url,
                        evidence_basis="YEAR_DIRECTORY_LISTING_ERROR",
                        error=exc,
                    )
                )
            continue

        listed_months = {
            int(entry.name)
            for entry in year_entries
            if entry.type == "directory"
            and len(entry.name) == 2
            and entry.name.isdigit()
            and 1 <= int(entry.name) <= 12
        }

        for month in pending:
            if month not in listed_months:
                persist(
                    _missing_record(
                        symbol=symbol,
                        year=year,
                        month=month,
                        base_url=base_url,
                        status="MONTH_DIRECTORY_MISSING",
                        evidence_basis="YEAR_DIRECTORY_LISTING",
                    )
                )
                continue

            month_url = _directory_url(base_url, symbol, str(year), f"{month:02d}")
            try:
                month_entries = loader(month_url)
            except ArchiveAcquisitionError as exc:
                persist(
                    _error_record(
                        symbol=symbol,
                        year=year,
                        month=month,
                        base_url=base_url,
                        evidence_basis="MONTH_DIRECTORY_LISTING_ERROR",
                        error=exc,
                    )
                )
                continue

            expected = expected_month_filename(symbol, year, month)
            entry = next(
                (
                    candidate
                    for candidate in month_entries
                    if candidate.type == "file" and candidate.name == expected
                ),
                None,
            )
            if entry is None:
                persist(
                    _missing_record(
                        symbol=symbol,
                        year=year,
                        month=month,
                        base_url=base_url,
                        status="EXPECTED_FILE_MISSING",
                        evidence_basis="MONTH_DIRECTORY_LISTING",
                    )
                )
                continue

            persist(
                ArchiveMonthRecord(
                    symbol=symbol,
                    year=year,
                    month=month,
                    directory_url=month_url,
                    expected_filename=expected,
                    status="AVAILABLE",
                    file_name=entry.name,
                    file_size=entry.size,
                    file_mtime=entry.mtime,
                    observed_at_utc=_now_utc(),
                    evidence_basis="MONTH_DIRECTORY_LISTING",
                )
            )

    return _coverage_result(
        records=records,
        symbol=symbol,
        start_year=start_year,
        end_year=end_year,
        months=selected_months,
        output_jsonl=output_jsonl,
        base_url=base_url,
    )


def _coverage_result(
    *,
    records: list[ArchiveMonthRecord],
    symbol: str,
    start_year: int,
    end_year: int,
    months: list[int],
    output_jsonl: str | Path,
    base_url: str,
) -> dict[str, Any]:
    summary = summarize_records(
        records,
        symbol=symbol,
        start_year=start_year,
        end_year=end_year,
        months=months,
    )
    return {
        "schema_version": "EXNESS_TICK_ARCHIVE_COVERAGE_V0.1",
        "mode": "READ_ONLY_EXTERNAL_METADATA_NO_ORDER_SEND",
        "symbol": symbol,
        "start_year": start_year,
        "end_year": end_year,
        "months": months,
        "base_url": base_url,
        "output_jsonl": str(output_jsonl),
        "expected_months": (end_year - start_year + 1) * len(months),
        "summary": summary,
        "interpretation_guard": (
            "Archive directory/file availability does not prove tick-level continuity, "
            "target-server equivalence, slippage, fills, or profitability. ERROR records "
            "are retryable on resume; terminal metadata observations are not re-probed."
        ),
    }
