import pandas as pd, json, os
periods = {
"DISCOVERY_2022_09_2023_03": r"D:\nexus-xau-engine-repo\data\raw\dukascopy\chunks\XAUUSD_M1_BID_2022-09-01_2023-03-31.csv",
"LATER_2024_09_11": r"D:\nexus-xau-engine-repo\data\raw\dukascopy\chunks\XAUUSD_M1_BID_2024-09-01_2024-11-30.csv",
"LATER_2025_09_11": r"D:\nexus-xau-engine-repo\data\raw\dukascopy\chunks\XAUUSD_M1_BID_2025-09-01_2025-11-30.csv",
"MT5_2026_05_26_09_01": r"D:\nexus-xau-engine-repo\data\raw\XAUUSDm_M1_MT5_2026-05-26_2026-09-01.csv",
}
out={"raw_periods":{}}
for name,f in periods.items():
    d=pd.read_csv(f)
    t=pd.to_datetime(d["timestamp"],utc=True)
    active = d["volume"]>0 if "volume" in d else pd.Series(True,index=d.index)
    ta=t[active]
    days=pd.Index(ta.dt.normalize().unique())
    boundary = set(ta[ta.dt.hour.eq(0) & ta.dt.minute.eq(0)].dt.normalize())
    out["raw_periods"][name]={
        "rows":len(d),
        "positive_volume_rows":int(active.sum()),
        "active_days":len(days),
        "days_with_0000_bar":len(boundary),
        "first_active":str(ta.iloc[0]) if len(ta) else None,
        "last_active":str(ta.iloc[-1]) if len(ta) else None,
    }

mtf_files = {
"DISCOVERY":r"D:\nexus-xau-engine-repo\results\PATH_REMAINING_DAILY_SIDE_MTF_V2\DISCOVERY_2022_09_TO_2023_03_EVENTS.csv",
"2024":r"D:\nexus-xau-engine-repo\results\PATH_REMAINING_DAILY_SIDE_MTF_V2\LATER_2024_09_TO_2024_11_EVENTS.csv",
"2025":r"D:\nexus-xau-engine-repo\results\PATH_REMAINING_DAILY_SIDE_MTF_V2\LATER_2025_09_TO_2025_11_EVENTS.csv",
}
out["mtf"]={}
for name,f in mtf_files.items():
    d=pd.read_csv(f)
    unique=d.drop_duplicates(["candidate_known_at","side"])
    exact=d[d["variant"]=="EXACT_COMPLETION"]
    out["mtf"][name]={
        "rows_all_variants":len(d),
        "unique_candidate_side":len(unique),
        "exact_completion_rows":len(exact),
        "exact_alignment_counts":{str(k):int(v) for k,v in exact["alignment_count"].value_counts().sort_index().to_dict().items()},
        "frame_side_counts_unique":{str(k):int(v) for k,v in unique["frame_side"].value_counts().to_dict().items()},
    }

re_files = {
"DISCOVERY":r"D:\nexus-xau-engine-repo\results\SOURCE_PARTIAL_REANCHORED_REMAINING_RUN\DISCOVERY_2022_09_TO_2023_03_REANCHORED_EVENTS.csv",
"2024":r"D:\nexus-xau-engine-repo\results\SOURCE_PARTIAL_REANCHORED_REMAINING_RUN\LATER_2024_09_TO_2024_11_REANCHORED_EVENTS.csv",
"2025":r"D:\nexus-xau-engine-repo\results\SOURCE_PARTIAL_REANCHORED_REMAINING_RUN\LATER_2025_09_TO_2025_11_REANCHORED_EVENTS.csv",
}
out["reanchored"]={}
for name,f in re_files.items():
    d=pd.read_csv(f)
    surv=d[d["state"]=="INHERITED_REMAINING_RUN"]
    out["reanchored"][name]={
        "candidates":len(d),
        "surviving_inherited":len(surv),
        "survival_fraction":float(len(surv)/len(d)) if len(d) else None,
        "surviving_by_side":{str(k):int(v) for k,v in surv["side"].value_counts().to_dict().items()},
    }
print(json.dumps(out,indent=2,ensure_ascii=False))
