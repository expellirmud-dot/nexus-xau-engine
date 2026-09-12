from __future__ import annotations

import pandas as pd
import pytest

from nexus_xau.research.continuous_mtf_q2_0700 import (
    ORIGIN_OUTCOME,
    PATH_OUTCOME,
    _spearman,
    build_associations,
    build_feature_events,
    build_mtf_count_groups,
)


def test_spearman_handles_positive_negative_and_constant() -> None:
    x = pd.Series([1.0, 2.0, 3.0, 4.0])
    assert _spearman(x, pd.Series([0.0, 0.0, 1.0, 1.0])) > 0
    assert _spearman(x, pd.Series([1.0, 1.0, 0.0, 0.0])) < 0
    assert _spearman(pd.Series([1.0, 1.0]), pd.Series([0.0, 1.0])) is None


def test_build_feature_events_filters_primary_scored_and_merges_recent_alignment() -> None:
    q1 = pd.DataFrame(
        [
            {
                "variant": "FIRST_EXPECTED_SIDE_PA_PROXY",
                "candidate_state": "SCORED",
                "context_id": "2026-01-01:BUY",
                "day_id": "2026-01-01",
                "side": "BUY",
                "origin_id": "H1:BUY:a",
                "origin_tf": "H1",
                "confirmation_event_id": "e1",
                "confirmation_event_tf": "M5",
                "confirmation_known_at": "2026-01-01T00:10:00+00:00",
                "origin_age_hours_at_0700": 4.0,
                "consumed_ratio_at_0700": 0.25,
                "remaining_points_at_0700": 750.0,
                "remaining_points_at_confirmation": 600.0,
                "nominal_run_points": 1000.0,
                PATH_OUTCOME: "TARGET_FIRST",
                ORIGIN_OUTCOME: "POINT_CHECK_FIRST",
            },
            {
                "variant": "FIRST_ANY_PA_PROXY",
                "candidate_state": "SCORED",
                "context_id": "2026-01-01:BUY",
                "day_id": "2026-01-01",
                "side": "BUY",
                "origin_id": "H1:BUY:a",
                "origin_tf": "H1",
                "confirmation_event_id": "e1",
                "confirmation_event_tf": "M5",
                "confirmation_known_at": "2026-01-01T00:05:00+00:00",
                "origin_age_hours_at_0700": 4.0,
                "consumed_ratio_at_0700": 0.25,
                "remaining_points_at_0700": 750.0,
                "remaining_points_at_confirmation": 650.0,
                "nominal_run_points": 1000.0,
                PATH_OUTCOME: "TARGET_FIRST",
                ORIGIN_OUTCOME: "TARGET_FIRST",
            },
            {
                "variant": "FIRST_EXPECTED_SIDE_PA_PROXY",
                "candidate_state": "POINT_CHECK_DESTROYED_BEFORE_CONFIRMATION",
                "context_id": "2026-01-02:SELL",
                "day_id": "2026-01-02",
                "side": "SELL",
                "origin_id": "H4:SELL:b",
                "origin_tf": "H4",
                "confirmation_event_id": "e2",
                "confirmation_event_tf": "M5",
                "confirmation_known_at": "2026-01-02T00:10:00+00:00",
                "origin_age_hours_at_0700": 8.0,
                "consumed_ratio_at_0700": 0.10,
                "remaining_points_at_0700": 1350.0,
                "remaining_points_at_confirmation": None,
                "nominal_run_points": 1500.0,
                PATH_OUTCOME: None,
                ORIGIN_OUTCOME: None,
            },
        ]
    )
    confirmations = pd.DataFrame(
        [
            {
                "event_id": "e1",
                "alignment_count_exact": 1,
                "alignment_count_recent_1_tf_bar": 2,
                "alignment_count_recent_2_tf_bars": 3,
            },
            {
                "event_id": "e2",
                "alignment_count_exact": 1,
                "alignment_count_recent_1_tf_bar": 1,
                "alignment_count_recent_2_tf_bars": 2,
            },
        ]
    )

    result = build_feature_events(
        q1_events=q1,
        confirmation_events=confirmations,
    )

    assert len(result) == 1
    row = result.iloc[0]
    assert row["confirmation_event_id"] == "e1"
    assert row["alignment_count_recent_1_tf_bar"] == 2
    assert row["alignment_count_recent_2_tf_bars"] == 3
    assert row["remaining_ratio_at_confirmation"] == pytest.approx(0.6)
    assert row[f"{PATH_OUTCOME}_indicator"] == 1.0
    assert row[f"{ORIGIN_OUTCOME}_indicator"] == 0.0


def test_build_feature_events_rejects_missing_confirmation_join() -> None:
    q1 = pd.DataFrame(
        [
            {
                "variant": "FIRST_EXPECTED_SIDE_PA_PROXY",
                "candidate_state": "SCORED",
                "context_id": "c",
                "day_id": "2026-01-01",
                "side": "BUY",
                "origin_id": "o",
                "origin_tf": "H1",
                "confirmation_event_id": "missing",
                "confirmation_event_tf": "M5",
                "confirmation_known_at": "2026-01-01T00:10:00+00:00",
                "origin_age_hours_at_0700": 1.0,
                "consumed_ratio_at_0700": 0.2,
                "remaining_points_at_0700": 800.0,
                "remaining_points_at_confirmation": 700.0,
                "nominal_run_points": 1000.0,
                PATH_OUTCOME: "TARGET_FIRST",
                ORIGIN_OUTCOME: "TARGET_FIRST",
            }
        ]
    )
    confirmations = pd.DataFrame(
        columns=[
            "event_id",
            "alignment_count_exact",
            "alignment_count_recent_1_tf_bar",
            "alignment_count_recent_2_tf_bars",
        ]
    )

    with pytest.raises(ValueError, match="missing confirmation events"):
        build_feature_events(
            q1_events=q1,
            confirmation_events=confirmations,
        )


def test_associations_report_origin_and_context_levels() -> None:
    frame = pd.DataFrame(
        [
            {
                "context_id": "a",
                "origin_tf": "H1",
                "origin_age_hours_at_0700": 1.0,
                "consumed_ratio_at_0700": 0.1,
                "remaining_ratio_at_confirmation": 0.9,
                "remaining_points_at_0700": 900.0,
                "remaining_points_at_confirmation": 900.0,
                "alignment_count_exact": 1,
                "alignment_count_recent_1_tf_bar": 1,
                "alignment_count_recent_2_tf_bars": 1,
                PATH_OUTCOME: "POINT_CHECK_FIRST",
                f"{PATH_OUTCOME}_indicator": 0.0,
                ORIGIN_OUTCOME: "POINT_CHECK_FIRST",
                f"{ORIGIN_OUTCOME}_indicator": 0.0,
            },
            {
                "context_id": "a",
                "origin_tf": "H4",
                "origin_age_hours_at_0700": 2.0,
                "consumed_ratio_at_0700": 0.2,
                "remaining_ratio_at_confirmation": 0.8,
                "remaining_points_at_0700": 1200.0,
                "remaining_points_at_confirmation": 1200.0,
                "alignment_count_exact": 1,
                "alignment_count_recent_1_tf_bar": 1,
                "alignment_count_recent_2_tf_bars": 1,
                PATH_OUTCOME: "POINT_CHECK_FIRST",
                f"{PATH_OUTCOME}_indicator": 0.0,
                ORIGIN_OUTCOME: "POINT_CHECK_FIRST",
                f"{ORIGIN_OUTCOME}_indicator": 0.0,
            },
            {
                "context_id": "b",
                "origin_tf": "H1",
                "origin_age_hours_at_0700": 8.0,
                "consumed_ratio_at_0700": 0.8,
                "remaining_ratio_at_confirmation": 0.2,
                "remaining_points_at_0700": 200.0,
                "remaining_points_at_confirmation": 200.0,
                "alignment_count_exact": 1,
                "alignment_count_recent_1_tf_bar": 3,
                "alignment_count_recent_2_tf_bars": 4,
                PATH_OUTCOME: "TARGET_FIRST",
                f"{PATH_OUTCOME}_indicator": 1.0,
                ORIGIN_OUTCOME: "TARGET_FIRST",
                f"{ORIGIN_OUTCOME}_indicator": 1.0,
            },
        ]
    )

    associations = build_associations(frame)
    origin = associations[
        (associations["outcome"] == PATH_OUTCOME)
        & (associations["analysis_level"] == "ORIGIN_ROW")
        & (associations["stratum"] == "ALL")
        & (associations["feature"] == "origin_age_hours_at_0700")
    ].iloc[0]
    context = associations[
        (associations["outcome"] == PATH_OUTCOME)
        & (associations["analysis_level"] == "CONTEXT")
        & (associations["feature"] == "origin_age_hours_at_0700")
    ].iloc[0]

    assert origin["n_rows"] == 3
    assert origin["rho"] > 0
    assert context["n_contexts"] == 2
    assert context["rho"] > 0
    assert context["median_resolved_origins_per_context"] == pytest.approx(1.5)


def test_mtf_group_counts_preserve_neither_and_ambiguous() -> None:
    frame = pd.DataFrame(
        [
            {
                "context_id": "a",
                "alignment_count_exact": 1,
                "alignment_count_recent_1_tf_bar": 2,
                "alignment_count_recent_2_tf_bars": 3,
                PATH_OUTCOME: "TARGET_FIRST",
                ORIGIN_OUTCOME: "POINT_CHECK_FIRST",
            },
            {
                "context_id": "b",
                "alignment_count_exact": 1,
                "alignment_count_recent_1_tf_bar": 2,
                "alignment_count_recent_2_tf_bars": 3,
                PATH_OUTCOME: "NEITHER_BEFORE_NEXT_0700",
                ORIGIN_OUTCOME: "AMBIGUOUS_SAME_BAR",
            },
        ]
    )

    groups = build_mtf_count_groups(frame)
    row = groups[
        (groups["outcome"] == PATH_OUTCOME)
        & (groups["alignment_feature"] == "alignment_count_recent_1_tf_bar")
        & (groups["alignment_count"] == 2.0)
    ].iloc[0]

    assert row["origin_rows"] == 2
    assert row["contexts"] == 2
    assert row["target_first"] == 1
    assert row["neither_before_next_0700"] == 1
    assert row["resolved_target_first_fraction"] == pytest.approx(1.0)
