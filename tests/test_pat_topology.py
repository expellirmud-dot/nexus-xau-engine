from nexus_xau.detectors.pat import (
    PatKind,
    PatSide,
    evaluate_pat_topology,
    get_pat_window_spec,
)
from nexus_xau.engine.candles import CandleFeatures
from nexus_xau.engine.rules import Decision, EvidenceStatus


def _bull(*, closed: bool = True) -> CandleFeatures:
    return CandleFeatures(open=100.0, high=106.0, low=98.0, close=104.0, is_closed=closed)


def _bear(*, closed: bool = True) -> CandleFeatures:
    return CandleFeatures(open=104.0, high=106.0, low=98.0, close=100.0, is_closed=closed)


def test_pat_reference_mapping_is_fixed() -> None:
    assert get_pat_window_spec(PatKind.PAT1).candle_count == 1
    assert get_pat_window_spec(PatKind.PAT1).post_sig_reference_number == 2
    assert get_pat_window_spec(PatKind.PAT2).candle_count == 2
    assert get_pat_window_spec(PatKind.PAT2).post_sig_reference_number == 3
    assert get_pat_window_spec(PatKind.PAT3).candle_count == 3
    assert get_pat_window_spec(PatKind.PAT3).post_sig_reference_number == 4


def test_open_candle_waits_even_when_topology_looks_valid() -> None:
    result = evaluate_pat_topology(
        kind=PatKind.PAT2,
        side=PatSide.BUY,
        candles=(_bear(), _bull(closed=False)),
        at_required_location=True,
    )

    assert result.decision is Decision.WAIT
    assert result.evidence_status is EvidenceStatus.CONFIRMED


def test_wrong_location_is_hard_reject() -> None:
    result = evaluate_pat_topology(
        kind=PatKind.PAT2,
        side=PatSide.BUY,
        candles=(_bear(), _bull()),
        at_required_location=False,
    )

    assert result.decision is Decision.REJECT
    assert result.evidence_status is EvidenceStatus.CONFIRMED


def test_pat2_buy_color_order_can_pass_only_to_parameterized_stage() -> None:
    result = evaluate_pat_topology(
        kind=PatKind.PAT2,
        side=PatSide.BUY,
        candles=(_bear(), _bull()),
        at_required_location=True,
    )

    assert result.decision is Decision.WAIT
    assert result.evidence_status is EvidenceStatus.PARAMETERIZED
    assert any("50%" in reason for reason in result.reasons)


def test_pat2_wrong_color_order_rejects() -> None:
    result = evaluate_pat_topology(
        kind=PatKind.PAT2,
        side=PatSide.BUY,
        candles=(_bull(), _bear()),
        at_required_location=True,
    )

    assert result.decision is Decision.REJECT
    assert result.evidence_status is EvidenceStatus.CONFIRMED


def test_missing_location_waits_for_human_confirmation() -> None:
    result = evaluate_pat_topology(
        kind=PatKind.PAT2,
        side=PatSide.SELL,
        candles=(_bull(), _bear()),
        at_required_location=None,
    )

    assert result.decision is Decision.WAIT
    assert result.evidence_status is EvidenceStatus.HUMAN_CONFIRM


def test_pat3_sell_topology_does_not_guess_numeric_geometry() -> None:
    result = evaluate_pat_topology(
        kind=PatKind.PAT3,
        side=PatSide.SELL,
        candles=(_bull(), _bear(), _bear()),
        at_required_location=True,
    )

    assert result.decision is Decision.WAIT
    assert result.evidence_status is EvidenceStatus.PARAMETERIZED
    assert any("equal-upper/lower-wick" in reason for reason in result.reasons)
