from __future__ import annotations

from datetime import timedelta

import pandas as pd
import pytest

from nexus_xau.research.state_0700_dataset_v1 import (
    ProxyOrigin,
    ProxyPaEvent,
    _alignment_snapshot,
    _build_proxy_origins,
    _event_index,
    _favorable_consumed_points,
    _first_point_check_touch,
    _frame_relation,
    _latest_completed_snapshot,
    _point_check_cutoff_state,
    _proxy_pa_events,
)


def _ohlc(index: pd.DatetimeIndex, rows: list[tuple[float, float, float, float]]) -> pd.DataFrame:
    return pd.DataFrame(
        rows,
        columns=["open", "high", "low", "close"],
        index=index,
    )


def test_proxy_pa_event_known_only_after_pattern_bar_close() -> None:
    index = pd.date_range("2026-01-01T00:00:00Z", periods=2, freq="1h")
    frame = _ohlc(
        index,
        [
            (10.0, 10.5, 7.5, 8.0),
            (8.0, 10.0, 7.8, 9.5),
        ],
    )

    events = _proxy_pa_events(frame, "H1")

    assert len(events) == 1
    assert events[0].side == "BUY"
    assert events[0].known_at == pd.Timestamp("2026-01-01T02:00:00Z")
    assert events[0].pattern_low == pytest.approx(7.5)
    assert events[0].pattern_high == pytest.approx(10.5)


def test_proxy_pa_detector_does_not_bridge_gap() -> None:
    index = pd.DatetimeIndex(
        [
            pd.Timestamp("2026-01-01T00:00:00Z"),
            pd.Timestamp("2026-01-01T02:00:00Z"),
        ]
    )
    frame = _ohlc(
        index,
        [
            (10.0, 10.5, 7.5, 8.0),
            (8.0, 10.0, 7.8, 9.5),
        ],
    )

    assert _proxy_pa_events(frame, "H1") == []


def test_h4_origin_retains_source_supported_1500_run() -> None:
    index = pd.date_range("2026-01-01T00:00:00Z", periods=3, freq="4h")
    frame = _ohlc(
        index,
        [
            (10.0, 10.5, 7.5, 8.0),
            (8.0, 10.0, 7.8, 9.5),
            (9.5, 10.2, 9.0, 9.8),
        ],
    )
    events = _proxy_pa_events(frame, "H4")

    origins = _build_proxy_origins(frame, timeframe="H4", pa_events=events)

    assert len(origins) == 1
    assert origins[0].origin_known_at == pd.Timestamp("2026-01-01T12:00:00Z")
    assert origins[0].anchor_price == pytest.approx(9.0)
    assert origins[0].nominal_run_points == 1500.0


def test_d1_origin_preserves_unknown_run_distance() -> None:
    index = pd.date_range("2026-01-01T00:00:00Z", periods=3, freq="1D")
    frame = _ohlc(
        index,
        [
            (10.0, 10.5, 7.5, 8.0),
            (8.0, 10.0, 7.8, 9.5),
            (9.5, 10.2, 9.0, 9.8),
        ],
    )
    events = _proxy_pa_events(frame, "D1")

    origins = _build_proxy_origins(frame, timeframe="D1", pa_events=events)

    assert len(origins) == 1
    assert origins[0].nominal_run_points is None


def test_latest_completed_snapshot_never_uses_open_h4_bar() -> None:
    index = pd.date_range("2026-01-01T00:00:00Z", periods=3, freq="4h")
    frame = _ohlc(
        index,
        [
            (10.0, 11.0, 9.0, 10.5),
            (10.5, 12.0, 10.0, 11.0),
            (11.0, 99.0, 1.0, 50.0),
        ],
    )

    current, previous, start = _latest_completed_snapshot(
        frame,
        cutoff=pd.Timestamp("2026-01-01T08:00:00Z"),
        timeframe="H4",
    )

    assert start == pd.Timestamp("2026-01-01T04:00:00Z")
    assert current is not None
    assert previous is not None
    assert float(current.close) == pytest.approx(11.0)
    assert float(previous.close) == pytest.approx(10.5)


def test_consumed_points_excludes_cutoff_bar() -> None:
    index = pd.date_range("2026-01-01T00:00:00Z", periods=3, freq="1min")
    highs = pd.Series([101.0, 102.0, 110.0], index=index).to_numpy()
    lows = pd.Series([99.0, 99.5, 99.0], index=index).to_numpy()
    origin = ProxyOrigin(
        origin_id="H1:BUY:test",
        timeframe="H1",
        side="BUY",
        pattern_known_at=index[0],
        origin_known_at=index[0],
        anchor_price=100.0,
        nominal_run_points=1000.0,
    )

    consumed = _favorable_consumed_points(
        index=index,
        highs=highs,
        lows=lows,
        origin=origin,
        cutoff=index[2],
    )

    assert consumed == pytest.approx(200.0)


def test_frame_relation_preserves_snap_tie_ambiguity() -> None:
    event = ProxyPaEvent(
        timeframe="M5",
        side="BUY",
        previous_bar_start=pd.Timestamp("2026-01-01T00:00:00Z"),
        pattern_bar_start=pd.Timestamp("2026-01-01T00:05:00Z"),
        known_at=pd.Timestamp("2026-01-01T00:10:00Z"),
        close=100.0,
        pattern_low=99.0,
        pattern_high=101.0,
    )
    day = pd.Series(
        {
            "daily_frame_tie_ambiguous": True,
            "daily_frame_lower": None,
            "daily_frame_upper": None,
        }
    )

    state, distance = _frame_relation(event=event, day_row=day)

    assert state == "AMBIGUOUS_FRAME_TIE"
    assert distance is None


def test_alignment_keeps_exact_and_recent_as_separate_variants() -> None:
    anchor = pd.Timestamp("2026-01-01T12:00:00Z")
    events = {
        "H1": [
            ProxyPaEvent(
                "H1",
                "BUY",
                anchor - timedelta(hours=2),
                anchor - timedelta(hours=1),
                anchor,
                100.0,
                99.0,
                101.0,
            )
        ],
        "M30": [
            ProxyPaEvent(
                "M30",
                "BUY",
                anchor - timedelta(hours=1),
                anchor - timedelta(minutes=30),
                anchor - timedelta(minutes=30),
                100.0,
                99.0,
                101.0,
            )
        ],
        "M15": [],
        "M5": [],
    }
    indexed = {tf: _event_index(rows) for tf, rows in events.items()}

    exact_count, exact_tfs = _alignment_snapshot(
        anchor_side="BUY",
        anchor_known_at=anchor,
        indexed_events=indexed,
        lookback_bars=0,
    )
    recent_count, recent_tfs = _alignment_snapshot(
        anchor_side="BUY",
        anchor_known_at=anchor,
        indexed_events=indexed,
        lookback_bars=1,
    )

    assert exact_count == 1
    assert exact_tfs == ("H1",)
    assert recent_count == 2
    assert recent_tfs == ("H1", "M30")


def test_first_point_check_touch_is_found_without_using_cutoff_logic() -> None:
    index = pd.date_range("2026-01-01T00:00:00Z", periods=4, freq="1min")
    highs = pd.Series([101.0, 100.5, 101.5, 102.0], index=index).to_numpy()
    lows = pd.Series([100.2, 99.8, 100.1, 100.5], index=index).to_numpy()
    origin = ProxyOrigin(
        origin_id="H1:BUY:touch",
        timeframe="H1",
        side="BUY",
        pattern_known_at=index[0],
        origin_known_at=index[0],
        anchor_price=100.0,
        nominal_run_points=1000.0,
    )

    first_touch = _first_point_check_touch(
        index=index,
        highs=highs,
        lows=lows,
        origin=origin,
    )

    assert first_touch == index[1]


def test_point_check_cutoff_state_hides_future_touch() -> None:
    cutoff = pd.Timestamp("2026-01-02T00:00:00Z")

    state, survives, visible = _point_check_cutoff_state(
        first_touch_at=pd.Timestamp("2026-01-02T03:00:00Z"),
        cutoff=cutoff,
    )

    assert state == "UNTOUCHED_BEFORE_0700"
    assert survives is True
    assert visible is None


def test_point_check_cutoff_state_exposes_only_past_touch() -> None:
    cutoff = pd.Timestamp("2026-01-02T00:00:00Z")
    touch = pd.Timestamp("2026-01-01T23:00:00Z")

    state, survives, visible = _point_check_cutoff_state(
        first_touch_at=touch,
        cutoff=cutoff,
    )

    assert state == "TOUCHED_BEFORE_0700"
    assert survives is False
    assert visible == touch
