from __future__ import annotations

from dataclasses import dataclass

from nexus_xau.engine.rules import Decision, EvidenceStatus, RuleDecision


@dataclass(frozen=True, slots=True)
class PostSigExtremeContext:
    """Minimal source-backed geometry for one post-SIG destruction check.

    The transcript supports rejection when the post-SIG reference disturbs or
    extends beyond the PA extreme. Passing this one check is not sufficient to
    declare a valid SIG because frame interaction and full wick semantics remain
    unresolved.
    """

    side: str
    pa_low: float
    pa_high: float
    post_sig_low: float
    post_sig_high: float

    def __post_init__(self) -> None:
        if self.pa_high < self.pa_low:
            raise ValueError("pa_high must be >= pa_low")
        if self.post_sig_high < self.post_sig_low:
            raise ValueError("post_sig_high must be >= post_sig_low")
        if self.side.upper() not in {"BUY", "SELL"}:
            raise ValueError("side must be BUY or SELL")


def evaluate_post_sig_extreme(context: PostSigExtremeContext) -> RuleDecision:
    """Reject a post-SIG reference that clearly exceeds the PA extreme.

    Confirmed partial rule:
    - BUY: post-SIG reference must not extend below the PA low.
    - SELL: post-SIG reference must not extend above the PA high.

    If the reference remains inside the PA extreme, return WAIT/PARAMETERIZED;
    other validity requirements are intentionally not guessed.
    """

    side = context.side.upper()
    if side == "BUY" and context.post_sig_low < context.pa_low:
        return RuleDecision(
            rule="POST_SIG_EXTREME_DESTRUCTION",
            decision=Decision.REJECT,
            evidence_status=EvidenceStatus.CONFIRMED,
            reasons=[
                "BUY post-SIG reference extends below the PA low.",
                "Primary transcript evidence treats a post-SIG wick that disturbs/exceeds the PA as destroyed.",
            ],
        )

    if side == "SELL" and context.post_sig_high > context.pa_high:
        return RuleDecision(
            rule="POST_SIG_EXTREME_DESTRUCTION",
            decision=Decision.REJECT,
            evidence_status=EvidenceStatus.CONFIRMED,
            reasons=[
                "SELL post-SIG reference extends above the PA high.",
                "Primary transcript evidence treats a post-SIG wick that disturbs/exceeds the PA as destroyed.",
            ],
        )

    return RuleDecision(
        rule="POST_SIG_EXTREME_DESTRUCTION",
        decision=Decision.WAIT,
        evidence_status=EvidenceStatus.PARAMETERIZED,
        reasons=[
            "Post-SIG reference does not exceed the PA extreme under this partial check.",
            "Full post-SIG validity still requires unresolved frame/wick qualification; do not promote to valid SIG yet.",
        ],
    )
