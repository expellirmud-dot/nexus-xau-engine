import json
from pathlib import Path

root=Path(r"D:\nexus-xau-engine-repo")
stamp="2026-09-13T06:31:00+07:00"
job_id="XAU-0700-MINIMAL-V2-DISCOVERY-20260913"
job_path=r"D:\tools\nexus-durable-work\_agent\jobs\XAU-0700-MINIMAL-V2-DISCOVERY-20260913\job.json"
timeout_ref="docs/0700_MINIMAL_V2_FIRST_DISCOVERY_TIMEOUT_2026-09-13.md"

for rel in ["docs/CURRENT_RESEARCH_STATE.json","docs/0700_WORKSTREAM_STATE.json","research_queue/QUEUE.json"]:
    p=root/rel
    d=json.loads(p.read_text(encoding="utf-8"))
    d["updated_at"]=stamp
    durable={
        "job_id":job_id,
        "job_path":job_path,
        "status":"RUNNING_AT_CHECKPOINT",
        "execution_layer":"D:/tools/nexus-durable-work Local Work Agent",
        "success_probe":"results/0700_MINIMAL_V2/DISCOVERY_2022_09_TO_2023_03/REPORT.json",
        "timeout_checkpoint":timeout_ref,
        "restart_rule":"Inspect this durable job before any retry. Do not resubmit the 150-day discovery while the job is RUNNING or before reconciling its persisted result/heartbeat."
    }
    if rel.endswith("CURRENT_RESEARCH_STATE.json"):
        d["active_durable_job"]=durable
        d["next_steps"]=[
            "Inspect the existing durable job XAU-0700-MINIMAL-V2-DISCOVERY-20260913; do not submit a duplicate while RUNNING.",
            "When DONE, read the persisted V2 discovery outputs and record the 150-day failure/unknown-state map without semantic tuning.",
            "Checkpoint and push Discovery before running the unchanged 60-day replication.",
            "If the durable job fails, inspect its persisted stdout/stderr/result and reconcile before retrying; do not infer a model/algorithm defect from transport timeout alone."
        ]
    elif rel.endswith("0700_WORKSTREAM_STATE.json"):
        d["active_durable_job"]=durable
        aq=d.get("active_question") or {}
        aq["status"]="ACTIVE_DISCOVERY_REPLAY_DURABLE_JOB_RUNNING"
        aq["next_action"]="Inspect the existing durable job and consume its persisted result when DONE. Do not submit another discovery run while it is active."
        d["active_question"]=aq
        vals=d.get("latest_completed_closures") or []
        if timeout_ref not in vals:
            vals.insert(0,timeout_ref)
        d["latest_completed_closures"]=vals
    else:
        active=d.get("active") or {}
        active["status"]="ACTIVE_MINIMAL_V2_DISCOVERY_DURABLE_JOB_RUNNING"
        active["latest_checkpoint"]=timeout_ref
        active["current_summary"]="The first synchronous run hit the Bridge 180-second execution timeout without opening outcomes. The same frozen V2.0 discovery is now RUNNING under the machine-side durable Local Work Agent. Inspect/reuse that job; do not duplicate-submit."
        active["durable_job_id"]=job_id
        d["active"]=active
        for item in d.get("items",[]):
            if isinstance(item,dict) and item.get("id")=="RQ-013":
                item["status"]="ACTIVE_MINIMAL_V2_DISCOVERY_DURABLE_JOB_RUNNING"
                item["checkpoint_ref"]=timeout_ref
                item["durable_job_id"]=job_id
                item["current_summary"]="Frozen V2.0 discovery is running durably on the local agent after the synchronous Bridge timeout. Next action is inspection/reuse of the persisted job result."
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

# active worksheet
p=root/"research_queue"/"active"/"RQ-013_0700_EXISTING_KNOWLEDGE_REANCHOR.md"
s=p.read_text(encoding="utf-8")
if "## Durable discovery execution" not in s:
    s += f"""

## Durable discovery execution

The first synchronous 150-day V2 run hit the explicit 180-second Bridge execution timeout before any output was written.

Authority:

`{timeout_ref}`

The unchanged frozen V2.0 replay was resubmitted through the existing machine-side Local Work Agent.

Durable job:

`{job_id}`

Persisted job state:

`{job_path}`

Rule:

- if RUNNING, inspect heartbeat and wait; do not submit another copy;
- if DONE, reuse the persisted result;
- if FAILED/BLOCKED, inspect persisted stdout/stderr/result before any retry;
- ChatGPT/UI/Bridge turn lifetime must not control the lifetime of deterministic long replay work.
"""
p.write_text(s,encoding="utf-8")
print("patched durable job into project state")
