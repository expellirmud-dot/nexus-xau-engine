import json
from pathlib import Path
root=Path(r"D:\nexus-xau-engine-repo")
for rel in [r"docs\CANONICAL_CLAIM_REGISTER_2026-09-03.json",r"docs\SOURCE_COVERAGE_LEDGER.json",r"research_queue\QUEUE.json"]:
    p=root/rel
    d=json.loads(p.read_text(encoding="utf-8"))
    print("\n###",rel)
    print("top_keys",list(d.keys()))
    if "claims" in d:
        print("claims",len(d["claims"]))
        for c in d["claims"]:
            cid=str(c.get("claim_id",""))
            if any(k in cid.upper() for k in ["PAT","DAILY","DAY","FRAME","0700","M5_BRAKE"]):
                print("CLAIM",cid,"|",c.get("status"),"|",c.get("canonical_statement","")[:220])
    if "entries" in d:
        print("entries",len(d["entries"]))
        print("sample_keys",list(d["entries"][0].keys()) if d["entries"] else [])
        for e in d["entries"]:
            s=json.dumps(e,ensure_ascii=False)
            if any(k in s for k in ["1E_PYPor1qQ","ESHDuiVPJow","jBEM-vWYj_o"]):
                print("ENTRY",e.get("coverage_id") or e.get("id"),"|",e.get("status"),"|",e.get("topic"))
    if "items" in d:
        print("queue_items",[(x.get("id"),x.get("status")) for x in d["items"][-5:]])
