from __future__ import annotations

import pandas as pd

from nexus_xau.research.minimal_v2_0700 import (
    H4Origin,
    Pat2Event,
    _day_frame_row,
    _first_m5_confirmation,
    action_state_for_candidate,
    boundary_hit,
    detect_pat2_full_range,
    first_point_check_touch,
    origin_state_at,
)


def _frame(rows: list[tuple[float, float, float, float]], *, freq: str) -> pd.DataFrame:
    index = pd.date_range("2026-01-01T00:00:00Z", periods=len(rows), freq=freq)
    return pd.DataFrame(rows, columns=["open", "high", "low", "close"], index=index)


def _m1(
    rows: list[tuple[float, float, float, float]], *, start: str = "2026-01-01T00:00:00Z"
) -> pd.DataFrame:
    index = pd.date_range(start, periods=len(rows), freq="1min")
    return pd.DataFrame(rows, columns=["open", "high", "low", "close"], index=index)


def _origin(side: str = "BUY", anchor: float = 100.0) -> H4Origin:
    ts = pd.Timestamp("2026-01-01T00:00:00Z")
    return H4Origin(
        origin_id=f"H4:{side}:TEST",
        side=side,
        pattern_known_at=ts,
        origin_known_at=ts,
        anchor_price=anchor,
    )


def test_pat2_buy_strict_full_range_midpoint_pass() -> None:
    frame = _frame(
        [
            (110.0, 130.0, 90.0, 100.0),
            (100.0, 116.0, 99.0, 111.0),
        ],
        freq="4h",
    )
    events = detect_pat2_full_range(frame, "H4")
    assert [event.side for event in events] == ["BUY"]


def test_pat2_buy_equality_at_midpoint_fails() -> None:
    frame = _frame(
        [
            (110.0, 130.0, 90.0, 100.0),
            (100.0, 112.0, 99.0, 110.0),
        ],
        freq="4h",
    )
    assert detect_pat2_full_range(frame, "H4") == []


def test_pat2_sell_strict_full_range_midpoint_pass() -> None:
    frame = _frame(
        [
            (100.0, 130.0, 90.0, 120.0),
            (120.0, 121.0, 99.0, 109.0),
        ],
        freq="4h",
    )
    events = detect_pat2_full_range(frame, "H4")
    assert [event.side for event in events] == ["SELL"]


def test_body_midpoint_can_pass_while_full_range_midpoint_fails() -> None:
    # Previous bearish body midpoint = 105, full-range midpoint = 110.
    frame = _frame(
        [
            (110.0, 130.0, 90.0, 100.0),
            (100.0, 108.0, 99.0, 107.0),
        ],
        freq="4h",
    )
    assert 107.0 > (110.0 + 100.0) / 2.0
    assert 107.0 < (130.0 + 90.0) / 2.0
    assert detect_pat2_full_range(frame, "H4") == []


def test_point_check_exact_touch_is_detected() -> None:
    frame = _m1([(101.0, 101.5, 100.0, 101.0)])
    touch = first_point_check_touch(
        active_m1=frame,
        anchor=100.0,
        start=frame.index[0],
        end=frame.index[0] + pd.Timedelta(minutes=1),
    )
    assert touch == frame.index[0]


def test_point_check_one_project_point_near_miss_survives() -> None:
    frame = _m1([(101.0, 101.5, 100.01, 101.0)])
    touch = first_point_check_touch(
        active_m1=frame,
        anchor=100.0,
        start=frame.index[0],
        end=frame.index[0] + pd.Timedelta(minutes=1),
    )
    assert touch is None


def test_origin_target_first_marks_run_complete() -> None:
    frame = _m1(
        [
            (101.0, 114.0, 100.1, 113.0),
            (113.0, 115.0, 112.0, 114.0),
        ]
    )
    state, consumed, remaining, _ = origin_state_at(
        active_m1=frame,
        origin=_origin(),
        at=frame.index[-1] + pd.Timedelta(minutes=1),
    )
    assert state == "RUN_COMPLETE"
    assert consumed >= 1500.0
    assert remaining == 0.0


def test_origin_point_check_first_marks_destroyed() -> None:
    frame = _m1(
        [
            (101.0, 102.0, 100.0, 101.0),
            (101.0, 116.0, 101.0, 115.0),
        ]
    )
    state, _, _, touch = origin_state_at(
        active_m1=frame,
        origin=_origin(),
        at=frame.index[-1] + pd.Timedelta(minutes=1),
    )
    assert state == "POINT_CHECK_DESTROYED"
    assert touch == frame.index[0]


def test_origin_run_completion_before_confirmation_is_terminal() -> None:
    frame = _m1(
        [
            (101.0, 114.0, 100.1, 113.0),
            (113.0, 115.1, 112.0, 115.0),
            (115.0, 116.0, 114.0, 115.0),
        ]
    )
    confirmation = frame.index[2]
    state, _, _, _ = origin_state_at(
        active_m1=frame,
        origin=_origin(),
        at=confirmation,
    )
    assert state == "RUN_COMPLETE"


def test_origin_destruction_before_confirmation_is_terminal() -> None:
    frame = _m1(
        [
            (101.0, 102.0, 100.0, 101.0),
            (101.0, 102.0, 100.5, 101.5),
            (101.5, 103.0, 101.0, 102.0),
        ]
    )
    confirmation = frame.index[2]
    state, _, _, touch = origin_state_at(
        active_m1=frame,
        origin=_origin(),
        at=confirmation,
    )
    assert state == "POINT_CHECK_DESTROYED"
    assert touch == frame.index[0]


def test_daily_frame_exact_half_step_is_tie_and_fail_closed_input() -> None:
    frame = _m1([(1002.5, 1002.6, 1002.4, 1002.5)])
    row = _day_frame_row(cutoff=frame.index[0], active_m1=frame)
    assert row["daily_frame_candidate_count"] == 2
    assert row["daily_frame_tie_ambiguous"] is True


def test_pre_0700_state_excludes_bar_starting_at_cutoff() -> None:
    frame = _m1(
        [
            (101.0, 102.0, 100.5, 101.0),
            (101.0, 102.0, 100.0, 101.0),
        ],
        start="2026-01-01T23:59:00Z",
    )
    cutoff = pd.Timestamp("2026-01-02T00:00:00Z")
    origin = H4Origin(
        origin_id="H4:BUY:NO_LOOKAHEAD",
        side="BUY",
        pattern_known_at=frame.index[0],
        origin_known_at=frame.index[0],
        anchor_price=100.0,
    )
    state, _, _, touch = origin_state_at(
        active_m1=frame,
        origin=origin,
        at=cutoff,
    )
    assert state == "ACTIVE"
    assert touch is None


def test_same_bar_target_and_point_check_is_ambiguous() -> None:
    frame = _m1([(105.0, 115.0, 100.0, 110.0)])
    hit = boundary_hit(
        path=frame,
        side="BUY",
        target_price=115.0,
        point_check_price=100.0,
    )
    assert hit.first_hit == "AMBIGUOUS_SAME_BAR"


def test_multiple_origins_fail_closed_for_action_lane() -> None:
    assert (
        action_state_for_candidate(
            same_side_origin_count=2,
            opposite_side_origin_count=0,
        )
        == "PASS_CONFLICT_UNRESOLVED"
    )
    assert (
        action_state_for_candidate(
            same_side_origin_count=1,
            opposite_side_origin_count=1,
        )
        == "PASS_CONFLICT_UNRESOLVED"
    )


def test_single_research_candidate_still_fails_closed_on_location_geometry() -> None:
    assert (
        action_state_for_candidate(
            same_side_origin_count=1,
            opposite_side_origin_count=0,
        )
        == "PASS_SOURCE_GEOMETRY_UNRESOLVED"
    )


def test_first_m5_confirmation_is_strictly_after_cutoff_and_before_next_cutoff() -> None:
    cutoff = pd.Timestamp("2026-01-01T00:00:00Z")
    next_cutoff = cutoff + pd.Timedelta(days=1)
    events = [
        Pat2Event(
            timeframe="M5",
            side="BUY",
            previous_bar_start=cutoff - pd.Timedelta(minutes=10),
            pattern_bar_start=cutoff - pd.Timedelta(minutes=5),
            known_at=cutoff,
            close=100.0,
            pattern_low=99.0,
            pattern_high=101.0,
        ),
        Pat2Event(
            timeframe="M5",
            side="BUY",
            previous_bar_start=cutoff,
            pattern_bar_start=cutoff + pd.Timedelta(minutes=5),
            known_at=cutoff + pd.Timedelta(minutes=10),
            close=101.0,
            pattern_low=100.0,
            pattern_high=102.0,
        ),
    ]
    selected = _first_m5_confirmation(
        events=events,
        side="BUY",
        cutoff=cutoff,
        next_cutoff=next_cutoff,
    )
    assert selected is not None
    assert selected.known_at == cutoff + pd.Timedelta(minutes=10)
