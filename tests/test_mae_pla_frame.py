import pytest

from nexus_xau.engine.mae_pla_frame import build_mae_pla_frame_candidates


def test_nearest_zero_five_reference_below() -> None:
    result = build_mae_pla_frame_candidates(3301.2)

    assert len(result.candidates) == 1
    candidate = result.candidates[0]
    assert candidate.reference_price == pytest.approx(3300.0)
    assert candidate.upper_price == pytest.approx(3305.0)
    assert candidate.lower_price == pytest.approx(3295.0)
    assert result.snap_tie_resolved is True
    assert result.timing_mapping_resolved is False


def test_nearest_zero_five_reference_above() -> None:
    result = build_mae_pla_frame_candidates(3303.8)

    assert len(result.candidates) == 1
    assert result.candidates[0].reference_price == pytest.approx(3305.0)


def test_exact_statistical_reference_stays_single() -> None:
    result = build_mae_pla_frame_candidates(3305.0)

    assert len(result.candidates) == 1
    assert result.candidates[0].reference_price == pytest.approx(3305.0)
    assert result.candidates[0].reference_distance == 0.0


def test_equal_distance_returns_both_instead_of_guessing_tie() -> None:
    result = build_mae_pla_frame_candidates(3302.5)

    assert [item.reference_price for item in result.candidates] == pytest.approx([3300.0, 3305.0])
    assert result.snap_tie_resolved is False


def test_project_point_size_kept_explicit() -> None:
    result = build_mae_pla_frame_candidates(
        3301.0,
        project_point_size=0.01,
        half_width_points=500,
    )

    candidate = result.candidates[0]
    assert candidate.upper_price - candidate.reference_price == pytest.approx(5.0)
    assert candidate.reference_price - candidate.lower_price == pytest.approx(5.0)


def test_invalid_point_size_rejected() -> None:
    with pytest.raises(ValueError, match="project_point_size"):
        build_mae_pla_frame_candidates(3300.0, project_point_size=0.0)
