from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from nexus_xau.engine.candles import CandleDirection, CandleFeatures
from nexus_xau.engine.rules import Decision, EvidenceStatus, RuleDecision


class PatKind(StrEnum):
    PAT1 = "PAT1"
    PAT2 = "PAT2"
    PAT3 = "PAT3"


class PatSide(StrEnum):
    BUY = "BUY"
    SELL = "SELL"


@dataclass(frozen=True, slots=True)
class PatWindowSpec:
    kind: PatKind
    candle_count: int
    post_sig_reference_number: int


PAT_WINDOW_SPECS: dict[PatKind, PatWindowSpec] = {
    PatKind.PAT1: PatWindowSpec(PatKind.PAT1, candle_count=1, post_sig_reference_number=2),
    PatKind.PAT2: PatWindowSpec(PatKind.PAT2, candle_count=2, post_sig_reference_number=3),
    PatKind.PAT3: PatWindowSpec(PatKind.PAT3, candle_count=3, post_sig_reference_number=4),
}


def get_pat_window_spec(kind: PatKind) -> PatWindowSpec:
    return PAT_WINDOW_SPECS[kind]


def _wait_for_open_candle(kind: PatKind) -> RuleDecision:
    return RuleDecision(
        rule=kind.value,
        decision=Decision.WAIT,
        evidence_status=EvidenceStatus.CONFIRMED,
        reasons=["PAT classification requires closed candles on the working timeframe."],
    )


def _wrong_location(kind: PatKind, side: PatSide) -> RuleDecision:
    required = "support" if side is PatSide.BUY else "resistance"
    return RuleDecision(
        rule=kind.value,
        decision=Decision.REJECT,
        evidence_status=EvidenceStatus.CONFIRMED,
        reasons=[f"{side.value} PAT is valid only at {required}."],
    )


def _location_unresolved(kind: PatKind, side: PatSide) -> RuleDecision:
    required = "support" if side is PatSide.BUY else "resistance"
    return RuleDecision(
        rule=kind.value,
        decision=Decision.WAIT,
        evidence_status=EvidenceStatus.HUMAN_CONFIRM,
        reasons=[
            f"Topology passed the currently deterministic checks, but {required} qualification was not supplied.",
            "Exact support/resistance proximity tolerance remains unresolved.",
        ],
    )


def evaluate_pat_topology(
    *,
    kind: PatKind,
    side: PatSide,
    candles: tuple[CandleFeatures, ...],
    at_required_location: bool | None = None,
) -> RuleDecision:
    """Evaluate only PAT facts that current project evidence makes deterministic.

    This intentionally does not guess PAT1 wick/body thresholds, PAT2/PAT3 50%
    measurement basis, PAT3 small-body threshold, PAT3 SELL equal-wick tolerance,
    or support/resistance distance tolerance.
    """
    spec = get_pat_window_spec(kind)
    if len(candles) != spec.candle_count:
        raise ValueError(
            f"{kind.value} requires {spec.candle_count} candles, got {len(candles)}"
        )

    if any(not candle.is_closed for candle in candles):
        return _wait_for_open_candle(kind)

    if at_required_location is False:
        return _wrong_location(kind, side)

    if kind is PatKind.PAT1:
        if at_required_location is None:
            return _location_unresolved(kind, side)
        return RuleDecision(
            rule=kind.value,
            decision=Decision.WAIT,
            evidence_status=EvidenceStatus.PARAMETERIZED,
            reasons=[
                "PAT1 location is valid, but exact long-wick/small-body numeric thresholds remain unresolved.",
            ],
        )

    if kind is PatKind.PAT2:
        c1, c2 = candles
        expected = (
            (CandleDirection.BEARISH, CandleDirection.BULLISH)
            if side is PatSide.BUY
            else (CandleDirection.BULLISH, CandleDirection.BEARISH)
        )
        actual = (c1.direction, c2.direction)
        if actual != expected:
            return RuleDecision(
                rule=kind.value,
                decision=Decision.REJECT,
                evidence_status=EvidenceStatus.CONFIRMED,
                reasons=[
                    f"{side.value} PAT2 requires candle colors {expected[0].value} -> {expected[1].value}; got {actual[0].value} -> {actual[1].value}."
                ],
            )
        if at_required_location is None:
            return _location_unresolved(kind, side)
        return RuleDecision(
            rule=kind.value,
            decision=Decision.WAIT,
            evidence_status=EvidenceStatus.PARAMETERIZED,
            reasons=[
                "PAT2 color order and location passed.",
                "The >50% close rule cannot be finalized until its BODY-vs-FULL_RANGE measurement basis and tolerance are resolved.",
            ],
        )

    c1, c2, c3 = candles
    expected_c1 = (
        CandleDirection.BEARISH if side is PatSide.BUY else CandleDirection.BULLISH
    )
    expected_c3 = (
        CandleDirection.BULLISH if side is PatSide.BUY else CandleDirection.BEARISH
    )
    if c1.direction is not expected_c1:
        return RuleDecision(
            rule=kind.value,
            decision=Decision.REJECT,
            evidence_status=EvidenceStatus.CONFIRMED,
            reasons=[f"{side.value} PAT3 candle #1 must be {expected_c1.value}."],
        )
    if c2.direction is CandleDirection.DOJI:
        return RuleDecision(
            rule=kind.value,
            decision=Decision.REJECT,
            evidence_status=EvidenceStatus.CONFIRMED,
            reasons=["PAT3 candle #2 is stated as green or red; an exact doji does not satisfy that topology."],
        )
    if c3.direction is not expected_c3:
        return RuleDecision(
            rule=kind.value,
            decision=Decision.REJECT,
            evidence_status=EvidenceStatus.CONFIRMED,
            reasons=[f"{side.value} PAT3 candle #3 must be {expected_c3.value}."],
        )
    if at_required_location is None:
        return _location_unresolved(kind, side)

    unresolved = [
        "PAT3 candle #2 small-body numeric threshold remains unresolved.",
        "PAT3 >50% close measurement basis/tolerance remains unresolved.",
    ]
    if side is PatSide.SELL:
        unresolved.append(
            "PAT3 SELL candle #2 equal-upper/lower-wick numeric tolerance remains unresolved."
        )
    return RuleDecision(
        rule=kind.value,
        decision=Decision.WAIT,
        evidence_status=EvidenceStatus.PARAMETERIZED,
        reasons=[f"{side.value} PAT3 confirmed color topology and location passed.", *unresolved],
    )


class PatDetector:
    """Safe PAT detector facade.

    The no-argument method remains as the original smoke-test guard. Production
    qualification should call ``evaluate_topology`` and must still fail closed on
    unresolved numeric geometry.
    """

    def evaluate(self) -> RuleDecision:
        return RuleDecision(
            rule="PAT",
            decision=Decision.WAIT,
            evidence_status=EvidenceStatus.NOT_IMPLEMENTED,
            reasons=[
                "Exact PAT numeric thresholds are unresolved; detector fails closed.",
                "Use evaluate_topology for deterministic topology prechecks only.",
            ],
        )

    def evaluate_topology(
        self,
        *,
        kind: PatKind,
        side: PatSide,
        candles: tuple[CandleFeatures, ...],
        at_required_location: bool | None = None,
    ) -> RuleDecision:
        return evaluate_pat_topology(
            kind=kind,
            side=side,
            candles=candles,
            at_required_location=at_required_location,
        )
