from __future__ import annotations

import hashlib
import json
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from typing import Any

GOVERNANCE_SCHEMA_VERSION = "WO055_RESEARCH_GOVERNANCE_V0.1"
RQ_ADMISSION_SCHEMA_VERSION = "WO055_RQ_ADMISSION_V0.1"
CLAIM_GOVERNANCE_SCHEMA_VERSION = "WO055_CLAIM_GOVERNANCE_V0.1"
RQ_ADMISSION_GOVERNANCE_SCHEMA_VERSION = "WO055_RQ_ADMISSION_GOVERNANCE_V0.1"

REQUIRED_VALIDATION_DIMENSIONS = {
    "SOURCE_VALIDATION",
    "REPRESENTATION_VALIDATION",
    "IMPLEMENTATION_VALIDATION",
    "HISTORICAL_EVIDENCE",
    "REPLICATION",
    "CONTROL",
    "HOLDOUT",
}
VALIDATION_OUTCOMES = {"PASS", "FAIL", "MIXED", "UNKNOWN", "NOT_APPLICABLE"}
VALIDATION_GOVERNANCE_ROLES = {
    "PROMOTION_ELIGIBLE",
    "CONTEXT_ONLY",
    "CONFIRMATORY_ONLY",
    "NO_PROMOTION_AUTHORITY",
}
ACTIVE_PREFIX = "ACTIVE"


def _pass(**extra: Any) -> dict[str, Any]:
    return {"status": "PASS", **extra}


def _fail(reason: str, **extra: Any) -> dict[str, Any]:
    return {"status": "FAIL", "reason": reason, **extra}


def _nonempty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _nonempty_text_list(value: Any) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(_nonempty_text(item) for item in value)
    )


def _canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def legacy_claim_fingerprint(claim: Mapping[str, Any]) -> str:
    fields = {
        "claim_id": claim.get("claim_id"),
        "canonical_statement": claim.get("canonical_statement"),
        "status": claim.get("status"),
        "engine_permission": claim.get("engine_permission"),
        "source_refs": claim.get("source_refs", []),
    }
    if "supersedes" in claim:
        fields["supersedes"] = claim.get("supersedes")
    if "supersession_note" in claim:
        fields["supersession_note"] = claim.get("supersession_note")
    return hashlib.sha256(_canonical_json_bytes(fields)).hexdigest()


def build_legacy_claim_fingerprints(
    claims: Sequence[Mapping[str, Any]],
) -> dict[str, str]:
    result: dict[str, str] = {}
    for claim in claims:
        claim_id = claim.get("claim_id")
        if _nonempty_text(claim_id):
            result[str(claim_id)] = legacy_claim_fingerprint(claim)
    return dict(sorted(result.items()))


def _validation_map(
    validations: Any,
) -> tuple[dict[str, Mapping[str, Any]] | None, dict[str, Any] | None]:
    if not isinstance(validations, list):
        return None, _fail("VALIDATION_DIMENSION_COLLAPSED")

    dimensions: list[str] = []
    mapped: dict[str, Mapping[str, Any]] = {}
    for item in validations:
        if not isinstance(item, Mapping):
            return None, _fail("VALIDATION_DIMENSION_COLLAPSED")
        dimension = item.get("dimension")
        if not _nonempty_text(dimension):
            return None, _fail("VALIDATION_DIMENSION_COLLAPSED")
        name = str(dimension).strip().upper()
        dimensions.append(name)
        mapped[name] = item

    counts = Counter(dimensions)
    if set(counts) != REQUIRED_VALIDATION_DIMENSIONS:
        return None, _fail(
            "VALIDATION_DIMENSION_COLLAPSED",
            dimensions=sorted(counts),
        )
    if any(count != 1 for count in counts.values()):
        return None, _fail(
            "VALIDATION_DIMENSION_COLLAPSED",
            duplicate_dimensions=sorted(
                dimension for dimension, count in counts.items() if count != 1
            ),
        )
    return mapped, None


def _validate_governed_claim(claim: Mapping[str, Any]) -> dict[str, Any]:
    governance = claim.get("governance")
    if not isinstance(governance, Mapping):
        return _pass(governed=False)

    source_refs = claim.get("source_refs")
    current_refs = governance.get("current_authority_refs")
    if not _nonempty_text_list(source_refs) or not _nonempty_text_list(current_refs):
        return _fail("CLAIM_AUTHORITY_OR_SOURCE_REF_MISSING")

    source_ref_set = set(source_refs)
    current_ref_set = set(current_refs)
    if not current_ref_set.issubset(source_ref_set):
        return _fail(
            "CLAIM_AUTHORITY_OR_SOURCE_REF_MISSING",
            authority_refs_not_in_source_refs=sorted(current_ref_set - source_ref_set),
        )

    mode = str(governance.get("authority_mode", "")).strip().upper()
    if mode == "EXCLUSIVE":
        if len(current_refs) != 1:
            return _fail(
                "EXCLUSIVE_AUTHORITY_CARDINALITY_VIOLATION",
                authority_count=len(current_refs),
            )
    elif mode == "COMPOSITE":
        if len(current_refs) < 2:
            return _fail(
                "COMPOSITE_AUTHORITY_CARDINALITY_VIOLATION",
                authority_count=len(current_refs),
            )
        if not _nonempty_text(governance.get("composite_compatibility_statement")):
            return _fail("COMPOSITE_AUTHORITY_COMPATIBILITY_MISSING")
    else:
        return _fail("CLAIM_AUTHORITY_MODE_INVALID", authority_mode=mode)

    validation_map, error = _validation_map(governance.get("validations"))
    if error is not None:
        return error
    assert validation_map is not None

    for dimension, record in validation_map.items():
        outcome = str(record.get("outcome", "")).strip().upper()
        role = str(record.get("governance_role", "")).strip().upper()
        evidence_refs = record.get("evidence_refs")

        if outcome not in VALIDATION_OUTCOMES:
            return _fail(
                "VALIDATION_OUTCOME_INVALID",
                dimension=dimension,
                outcome=outcome,
            )
        if role not in VALIDATION_GOVERNANCE_ROLES:
            return _fail(
                "VALIDATION_GOVERNANCE_ROLE_INVALID",
                dimension=dimension,
                governance_role=role,
            )
        if not isinstance(evidence_refs, list) or not all(
            _nonempty_text(ref) for ref in evidence_refs
        ):
            return _fail(
                "VALIDATION_EVIDENCE_REFS_INVALID",
                dimension=dimension,
            )
        if outcome in {"PASS", "FAIL", "MIXED"} and not evidence_refs:
            return _fail(
                "VALIDATION_EVIDENCE_REFS_REQUIRED",
                dimension=dimension,
                outcome=outcome,
            )

    historical = validation_map["HISTORICAL_EVIDENCE"]
    historical_refs = set(historical.get("evidence_refs", []))
    non_historical_authority_refs: set[str] = set()
    for dimension, record in validation_map.items():
        if dimension == "HISTORICAL_EVIDENCE":
            continue
        role = str(record.get("governance_role", "")).strip().upper()
        if role == "PROMOTION_ELIGIBLE":
            non_historical_authority_refs.update(record.get("evidence_refs", []))

    if current_ref_set & historical_refs and not (
        current_ref_set & non_historical_authority_refs
    ):
        return _fail("HISTORICAL_EVIDENCE_USED_AS_CURRENT_AUTHORITY")

    holdout = validation_map["HOLDOUT"]
    holdout_refs = set(holdout.get("evidence_refs", []))
    holdout_role = str(holdout.get("governance_role", "")).strip().upper()
    engine_permission = str(claim.get("engine_permission", "")).upper()
    if holdout_refs & current_ref_set and (
        holdout_role == "PROMOTION_ELIGIBLE"
        or "DESIGN" in engine_permission
        or "TUNING" in engine_permission
    ):
        return _fail("HOLDOUT_EVIDENCE_USED_FOR_DESIGN_TUNING")

    if str(historical.get("governance_role", "")).strip().upper() not in {
        "CONTEXT_ONLY",
        "NO_PROMOTION_AUTHORITY",
    }:
        return _fail(
            "VALIDATION_GOVERNANCE_ROLE_INVALID",
            dimension="HISTORICAL_EVIDENCE",
        )
    if holdout_role not in {"CONFIRMATORY_ONLY", "NO_PROMOTION_AUTHORITY"}:
        return _fail(
            "VALIDATION_GOVERNANCE_ROLE_INVALID",
            dimension="HOLDOUT",
        )

    return _pass(governed=True, authority_mode=mode)


def _supersession_graph(
    claims: Sequence[Mapping[str, Any]],
) -> dict[str, set[str]]:
    known = {
        str(claim.get("claim_id"))
        for claim in claims
        if _nonempty_text(claim.get("claim_id"))
    }
    graph = {claim_id: set() for claim_id in known}

    for claim in claims:
        claim_id = claim.get("claim_id")
        if not _nonempty_text(claim_id):
            continue
        source = str(claim_id)

        superseded_by = claim.get("superseded_by")
        if _nonempty_text(superseded_by) and str(superseded_by) in known:
            graph[source].add(str(superseded_by))

        supersedes = claim.get("supersedes", [])
        if isinstance(supersedes, list):
            for older in supersedes:
                if _nonempty_text(older) and str(older) in known:
                    graph[str(older)].add(source)
    return graph


def _has_cycle(graph: Mapping[str, set[str]]) -> bool:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        for child in graph.get(node, set()):
            if visit(child):
                return True
        visiting.remove(node)
        visited.add(node)
        return False

    return any(visit(node) for node in graph)


def validate_claim_store(store: Mapping[str, Any]) -> dict[str, Any]:
    claims = store.get("claims")
    if not isinstance(claims, list):
        return _fail("CANONICAL_CLAIMS_INVALID")

    claim_ids: list[str] = []
    for claim in claims:
        if not isinstance(claim, Mapping) or not _nonempty_text(claim.get("claim_id")):
            return _fail("CANONICAL_CLAIM_ID_MISSING")
        claim_ids.append(str(claim["claim_id"]))

    duplicates = sorted(
        claim_id for claim_id, count in Counter(claim_ids).items() if count > 1
    )
    if duplicates:
        return _fail(
            "DUPLICATE_CANONICAL_CLAIM_ID",
            duplicate_claim_ids=duplicates,
        )

    for claim in claims:
        source_refs = claim.get("source_refs")
        if not _nonempty_text_list(source_refs):
            return _fail(
                "CLAIM_AUTHORITY_OR_SOURCE_REF_MISSING",
                claim_id=claim.get("claim_id"),
            )

        status = str(claim.get("status", "")).strip().upper()
        if status.startswith(ACTIVE_PREFIX) and (
            _nonempty_text(claim.get("superseded_by"))
            or bool(claim.get("superseded"))
        ):
            return _fail(
                "ACTIVE_CLAIM_MARKED_SUPERSEDED",
                claim_id=claim.get("claim_id"),
            )

        governed = _validate_governed_claim(claim)
        if governed.get("status") != "PASS":
            return {"claim_id": claim.get("claim_id"), **governed}

    if _has_cycle(_supersession_graph(claims)):
        return _fail("CLAIM_SUPERSESSION_CYCLE")

    top_governance = store.get("governance")
    if top_governance is not None:
        if not isinstance(top_governance, Mapping):
            return _fail("LEGACY_CLAIM_FINGERPRINT_BASELINE_INVALID")
        if top_governance.get("schema_version") != GOVERNANCE_SCHEMA_VERSION:
            return _fail(
                "CLAIM_GOVERNANCE_SCHEMA_INVALID",
                schema_version=top_governance.get("schema_version"),
            )
        baseline = top_governance.get("legacy_claim_fingerprints")
        if not isinstance(baseline, Mapping):
            return _fail("LEGACY_CLAIM_FINGERPRINT_BASELINE_INVALID")

        known_ids = set(claim_ids)
        orphaned = sorted({str(key) for key in baseline} - known_ids)
        if orphaned:
            return _fail(
                "LEGACY_CLAIM_BASELINE_ORPHANED",
                claim_ids=orphaned,
            )

        for claim in claims:
            claim_id = str(claim["claim_id"])
            if "governance" in claim:
                continue
            expected = baseline.get(claim_id)
            if expected is None:
                return _fail(
                    "UNGOVERNED_CLAIM_NOT_IN_LEGACY_BASELINE",
                    claim_id=claim_id,
                )
            if not isinstance(expected, str) or len(expected) != 64:
                return _fail(
                    "LEGACY_CLAIM_FINGERPRINT_BASELINE_INVALID",
                    claim_id=claim_id,
                )
            actual = legacy_claim_fingerprint(claim)
            if expected != actual:
                return _fail(
                    "LEGACY_CLAIM_CHANGED_WITHOUT_GOVERNANCE",
                    claim_id=claim_id,
                    expected_fingerprint=expected,
                    actual_fingerprint=actual,
                )

    return _pass(claim_count=len(claims))


def validate_rq_admission(
    payload: Mapping[str, Any],
    *,
    existing_rq_ids: Iterable[str] = (),
) -> dict[str, Any]:
    if not _nonempty_text(payload.get("newness_statement")):
        return {
            "status": "FAIL",
            "reason": "RQ_ADMISSION_NEWNESS_MISSING",
            "admission_result": "BLOCKED_INCOMPLETE",
        }

    boundary = payload.get("boundary")
    if not isinstance(boundary, Mapping) or not _nonempty_text_list(
        boundary.get("in_scope")
    ) or not _nonempty_text_list(boundary.get("out_of_scope")):
        return {
            "status": "FAIL",
            "reason": "RQ_ADMISSION_BOUNDARY_MISSING",
            "admission_result": "BLOCKED_INCOMPLETE",
        }

    if not _nonempty_text(payload.get("falsification_condition")):
        return {
            "status": "FAIL",
            "reason": "RQ_ADMISSION_FALSIFICATION_MISSING",
            "admission_result": "BLOCKED_INCOMPLETE",
        }

    consequence = payload.get("decision_consequence")
    if not isinstance(consequence, Mapping) or not all(
        _nonempty_text(consequence.get(key))
        for key in ("positive", "negative", "unresolved")
    ):
        return {
            "status": "FAIL",
            "reason": "RQ_ADMISSION_DECISION_CONSEQUENCE_MISSING",
            "admission_result": "BLOCKED_INCOMPLETE",
        }

    if payload.get("outcome_bearing") is True and not _nonempty_text(
        payload.get("holdout_or_leakage_guard")
    ):
        return {
            "status": "FAIL",
            "reason": "RQ_ADMISSION_HOLDOUT_GUARD_MISSING",
            "admission_result": "BLOCKED_EVIDENCE_OR_HOLDOUT_GUARD",
        }

    required_text = ("rq_id", "rq_type", "question", "stop_condition")
    if not all(_nonempty_text(payload.get(field)) for field in required_text):
        return {
            "status": "FAIL",
            "reason": "RQ_ADMISSION_INCOMPLETE",
            "admission_result": "BLOCKED_INCOMPLETE",
        }
    if not _nonempty_text_list(payload.get("expected_evidence")):
        return {
            "status": "FAIL",
            "reason": "RQ_ADMISSION_INCOMPLETE",
            "admission_result": "BLOCKED_INCOMPLETE",
        }
    dependencies = payload.get("dependencies")
    if not isinstance(dependencies, list) or not all(
        _nonempty_text(dep) for dep in dependencies
    ):
        return {
            "status": "FAIL",
            "reason": "RQ_ADMISSION_INCOMPLETE",
            "admission_result": "BLOCKED_INCOMPLETE",
        }

    rq_id = str(payload["rq_id"])
    if rq_id in {str(value) for value in existing_rq_ids}:
        return {
            "status": "FAIL",
            "reason": "RQ_ADMISSION_DUPLICATE_OR_ALREADY_CLOSED",
            "admission_result": "BLOCKED_DUPLICATE_OR_ALREADY_CLOSED",
        }

    return {
        "status": "ADMISSIBLE",
        "admission_result": "ADMISSIBLE",
        "rq_id": rq_id,
    }


def validate_queue_governance(queue: Mapping[str, Any]) -> dict[str, Any]:
    governance = queue.get("governance")
    if governance is None:
        return _pass(migrated=False)
    if not isinstance(governance, Mapping):
        return _fail("RQ_ADMISSION_GOVERNANCE_INVALID")
    if governance.get("schema_version") != RQ_ADMISSION_GOVERNANCE_SCHEMA_VERSION:
        return _fail(
            "RQ_ADMISSION_GOVERNANCE_SCHEMA_INVALID",
            schema_version=governance.get("schema_version"),
        )
    if governance.get("admission_required_for_activation") is not True:
        return _fail("RQ_ADMISSION_ENFORCEMENT_DISABLED")

    admissions = queue.get("admissions")
    if not isinstance(admissions, Mapping):
        return _fail("RQ_ADMISSION_STORE_INVALID")

    active = queue.get("active")
    if active is None:
        return _pass(migrated=True, active_rq=None)
    if not isinstance(active, Mapping):
        return _fail("QUEUE_ACTIVE_INVALID")

    active_id = active.get("id")
    if not _nonempty_text(active_id):
        return _fail("QUEUE_ACTIVE_INVALID")
    active_id = str(active_id)

    admission = admissions.get(active_id)
    if not isinstance(admission, Mapping):
        return _fail(
            "RQ_ADMISSION_MISSING_FOR_ACTIVE_RQ",
            rq_id=active_id,
        )
    if admission.get("rq_id") != active_id:
        return _fail(
            "RQ_ADMISSION_ACTIVE_ID_MISMATCH",
            active_rq=active_id,
            admission_rq=admission.get("rq_id"),
        )

    items = queue.get("items")
    if not isinstance(items, list):
        return _fail("QUEUE_ITEMS_INVALID")
    other_ids = {
        str(item.get("id"))
        for item in items
        if isinstance(item, Mapping)
        and _nonempty_text(item.get("id"))
        and str(item.get("id")) != active_id
    }
    result = validate_rq_admission(admission, existing_rq_ids=other_ids)
    if result.get("status") != "ADMISSIBLE":
        return result

    return _pass(migrated=True, active_rq=active_id)


def validate_fixture(kind: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    normalized = str(kind).strip().lower()
    if normalized == "claims":
        return validate_claim_store(payload)
    if normalized == "admission":
        return validate_rq_admission(payload)
    if normalized == "report":
        return _fail("WO055_REPORT_VALIDATOR_NOT_IMPLEMENTED")
    return _fail("WO055_FIXTURE_VALIDATOR_UNKNOWN", validator=kind)
