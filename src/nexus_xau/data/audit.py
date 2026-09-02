from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

import pandas as pd

from nexus_xau.data.csv_loader import load_ohlc_csv
from nexus_xau.data.resample import resample_ohlc


@dataclass(frozen=True)
class GapRecord:
    previous_utc: str
    next_utc: str
    gap_seconds: float
    missing_m1_slots: int


@dataclass(frozen=True)
class DatasetAudit:
    rows: int
    start_utc: str
    end_utc: str
    span_seconds: float
    one_minute_steps: int
    gaps_over_one_minute: int
    largest_gap_seconds: float
    gap_records: tuple[GapRecord, ...]
    m5_bars: int
    h1_bars: int
    h4_bars: int
    d1_bars: int


def _iso(ts: pd.Timestamp) -> str:
    return ts.isoformat()


def audit_ohlc_csv(
    path: str | Path,
    *,
    processed_dir: str | Path | None = None,
    report_path: str | Path | None = None,
) -> DatasetAudit:
    """Audit a normalized OHLC CSV and optionally write resampled outputs.

    Gaps are reported, not automatically treated as errors. XAUUSD data can have
    broker/session/weekend pauses; the purpose here is to make them visible before
    detector work begins.
    """
    frame = load_ohlc_csv(path)
    if frame.empty:
        raise ValueError("Dataset is empty")

    deltas = frame.index.to_series().diff().dropna()
    one_minute = pd.Timedelta(60, unit="s")
    gap_mask = deltas > one_minute

    gap_records: list[GapRecord] = []
    for next_ts, delta in deltas[gap_mask].items():
        previous_ts = next_ts - delta
        gap_seconds = float(delta.total_seconds())
        gap_records.append(
            GapRecord(
                previous_utc=_iso(previous_ts),
                next_utc=_iso(next_ts),
                gap_seconds=gap_seconds,
                missing_m1_slots=max(int(gap_seconds // 60) - 1, 0),
            )
        )

    m5 = resample_ohlc(frame, "M5")
    h1 = resample_ohlc(frame, "H1")
    h4 = resample_ohlc(frame, "H4")
    d1 = resample_ohlc(frame, "D1")

    audit = DatasetAudit(
        rows=len(frame),
        start_utc=_iso(frame.index[0]),
        end_utc=_iso(frame.index[-1]),
        span_seconds=float((frame.index[-1] - frame.index[0]).total_seconds()),
        one_minute_steps=int((deltas == one_minute).sum()),
        gaps_over_one_minute=len(gap_records),
        largest_gap_seconds=(
            float(deltas.max().total_seconds()) if not deltas.empty else 0.0
        ),
        gap_records=tuple(gap_records),
        m5_bars=len(m5),
        h1_bars=len(h1),
        h4_bars=len(h4),
        d1_bars=len(d1),
    )

    if processed_dir is not None:
        target = Path(processed_dir)
        target.mkdir(parents=True, exist_ok=True)
        stem = Path(path).stem
        for timeframe, data in (("M5", m5), ("H1", h1), ("H4", h4), ("D1", d1)):
            out = data.reset_index()
            out.to_csv(target / f"{stem}_{timeframe}.csv", index=False)

    if report_path is not None:
        report = Path(report_path)
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(
            json.dumps(asdict(audit), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    return audit
