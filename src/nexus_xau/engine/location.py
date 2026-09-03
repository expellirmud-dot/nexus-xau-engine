from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from nexus_xau.engine.rules import Decision, EvidenceStatus, RuleDecision


class LocationSide(StrEnum):
    SUPPORT = "SUPPORT"
    RESISTANCE = "RESISTANCE"


class LocationSourceType(StrEnum):
    """Source family for support/resistance context.

    These values intentionally separate evidence-backed frame/zone families so
    research does not collapse them into one generic S/R detector.
    """

    MAE_PLA_STAT_FRAME = "MAE_PLA_STAT_FRAME"
    WICK_CONTACT_FRAME = "WICK_CONTACT_FRAME"
    BODY_COLLECTION_ZONE = "BODY_COLLECTION_ZONE"
    POR_CHON_ATH_FRAME = "POR_CHON_ATH_FRAME"
    SIDEWAY_FRAME = "SIDEWAY_FRAME"
    MANUAL_SUPPORT_RESISTANCE = "MANUAL_SUPPORT_RESISTANCE"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True, slots=True)
class LocationContext:
    source_type: LocationSourceType
    side: LocationSide
    timeframe: str | None = None
    frame_id: str | None = None
    price: float | None = None
    zone_low: float | None = None
    zone_high: float | None = None
    distance_points: float | None = None
    qualifies: bool | None = None
    evidence_note: str | None = None


def required_location_for_trade_side(side: str) -> LocationSide:
    normalized = side.upper()
    if normalized == "BUY":
        return LocationSide.SUPPORT
    if normalized == "SELL":
        return LocationSide.RESISTANCE
    raise ValueError(f"Unsupported trade side: {side}")


def evaluate_location_context(*, trade_side: str, context: LocationContext | None) -> RuleDecision:
    """Evaluate only evidence-backed location semantics.

    This function does not invent a universal distance tolerance. `qualifies`
    must come from a source-family-specific detector or human label. When that
    family-specific qualification is unavailable, the engine fails closed.
    """

    required = required_location_for_trade_side(trade_side)

    if context is None:
        return RuleDecision(
            rule="PA_LOCATION",
            decision=Decision.WAIT,
            evidence_status=EvidenceStatus.HUMAN_CONFIRM,
            reasons=[
                f"{trade_side.upper()} PA requires {required.value.lower()} context.",
                "No location context was supplied.",
            ],
        )

    if context.side is not required:
        return RuleDecision(
            rule="PA_LOCATION",
            decision=Decision.REJECT,
            evidence_status=EvidenceStatus.CONFIRMED,
            reasons=[
                (
                    f"{trade_side.upper()} PA requires {required.value.lower()}, "
                    f"but supplied context is {context.side.value.lower()}."
                ),
            ],
        )

    if context.source_type is LocationSourceType.UNKNOWN:
        return RuleDecision(
            rule="PA_LOCATION",
            decision=Decision.WAIT,
            evidence_status=EvidenceStatus.HUMAN_CONFIRM,
            reasons=[
                "Support/resistance side matches, but the source family is unknown.",
                "Do not promote a generic untraceable line to a valid PA location.",
            ],
        )

    if context.qualifies is False:
        return RuleDecision(
            rule="PA_LOCATION",
            decision=Decision.REJECT,
            evidence_status=EvidenceStatus.CONFIRMED,
            reasons=[
                f"{context.source_type.value} was supplied but did not qualify the candidate location.",
            ],
        )

    if context.qualifies is None:
        return RuleDecision(
            rule="PA_LOCATION",
            decision=Decision.WAIT,
            evidence_status=EvidenceStatus.PARAMETERIZED,
            reasons=[
                f"{context.source_type.value} matches the required {required.value.lower()} side.",
                "The source-family-specific touch/proximity rule is not yet deterministic.",
            ],
        )

    return RuleDecision(
        rule="PA_LOCATION",
        decision=Decision.TAKE,
        evidence_status=EvidenceStatus.CONFIRMED,
        reasons=[
            (
                f"Candidate is externally/source-family qualified at {required.value.lower()} "
                f"via {context.source_type.value}."
            ),
            "This does not imply that one universal S/R tolerance has been solved.",
        ],
    )
