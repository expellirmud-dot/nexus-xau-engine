from decimal import Decimal

import pytest

from nexus_xau.data.price_grid import PriceGrid


def test_xauusdm_tick_index_uses_exact_broker_grid() -> None:
    grid = PriceGrid.from_tick_size("0.001")

    assert grid.tick_index("4373.383") == 4_373_383
    assert grid.price_from_tick(4_373_383) == Decimal("4373.383")


def test_same_price_means_same_tick_without_positive_tolerance() -> None:
    grid = PriceGrid.from_tick_size("0.001")

    assert grid.same_price("3563.590", 3563.59)
    assert not grid.same_price("3563.590", "3563.591")


def test_bar_touch_includes_exact_boundary_contact() -> None:
    grid = PriceGrid.from_tick_size("0.001")

    assert grid.bar_touches_price(low="3339.999", high="3340.000", level="3340.000")
    assert grid.bar_touches_price(low="3340.000", high="3340.010", level="3340.000")


def test_bar_near_miss_one_tick_away_is_not_contact() -> None:
    grid = PriceGrid.from_tick_size("0.001")

    assert not grid.bar_touches_price(
        low="3340.001",
        high="3340.010",
        level="3340.000",
    )


def test_off_grid_price_fails_closed_instead_of_being_rounded() -> None:
    grid = PriceGrid.from_tick_size("0.001")

    with pytest.raises(ValueError, match="not aligned"):
        grid.tick_index("4373.3835")


def test_invalid_tick_size_and_bar_order_fail_closed() -> None:
    with pytest.raises(ValueError, match="positive"):
        PriceGrid.from_tick_size("0")

    grid = PriceGrid.from_tick_size("0.001")
    with pytest.raises(ValueError, match="low"):
        grid.bar_touches_price(low="10.001", high="10.000", level="10.000")
