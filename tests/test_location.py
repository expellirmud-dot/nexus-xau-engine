from nexus_xau.engine.location import (
    LocationContext,
    LocationSide,
    LocationSourceType,
    evaluate_location_context,
)
from nexus_xau.engine.rules import Decision, EvidenceStatus


def test_buy_requires_support() -> None:
    result = evaluate_location_context(
        trade_side="BUY",
        context=LocationContext(
            source_type=LocationSourceType.WICK_CONTACT_FRAME,
            side=LocationSide.RESISTANCE,
            qualifies=True,
        ),
    )
    assert result.decision is Decision.REJECT
    assert result.evidence_status is EvidenceStatus.CONFIRMED


def test_sell_requires_resistance() -> None:
    result = evaluate_location_context(
        trade_side="SELL",
        context=LocationContext(
            source_type=LocationSourceType.MAE_PLA_STAT_FRAME,
            side=LocationSide.SUPPORT,
            qualifies=True,
        ),
    )
    assert result.decision is Decision.REJECT


def test_unknown_source_fails_closed() -> None:
    result = evaluate_location_context(
        trade_side="BUY",
        context=LocationContext(
            source_type=LocationSourceType.UNKNOWN,
            side=LocationSide.SUPPORT,
            qualifies=True,
        ),
    )
    assert result.decision is Decision.WAIT
    assert result.evidence_status is EvidenceStatus.HUMAN_CONFIRM


def test_known_source_without_family_tolerance_stays_parameterized() -> None:
    result = evaluate_location_context(
        trade_side="BUY",
        context=LocationContext(
            source_type=LocationSourceType.WICK_CONTACT_FRAME,
            side=LocationSide.SUPPORT,
            qualifies=None,
        ),
    )
    assert result.decision is Decision.WAIT
    assert result.evidence_status is EvidenceStatus.PARAMETERIZED


def test_externally_qualified_location_can_pass_semantics() -> None:
    result = evaluate_location_context(
        trade_side="SELL",
        context=LocationContext(
            source_type=LocationSourceType.BODY_COLLECTION_ZONE,
            side=LocationSide.RESISTANCE,
            qualifies=True,
        ),
    )
    assert result.decision is Decision.TAKE
    assert result.evidence_status is EvidenceStatus.CONFIRMED
