from __future__ import annotations

from pathlib import Path

import pandas as pd

from nexus_xau.research.path_remaining_daily_side_mtf_batch import (
    cross_period_decision,
    discover_interaction_events_file,
    discover_m1_file,
)


def test_cross_period_decision_keeps_specificity_separate() -> None:
    assert (
        cross_period_decision(
            ["SIDE_CONDITIONAL_SUPPORT", "SIDE_CONDITIONAL_SUPPORT", "INCONCLUSIVE"]
        )
        == "SUPPORTED_SIDE_CONDITIONAL_REPLICATION"
    )
    assert (
        cross_period_decision(
            [
                "GENERAL_MTF_SUPPORT_NOT_SIDE_SPECIFIC",
                "GENERAL_MTF_SUPPORT_NOT_SIDE_SPECIFIC",
                "INCONCLUSIVE",
            ]
        )
        == "SUPPORTED_GENERAL_MTF_NOT_SIDE_SPECIFIC"
    )
    assert (
        cross_period_decision(
            [
                "SIDE_CONDITIONAL_SUPPORT",
                "GENERAL_MTF_SUPPORT_NOT_SIDE_SPECIFIC",
                "INCONCLUSIVE",
            ]
        )
        == "SUPPORTED_MTF_RELATION_SPECIFICITY_MIXED"
    )
    assert (
        cross_period_decision(
            ["EXPECTED_SIDE_OPPOSE", "EXPECTED_SIDE_OPPOSE", "INCONCLUSIVE"]
        )
        == "NOT_SUPPORTED_EXPECTED_SIDE"
    )


def test_discovery_finds_covering_m1_and_parent_interaction(tmp_path: Path) -> None:
    data_root = tmp_path / "data"
    results_root = tmp_path / "results"
    data_root.mkdir()
    results_root.mkdir()

    m1_path = data_root / "XAUUSD_M1_BID_2024-09-01_2024-11-30.csv"
    pd.DataFrame(
        {
            "timestamp": [
                "2024-09-01T00:00:00+00:00",
                "2024-11-30T23:59:00+00:00",
            ],
            "open": [1.0, 1.0],
            "high": [1.0, 1.0],
            "low": [1.0, 1.0],
            "close": [1.0, 1.0],
            "volume": [1.0, 1.0],
        }
    ).to_csv(m1_path, index=False)

    parent = results_root / "DAILY_FRAME_REMAINING_INTERACTION_2024.csv"
    pd.DataFrame(
        {
            "candidate_known_at": ["2024-10-01T01:00:00+00:00"],
            "side": ["BUY"],
            "signed_valid_side_distance_points": [10.0],
            "path_remaining_reached": [True],
            "path_remaining_first_hit": ["TARGET_FIRST"],
            "fresh_mfe_points": [100.0],
            "fresh_mae_points": [50.0],
        }
    ).to_csv(parent, index=False)

    enriched = results_root / "ALREADY_ENRICHED.csv"
    pd.DataFrame(
        {
            "candidate_known_at": ["2024-10-01T01:00:00+00:00"],
            "side": ["BUY"],
            "signed_valid_side_distance_points": [10.0],
            "path_remaining_reached": [True],
            "path_remaining_first_hit": ["TARGET_FIRST"],
            "fresh_mfe_points": [100.0],
            "fresh_mae_points": [50.0],
            "alignment_count": [2],
            "variant": ["RECENT_1_TF_BAR"],
        }
    ).to_csv(enriched, index=False)

    assert discover_m1_file(data_root, start="2024-09-01", end="2024-11-30") == m1_path
    assert (
        discover_interaction_events_file(
            results_root,
            start="2024-09-01",
            end="2024-11-30",
        )
        == parent
    )
