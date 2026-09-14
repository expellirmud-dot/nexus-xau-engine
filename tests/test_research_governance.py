import json
from copy import deepcopy
from pathlib import Path

import pytest

from nexus_xau.governance.research_governance import (
    GOVERNANCE_SCHEMA_VERSION,
    RQ_ADMISSION_GOVERNANCE_SCHEMA_VERSION,
    build_legacy_claim_fingerprints,
    validate_claim_store,
    validate_fixture,
    validate_queue_governance,
    validate_rq_admission,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "tests" / "fixtures" / "wo055" / "governance_matrix.json"


def _matrix() -> dict:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    "case",
    [case for case in _matrix()["known_failure_cases"] if case["validator"] != "report"],
    ids=lambda case: case["id"],
)
def test_frozen_governance_failure_reason_codes(case: dict) -> None:
    result = validate_fixture(case["validator"], case["payload"])
    assert result["status"] == "FAIL"
    assert result["reason"] == case["expected_reason"]


@pytest.mark.parametrize(
    "case",
    _matrix()["valid_cases"],
    ids=lambda case: case["id"],
)
def test_frozen_valid_governance_cases(case: dict) -> None:
    result = validate_fixture(case["validator"], case["payload"])
    assert result["status"] == case["expected_status"]


def test_current_canonical_claim_store_remains_valid_before_migration() -> None:
    store = json.loads(
        (ROOT / "docs" / "CANONICAL_CLAIM_REGISTER_2026-09-03.json").read_text(
            encoding="utf-8"
        )
    )
    result = validate_claim_store(store)
    assert result == {"status": "PASS", "claim_count": 45}


def test_legacy_fingerprint_baseline_detects_silent_authority_sensitive_change() -> None:
    claim = {
        "claim_id": "LEGACY",
        "canonical_statement": "A",
        "status": "ACTIVE_SOURCE_BACKED",
        "engine_permission": "NONE",
        "source_refs": ["docs/a.md"],
        "risk_flags": [],
    }
    store = {"claims": [claim]}
    fingerprints = build_legacy_claim_fingerprints(store["claims"])
    migrated = {
        "claims": [deepcopy(claim)],
        "governance": {
            "schema_version": GOVERNANCE_SCHEMA_VERSION,
            "legacy_claim_fingerprints": fingerprints,
        },
    }

    assert validate_claim_store(migrated)["status"] == "PASS"

    migrated["claims"][0]["canonical_statement"] = "Changed without governance"
    result = validate_claim_store(migrated)
    assert result["status"] == "FAIL"
    assert result["reason"] == "LEGACY_CLAIM_CHANGED_WITHOUT_GOVERNANCE"


def test_candidate_admission_rejects_existing_rq_identity() -> None:
    admission = deepcopy(
        next(case for case in _matrix()["valid_cases"] if case["id"] == "VC_ADMISSION")[
            "payload"
        ]
    )
    result = validate_rq_admission(admission, existing_rq_ids={admission["rq_id"]})
    assert result["status"] == "FAIL"
    assert result["reason"] == "RQ_ADMISSION_DUPLICATE_OR_ALREADY_CLOSED"
    assert result["admission_result"] == "BLOCKED_DUPLICATE_OR_ALREADY_CLOSED"


def test_migrated_claim_store_rejects_new_ungoverned_claim_outside_legacy_baseline() -> None:
    legacy = {
        "claim_id": "LEGACY",
        "canonical_statement": "A",
        "status": "ACTIVE_SOURCE_BACKED",
        "engine_permission": "NONE",
        "source_refs": ["docs/a.md"],
        "risk_flags": [],
    }
    store = {
        "claims": [legacy],
        "governance": {
            "schema_version": GOVERNANCE_SCHEMA_VERSION,
            "legacy_claim_fingerprints": build_legacy_claim_fingerprints([legacy]),
        },
    }
    assert validate_claim_store(store)["status"] == "PASS"

    store["claims"].append(
        {
            "claim_id": "NEW_UNGOVERNED",
            "canonical_statement": "B",
            "status": "ACTIVE",
            "engine_permission": "NONE",
            "source_refs": ["docs/b.md"],
            "risk_flags": [],
        }
    )
    result = validate_claim_store(store)
    assert result["status"] == "FAIL"
    assert result["reason"] == "UNGOVERNED_CLAIM_NOT_IN_LEGACY_BASELINE"


def test_queue_admission_enforcement_blocks_active_without_admission() -> None:
    queue = {
        "governance": {
            "schema_version": RQ_ADMISSION_GOVERNANCE_SCHEMA_VERSION,
            "admission_required_for_activation": True,
        },
        "admissions": {},
        "items": [{"id": "RQ-999"}],
        "active": {"id": "RQ-999"},
    }
    result = validate_queue_governance(queue)
    assert result["status"] == "FAIL"
    assert result["reason"] == "RQ_ADMISSION_MISSING_FOR_ACTIVE_RQ"


def test_queue_admission_enforcement_accepts_valid_active_admission() -> None:
    admission = deepcopy(
        next(case for case in _matrix()["valid_cases"] if case["id"] == "VC_ADMISSION")[
            "payload"
        ]
    )
    active_id = admission["rq_id"]
    queue = {
        "governance": {
            "schema_version": RQ_ADMISSION_GOVERNANCE_SCHEMA_VERSION,
            "admission_required_for_activation": True,
        },
        "admissions": {active_id: admission},
        "items": [{"id": active_id}],
        "active": {"id": active_id},
    }
    result = validate_queue_governance(queue)
    assert result == {"status": "PASS", "migrated": True, "active_rq": active_id}
