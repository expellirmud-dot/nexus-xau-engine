from __future__ import annotations

import pandas as pd

from nexus_xau.research.mtf_alignment_variant_relation_test import LOOKBACK_VARIANTS
from nexus_xau.research.path_remaining_daily_side_mtf_relation_v2 import (
    _period_state,
    _side_relation_state,
    summarize_enriched_events,
)


def test_v2_side_state_inherits_parent_minimum_and_uses_observed_levels() -> None:
    supportive = {
        "events": 10,
        "distinct_alignment_levels": 2,
        "spearman_alignment_vs_target_first": 0.2,
        "spearman_alignment_vs_path_remaining_reach": 0.1,
        "spearman_alignment_vs_fresh_mfe": 0.1,
        "spearman_alignment_vs_fresh_mae": -0.1,
    }
    insufficient = {**supportive, "events": 9}
    indistinguishable = {**supportive, "distinct_alignment_levels": 1}

    assert _side_relation_state(supportive) == "SUPPORT"
    assert _side_relation_state(insufficient) == "INSUFFICIENT"
    assert _side_relation_state(indistinguishable) == "INDISTINGUISHABLE"


def test_v2_period_state_keeps_side_specificity_explicit() -> None:
    assert _period_state("SUPPORT", "MIXED") == "SIDE_CONDITIONAL_SUPPORT"
    assert _period_state("SUPPORT", "SUPPORT") == "GENERAL_MTF_SUPPORT_NOT_SIDE_SPECIFIC"
    assert _period_state("OPPOSE", "SUPPORT") == "EXPECTED_SIDE_OPPOSE"
    assert _period_state("INDISTINGUISHABLE", "SUPPORT") == "EXPECTED_SIDE_INDISTINGUISHABLE"


def _rows(variant: str, frame_side: str, supportive: bool) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for level in (1, 2):
        for i in range(6):
            improved = supportive and level == 2
            target = improved or i % 2 == 0
            rows.append(
                {
                    "variant": variant,
                    "frame_side": frame_side,
                    "alignment_count": level,
                    "aligned_timeframes": "H1" if level == 1 else "H1,M5",
                    "path_remaining_reached": target,
                    "path_remaining_first_hit": "TARGET_FIRST" if target else "STOP_FIRST",
                    "fresh_mfe_points": 100.0 + i + (100.0 if improved else 0.0),
                    "fresh_mae_points": 200.0 + i - (100.0 if improved else 0.0),
                }
            )
    return rows


def test_v2_summary_reports_graded_relation_without_per_level_threshold() -> None:
    variant = next(iter(LOOKBACK_VARIANTS))
    events = pd.DataFrame(
        _rows(variant, "EXPECTED_SIDE", True)
        + _rows(variant, "CROSSED_SIDE", False)
    )

    report = summarize_enriched_events(events)
    expected = report["variant_reports"][variant]["sides"]["EXPECTED_SIDE"]

    assert expected["relation"]["events"] == 12
    assert expected["relation"]["distinct_alignment_levels"] == 2
    assert expected["relation"]["alignment_level_counts"] == {"1": 6, "2": 6}
    assert expected["relation_state"] == "SUPPORT"
    assert report["period_states"][variant] == "SIDE_CONDITIONAL_SUPPORT"
