from nexus_xau.research.evidence_provenance import (
    ClaimLifecycle,
    CodingPermission,
    CrosscheckStatus,
    EvidenceClaim,
    InterpretationLevel,
    SourceRisk,
    coding_permission,
)


def _claim(**overrides: object) -> EvidenceClaim:
    data: dict[str, object] = {
        "claim_id": "c1",
        "claim_text": "Teaching material references 07:00.",
        "source_origin": "PRIMARY_IMAGE",
        "source_id": "book_photo_0700",
        "source_locator": "page/slide visible in project image intake",
        "source_actor": "instructor",
        "capture_method": "image",
        "extraction_method": "human_extraction",
        "transformation_chain": (),
        "interpretation_level": InterpretationLevel.DIRECT,
        "verbatim_available": False,
        "source_media_available": True,
    }
    data.update(overrides)
    return EvidenceClaim(**data)  # type: ignore[arg-type]


def test_traceable_direct_claim_can_be_considered_for_confirmation() -> None:
    assert coding_permission(_claim()) is CodingPermission.CAN_CONSIDER_CONFIRMED


def test_direct_claim_without_locator_requires_crosscheck() -> None:
    claim = _claim(source_locator=None)
    assert coding_permission(claim) is CodingPermission.REQUIRES_SOURCE_CROSSCHECK


def test_paraphrase_never_inherits_direct_confirmation() -> None:
    claim = _claim(interpretation_level=InterpretationLevel.PARAPHRASE)
    assert coding_permission(claim) is CodingPermission.REQUIRES_SOURCE_CROSSCHECK


def test_supported_inference_is_research_only() -> None:
    claim = _claim(
        claim_text="07:00 likely means Asia/Bangkok.",
        interpretation_level=InterpretationLevel.SUPPORTED_INFERENCE,
        transformation_chain=("timezone_inference",),
    )
    assert coding_permission(claim) is CodingPermission.RESEARCH_ONLY


def test_analyst_inference_is_hypothesis_only() -> None:
    claim = _claim(
        interpretation_level=InterpretationLevel.ANALYST_INFERENCE,
        transformation_chain=("analyst_rewrite",),
    )
    assert coding_permission(claim) is CodingPermission.HYPOTHESIS_ONLY


def test_unknown_interpretation_is_quarantined() -> None:
    claim = _claim(
        interpretation_level=InterpretationLevel.UNKNOWN,
        extraction_method="unknown",
    )
    assert coding_permission(claim) is CodingPermission.QUARANTINE


def test_superseded_claim_is_quarantined_even_if_old_source_was_direct() -> None:
    claim = _claim(lifecycle=ClaimLifecycle.SUPERSEDED)
    assert coding_permission(claim) is CodingPermission.QUARANTINE


def test_uncrosschecked_youtube_asr_direct_claim_requires_crosscheck() -> None:
    claim = _claim(
        source_origin="ORIGINAL_INSTRUCTOR_VIDEO",
        capture_method="YOUTUBE_SHOW_TRANSCRIPT",
        extraction_method="YOUTUBE_AUTO_CAPTION_ASR",
        source_risks=(SourceRisk.ASR_RISK,),
        verbatim_available=True,
        source_media_available=False,
        crosscheck_status=CrosscheckStatus.PENDING,
    )
    assert coding_permission(claim) is CodingPermission.REQUIRES_SOURCE_CROSSCHECK


def test_user_confirmed_asr_claim_can_return_to_direct_permission() -> None:
    claim = _claim(
        source_origin="ORIGINAL_INSTRUCTOR_VIDEO",
        capture_method="YOUTUBE_SHOW_TRANSCRIPT",
        extraction_method="YOUTUBE_AUTO_CAPTION_ASR",
        source_risks=(SourceRisk.ASR_RISK,),
        verbatim_available=True,
        source_media_available=False,
        crosscheck_status=CrosscheckStatus.USER_CONFIRMED,
    )
    assert coding_permission(claim) is CodingPermission.CAN_CONSIDER_CONFIRMED
