from __future__ import annotations

from nexus_xau.engine.rules import Decision, EvidenceStatus, RuleDecision


class PatDetector:
    """Safe starter contract for PAT detection.

    Exact production PAT detection is intentionally not implemented yet.
    Current evidence still leaves numeric geometry/tolerances unresolved
    (for example PAT1 wick/body ratio, PAT2/PAT3 50% measurement basis,
    small-body thresholds, and support/resistance proximity tolerance).
    """

    def evaluate(self) -> RuleDecision:
        return RuleDecision(
            rule="PAT",
            decision=Decision.WAIT,
            evidence_status=EvidenceStatus.NOT_IMPLEMENTED,
            reasons=[
                "Exact PAT numeric thresholds are unresolved; detector fails closed.",
                "See CURRENT_ENGINE_SPEC_2026-09-02.md and DIRECT_PAT_GEOMETRY_RULES_2026-09-01.md.",
            ],
        )
