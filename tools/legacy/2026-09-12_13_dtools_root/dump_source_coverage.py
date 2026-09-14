import json
from pathlib import Path
p=Path(r"D:\nexus-xau-engine-repo\docs\SOURCE_COVERAGE_LEDGER.json")
d=json.loads(p.read_text(encoding="utf-8"))
for e in d["entries"]:
    print(json.dumps({
        "coverage_id":e.get("coverage_id"),
        "source_id":e.get("source_id"),
        "topic":e.get("topic"),
        "window":e.get("window"),
        "status":e.get("status"),
        "finding":e.get("finding"),
        "residual_unknowns":e.get("residual_unknowns"),
        "last_reviewed_at":e.get("last_reviewed_at")
    },ensure_ascii=False))
