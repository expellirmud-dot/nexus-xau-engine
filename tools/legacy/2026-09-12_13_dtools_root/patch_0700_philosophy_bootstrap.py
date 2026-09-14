from pathlib import Path
import json

root = Path(r"D:\nexus-xau-engine-repo")
philosophy = "docs/0700_OPERATING_PHILOSOPHY_AND_SUCCESS_CRITERIA_2026-09-13.md"

# AGENTS
p = root / "AGENTS.md"
s = p.read_text(encoding="utf-8")
s = s.replace(
    "6. `docs/CURRENT_RESEARCH_STATE.json`\n7. `docs/CANONICAL_CLAIM_REGISTER_2026-09-03.json`",
    "6. `docs/CURRENT_RESEARCH_STATE.json`\n7. the active workstream dashboard referenced by current state; currently `docs/0700_WORKSTREAM_STATE.json`\n8. `docs/0700_OPERATING_PHILOSOPHY_AND_SUCCESS_CRITERIA_2026-09-13.md` for the current 07:00 workstream purpose/success criteria\n9. `docs/CANONICAL_CLAIM_REGISTER_2026-09-03.json`"
)
s = s.replace(
    "8. `docs/SOURCE_COVERAGE_LEDGER.json`\n9. `research_queue/QUEUE.json`\n10. the active worksheet",
    "10. `docs/SOURCE_COVERAGE_LEDGER.json`\n11. `research_queue/QUEUE.json`\n12. the active worksheet"
)
s = s.replace(
    "11. the latest checkpoint referenced by the active queue/current-state checkpoint fields\n12. any additional latest source/checkpoint files",
    "13. the latest checkpoint referenced by the active queue/current-state/workstream checkpoint fields\n14. any additional latest source/checkpoint files"
)
s = s.replace(
    "- What is the active research question?\n",
    "- What is the active workstream and research question?\n- What does success mean for this workstream, and what is explicitly not the goal?\n"
)
s = s.replace(
    "1. check `CURRENT_RESEARCH_STATE`;\n2. check the canonical claim register;",
    "1. check `CURRENT_RESEARCH_STATE` and the active workstream dashboard;\n2. check the current workstream philosophy/success-criteria document when one exists;\n3. check the canonical claim register;"
)
s = s.replace(
    "3. check the active RQ worksheet and its checkpoint references;\n4. check `SOURCE_COVERAGE_LEDGER`.",
    "4. check the active RQ worksheet and its checkpoint references;\n5. check `SOURCE_COVERAGE_LEDGER`."
)
s = s.replace(
    "3. update `CURRENT_RESEARCH_STATE.json`;\n4. update `research_queue/QUEUE.json`",
    "3. update `CURRENT_RESEARCH_STATE.json` and the active workstream dashboard when workstream state changed;\n4. update `research_queue/QUEUE.json`"
)
s = s.replace(
    "Current State -> Active Workstream Dashboard -> Canonical Claims",
    "Current State -> Active Workstream Dashboard -> Workstream Philosophy -> Canonical Claims"
)
p.write_text(s, encoding="utf-8")

# PROJECT_BOOTSTRAP
p = root / "PROJECT_BOOTSTRAP.md"
s = p.read_text(encoding="utf-8")
needle = "   - the active workstream dashboard referenced by current state; currently `docs/0700_WORKSTREAM_STATE.json`\n"
if philosophy not in s:
    s = s.replace(needle, needle + f"   - `{philosophy}` for current 07:00 purpose/success criteria\n")
s = s.replace(
    "- current active workstream;\n",
    "- current active workstream;\n- current workstream purpose/success criteria and the valid PASS/UNKNOWN behavior;\n"
)
p.write_text(s, encoding="utf-8")

# SKILL
p = root / "skills" / "nexus-xau-research" / "SKILL.md"
s = p.read_text(encoding="utf-8")
s = s.replace(
    "4. read the active/current files identified by preflight, including the active workstream dashboard;\n5. state what the workstream already knows",
    "4. read the active/current files identified by preflight, including the active workstream dashboard and current workstream philosophy/success criteria;\n5. state what the workstream already knows"
)
p.write_text(s, encoding="utf-8")

# Structured states
wp = root / "docs" / "0700_WORKSTREAM_STATE.json"
wd = json.loads(wp.read_text(encoding="utf-8"))
wd["operating_philosophy"] = philosophy
wd["success_definition"] = {
    "primary": "Assemble all legitimately knowable pre-07:00 information into a reproducible 07:00 state and act only when the state is sufficiently understood.",
    "pass_is_valid": True,
    "unknown_behavior": "PASS_NO_TRADE_RECORD_AND_RESEARCH",
    "not_goal": [
        "continuous auto-trading",
        "forcing an entry every day",
        "hard-coding a finite list of winning historical patterns",
        "claiming guaranteed market outcomes"
    ]
}
wp.write_text(json.dumps(wd, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

cp = root / "docs" / "CURRENT_RESEARCH_STATE.json"
cd = json.loads(cp.read_text(encoding="utf-8"))
aw = cd.get("active_0700_workstream") or {}
aw["operating_philosophy"] = philosophy
aw["method"] = "Build a restart-safe 07:00 state engine: use all knowable pre-07:00 context, allow PASS on unknown/unsupported states, learn from replay failures, use synthetic data for controlled logic tests and real data for market evidence."
cd["active_0700_workstream"] = aw
loop = cd.get("research_loop") or {}
lo = loop.get("load_order") or []
if philosophy not in lo:
    insert_at = 7 if len(lo) >= 7 else len(lo)
    lo.insert(insert_at, philosophy)
loop["load_order"] = lo
cd["research_loop"] = loop
cp.write_text(json.dumps(cd, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Preflight required path
pp = root / "scripts" / "research_preflight.py"
s = pp.read_text(encoding="utf-8")
req = '    Path("docs/0700_OPERATING_PHILOSOPHY_AND_SUCCESS_CRITERIA_2026-09-13.md"),\n'
if req not in s:
    s = s.replace('    Path("docs/0700_WORKSTREAM_STATE.json"),\n', '    Path("docs/0700_WORKSTREAM_STATE.json"),\n' + req)
pp.write_text(s, encoding="utf-8")

print("patched philosophy into bootstrap/state/preflight")
