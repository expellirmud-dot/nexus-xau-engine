import json
from pathlib import Path

root = Path(r"D:\nexus-xau-engine-repo")
stamp = "2026-09-13T05:40:00+07:00"
doctrine = "docs/0700_PROJECT_OBJECTIVE_AND_DECISION_DOCTRINE_2026-09-13.md"

# AGENTS.md
p = root / "AGENTS.md"
s = p.read_text(encoding="utf-8")
s = s.replace(
    "1. `PROJECT_BOOTSTRAP.md`\n2. `skills/nexus-xau-research/SKILL.md`",
    "1. `PROJECT_BOOTSTRAP.md`\n2. `docs/0700_PROJECT_OBJECTIVE_AND_DECISION_DOCTRINE_2026-09-13.md`\n3. `skills/nexus-xau-research/SKILL.md`"
)
# renumber subsequent list if still old numbering
s = s.replace("3. run `.venv\\Scripts\\python.exe scripts\\research_preflight.py`", "4. run `.venv\\Scripts\\python.exe scripts\\research_preflight.py`")
s = s.replace("4. `docs/NEXUS_PROJECT_MAINTENANCE_POLICY.md`", "5. `docs/NEXUS_PROJECT_MAINTENANCE_POLICY.md`")
s = s.replace("5. `TOOLS.md`", "6. `TOOLS.md`")
s = s.replace("6. `docs/CURRENT_RESEARCH_STATE.json`", "7. `docs/CURRENT_RESEARCH_STATE.json`")
s = s.replace("7. `docs/CANONICAL_CLAIM_REGISTER_2026-09-03.json`", "8. `docs/CANONICAL_CLAIM_REGISTER_2026-09-03.json`")
s = s.replace("8. `docs/SOURCE_COVERAGE_LEDGER.json`", "9. `docs/SOURCE_COVERAGE_LEDGER.json`")
s = s.replace("9. `research_queue/QUEUE.json`", "10. `research_queue/QUEUE.json`")
s = s.replace("10. the active worksheet", "11. the active worksheet")
s = s.replace("11. the latest checkpoint", "12. the latest checkpoint")
s = s.replace("12. any additional latest", "13. any additional latest")
if "What is the governing 07:00 project objective and what does PASS mean?" not in s:
    s = s.replace(
        "- What is the active workstream and research question?\n",
        "- What is the governing 07:00 project objective and what does PASS mean?\n- What is the active workstream and research question?\n"
    )
s = s.replace(
    "`AGENTS.md -> PROJECT_BOOTSTRAP.md -> nexus-xau-research SKILL",
    "`AGENTS.md -> PROJECT_BOOTSTRAP.md -> 07:00 Project Objective/Decision Doctrine -> nexus-xau-research SKILL"
)
p.write_text(s, encoding="utf-8")

# PROJECT_BOOTSTRAP.md
p = root / "PROJECT_BOOTSTRAP.md"
s = p.read_text(encoding="utf-8")
if "0700_PROJECT_OBJECTIVE_AND_DECISION_DOCTRINE_2026-09-13.md" not in s:
    s = s.replace(
        "1. Read `AGENTS.md`.\n2. Read `skills/nexus-xau-research/SKILL.md`.",
        "1. Read `AGENTS.md`.\n2. Read `docs/0700_PROJECT_OBJECTIVE_AND_DECISION_DOCTRINE_2026-09-13.md`.\n3. Read `skills/nexus-xau-research/SKILL.md`."
    )
    s = s.replace("3. Run the repository preflight:", "4. Run the repository preflight:")
    s = s.replace("4. Read the files reported by preflight", "5. Read the files reported by preflight")
    s = s.replace("5. Read any additional current checkpoint", "6. Read any additional current checkpoint")
if "- governing 07:00 project objective;" not in s:
    s = s.replace(
        "- current active workstream;\n",
        "- governing 07:00 project objective;\n- meaning of PASS / unknown-state handling;\n- current active workstream;\n"
    )
if "0700_PROJECT_OBJECTIVE_AND_DECISION_DOCTRINE" not in s.split("## Memory model",1)[-1]:
    s = s.replace(
        "Use these files for different kinds of project memory:\n",
        "Use these files for different kinds of project memory:\n\n- `docs/0700_PROJECT_OBJECTIVE_AND_DECISION_DOCTRINE_2026-09-13.md` = owner-direct definition of what the 07:00 system is, what success means, how unknown states are handled, and how real versus synthetic data may be used.\n"
    )
p.write_text(s, encoding="utf-8")

# SKILL.md
p = root / "skills" / "nexus-xau-research" / "SKILL.md"
s = p.read_text(encoding="utf-8")
if "0700_PROJECT_OBJECTIVE_AND_DECISION_DOCTRINE_2026-09-13.md" not in s:
    s = s.replace(
        "1. read `AGENTS.md`;\n2. read `PROJECT_BOOTSTRAP.md`;",
        "1. read `AGENTS.md`;\n2. read `PROJECT_BOOTSTRAP.md`;\n3. read `docs/0700_PROJECT_OBJECTIVE_AND_DECISION_DOCTRINE_2026-09-13.md`;"
    )
    s = s.replace("3. run `.venv\\Scripts\\python.exe scripts\\research_preflight.py`;", "4. run `.venv\\Scripts\\python.exe scripts\\research_preflight.py`;")
    s = s.replace("4. read the active/current files", "5. read the active/current files")
    s = s.replace("5. state what the workstream already knows", "6. state what the workstream already knows")
    s = s.replace("6. inspect `docs/SOURCE_COVERAGE_LEDGER.json`", "7. inspect `docs/SOURCE_COVERAGE_LEDGER.json`")
if "PASS / NO TRADE / STUDY" not in s:
    s = s.replace(
        "Do not continue if preflight fails or if the active workstream/question cannot be reconstructed from repository state.",
        "For 07:00 work, preserve the owner-direct doctrine that unresolved/novel states may terminate as PASS / NO TRADE / STUDY rather than being forced into a known rule.\n\nDo not continue if preflight fails or if the active workstream/question cannot be reconstructed from repository state."
    )
p.write_text(s, encoding="utf-8")

# Preflight core and comprehension gate
p = root / "scripts" / "research_preflight.py"
s = p.read_text(encoding="utf-8")
core_line = '    Path("docs/0700_PROJECT_OBJECTIVE_AND_DECISION_DOCTRINE_2026-09-13.md"),\n'
if core_line not in s:
    s = s.replace(
        '    Path("PROJECT_BOOTSTRAP.md"),\n',
        '    Path("PROJECT_BOOTSTRAP.md"),\n' + core_line
    )
if 'State the 07:00 project objective and unknown-state/PASS doctrine.' not in s:
    s = s.replace(
        '            "State the active 07:00 workstream and active RQ/worksheet.",\n',
        '            "State the 07:00 project objective and unknown-state/PASS doctrine.",\n            "State the active 07:00 workstream and active RQ/worksheet.",\n'
    )
p.write_text(s, encoding="utf-8")

# Current research state
p = root / "docs" / "CURRENT_RESEARCH_STATE.json"
d = json.loads(p.read_text(encoding="utf-8"))
d["updated_at"] = stamp
d["project_objective"] = {
    "authority": "OWNER_DIRECT",
    "ref": doctrine,
    "summary": "Selective evidence-driven 07:00 decision system, not a generic always-trading EA. Use all relevant pre-07:00 evidence; act only when the current version understands the state sufficiently; otherwise PASS/NO TRADE/STUDY and record the novel state.",
    "success_definition": "Maximize process completeness, traceability, deterministic handling of known states, and safe fail-closed behavior. Do not require or manufacture a target market win rate.",
    "data_policy": "Real historical/forward data tests market behavior; synthetic data tests logic, invariants, and controlled edge cases. Synthetic data cannot establish market frequency or profitability."
}
loop = d.get("research_loop") or {}
load_order = loop.get("load_order") or []
if doctrine not in load_order:
    # place immediately after bootstrap/skill if possible
    load_order.insert(3 if len(load_order) >= 3 else 0, doctrine)
loop["load_order"] = load_order
d["research_loop"] = loop
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Workstream dashboard
p = root / "docs" / "0700_WORKSTREAM_STATE.json"
d = json.loads(p.read_text(encoding="utf-8"))
d["updated_at"] = stamp
d["owner_objective"] = {
    "ref": doctrine,
    "system_type": "SELECTIVE_0700_EVIDENCE_DRIVEN_DECISION_SYSTEM",
    "not": "GENERIC_24_7_AUTO_TRADER",
    "unknown_state_action": "PASS_NO_TRADE_RECORD_AND_STUDY",
    "success_focus": [
        "process correctness",
        "evidence completeness",
        "traceability",
        "safe handling of unknown/conflicting state",
        "versioned learning from historical and forward evidence"
    ],
    "synthetic_data_role": "Controlled logic/edge-case verification only; never evidence of market frequency or profitability."
}
if doctrine not in d.get("latest_completed_closures", []):
    d["latest_completed_closures"] = [doctrine] + d.get("latest_completed_closures", [])
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Active RQ worksheet
p = root / "research_queue" / "active" / "RQ-013_0700_EXISTING_KNOWLEDGE_REANCHOR.md"
s = p.read_text(encoding="utf-8")
if "## Governing project objective" not in s:
    insert = f"""\n## Governing project objective\n\nMandatory owner-direct authority:\n\n`{doctrine}`\n\nThis workstream is building a selective evidence-driven 07:00 decision system, not a generic always-trading EA. Unknown or insufficiently understood states must be eligible for PASS / NO TRADE / RECORD FOR RESEARCH. Real historical data is used to test market behavior; synthetic data may be used for controlled logic/edge-case verification but cannot prove market frequency or profitability.\n\n"""
    s = s.replace("## Current audit authority\n", insert + "## Current audit authority\n")
p.write_text(s, encoding="utf-8")

# Canonical claim register: owner-direct project objective
p = root / "docs" / "CANONICAL_CLAIM_REGISTER_2026-09-03.json"
d = json.loads(p.read_text(encoding="utf-8"))
d["updated_at"] = stamp
claims = d.get("claims", [])
cid = "0700_OWNER_DECISION_SYSTEM_OBJECTIVE"
claim = {
    "claim_id": cid,
    "canonical_statement": "The 07:00 project is a selective evidence-driven decision system, not a generic 24/7 auto-trader. It may use all relevant information knowable before/at 07:00 to construct state. If the current version encounters insufficient, conflicting, or materially novel state, PASS/NO TRADE/RECORD FOR RESEARCH is a correct terminal decision. Synthetic data may verify logic and edge cases but cannot establish market frequency, robustness, profitability, or win rate.",
    "status": "ACTIVE_OWNER_DIRECT_PROJECT_OBJECTIVE",
    "engine_permission": "GOVERNING_DECISION_AND_RESEARCH_DOCTRINE",
    "source_refs": [doctrine],
    "risk_flags": [
        "DO_NOT_FORCE_DAILY_TRADE",
        "DO_NOT_HARDCODE_OUTCOME_SELECTED_PATTERN_CATALOG",
        "DO_NOT_USE_SYNTHETIC_DATA_AS_MARKET_PERFORMANCE_EVIDENCE",
        "UNKNOWN_STATE_MUST_BE_FAIL_CLOSED_OR_RESEARCHED",
        "NO_PRECOMMITTED_WIN_RATE_CLAIM"
    ],
    "provenance_note": "Direct owner clarification recorded 2026-09-13. Highest project authority for interpreting the purpose and success criteria of the narrow 07:00 workstream."
}
found = False
for i, c in enumerate(claims):
    if isinstance(c, dict) and c.get("claim_id") == cid:
        claims[i].update(claim)
        found = True
        break
if not found:
    claims.append(claim)
d["claims"] = claims
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Queue timestamp + active summary
p = root / "research_queue" / "QUEUE.json"
d = json.loads(p.read_text(encoding="utf-8"))
d["updated_at"] = stamp
active = d.get("active") or {}
active["governing_objective_ref"] = doctrine
active["current_summary"] = "Persist owner-direct 07:00 decision doctrine, verify restart visibility, then audit historical-data sufficiency before freezing MINIMAL_V2."
d["active"] = active
for item in d.get("items", []):
    if isinstance(item, dict) and item.get("id") == "RQ-013":
        item["current_summary"] = "Persist and enforce the owner-direct 07:00 decision doctrine, complete restart-safe re-anchor, then audit historical-data sufficiency and freeze MINIMAL_V2."
        item["governing_objective_ref"] = doctrine
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print("patched doctrine into bootstrap/current-state/workstream/queue/claims/preflight")
