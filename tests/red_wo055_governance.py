import importlib
import json
from pathlib import Path

import pytest

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "wo055" / "governance_matrix.json"


def _matrix() -> dict:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _governance_module():
    # Intentionally RED in Phase A: production validator does not exist yet.
    return importlib.import_module("nexus_xau.governance.research_governance")


@pytest.mark.parametrize(
    "case",
    _matrix()["known_failure_cases"],
    ids=lambda case: case["id"],
)
def test_wo055_known_failure_reason_codes_are_frozen(case: dict) -> None:
    module = _governance_module()
    result = module.validate_fixture(case["validator"], case["payload"])
    assert result["status"] == "FAIL"
    assert result["reason"] == case["expected_reason"]


@pytest.mark.parametrize(
    "case",
    _matrix()["valid_cases"],
    ids=lambda case: case["id"],
)
def test_wo055_valid_governance_fixtures_are_frozen(case: dict) -> None:
    module = _governance_module()
    result = module.validate_fixture(case["validator"], case["payload"])
    assert result["status"] == case["expected_status"]
