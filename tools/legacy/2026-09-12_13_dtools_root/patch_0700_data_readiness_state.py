import json
from pathlib import Path

root = Path(r"D:\nexus-xau-engine-repo")
stamp = "2026-09-13T05:40:00+07:00"
checkpoint = "docs/0700_DATA_SUFFICIENCY_AND_TEST_STRATEGY_2026-09-13.md"

# Current state
p = root / "docs" / "CURRENT_RESEARCH_STATE.json"
d = json.loads(p.read_text(encoding="utf-8"))
d["updated_at"] = stamp
d["data_readiness_0700"] = {
    "status": "SUFFICIENT_FOR_MINIMAL_V2_DEVELOPMENT_NOT_PRISTINE_CONFIRMATION",
    "checkpoint": checkpoint,
    "complete_real_periods": [
        {
            "range": "2022-09-01..2023-03-31",
            "m1_rows": 305280,
            "v1_0700_days": 150,
            "role": "development_discovery_failure_map",
            "pristine": False
        },
        {
            "range": "2023-09-01..2023-11-23",
            "m1_rows": 120960,
            "v1_0700_days": 60,
            "role": "cross_period_development_replay",
            "pristine": False
        }
    ],
    "complete_0700_snapshots": 210,
    "synthetic_policy": "Use for deterministic logic/boundary/edge-case verification only; never for market frequency, win rate, robustness, or profitability claims.",
    "confirmatory_gap": "Need repaired/reserved untouched historical range or future prospective/forward data after V2 freeze."
}
d["next_steps"] = [
    "Freeze 0700_MINIMAL_V2 specification from existing evidence: H4-only origin/run, PAT2 FULL-RANGE, existing Daily Frame, PATH_REMAINING, no consumed threshold.",
    "Version the V1 scaffold into V2 without rewriting Q1-Q4 historical outputs.",
    "Create synthetic boundary fixtures for no-lookahead, point-check touch/near-miss, PAT2 midpoint boundaries, ambiguous same-bar, Daily Frame tie, and unknown/PASS states.",
    "Replay the two complete real periods (210 07:00 daily snapshots) and produce a failure/novelty map, not only an outcome percentage.",
    "Only reopen source research for named blockers; reserve/repair new data only after V2 is frozen for confirmatory use."
]
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Workstream
p = root / "docs" / "0700_WORKSTREAM_STATE.json"
d = json.loads(p.read_text(encoding="utf-8"))
d["updated_at"] = stamp
d["data_readiness"] = {
    "checkpoint": checkpoint,
    "development": "READY",
    "real_complete_0700_snapshots": 210,
    "confirmatory": "NOT_PRISTINE_YET",
    "synthetic": "ALLOWED_FOR_LOGIC_EDGE_CASES_ONLY",
    "execution_pnl": "NOT_READY"
}
aq = d.get("active_question") or {}
aq["next_action"] = "Freeze 0700_MINIMAL_V2 from existing evidence, then implement synthetic boundary tests before replaying the two complete real historical periods."
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
active["latest_checkpoint"] = checkpoint
active["current_summary"] = "Owner philosophy and data-readiness audit are persisted. Existing real data is sufficient for MINIMAL_V2 development; next action is to freeze V2 before any new outcome replay or broad YouTube review."
d["active"] = active
for item in d.get("items", []):
    if isinstance(item, dict) and item.get("id") == "RQ-013":
        item["checkpoint_ref"] = checkpoint
        item["current_summary"] = "Continuity is repaired and data readiness is established. Freeze H4/PAT2-only 0700_MINIMAL_V2, then synthetic boundary tests and real-period failure-map replay."
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Active worksheet
p = root / "research_queue" / "active" / "RQ-013_0700_EXISTING_KNOWLEDGE_REANCHOR.md"
s = p.read_text(encoding="utf-8")
if "## Data readiness checkpoint" not in s:
    s += f"""\n\n## Data readiness checkpoint\n\nAuthority:\n\n`{checkpoint}`\n\nCurrent decision:\n\n- existing complete real historical data is sufficient to build/debug and run the first MINIMAL_V2 failure-map replay;\n- two complete periods provide 210 07:00 daily snapshots under the V1 scaffold;\n- those periods are not pristine confirmation data because Q1-Q4 already used them;\n- synthetic data is authorized for deterministic boundary/edge-case verification only;\n- new market-performance confirmation requires a repaired/reserved untouched historical range or prospective data after V2 freeze.\n\nNext action: freeze `0700_MINIMAL_V2` before changing the engine or opening new V2 outcomes.\n"""
p.write_text(s, encoding="utf-8")

print("patched data readiness into central state")
