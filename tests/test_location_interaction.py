import pytest

from nexus_xau.engine.candles import CandleFeatures
from nexus_xau.engine.location_interaction import (
    BoundaryKind,
    PriceBoundary,
    measure_boundary_interaction,
)


def test_line_requires_zero_width() -> None:
    with pytest.raises(ValueError, match="LINE boundary"):
        PriceBoundary(kind=BoundaryKind.LINE, low=100.0, high=101.0)


def test_wick_only_touch_is_distinguished_from_body_touch() -> None:
    candle = CandleFeatures(open=101.0, high=102.0, low=99.5, close=101.5)
    boundary = PriceBoundary(kind=BoundaryKind.LINE, low=100.0, high=100.0)

    interaction = measure_boundary_interaction(candle, boundary)

    assert interaction.wick_intersects is True
    assert interaction.body_intersects is False
    assert interaction.nearest_distance == 0.0
    assert interaction.penetration_below == pytest.approx(0.5)
    assert interaction.penetration_above == pytest.approx(2.0)


def test_body_straddling_zone_is_recorded_without_qualification() -> None:
    candle = CandleFeatures(open=99.8, high=101.5, low=99.0, close=100.8)
    boundary = PriceBoundary(kind=BoundaryKind.ZONE, low=100.0, high=100.5)

    interaction = measure_boundary_interaction(candle, boundary)

    assert interaction.wick_intersects is True
    assert interaction.body_intersects is True
    assert interaction.open_inside is False
    assert interaction.close_inside is False
    assert interaction.body_above is False
    assert interaction.body_below is False


def test_candle_fully_above_support_line_has_positive_distance() -> None:
    candle = CandleFeatures(open=101.5, high=102.0, low=101.0, close=101.8)
    boundary = PriceBoundary(kind=BoundaryKind.LINE, low=100.0, high=100.0)

    interaction = measure_boundary_interaction(candle, boundary)

    assert interaction.full_candle_above is True
    assert interaction.full_candle_below is False
    assert interaction.nearest_distance == pytest.approx(1.0)
    assert interaction.penetration_below == 0.0


def test_candle_fully_below_resistance_line_has_positive_distance() -> None:
    candle = CandleFeatures(open=98.5, high=99.0, low=98.0, close=98.2)
    boundary = PriceBoundary(kind=BoundaryKind.LINE, low=100.0, high=100.0)

    interaction = measure_boundary_interaction(candle, boundary)

    assert interaction.full_candle_below is True
    assert interaction.full_candle_above is False
    assert interaction.nearest_distance == pytest.approx(1.0)
    assert interaction.penetration_above == 0.0
