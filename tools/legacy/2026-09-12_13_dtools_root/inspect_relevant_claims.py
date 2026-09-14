import json
from pathlib import Path
p=Path(r"D:\nexus-xau-engine-repo\docs\CANONICAL_CLAIM_REGISTER_2026-09-03.json")
d=json.loads(p.read_text(encoding="utf-8"))
out=[]
for c in d["claims"]:
    cid=str(c.get("claim_id",""))
    st=str(c.get("canonical_statement",""))
    blob=(cid+" "+st).upper()
    if any(k in blob for k in ["1000","1500","5000","10000","REMAINING"," RUN","DAILY FRAME","MAE PLA","SUPPORT","RESISTANCE"]):
        out.append({"claim_id":cid,"status":c.get("status"),"canonical_statement":st,"source_refs":c.get("source_refs"),"risk_flags":c.get("risk_flags")})
print(json.dumps(out,ensure_ascii=False,indent=2))
