from __future__ import annotations

import hashlib

import pandas as pd
import pytest

from nexus_xau.research.minimal_v2_0700 import (
    TARGET_MODE_FIXED_ORIGIN_V2_1,
    TARGET_MODE_PATH_REMAINING_V2_0,
    H4Origin,
    _build_minimal_v2_core,
    _candidate_target_price,
    _normalize_m1_frame,
    build_minimal_v2_from_frame,
    fixed_origin_target_price,
)
from nexus_xau.research.minimal_v21_0700 import (
    build_minimal_v21,
    build_minimal_v21_from_frame,
)


def _expand_h4_bar(
    start: str,
    *,
    open_price: float,
    high_price: float,
    low_price: float,
    close_price: float,
) -> pd.DataFrame:
    index = pd.date_range(start, periods=240, freq="1min")
    prices = [
        open_price + (close_price - open_price) * i / 239.0
        for i in range(240)
    ]
    prices[60] = high_price
    prices[120] = low_price
    prices[-1] = close_price
    return pd.DataFrame(
        {"open": prices, "high": prices, "low": prices, "close": prices},
        index=index,
    )


def _synthetic_m1() -> pd.DataFrame:
    specs = [
        ("2026-01-01T00:00:00Z", 110.0, 112.0, 99.0, 100.0),
        ("2026-01-01T04:00:00Z", 100.0, 112.0, 100.0, 108.0),
        ("2026-01-01T08:00:00Z", 108.0, 111.0, 101.0, 109.0),
        ("2026-01-01T12:00:00Z", 109.0, 113.0, 108.0, 112.0),
        ("2026-01-01T16:00:00Z", 112.0, 113.0, 108.0, 109.0),
        ("2026-01-01T20:00:00Z", 109.0, 114.0, 108.0, 112.0),
        ("2026-01-02T00:00:00Z", 112.0, 114.0, 109.0, 113.0),
        ("2026-01-02T04:00:00Z", 113.0, 115.0, 110.0, 114.0),
        ("2026-01-02T08:00:00Z", 114.0, 116.2, 111.0, 115.0),
        ("2026-01-02T12:00:00Z", 115.0, 117.0, 112.0, 116.0),
        ("2026-01-02T16:00:00Z", 116.0, 118.0, 113.0, 117.0),
        ("2026-01-02T20:00:00Z", 117.0, 119.0, 114.0, 118.0),
        ("2026-01-03T00:00:00Z", 118.0, 120.0, 115.0, 119.0),
    ]
    return pd.concat(
        [
            _expand_h4_bar(
                start,
                open_price=open_price,
                high_price=high_price,
                low_price=low_price,
                close_price=close_price,
            )
            for start, open_price, high_price, low_price, close_price in specs
        ]
    ).sort_index()


def _with_retraced_m5_buy(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    before = pd.date_range("2026-01-01T23:55:00Z", periods=5, freq="1min")
    after = pd.date_range("2026-01-02T00:00:00Z", periods=5, freq="1min")
    before_prices = [114.0, 113.5, 113.0, 112.5, 112.0]
    # Bullish M5 closes above prior full-range midpoint 113.0, but its intrabar
    # high reaches 114.1 before closing back at 113.5. This creates a deliberate
    # distinction between consumed MFE and confirmation-to-fixed-target distance.
    after_prices = [112.0, 114.1, 113.8, 113.6, 113.5]
    for index, prices in ((before, before_prices), (after, after_prices)):
        for timestamp, price in zip(index, prices, strict=True):
            out.loc[timestamp, ["open", "high", "low", "close"]] = price
    return out


def _candidate_row(frame: pd.DataFrame) -> pd.Series:
    _, _, events, report = build_minimal_v21_from_frame(
        m1=frame,
        source_descriptor="SYNTHETIC:V21",
    )
    assert report["version"] == "0700_MINIMAL_V2.1_FIXED_ORIGIN_TARGET"
    rows = events.loc[
        (events["candidate_state"] == "RESEARCH_CANDIDATE")
        & (events["side"] == "BUY")
    ]
    assert len(rows) == 1
    return rows.iloc[0]


def test_buy_fixed_origin_target_is_anchor_plus_1500_points() -> None:
    assert fixed_origin_target_price(side="BUY", anchor_price=101.0) == 116.0


def test_sell_fixed_origin_target_is_anchor_minus_1500_points() -> None:
    assert fixed_origin_target_price(side="SELL", anchor_price=120.0) == 105.0


def test_fixed_target_is_invariant_to_confirmation_close() -> None:
    ts = pd.Timestamp("2026-01-01T00:00:00Z")
    origin = H4Origin("H4:BUY:FIXED", "BUY", ts, ts, 101.0)

    first = _candidate_target_price(
        target_mode=TARGET_MODE_FIXED_ORIGIN_V2_1,
        origin=origin,
        confirmation_close=113.5,
        remaining_points=190.0,
    )
    second = _candidate_target_price(
        target_mode=TARGET_MODE_FIXED_ORIGIN_V2_1,
        origin=origin,
        confirmation_close=109.0,
        remaining_points=700.0,
    )

    assert first == 116.0
    assert second == 116.0


def test_retracement_separates_remaining_progress_from_entry_to_fixed_target() -> None:
    row = _candidate_row(_with_retraced_m5_buy(_synthetic_m1()))

    assert float(row["origin_anchor_price"]) == 101.0
    assert float(row["fixed_origin_target_price"]) == 116.0
    assert float(row["consumed_points_at_confirmation"]) == pytest.approx(1310.0)
    assert float(row["remaining_points_at_confirmation"]) == pytest.approx(190.0)
    assert float(row["confirmation_close"]) == 113.5
    assert float(row["confirmation_to_fixed_target_points"]) == 250.0
    assert (
        float(row["remaining_points_at_confirmation"])
        != float(row["confirmation_to_fixed_target_points"])
    )


def test_v21_does_not_reset_fresh_1500_point_target_from_confirmation() -> None:
    row = _candidate_row(_with_retraced_m5_buy(_synthetic_m1()))
    fresh_target = float(row["confirmation_close"]) + 15.0

    assert float(row["fixed_origin_target_price"]) == 116.0
    assert float(row["fixed_origin_target_price"]) != fresh_target
    assert row["target_representation"] == TARGET_MODE_FIXED_ORIGIN_V2_1


def test_v21_target_first_uses_fixed_origin_boundary() -> None:
    row = _candidate_row(_with_retraced_m5_buy(_synthetic_m1()))

    assert row["fixed_origin_first_hit"] == "TARGET_FIRST"
    assert pd.Timestamp(row["fixed_origin_target_at"]) == pd.Timestamp(
        "2026-01-02T09:00:00Z"
    )


def test_v21_point_check_first_uses_existing_literal_anchor_contact() -> None:
    frame = _with_retraced_m5_buy(_synthetic_m1())
    touch = pd.Timestamp("2026-01-02T00:30:00Z")
    frame.loc[touch, ["open", "high", "low", "close"]] = [105.0, 110.0, 101.0, 105.0]

    row = _candidate_row(frame)

    assert row["fixed_origin_first_hit"] == "POINT_CHECK_FIRST"
    assert pd.Timestamp(row["fixed_origin_point_check_at"]) == touch
    assert pd.Timestamp(row["fixed_origin_target_at"]) > touch


def test_v21_same_bar_target_and_point_check_remains_ambiguous() -> None:
    frame = _with_retraced_m5_buy(_synthetic_m1())
    both = pd.Timestamp("2026-01-02T00:30:00Z")
    frame.loc[both, ["open", "high", "low", "close"]] = [110.0, 116.0, 101.0, 110.0]

    row = _candidate_row(frame)

    assert row["fixed_origin_first_hit"] == "AMBIGUOUS_SAME_BAR"
    assert pd.Timestamp(row["fixed_origin_target_at"]) == both
    assert pd.Timestamp(row["fixed_origin_point_check_at"]) == both


def test_multiple_origins_keep_independent_fixed_targets() -> None:
    ts = pd.Timestamp("2026-01-01T00:00:00Z")
    origins = [
        H4Origin("BUY:A", "BUY", ts, ts, 101.0),
        H4Origin("BUY:B", "BUY", ts, ts, 103.0),
        H4Origin("SELL:A", "SELL", ts, ts, 120.0),
    ]

    targets = {
        origin.origin_id: fixed_origin_target_price(
            side=origin.side,
            anchor_price=origin.anchor_price,
        )
        for origin in origins
    }

    assert targets == {"BUY:A": 116.0, "BUY:B": 118.0, "SELL:A": 105.0}


def test_v2_default_mode_remains_path_remaining_and_has_no_v21_fields() -> None:
    frame = _with_retraced_m5_buy(_synthetic_m1())
    default = build_minimal_v2_from_frame(
        m1=frame,
        source_descriptor="SYNTHETIC:DEFAULT-V2",
    )

    normalized = _normalize_m1_frame(frame)
    explicit = _build_minimal_v2_core(
        active_m1=normalized,
        source_descriptor="SYNTHETIC:DEFAULT-V2",
        source_metadata_descriptor=None,
        source_sha256=None,
        candidate_target_mode=TARGET_MODE_PATH_REMAINING_V2_0,
    )

    for actual, expected in zip(default[:3], explicit[:3], strict=True):
        pd.testing.assert_frame_equal(actual, expected)
    assert default[3] == explicit[3]
    assert default[3]["version"] == "0700_MINIMAL_V2.0"

    events = default[2]
    assert "path_remaining_target_price" in events.columns
    assert "fixed_origin_target_price" not in events.columns
    assert "target_representation" not in events.columns


def test_v21_schema_uses_fixed_origin_fields_not_path_remaining_target() -> None:
    frame = _with_retraced_m5_buy(_synthetic_m1())
    _, _, events, report = build_minimal_v21_from_frame(
        m1=frame,
        source_descriptor="SYNTHETIC:V21-SCHEMA",
    )

    assert report["candidate_target_representation"] == TARGET_MODE_FIXED_ORIGIN_V2_1
    assert "fixed_origin_target_price" in events.columns
    assert "confirmation_to_fixed_target_points" in events.columns
    assert "fixed_origin_first_hit" in events.columns
    assert "path_remaining_target_price" not in events.columns


def test_v21_file_and_frame_entry_points_are_identical(tmp_path) -> None:
    frame = _with_retraced_m5_buy(_synthetic_m1())
    path = tmp_path / "m1.csv"
    frame.reset_index(names="timestamp").to_csv(path, index=False)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()

    file_result = build_minimal_v21(m1_path=path)
    frame_result = build_minimal_v21_from_frame(
        m1=frame,
        source_descriptor=str(path),
        source_sha256=digest,
    )

    for actual, expected in zip(file_result[:3], frame_result[:3], strict=True):
        pd.testing.assert_frame_equal(actual, expected)
    assert file_result[3] == frame_result[3]


def test_v21_does_not_add_economic_or_execution_fields() -> None:
    frame = _with_retraced_m5_buy(_synthetic_m1())
    days, origins, events, report = build_minimal_v21_from_frame(
        m1=frame,
        source_descriptor="SYNTHETIC:V21-GUARDS",
    )
    forbidden_tokens = (
        "pnl",
        "p&l",
        "win_rate",
        "win rate",
        "expectancy",
        "profitability",
        "broker_fill",
        "broker-fill",
        "slippage",
        "order_send",
        "order-send",
    )

    names: list[str] = []
    names.extend(str(key).lower() for key in report)
    for output in (days, origins, events):
        names.extend(str(column).lower() for column in output.columns)

    assert not [
        name
        for name in names
        if any(token in name for token in forbidden_tokens)
    ]
