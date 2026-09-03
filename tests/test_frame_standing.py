from nexus_xau.engine.frame_standing import (
    FrameStandingBar,
    FrameStandingConfig,
    evaluate_frame_standing,
)
from nexus_xau.engine.rules import Decision, EvidenceStatus


def _bar(open_: float, close: float, low: float, high: float) -> FrameStandingBar:
    return FrameStandingBar(open=open_, high=high, low=low, close=close)


def test_waits_before_minimum_observation_window() -> None:
    result = evaluate_frame_standing(
        side="BUY",
        frame_price=100.0,
        bars_from_first_touch=(
            _bar(100.2, 100.4, 99.9, 100.5),
            _bar(100.3, 100.5, 100.0, 100.6),
            _bar(100.4, 100.6, 100.1, 100.7),
        ),
        config=FrameStandingConfig(),
    )
    assert result.decision is Decision.WAIT
    assert result.evidence_status is EvidenceStatus.CONFIRMED


def test_buy_all_bodies_above_frame_remains_parameterized() -> None:
    bars = tuple(_bar(100.1, 100.4, 99.9, 100.5) for _ in range(4))
    result = evaluate_frame_standing(
        side="BUY",
        frame_price=100.0,
        bars_from_first_touch=bars,
        config=FrameStandingConfig(),
    )
    assert result.decision is Decision.WAIT
    assert result.evidence_status is EvidenceStatus.PARAMETERIZED
    assert any("4/4" in reason for reason in result.reasons)


def test_sell_wrong_side_variant_can_reject() -> None:
    bars = tuple(_bar(100.2, 100.5, 100.1, 100.6) for _ in range(4))
    result = evaluate_frame_standing(
        side="SELL",
        frame_price=100.0,
        bars_from_first_touch=bars,
        config=FrameStandingConfig(),
    )
    assert result.decision is Decision.REJECT
    assert result.evidence_status is EvidenceStatus.PARAMETERIZED


def test_tolerance_and_fraction_are_explicit_research_parameters() -> None:
    bars = tuple(_bar(99.9, 100.2, 99.8, 100.3) for _ in range(4))
    strict = evaluate_frame_standing(
        side="BUY",
        frame_price=100.0,
        bars_from_first_touch=bars,
        config=FrameStandingConfig(
            tolerance_price=0.0,
            minimum_body_fraction_on_correct_side=1.0,
        ),
    )
    looser = evaluate_frame_standing(
        side="BUY",
        frame_price=100.0,
        bars_from_first_touch=bars,
        config=FrameStandingConfig(
            tolerance_price=0.1,
            minimum_body_fraction_on_correct_side=0.5,
        ),
    )
    assert strict.decision is Decision.REJECT
    assert looser.decision is Decision.WAIT
    assert looser.evidence_status is EvidenceStatus.PARAMETERIZED
