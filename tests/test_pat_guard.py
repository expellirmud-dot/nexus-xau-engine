from nexus_xau.detectors.pat import PatDetector
from nexus_xau.engine.rules import Decision, EvidenceStatus


def test_unresolved_pat_detector_fails_closed() -> None:
    result = PatDetector().evaluate()
    assert result.decision is Decision.WAIT
    assert result.evidence_status is EvidenceStatus.NOT_IMPLEMENTED
