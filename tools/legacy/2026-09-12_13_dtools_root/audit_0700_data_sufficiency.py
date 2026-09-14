from __future__ import annotations
import json
from pathlib import Path
import pandas as pd

root = Path(r"D:\nexus-xau-engine-repo")

meta_paths = [
    root / r"data\raw\dukascopy\chunks\XAUUSD_M1_BID_2022-09-01_2023-03-31.csv.meta.json",
    root / r"data\raw\dukascopy\chunks\XAUUSD_M1_BID_2022-09-01_2023-08-31.csv.meta.json",
    root / r"data\raw\dukascopy\chunks\XAUUSD_M1_BID_2023-09-01_2023-11-23.csv.meta.json",
    root / r"data\raw\dukascopy\chunks\XAUUSD_M1_BID_2023-09-01_2023-11-30.csv.meta.json",
    root / r"data\raw\dukascopy\chunks\XAUUSD_M1_BID_2024-09-01_2024-11-30.csv.meta.json",
    root / r"data\raw\dukascopy\chunks\XAUUSD_M1_BID_2025-09-01_2025-11-30.csv.meta.json",
    root / r"data\raw\XAUUSDm_M1_MT5_2026-08-01_2026-09-02.csv.meta.json",
]
datasets = []
for p in meta_paths:
    d = json.loads(p.read_text(encoding="utf-8"))
    datasets.append({
        "file": p.name.removesuffix(".meta.json"),
        "source": d.get("source"),
        "start": d.get("start_date") or d.get("start_utc"),
        "end": d.get("end_date") or d.get("end_utc"),
        "rows": d.get("rows"),
        "complete": d.get("complete_cache_range"),
        "missing_count": len(d.get("missing_cache_dates", [])),
        "failed_count": int(d.get("days_failed", 0) or 0),
        "warning": d.get("warning") or d.get("research_warning"),
    })

result_files = {
    "v1_discovery_days": root / r"results\0700_STATE_DATASET_V1\DISCOVERY_2022_09_TO_2023_03\0700_day_state.csv",
    "v1_replication_days": root / r"results\0700_STATE_DATASET_V1\REPLICATION_2023_09_TO_2023_11_23\0700_day_state.csv",
    "q1_discovery": root / r"results\0700_Q1_ORIGIN_CONTEXT\DISCOVERY_2022_09_TO_2023_03\Q1_ORIGIN_CONTEXT_EVENTS.csv",
    "q1_replication": root / r"results\0700_Q1_ORIGIN_CONTEXT\REPLICATION_2023_09_TO_2023_11_23\Q1_ORIGIN_CONTEXT_EVENTS.csv",
    "q4_discovery": root / r"results\0700_Q4_H4_CONSUMED_SHAPE\DISCOVERY_2022_09_TO_2023_03\Q4_FEATURE_ROWS.csv",
    "q4_replication": root / r"results\0700_Q4_H4_CONSUMED_SHAPE\REPLICATION_2023_09_TO_2023_11_23\Q4_FEATURE_ROWS.csv",
}
counts = {}
for k, p in result_files.items():
    if p.exists():
        df = pd.read_csv(p)
        counts[k] = {
            "rows": len(df),
            "contexts": int(df["context_id"].nunique()) if "context_id" in df.columns else None,
            "days": int(df["day_id"].nunique()) if "day_id" in df.columns else len(df) if "day_state" in k else None,
        }

# resolved H4 rows in Q4, plus target/point counts if available
for k in ("q4_discovery", "q4_replication"):
    p = result_files[k]
    if p.exists():
        df = pd.read_csv(p)
        h4 = df[df["origin_tf"].eq("H4")] if "origin_tf" in df.columns else df.iloc[0:0]
        counts[k]["h4_rows"] = len(h4)
        if "path_remaining_first_hit" in h4.columns:
            counts[k]["h4_outcomes"] = h4["path_remaining_first_hit"].value_counts().to_dict()

print(json.dumps({"datasets": datasets, "result_counts": counts}, ensure_ascii=False, indent=2, default=str))
