import pandas as pd, json, os
files = [
r"D:\nexus-xau-engine-repo\data\raw\XAUUSDm_M1_MT5_2026-05-26_2026-09-01.csv",
r"D:\nexus-xau-engine-repo\data\processed\2026-05-26_2026-09-01\XAUUSDm_M1_MT5_2026-05-26_2026-09-01_M5.csv",
r"D:\nexus-xau-engine-repo\data\processed\2026-05-26_2026-09-01\XAUUSDm_M1_MT5_2026-05-26_2026-09-01_H1.csv",
r"D:\nexus-xau-engine-repo\data\processed\2026-05-26_2026-09-01\XAUUSDm_M1_MT5_2026-05-26_2026-09-01_H4.csv",
r"D:\nexus-xau-engine-repo\data\processed\2026-05-26_2026-09-01\XAUUSDm_M1_MT5_2026-05-26_2026-09-01_D1.csv",
r"D:\nexus-xau-engine-repo\data\raw\dukascopy\chunks\XAUUSD_M1_BID_2022-09-01_2023-03-31.csv",
r"D:\nexus-xau-engine-repo\data\raw\dukascopy\chunks\XAUUSD_M1_BID_2024-09-01_2024-11-30.csv",
r"D:\nexus-xau-engine-repo\data\raw\dukascopy\chunks\XAUUSD_M1_BID_2025-09-01_2025-11-30.csv",
r"D:\nexus-xau-engine-repo\results\REMAINING_RUN_STATE_DISCOVERY_2022-09_2023-03_EVENTS.csv",
r"D:\nexus-xau-engine-repo\results\REMAINING_RUN_STATE_2024-09_2024-11_EVENTS.csv",
r"D:\nexus-xau-engine-repo\results\REMAINING_RUN_STATE_2025-09_2025-11_EVENTS.csv",
r"D:\nexus-xau-engine-repo\results\PATH_REMAINING_DAILY_SIDE_MTF_V2\DISCOVERY_2022_09_TO_2023_03_EVENTS.csv",
r"D:\nexus-xau-engine-repo\results\PATH_REMAINING_DAILY_SIDE_MTF_V2\LATER_2024_09_TO_2024_11_EVENTS.csv",
r"D:\nexus-xau-engine-repo\results\PATH_REMAINING_DAILY_SIDE_MTF_V2\LATER_2025_09_TO_2025_11_EVENTS.csv",
r"D:\nexus-xau-engine-repo\results\INHERITED_ORIGIN_CONTEXT_RELATION\DISCOVERY_2022_09_TO_2023_03_EVENTS.csv",
]
out=[]
for f in files:
    if not os.path.exists(f):
        out.append({"file":f,"exists":False})
        continue
    df=pd.read_csv(f)
    info={"file":f,"exists":True,"rows":len(df),"columns":list(df.columns)}
    for c in df.columns:
        lc=c.lower()
        if "time" in lc or "date" in lc:
            vals=df[c].dropna()
            if len(vals):
                info["time_col"]=c
                info["first"]=str(vals.iloc[0])
                info["last"]=str(vals.iloc[-1])
                break
    info["sample"]=df.head(2).to_dict(orient="records")
    out.append(info)
print(json.dumps(out,ensure_ascii=False,indent=2,default=str))
