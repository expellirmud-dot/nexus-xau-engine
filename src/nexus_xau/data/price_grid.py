from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import SupportsFloat

PriceLike = str | int | float | Decimal | SupportsFloat


def _decimal(value: PriceLike, *, field: str) -> Decimal:
    if isinstance(value, Decimal):
        result = value
    else:
        result = Decimal(str(value))
    if not result.is_finite():
        raise ValueError(f"{field} must be finite")
    return result


@dataclass(frozen=True)
class PriceGrid:
    """Exact broker-tick grid for chart-price equality/contact research.

    This class normalizes already observed broker prices to integer ticks. It does
    not add a trading tolerance, model Bid/Ask execution, or convert course/system
    points into broker points.
    """

    tick_size: Decimal

    @classmethod
    def from_tick_size(cls, tick_size: PriceLike) -> PriceGrid:
        tick = _decimal(tick_size, field="tick_size")
        if tick <= 0:
            raise ValueError("tick_size must be positive")
        return cls(tick_size=tick)

    def tick_index(self, price: PriceLike) -> int:
        value = _decimal(price, field="price")
        ticks = value / self.tick_size
        integral = ticks.to_integral_value()
        if ticks != integral:
            raise ValueError(
                f"price {value} is not aligned to broker tick size {self.tick_size}"
            )
        return int(integral)

    def price_from_tick(self, tick_index: int) -> Decimal:
        return self.tick_size * tick_index

    def same_price(self, left: PriceLike, right: PriceLike) -> bool:
        """Return True only when both prices resolve to the same broker tick."""

        return self.tick_index(left) == self.tick_index(right)

    def bar_touches_price(
        self,
        *,
        low: PriceLike,
        high: PriceLike,
        level: PriceLike,
    ) -> bool:
        """Detect chart-side price contact from an OHLC bar.

        The result establishes only that the bar's observed price range included
        the level. It does not establish intrabar ordering or broker order fill.
        """

        low_tick = self.tick_index(low)
        high_tick = self.tick_index(high)
        if low_tick > high_tick:
            raise ValueError("low must be less than or equal to high")
        level_tick = self.tick_index(level)
        return low_tick <= level_tick <= high_tick
