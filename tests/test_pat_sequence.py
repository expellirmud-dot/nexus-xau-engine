from datetime import UTC, datetime

from nexus_xau.engine.pat_sequence import PatSequenceInput, build_pat_location_postsig_path
from nexus_xau.engine.rules import Decision, EvidenceStatus, RuleDecision


def _dt(minute: int) -> datetime:
    return datetime(2026, 9, 3, 6, minute, tzinfo=UTC)


def _rule(name: str, decision: Decision, status: EvidenceStatus, reason: str) -> RuleDecision:
    return RuleDecision(rule=name, decision=decision, evidence_status=status, reasons=[reason])


def test_path_stops_after_pat_when_location_missing() -> None:
    path = build_pat_location_postsig_path(
        PatSequenceInput(path_id="p1", pat_completed_at=_dt(1))
    )

    assert len(path) == 1
    assert path[-1].state_after == "WAIT_LOCATION"


def test_unresolved_location_waits_without_postsig() -> None:
    path = build_pat_location_postsig_path(
        PatSequenceInput(
            path_id="p1",
            pat_completed_at=_dt(1),
            location_decision=_rule(
                "PA_LOCATION",
                Decision.WAIT,
                EvidenceStatus.PARAMETERIZED,
                "touch tolerance unresolved",
            ),
            location_known_at=_dt(2),
        )
    )

    assert len(path) == 2
    assert path[-1].chosen_action.value == "WAIT"
    assert path[-1].state_after == "WAIT_LOCATION_RULE"


def test_wrong_location_stops_setup() -> None:
    path = build_pat_location_postsig_path(
        PatSequenceInput(
            path_id="p1",
            pat_completed_at=_dt(1),
            location_decision=_rule(
                "PA_LOCATION",
                Decision.REJECT,
                EvidenceStatus.CONFIRMED,
                "BUY at resistance",
            ),
            location_known_at=_dt(2),
        )
    )

    assert len(path) == 2
    assert path[-1].event_type.value == "LOCATION_REJECTED"
    assert path[-1].chosen_action.value == "SKIP"


def test_qualified_location_then_destroyed_postsig_reevaluates() -> None:
    path = build_pat_location_postsig_path(
        PatSequenceInput(
            path_id="p1",
            pat_completed_at=_dt(1),
            location_decision=_rule(
                "PA_LOCATION",
                Decision.TAKE,
                EvidenceStatus.CONFIRMED,
                "support qualified",
            ),
            location_known_at=_dt(2),
            post_sig_decision=_rule(
                "POST_SIG_EXTREME_DESTRUCTION",
                Decision.REJECT,
                EvidenceStatus.CONFIRMED,
                "post-SIG exceeds PA",
            ),
            post_sig_known_at=_dt(3),
        )
    )

    assert len(path) == 3
    assert path[1].state_after == "WAIT_POST_SIG"
    assert path[-1].event_type.value == "POST_SIG_DESTROYED"
    assert path[-1].chosen_action.value == "RE_EVALUATE"
    assert path[-1].state_after == "REEVALUATE_OR_SIDEWAY"


def test_non_destroyed_partial_postsig_still_waits() -> None:
    path = build_pat_location_postsig_path(
        PatSequenceInput(
            path_id="p1",
            pat_completed_at=_dt(1),
            location_decision=_rule(
                "PA_LOCATION",
                Decision.TAKE,
                EvidenceStatus.CONFIRMED,
                "support qualified",
            ),
            location_known_at=_dt(2),
            post_sig_decision=_rule(
                "POST_SIG_EXTREME_DESTRUCTION",
                Decision.WAIT,
                EvidenceStatus.PARAMETERIZED,
                "inside PA extreme but full validity unresolved",
            ),
            post_sig_known_at=_dt(3),
        )
    )

    assert len(path) == 3
    assert path[-1].event_type.value == "POST_SIG_CLOSED"
    assert path[-1].chosen_action.value == "WAIT"
    assert path[-1].state_after == "WAIT_FULL_SIG_VALIDATION"
