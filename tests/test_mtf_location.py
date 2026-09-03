from nexus_xau.engine.location import (
    LocationContext,
    LocationSide,
    LocationSourceType,
)
from nexus_xau.engine.mtf_location import evaluate_higher_tf_location_guard
from nexus_xau.engine.rules import Decision, EvidenceStatus


def _ctx(side: LocationSide, *, qualifies: bool | None, timeframe: str) -> LocationContext:
    return LocationContext(
        source_type=LocationSourceType.MANUAL_SUPPORT_RESISTANCE,
        side=side,
        timeframe=timeframe,
        qualifies=qualifies,
    )


def test_qualified_higher_tf_conflict_rejects_lower_tf_buy() -> None:
    result = evaluate_higher_tf_location_guard(
        trade_side="BUY",
        lower_context=_ctx(LocationSide.SUPPORT, qualifies=True, timeframe="M5"),
        higher_context=_ctx(LocationSide.RESISTANCE, qualifies=True, timeframe="H4"),
    )

    assert result.decision is Decision.REJECT
    assert result.evidence_status is EvidenceStatus.CONFIRMED


def test_unresolved_higher_tf_context_waits() -> None:
    result = evaluate_higher_tf_location_guard(
        trade_side="SELL",
        lower_context=_ctx(LocationSide.RESISTANCE, qualifies=True, timeframe="M5"),
        higher_context=_ctx(LocationSide.SUPPORT, qualifies=None, timeframe="H1"),
    )

    assert result.decision is Decision.WAIT
    assert result.evidence_status is EvidenceStatus.PARAMETERIZED


def test_noncontradicting_higher_tf_does_not_auto_promote_take() -> None:
    result = evaluate_higher_tf_location_guard(
        trade_side="SELL",
        lower_context=_ctx(LocationSide.RESISTANCE, qualifies=True, timeframe="M5"),
        higher_context=_ctx(LocationSide.RESISTANCE, qualifies=True, timeframe="H4"),
    )

    assert result.decision is Decision.WAIT
    assert result.evidence_status is EvidenceStatus.PARAMETERIZED


def test_rejected_higher_tf_context_cannot_override() -> None:
    result = evaluate_higher_tf_location_guard(
        trade_side="BUY",
        lower_context=_ctx(LocationSide.SUPPORT, qualifies=True, timeframe="M5"),
        higher_context=_ctx(LocationSide.RESISTANCE, qualifies=False, timeframe="H4"),
    )

    assert result.decision is Decision.WAIT
    assert result.evidence_status is EvidenceStatus.CONFIRMED


def test_explicitly_rejected_lower_context_rejects_even_without_conflict() -> None:
    result = evaluate_higher_tf_location_guard(
        trade_side="BUY",
        lower_context=_ctx(LocationSide.SUPPORT, qualifies=False, timeframe="M5"),
        higher_context=_ctx(LocationSide.SUPPORT, qualifies=True, timeframe="H4"),
    )

    assert result.decision is Decision.REJECT
    assert result.evidence_status is EvidenceStatus.CONFIRMED
