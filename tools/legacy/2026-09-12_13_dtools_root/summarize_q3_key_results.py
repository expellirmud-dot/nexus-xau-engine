import pandas as pd, json
from pathlib import Path
roots={
"D":Path(r"D:\nexus-xau-engine-repo\results\0700_Q3_DISTINCT_INFORMATION\DISCOVERY_2022_09_TO_2023_03"),
"R":Path(r"D:\nexus-xau-engine-repo\results\0700_Q3_DISTINCT_INFORMATION\REPLICATION_2023_09_TO_2023_11_23"),
}
out={}
for label,root in roots.items():
    p=pd.read_csv(root/"Q3_PARTIAL_ASSOCIATIONS.csv")
    pair=pd.read_csv(root/"Q3_PAIRWISE_SPEARMAN.csv")
    loo=pd.read_csv(root/"Q3_LEAVE_ONE_OUT.csv")
    out[label]={
      "H4_partial":p[p.origin_tf.eq("H4")][["analysis_level","model_family","feature","n_rows","partial_rho"]].to_dict("records"),
      "H1_partial":p[p.origin_tf.eq("H1")][["analysis_level","model_family","feature","n_rows","partial_rho"]].to_dict("records"),
      "H4_pair":pair[pair.origin_tf.eq("H4")][["feature_a","feature_b","rho"]].to_dict("records"),
      "H1_pair":pair[pair.origin_tf.eq("H1")][["feature_a","feature_b","rho"]].to_dict("records"),
      "H4_loo":loo[(loo.origin_tf.eq("H4"))][["model_family","model","removed_feature","fit_status","log_loss","delta_log_loss_vs_full","coefficient_signs"]].to_dict("records"),
      "H1_loo":loo[(loo.origin_tf.eq("H1"))][["model_family","model","removed_feature","fit_status","log_loss","delta_log_loss_vs_full","coefficient_signs"]].to_dict("records"),
    }
print(json.dumps(out,ensure_ascii=False,indent=2))
