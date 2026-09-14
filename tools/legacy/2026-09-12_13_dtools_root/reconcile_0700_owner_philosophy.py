import json
from pathlib import Path

root = Path(r"D:\nexus-xau-engine-repo")
old_ref = "docs/0700_PROJECT_OBJECTIVE_AND_DECISION_DOCTRINE_2026-09-13.md"
ref = "docs/0700_OPERATING_PHILOSOPHY_AND_SUCCESS_CRITERIA_2026-09-13.md"
stamp = "2026-09-13T05:40:00+07:00"

# Update the existing canonical philosophy doc instead of creating a duplicate.
p = root / ref
s = p.read_text(encoding="utf-8")
if "Authority: OWNER-DIRECT PROJECT OBJECTIVE" not in s:
    s = s.replace(
        "Status: PROJECT-LEVEL OPERATING PRINCIPLE / MUST BE READ BEFORE 07:00 RESEARCH OR IMPLEMENTATION",
        "Status: PROJECT-LEVEL OPERATING PRINCIPLE / MUST BE READ BEFORE 07:00 RESEARCH OR IMPLEMENTATION\n\nAuthority: OWNER-DIRECT PROJECT OBJECTIVE"
    )
if "## Human-understandable UI / explainability requirement" not in s:
    s += """\n\n## Human-understandable UI / explainability requirement\n\nThe owner must not be required to trust hidden equations that only NEXUS understands.\n\nA later 07:00 UI should expose, in understandable language and visual state:\n\n- current timeframe/context;\n- active origin/run;\n- consumed and remaining run state;\n- point-check status;\n- Daily Frame/location;\n- PA/PAT/SIG state and definitions;\n- relevant wick/body/zone references;\n- confirmation state;\n- conflicting or unresolved evidence;\n- final decision: ENTER / PASS / STUDY;\n- plain-language reason for that decision;\n- source links/timestamps where useful.\n\nThe UI is an explainability and inspection layer. It must display the evidence used by the engine and must not invent or override research logic.\n\nThis requirement exists because project success includes human auditability and shared understanding, not only correct hidden computation.\n"""
p.write_text(s, encoding="utf-8")

# AGENTS: replace duplicate reference and normalize bootstrap numbering/order.
p = root / "AGENTS.md"
s = p.read_text(encoding="utf-8").replace(old_ref, ref)
start = s.index("1. `PROJECT_BOOTSTRAP.md`")
end = s.index("\n\nDo not begin a new source investigation", start)
block = """1. `PROJECT_BOOTSTRAP.md`
2. `docs/0700_OPERATING_PHILOSOPHY_AND_SUCCESS_CRITERIA_2026-09-13.md`
3. `skills/nexus-xau-research/SKILL.md`
4. run `.venv\\Scripts\\python.exe scripts\\research_preflight.py` and require `NEXUS_RESEARCH_PREFLIGHT=PASS`;
5. `docs/NEXUS_PROJECT_MAINTENANCE_POLICY.md`
6. `TOOLS.md`
7. `docs/CURRENT_RESEARCH_STATE.json`
8. the active workstream dashboard referenced by current state; currently `docs/0700_WORKSTREAM_STATE.json`
9. `docs/CANONICAL_CLAIM_REGISTER_2026-09-03.json`
10. `docs/SOURCE_COVERAGE_LEDGER.json`
11. `research_queue/QUEUE.json`
12. the active worksheet referenced by `research_queue/QUEUE.json -> active.worksheet`
13. the latest checkpoint referenced by the active queue/current-state/workstream checkpoint fields
14. any additional latest source/checkpoint files listed in `docs/CURRENT_RESEARCH_STATE.json -> research_loop.load_order`"""
s = s[:start] + block + s[end:]
s = s.replace(" -> Workstream Philosophy ->", " ->")
p.write_text(s, encoding="utf-8")

# Bootstrap and skill: replace any duplicate doctrine ref with the existing philosophy ref.
for rel in ["PROJECT_BOOTSTRAP.md", "skills/nexus-xau-research/SKILL.md"]:
    p = root / rel
    s = p.read_text(encoding="utf-8").replace(old_ref, ref)
    # remove duplicate minimum-read bullet if it appears twice by exact text
    lines = s.splitlines()
    out = []
    seen = set()
    duplicate_key = ref
    for line in lines:
        if duplicate_key in line:
            norm = line.strip()
            if norm in seen:
                continue
            seen.add(norm)
        out.append(line)
    p.write_text("\n".join(out) + "\n", encoding="utf-8")

# Preflight core path.
p = root / "scripts" / "research_preflight.py"
s = p.read_text(encoding="utf-8").replace(old_ref, ref)
p.write_text(s, encoding="utf-8")

# Structured files: replace references and dedupe load_order/latest lists.
for rel in [
    "docs/CURRENT_RESEARCH_STATE.json",
    "docs/0700_WORKSTREAM_STATE.json",
    "docs/CANONICAL_CLAIM_REGISTER_2026-09-03.json",
    "research_queue/QUEUE.json",
]:
    p = root / rel
    d = json.loads(p.read_text(encoding="utf-8"))
    raw = json.dumps(d, ensure_ascii=False)
    raw = raw.replace(old_ref, ref)
    d = json.loads(raw)
    d["updated_at"] = stamp

    if rel.endswith("CURRENT_RESEARCH_STATE.json"):
        loop = d.get("research_loop") or {}
        order = loop.get("load_order") or []
        dedup = []
        for x in order:
            if x not in dedup:
                dedup.append(x)
        loop["load_order"] = dedup
        d["research_loop"] = loop
    elif rel.endswith("0700_WORKSTREAM_STATE.json"):
        vals = d.get("latest_completed_closures") or []
        d["latest_completed_closures"] = list(dict.fromkeys(vals))

    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Active worksheet reference.
p = root / "research_queue" / "active" / "RQ-013_0700_EXISTING_KNOWLEDGE_REANCHOR.md"
s = p.read_text(encoding="utf-8").replace(old_ref, ref)
p.write_text(s, encoding="utf-8")

print("reconciled owner philosophy to existing canonical document")
