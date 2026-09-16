from __future__ import annotations

from copy import deepcopy

from nexus_xau.reporting.pilot_operations import (
    HEALTH_FAIL,
    HEALTH_PASS,
    HEALTH_UNKNOWN,
    archive_health_check,
    build_pilot_operations_snapshot,
    collector_health_check,
)


def _state():
    return {
        "state_authority": {
            "latest_progress_checkpoint": "docs/checkpoint.md"
        },
        "origin_history_initialization_next": {
            "status": "STRUCTURAL_BLOCKER_CURRENT_EVIDENCE_ROUTES_EXHAUSTED",
            "closure": "docs/origin-closure.md",
            "real_exness_state": "DATA_EXCLUDED_ORIGIN_HISTORY_UNSEEDED",
        },
    }


def _readiness():
    return {
        "components": [
            {
                "id": "P1-08",
                "component": "origin seed",
                "status": "BLOCKING",
                "blocks": ["MULTI_YEAR"],
                "missing": ["origin seed evidence"],
                "evidence_refs": ["docs/origin-closure.md"],
            },
            {
                "id": "P1-13",
                "component": "pilot operations",
                "status": "PARTIAL",
                "blocks": [],
                "missing": ["future confirmation"],
                "evidence_refs": ["docs/pilot.md"],
            },
        ]
    }


def _registry():
    return {
        "entries": [
            {
                "id": "U-STRUCTURAL",
                "readiness_component_id": "P1-08",
                "readiness_missing": "origin seed evidence",
                "status": "OPEN",
                "epistemic_class": "STRUCTURAL_UNKNOWN",
                "blocking_axis": "BLOCKING",
                "resolution_basis": "needs new external evidence",
                "evidence_refs": ["docs/origin-closure.md"],
            },
            {
                "id": "U-FUTURE",
                "readiness_component_id": "P1-13",
                "readiness_missing": "future confirmation",
                "status": "OPEN",
                "epistemic_class": "RUNTIME_OBSERVABLE",
                "blocking_axis": "REQUIRED_LATER",
                "resolution_basis": "future event not yet observed",
                "evidence_refs": ["docs/pilot.md"],
            },
        ]
    }


def _git_identity():
    return {
        "head": "a" * 40,
        "branch": "main",
        "origin_main": "a" * 40,
        "working_tree_clean": True,
    }


def _snapshot(**overrides):
    values = {
        "state": _state(),
        "readiness": _readiness(),
        "registry": _registry(),
        "preflight": {"status": "PASS", "reason": None},
        "health_checks": [
            archive_health_check(window_status="OK", required=True)
        ],
        "git_identity": _git_identity(),
        "project_version": "0700_MINIMAL_V2.0",
        "state_sha256": "b" * 64,
        "registry_sha256": "c" * 64,
        "observed_at_utc": "2026-09-17T00:00:00+00:00",
        "rollback_reference": None,
    }
    values.update(overrides)
    return build_pilot_operations_snapshot(**values)

def test_snapshot_is_deterministic_for_identical_inputs() -> None:
    first = _snapshot()
    second = _snapshot()
    assert first == second


def test_preflight_fail_yields_fail_closed_governance_reason() -> None:
    report = _snapshot(preflight={"status": "FAIL", "reason": "BROKEN"})
    assert report["operational_gate"] == "FAIL_CLOSED"
    assert any(
        item["code"] == "GOVERNANCE_PREFLIGHT_FAIL" for item in report["reasons"]
    )


def test_structural_and_runtime_unknowns_remain_distinct() -> None:
    report = _snapshot()
    classes = {
        item["id"]: (item["epistemic_class"], item["blocking_axis"])
        for item in report["unknowns"]["open"]
    }
    assert classes["U-STRUCTURAL"] == ("STRUCTURAL_UNKNOWN", "BLOCKING")
    assert classes["U-FUTURE"] == ("RUNTIME_OBSERVABLE", "REQUIRED_LATER")


def test_collector_error_yields_health_fail_without_threshold() -> None:
    check = collector_health_check(
        {"state": "ERROR", "last_error": "api failed"}, required_live=True
    )
    assert check["status"] == HEALTH_FAIL
    report = _snapshot(health_checks=[check])
    assert report["data_health"]["overall"] == "FAIL_CLOSED"
    assert any(
        item["code"] == "DATA_HEALTH_FAIL:mt5_collector"
        for item in report["reasons"]
    )


def test_unknown_collector_state_is_unknown_not_pass() -> None:
    check = collector_health_check(
        {"state": "STOPPED", "last_error": None}, required_live=True
    )
    assert check["status"] == HEALTH_UNKNOWN
    report = _snapshot(health_checks=[check])
    assert report["data_health"]["overall"] == HEALTH_UNKNOWN


def test_all_required_health_checks_pass() -> None:
    checks = [
        collector_health_check(
            {"state": "RUNNING", "last_error": None}, required_live=True
        ),
        archive_health_check(window_status="OK", required=True),
    ]
    report = _snapshot(health_checks=checks)
    assert report["data_health"]["overall"] == HEALTH_PASS

def test_git_state_identity_missing_or_inconsistent_never_passes() -> None:
    missing = deepcopy(_git_identity())
    missing["head"] = None
    missing_report = _snapshot(git_identity=missing)
    assert missing_report["identity"]["status"] == HEALTH_UNKNOWN
    assert missing_report["operational_gate"] == "FAIL_CLOSED"

    mismatch = deepcopy(_git_identity())
    mismatch["origin_main"] = "d" * 40
    mismatch_report = _snapshot(git_identity=mismatch)
    assert mismatch_report["identity"]["status"] == HEALTH_FAIL
    assert mismatch_report["identity"]["identity_issue"] == "head_origin_main_mismatch"


def test_rollback_reference_is_non_destructive_reference_only() -> None:
    report = _snapshot(
        rollback_reference={
            "git_commit": "1" * 40,
            "checkpoint": "docs/previous.md",
            "note": "prior verified checkpoint",
            "command": "git reset --hard HEAD~1",
        }
    )
    rollback = report["rollback_reference"]
    assert rollback["mode"] == "REFERENCE_ONLY"
    assert rollback["destructive_action_permitted"] is False
    assert "command" not in rollback
    serialized = str(rollback).lower()
    assert "reset --hard" not in serialized
    assert "force-push" not in serialized


def test_snapshot_guards_keep_execution_and_holdout_disabled() -> None:
    report = _snapshot()
    governance = report["governance"]
    assert governance["order_send"] == "DISABLED"
    assert governance["holdout_scoring"] == "DISABLED"
    assert governance["economic_scoring"] == "DISABLED"
    assert any(
        item["code"] == "REAL_EXNESS_ORIGIN_SEED_UNSEEDED"
        for item in report["reasons"]
    )


def test_output_has_no_performance_or_market_entry_recommendation_fields() -> None:
    report = _snapshot()

    def keys(value):
        result = []
        if isinstance(value, dict):
            for key, nested in value.items():
                result.append(str(key).lower())
                result.extend(keys(nested))
        elif isinstance(value, list):
            for nested in value:
                result.extend(keys(nested))
        return result

    output_keys = set(keys(report))
    forbidden = {
        "win_rate",
        "expectancy",
        "profitability",
        "pnl",
        "broker_fill",
        "market_entry",
        "trade_recommendation",
    }
    assert output_keys.isdisjoint(forbidden)