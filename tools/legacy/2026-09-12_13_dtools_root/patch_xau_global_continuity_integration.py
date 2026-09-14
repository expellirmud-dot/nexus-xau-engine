from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

root = Path(r"D:\nexus-xau-engine-repo")
stamp = datetime.now().astimezone().isoformat(timespec="seconds")
checkpoint = "docs/GLOBAL_PROJECT_CONTINUITY_BOOTSTRAP_2026-09-13.md"
job_id = "XAU-0700-MINIMAL-V2-DISCOVERY-20260913"
report = "results/0700_MINIMAL_V2/DISCOVERY_2022_09_TO_2023_03/REPORT.json"

# current state
p = root / "docs" / "CURRENT_RESEARCH_STATE.json"
d = json.loads(p.read_text(encoding="utf-8"))
d["updated_at"] = stamp
d["continuity_tool"] = {
    "scope": "GLOBAL_SHARED_INFRASTRUCTURE",
    "path": "D:/tools/nexus-project-continuity",
    "project_id": "xau",
    "default_reconnect": "py -3 D:/tools/nexus-project-continuity/continuity.py resume --project xau",
    "boot_rule": "COMPACT_FIRST_DEEP_LOAD_ON_DEMAND",
    "purpose": "Recover project/git/workstream/version/next-action/live durable-job/tool capability state without bulk-loading project documents."
}
job = d.get("active_durable_job") or {}
job.update({
    "job_id": job_id,
    "status": "DONE_RESULT_UNOPENED",
    "live_status_verified": "DONE",
    "success_probe": report,
    "result_exists_nonempty": True,
    "restart_rule": "Do not rerun. Inspect the persisted result next. Deep-load only the frozen V2 spec/checkpoint needed for outcome interpretation."
})
d["active_durable_job"] = job
v2 = d.get("minimal_v2") or {}
v2["real_discovery_execution_status"] = "DONE_RESULT_UNOPENED"
v2["real_discovery_opened"] = False
d["minimal_v2"] = v2
d["completed_checkpoint"] = "GLOBAL_COMPACT_CONTINUITY_BOOTSTRAP_INTEGRATED"
d["next_steps"] = [
    "Use the compact global continuity capsule on reconnect; do not bulk-load the docs tree.",
    "Inspect the existing persisted V2 discovery REPORT.json; do not rerun the completed durable job.",
    "Interpret the 150-day failure/unknown-state map only under the frozen V2.0 spec and pre-outcome checkpoint.",
    "Checkpoint/push Discovery before unchanged 60-day replication."
]
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# workstream
p = root / "docs" / "0700_WORKSTREAM_STATE.json"
d = json.loads(p.read_text(encoding="utf-8"))
d["updated_at"] = stamp
d["status"] = "MINIMAL_V2_DISCOVERY_RESULT_READY_UNOPENED"
d["continuity_tool"] = {
    "path": "D:/tools/nexus-project-continuity",
    "project_id": "xau",
    "boot_rule": "COMPACT_FIRST"
}
job = d.get("active_durable_job") or {}
job.update({
    "job_id": job_id,
    "status": "DONE_RESULT_UNOPENED",
    "live_status_verified": "DONE",
    "success_probe": report
})
d["active_durable_job"] = job
v2 = d.get("minimal_v2") or {}
v2["real_outcomes_opened"] = False
v2["discovery_execution_status"] = "DONE_RESULT_UNOPENED"
d["minimal_v2"] = v2
aq = d.get("active_question") or {}
aq["status"] = "ACTIVE_DISCOVERY_RESULT_READY_UNOPENED"
aq["next_action"] = "Open the persisted frozen V2.0 discovery result once, build the 150-day failure/unknown-state map, and checkpoint it without semantic tuning."
d["active_question"] = aq
vals = d.get("latest_completed_closures") or []
if checkpoint not in vals:
    vals.insert(0, checkpoint)
d["latest_completed_closures"] = vals
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# queue
p = root / "research_queue" / "QUEUE.json"
d = json.loads(p.read_text(encoding="utf-8"))
d["updated_at"] = stamp
active = d.get("active") or {}
active.update({
    "status": "ACTIVE_MINIMAL_V2_DISCOVERY_RESULT_READY_UNOPENED",
    "latest_checkpoint": checkpoint,
    "current_summary": "Global compact continuity is integrated. Frozen V2.0 150-day durable replay is DONE and its result exists, but outcomes remain unopened. Next: inspect persisted result once and record failure/unknown map without tuning.",
    "durable_job_id": job_id
})
d["active"] = active
for item in d.get("items", []):
    if isinstance(item, dict) and item.get("id") == "RQ-013":
        item["status"] = "ACTIVE_MINIMAL_V2_DISCOVERY_RESULT_READY_UNOPENED"
        item["checkpoint_ref"] = checkpoint
        item["current_summary"] = "Compact global reconnect is active. Durable V2.0 Discovery is DONE_RESULT_UNOPENED; consume persisted result next without rerun or semantic tuning."
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print(stamp)
