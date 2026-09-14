import json
from pathlib import Path
import pandas as pd

root=Path(r"D:\nexus-xau-engine-repo\results\0700_STATE_DATASET_V1\DISCOVERY_2022_09_TO_2023_03")
orig=pd.read_csv(root/"0700_origin_candidates.csv")
surv=orig[(orig["is_measurable_incomplete"]==True) & (orig["source_partial_survival_proxy"]==True)].copy()

day_rows=[]
for day_id,g in surv.groupby("day_id"):
    dirs=sorted(g["origin_side"].unique())
    tfs=sorted(g["origin_tf"].unique())
    day_rows.append({
        "day_id":day_id,
        "n":len(g),
        "dirs":",".join(dirs),
        "tfs":",".join(tfs),
        "conflict":len(dirs)>1,
    })
day=pd.DataFrame(day_rows)

context=[]
for (day_id,side),g in surv.groupby(["day_id","origin_side"]):
    context.append({
        "day_id":day_id,
        "side":side,
        "n":len(g),
        "tf_set":",".join(sorted(g["origin_tf"].unique())),
        "h1":int((g["origin_tf"]=="H1").sum()),
        "h4":int((g["origin_tf"]=="H4").sum()),
    })
ctx=pd.DataFrame(context)

out={
    "surviving_rows":len(surv),
    "surviving_unique_origins":int(surv["origin_id"].nunique()),
    "rows_by_tf":{str(k):int(v) for k,v in surv["origin_tf"].value_counts().to_dict().items()},
    "rows_by_side":{str(k):int(v) for k,v in surv["origin_side"].value_counts().to_dict().items()},
    "days_with_any":int(day["day_id"].nunique()) if not day.empty else 0,
    "days_direction_state":({
        "BUY_ONLY":int((day["dirs"]=="BUY").sum()),
        "SELL_ONLY":int((day["dirs"]=="SELL").sum()),
        "BUY_SELL_CONFLICT":int(day["conflict"].sum()),
    } if not day.empty else {}),
    "days_tf_set":({str(k):int(v) for k,v in day["tfs"].value_counts().to_dict().items()} if not day.empty else {}),
    "day_side_context_tf_set":({str(k):int(v) for k,v in ctx["tf_set"].value_counts().to_dict().items()} if not ctx.empty else {}),
    "day_side_context_count":len(ctx),
    "day_side_multiple_survivors":int((ctx["n"]>1).sum()) if not ctx.empty else 0,
    "origin_age_hours":surv["origin_age_hours"].describe().to_dict(),
    "remaining_points":surv["remaining_points_at_0700"].describe().to_dict(),
    "consumed_ratio":surv["consumed_ratio_at_0700"].describe().to_dict(),
}
print(json.dumps(out,ensure_ascii=False,indent=2,default=float))
