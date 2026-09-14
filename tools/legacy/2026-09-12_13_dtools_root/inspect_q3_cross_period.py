import pandas as pd, json
from pathlib import Path

roots={
"D":Path(r"D:\nexus-xau-engine-repo\results\0700_Q3_DISTINCT_INFORMATION\DISCOVERY_2022_09_TO_2023_03"),
"R":Path(r"D:\nexus-xau-engine-repo\results\0700_Q3_DISTINCT_INFORMATION\REPLICATION_2023_09_TO_2023_11_23"),
}
out={}
for label,root in roots.items():
    partial=pd.read_csv(root/"Q3_PARTIAL_ASSOCIATIONS.csv")
    pair=pd.read_csv(root/"Q3_PAIRWISE_SPEARMAN.csv")
    loo=pd.read_csv(root/"Q3_LEAVE_ONE_OUT.csv")
    out[label]={
        "partial":partial.to_dict("records"),
        "pairwise":pair.to_dict("records"),
        "leave_one_out":loo.to_dict("records"),
    }
print(json.dumps(out,ensure_ascii=False,indent=2))
