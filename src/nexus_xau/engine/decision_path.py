from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class DecisionAction(StrEnum):
    WAIT = "WAIT"
    SKIP = "SKIP"
    ENTER = "ENTER"
    HOLD = "HOLD"
    REDUCE_RISK = "REDUCE_RISK"
    EXIT = "EXIT"
    ACCEPT_LOSS = "ACCEPT_LOSS"
    RE_ANCHOR = "RE_ANCHOR"
    RE_EVALUATE = "RE_EVALUATE"
    STOP_TRADING_THIS_SETUP = "STOP_TRADING_THIS_SETUP"


class EventType(StrEnum):
    PAT_COMPLETED = "PAT_COMPLETED"
    LOCATION_QUALIFIED = "LOCATION_QUALIFIED"
    LOCATION_REJECTED = "LOCATION_REJECTED"
    POST_SIG_CLOSED = "POST_SIG_CLOSED"
    POST_SIG_VALID = "POST_SIG_VALID"
    POST_SIG_DESTROYED = "POST_SIG_DESTROYED"
    LOWER_TF_CONFIRMED = "LOWER_TF_CONFIRMED"
    LOWER_TF_FAILED = "LOWER_TF_FAILED"
    TP_COMPLETE = "TP_COMPLETE"
    OVERRUN = "OVERRUN"
    OPPOSITE_PA = "OPPOSITE_PA"
    SIDEWAY_FORMED = "SIDEWAY_FORMED"
    BODY_ZONE_TOUCHED = "BODY_ZONE_TOUCHED"
    BODY_ZONE_RETIRED = "BODY_ZONE_RETIRED"
    INVALIDATION = "INVALIDATION"
    OTHER = "OTHER"


@dataclass(frozen=True, slots=True)
class DecisionTransitionRecord:
    """One no-hindsight decision step inside a multi-event setup path.

    This is a research/audit record, not an execution command. It stores what
    was knowable at decision time so later outcome analysis can score a policy
    without rewriting the decision after future bars are revealed.
    """

    path_id: str
    event_index: int
    event_time: datetime
    visible_data_until: datetime
    state_before: str
    event_type: EventType
    evidence_available: tuple[str, ...]
    candidate_actions: tuple[DecisionAction, ...]
    chosen_action: DecisionAction
    rule_ids_used: tuple[str, ...]
    state_after: str
    future_data_used: bool = False

    def __post_init__(self) -> None:
        if not self.path_id:
            raise ValueError("path_id is required")
        if self.event_index < 1:
            raise ValueError("event_index must start at 1")
        if self.event_time.tzinfo is None or self.visible_data_until.tzinfo is None:
            raise ValueError("event_time and visible_data_until must be timezone-aware")
        if self.visible_data_until > self.event_time:
            raise ValueError("visible_data_until cannot be later than event_time")
        if not self.state_before or not self.state_after:
            raise ValueError("state_before and state_after are required")
        if self.chosen_action not in self.candidate_actions:
            raise ValueError("chosen_action must be one of candidate_actions")
        if self.future_data_used:
            raise ValueError("decision records must be created without future data")


def validate_decision_path(records: tuple[DecisionTransitionRecord, ...]) -> None:
    """Validate ordering and state continuity for one recorded decision path."""

    if not records:
        raise ValueError("decision path must contain at least one record")

    path_id = records[0].path_id
    previous: DecisionTransitionRecord | None = None
    for expected_index, record in enumerate(records, start=1):
        if record.path_id != path_id:
            raise ValueError("all records in one path must share path_id")
        if record.event_index != expected_index:
            raise ValueError("event_index must be contiguous and start at 1")
        if previous is not None:
            if record.event_time < previous.event_time:
                raise ValueError("event_time must be monotonic")
            if record.state_before != previous.state_after:
                raise ValueError("state transition continuity is broken")
        previous = record
