from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class InterpretationLevel(StrEnum):
    DIRECT = "DIRECT"
    PARAPHRASE = "PARAPHRASE"
    SUPPORTED_INFERENCE = "SUPPORTED_INFERENCE"
    ANALYST_INFERENCE = "ANALYST_INFERENCE"
    UNKNOWN = "UNKNOWN"


class CodingPermission(StrEnum):
    CAN_CONSIDER_CONFIRMED = "CAN_CONSIDER_CONFIRMED"
    REQUIRES_SOURCE_CROSSCHECK = "REQUIRES_SOURCE_CROSSCHECK"
    RESEARCH_ONLY = "RESEARCH_ONLY"
    HYPOTHESIS_ONLY = "HYPOTHESIS_ONLY"
    QUARANTINE = "QUARANTINE"


@dataclass(frozen=True, slots=True)
class EvidenceClaim:
    claim_id: str
    claim_text: str
    source_origin: str
    source_id: str
    source_locator: str | None
    source_actor: str
    capture_method: str
    extraction_method: str
    transformation_chain: tuple[str, ...]
    interpretation_level: InterpretationLevel
    verbatim_available: bool
    source_media_available: bool

    def __post_init__(self) -> None:
        if not self.claim_id or not self.claim_text:
            raise ValueError("claim_id and claim_text are required")
        if not self.source_origin or not self.source_id:
            raise ValueError("source_origin and source_id are required")
        if not self.source_actor or not self.capture_method or not self.extraction_method:
            raise ValueError("source actor/capture/extraction metadata are required")


def coding_permission(claim: EvidenceClaim) -> CodingPermission:
    """Return the strongest coding status allowed by provenance alone.

    Provenance permission does not prove that the trading rule itself is
    correct or mechanically complete. It only limits how strongly the claim
    may be used before source cross-checking.
    """

    if claim.interpretation_level is InterpretationLevel.DIRECT:
        if claim.source_locator and (claim.verbatim_available or claim.source_media_available):
            return CodingPermission.CAN_CONSIDER_CONFIRMED
        return CodingPermission.REQUIRES_SOURCE_CROSSCHECK

    if claim.interpretation_level is InterpretationLevel.PARAPHRASE:
        return CodingPermission.REQUIRES_SOURCE_CROSSCHECK

    if claim.interpretation_level is InterpretationLevel.SUPPORTED_INFERENCE:
        return CodingPermission.RESEARCH_ONLY

    if claim.interpretation_level is InterpretationLevel.ANALYST_INFERENCE:
        return CodingPermission.HYPOTHESIS_ONLY

    return CodingPermission.QUARANTINE
