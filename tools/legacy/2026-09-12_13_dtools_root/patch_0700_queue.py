import json
from pathlib import Path

p = Path(r"D:\nexus-xau-engine-repo\research_queue\QUEUE.json")
d = json.loads(p.read_text(encoding="utf-8"))

d["updated_at"] = "2026-09-13T05:03:39+07:00"
d["active"] = {
    "id": "RQ-013",
    "title": "07:00 Existing-Knowledge Re-anchor and Minimal V2 Freeze",
    "worksheet": "research_queue/active/RQ-013_0700_EXISTING_KNOWLEDGE_REANCHOR.md",
    "status": "ACTIVE_REANCHOR_SPEC_PREP",
    "latest_checkpoint": "docs/0700_EXISTING_KNOWLEDGE_SUFFICIENCY_AUDIT_2026-09-13.md"
}
d["priority_order"] = ["RQ-013", "RQ-012", "RQ-014"]
d["queue_state"] = "ACTIVE_0700_REANCHOR_MINIMAL_V2_PREP"
d["reopen_reason"] = "Project owner prioritized the narrow 07:00 method and requested an audit of existing work before any new YouTube review. Audit found stale central state and enough existing evidence to prepare a minimal H4/PAT2-only V2."

items = d.get("items", [])
by_id = {item.get("id"): item for item in items if isinstance(item, dict)}

rq12 = by_id.get("RQ-012")
if rq12:
    rq12["status"] = "QUEUED_FROZEN_PROTOCOL_NO_OUTCOME_SCORE"
    rq12["worksheet"] = "research_queue/queued/RQ-012_V0_HOLDOUT_LEDGER_AND_ACTIVATION_LOCK.md"
    rq12["current_summary"] = "Frozen V0.1 holdout tooling is paused while the owner-prioritized 07:00 workstream is re-anchored. No holdout outcome scoring is authorized."
    rq12["why_now"] = "RQ-011 remains frozen. RQ-012 is preserved and queued; it is not abandoned or superseded by the 07:00 workstream."

rq13 = {
    "id": "RQ-013",
    "title": "07:00 Existing-Knowledge Re-anchor and Minimal V2 Freeze",
    "type": "RESEARCH_RECONCILIATION",
    "status": "ACTIVE_REANCHOR_SPEC_PREP",
    "why_now": "Central restart state was stale and caused duplicate source work. Existing Q1-Q4 plus 2026-09-13 source closures indicate a narrow H4/PAT2-only 07:00 V2 may be calculable without further broad YouTube review.",
    "depends_on": [],
    "blocks": [
        "restart-safe 07:00 continuity",
        "0700_MINIMAL_V2 specification",
        "new V2 rerun using current PAT2 source geometry"
    ],
    "preferred_method": "Existing repository evidence -> chronology/reconciliation -> structured-state repair -> freeze minimal V2 -> targeted computation; no broad new source search unless a named blocker remains.",
    "worksheet": "research_queue/active/RQ-013_0700_EXISTING_KNOWLEDGE_REANCHOR.md",
    "checkpoint_ref": "docs/0700_EXISTING_KNOWLEDGE_SUFFICIENCY_AUDIT_2026-09-13.md",
    "current_summary": "Re-anchor current knowledge, prevent duplicate source work, and freeze H4/PAT2-only minimal 07:00 V2 from existing evidence."
}
if "RQ-013" in by_id:
    by_id["RQ-013"].update(rq13)
else:
    items.append(rq13)

rq14 = {
    "id": "RQ-014",
    "title": "07:00 PAT3 Combined Multi-Candle Geometry",
    "type": "SOURCE_RESEARCH",
    "status": "QUEUED_NOT_REQUIRED_FOR_MINIMAL_V2",
    "why_now": "PAT3 arithmetic remains a genuine source gap but the minimal H4/PAT2-only 07:00 V2 can exclude PAT3.",
    "depends_on": ["RQ-013"],
    "blocks": ["future broader autonomous PAT detector"],
    "preferred_method": "Mapped PA/PAT sources -> transcript windows -> synchronized visual -> audio cross-check -> close exact arithmetic or retain UNKNOWN. Never select formula from outcomes.",
    "worksheet": "research_queue/queued/RQ-014_0700_PAT3_COMBINED_GEOMETRY.md",
    "checkpoint_ref": "docs/0700_PAT3_COMBINED_GEOMETRY_REVIEW_START_2026-09-13.md",
    "current_summary": "Queued source gap. Do not resume until minimal V2 requires PAT3 or scope is intentionally broadened."
}
if "RQ-014" in by_id:
    by_id["RQ-014"].update(rq14)
else:
    items.append(rq14)

d["items"] = items
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("updated", p)
