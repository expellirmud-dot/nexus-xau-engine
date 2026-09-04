from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from nexus_xau.data.csv_loader import load_ohlc_csv
from nexus_xau.data.resample import resample_ohlc
from nexus_xau.research.mtf_alignment_variant_relation_test import (
    H1_TARGET_POINTS,
    PROJECT_POINT_SIZE,
    TF_DELTA,
    _group_summary,
    _pat2_body_events,
    _safe_spearman,
)
from nexus_xau.research.outcomes import OutcomeSpec, measure_outcome
from nexus_xau.research.sw_proxy_variant_relation_test import _sw_shape_features

WINDOW_H1 = 6
FROZEN_LOW = 0.3133975223863906
FROZEN_HIGH = 0.7837295932951441
MIN_EVENTS = 100
MIN_BUCKET = 20


def run(*, m1_path: str | Path, report_path: str | Path, events_path: str | Path) -> dict[str, object]:
    m1 = load_ohlc_csv(m1_path)
    active = m1[m1["volume"] > 0].copy()
    h1 = resample_ohlc(active, "H1")
    anchors = _pat2_body_events(h1, "H1")
    rows: list[dict[str, object]] = []

    for anchor in anchors:
        future_h1 = h1.loc[h1.index >= anchor.known_at]
        if len(future_h1) < 24:
            continue
        horizon_end = future_h1.index[23] + TF_DELTA["H1"] - pd.Timedelta(minutes=1)
        first_pat_bar_start = anchor.known_at - pd.Timedelta(hours=2)
        pre = h1[h1.index < first_pat_bar_start]
        if len(pre) < WINDOW_H1:
            continue
        history = pre.iloc[-WINDOW_H1:]
        feature = _sw_shape_features(history)["oscillation_strength"]
        if feature is None:
            continue
        outcome = measure_outcome(
            active,
            OutcomeSpec(
                side=anchor.side,
                reference_price=anchor.close,
                known_at=anchor.known_at,
                horizon_end=horizon_end,
                point_size=PROJECT_POINT_SIZE,
                target_points=H1_TARGET_POINTS,
                stop_points=H1_TARGET_POINTS,
            ),
        )
        rows.append(
            {
                "anchor_known_at": anchor.known_at.isoformat(),
                "anchor_side": anchor.side,
                "oscillation_strength": feature,
                "target_reached_anywhere": outcome.mfe_points >= H1_TARGET_POINTS,
                "first_hit": outcome.first_hit.value,
                "mfe_points": outcome.mfe_points,
                "mae_points": outcome.mae_points,
            }
        )

    events = pd.DataFrame(rows)
    Path(events_path).parent.mkdir(parents=True, exist_ok=True)
    events.to_csv(events_path, index=False)
    low = events[events["oscillation_strength"] <= FROZEN_LOW]
    high = events[events["oscillation_strength"] >= FROZEN_HIGH]
    resolved = events[events["first_hit"].isin(["TARGET_FIRST", "STOP_FIRST"])].copy()
    resolved["target_first_binary"] = (resolved["first_hit"] == "TARGET_FIRST").astype(int)
    relation = {
        "events": len(events),
        "low_events": len(low),
        "high_events": len(high),
        "spearman_target_first": _safe_spearman(resolved, "oscillation_strength", "target_first_binary"),
        "spearman_target_reach": _safe_spearman(events, "oscillation_strength", "target_reached_anywhere"),
        "spearman_mfe": _safe_spearman(events, "oscillation_strength", "mfe_points"),
        "spearman_mae": _safe_spearman(events, "oscillation_strength", "mae_points"),
        "low": _group_summary(low),
        "high": _group_summary(high),
    }
    vals = [relation["spearman_target_first"], relation["spearman_target_reach"], relation["spearman_mfe"], relation["spearman_mae"]]
    enough = len(events) >= MIN_EVENTS and len(low) >= MIN_BUCKET and len(high) >= MIN_BUCKET
    positive = enough and all(isinstance(v, float) for v in vals) and vals[0] > 0 and vals[1] >= 0 and vals[2] >= 0 and vals[3] <= 0
    low_s = relation["low"]
    high_s = relation["high"]
    better = (
        isinstance(low_s["target_first_rate_resolved"], float)
        and isinstance(high_s["target_first_rate_resolved"], float)
        and isinstance(low_s["target_reach_rate_anywhere"], float)
        and isinstance(high_s["target_reach_rate_anywhere"], float)
        and high_s["target_first_rate_resolved"] > low_s["target_first_rate_resolved"]
        and high_s["target_reach_rate_anywhere"] >= low_s["target_reach_rate_anywhere"]
    )
    decision = "SUPPORTED_FRESH" if positive and better else ("INSUFFICIENT" if not enough else "NOT_CONFIRMED")
    report = {
        "research_status": "FROZEN_W6_SW_PROXY_FRESH_CONFIRMATION",
        "source_m1": str(m1_path),
        "frozen_from_prior_round": {"window_h1": WINDOW_H1, "low": FROZEN_LOW, "high": FROZEN_HIGH},
        "decision": decision,
        "relation": relation,
        "limitations": [
            "This confirms only the W6 oscillation proxy, not canonical Sideway geometry.",
            "H1 PAT2 BODY remains a research anchor proxy.",
            "Symmetric 1,000-point adverse barrier is a research control, not a canonical SL.",
        ],
    }
    Path(report_path).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--m1", required=True)
    p.add_argument("--report", required=True)
    p.add_argument("--events", required=True)
    a = p.parse_args()
    report = run(m1_path=a.m1, report_path=a.report, events_path=a.events)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
