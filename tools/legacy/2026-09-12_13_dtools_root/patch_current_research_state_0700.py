import json
from pathlib import Path

p = Path(r"D:\nexus-xau-engine-repo\docs\CURRENT_RESEARCH_STATE.json")
d = json.loads(p.read_text(encoding="utf-8"))

d["updated_at"] = "2026-09-13T05:03:39+07:00"
d["mode"] = "RESTART_SAFE_0700_REANCHOR_MINIMAL_V2_PREP"
d["completed_checkpoint"] = "0700_EXISTING_KNOWLEDGE_SUFFICIENCY_AUDIT_REANCHORED"

d["active_0700_workstream"] = {
    "status": "ACTIVE",
    "active_rq": "RQ-013",
    "worksheet": "research_queue/active/RQ-013_0700_EXISTING_KNOWLEDGE_REANCHOR.md",
    "dashboard": "docs/0700_WORKSTREAM_STATE.json",
    "audit": "docs/0700_EXISTING_KNOWLEDGE_SUFFICIENCY_AUDIT_2026-09-13.md",
    "source_map": "docs/0700_YOUTUBE_SOURCE_GAP_MAP_2026-09-13.md",
    "current_goal": "Freeze a narrow H4/PAT2-only 07:00 V2 from existing evidence before any broad new YouTube review.",
    "current_assessment": (
        "Existing work is sufficient for a narrow signal/run V2. "
        "H4 consumed/run-progress is the strongest replicated state lead, but no consumed threshold or 100% system win-rate claim is established."
    ),
    "historical_guards": [
        "Q1-Q4 used PAT2 BODY midpoint as an explicit historical research proxy; current PAT2 source authority is FULL RANGE and requires a new version.",
        "Legacy pre-reanchor Daily Frame side support is not current confirmation.",
        "D1 current authority is a 5,000-10,000 run family with exact stage transition open; do not use one universal D1 scalar."
    ]
}

loop = d.get("research_loop") or {}
loop["operating_rule"] = (
    "Resume from the current 07:00 workstream dashboard and source coverage before opening sources or running tests. "
    "Do not repeat closed/unresolved checks. Prefer a narrow existing-evidence V2 before broader source hunting."
)
loop["load_order"] = [
    "PROJECT_BOOTSTRAP.md",
    "skills/nexus-xau-research/SKILL.md",
    "docs/NEXUS_PROJECT_MAINTENANCE_POLICY.md",
    "TOOLS.md",
    "docs/CURRENT_RESEARCH_STATE.json",
    "docs/0700_WORKSTREAM_STATE.json",
    "docs/0700_EXISTING_KNOWLEDGE_SUFFICIENCY_AUDIT_2026-09-13.md",
    "docs/CANONICAL_CLAIM_REGISTER_2026-09-03.json",
    "docs/SOURCE_COVERAGE_LEDGER.json",
    "research_queue/QUEUE.json",
    "research_queue/active/RQ-013_0700_EXISTING_KNOWLEDGE_REANCHOR.md",
    "docs/0700_PAT50_DENOMINATOR_SOURCE_CLOSURE_2026-09-13.md",
    "docs/0700_D1_DAY_RUN_SOURCE_REREVIEW_2026-09-13.md",
    "docs/0700_DAILY_FRAME_SR_SELECTOR_SOURCE_CLOSURE_2026-09-13.md",
    "docs/0700_Q1_ORIGIN_CONTEXT_REPLICATION_2026-09-12.md",
    "docs/0700_Q3_DISTINCT_INFORMATION_CROSS_PERIOD_2026-09-12.md",
    "docs/0700_Q4_H4_CONSUMED_SHAPE_CROSS_PERIOD_2026-09-12.md"
]
d["research_loop"] = loop

d["rq012_holdout_state"] = {
    "status": "QUEUED_FROZEN_PROTOCOL_NO_OUTCOME_SCORE",
    "worksheet": "research_queue/queued/RQ-012_V0_HOLDOUT_LEDGER_AND_ACTIVATION_LOCK.md",
    "protocol": "docs/RQ011_PRISTINE_V0_HOLDOUT_PROTOCOL_2026-09-09.md",
    "note": "Paused while owner-prioritized 07:00 workstream is re-anchored. Frozen V0.1 identities remain unchanged and outcome scoring is not authorized."
}

d["next_steps"] = [
    "Complete structured 07:00 re-anchor validation and checkpoint it.",
    "Freeze a separate 0700_MINIMAL_V2 specification using existing evidence: H4-only origin/run, PAT2 FULL-RANGE, existing Daily Frame, PATH_REMAINING, no consumed threshold.",
    "Version the existing 0700_STATE_DATASET_V1 machinery rather than starting over; keep Q1-Q4 historical outputs unchanged.",
    "Rerun discovery and replication under the frozen V2 without selecting a threshold from outcomes.",
    "Only reopen YouTube/source work if the minimal V2 reaches a named blocker that cannot be excluded or fail-closed."
]

blocked = list(d.get("blocked_from_claiming") or [])
for x in [
    "07:00 system/trade Win rate",
    "100% win claim",
    "07:00 profitability/expectancy",
    "canonical consumed-ratio threshold",
    "universal D1 scalar",
    "universal exact broker fill"
]:
    if x not in blocked:
        blocked.append(x)
d["blocked_from_claiming"] = blocked

d["resume_instruction"] = (
    "Resume RQ-013 from docs/0700_WORKSTREAM_STATE.json and docs/0700_EXISTING_KNOWLEDGE_SUFFICIENCY_AUDIT_2026-09-13.md. "
    "Do not start broad YouTube review. Finish central-state reconciliation, freeze 0700_MINIMAL_V2 from existing evidence, then version/rerun the existing V1 pipeline."
)

validation = d.get("validation_status") or {}
validation["research_preflight"] = "MUST_RERUN_AFTER_2026-09-13_REANCHOR"
validation["structured_state_reanchor"] = "PENDING_VALIDATION"
d["validation_status"] = validation

p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("updated", p)
