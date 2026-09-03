from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from nexus_xau.engine.decision_path import (
    DecisionAction,
    DecisionTransitionRecord,
    EventType,
    validate_decision_path,
)
from nexus_xau.engine.rules import Decision, RuleDecision


@dataclass(frozen=True, slots=True)
class PatSequenceInput:
    path_id: str
    pat_completed_at: datetime
    location_decision: RuleDecision | None = None
    location_known_at: datetime | None = None
    post_sig_decision: RuleDecision | None = None
    post_sig_known_at: datetime | None = None


def build_pat_location_postsig_path(
    sequence: PatSequenceInput,
) -> tuple[DecisionTransitionRecord, ...]:
    """Build a no-hindsight PAT -> location -> post-SIG research path.

    This function intentionally stops at unresolved gates. A qualified PA is not
    interpreted as an entry order. A non-destroyed post-SIG partial check is not
    promoted to a valid SIG until the remaining source rules are frozen.
    """

    if sequence.pat_completed_at.tzinfo is None:
        raise ValueError("pat_completed_at must be timezone-aware")

    records: list[DecisionTransitionRecord] = [
        DecisionTransitionRecord(
            path_id=sequence.path_id,
            event_index=1,
            event_time=sequence.pat_completed_at,
            visible_data_until=sequence.pat_completed_at,
            state_before="WATCH",
            event_type=EventType.PAT_COMPLETED,
            evidence_available=("closed PAT candidate completed",),
            candidate_actions=(DecisionAction.WAIT, DecisionAction.SKIP),
            chosen_action=DecisionAction.WAIT,
            rule_ids_used=("PAT_CANDIDATE",),
            state_after="WAIT_LOCATION",
        )
    ]

    if sequence.location_decision is None:
        return tuple(records)
    if sequence.location_known_at is None:
        raise ValueError("location_known_at is required when location_decision is supplied")
    if sequence.location_known_at.tzinfo is None:
        raise ValueError("location_known_at must be timezone-aware")
    if sequence.location_known_at < sequence.pat_completed_at:
        raise ValueError("location cannot be known before PAT completion in this path")

    location = sequence.location_decision
    if location.decision is Decision.REJECT:
        records.append(
            DecisionTransitionRecord(
                path_id=sequence.path_id,
                event_index=2,
                event_time=sequence.location_known_at,
                visible_data_until=sequence.location_known_at,
                state_before="WAIT_LOCATION",
                event_type=EventType.LOCATION_REJECTED,
                evidence_available=tuple(location.reasons),
                candidate_actions=(DecisionAction.SKIP, DecisionAction.RE_EVALUATE),
                chosen_action=DecisionAction.SKIP,
                rule_ids_used=(location.rule,),
                state_after="LOCATION_REJECTED",
            )
        )
        validate_decision_path(tuple(records))
        return tuple(records)

    if location.decision is Decision.WAIT:
        records.append(
            DecisionTransitionRecord(
                path_id=sequence.path_id,
                event_index=2,
                event_time=sequence.location_known_at,
                visible_data_until=sequence.location_known_at,
                state_before="WAIT_LOCATION",
                event_type=EventType.OTHER,
                evidence_available=tuple(location.reasons),
                candidate_actions=(DecisionAction.WAIT,),
                chosen_action=DecisionAction.WAIT,
                rule_ids_used=(location.rule,),
                state_after="WAIT_LOCATION_RULE",
            )
        )
        validate_decision_path(tuple(records))
        return tuple(records)

    records.append(
        DecisionTransitionRecord(
            path_id=sequence.path_id,
            event_index=2,
            event_time=sequence.location_known_at,
            visible_data_until=sequence.location_known_at,
            state_before="WAIT_LOCATION",
            event_type=EventType.LOCATION_QUALIFIED,
            evidence_available=tuple(location.reasons),
            candidate_actions=(DecisionAction.WAIT, DecisionAction.SKIP),
            chosen_action=DecisionAction.WAIT,
            rule_ids_used=(location.rule,),
            state_after="WAIT_POST_SIG",
        )
    )

    if sequence.post_sig_decision is None:
        validate_decision_path(tuple(records))
        return tuple(records)
    if sequence.post_sig_known_at is None:
        raise ValueError("post_sig_known_at is required when post_sig_decision is supplied")
    if sequence.post_sig_known_at.tzinfo is None:
        raise ValueError("post_sig_known_at must be timezone-aware")
    if sequence.post_sig_known_at < sequence.location_known_at:
        raise ValueError("post-SIG decision cannot precede location decision")

    post_sig = sequence.post_sig_decision
    if post_sig.decision is Decision.REJECT:
        records.append(
            DecisionTransitionRecord(
                path_id=sequence.path_id,
                event_index=3,
                event_time=sequence.post_sig_known_at,
                visible_data_until=sequence.post_sig_known_at,
                state_before="WAIT_POST_SIG",
                event_type=EventType.POST_SIG_DESTROYED,
                evidence_available=tuple(post_sig.reasons),
                candidate_actions=(DecisionAction.RE_EVALUATE, DecisionAction.SKIP),
                chosen_action=DecisionAction.RE_EVALUATE,
                rule_ids_used=(post_sig.rule,),
                state_after="REEVALUATE_OR_SIDEWAY",
            )
        )
    else:
        records.append(
            DecisionTransitionRecord(
                path_id=sequence.path_id,
                event_index=3,
                event_time=sequence.post_sig_known_at,
                visible_data_until=sequence.post_sig_known_at,
                state_before="WAIT_POST_SIG",
                event_type=EventType.POST_SIG_CLOSED,
                evidence_available=tuple(post_sig.reasons),
                candidate_actions=(DecisionAction.WAIT,),
                chosen_action=DecisionAction.WAIT,
                rule_ids_used=(post_sig.rule,),
                state_after="WAIT_FULL_SIG_VALIDATION",
            )
        )

    validate_decision_path(tuple(records))
    return tuple(records)
