from __future__ import annotations

import pandas as pd

from nexus_xau.research.inherited_origin_context_relation import (
    age_relation_state,
    build_context_events,
    consumed_relation_state,
    cycle_relation_state,
    summarize_context_events,
)


def test_direction_labels_follow_frozen_sign_rules() -> None:
    younger = {
        "events": 20,
        "distinct_feature_values": 10,
        "spearman_vs_fixed_target_first": -0.2,
        "spearman_vs_fixed_reach": -0.1,
        "spearman_vs_fresh_mfe": -0.3,
        "spearman_vs_fresh_mae": 0.2,
    }
    older = {
        **younger,
        "spearman_vs_fixed_target_first": 0.2,
        "spearman_vs_fixed_reach": 0.1,
        "spearman_vs_fresh_mfe": 0.3,
        "spearman_vs_fresh_mae": -0.2,
    }
    assert age_relation_state(younger) == "YOUNGER_ORIGIN_FAVORED"
    assert age_relation_state(older) == "OLDER_ORIGIN_FAVORED"
    assert consumed_relation_state(older) == "MORE_CONSUMED_FAVORED"
    assert consumed_relation_state(younger) == "LESS_CONSUMED_FAVORED"


def test_cycle_state_uses_fixed_1000_control() -> None:
    previous = {
        "events": 20,
        "target_first_rate_resolved": 0.70,
        "fresh_1000_reach_rate": 0.80,
        "fresh_mfe_median": 1400.0,
        "fresh_mae_median": 700.0,
    }
    older = {
        "events": 20,
        "target_first_rate_resolved": 0.50,
        "fresh_1000_reach_rate": 0.60,
        "fresh_mfe_median": 1000.0,
        "fresh_mae_median": 900.0,
    }
    assert cycle_relation_state(previous, older) == "PREVIOUS_24H_FAVORED"
    assert cycle_relation_state(older, previous) == "OLDER_CYCLE_FAVORED"


def _remaining_rows() -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    cutoff = pd.Timestamp("2025-09-02T00:00:00Z")
    for index in range(12):
        candidate = cutoff + pd.Timedelta(hours=8 + index)
        origin = cutoff - pd.Timedelta(hours=12 + index)
        rows.append(
            {
                "state": "INHERITED_REMAINING_RUN",
                "cutoff_utc": cutoff.isoformat(),
                "candidate_known_at": candidate.isoformat(),
                "side": "BUY",
                "origin_anchor_known_at": origin.isoformat(),
                "remaining_at_entry_points": 900.0 - index * 20.0,
                "fresh_target_reached_anywhere": index >= 4,
                "fresh_first_hit": "TARGET_FIRST" if index >= 6 else "STOP_FIRST",
                "fresh_mfe_points": 800.0 + index * 100.0,
                "fresh_mae_points": 1500.0 - index * 50.0,
                "path_remaining_reached": True,
                "path_remaining_first_hit": "TARGET_FIRST",
                "origin_level_reached": index >= 5,
                "origin_level_first_hit": "TARGET_FIRST" if index >= 5 else "STOP_FIRST",
            }
        )
    return pd.DataFrame(rows)


def _daily_rows() -> pd.DataFrame:
    remaining = _remaining_rows()
    return pd.DataFrame(
        {
            "candidate_known_at": remaining["candidate_known_at"],
            "side": remaining["side"],
            "signed_valid_side_distance_points": [100.0] * len(remaining),
        }
    )


def test_build_context_events_derives_age_consumed_ratio_and_cycle() -> None:
    events = build_context_events(
        remaining_events=_remaining_rows(),
        daily_events=_daily_rows(),
    )
    assert len(events) == 12
    assert set(events["frame_side"]) == {"EXPECTED_SIDE"}
    assert events["origin_age_hours"].min() > 0
    assert events["consumed_run_ratio_at_entry"].between(0.0, 1.0).all()
    assert set(events["origin_cycle_group"]) == {"PREVIOUS_24H_CYCLE"}


def test_summary_uses_fixed_control_for_continuous_relations() -> None:
    events = build_context_events(
        remaining_events=_remaining_rows(),
        daily_events=_daily_rows(),
    )
    summary = summarize_context_events(events)
    expected = summary["side_reports"]["EXPECTED_SIDE"]
    assert expected["events"] == 12
    assert expected["origin_age"]["relation"]["distinct_feature_values"] >= 2
    assert (
        expected["consumed_run_ratio_at_entry"]["relation"]["distinct_feature_values"]
        >= 2
    )
    assert summary["expected_side_cycle_comparison"]["state"] == "INSUFFICIENT"
