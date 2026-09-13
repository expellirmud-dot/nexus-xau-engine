from __future__ import annotations

from copy import deepcopy

from scripts.research_preflight import validate_state_consistency


def _fixtures():
    state = {
        "updated_at": "2026-09-13T19:51:00+07:00",
        "state_authority": {
            "scope": "PROJECT_CURRENT",
            "project_current_research_checkpoint": "docs/rq012.md",
            "latest_state_reconciliation": "docs/state_drift.md",
        },
        "mode": "RESTART_SAFE_HOLDOUT_RESERVED_UNSCORED_NO_ACTIVE_RQ",
        "operational_research_queue": {
            "active_id": None,
            "active_worksheet": None,
            "active_status": None,
            "queue_state": "NO_ACTIVE_DECISION_CRITICAL_RQ_HOLDOUT_RESERVED_UNSCORED",
            "last_closed_id": "RQ-012",
            "last_closure_ref": "docs/rq012.md",
            "latest_checkpoint": "docs/rq012.md",
        },
        "rq012_v0_holdout_ledger_activation": {
            "status": "CLOSED_TOOLING_IMPLEMENTED_ACTIVATION_RESERVED_UNSCORED",
            "worksheet": "research_queue/closed/RQ-012.md",
            "engine_freeze_commit": "75866d2",
            "protocol_freeze_commit": "43c29be",
            "prospective_boundary": "2026-09-14T07:00:00+07:00",
            "holdout_open": False,
            "outcome_scoring_authorized": False,
        },
    }
    queue = {
        "updated_at": "2026-09-13T19:51:00+07:00",
        "active": None,
        "queue_state": "NO_ACTIVE_DECISION_CRITICAL_RQ_HOLDOUT_RESERVED_UNSCORED",
        "items": [
            {
                "id": "RQ-012",
                "status": "CLOSED_TOOLING_IMPLEMENTED_ACTIVATION_RESERVED_UNSCORED",
                "worksheet": "research_queue/closed/RQ-012.md",
                "closure_ref": "docs/rq012.md",
            }
        ],
    }
    workstream = {
        "updated_at": "2026-09-13T19:51:00+07:00",
        "scope": "WORKSTREAM_CURRENT_0700_ONLY",
        "project_active_rq": None,
        "project_queue_state": "NO_ACTIVE_DECISION_CRITICAL_RQ_HOLDOUT_RESERVED_UNSCORED",
        "project_current_checkpoint": "docs/rq012.md",
        "active_question": {
            "rq_id": None,
            "status": "CLOSED_NO_REOPEN_TRIGGER",
        },
    }
    canonical = {"updated_at": "2026-09-13T19:50:00+07:00"}
    ledger = {"updated_at": "2026-09-13T19:50:00+07:00"}
    activation_lock = {
        "engine_freeze_commit": "75866d2",
        "protocol_freeze_commit": "43c29be",
        "prospective_boundary": "2026-09-14T07:00:00+07:00",
        "outcome_scoring_enabled": False,
    }
    return state, queue, canonical, ledger, workstream, activation_lock


def _validate(parts):
    state, queue, canonical, ledger, workstream, activation_lock = parts
    return validate_state_consistency(
        state=state,
        queue=queue,
        canonical=canonical,
        ledger=ledger,
        workstream=workstream,
        activation_lock=activation_lock,
    )


def test_state_consistency_passes_when_project_current_sources_agree():
    assert _validate(_fixtures())["status"] == "PASS"


def test_state_consistency_fails_on_queue_state_drift():
    parts = list(_fixtures())
    parts[1] = deepcopy(parts[1])
    parts[1]["queue_state"] = "DIFFERENT"
    result = _validate(tuple(parts))
    assert result["status"] == "FAIL"
    assert result["reason"] == "PROJECT_QUEUE_POINTER_MISMATCH"


def test_state_consistency_fails_on_workstream_project_pointer_drift():
    parts = list(_fixtures())
    parts[4] = deepcopy(parts[4])
    parts[4]["project_current_checkpoint"] = "docs/old.md"
    result = _validate(tuple(parts))
    assert result["status"] == "FAIL"
    assert result["reason"] == "WORKSTREAM_PROJECT_POINTER_MISMATCH"


def test_state_consistency_fails_on_holdout_identity_drift():
    parts = list(_fixtures())
    parts[5] = deepcopy(parts[5])
    parts[5]["engine_freeze_commit"] = "deadbee"
    result = _validate(tuple(parts))
    assert result["status"] == "FAIL"
    assert result["reason"] == "HOLDOUT_ACTIVATION_IDENTITY_MISMATCH"


def test_state_consistency_fails_on_stale_rq012_implementation_instruction():
    parts = list(_fixtures())
    parts[0] = deepcopy(parts[0])
    parts[0]["rq012_holdout_state"] = {
        "status": "RESERVED_OR_COLLECTION_READY_UNSCORED",
        "note": "Implement tooling next; outcome scoring remains unauthorized.",
    }
    result = _validate(tuple(parts))
    assert result["status"] == "FAIL"
    assert result["reason"] == "RQ012_STALE_IMPLEMENTATION_INSTRUCTION"


def test_state_consistency_fails_if_scoring_is_enabled():
    parts = list(_fixtures())
    parts[5] = deepcopy(parts[5])
    parts[5]["outcome_scoring_enabled"] = True
    result = _validate(tuple(parts))
    assert result["status"] == "FAIL"
    assert result["reason"] == "HOLDOUT_SCORING_ENABLED"
