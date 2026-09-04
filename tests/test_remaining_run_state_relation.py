from __future__ import annotations

import pandas as pd

from nexus_xau.research.remaining_run_state_relation_test import (
    OriginRun,
    _consumed_points,
    _decision,
)


def test_consumed_points_buy_and_sell() -> None:
    idx = pd.date_range("2026-01-01T01:00:00Z", periods=3, freq="min")
    frame = pd.DataFrame(
        {
            "open": [100.0, 100.5, 101.0],
            "high": [101.0, 102.0, 103.0],
            "low": [99.0, 98.0, 97.0],
            "close": [100.5, 101.0, 102.0],
            "volume": [1.0, 1.0, 1.0],
        },
        index=idx,
    )
    buy = OriginRun("BUY", idx[0], idx[0], 100.0)
    sell = OriginRun("SELL", idx[0], idx[0], 100.0)
    end = idx[-1] + pd.Timedelta(minutes=1)
    assert _consumed_points(frame, buy, end) == 300.0
    assert _consumed_points(frame, sell, end) == 300.0


def test_decision_requires_minimum_group() -> None:
    summary = {
        "events": 29,
        "target_first_rate_resolved": 0.8,
        "target_reach_rate_anywhere": 0.8,
        "mfe_median": 1500.0,
        "mae_median": 500.0,
    }
    control = {
        "events": 40,
        "target_first_rate_resolved": 0.4,
        "target_reach_rate_anywhere": 0.4,
        "mfe_median": 800.0,
        "mae_median": 1000.0,
    }
    assert _decision(summary, control) == "INCONCLUSIVE_INSUFFICIENT"
