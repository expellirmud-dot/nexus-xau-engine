import json
from pathlib import Path

root = Path(r"D:\nexus-xau-engine-repo")
stamp = "2026-09-13T06:18:00+07:00"
checkpoint = "docs/0700_MINIMAL_V2_PRE_OUTCOME_IMPLEMENTATION_FREEZE_2026-09-13.md"

# Current State
p = root / "docs" / "CURRENT_RESEARCH_STATE.json"
d = json.loads(p.read_text(encoding="utf-8"))
d["updated_at"] = stamp
d["completed_checkpoint"] = "0700_MINIMAL_V2_PRE_OUTCOME_IMPLEMENTATION_FROZEN"
v2 = d.get("minimal_v2") or {}
v2.update({
    "version": "0700_MINIMAL_V2.0",
    "status": "IMPLEMENTATION_FROZEN_SYNTHETIC_PASS_REAL_OUTCOME_UNOPENED",
    "implementation": "src/nexus_xau/research/minimal_v2_0700.py",
    "tests": "tests/test_minimal_v2_0700.py",
    "implementation_checkpoint": checkpoint,
    "synthetic_contract": "16_PASS",
    "full_pytest": "EXIT_CODE_0",
    "real_discovery_opened": False,
})
d["minimal_v2"] = v2
d["next_steps"] = [
    "Run frozen 0700_MINIMAL_V2.0 on the 2022-09-01..2023-03-31 complete development period without semantic changes.",
    "Record the 150-day terminal/PASS/failure/unknown-state map and descriptive signal/run outcomes; do not optimize thresholds.",
    "Checkpoint and push Discovery before running replication.",
    "Run unchanged V2.0 on the 2023-09-01..2023-11-23 complete cross-period dataset.",
    "Only after cross-period comparison decide whether a named blocker requires V2.1 or new source work."
]
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Workstream
p = root / "docs" / "0700_WORKSTREAM_STATE.json"
d = json.loads(p.read_text(encoding="utf-8"))
d["updated_at"] = stamp
d["status"] = "MINIMAL_V2_DISCOVERY_READY"
v2 = d.get("minimal_v2") or {}
v2.update({
    "status": "IMPLEMENTATION_FROZEN_SYNTHETIC_PASS_REAL_OUTCOME_UNOPENED",
    "implementation": "src/nexus_xau/research/minimal_v2_0700.py",
    "tests": "tests/test_minimal_v2_0700.py",
    "checkpoint": checkpoint,
    "synthetic_contract": "16_PASS",
    "real_outcomes_opened": False,
})
d["minimal_v2"] = v2
aq = d.get("active_question") or {}
aq["title"] = "Run frozen 07:00 MINIMAL V2 discovery replay"
aq["status"] = "ACTIVE_DISCOVERY_REPLAY_FROZEN_CODE"
aq["question"] = "Across the 150-day complete discovery period, what states become research candidates, PASS, failure, or unknown under frozen V2.0?"
aq["next_action"] = "Run frozen V2.0 on 2022-09-01..2023-03-31 and checkpoint the descriptive failure/unknown-state map without tuning."
d["active_question"] = aq
vals = d.get("latest_completed_closures") or []
if checkpoint not in vals:
    vals.insert(0, checkpoint)
d["latest_completed_closures"] = vals
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Queue
p = root / "research_queue" / "QUEUE.json"
d = json.loads(p.read_text(encoding="utf-8"))
d["updated_at"] = stamp
active = d.get("active") or {}
active["status"] = "ACTIVE_MINIMAL_V2_DISCOVERY_REPLAY"
active["latest_checkpoint"] = checkpoint
active["current_summary"] = "V2.0 implementation is frozen and synthetic contract passed 16/16 before real outcomes. Next: run 150-day discovery unchanged and record failure/unknown map."
d["active"] = active
for item in d.get("items", []):
    if isinstance(item, dict) and item.get("id") == "RQ-013":
        item["status"] = "ACTIVE_MINIMAL_V2_DISCOVERY_REPLAY"
        item["checkpoint_ref"] = checkpoint
        item["current_summary"] = "Frozen V2.0 + 16/16 synthetic contract pass. Open first 150-day discovery report next with no semantic tuning."
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Active worksheet
p = root / "research_queue" / "active" / "RQ-013_0700_EXISTING_KNOWLEDGE_REANCHOR.md"
s = p.read_text(encoding="utf-8")
if "## V2 pre-outcome implementation freeze" not in s:
    s += f"""\n\n## V2 pre-outcome implementation freeze\n\nCheckpoint:\n\n`{checkpoint}`\n\nSynthetic contract: `16/16 PASS`\n\nFull pytest: `exit code 0`\n\nReal V2 discovery opened at this checkpoint: `NO`\n\nNext action: run frozen V2.0 unchanged on the 150-day complete discovery period and record the failure/unknown-state map before any replication or semantic change.\n"""
p.write_text(s, encoding="utf-8")

print("updated state for V2 discovery-ready checkpoint")
