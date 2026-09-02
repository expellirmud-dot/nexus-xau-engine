from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class CandleDirection(StrEnum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    DOJI = "DOJI"


@dataclass(frozen=True, slots=True)
class CandleFeatures:
    """Deterministic OHLC geometry with no strategy thresholds embedded.

    The engine may safely compute these raw features before PAT thresholds are
    resolved. Whether a body is "small" or a wick is "long" remains a separate,
    evidence-tagged rule decision.
    """

    open: float
    high: float
    low: float
    close: float
    is_closed: bool = True

    def __post_init__(self) -> None:
        if self.high < self.low:
            raise ValueError("high must be >= low")
        if self.high < max(self.open, self.close):
            raise ValueError("high must be >= open and close")
        if self.low > min(self.open, self.close):
            raise ValueError("low must be <= open and close")

    @property
    def direction(self) -> CandleDirection:
        if self.close > self.open:
            return CandleDirection.BULLISH
        if self.close < self.open:
            return CandleDirection.BEARISH
        return CandleDirection.DOJI

    @property
    def range(self) -> float:
        return self.high - self.low

    @property
    def body(self) -> float:
        return abs(self.close - self.open)

    @property
    def upper_wick(self) -> float:
        return self.high - max(self.open, self.close)

    @property
    def lower_wick(self) -> float:
        return min(self.open, self.close) - self.low

    @property
    def body_fraction_of_range(self) -> float | None:
        if self.range == 0:
            return None
        return self.body / self.range

    @property
    def body_midpoint(self) -> float:
        return (self.open + self.close) / 2.0

    @property
    def full_range_midpoint(self) -> float:
        return (self.high + self.low) / 2.0
