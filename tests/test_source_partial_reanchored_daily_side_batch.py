from __future__ import annotations

from nexus_xau.research.source_partial_reanchored_daily_side_batch import (
    cross_period_decision,
)


def test_cross_period_support_requires_two_support_and_no_oppose() -> None:
    assert cross_period_decision(["SUPPORT", "SUPPORT", "INSUFFICIENT"]) == (
        "SUPPORTED_AFTER_SOURCE_PARTIAL_REANCHOR"
    )


def test_cross_period_conflict_is_not_stable() -> None:
    assert cross_period_decision(["SUPPORT", "OPPOSE", "INSUFFICIENT"]) == (
        "NOT_STABLE_AFTER_SOURCE_PARTIAL_REANCHOR"
    )


def test_cross_period_oppose_requires_two_periods() -> None:
    assert cross_period_decision(["OPPOSE", "OPPOSE", "MIXED"]) == (
        "NOT_SUPPORTED_AFTER_SOURCE_PARTIAL_REANCHOR"
    )


def test_cross_period_otherwise_inconclusive() -> None:
    assert cross_period_decision(["SUPPORT", "MIXED", "INSUFFICIENT"]) == (
        "INCONCLUSIVE_AFTER_SOURCE_PARTIAL_REANCHOR"
    )
