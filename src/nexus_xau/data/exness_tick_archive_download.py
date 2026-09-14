from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import os
import zipfile
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from urllib.request import Request, urlopen

from nexus_xau.data.exness_tick_archive import BASE_URL, USER_AGENT, expected_month_filename


@dataclass(frozen=True)
class DownloadValidationRecord:
    symbol: str
    year: int
    month: int
    url: str
    local_path: str
    expected_size: int | None
    actual_size: int
    sha256: str
    zip_integrity: str
    csv_member: str
    row_count: int
    first_timestamp: str | None
    last_timestamp: str | None
    distinct_dates: int
    provider_mismatch: int
    symbol_mismatch: int
    ask_lt_bid: int
    non_finite: int
    timestamp_regression: int
    consecutive_equal_timestamp: int
    consecutive_exact_duplicate: int
    status: str
    validated_at_utc: str


def month_url(symbol: str, year: int, month: int, *, base_url: str = BASE_URL) -> str:
    filename = expected_month_filename(symbol, year, month)
    return f"{base_url.rstrip('/')}/{symbol}/{year}/{month:02d}/{filename}"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _download_with_resume(url: str, target: Path, *, timeout_seconds: float = 60.0) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    partial = target.with_suffix(target.suffix + ".part")
    offset = partial.stat().st_size if partial.exists() else 0
    headers = {"User-Agent": USER_AGENT}
    if offset:
        headers["Range"] = f"bytes={offset}-"
    request = Request(url, headers=headers)
    with urlopen(request, timeout=timeout_seconds) as response:
        status = getattr(response, "status", response.getcode())
        if offset and status == 206:
            mode = "ab"
        else:
            mode = "wb"
            offset = 0
        with partial.open(mode) as handle:
            while True:
                block = response.read(1024 * 1024)
                if not block:
                    break
                handle.write(block)
            handle.flush()
            os.fsync(handle.fileno())
    os.replace(partial, target)


def _parse_ts(value: str) -> datetime:
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    return datetime.fromisoformat(text).astimezone(UTC)


def validate_zip(path: Path, *, symbol: str) -> dict[str, object]:
    with zipfile.ZipFile(path) as archive:
        bad = archive.testzip()
        if bad is not None:
            raise ValueError(f"ZIP integrity failure at member {bad}")
        csv_members = [name for name in archive.namelist() if name.lower().endswith(".csv")]
        if len(csv_members) != 1:
            raise ValueError(f"expected exactly one CSV member, got {csv_members}")
        member = csv_members[0]
        with archive.open(member, "r") as raw:
            text = io.TextIOWrapper(raw, encoding="utf-8-sig", newline="")
            reader = csv.reader(text)
            header = next(reader, None)
            normalized = [cell.strip() for cell in (header or [])]
            if normalized != ["Exness", "Symbol", "Timestamp", "Bid", "Ask"]:
                raise ValueError(f"unexpected CSV header: {header}")

            row_count = 0
            first_timestamp: str | None = None
            last_timestamp: str | None = None
            dates: set[str] = set()
            provider_mismatch = 0
            symbol_mismatch = 0
            ask_lt_bid = 0
            non_finite = 0
            timestamp_regression = 0
            consecutive_equal_timestamp = 0
            consecutive_exact_duplicate = 0
            previous_ts: datetime | None = None
            previous_row: tuple[str, ...] | None = None

            for row in reader:
                if len(row) != 5:
                    raise ValueError(f"unexpected CSV row width at row {row_count + 2}: {len(row)}")
                provider, row_symbol, timestamp, bid_text, ask_text = (cell.strip() for cell in row)
                ts = _parse_ts(timestamp)
                try:
                    bid = float(bid_text)
                    ask = float(ask_text)
                except ValueError:
                    bid = math.nan
                    ask = math.nan

                row_count += 1
                if first_timestamp is None:
                    first_timestamp = ts.isoformat().replace("+00:00", "Z")
                last_timestamp = ts.isoformat().replace("+00:00", "Z")
                dates.add(ts.date().isoformat())
                provider_mismatch += provider != "Exness"
                symbol_mismatch += row_symbol != symbol
                finite = math.isfinite(bid) and math.isfinite(ask)
                non_finite += not finite
                if finite:
                    ask_lt_bid += ask < bid
                if previous_ts is not None:
                    timestamp_regression += ts < previous_ts
                    consecutive_equal_timestamp += ts == previous_ts
                current_row = (provider, row_symbol, timestamp, bid_text, ask_text)
                if previous_row is not None:
                    consecutive_exact_duplicate += current_row == previous_row
                previous_ts = ts
                previous_row = current_row

    return {
        "zip_integrity": "PASS",
        "csv_member": member,
        "row_count": row_count,
        "first_timestamp": first_timestamp,
        "last_timestamp": last_timestamp,
        "distinct_dates": len(dates),
        "provider_mismatch": provider_mismatch,
        "symbol_mismatch": symbol_mismatch,
        "ask_lt_bid": ask_lt_bid,
        "non_finite": non_finite,
        "timestamp_regression": timestamp_regression,
        "consecutive_equal_timestamp": consecutive_equal_timestamp,
        "consecutive_exact_duplicate": consecutive_exact_duplicate,
    }


def load_manifest(path: Path) -> dict[tuple[str, int, int], dict[str, object]]:
    latest: dict[tuple[str, int, int], dict[str, object]] = {}
    if not path.exists():
        return latest
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        item = json.loads(line)
        latest[(str(item["symbol"]), int(item["year"]), int(item["month"]))] = item
    return latest


def append_manifest(path: Path, record: DownloadValidationRecord) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(asdict(record), ensure_ascii=False) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def download_and_validate_month(
    *,
    symbol: str,
    year: int,
    month: int,
    output_root: Path,
    manifest_path: Path,
    expected_size: int | None = None,
    timeout_seconds: float = 60.0,
    base_url: str = BASE_URL,
) -> DownloadValidationRecord:
    latest = load_manifest(manifest_path)
    key = (symbol, year, month)
    prior = latest.get(key)
    if prior and prior.get("status") == "VALIDATED":
        prior_path = Path(str(prior["local_path"]))
        if prior_path.exists() and prior_path.stat().st_size == int(prior["actual_size"]):
            return DownloadValidationRecord(**prior)

    filename = expected_month_filename(symbol, year, month)
    target = output_root / symbol / f"{year:04d}" / filename
    url = month_url(symbol, year, month, base_url=base_url)

    if not target.exists() or (expected_size is not None and target.stat().st_size != expected_size):
        _download_with_resume(url, target, timeout_seconds=timeout_seconds)

    actual_size = target.stat().st_size
    if expected_size is not None and actual_size != expected_size:
        raise ValueError(f"download size mismatch: expected {expected_size}, got {actual_size}")

    validation = validate_zip(target, symbol=symbol)
    record = DownloadValidationRecord(
        symbol=symbol,
        year=year,
        month=month,
        url=url,
        local_path=str(target),
        expected_size=expected_size,
        actual_size=actual_size,
        sha256=_sha256(target),
        status="VALIDATED",
        validated_at_utc=datetime.now(UTC).isoformat(),
        **validation,
    )
    append_manifest(manifest_path, record)
    return record
