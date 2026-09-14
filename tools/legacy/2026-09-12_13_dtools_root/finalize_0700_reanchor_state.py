import json
from pathlib import Path

root=Path(r"D:\nexus-xau-engine-repo")
stamp="2026-09-13T05:18:16+07:00"

paths=[
    root/"docs"/"CURRENT_RESEARCH_STATE.json",
    root/"docs"/"0700_WORKSTREAM_STATE.json",
    root/"docs"/"CANONICAL_CLAIM_REGISTER_2026-09-03.json",
    root/"docs"/"SOURCE_COVERAGE_LEDGER.json",
    root/"research_queue"/"QUEUE.json",
]
for p in paths:
    d=json.loads(p.read_text(encoding="utf-8"))
    d["updated_at"]=stamp
    if p.name=="CURRENT_RESEARCH_STATE.json":
        validation=d.get("validation_status") or {}
        validation["structured_state_reanchor"]="PASSED"
        validation["research_preflight"]="PASS_AFTER_2026_09_13_REANCHOR"
        validation["ruff_current"]="PASS_AFTER_2026_09_13_REANCHOR"
        validation["pytest_current"]="FULL_SUITE_EXIT_CODE_0_AFTER_2026_09_13_REANCHOR"
        d["validation_status"]=validation
        d["completed_checkpoint"]="0700_EXISTING_KNOWLEDGE_SUFFICIENCY_AUDIT_REANCHORED_VALIDATED"
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("updated",p)
