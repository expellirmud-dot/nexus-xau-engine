from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd


@dataclass(frozen=True)
class Mt5ExportResult:
    symbol: str
    timeframe: str
    start_utc: str
    end_utc: str
    rows: int
    csv_path: str
    metadata_path: str


def parse_aware_datetime(value: str) -> datetime:
    """Parse an ISO-8601 datetime and require an explicit timezone."""
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError(
            "Datetime must include timezone, e.g. 2026-08-24T00:00:00+00:00"
        )
    return parsed.astimezone(UTC)


def export_mt5_m1(
    *,
    symbol: str,
    start: datetime,
    end: datetime,
    output_path: str | Path,
) -> Mt5ExportResult:
    """Export MT5 M1 bars to a UTC, replay-loader-compatible CSV.

    This is for pipeline/time-boundary validation first. It does not provide
    full Bid+Ask tick history and therefore is not the final execution-quality
    backtest dataset.
    """
    if start.tzinfo is None or end.tzinfo is None:
        raise ValueError("start/end must be timezone-aware")

    start_utc = start.astimezone(UTC)
    end_utc = end.astimezone(UTC)
    if end_utc <= start_utc:
        raise ValueError("end must be later than start")

    try:
        import MetaTrader5 as mt5
    except ImportError as exc:  # pragma: no cover - depends on Windows/MT5 install
        raise RuntimeError(
            'MetaTrader5 package is not installed. Run: pip install -e ".[dev,mt5]"'
        ) from exc

    if not mt5.initialize():  # pragma: no cover - requires live terminal
        code, message = mt5.last_error()
        raise RuntimeError(f"MT5 initialize failed: {code} {message}")

    try:
        if not mt5.symbol_select(symbol, True):
            code, message = mt5.last_error()
            raise RuntimeError(f"Cannot select symbol {symbol}: {code} {message}")

        rates: Any = mt5.copy_rates_range(
            symbol,
            mt5.TIMEFRAME_M1,
            start_utc,
            end_utc,
        )
        if rates is None:
            code, message = mt5.last_error()
            raise RuntimeError(f"MT5 copy_rates_range failed: {code} {message}")
        if len(rates) == 0:
            raise RuntimeError(
                "MT5 returned zero M1 bars. Check symbol name, login/history availability, and range."
            )

        frame = pd.DataFrame(rates)
        frame["timestamp"] = pd.to_datetime(frame["time"], unit="s", utc=True)
        frame = frame.rename(columns={"tick_volume": "volume"})

        columns = [
            "timestamp",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "spread",
            "real_volume",
        ]
        frame = frame[[column for column in columns if column in frame.columns]]
        frame = frame.sort_values("timestamp")
        frame = frame.drop_duplicates(subset=["timestamp"], keep="last")

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        frame.to_csv(output, index=False, date_format="%Y-%m-%dT%H:%M:%S%z")

        metadata_path = output.with_suffix(output.suffix + ".meta.json")
        result = Mt5ExportResult(
            symbol=symbol,
            timeframe="M1",
            start_utc=start_utc.isoformat(),
            end_utc=end_utc.isoformat(),
            rows=len(frame),
            csv_path=str(output),
            metadata_path=str(metadata_path),
        )
        metadata = {
            **asdict(result),
            "source": "MetaTrader5.copy_rates_range",
            "timestamp_timezone": "UTC",
            "purpose": "pipeline_resample_timezone_validation",
            "warning": "M1 bars only; not final Bid+Ask/tick execution-quality backtest data",
        }
        metadata_path.write_text(
            json.dumps(metadata, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return result
    finally:  # pragma: no cover - requires live terminal
        mt5.shutdown()
