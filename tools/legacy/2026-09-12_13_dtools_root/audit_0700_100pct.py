import json, re
from pathlib import Path
import pandas as pd

root=Path(r"D:\nexus-xau-engine-repo")
rows=[]

# Scan relevant CSV/JSON result artifacts for rate/fraction columns hitting 1.0
for base in [
    root/"results"/"0700_Q1_ORIGIN_CONTEXT",
    root/"results"/"0700_Q2_CONTINUOUS_MTF",
    root/"results"/"0700_Q3_DISTINCT_INFORMATION",
    root/"results"/"0700_Q4_H4_CONSUMED_SHAPE",
    root/"results"/"PATH_REMAINING_DAILY_SIDE_MTF_V2",
    root/"results"/"INHERITED_ORIGIN_CONTEXT_RELATION",
    root/"results"/"SOURCE_PARTIAL_REANCHORED_REMAINING_RUN",
]:
    if not base.exists(): continue
    for p in base.rglob("*.csv"):
        try:
            df=pd.read_csv(p)
        except Exception:
            continue
        for col in df.columns:
            lc=col.lower()
            if any(k in lc for k in ["fraction","rate","pct","percent","reach"]):
                vals=pd.to_numeric(df[col], errors="coerce")
                idx=vals[vals>=0.999999].index
                for i in idx[:20]:
                    rec=df.loc[i].to_dict()
                    # keep compact dimensions and common n/count fields
                    compact={"artifact":str(p.relative_to(root)),"column":col,"value":float(vals.loc[i])}
                    for k,v in rec.items():
                        lk=str(k).lower()
                        if any(t in lk for t in ["period","origin_tf","context","variant","state","quintile","alignment","n_","rows","count","target_first","point_check","sample"]):
                            if pd.notna(v):
                                compact[k]=v
                    rows.append(compact)

print(json.dumps(rows[:300],ensure_ascii=False,indent=2,default=str))
