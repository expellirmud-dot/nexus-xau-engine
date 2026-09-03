from __future__ import annotations

import hashlib
import json
import lzma
import struct
import time
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import pandas as pd

DATAFEED_ROOT = "https://datafeed.dukascopy.com/datafeed"
_CANDLE_STRUCT = struct.Struct(">5If")
_CANDLE_RECORD_BYTES = _CANDLE_STRUCT.size
_SUPPORTED_SIDES = {"BID", "ASK"}
_PRICE_DIVISORS = {
    "XAUUSD": 1000.0,
}


@dataclass(frozen=True, slots=True)
class DukascopyExportResult:
    symbol: str
    side: str
    start_date: str
    end_date: str
    rows: int
    days_requested: int
    days_with_data: int
    days_no_data: int
    days_failed: int
    csv_path: str
    metadata_path: str
    sha256: str
    failed_dates: tuple[str, ...]


def parse_iso_date(value: str) -> date:
    return date.fromisoformat(value)


def _normalize_symbol(symbol: str) -> str:
    normalized = symbol.replace("/", "").replace("-", "").upper()
    if not normalized:
        raise ValueError("symbol is required")
    return normalized


def _normalize_side(side: str) -> str:
    normalized = side.upper()
    if normalized not in _SUPPORTED_SIDES:
        raise ValueError(f"side must be one of {sorted(_SUPPORTED_SIDES)}")
    return normalized


def price_divisor_for_symbol(symbol: str, explicit: float | None = None) -> float:
    if explicit is not None:
        if explicit <= 0:
            raise ValueError("price_divisor must be positive")
        return float(explicit)
    normalized = _normalize_symbol(symbol)
    if normalized not in _PRICE_DIVISORS:
        raise ValueError(
            f"No verified price divisor is registered for {normalized}; "
            "pass --price-divisor explicitly."
        )
    return _PRICE_DIVISORS[normalized]


def dukascopy_m1_day_url(*, symbol: str, day: date, side: str) -> str:
    """Build Dukascopy's daily M1 candle URL.

    Dukascopy datafeed months are zero-based (January=00, September=08).
    """

    normalized_symbol = _normalize_symbol(symbol)
    normalized_side = _normalize_side(side)
    zero_based_month = day.month - 1
    return (
        f"{DATAFEED_ROOT}/{normalized_symbol}/{day.year:04d}/"
        f"{zero_based_month:02d}/{day.day:02d}/"
        f"{normalized_side}_candles_min_1.bi5"
    )


def decode_dukascopy_m1_bi5(
    payload: bytes,
    *,
    day: date,
    price_divisor: float,
) -> pd.DataFrame:
    """Decode one Dukascopy daily M1 candle .bi5 payload to UTC OHLCV.

    Record layout is big-endian: seconds-from-day-start, open, close, low,
    high (uint32), then volume (float32). Prices are divided by the verified
    instrument-specific divisor.
    """

    if not payload:
        return pd.DataFrame(columns=["timestamp", "open", "high", "low", "close", "volume"])
    if price_divisor <= 0:
        raise ValueError("price_divisor must be positive")

    try:
        raw = lzma.decompress(payload)
    except lzma.LZMAError as exc:
        raise ValueError("Dukascopy .bi5 payload could not be LZMA-decompressed") from exc

    if len(raw) % _CANDLE_RECORD_BYTES != 0:
        raise ValueError(
            f"Decoded candle payload length {len(raw)} is not divisible by "
            f"{_CANDLE_RECORD_BYTES} bytes"
        )

    day_start = datetime(day.year, day.month, day.day, tzinfo=UTC)
    rows: list[dict[str, object]] = []
    for offset in range(0, len(raw), _CANDLE_RECORD_BYTES):
        seconds, open_raw, close_raw, low_raw, high_raw, volume = _CANDLE_STRUCT.unpack_from(
            raw, offset
        )
        if seconds >= 86_400:
            raise ValueError(f"Invalid seconds-from-day-start value: {seconds}")

        open_price = open_raw / price_divisor
        close_price = close_raw / price_divisor
        low_price = low_raw / price_divisor
        high_price = high_raw / price_divisor
        if high_price < max(open_price, close_price, low_price):
            raise ValueError("Invalid Dukascopy candle: high is below OHLC components")
        if low_price > min(open_price, close_price, high_price):
            raise ValueError("Invalid Dukascopy candle: low is above OHLC components")

        rows.append(
            {
                "timestamp": day_start + timedelta(seconds=int(seconds)),
                "open": open_price,
                "high": high_price,
                "low": low_price,
                "close": close_price,
                "volume": float(volume),
            }
        )

    frame = pd.DataFrame(rows)
    if frame.empty:
        return frame
    frame = frame.sort_values("timestamp")
    if frame["timestamp"].duplicated().any():
        raise ValueError("Duplicate timestamps inside Dukascopy day payload")
    return frame


def _download_bytes(url: str, *, timeout_seconds: float, retries: int) -> bytes | None:
    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be positive")
    if retries < 0:
        raise ValueError("retries cannot be negative")

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "NEXUS-XAU-Research/0.1"},
    )
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
                return response.read()
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return None
            last_error = exc
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last_error = exc

        if attempt < retries:
            time.sleep(min(2**attempt, 8))

    assert last_error is not None
    raise RuntimeError(f"Download failed after {retries + 1} attempt(s): {url}") from last_error


def _cache_path(*, cache_dir: Path, symbol: str, day: date, side: str) -> Path:
    normalized_symbol = _normalize_symbol(symbol)
    normalized_side = _normalize_side(side)
    return (
        cache_dir
        / normalized_symbol
        / f"{day.year:04d}"
        / f"{day.month:02d}"
        / f"{day.day:02d}"
        / f"{normalized_side}_candles_min_1.bi5"
    )


def _iter_days(start_date: date, end_date: date) -> list[date]:
    if end_date < start_date:
        raise ValueError("end_date must be on or after start_date")
    count = (end_date - start_date).days + 1
    return [start_date + timedelta(days=offset) for offset in range(count)]


def export_dukascopy_m1(
    *,
    symbol: str,
    side: str,
    start_date: date,
    end_date: date,
    output_path: str | Path,
    cache_dir: str | Path = "data/raw/dukascopy/cache",
    price_divisor: float | None = None,
    timeout_seconds: float = 30.0,
    retries: int = 3,
    pause_seconds: float = 0.10,
) -> DukascopyExportResult:
    """Download and merge an inclusive date range of Dukascopy M1 candles.

    Daily compressed files are cached. Re-running the same range therefore
    resumes from cached days instead of downloading successful days again.
    Missing/holiday days are recorded as no-data; network failures are recorded
    separately and do not get silently treated as market closures.
    """

    normalized_symbol = _normalize_symbol(symbol)
    normalized_side = _normalize_side(side)
    divisor = price_divisor_for_symbol(normalized_symbol, explicit=price_divisor)
    days = _iter_days(start_date, end_date)
    output = Path(output_path)
    cache_root = Path(cache_dir)
    output.parent.mkdir(parents=True, exist_ok=True)
    cache_root.mkdir(parents=True, exist_ok=True)

    frames: list[pd.DataFrame] = []
    no_data_dates: list[str] = []
    failed_dates: list[str] = []
    days_with_data = 0

    for index, day in enumerate(days):
        cached = _cache_path(
            cache_dir=cache_root,
            symbol=normalized_symbol,
            day=day,
            side=normalized_side,
        )
        payload: bytes | None
        downloaded_now = False
        if cached.exists():
            payload = cached.read_bytes()
        else:
            url = dukascopy_m1_day_url(symbol=normalized_symbol, day=day, side=normalized_side)
            try:
                payload = _download_bytes(
                    url,
                    timeout_seconds=timeout_seconds,
                    retries=retries,
                )
            except RuntimeError:
                failed_dates.append(day.isoformat())
                continue
            if payload is not None:
                cached.parent.mkdir(parents=True, exist_ok=True)
                cached.write_bytes(payload)
                downloaded_now = True

        if payload is None or len(payload) == 0:
            no_data_dates.append(day.isoformat())
            continue

        frame = decode_dukascopy_m1_bi5(payload, day=day, price_divisor=divisor)
        if frame.empty:
            no_data_dates.append(day.isoformat())
            continue
        frames.append(frame)
        days_with_data += 1

        if pause_seconds > 0 and index < len(days) - 1 and downloaded_now:
            time.sleep(pause_seconds)

    if frames:
        merged = pd.concat(frames, ignore_index=True).sort_values("timestamp")
        if merged["timestamp"].duplicated().any():
            duplicates = int(merged["timestamp"].duplicated().sum())
            raise ValueError(f"Duplicate timestamps across Dukascopy days: {duplicates}")
    else:
        merged = pd.DataFrame(columns=["timestamp", "open", "high", "low", "close", "volume"])

    merged.to_csv(output, index=False, date_format="%Y-%m-%dT%H:%M:%S%z")
    sha256 = hashlib.sha256(output.read_bytes()).hexdigest()
    metadata_path = output.with_suffix(output.suffix + ".meta.json")
    result = DukascopyExportResult(
        symbol=normalized_symbol,
        side=normalized_side,
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat(),
        rows=len(merged),
        days_requested=len(days),
        days_with_data=days_with_data,
        days_no_data=len(no_data_dates),
        days_failed=len(failed_dates),
        csv_path=str(output),
        metadata_path=str(metadata_path),
        sha256=sha256,
        failed_dates=tuple(failed_dates),
    )
    metadata = {
        **asdict(result),
        "source": "Dukascopy datafeed daily M1 candle .bi5",
        "datafeed_root": DATAFEED_ROOT,
        "timestamp_timezone": "UTC",
        "date_range_semantics": "inclusive start_date and end_date",
        "price_divisor": divisor,
        "no_data_dates": no_data_dates,
        "cache_dir": str(cache_root),
        "research_warning": (
            "Dukascopy is a research feed and must not be silently treated as identical "
            "to Exness/MT5 execution feed. Cross-feed validation is required."
        ),
    }
    metadata_path.write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return result



def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Download Dukascopy XAUUSD M1 candles")
    parser.add_argument("--symbol", default="XAUUSD")
    parser.add_argument("--side", choices=["BID", "ASK"], default="BID")
    parser.add_argument("--start", required=True, help="inclusive YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="inclusive YYYY-MM-DD")
    parser.add_argument("--out", required=True)
    parser.add_argument("--cache-dir", default="data/raw/dukascopy/cache")
    parser.add_argument("--price-divisor", type=float, default=None)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--pause", type=float, default=0.10)
    args = parser.parse_args()

    result = export_dukascopy_m1(
        symbol=args.symbol,
        side=args.side,
        start_date=parse_iso_date(args.start),
        end_date=parse_iso_date(args.end),
        output_path=args.out,
        cache_dir=args.cache_dir,
        price_divisor=args.price_divisor,
        timeout_seconds=args.timeout,
        retries=args.retries,
        pause_seconds=args.pause,
    )
    print(
        f"Dukascopy export: {result.rows} M1 bars / "
        f"data_days={result.days_with_data} / no_data={result.days_no_data} / "
        f"failed={result.days_failed}"
    )
    print(f"CSV: {result.csv_path}")
    print(f"Metadata: {result.metadata_path}")
    if result.failed_dates:
        print("Failed dates: " + ", ".join(result.failed_dates))
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
