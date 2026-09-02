from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class EvidenceStatus(StrEnum):
    CONFIRMED = "CONFIRMED"
    PARAMETERIZED = "PARAMETERIZED"
    HUMAN_CONFIRM = "HUMAN_CONFIRM"
    NOT_IMPLEMENTED = "NOT_IMPLEMENTED"


class Decision(StrEnum):
    TAKE = "TAKE"
    WAIT = "WAIT"
    REJECT = "REJECT"


@dataclass(slots=True)
class RuleDecision:
    rule: str
    decision: Decision
    evidence_status: EvidenceStatus
    reasons: list[str] = field(default_factory=list)
