from __future__ import annotations

import pandas as pd

from nexus_xau.research.daily_frame_side_remaining_relation import _state, _summary


def test_summary_includes_path_and_fresh_path_context() -> None:
    frame = pd.DataFrame(
        {
            "path_remaining_first_hit": ["TARGET_FIRST", "STOP_FIRST", "NEITHER"],
            "path_remaining_reached": [True, False, True],
            "fresh_mfe_points": [1200.0, 800.0, 1000.0],
            "fresh_mae_points": [400.0, 900.0, 600.0],
        }
    )
    summary = _summary(frame)
    assert summary["events"] == 3
    assert summary["resolved_events"] == 2
    assert summary["target_first_rate_resolved"] == 0.5
    assert summary["target_reach_rate"] == 2 / 3
    assert summary["fresh_mfe_median"] == 1000.0
    assert summary["fresh_mae_median"] == 600.0


def test_state_support_and_minimum_guard() -> None:
    expected = {
        "events": 20,
        "target_first_rate_resolved": 0.65,
        "target_reach_rate": 0.75,
    }
    crossed = {
        "events": 20,
        "target_first_rate_resolved": 0.55,
        "target_reach_rate": 0.70,
    }
    assert _state(expected, crossed) == "SUPPORT"

    expected["events"] = 9
    assert _state(expected, crossed) == "INSUFFICIENT"
