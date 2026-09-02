from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

import pandas as pd

from nexus_xau.data.csv_loader import load_ohlc_csv
from nexus_xau.data.resample import resample_ohlc
from nexus_xau.engine.candles import CandleDirection


@dataclass(frozen=True, slots=True)
class TopologyHit:
    timeframe: str
    kind: str
    side: str
    window_start_utc: str
    window_end_utc: str


@dataclass(frozen=True, slots=True)
class TimeframeTopologySummary:
    timeframe: str
    bars: int
    pat2_windows_tested: int
    pat2_buy_color_candidates: int
    pat2_sell_color_candidates: int
    pat3_windows_tested: int
    pat3_buy_color_candidates: int
    pat3_sell_color_candidates: int


@dataclass(frozen=True, slots=True)
class PatTopologyResearchResult:
    source_csv: str
    start_utc: str
    end_utc: str
    summaries: tuple[TimeframeTopologySummary, ...]
    total_hits: int


def _direction(open_: float, close: float) -> CandleDirection:
    if close > open_:
        return CandleDirection.BULLISH
    if close < open_:
        return CandleDirection.BEARISH
    return CandleDirection.DOJI


def _iso(value: pd.Timestamp) -> str:
    return value.isoformat()


def _frames_from_m1(m1: pd.DataFrame) -> dict[str, pd.DataFrame]:
    return {
        "M1": m1,
        "M5": resample_ohlc(m1, "M5"),
        "H1": resample_ohlc(m1, "H1"),
        "H4": resample_ohlc(m1, "H4"),
        "D1": resample_ohlc(m1, "D1"),
    }


def scan_pat_color_topology(
    m1: pd.DataFrame,
) -> tuple[tuple[TimeframeTopologySummary, ...], tuple[TopologyHit, ...]]:
    """Scan confirmed PAT2/PAT3 candle-color topology only.

    This scanner intentionally does NOT check support/resistance location, the
    >50% close rule, PAT3 small-body geometry, PAT3 SELL equal-wick geometry, or
    any PAT1 wick/body threshold. Therefore every emitted row is a research-only
    color-topology candidate, never a valid PA/PAT signal.

    Overlapping windows are retained because project evidence explicitly allows
    PAT windows to overlap.
    """
    if m1.empty:
        raise ValueError("Dataset is empty")
    if not isinstance(m1.index, pd.DatetimeIndex) or m1.index.tz is None:
        raise ValueError("Input index must be timezone-aware")

    summaries: list[TimeframeTopologySummary] = []
    hits: list[TopologyHit] = []

    for timeframe, frame in _frames_from_m1(m1).items():
        directions = [
            _direction(float(row.open), float(row.close))
            for row in frame.itertuples()
        ]
        index = frame.index

        pat2_buy = 0
        pat2_sell = 0
        for i in range(1, len(frame)):
            pair = (directions[i - 1], directions[i])
            if pair == (CandleDirection.BEARISH, CandleDirection.BULLISH):
                pat2_buy += 1
                hits.append(
                    TopologyHit(
                        timeframe=timeframe,
                        kind="PAT2",
                        side="BUY",
                        window_start_utc=_iso(index[i - 1]),
                        window_end_utc=_iso(index[i]),
                    )
                )
            elif pair == (CandleDirection.BULLISH, CandleDirection.BEARISH):
                pat2_sell += 1
                hits.append(
                    TopologyHit(
                        timeframe=timeframe,
                        kind="PAT2",
                        side="SELL",
                        window_start_utc=_iso(index[i - 1]),
                        window_end_utc=_iso(index[i]),
                    )
                )

        pat3_buy = 0
        pat3_sell = 0
        for i in range(2, len(frame)):
            c1, c2, c3 = directions[i - 2], directions[i - 1], directions[i]
            if c2 is CandleDirection.DOJI:
                continue
            if c1 is CandleDirection.BEARISH and c3 is CandleDirection.BULLISH:
                pat3_buy += 1
                hits.append(
                    TopologyHit(
                        timeframe=timeframe,
                        kind="PAT3",
                        side="BUY",
                        window_start_utc=_iso(index[i - 2]),
                        window_end_utc=_iso(index[i]),
                    )
                )
            if c1 is CandleDirection.BULLISH and c3 is CandleDirection.BEARISH:
                pat3_sell += 1
                hits.append(
                    TopologyHit(
                        timeframe=timeframe,
                        kind="PAT3",
                        side="SELL",
                        window_start_utc=_iso(index[i - 2]),
                        window_end_utc=_iso(index[i]),
                    )
                )

        summaries.append(
            TimeframeTopologySummary(
                timeframe=timeframe,
                bars=len(frame),
                pat2_windows_tested=max(len(frame) - 1, 0),
                pat2_buy_color_candidates=pat2_buy,
                pat2_sell_color_candidates=pat2_sell,
                pat3_windows_tested=max(len(frame) - 2, 0),
                pat3_buy_color_candidates=pat3_buy,
                pat3_sell_color_candidates=pat3_sell,
            )
        )

    return tuple(summaries), tuple(hits)


def run_pat_topology_research(
    csv_path: str | Path,
    *,
    report_path: str | Path | None = None,
    hits_path: str | Path | None = None,
) -> PatTopologyResearchResult:
    m1 = load_ohlc_csv(csv_path)
    summaries, hits = scan_pat_color_topology(m1)

    result = PatTopologyResearchResult(
        source_csv=str(csv_path),
        start_utc=_iso(m1.index[0]),
        end_utc=_iso(m1.index[-1]),
        summaries=summaries,
        total_hits=len(hits),
    )

    if report_path is not None:
        target = Path(report_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            **asdict(result),
            "research_status": "COLOR_TOPOLOGY_ONLY_NOT_A_SIGNAL",
            "omitted_qualifiers": [
                "support_resistance_location",
                "PAT2_PAT3_50pct_measurement_basis_and_tolerance",
                "PAT3_small_body_threshold",
                "PAT3_SELL_equal_wick_tolerance",
                "PAT1_numeric_geometry",
            ],
            "overlap_policy": "retained",
        }
        target.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    if hits_path is not None:
        target = Path(hits_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame([asdict(hit) for hit in hits]).to_csv(target, index=False)

    return result
