from __future__ import annotations

import pandas as pd

from nexus_xau.research.post_sig_invalidation_conflict_batch import cross_period_decision
from nexus_xau.research.post_sig_invalidation_conflict_scan import (
    selected_origin_conflict,
)


def _m1() -> pd.DataFrame:
    index = pd.date_range("2026-01-01T01:00:00Z", periods=4, freq="min")
    return pd.DataFrame(
        {
            "open": [100.0, 100.0, 100.0, 100.0],
            "high": [100.0, 100.0, 101.0, 100.0],
            "low": [100.0, 100.0, 99.0, 100.0],
            "close": [100.0, 100.0, 100.0, 100.0],
            "volume": [1.0, 1.0, 1.0, 1.0],
        },
        index=index,
    )


def test_buy_destroyed_only_when_low_moves_strictly_below_anchor() -> None:
    frame = _m1()
    result = selected_origin_conflict(
        m1=frame,
        side="BUY",
        origin_anchor_known_at=frame.index[0],
        origin_anchor_price=100.0,
        candidate_known_at=frame.index[-1],
    )
    assert result["evaluable"] is True
    assert result["destroyed_before_candidate"] is True
    assert result["first_destruction_at"] == frame.index[2].isoformat()
    assert result["max_anchor_exceed_points"] == 100.0


def test_sell_destroyed_only_when_high_moves_strictly_above_anchor() -> None:
    frame = _m1()
    result = selected_origin_conflict(
        m1=frame,
        side="SELL",
        origin_anchor_known_at=frame.index[0],
        origin_anchor_price=100.0,
        candidate_known_at=frame.index[-1],
    )
    assert result["destroyed_before_candidate"] is True
    assert result["first_destruction_at"] == frame.index[2].isoformat()
    assert result["max_anchor_exceed_points"] == 100.0


def test_equal_anchor_is_not_destroyed_under_strict_beyond_rule() -> None:
    frame = _m1().iloc[:2].copy()
    result = selected_origin_conflict(
        m1=frame,
        side="BUY",
        origin_anchor_known_at=frame.index[0],
        origin_anchor_price=100.0,
        candidate_known_at=frame.index[-1] + pd.Timedelta(minutes=1),
    )
    assert result["destroyed_before_candidate"] is False
    assert result["max_anchor_exceed_points"] == 0.0


def test_cross_period_decision_uses_presence_not_invented_fraction_threshold() -> None:
    assert (
        cross_period_decision(
            ["CONFLICT_OBSERVED", "CONFLICT_OBSERVED", "NO_CONFLICT_OBSERVED"]
        )
        == "REPLICATED_SOURCE_PARTIAL_CONFLICT_OBSERVED"
    )
    assert (
        cross_period_decision(
            ["CONFLICT_OBSERVED", "NO_CONFLICT_OBSERVED", "NOT_TESTABLE_WITH_CURRENT_EVIDENCE"]
        )
        == "SOURCE_PARTIAL_CONFLICT_SINGLE_PERIOD"
    )
    assert (
        cross_period_decision(
            ["NO_CONFLICT_OBSERVED", "NO_CONFLICT_OBSERVED", "NOT_TESTABLE_WITH_CURRENT_EVIDENCE"]
        )
        == "NO_SOURCE_PARTIAL_CONFLICT_OBSERVED"
    )
