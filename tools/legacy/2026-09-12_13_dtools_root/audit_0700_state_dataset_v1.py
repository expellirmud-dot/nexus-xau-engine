import json
from pathlib import Path
import pandas as pd

root=Path(r"D:\nexus-xau-engine-repo\results\0700_STATE_DATASET_V1\DISCOVERY_2022_09_TO_2023_03")
day=pd.read_csv(root/"0700_day_state.csv")
orig=pd.read_csv(root/"0700_origin_candidates.csv")
ev=pd.read_csv(root/"0700_confirmation_events.csv")

def counts(s):
    return {str(k):int(v) for k,v in s.value_counts(dropna=False).to_dict().items()}

out={
"day_rows":len(day),
"day_unique":int(day["day_id"].nunique()),
"day_first":str(day["cutoff_utc"].iloc[0]),
"day_last":str(day["cutoff_utc"].iloc[-1]),
"frame_candidate_counts":counts(day["daily_frame_candidate_count"]),
"frame_tie_count":int(day["daily_frame_tie_ambiguous"].sum()),
"origin_rows":len(orig),
"origin_unique_ids":int(orig["origin_id"].nunique()),
"origin_tf_rows":counts(orig["origin_tf"]),
"origin_tf_unique_ids":{tf:int(g["origin_id"].nunique()) for tf,g in orig.groupby("origin_tf")},
"origin_side_rows":counts(orig["origin_side"]),
"origin_validity":counts(orig["origin_validity_state"]),
"point_check_state":counts(orig["point_check_state"]),
"source_partial_survival_proxy":counts(orig["source_partial_survival_proxy"]),
"origin_days_with_measurable":int((day["measurable_incomplete_origin_count"]>0).sum()),
"origin_measurable_count_summary":day["measurable_incomplete_origin_count"].describe().to_dict(),
"source_partial_surviving_days":int((day["source_partial_surviving_origin_count"]>0).sum()),
"source_partial_surviving_count_summary":day["source_partial_surviving_origin_count"].describe().to_dict(),
"d1_unresolved_count_summary":day["unresolved_d1_origin_count"].describe().to_dict(),
"confirmation_rows":len(ev),
"confirmation_unique_ids":int(ev["event_id"].nunique()),
"confirmation_tf":counts(ev["event_tf"]),
"confirmation_side":counts(ev["event_side"]),
"frame_side":counts(ev["frame_side"]),
"alignment_exact":counts(ev["alignment_count_exact"]),
"alignment_recent1":counts(ev["alignment_count_recent_1_tf_bar"]),
"alignment_recent2":counts(ev["alignment_count_recent_2_tf_bars"]),
"max_minutes_since_0700":float(ev["minutes_since_0700"].max()),
"min_minutes_since_0700":float(ev["minutes_since_0700"].min()),
"duplicate_day":int(day.duplicated(["day_id"]).sum()),
"duplicate_origin_day":int(orig.duplicated(["day_id","origin_id"]).sum()),
"duplicate_event":int(ev.duplicated(["event_id"]).sum()),
"null_cutoff_h1":int(day["h1_close"].isna().sum()),
"null_cutoff_h4":int(day["h4_close"].isna().sum()),
"null_cutoff_d1":int(day["d1_close"].isna().sum()),
"negative_origin_age":int((orig["origin_age_hours"]<0).sum()),
"nonpositive_remaining":int((orig["remaining_points_at_0700"].dropna()<=0).sum()),
"event_at_or_before_cutoff":int((pd.to_datetime(ev["event_known_at"],utc=True)<=pd.to_datetime(ev["day_id"],utc=True)).sum()),
"future_touch_timestamp_leak":int((
    pd.to_datetime(orig["point_check_first_touch_before_cutoff_at"],utc=True,errors="coerce")
    >= pd.to_datetime(orig["cutoff_utc"],utc=True)
).fillna(False).sum()),
}
print(json.dumps(out,ensure_ascii=False,indent=2,default=float))
