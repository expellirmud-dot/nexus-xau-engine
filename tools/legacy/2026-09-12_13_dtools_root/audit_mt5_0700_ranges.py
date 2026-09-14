import pandas as pd
from pathlib import Path

files = [
    Path(r"D:\nexus-xau-engine-repo\data\raw\XAUUSDm_M1_MT5_2026-05-26_2026-09-01.csv"),
    Path(r"D:\nexus-xau-engine-repo\data\raw\XAUUSDm_M1_MT5_2026-08-03_2026-09-01.csv"),
    Path(r"D:\nexus-xau-engine-repo\data\raw\XAUUSDm_M1_MT5_2026-08-24_2026-08-28.csv"),
]

for p in files:
    df = pd.read_csv(p, usecols=["timestamp"])
    ts = pd.to_datetime(df["timestamp"], utc=True)
    midnight = ((ts.dt.hour == 0) & (ts.dt.minute == 0)).sum()
    print(
        p.name,
        "rows=", len(df),
        "first=", ts.iloc[0],
        "last=", ts.iloc[-1],
        "00UTC=", int(midnight),
        "unique_dates=", ts.dt.date.nunique(),
    )
