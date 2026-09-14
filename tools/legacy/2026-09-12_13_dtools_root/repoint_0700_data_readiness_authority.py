import json
from pathlib import Path

root = Path(r"D:\nexus-xau-engine-repo")
old = "docs/0700_DATA_SUFFICIENCY_AND_TEST_STRATEGY_2026-09-13.md"
cur = "docs/0700_HISTORICAL_DATA_READINESS_AND_TEST_STRATEGY_2026-09-13.md"

for rel in [
    "docs/CURRENT_RESEARCH_STATE.json",
    "docs/0700_WORKSTREAM_STATE.json",
    "research_queue/QUEUE.json",
]:
    p = root / rel
    d = json.loads(p.read_text(encoding="utf-8"))
    raw = json.dumps(d, ensure_ascii=False).replace(old, cur)
    d = json.loads(raw)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

p = root / "research_queue" / "active" / "RQ-013_0700_EXISTING_KNOWLEDGE_REANCHOR.md"
s = p.read_text(encoding="utf-8").replace(old, cur)
p.write_text(s, encoding="utf-8")

print("repointed data readiness authority")
