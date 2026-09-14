from __future__ import annotations

import json
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

import pandas as pd


@dataclass(frozen=True)
class CoverageProbe:
    symbol: str
    data_class: str
    timeframe: str | None
    requested_start_utc: str
    requested_end_utc: str
    calendar_class: str
    rows: int
    first_timestamp_utc: str | None
    last_timestamp_utc: str | None
    duplicate_timestamps: int
    non_monotonic_timestamps: int
    status: str
    raw_rows: int = 0
    out_of_range_rows: int = 0
    mt5_error_code: int | None = None
    mt5_error_message: str | None = None
    nominal_expected_rows: int | None = None
    nominal_row_fraction: float | None = None


def iter_probe_datetimes(
    start_date: date,
    end_date: date,
    *,
    step_days: int,
    probe_hour_utc: int,
) -> Iterable[datetime]:
    if end_date < start_date:
        raise ValueError("end_date must be on or after start_date")
    if step_days < 1:
        raise ValueError("step_days must be >= 1")
    if not 0 <= probe_hour_utc <= 23:
        raise ValueError("probe_hour_utc must be 0..23")

    current = start_date
    while current <= end_date:
        yield datetime(
            current.year,
            current.month,
            current.day,
            probe_hour_utc,
            tzinfo=UTC,
        )
        current += timedelta(days=step_days)


def _calendar_class(value: datetime) -> str:
    return "WEEKEND" if value.weekday() >= 5 else "WEEKDAY"


def _timestamp_stats(values: pd.Series) -> tuple[str | None, str | None, int, int]:
    if values.empty:
        return None, None, 0, 0

    duplicate_count = int(values.duplicated().sum())
    diffs = values.diff().dropna()
    non_monotonic = int((diffs < pd.Timedelta(0)).sum())
    return (
        values.iloc[0].isoformat(),
        values.iloc[-1].isoformat(),
        duplicate_count,
        non_monotonic,
    )


def _in_requested_range(
    timestamps: pd.Series,
    *,
    start_utc: datetime,
    end_utc: datetime,
) -> pd.Series:
    start = pd.Timestamp(start_utc)
    end = pd.Timestamp(end_utc)
    return (timestamps >= start) & (timestamps < end)


def summarize_ticks(
    ticks: Any,
    *,
    symbol: str,
    start_utc: datetime,
    end_utc: datetime,
    error: tuple[int, str] | None = None,
) -> CoverageProbe:
    base = {
        "symbol": symbol,
        "data_class": "MT5_HISTORICAL_TICK",
        "timeframe": None,
        "requested_start_utc": start_utc.isoformat(),
        "requested_end_utc": end_utc.isoformat(),
        "calendar_class": _calendar_class(start_utc),
    }
    if ticks is None:
        code, message = error or (None, None)
        return CoverageProbe(
            **base,
            rows=0,
            first_timestamp_utc=None,
            last_timestamp_utc=None,
            duplicate_timestamps=0,
            non_monotonic_timestamps=0,
            status="ERROR",
            mt5_error_code=code,
            mt5_error_message=message,
        )

    frame = pd.DataFrame(ticks)
    raw_rows = len(frame)
    if frame.empty:
        return CoverageProbe(
            **base,
            rows=0,
            first_timestamp_utc=None,
            last_timestamp_utc=None,
            duplicate_timestamps=0,
            non_monotonic_timestamps=0,
            status="EMPTY",
            raw_rows=0,
        )

    if "time_msc" in frame.columns:
        timestamps = pd.to_datetime(frame["time_msc"], unit="ms", utc=True)
    elif "time" in frame.columns:
        timestamps = pd.to_datetime(frame["time"], unit="s", utc=True)
    else:
        raise ValueError("tick payload has no time/time_msc field")

    mask = _in_requested_range(
        timestamps,
        start_utc=start_utc,
        end_utc=end_utc,
    )
    in_range = timestamps.loc[mask].reset_index(drop=True)
    out_of_range_rows = raw_rows - len(in_range)
    if in_range.empty:
        return CoverageProbe(
            **base,
            rows=0,
            first_timestamp_utc=None,
            last_timestamp_utc=None,
            duplicate_timestamps=0,
            non_monotonic_timestamps=0,
            status="EMPTY",
            raw_rows=raw_rows,
            out_of_range_rows=out_of_range_rows,
        )

    first, last, duplicates, non_monotonic = _timestamp_stats(in_range)
    return CoverageProbe(
        **base,
        rows=len(in_range),
        first_timestamp_utc=first,
        last_timestamp_utc=last,
        duplicate_timestamps=duplicates,
        non_monotonic_timestamps=non_monotonic,
        status="AVAILABLE",
        raw_rows=raw_rows,
        out_of_range_rows=out_of_range_rows,
    )


def summarize_m1_rates(
    rates: Any,
    *,
    symbol: str,
    start_utc: datetime,
    end_utc: datetime,
    window_minutes: int,
    error: tuple[int, str] | None = None,
) -> CoverageProbe:
    base = {
        "symbol": symbol,
        "data_class": "MT5_OHLC",
        "timeframe": "M1",
        "requested_start_utc": start_utc.isoformat(),
        "requested_end_utc": end_utc.isoformat(),
        "calendar_class": _calendar_class(start_utc),
    }
    if rates is None:
        code, message = error or (None, None)
        return CoverageProbe(
            **base,
            rows=0,
            first_timestamp_utc=None,
            last_timestamp_utc=None,
            duplicate_timestamps=0,
            non_monotonic_timestamps=0,
            status="ERROR",
            mt5_error_code=code,
            mt5_error_message=message,
            nominal_expected_rows=window_minutes,
        )

    frame = pd.DataFrame(rates)
    raw_rows = len(frame)
    if frame.empty:
        return CoverageProbe(
            **base,
            rows=0,
            first_timestamp_utc=None,
            last_timestamp_utc=None,
            duplicate_timestamps=0,
            non_monotonic_timestamps=0,
            status="EMPTY",
            raw_rows=0,
            nominal_expected_rows=window_minutes,
            nominal_row_fraction=0.0,
        )

    if "time" not in frame.columns:
        raise ValueError("rate payload has no time field")

    timestamps = pd.to_datetime(frame["time"], unit="s", utc=True)
    mask = _in_requested_range(
        timestamps,
        start_utc=start_utc,
        end_utc=end_utc,
    )
    in_range = timestamps.loc[mask].reset_index(drop=True)
    out_of_range_rows = raw_rows - len(in_range)
    if in_range.empty:
        return CoverageProbe(
            **base,
            rows=0,
            first_timestamp_utc=None,
            last_timestamp_utc=None,
            duplicate_timestamps=0,
            non_monotonic_timestamps=0,
            status="EMPTY",
            raw_rows=raw_rows,
            out_of_range_rows=out_of_range_rows,
            nominal_expected_rows=window_minutes,
            nominal_row_fraction=0.0,
        )

    first, last, duplicates, non_monotonic = _timestamp_stats(in_range)
    return CoverageProbe(
        **base,
        rows=len(in_range),
        first_timestamp_utc=first,
        last_timestamp_utc=last,
        duplicate_timestamps=duplicates,
        non_monotonic_timestamps=non_monotonic,
        status="AVAILABLE",
        raw_rows=raw_rows,
        out_of_range_rows=out_of_range_rows,
        nominal_expected_rows=window_minutes,
        nominal_row_fraction=len(in_range) / window_minutes,
    )


def _probe_key(record: CoverageProbe) -> tuple[str, str, str | None]:
    return (
        record.requested_start_utc,
        record.data_class,
        record.timeframe,
    )


def load_existing_records(path: str | Path) -> list[CoverageProbe]:
    target = Path(path)
    if not target.exists():
        return []

    records: list[CoverageProbe] = []
    for raw in target.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        records.append(CoverageProbe(**json.loads(raw)))
    return records


def append_record(path: str | Path, record: CoverageProbe) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(asdict(record), ensure_ascii=False) + "\n")
        handle.flush()


def summarize_coverage(records: list[CoverageProbe]) -> dict[str, Any]:
    groups: dict[str, list[CoverageProbe]] = {}
    for record in records:
        label = (
            record.data_class
            if record.timeframe is None
            else f"{record.data_class}_{record.timeframe}"
        )
        groups.setdefault(label, []).append(record)

    summary: dict[str, Any] = {}
    for label, items in groups.items():
        available = [item for item in items if item.status == "AVAILABLE"]
        weekday_empty = [
            item
            for item in items
            if item.status == "EMPTY" and item.calendar_class == "WEEKDAY"
        ]
        errors = [item for item in items if item.status == "ERROR"]
        out_of_range = [item for item in items if item.out_of_range_rows > 0]
        summary[label] = {
            "probes": len(items),
            "available": len(available),
            "empty": sum(item.status == "EMPTY" for item in items),
            "weekday_empty": len(weekday_empty),
            "errors": len(errors),
            "responses_with_out_of_range_rows": len(out_of_range),
            "earliest_available_request_utc": (
                min(item.requested_start_utc for item in available)
                if available
                else None
            ),
            "latest_available_request_utc": (
                max(item.requested_start_utc for item in available)
                if available
                else None
            ),
            "earliest_weekday_empty_request_utc": (
                min(item.requested_start_utc for item in weekday_empty)
                if weekday_empty
                else None
            ),
            "latest_weekday_empty_request_utc": (
                max(item.requested_start_utc for item in weekday_empty)
                if weekday_empty
                else None
            ),
        }
    return summary


def scan_mt5_history_coverage(
    *,
    symbol: str,
    start_date: date,
    end_date: date,
    step_days: int,
    probe_hour_utc: int,
    window_minutes: int,
    output_jsonl: str | Path,
) -> dict[str, Any]:
    if window_minutes < 1:
        raise ValueError("window_minutes must be >= 1")

    try:
        import MetaTrader5 as mt5
    except ImportError as exc:  # pragma: no cover - Windows/MT5 dependent
        raise RuntimeError(
            'MetaTrader5 package is not installed. Run: pip install -e ".[dev,mt5]"'
        ) from exc

    if not mt5.initialize():  # pragma: no cover - live terminal required
        code, message = mt5.last_error()
        raise RuntimeError(f"MT5 initialize failed: {code} {message}")

    existing = load_existing_records(output_jsonl)
    completed = {_probe_key(record) for record in existing}
    records = list(existing)

    try:  # pragma: no cover - live terminal required
        if not mt5.symbol_select(symbol, True):
            code, message = mt5.last_error()
            raise RuntimeError(f"Cannot select symbol {symbol}: {code} {message}")

        for start_utc in iter_probe_datetimes(
            start_date,
            end_date,
            step_days=step_days,
            probe_hour_utc=probe_hour_utc,
        ):
            end_utc = start_utc + timedelta(minutes=window_minutes)

            tick_key = (start_utc.isoformat(), "MT5_HISTORICAL_TICK", None)
            if tick_key not in completed:
                ticks = mt5.copy_ticks_range(
                    symbol,
                    start_utc,
                    end_utc,
                    mt5.COPY_TICKS_ALL,
                )
                error = mt5.last_error() if ticks is None else None
                record = summarize_ticks(
                    ticks,
                    symbol=symbol,
                    start_utc=start_utc,
                    end_utc=end_utc,
                    error=error,
                )
                append_record(output_jsonl, record)
                records.append(record)
                completed.add(tick_key)

            rate_key = (start_utc.isoformat(), "MT5_OHLC", "M1")
            if rate_key not in completed:
                rates = mt5.copy_rates_range(
                    symbol,
                    mt5.TIMEFRAME_M1,
                    start_utc,
                    end_utc,
                )
                error = mt5.last_error() if rates is None else None
                record = summarize_m1_rates(
                    rates,
                    symbol=symbol,
                    start_utc=start_utc,
                    end_utc=end_utc,
                    window_minutes=window_minutes,
                    error=error,
                )
                append_record(output_jsonl, record)
                records.append(record)
                completed.add(rate_key)

        return {
            "schema_version": "MT5_HISTORY_COVERAGE_V0.2",
            "symbol": symbol,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "step_days": step_days,
            "probe_hour_utc": probe_hour_utc,
            "window_minutes": window_minutes,
            "output_jsonl": str(output_jsonl),
            "interval_semantics": "[start_utc, end_utc)",
            "interpretation_guard": (
                "Availability probes do not by themselves prove continuous history. "
                "WEEKDAY EMPTY requires session/holiday context before calling it a gap. "
                "Rows returned outside the requested interval are recorded but do not "
                "count as availability for that interval."
            ),
            "summary": summarize_coverage(records),
        }
    finally:  # pragma: no cover - live terminal required
        mt5.shutdown()
