from __future__ import annotations

from datetime import timedelta

import numpy as np
import pandas as pd

from nexus_xau.replay.prehistory_forward_closure import (
    HYPOTHESIS,
    construct_surviving_counterexamples,
    evaluate_finite_forward_closure,
)
from nexus_xau.research.minimal_v2_0700 import (
    H4_RUN_POINTS,
    PROJECT_POINT_SIZE,
    build_h4_origins,
    detect_pat2_full_range,
    origin_state_at,
)


def _finite_path(*, extension: bool = False) -> pd.DataFrame:
    index = pd.date_range("2026-01-01T00:00:00Z", periods=12, freq="1min")
    base = np.linspace(1900.0, 1904.0, len(index))
    frame = pd.DataFrame(
        {
            "open": base,
            "high": base + 0.5,
            "low": base - 0.5,
            "close": base + 0.1,
            "volume": 1.0,
        },
        index=index,
    )
    if extension:
        later_index = pd.date_range(index[-1] + timedelta(minutes=1), periods=8, freq="1min")
        later_base = np.linspace(1890.0, 1915.0, len(later_index))
        later = pd.DataFrame(
            {
                "open": later_base,
                "high": later_base + 0.75,
                "low": later_base - 0.75,
                "close": later_base + 0.2,
                "volume": 1.0,
            },
            index=later_index,
        )
        frame = pd.concat([frame, later])
    return frame


def test_buy_anchor_above_finite_maximum_remains_active() -> None:
    frame = _finite_path()
    buy, _, at = construct_surviving_counterexamples(frame)
    state, consumed, remaining, touch = origin_state_at(
        active_m1=frame, origin=buy, at=at
    )
    assert buy.anchor_price > float(frame["high"].max())
    assert state == "ACTIVE"
    assert consumed == 0.0
    assert remaining == H4_RUN_POINTS
    assert touch is None


def test_sell_anchor_below_finite_minimum_remains_active() -> None:
    frame = _finite_path()
    _, sell, at = construct_surviving_counterexamples(frame)
    state, consumed, remaining, touch = origin_state_at(
        active_m1=frame, origin=sell, at=at
    )
    assert 0.0 < sell.anchor_price < float(frame["low"].min())
    assert state == "ACTIVE"
    assert consumed == 0.0
    assert remaining == H4_RUN_POINTS
    assert touch is None


def test_extended_finite_path_still_has_new_surviving_counterexamples() -> None:
    first = evaluate_finite_forward_closure(_finite_path())
    extended = evaluate_finite_forward_closure(_finite_path(extension=True))
    assert first["hypothesis"] == HYPOTHESIS
    assert extended["hypothesis"] == HYPOTHESIS
    assert first["hypothesis_result"] == "FALSIFIED"
    assert extended["hypothesis_result"] == "FALSIFIED"
    assert extended["buy_counterexample"]["anchor_price"] > first["buy_counterexample"]["anchor_price"]
    assert extended["sell_counterexample"]["anchor_price"] < first["sell_counterexample"]["anchor_price"]


def test_report_introduces_no_warmup_expiry_tolerance_or_trade_scoring() -> None:
    report = evaluate_finite_forward_closure(_finite_path())
    serialized = str(report).lower()
    forbidden = (
        "warmup",
        "expiry",
        "tolerance",
        "win_rate",
        "win rate",
        "expectancy",
        "profitability",
        "broker_fill",
        "broker-fill",
        "pnl",
        "p&l",
        "holdout_score",
        "order_send",
    )
    assert not [token for token in forbidden if token in serialized]
    assert report["finite_forward_complete_seed_authorized"] is False
    assert report["independent_anchor_domain_required"] is True


def _construct_h4_origin(side: str, anchor: float):
    index = pd.date_range("2015-08-09T00:00:00Z", periods=3, freq="4h")
    if side == "BUY":
        rows = [
            (anchor + 5.0, anchor + 6.0, anchor, anchor + 1.0),
            (anchor + 1.0, anchor + 7.0, anchor + 0.5, anchor + 5.0),
            (anchor + 4.0, anchor + 8.0, anchor, anchor + 6.0),
        ]
    else:
        rows = [
            (anchor - 6.0, anchor, anchor - 7.0, anchor - 1.0),
            (anchor - 1.0, anchor - 0.5, anchor - 8.0, anchor - 6.0),
            (anchor - 4.0, anchor, anchor - 9.0, anchor - 5.0),
        ]
    h4 = pd.DataFrame(rows, columns=["open", "high", "low", "close"], index=index)
    events = detect_pat2_full_range(h4, "H4")
    origins = build_h4_origins(h4, events)
    return next(origin for origin in origins if origin.side == side)


def test_counterexample_anchor_values_are_constructible_by_frozen_h4_mapping() -> None:
    future = _finite_path()
    buy_anchor = float(np.nextafter(float(future["high"].max()), np.inf))
    sell_anchor = float(np.nextafter(float(future["low"].min()), -np.inf))
    buy = _construct_h4_origin("BUY", buy_anchor)
    sell = _construct_h4_origin("SELL", sell_anchor)
    assert buy.anchor_price == buy_anchor
    assert sell.anchor_price == sell_anchor
    assert buy.anchor_price + H4_RUN_POINTS * PROJECT_POINT_SIZE > buy.anchor_price
    assert sell.anchor_price - H4_RUN_POINTS * PROJECT_POINT_SIZE < sell.anchor_price