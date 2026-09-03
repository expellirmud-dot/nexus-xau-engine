from __future__ import annotations

import pandas as pd

from nexus_xau.research.mtf_alignment_variant_relation_test import (
    Pat2BodyEvent,
    _alignment_count,
    _event_index,
    _pat2_body_events,
    _safe_spearman,
)


def test_pat2_body_detector_marks_known_at_after_bar_close() -> None:
    index = pd.date_range("2026-01-01T00:00:00Z", periods=2, freq="1h")
    frame = pd.DataFrame(
        {
            "open": [10.0, 8.0],
            "high": [10.5, 10.0],
            "low": [7.5, 7.8],
            "close": [8.0, 9.5],
        },
        index=index,
    )
    events = _pat2_body_events(frame, "H1")
    assert len(events) == 1
    assert events[0].side == "BUY"
    assert events[0].known_at == pd.Timestamp("2026-01-01T02:00:00Z")


def test_pat2_body_detector_does_not_bridge_time_gap() -> None:
    index = pd.DatetimeIndex(
        [pd.Timestamp("2026-01-01T00:00:00Z"), pd.Timestamp("2026-01-01T02:00:00Z")]
    )
    frame = pd.DataFrame(
        {
            "open": [10.0, 8.0],
            "high": [10.5, 10.0],
            "low": [7.5, 7.8],
            "close": [8.0, 9.5],
        },
        index=index,
    )
    assert _pat2_body_events(frame, "H1") == []


def test_alignment_uses_latest_event_and_freshness_window() -> None:
    anchor = pd.Timestamp("2026-01-01T12:00:00Z")
    events = {
        "H1": [Pat2BodyEvent("H1", "BUY", anchor - pd.Timedelta("1h"), anchor, 100.0)],
        "M30": [
            Pat2BodyEvent(
                "M30",
                "BUY",
                anchor - pd.Timedelta("1h"),
                anchor - pd.Timedelta("30min"),
                99.0,
            )
        ],
        "M15": [
            Pat2BodyEvent(
                "M15",
                "SELL",
                anchor - pd.Timedelta("15min"),
                anchor,
                101.0,
            )
        ],
        "M5": [
            Pat2BodyEvent(
                "M5",
                "BUY",
                anchor - pd.Timedelta("5min"),
                anchor,
                100.0,
            )
        ],
    }
    indexed = {timeframe: _event_index(rows) for timeframe, rows in events.items()}

    exact_count, exact_tfs = _alignment_count(
        anchor_side="BUY",
        anchor_known_at=anchor,
        indexed_events=indexed,
        lookback_bars=0,
    )
    assert exact_count == 2
    assert exact_tfs == ("H1", "M5")

    recent_count, recent_tfs = _alignment_count(
        anchor_side="BUY",
        anchor_known_at=anchor,
        indexed_events=indexed,
        lookback_bars=1,
    )
    assert recent_count == 3
    assert recent_tfs == ("H1", "M30", "M5")


def test_safe_spearman_uses_rank_correlation_without_scipy() -> None:
    frame = pd.DataFrame({"x": [1, 2, 3, 4], "y": [10, 20, 30, 40]})
    assert _safe_spearman(frame, "x", "y") == 1.0
