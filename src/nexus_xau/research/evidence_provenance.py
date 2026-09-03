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


class ClaimLifecycle(StrEnum):
    ACTIVE = "ACTIVE"
    SUPERSEDED = "SUPERSEDED"
    QUARANTINED = "QUARANTINED"


class SourceRisk(StrEnum):
    ASR_RISK = "ASR_RISK"
    STT_RISK = "STT_RISK"


class CrosscheckStatus(StrEnum):
    NOT_REQUIRED = "NOT_REQUIRED"
    PENDING = "PENDING"
    VERIFIED_SOURCE = "VERIFIED_SOURCE"
    USER_CONFIRMED = "USER_CONFIRMED"


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
    lifecycle: ClaimLifecycle = ClaimLifecycle.ACTIVE
    source_risks: tuple[SourceRisk, ...] = ()
    crosscheck_status: CrosscheckStatus = CrosscheckStatus.NOT_REQUIRED

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

    A historical claim that has been superseded/quarantined can never regain
    coding authority merely because its old source was strong. Likewise,
    ASR/STT-risk wording that could materially change a rule must be
    cross-checked before it can be considered confirmed.
    """

    if claim.lifecycle is not ClaimLifecycle.ACTIVE:
        return CodingPermission.QUARANTINE

    has_speech_recognition_risk = any(
        risk in {SourceRisk.ASR_RISK, SourceRisk.STT_RISK}
        for risk in claim.source_risks
    )
    risk_crosschecked = claim.crosscheck_status in {
        CrosscheckStatus.VERIFIED_SOURCE,
        CrosscheckStatus.USER_CONFIRMED,
    }

    if claim.interpretation_level is InterpretationLevel.DIRECT:
        if has_speech_recognition_risk and not risk_crosschecked:
            return CodingPermission.REQUIRES_SOURCE_CROSSCHECK
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
