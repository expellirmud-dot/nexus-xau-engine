from __future__ import annotations

import pandas as pd
import pytest

from nexus_xau.research.geometry_null_rq015 import classify, derive_geometry


def _row(**overrides):
    row = {
        "candidate_state": "RESEARCH_CANDIDATE",
        "path_remaining_first_hit": "TARGET_FIRST",
        "path_remaining_target_price": 101.0,
        "confirmation_close": 100.0,
        "origin_anchor_price": 99.5,
        "remaining_points_at_confirmation": 100.0,
        "confirmation_known_at": "2026-01-01T01:00:00+00:00",
        "next_cutoff_utc": "2026-01-02T00:00:00+00:00",
        "consumed_ratio_at_0700": 0.4,
        "consumed_points_at_confirmation": 1400.0,
    }
    row.update(overrides)
    return row


def test_derive_geometry_preserves_states_and_validates_distances():
    frame = pd.DataFrame(
        [
            _row(),
            _row(
                path_remaining_first_hit="NEITHER_BY_NEXT_0700",
                path_remaining_target_price=100.5,
                remaining_points_at_confirmation=50.0,
                consumed_points_at_confirmation=1450.0,
            ),
        ]
    )
    out = derive_geometry(frame)
    assert list(out["path_remaining_first_hit"]) == [
        "TARGET_FIRST",
        "NEITHER_BY_NEXT_0700",
    ]
    assert out.iloc[0]["target_distance_points"] == pytest.approx(100.0)
    assert out.iloc[0]["point_distance_points"] == pytest.approx(50.0)
    assert out.iloc[0]["geometry_target_advantage"] == pytest.approx(1 / 3)
    assert out.iloc[0]["total_boundary_distance_points"] == pytest.approx(150.0)
    assert out.iloc[0]["horizon_minutes"] == pytest.approx(23 * 60)


def test_derive_geometry_rejects_nonpositive_denominator():
    frame = pd.DataFrame(
        [
            _row(
                path_remaining_target_price=100.0,
                origin_anchor_price=100.0,
                remaining_points_at_confirmation=0.0,
                consumed_points_at_confirmation=1500.0,
            )
        ]
    )
    with pytest.raises(ValueError, match="non-positive geometry denominator"):
        derive_geometry(frame)


def _summary(partial, geometry=0.6, consumed_geometry=0.8):
    return {
        "resolved_diagnostics": {
            "partial_rank_consumed_0700_given_geometry": partial,
            "rho_geometry_outcome": geometry,
            "rho_consumed_0700_geometry": consumed_geometry,
        }
    }


def test_classify_surviving_residual_requires_positive_both_periods():
    assert classify(_summary(0.1), _summary(0.2)) == (
        "CONSUMED_RESIDUAL_RELATION_SURVIVES_GEOMETRY_CONTROL"
    )


def test_classify_geometry_dominated_requires_nonpositive_residual_both_periods():
    assert classify(_summary(-0.1), _summary(0.0)) == (
        "CONSUMED_ASSOCIATION_EXPLAINED_OR_DOMINATED_BY_GEOMETRY"
    )


def test_classify_mixed_sign_is_not_identifiable():
    assert classify(_summary(0.1), _summary(-0.1)) == (
        "INDEPENDENT_EFFECT_NOT_IDENTIFIABLE_WITH_CURRENT_DATA"
    )
