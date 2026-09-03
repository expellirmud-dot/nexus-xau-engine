import json
from pathlib import Path

FILES = (
    "XAUUSDm_PAT_geometry_sensitivity_2026-08-24_2026-08-28.json",
    "XAUUSDm_PAT_geometry_sensitivity_2026-08-03_2026-09-01.json",
)

for name in FILES:
    data = json.loads((Path("results") / name).read_text(encoding="utf-8"))
    total = body = full = disagree = 0
    for timeframe in data["timeframes"]:
        for kind in ("PAT2", "PAT3"):
            for side in ("BUY", "SELL"):
                node = timeframe[kind][side]
                total += node["topology_candidates"]
                body += node["midpoint_pass"]["BODY"]
                full += node["midpoint_pass"]["FULL_RANGE"]
                agreement = node["basis_agreement"]
                disagree += agreement["body_only"] + agreement["full_range_only"]
    print(
        name,
        f"topology={total}",
        f"BODY={body} ({body / total * 100:.2f}%)",
        f"FULL={full} ({full / total * 100:.2f}%)",
        f"basis_disagree={disagree} ({disagree / total * 100:.2f}%)",
    )

print("--- selected PAT3 sensitivity month ---")
data = json.loads(
    Path("results/XAUUSDm_PAT_geometry_sensitivity_2026-08-03_2026-09-01.json").read_text(
        encoding="utf-8"
    )
)
for tf_name in ("M1", "M5", "H1", "H4"):
    timeframe = next(item for item in data["timeframes"] if item["timeframe"] == tf_name)
    buy_rows = timeframe["PAT3"]["BUY"]["threshold_sensitivity"]
    buy_count = next(
        row["count"]
        for row in buy_rows
        if row["basis"] == "BODY" and row["small_body_max_range_fraction"] == 0.3
    )
    sell_rows = timeframe["PAT3"]["SELL"]["threshold_sensitivity"]
    sell_counts = {
        wick: next(
            row["count"]
            for row in sell_rows
            if row["basis"] == "BODY"
            and row["small_body_max_range_fraction"] == 0.3
            and row["equal_wick_max_range_fraction"] == wick
        )
        for wick in (0.1, 0.2, 0.3)
    }
    print(
        tf_name,
        f"BUY_BODY50_small<=0.3={buy_count}",
        f"SELL_BODY50_small<=0.3_wick={sell_counts}",
    )
