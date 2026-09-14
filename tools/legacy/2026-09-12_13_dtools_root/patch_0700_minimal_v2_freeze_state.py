import json
from pathlib import Path

root = Path(r"D:\nexus-xau-engine-repo")
stamp = "2026-09-13T06:05:00+07:00"
spec = "docs/0700_MINIMAL_V2_FROZEN_SPEC_2026-09-13.md"

# Current state
p = root / "docs" / "CURRENT_RESEARCH_STATE.json"
d = json.loads(p.read_text(encoding="utf-8"))
d["updated_at"] = stamp
d["completed_checkpoint"] = "0700_MINIMAL_V2_SPEC_FROZEN_PRE_OUTCOME"
d["minimal_v2"] = {
    "version": "0700_MINIMAL_V2.0",
    "status": "FROZEN_PRE_OUTCOME",
    "spec": spec,
    "scope": "H4-only origin/run; PAT2 FULL-RANGE; M5 confirmation; existing Daily Frame; PATH_REMAINING; no consumed threshold; action lane fail-closed on unresolved location geometry.",
    "next": "Implement V2 contract and synthetic tests without opening/summarizing discovery outcomes until synthetic suite passes."
}
d["next_steps"] = [
    "Implement 0700_MINIMAL_V2.0 exactly from the frozen spec without semantic changes.",
    "Add and pass synthetic contract tests before interpreting any real V2 outcome.",
    "Run 150-day discovery replay and generate terminal/PASS/failure/unknown-state map without threshold optimization.",
    "Run unchanged code on the 60-day cross-period replication period.",
    "Only then decide whether a named source blocker or new state requires V2.1."
]
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Workstream
p = root / "docs" / "0700_WORKSTREAM_STATE.json"
d = json.loads(p.read_text(encoding="utf-8"))
d["updated_at"] = stamp
d["status"] = "MINIMAL_V2_FROZEN_IMPLEMENTATION_NEXT"
d["minimal_v2"] = {
    "version": "0700_MINIMAL_V2.0",
    "status": "FROZEN_PRE_OUTCOME",
    "spec": spec,
    "real_outcomes_opened": False,
    "synthetic_contract_required": True
}
aq = d.get("active_question") or {}
aq["title"] = "Implement frozen 07:00 MINIMAL V2 and synthetic contract suite"
aq["status"] = "ACTIVE_IMPLEMENTATION_PRE_OUTCOME"
aq["question"] = "Does the frozen H4/PAT2 FULL-RANGE minimal representation behave exactly as specified before any real discovery outcome is interpreted?"
aq["next_action"] = "Implement V2 and synthetic contract tests. Do not summarize real V2 discovery outcomes until contract tests pass."
d["active_question"] = aq
vals = d.get("latest_completed_closures") or []
if spec not in vals:
    vals.insert(0, spec)
d["latest_completed_closures"] = vals
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Queue
p = root / "research_queue" / "QUEUE.json"
d = json.loads(p.read_text(encoding="utf-8"))
d["updated_at"] = stamp
active = d.get("active") or {}
active["status"] = "ACTIVE_MINIMAL_V2_IMPLEMENTATION_PRE_OUTCOME"
active["latest_checkpoint"] = spec
active["current_summary"] = "0700_MINIMAL_V2.0 is frozen before new V2 outcomes. Implement exact spec + synthetic contract tests next; real discovery interpretation is blocked until tests pass."
d["active"] = active
for item in d.get("items", []):
    if isinstance(item, dict) and item.get("id") == "RQ-013":
        item["status"] = "ACTIVE_MINIMAL_V2_IMPLEMENTATION_PRE_OUTCOME"
        item["checkpoint_ref"] = spec
        item["current_summary"] = "MINIMAL_V2.0 frozen. Next: exact implementation and synthetic contract suite before opening real V2 outcomes."
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Active worksheet
p = root / "research_queue" / "active" / "RQ-013_0700_EXISTING_KNOWLEDGE_REANCHOR.md"
s = p.read_text(encoding="utf-8")
if "## MINIMAL V2 freeze" not in s:
    s += f"""\n\n## MINIMAL V2 freeze\n\nFrozen pre-outcome specification:\n\n`{spec}`\n\nVersion: `0700_MINIMAL_V2.0`\n\nNo new V2 discovery outcome may be interpreted before the synthetic contract suite passes. Semantic changes after outcome inspection require a new version.\n"""
p.write_text(s, encoding="utf-8")

print("patched central state for MINIMAL_V2 freeze")
