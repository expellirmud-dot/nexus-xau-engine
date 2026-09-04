from __future__ import annotations

import pandas as pd

from nexus_xau.research.mtf_alignment_variant_relation_test import LOOKBACK_VARIANTS
from nexus_xau.research.path_remaining_daily_side_mtf_relation import (
    _normalize_bool,
    _period_state,
    _side_relation_state,
    summarize_enriched_events,
)


def test_normalize_bool_handles_csv_like_values() -> None:
    assert _normalize_bool(True) is True
    assert _normalize_bool(False) is False
    assert _normalize_bool("true") is True
    assert _normalize_bool("FALSE") is False
    assert _normalize_bool(1) is True
    assert _normalize_bool(0) is False


def test_side_relation_state_uses_frozen_directional_rule() -> None:
    supportive = {
        "events": 80,
        "levels_with_at_least_min_events": 3,
        "spearman_alignment_vs_target_first": 0.20,
        "spearman_alignment_vs_path_remaining_reach": 0.10,
        "spearman_alignment_vs_fresh_mfe": 0.15,
        "spearman_alignment_vs_fresh_mae": -0.05,
    }
    opposing = {
        "events": 80,
        "levels_with_at_least_min_events": 3,
        "spearman_alignment_vs_target_first": -0.20,
        "spearman_alignment_vs_path_remaining_reach": -0.10,
        "spearman_alignment_vs_fresh_mfe": -0.15,
        "spearman_alignment_vs_fresh_mae": 0.05,
    }

    assert _side_relation_state(supportive) == "SUPPORT"
    assert _side_relation_state(opposing) == "OPPOSE"


def test_period_state_separates_conditional_from_general_support() -> None:
    assert _period_state("SUPPORT", "MIXED") == "SIDE_CONDITIONAL_SUPPORT"
    assert _period_state("SUPPORT", "SUPPORT") == "GENERAL_MTF_SUPPORT_NOT_SIDE_SPECIFIC"
    assert _period_state("OPPOSE", "SUPPORT") == "EXPECTED_SIDE_OPPOSE"
    assert _period_state("INSUFFICIENT", "SUPPORT") == "INCONCLUSIVE"


def _rows_for_variant(variant: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    # EXPECTED_SIDE: count=2 has better target/reach/MFE and lower MAE than count=1.
    for level in (1, 2):
        for i in range(20):
            better = level == 2
            target_first = better or i % 2 == 0
            reached = better or i % 2 == 0
            rows.append(
                {
                    "variant": variant,
                    "frame_side": "EXPECTED_SIDE",
                    "alignment_count": level,
                    "aligned_timeframes": "H1" if level == 1 else "H1,M5",
                    "path_remaining_reached": reached,
                    "path_remaining_first_hit": (
                        "TARGET_FIRST" if target_first else "STOP_FIRST"
                    ),
                    "fresh_mfe_points": 100.0 + (100.0 if better else 0.0) + i,
                    "fresh_mae_points": 200.0 - (100.0 if better else 0.0) + i,
                }
            )

    # CROSSED_SIDE: identical outcome pattern at both count levels -> no graded improvement.
    for level in (1, 2):
        for i in range(20):
            target_first = i % 2 == 0
            rows.append(
                {
                    "variant": variant,
                    "frame_side": "CROSSED_SIDE",
                    "alignment_count": level,
                    "aligned_timeframes": "H1" if level == 1 else "H1,M5",
                    "path_remaining_reached": target_first,
                    "path_remaining_first_hit": (
                        "TARGET_FIRST" if target_first else "STOP_FIRST"
                    ),
                    "fresh_mfe_points": 100.0 + i,
                    "fresh_mae_points": 100.0 + i,
                }
            )
    return rows


def test_summary_keeps_alignment_graded_and_conditioned_by_frame_side() -> None:
    variant = next(iter(LOOKBACK_VARIANTS))
    events = pd.DataFrame(_rows_for_variant(variant))

    report = summarize_enriched_events(events)
    detail = report["variant_reports"][variant]
    expected = detail["sides"]["EXPECTED_SIDE"]

    assert expected["relation_state"] == "SUPPORT"
    assert expected["relation"]["alignment_level_counts"] == {"1": 20, "2": 20}
    assert set(expected["by_alignment_count"]) == {"1", "2"}
    assert detail["period_interaction_state"] == "SIDE_CONDITIONAL_SUPPORT"

    # Missing variants remain explicit rather than being silently promoted.
    for other in LOOKBACK_VARIANTS:
        if other == variant:
            continue
        assert report["variant_reports"][other]["period_interaction_state"] == "INCONCLUSIVE"
