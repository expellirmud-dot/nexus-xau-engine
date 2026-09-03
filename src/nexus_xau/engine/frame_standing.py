from __future__ import annotations

from dataclasses import dataclass

from nexus_xau.engine.rules import Decision, EvidenceStatus, RuleDecision


@dataclass(frozen=True, slots=True)
class FrameStandingBar:
    open: float
    high: float
    low: float
    close: float

    def __post_init__(self) -> None:
        if self.high < max(self.open, self.close):
            raise ValueError("high must be >= open and close")
        if self.low > min(self.open, self.close):
            raise ValueError("low must be <= open and close")

    @property
    def body_low(self) -> float:
        return min(self.open, self.close)

    @property
    def body_high(self) -> float:
        return max(self.open, self.close)


@dataclass(frozen=True, slots=True)
class FrameStandingConfig:
    """Research-only parameters for the partially evidenced frame-standing rule."""

    tolerance_price: float = 0.0
    minimum_bars: int = 4
    maximum_bars: int = 10
    minimum_body_fraction_on_correct_side: float = 1.0

    def __post_init__(self) -> None:
        if self.tolerance_price < 0:
            raise ValueError("tolerance_price must be >= 0")
        if self.minimum_bars < 1:
            raise ValueError("minimum_bars must be >= 1")
        if self.maximum_bars < self.minimum_bars:
            raise ValueError("maximum_bars must be >= minimum_bars")
        if not 0.0 <= self.minimum_body_fraction_on_correct_side <= 1.0:
            raise ValueError("minimum_body_fraction_on_correct_side must be between 0 and 1")


def _body_fraction_on_correct_side(
    bar: FrameStandingBar,
    *,
    side: str,
    frame_price: float,
    tolerance_price: float,
) -> float:
    body_low = bar.body_low
    body_high = bar.body_high
    body_size = body_high - body_low
    boundary = frame_price - tolerance_price if side == "BUY" else frame_price + tolerance_price

    if body_size == 0:
        if side == "BUY":
            return 1.0 if bar.close >= boundary else 0.0
        return 1.0 if bar.close <= boundary else 0.0

    if side == "BUY":
        correct = max(0.0, body_high - max(body_low, boundary))
    else:
        correct = max(0.0, min(body_high, boundary) - body_low)
    return min(correct / body_size, 1.0)


def evaluate_frame_standing(
    *,
    side: str,
    frame_price: float,
    bars_from_first_touch: tuple[FrameStandingBar, ...],
    config: FrameStandingConfig,
) -> RuleDecision:
    """Evaluate a parameterized version of the source-backed frame-standing concept.

    Evidence supports:
    - count from the first candle touching the frame;
    - observe roughly 4-10 closed candles on M1/M5;
    - primarily evaluate candle bodies standing on the correct side;
    - wick-on-line may be secondary.

    Exact tolerance and all-vs-majority requirements are unresolved, so even a
    passing research variant remains PARAMETERIZED rather than CONFIRMED.
    """

    normalized_side = side.upper()
    if normalized_side not in {"BUY", "SELL"}:
        raise ValueError("side must be BUY or SELL")

    count = len(bars_from_first_touch)
    if count < config.minimum_bars:
        return RuleDecision(
            rule="FRAME_STANDING",
            decision=Decision.WAIT,
            evidence_status=EvidenceStatus.CONFIRMED,
            reasons=[
                f"Only {count} closed bars observed from first frame touch.",
                f"Primary transcript uses an approximately {config.minimum_bars}-{config.maximum_bars} bar observation window.",
            ],
        )

    observed = bars_from_first_touch[: config.maximum_bars]
    fractions = tuple(
        _body_fraction_on_correct_side(
            bar,
            side=normalized_side,
            frame_price=frame_price,
            tolerance_price=config.tolerance_price,
        )
        for bar in observed
    )
    qualifying = sum(
        fraction >= config.minimum_body_fraction_on_correct_side for fraction in fractions
    )

    if qualifying == 0:
        return RuleDecision(
            rule="FRAME_STANDING",
            decision=Decision.REJECT,
            evidence_status=EvidenceStatus.PARAMETERIZED,
            reasons=[
                "No observed candle body satisfies the configured correct-side standing variant.",
                "Numeric tolerance and aggregation threshold remain research parameters.",
            ],
        )

    return RuleDecision(
        rule="FRAME_STANDING",
        decision=Decision.WAIT,
        evidence_status=EvidenceStatus.PARAMETERIZED,
        reasons=[
            f"{qualifying}/{len(observed)} observed bodies satisfy the configured correct-side standing variant.",
            "Source supports body-standing over a 4-10 candle observation window, but exact tolerance and all-vs-majority rule remain unresolved.",
        ],
    )
