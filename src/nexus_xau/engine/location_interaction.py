from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from nexus_xau.engine.candles import CandleFeatures


class BoundaryKind(StrEnum):
    LINE = "LINE"
    ZONE = "ZONE"


@dataclass(frozen=True, slots=True)
class PriceBoundary:
    """Traceable line/zone geometry with no strategy tolerance embedded."""

    kind: BoundaryKind
    low: float
    high: float

    def __post_init__(self) -> None:
        if self.high < self.low:
            raise ValueError("boundary high must be >= low")
        if self.kind is BoundaryKind.LINE and self.high != self.low:
            raise ValueError("LINE boundary requires low == high")

    @property
    def midpoint(self) -> float:
        return (self.low + self.high) / 2.0


@dataclass(frozen=True, slots=True)
class CandleBoundaryInteraction:
    candle_low: float
    candle_high: float
    body_low: float
    body_high: float
    open: float
    close: float
    boundary_low: float
    boundary_high: float
    wick_intersects: bool
    body_intersects: bool
    open_inside: bool
    close_inside: bool
    full_candle_above: bool
    full_candle_below: bool
    body_above: bool
    body_below: bool
    nearest_distance: float
    penetration_below: float
    penetration_above: float


def measure_boundary_interaction(
    candle: CandleFeatures,
    boundary: PriceBoundary,
) -> CandleBoundaryInteraction:
    """Measure raw candle-vs-boundary geometry without deciding validity.

    This is intentionally threshold-free. It supports later evidence work on
    touch, penetration, body standing, close location and line-vs-zone rules.
    """

    body_low = min(candle.open, candle.close)
    body_high = max(candle.open, candle.close)

    wick_intersects = candle.high >= boundary.low and candle.low <= boundary.high
    body_intersects = body_high >= boundary.low and body_low <= boundary.high
    open_inside = boundary.low <= candle.open <= boundary.high
    close_inside = boundary.low <= candle.close <= boundary.high

    full_candle_above = candle.low > boundary.high
    full_candle_below = candle.high < boundary.low
    body_above = body_low >= boundary.high
    body_below = body_high <= boundary.low

    if wick_intersects:
        nearest_distance = 0.0
    elif candle.low > boundary.high:
        nearest_distance = candle.low - boundary.high
    else:
        nearest_distance = boundary.low - candle.high

    penetration_below = max(boundary.low - candle.low, 0.0)
    penetration_above = max(candle.high - boundary.high, 0.0)

    return CandleBoundaryInteraction(
        candle_low=candle.low,
        candle_high=candle.high,
        body_low=body_low,
        body_high=body_high,
        open=candle.open,
        close=candle.close,
        boundary_low=boundary.low,
        boundary_high=boundary.high,
        wick_intersects=wick_intersects,
        body_intersects=body_intersects,
        open_inside=open_inside,
        close_inside=close_inside,
        full_candle_above=full_candle_above,
        full_candle_below=full_candle_below,
        body_above=body_above,
        body_below=body_below,
        nearest_distance=nearest_distance,
        penetration_below=penetration_below,
        penetration_above=penetration_above,
    )
