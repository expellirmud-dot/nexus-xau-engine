from datetime import UTC, datetime

import pytest

from nexus_xau.engine.decision_path import (
    DecisionAction,
    DecisionTransitionRecord,
    EventType,
    validate_decision_path,
)


def _dt(minute: int) -> datetime:
    return datetime(2026, 9, 3, 5, minute, tzinfo=UTC)


def test_record_rejects_future_data() -> None:
    with pytest.raises(ValueError, match="without future data"):
        DecisionTransitionRecord(
            path_id="p1",
            event_index=1,
            event_time=_dt(1),
            visible_data_until=_dt(1),
            state_before="WATCH",
            event_type=EventType.PAT_COMPLETED,
            evidence_available=("PAT2 BUY closed",),
            candidate_actions=(DecisionAction.WAIT, DecisionAction.ENTER),
            chosen_action=DecisionAction.WAIT,
            rule_ids_used=("PAT2_TOPOLOGY",),
            state_after="WAIT_LOCATION",
            future_data_used=True,
        )


def test_record_requires_chosen_action_to_be_available() -> None:
    with pytest.raises(ValueError, match="candidate_actions"):
        DecisionTransitionRecord(
            path_id="p1",
            event_index=1,
            event_time=_dt(1),
            visible_data_until=_dt(1),
            state_before="WATCH",
            event_type=EventType.PAT_COMPLETED,
            evidence_available=("PAT2 BUY closed",),
            candidate_actions=(DecisionAction.WAIT,),
            chosen_action=DecisionAction.ENTER,
            rule_ids_used=("PAT2_TOPOLOGY",),
            state_after="ENTERED",
        )


def test_multi_event_path_validates_state_continuity() -> None:
    records = (
        DecisionTransitionRecord(
            path_id="p1",
            event_index=1,
            event_time=_dt(1),
            visible_data_until=_dt(1),
            state_before="WATCH",
            event_type=EventType.PAT_COMPLETED,
            evidence_available=("PAT2 BUY closed",),
            candidate_actions=(DecisionAction.WAIT, DecisionAction.SKIP),
            chosen_action=DecisionAction.WAIT,
            rule_ids_used=("PAT2_TOPOLOGY",),
            state_after="WAIT_LOCATION",
        ),
        DecisionTransitionRecord(
            path_id="p1",
            event_index=2,
            event_time=_dt(2),
            visible_data_until=_dt(2),
            state_before="WAIT_LOCATION",
            event_type=EventType.LOCATION_QUALIFIED,
            evidence_available=("support source family qualified",),
            candidate_actions=(DecisionAction.WAIT, DecisionAction.ENTER),
            chosen_action=DecisionAction.ENTER,
            rule_ids_used=("PA_LOCATION",),
            state_after="SIG_ACTIVE",
        ),
        DecisionTransitionRecord(
            path_id="p1",
            event_index=3,
            event_time=_dt(3),
            visible_data_until=_dt(3),
            state_before="SIG_ACTIVE",
            event_type=EventType.POST_SIG_DESTROYED,
            evidence_available=("post-SIG reference destroyed",),
            candidate_actions=(
                DecisionAction.EXIT,
                DecisionAction.ACCEPT_LOSS,
                DecisionAction.RE_EVALUATE,
            ),
            chosen_action=DecisionAction.RE_EVALUATE,
            rule_ids_used=("POST_SIG_INVALIDATION",),
            state_after="REEVALUATE",
        ),
    )

    validate_decision_path(records)


def test_path_rejects_broken_state_continuity() -> None:
    first = DecisionTransitionRecord(
        path_id="p1",
        event_index=1,
        event_time=_dt(1),
        visible_data_until=_dt(1),
        state_before="WATCH",
        event_type=EventType.PAT_COMPLETED,
        evidence_available=("PAT",),
        candidate_actions=(DecisionAction.WAIT,),
        chosen_action=DecisionAction.WAIT,
        rule_ids_used=(),
        state_after="WAIT_LOCATION",
    )
    second = DecisionTransitionRecord(
        path_id="p1",
        event_index=2,
        event_time=_dt(2),
        visible_data_until=_dt(2),
        state_before="WRONG_STATE",
        event_type=EventType.LOCATION_QUALIFIED,
        evidence_available=("support",),
        candidate_actions=(DecisionAction.ENTER,),
        chosen_action=DecisionAction.ENTER,
        rule_ids_used=(),
        state_after="SIG_ACTIVE",
    )

    with pytest.raises(ValueError, match="continuity"):
        validate_decision_path((first, second))
