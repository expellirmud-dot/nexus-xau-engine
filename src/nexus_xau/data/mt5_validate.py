from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from nexus_xau.data.csv_loader import load_ohlc_csv
from nexus_xau.data.resample import resample_ohlc


@dataclass(frozen=True)
class TimeframeComparison:
    timeframe: str
    local_bars: int
    mt5_bars: int
    common_timestamps: int
    only_local_timestamps: int
    only_mt5_timestamps: int
    ohlc_mismatch_rows: int
    max_abs_ohlc_diff: float


@dataclass(frozen=True)
class Mt5ResampleValidation:
    symbol: str
    start_utc: str
    end_utc: str
    comparisons: tuple[TimeframeComparison, ...]


def compare_ohlc_frames(
    local: pd.DataFrame,
    reference: pd.DataFrame,
    *,
    timeframe: str,
    tolerance: float = 1e-9,
) -> TimeframeComparison:
    """Compare local OHLC bars to a reference on matching timestamps."""
    columns = ["open", "high", "low", "close"]
    for name, frame in (("local", local), ("reference", reference)):
        if not isinstance(frame.index, pd.DatetimeIndex) or frame.index.tz is None:
            raise ValueError(f"{name} index must be timezone-aware")
        missing = [column for column in columns if column not in frame.columns]
        if missing:
            raise ValueError(f"{name} missing OHLC columns: {missing}")

    local_idx = local.index
    ref_idx = reference.index
    common = local_idx.intersection(ref_idx)

    if len(common):
        diff = (
            local.loc[common, columns].astype(float)
            - reference.loc[common, columns].astype(float)
        ).abs()
        mismatch = (diff > tolerance).any(axis=1)
        mismatch_rows = int(mismatch.sum())
        max_abs_diff = float(diff.to_numpy().max())
    else:
        mismatch_rows = 0
        max_abs_diff = 0.0

    return TimeframeComparison(
        timeframe=timeframe,
        local_bars=len(local),
        mt5_bars=len(reference),
        common_timestamps=len(common),
        only_local_timestamps=len(local_idx.difference(ref_idx)),
        only_mt5_timestamps=len(ref_idx.difference(local_idx)),
        ohlc_mismatch_rows=mismatch_rows,
        max_abs_ohlc_diff=max_abs_diff,
    )


def _rates_to_frame(rates: Any) -> pd.DataFrame:
    frame = pd.DataFrame(rates)
    frame["timestamp"] = pd.to_datetime(frame["time"], unit="s", utc=True)
    frame = frame.rename(columns={"tick_volume": "volume"})
    keep = [c for c in ("timestamp", "open", "high", "low", "close", "volume") if c in frame]
    frame = frame[keep].sort_values("timestamp").drop_duplicates("timestamp", keep="last")
    return frame.set_index("timestamp")


def validate_resample_against_mt5(
    csv_path: str | Path,
    *,
    symbol: str,
    report_path: str | Path | None = None,
    tolerance: float = 1e-9,
) -> Mt5ResampleValidation:
    """Compare UTC local M1->M5/H1/H4/D1 resampling with MT5 native bars.

    This is specifically a boundary/timezone validation step. A mismatch is not
    automatically a data error: if timestamps differ systematically, it can reveal
    broker/server timeframe alignment that must be modeled explicitly.
    """
    m1 = load_ohlc_csv(csv_path)
    if m1.empty:
        raise ValueError("Dataset is empty")

    try:
        import MetaTrader5 as mt5
    except ImportError as exc:  # pragma: no cover - Windows/MT5 dependent
        raise RuntimeError(
            'MetaTrader5 package is not installed. Run: pip install -e ".[dev,mt5]"'
        ) from exc

    if not mt5.initialize():  # pragma: no cover - live terminal required
        code, message = mt5.last_error()
        raise RuntimeError(f"MT5 initialize failed: {code} {message}")

    try:  # pragma: no cover - live terminal required
        if not mt5.symbol_select(symbol, True):
            code, message = mt5.last_error()
            raise RuntimeError(f"Cannot select symbol {symbol}: {code} {message}")

        start = m1.index[0].to_pydatetime()
        end = m1.index[-1].to_pydatetime()
        tf_map = {
            "M5": mt5.TIMEFRAME_M5,
            "H1": mt5.TIMEFRAME_H1,
            "H4": mt5.TIMEFRAME_H4,
            "D1": mt5.TIMEFRAME_D1,
        }
        comparisons: list[TimeframeComparison] = []

        for timeframe, mt5_tf in tf_map.items():
            local = resample_ohlc(m1, timeframe)
            rates = mt5.copy_rates_range(symbol, mt5_tf, start, end)
            if rates is None:
                code, message = mt5.last_error()
                raise RuntimeError(
                    f"MT5 copy_rates_range failed for {timeframe}: {code} {message}"
                )
            reference = _rates_to_frame(rates)
            comparisons.append(
                compare_ohlc_frames(
                    local,
                    reference,
                    timeframe=timeframe,
                    tolerance=tolerance,
                )
            )

        result = Mt5ResampleValidation(
            symbol=symbol,
            start_utc=m1.index[0].isoformat(),
            end_utc=m1.index[-1].isoformat(),
            comparisons=tuple(comparisons),
        )

        if report_path is not None:
            target = Path(report_path)
            target.parent.mkdir(parents=True, exist_ok=True)
            payload = {
                "symbol": result.symbol,
                "start_utc": result.start_utc,
                "end_utc": result.end_utc,
                "comparisons": [asdict(item) for item in result.comparisons],
                "purpose": "validate_M1_resample_boundaries_against_MT5_native_timeframes",
            }
            target.write_text(
                json.dumps(payload, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )

        return result
    finally:  # pragma: no cover - live terminal required
        mt5.shutdown()
