import pandas as pd, json
from pathlib import Path

roots={
"D":Path(r"D:\nexus-xau-engine-repo\results\0700_Q2_CONTINUOUS_MTF\DISCOVERY_2022_09_TO_2023_03\Q2_ASSOCIATIONS.csv"),
"R":Path(r"D:\nexus-xau-engine-repo\results\0700_Q2_CONTINUOUS_MTF\REPLICATION_2023_09_TO_2023_11_23\Q2_ASSOCIATIONS.csv"),
}
out={}
for k,p in roots.items():
    df=pd.read_csv(p)
    x=df[df["outcome"].eq("path_remaining_first_hit")].copy()
    out[k]=x[["analysis_level","stratum","feature","n_rows","n_contexts","rho","target_feature_median","point_feature_median"]].to_dict("records")
print(json.dumps(out,ensure_ascii=False,indent=2))
