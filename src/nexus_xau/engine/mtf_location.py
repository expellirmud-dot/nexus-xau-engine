from __future__ import annotations

from nexus_xau.engine.location import (
    LocationContext,
    required_location_for_trade_side,
)
from nexus_xau.engine.rules import Decision, EvidenceStatus, RuleDecision


def evaluate_higher_tf_location_guard(
    *,
    trade_side: str,
    lower_context: LocationContext | None,
    higher_context: LocationContext | None,
) -> RuleDecision:
    """Guard a lower-TF PA from an explicitly qualified higher-TF conflict.

    Primary transcript evidence supports only the semantic precedence that a
    larger-timeframe S/R context is stronger than a small-timeframe look-alike.
    It does not close a full timeframe conflict matrix. Therefore this function
    can reject a known, qualified higher-TF contradiction, but it does not rank
    multiple higher frames or manufacture a TAKE decision.
    """

    required = required_location_for_trade_side(trade_side)

    if lower_context is None:
        return RuleDecision(
            rule="MTF_LOCATION_GUARD",
            decision=Decision.WAIT,
            evidence_status=EvidenceStatus.HUMAN_CONFIRM,
            reasons=["Lower-timeframe location context is missing."],
        )

    if higher_context is None:
        return RuleDecision(
            rule="MTF_LOCATION_GUARD",
            decision=Decision.WAIT,
            evidence_status=EvidenceStatus.PARAMETERIZED,
            reasons=[
                "No higher-timeframe context was supplied.",
                "The source does not require one universal higher-TF gate for every setup.",
            ],
        )

    if higher_context.qualifies is None:
        return RuleDecision(
            rule="MTF_LOCATION_GUARD",
            decision=Decision.WAIT,
            evidence_status=EvidenceStatus.PARAMETERIZED,
            reasons=[
                "Higher-timeframe location exists but its qualification is unresolved.",
                "Do not resolve a timeframe conflict from an unqualified frame/zone.",
            ],
        )

    if higher_context.qualifies is False:
        return RuleDecision(
            rule="MTF_LOCATION_GUARD",
            decision=Decision.WAIT,
            evidence_status=EvidenceStatus.CONFIRMED,
            reasons=[
                "Supplied higher-timeframe context does not qualify at this event.",
                "No higher-TF override can be inferred from a rejected context.",
            ],
        )

    if higher_context.side is not required:
        return RuleDecision(
            rule="MTF_LOCATION_GUARD",
            decision=Decision.REJECT,
            evidence_status=EvidenceStatus.CONFIRMED,
            reasons=[
                (
                    f"Qualified higher-timeframe {higher_context.side.value.lower()} "
                    f"conflicts with required {required.value.lower()} for {trade_side.upper()}."
                ),
                "Primary transcript states larger-timeframe location context is stronger than a small-TF look-alike.",
            ],
        )

    if lower_context.qualifies is False:
        return RuleDecision(
            rule="MTF_LOCATION_GUARD",
            decision=Decision.REJECT,
            evidence_status=EvidenceStatus.CONFIRMED,
            reasons=["Lower-timeframe location itself is explicitly rejected."],
        )

    return RuleDecision(
        rule="MTF_LOCATION_GUARD",
        decision=Decision.WAIT,
        evidence_status=EvidenceStatus.PARAMETERIZED,
        reasons=[
            "Higher-timeframe context does not contradict the trade side.",
            "The full multi-timeframe priority/confluence matrix is still unresolved, so this guard cannot promote a TAKE decision.",
        ],
    )
