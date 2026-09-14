from __future__ import annotations

from copy import deepcopy

from scripts.research_preflight import validate_finding_ledger


def _canonical():
    return {"claims": [{"claim_id": "CLAIM-1"}]}


def _ledger():
    return {
        "schema_version": "PHASE1_FINDING_LEDGER_V0.1",
        "role": "NON_CANONICAL_RESEARCH_FINDING_INDEX",
        "findings": [
            {
                "finding_id": "FIND-1",
                "relation_key": "A__B",
                "title": "test",
                "status": "RECONCILED",
                "scope": "Phase 1",
                "current_interpretation": "current",
                "observations": [
                    {
                        "observation_id": "OBS-1",
                        "statement": "old",
                        "representation": "r1",
                        "conditions": ["c1"],
                        "evidence_refs": ["AGENTS.md"],
                    },
                    {
                        "observation_id": "OBS-2",
                        "statement": "new",
                        "representation": "r2",
                        "conditions": ["c2"],
                        "evidence_refs": ["PROJECT_BOOTSTRAP.md"],
                    },
                ],
                "reconciliation": {"type": "CONTROL", "statement": "compatible"},
                "canonical_claim_ref": "CLAIM-1",
                "allowed_uses": ["CONTEXT"],
                "forbidden_uses": ["AUTHORITY"],
                "blocking": False,
            }
        ],
    }


def test_finding_ledger_valid():
    result = validate_finding_ledger(_ledger(), _canonical())
    assert result == {"status": "PASS", "finding_count": 1, "observation_count": 2}


def test_finding_ledger_rejects_duplicate_relation_key():
    ledger = _ledger()
    duplicate = deepcopy(ledger["findings"][0])
    duplicate["finding_id"] = "FIND-2"
    duplicate["observations"][0]["observation_id"] = "OBS-3"
    duplicate["observations"][1]["observation_id"] = "OBS-4"
    ledger["findings"].append(duplicate)
    result = validate_finding_ledger(ledger, _canonical())
    assert result["status"] == "FAIL"
    assert result["reason"] == "DUPLICATE_FINDING_RELATION_KEY"


def test_finding_ledger_rejects_unknown_canonical_ref():
    ledger = _ledger()
    ledger["findings"][0]["canonical_claim_ref"] = "MISSING"
    result = validate_finding_ledger(ledger, _canonical())
    assert result["status"] == "FAIL"
    assert result["reason"] == "FINDING_CANONICAL_REF_UNKNOWN"


def test_finding_ledger_rejects_missing_reconciliation():
    ledger = _ledger()
    ledger["findings"][0].pop("reconciliation")
    result = validate_finding_ledger(ledger, _canonical())
    assert result["status"] == "FAIL"
    assert result["reason"] == "FINDING_RECONCILIATION_MISSING"
