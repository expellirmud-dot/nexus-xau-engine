import json
from pathlib import Path

p = Path(r"D:\nexus-xau-engine-repo\docs\0700_WORKSTREAM_STATE.json")
d = json.loads(p.read_text(encoding="utf-8"))

d["updated_at"] = "2026-09-13T05:03:39+07:00"
d["status"] = "ACTIVE_REANCHOR_MINIMAL_V2_PREP"
d["active_question"] = {
    "rq_id": "RQ-013",
    "title": "07:00 Existing-Knowledge Re-anchor and Minimal V2 Freeze",
    "status": "ACTIVE_REANCHOR_SPEC_PREP",
    "worksheet": "research_queue/active/RQ-013_0700_EXISTING_KNOWLEDGE_REANCHOR.md",
    "audit": "docs/0700_EXISTING_KNOWLEDGE_SUFFICIENCY_AUDIT_2026-09-13.md",
    "question": "Can the already-known source and research pieces be frozen into a narrow H4/PAT2-only 07:00 V2 without reopening broad YouTube research?",
    "next_action": "Repair central structured state and freeze 0700_MINIMAL_V2 before changing the V1 generator or inspecting new V2 outcomes."
}

for item in d.get("established_source_state", []):
    if item.get("topic") == "D1 staged run distance":
        item["topic"] = "D1 / Day run family"
        item["state"] = "SOURCE_BACKED_RANGE_STAGE_EXACT_TRANSITION_OPEN"
        item["current"] = "Day has source-backed run magnitude references around 5,000–10,000 project points. Do not promote one universal D1 scalar or exact 5K->10K stage equation."
        item["residual"] = "Exact stage/set transition and active-stage selection at 07:00 remain unresolved."
        item["refs"] = [
            "docs/0700_D1_DAY_RUN_SOURCE_REREVIEW_2026-09-13.md",
            "docs/0700_D1_DAY_RUN_SOURCE_CLOSURE_2026-09-13.md"
        ]

d["open_gaps_priority"] = [
    {
        "priority": 1,
        "topic": "Freeze 0700_MINIMAL_V2 from existing evidence",
        "state": "ACTIVE",
        "next": "H4-only origin/run + PAT2 FULL-RANGE + existing Daily Frame + PATH_REMAINING; no new YouTube unless a named blocker appears."
    },
    {
        "priority": 2,
        "topic": "Exact Daily Frame 0/5 snap/tie and numeric qualification",
        "state": "OPEN_FAIL_CLOSED_FOR_MINIMAL_V2"
    },
    {
        "priority": 3,
        "topic": "D1 5,000–10,000 stage transition semantics",
        "state": "OPEN_NOT_REQUIRED_FOR_MINIMAL_H4_V2"
    },
    {
        "priority": 4,
        "topic": "PAT3 combined-candle arithmetic",
        "state": "QUEUED_NOT_REQUIRED_FOR_PAT2_ONLY_V2",
        "worksheet": "research_queue/queued/RQ-014_0700_PAT3_COMBINED_GEOMETRY.md"
    },
    {
        "priority": 5,
        "topic": "Exact M1/M5 quantitative brake/standing predicates and fill convention",
        "state": "OPEN_NOT_REQUIRED_FOR_FIRST_PAT2_SIGNAL_RUN_V2"
    },
    {
        "priority": 6,
        "topic": "Universal Sideway / Body Collection / cross-family conflict resolver",
        "state": "OPEN_EXCLUDED_FROM_MINIMAL_V2"
    },
    {
        "priority": 7,
        "topic": "Trade execution layer and prospective proof",
        "state": "AFTER_SIGNAL_RUN_V2_FREEZE"
    }
]

d["latest_completed_closures"] = [
    "docs/0700_EXISTING_KNOWLEDGE_SUFFICIENCY_AUDIT_2026-09-13.md",
    "docs/0700_D1_DAY_RUN_SOURCE_REREVIEW_2026-09-13.md",
    "docs/0700_DAILY_FRAME_SR_SELECTOR_SOURCE_CLOSURE_2026-09-13.md",
    "docs/0700_PAT50_DENOMINATOR_SOURCE_CLOSURE_2026-09-13.md",
    "docs/0700_Q4_H4_CONSUMED_SHAPE_CROSS_PERIOD_2026-09-12.md"
]

d["supersession_notes"] = [
    {
        "old": "docs/0700_D1_DAY_RUN_SOURCE_CLOSURE_2026-09-13.md stronger staged equation",
        "current": "docs/0700_D1_DAY_RUN_SOURCE_REREVIEW_2026-09-13.md",
        "reason": "Later re-review narrows safe authority to a 5,000–10,000 Day run family with exact stage semantics still open."
    },
    {
        "old": "PAT2 exact denominator unresolved through 2026-09-09",
        "current": "docs/0700_PAT50_DENOMINATOR_SOURCE_CLOSURE_2026-09-13.md",
        "reason": "Cross-source review closes PAT2 midpoint basis as prior full candle range including wick."
    },
    {
        "old": "docs/CURRENT_RESEARCH_STATE.json updated 2026-09-09 with RQ-012 active",
        "current": "RQ-013 + docs/0700_WORKSTREAM_STATE.json",
        "reason": "07:00 research Q1-Q4 and source closures continued after the central state stopped being maintained."
    }
]

d["do_not_repeat"] = [
    "Do not restart 07:00 research from raw YouTube inventory before checking this workstream state and the source coverage ledger.",
    "Do not claim D1 exact 5,000-primary / 10,000-continuation semantics as universal; later re-review narrowed it.",
    "Do not restart PAT2 denominator discovery: FULL candle range including wick is source-closed for PAT2.",
    "Do not reopen Q1-Q4 to replace the historical PAT2 BODY proxy; create a new V2.",
    "Do not treat legacy Daily Frame side support from pre-reanchor origin selection as current confirmation.",
    "Do not treat opposite-direction surviving origin as a proven veto.",
    "Do not impose an exact simultaneous MTF minimum.",
    "Do not turn the Q4 replication 8/8 high-consumed subgroup into a 100% system rule.",
    "Do not derive unresolved source geometry by selecting the best historical backtest result."
]

p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("updated", p)
