from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from scripts.research_preflight import validate_unknown_classification_registry


def _fixtures(tmp_path: Path):
    evidence = tmp_path / "evidence.md"
    evidence.write_text("evidence", encoding="utf-8")
    readiness = {
        "components": [
            {
                "id": "P1-X",
                "component": "Synthetic blocker",
                "status": "BLOCKING",
                "missing": ["future confirmation"],
            }
        ]
    }
    registry = {
        "schema_version": "PHASE1_UNKNOWN_CLASSIFICATION_REGISTRY_V0.1",
        "scope": "Phase 1 readiness unresolved dependencies",
        "allowed_epistemic_classes": [
            "KNOWN_NOW",
            "DERIVABLE",
            "RUNTIME_OBSERVABLE",
            "STRUCTURAL_UNKNOWN",
            "IRREDUCIBLE_OR_NOT_YET_REDUCIBLE",
        ],
        "allowed_blocking_axes": [
            "BLOCKING",
            "NON_BLOCKING",
            "REQUIRED_LATER",
            "IRRELEVANT",
        ],
        "allowed_statuses": ["OPEN", "RESOLVED", "SUPERSEDED"],
        "entries": [
            {
                "id": "U-X",
                "readiness_component_id": "P1-X",
                "readiness_missing": "future confirmation",
                "status": "OPEN",
                "epistemic_class": "RUNTIME_OBSERVABLE",
                "blocking_axis": "REQUIRED_LATER",
                "resolution_basis": "Acquisition method is known but event has not happened.",
                "observation_method": "Observe the future event when authorized.",
                "evidence_refs": ["evidence.md"],
            }
        ],
    }
    return registry, readiness


def _validate(registry, readiness, tmp_path: Path):
    return validate_unknown_classification_registry(
        registry, readiness, root=tmp_path
    )


def test_valid_registry_covers_current_readiness_gap(tmp_path: Path) -> None:
    registry, readiness = _fixtures(tmp_path)
    result = _validate(registry, readiness, tmp_path)
    assert result == {
        "status": "PASS",
        "entry_count": 1,
        "open_count": 1,
        "required_missing_count": 1,
    }


def test_generic_unknown_epistemic_class_is_rejected(tmp_path: Path) -> None:
    registry, readiness = _fixtures(tmp_path)
    registry["entries"][0]["epistemic_class"] = "UNKNOWN"
    result = _validate(registry, readiness, tmp_path)
    assert result["reason"] == "UNKNOWN_REGISTRY_EPISTEMIC_CLASS_INVALID"


def test_open_known_now_is_rejected(tmp_path: Path) -> None:
    registry, readiness = _fixtures(tmp_path)
    registry["entries"][0]["epistemic_class"] = "KNOWN_NOW"
    result = _validate(registry, readiness, tmp_path)
    assert result["reason"] == "UNKNOWN_REGISTRY_OPEN_KNOWN_NOW_INVALID"


def test_class_specific_method_is_required(tmp_path: Path) -> None:
    registry, readiness = _fixtures(tmp_path)
    del registry["entries"][0]["observation_method"]
    result = _validate(registry, readiness, tmp_path)
    assert result["reason"] == "UNKNOWN_REGISTRY_CLASS_METHOD_MISSING"
    assert result["field"] == "observation_method"


def test_missing_readiness_coverage_is_rejected(tmp_path: Path) -> None:
    registry, readiness = _fixtures(tmp_path)
    registry["entries"] = []
    result = _validate(registry, readiness, tmp_path)
    assert result["reason"] == "UNKNOWN_REGISTRY_COVERAGE_MISSING"


def test_duplicate_open_mapping_is_rejected(tmp_path: Path) -> None:
    registry, readiness = _fixtures(tmp_path)
    duplicate = deepcopy(registry["entries"][0])
    duplicate["id"] = "U-X-2"
    registry["entries"].append(duplicate)
    result = _validate(registry, readiness, tmp_path)
    assert result["reason"] == "UNKNOWN_REGISTRY_DUPLICATE_OPEN_MAPPING"


def test_dangling_missing_mapping_is_rejected(tmp_path: Path) -> None:
    registry, readiness = _fixtures(tmp_path)
    registry["entries"][0]["readiness_missing"] = "different gap"
    result = _validate(registry, readiness, tmp_path)
    assert result["reason"] == "UNKNOWN_REGISTRY_DANGLING_MISSING_MAPPING"


def test_missing_evidence_file_is_rejected(tmp_path: Path) -> None:
    registry, readiness = _fixtures(tmp_path)
    registry["entries"][0]["evidence_refs"] = ["missing.md"]
    result = _validate(registry, readiness, tmp_path)
    assert result["reason"] == "UNKNOWN_REGISTRY_EVIDENCE_NOT_FOUND"


def test_partial_or_blocking_component_requires_explicit_missing_array(
    tmp_path: Path,
) -> None:
    registry, readiness = _fixtures(tmp_path)
    registry["entries"] = []
    del readiness["components"][0]["missing"]
    result = _validate(registry, readiness, tmp_path)
    assert result["reason"] == "UNKNOWN_REGISTRY_READINESS_MISSING_ARRAY_REQUIRED"


def test_open_entry_cannot_target_ready_component(tmp_path: Path) -> None:
    registry, readiness = _fixtures(tmp_path)
    readiness["components"][0]["status"] = "READY_RESEARCH_LEVEL"
    result = _validate(registry, readiness, tmp_path)
    assert result["reason"] == "UNKNOWN_REGISTRY_OPEN_ENTRY_ON_READY_COMPONENT"


def test_declared_enum_drift_is_rejected(tmp_path: Path) -> None:
    registry, readiness = _fixtures(tmp_path)
    registry["allowed_blocking_axes"].append("MAYBE")
    result = _validate(registry, readiness, tmp_path)
    assert result["reason"] == "UNKNOWN_REGISTRY_BLOCKING_ENUM_DRIFT"