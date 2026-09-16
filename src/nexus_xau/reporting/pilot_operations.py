from __future__ import annotations

from collections.abc import Mapping, Sequence
from copy import deepcopy
from typing import Any

CONTRACT = "PHASE1_PILOT_OPERATIONS_SCAFFOLD_V0.1"

HEALTH_PASS = "PASS"
HEALTH_FAIL = "FAIL"
HEALTH_UNKNOWN = "UNKNOWN"
HEALTH_NOT_APPLICABLE = "NOT_APPLICABLE"
HEALTH_STATUSES = {
    HEALTH_PASS,
    HEALTH_FAIL,
    HEALTH_UNKNOWN,
    HEALTH_NOT_APPLICABLE,
}

ORDER_SEND_DISABLED = "DISABLED"
HOLDOUT_SCORING_DISABLED = "DISABLED"
ECONOMIC_SCORING_DISABLED = "DISABLED"


class PilotOperationsError(ValueError):
    pass


def collector_health_check(
    status_payload: Mapping[str, Any] | None,
    *,
    required_live: bool = True,
) -> dict[str, Any]:
    if not required_live:
        return {
            "name": "mt5_collector",
            "required": False,
            "status": HEALTH_NOT_APPLICABLE,
            "source": "MT5_COLLECTOR_STATUS",
            "detail": "live collector not required for declared snapshot mode",
        }
    if not isinstance(status_payload, Mapping):
        return {
            "name": "mt5_collector",
            "required": True,
            "status": HEALTH_UNKNOWN,
            "source": "MT5_COLLECTOR_STATUS",
            "detail": "collector status unavailable",
        }

    raw_state = str(status_payload.get("state", "")).upper()
    last_error = status_payload.get("last_error")
    if raw_state in {"ERROR", "BLOCKED"} or bool(last_error):
        status = HEALTH_FAIL
    elif raw_state in {"RUNNING", "BACKFILLING"}:
        status = HEALTH_PASS
    else:
        status = HEALTH_UNKNOWN
    return {
        "name": "mt5_collector",
        "required": True,
        "status": status,
        "source": "MT5_COLLECTOR_STATUS",
        "detail": {
            "collector_state": raw_state or None,
            "mode": status_payload.get("mode"),
            "source_identity": status_payload.get("source_identity"),
            "latest_committed_tick_time_msc": status_payload.get(
                "latest_committed_tick_time_msc"
            ),
            "last_successful_commit_utc": status_payload.get(
                "last_successful_commit_utc"
            ),
            "gap_counts": deepcopy(status_payload.get("gap_counts", {})),
            "last_error": last_error,
        },
    }


def archive_health_check(
    *,
    window_status: str | None,
    error_code: str | None = None,
    required: bool = True,
) -> dict[str, Any]:
    if not required:
        status = HEALTH_NOT_APPLICABLE
    elif error_code:
        status = HEALTH_FAIL
    elif window_status == "OK":
        status = HEALTH_PASS
    else:
        status = HEALTH_UNKNOWN
    return {
        "name": "exness_archive_window",
        "required": required,
        "status": status,
        "source": "EXNESS_ARCHIVE_WINDOW_GUARD",
        "detail": {"window_status": window_status, "error_code": error_code},
    }


def summarize_health(checks: Sequence[Mapping[str, Any]]) -> str:
    required = [check for check in checks if bool(check.get("required", True))]
    if not required:
        return HEALTH_NOT_APPLICABLE
    statuses = [str(check.get("status", HEALTH_UNKNOWN)) for check in required]
    invalid = [status for status in statuses if status not in HEALTH_STATUSES]
    if invalid:
        raise PilotOperationsError(f"invalid health status: {invalid[0]}")
    if HEALTH_FAIL in statuses:
        return "FAIL_CLOSED"
    if HEALTH_UNKNOWN in statuses or HEALTH_NOT_APPLICABLE in statuses:
        return HEALTH_UNKNOWN
    return HEALTH_PASS

def _version_identity(
    *,
    project_version: str,
    checkpoint: str | None,
    state_sha256: str,
    registry_sha256: str,
    git_identity: Mapping[str, Any],
) -> tuple[str, dict[str, Any]]:
    identity = {
        "project_version": project_version or None,
        "git_head": git_identity.get("head"),
        "branch": git_identity.get("branch"),
        "origin_main": git_identity.get("origin_main"),
        "working_tree_clean": git_identity.get("working_tree_clean"),
        "latest_progress_checkpoint": checkpoint,
        "current_state_sha256": state_sha256 or None,
        "unknown_registry_sha256": registry_sha256 or None,
    }
    required = (
        "project_version",
        "git_head",
        "branch",
        "latest_progress_checkpoint",
        "current_state_sha256",
        "unknown_registry_sha256",
    )
    missing = [key for key in required if not identity.get(key)]
    if missing:
        return HEALTH_UNKNOWN, {**identity, "identity_issue": f"missing:{','.join(missing)}"}
    if identity["working_tree_clean"] is False:
        return HEALTH_FAIL, {**identity, "identity_issue": "working_tree_dirty"}
    origin_main = identity.get("origin_main")
    if origin_main and origin_main != identity["git_head"]:
        return HEALTH_FAIL, {**identity, "identity_issue": "head_origin_main_mismatch"}
    return HEALTH_PASS, {**identity, "identity_issue": None}


def _readiness_open_components(readiness: Mapping[str, Any]) -> list[dict[str, Any]]:
    components = readiness.get("components", [])
    if not isinstance(components, list):
        raise PilotOperationsError("readiness components must be a list")
    result: list[dict[str, Any]] = []
    for component in components:
        if not isinstance(component, Mapping):
            continue
        status = str(component.get("status", ""))
        if status not in {"PARTIAL", "BLOCKING"}:
            continue
        result.append(
            {
                "id": component.get("id"),
                "component": component.get("component"),
                "status": status,
                "blocks": deepcopy(component.get("blocks", [])),
                "missing": deepcopy(component.get("missing", [])),
                "evidence_refs": deepcopy(component.get("evidence_refs", [])),
            }
        )
    return sorted(result, key=lambda item: str(item.get("id", "")))


def _open_unknowns(registry: Mapping[str, Any]) -> list[dict[str, Any]]:
    entries = registry.get("entries", [])
    if not isinstance(entries, list):
        raise PilotOperationsError("unknown registry entries must be a list")
    result: list[dict[str, Any]] = []
    for entry in entries:
        if not isinstance(entry, Mapping) or entry.get("status") != "OPEN":
            continue
        result.append(
            {
                "id": entry.get("id"),
                "readiness_component_id": entry.get("readiness_component_id"),
                "readiness_missing": entry.get("readiness_missing"),
                "epistemic_class": entry.get("epistemic_class"),
                "blocking_axis": entry.get("blocking_axis"),
                "resolution_basis": entry.get("resolution_basis"),
                "evidence_refs": deepcopy(entry.get("evidence_refs", [])),
            }
        )
    return sorted(result, key=lambda item: str(item.get("id", "")))


def _rollback_reference(payload: Mapping[str, Any] | None) -> dict[str, Any]:
    result = {
        "mode": "REFERENCE_ONLY",
        "provided": bool(payload),
        "git_commit": None,
        "checkpoint": None,
        "note": None,
        "destructive_action_permitted": False,
    }
    if payload:
        result.update(
            {
                "git_commit": payload.get("git_commit"),
                "checkpoint": payload.get("checkpoint"),
                "note": payload.get("note"),
            }
        )
    return result

def build_pilot_operations_snapshot(
    *,
    state: Mapping[str, Any],
    readiness: Mapping[str, Any],
    registry: Mapping[str, Any],
    preflight: Mapping[str, Any],
    health_checks: Sequence[Mapping[str, Any]],
    git_identity: Mapping[str, Any],
    project_version: str,
    state_sha256: str,
    registry_sha256: str,
    observed_at_utc: str,
    rollback_reference: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    if not observed_at_utc:
        raise PilotOperationsError("observed_at_utc is required")

    authority = state.get("state_authority")
    if not isinstance(authority, Mapping):
        authority = {}
    checkpoint = authority.get("latest_progress_checkpoint")
    version_status, identity = _version_identity(
        project_version=project_version,
        checkpoint=str(checkpoint) if checkpoint else None,
        state_sha256=state_sha256,
        registry_sha256=registry_sha256,
        git_identity=git_identity,
    )

    open_components = _readiness_open_components(readiness)
    open_unknowns = _open_unknowns(registry)
    health = [deepcopy(dict(check)) for check in health_checks]
    health_status = summarize_health(health)
    preflight_status = str(preflight.get("status", HEALTH_UNKNOWN))

    reasons: list[dict[str, Any]] = []
    if preflight_status != HEALTH_PASS:
        reasons.append(
            {
                "code": "GOVERNANCE_PREFLIGHT_FAIL",
                "severity": "BLOCKING",
                "source": "research_preflight",
                "detail": preflight.get("reason"),
                "evidence_refs": ["scripts/research_preflight.py"],
            }
        )

    for component in open_components:
        if component["status"] != "BLOCKING":
            continue
        reasons.append(
            {
                "code": f"READINESS_BLOCKING:{component['id']}",
                "severity": "BLOCKING",
                "source": "PHASE1_READINESS_MATRIX",
                "detail": component["component"],
                "evidence_refs": deepcopy(component["evidence_refs"]),
            }
        )

    for entry in open_unknowns:
        axis = str(entry.get("blocking_axis", ""))
        if axis not in {"BLOCKING", "REQUIRED_LATER", "NON_BLOCKING", "IRRELEVANT"}:
            axis = "BLOCKING"
        reasons.append(
            {
                "code": f"UNKNOWN_{axis}:{entry['id']}",
                "severity": axis,
                "source": "PHASE1_UNKNOWN_CLASSIFICATION_REGISTRY",
                "detail": {
                    "epistemic_class": entry.get("epistemic_class"),
                    "readiness_missing": entry.get("readiness_missing"),
                },
                "evidence_refs": deepcopy(entry["evidence_refs"]),
            }
        )

    for check in health:
        if not bool(check.get("required", True)):
            continue
        status = str(check.get("status", HEALTH_UNKNOWN))
        if status == HEALTH_FAIL:
            reasons.append(
                {
                    "code": f"DATA_HEALTH_FAIL:{check.get('name')}",
                    "severity": "BLOCKING",
                    "source": check.get("source"),
                    "detail": deepcopy(check.get("detail")),
                    "evidence_refs": deepcopy(check.get("evidence_refs", [])),
                }
            )
        elif status in {HEALTH_UNKNOWN, HEALTH_NOT_APPLICABLE}:
            reasons.append(
                {
                    "code": f"DATA_HEALTH_UNKNOWN:{check.get('name')}",
                    "severity": "BLOCKING",
                    "source": check.get("source"),
                    "detail": deepcopy(check.get("detail")),
                    "evidence_refs": deepcopy(check.get("evidence_refs", [])),
                }
            )

    if version_status == HEALTH_FAIL:
        reasons.append(
            {
                "code": "VERSION_IDENTITY_FAIL",
                "severity": "BLOCKING",
                "source": "GIT_AND_CURRENT_STATE",
                "detail": identity.get("identity_issue"),
                "evidence_refs": ["docs/CURRENT_RESEARCH_STATE.json"],
            }
        )
    elif version_status == HEALTH_UNKNOWN:
        reasons.append(
            {
                "code": "VERSION_IDENTITY_UNKNOWN",
                "severity": "BLOCKING",
                "source": "GIT_AND_CURRENT_STATE",
                "detail": identity.get("identity_issue"),
                "evidence_refs": ["docs/CURRENT_RESEARCH_STATE.json"],
            }
        )

    origin_seed = state.get("origin_history_initialization_next")
    if isinstance(origin_seed, Mapping) and origin_seed.get("real_exness_state") == (
        "DATA_EXCLUDED_ORIGIN_HISTORY_UNSEEDED"
    ):
        reasons.append(
            {
                "code": "REAL_EXNESS_ORIGIN_SEED_UNSEEDED",
                "severity": "BLOCKING",
                "source": "CURRENT_RESEARCH_STATE",
                "detail": origin_seed.get("status"),
                "evidence_refs": [
                    str(origin_seed.get("closure"))
                    if origin_seed.get("closure")
                    else "docs/CURRENT_RESEARCH_STATE.json"
                ],
            }
        )

    reasons = sorted(reasons, key=lambda item: str(item.get("code", "")))
    has_blocking_reason = any(reason.get("severity") == "BLOCKING" for reason in reasons)
    if has_blocking_reason:
        operational_gate = "FAIL_CLOSED"
    elif health_status == HEALTH_UNKNOWN or version_status == HEALTH_UNKNOWN:
        operational_gate = HEALTH_UNKNOWN
    else:
        operational_gate = "OBSERVE_ONLY"

    return {
        "contract": CONTRACT,
        "observed_at_utc": observed_at_utc,
        "identity": {**identity, "status": version_status},
        "governance": {
            "preflight_status": preflight_status,
            "preflight_reason": preflight.get("reason"),
            "order_send": ORDER_SEND_DISABLED,
            "holdout_scoring": HOLDOUT_SCORING_DISABLED,
            "economic_scoring": ECONOMIC_SCORING_DISABLED,
        },
        "readiness": {
            "open_components": open_components,
            "blocking_count": sum(
                component["status"] == "BLOCKING" for component in open_components
            ),
            "partial_count": sum(
                component["status"] == "PARTIAL" for component in open_components
            ),
        },
        "unknowns": {
            "open": open_unknowns,
            "open_count": len(open_unknowns),
        },
        "data_health": {
            "overall": health_status,
            "checks": health,
        },
        "reasons": reasons,
        "rollback_reference": _rollback_reference(rollback_reference),
        "operational_gate": operational_gate,
    }