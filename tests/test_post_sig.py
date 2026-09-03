from nexus_xau.engine.post_sig import PostSigExtremeContext, evaluate_post_sig_extreme
from nexus_xau.engine.rules import Decision, EvidenceStatus


def test_buy_post_sig_below_pa_low_is_destroyed() -> None:
    result = evaluate_post_sig_extreme(
        PostSigExtremeContext(
            side="BUY",
            pa_low=100.0,
            pa_high=110.0,
            post_sig_low=99.5,
            post_sig_high=108.0,
        )
    )
    assert result.decision is Decision.REJECT
    assert result.evidence_status is EvidenceStatus.CONFIRMED


def test_sell_post_sig_above_pa_high_is_destroyed() -> None:
    result = evaluate_post_sig_extreme(
        PostSigExtremeContext(
            side="SELL",
            pa_low=100.0,
            pa_high=110.0,
            post_sig_low=102.0,
            post_sig_high=110.5,
        )
    )
    assert result.decision is Decision.REJECT
    assert result.evidence_status is EvidenceStatus.CONFIRMED


def test_inside_pa_extreme_is_not_promoted_to_valid_sig() -> None:
    result = evaluate_post_sig_extreme(
        PostSigExtremeContext(
            side="BUY",
            pa_low=100.0,
            pa_high=110.0,
            post_sig_low=100.0,
            post_sig_high=108.0,
        )
    )
    assert result.decision is Decision.WAIT
    assert result.evidence_status is EvidenceStatus.PARAMETERIZED
    assert any("do not promote" in reason.lower() for reason in result.reasons)
