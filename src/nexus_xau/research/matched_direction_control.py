from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from nexus_xau.data.csv_loader import load_ohlc_csv
from nexus_xau.data.resample import resample_ohlc
from nexus_xau.research.outcomes import FirstHit, OutcomeSpec, measure_outcome
from nexus_xau.research.topology_outcome_baseline import (
    PROJECT_REFERENCE_POINT_SIZE,
    RESEARCH_HORIZON_BARS,
    RUN_TARGET_PROJECT_POINTS,
)


def _frame_for(m1: pd.DataFrame, timeframe: str) -> pd.DataFrame:
    return resample_ohlc(m1, timeframe)


def _opposite(side: str) -> str:
    return "SELL" if side == "BUY" else "BUY"


def _score(
    *,
    m1: pd.DataFrame,
    side: str,
    post_sig_bar: pd.Series,
    known_at: pd.Timestamp,
    horizon_end: pd.Timestamp,
    target_points: float,
) -> FirstHit:
    anchor = float(post_sig_bar["low"] if side == "BUY" else post_sig_bar["high"])
    outcome = measure_outcome(
        m1,
        OutcomeSpec(
            side=side,
            reference_price=anchor,
            known_at=known_at,
            horizon_end=horizon_end,
            point_size=PROJECT_REFERENCE_POINT_SIZE,
            target_points=target_points,
            stop_points=target_points,
        ),
    )
    return outcome.first_hit


def _summarize_first_hit(values: pd.Series) -> dict[str, float | int | None]:
    counts = values.value_counts()
    target = int(counts.get(FirstHit.TARGET_FIRST.value, 0))
    adverse = int(counts.get(FirstHit.STOP_FIRST.value, 0))
    ambiguous = int(counts.get(FirstHit.AMBIGUOUS_SAME_BAR.value, 0))
    neither = int(counts.get(FirstHit.NEITHER.value, 0))
    resolved = target + adverse
    return {
        "target_first": target,
        "adverse_first": adverse,
        "ambiguous": ambiguous,
        "neither": neither,
        "resolved": resolved,
        "target_first_rate_resolved": target / resolved if resolved else None,
    }


def run_control(
    *,
    m1_path: str | Path,
    hits_path: str | Path,
    report_path: str | Path,
    events_path: str | Path,
) -> dict[str, object]:
    m1 = load_ohlc_csv(m1_path)
    hits = pd.read_csv(hits_path)
    hits["window_end_utc"] = pd.to_datetime(hits["window_end_utc"], utc=True)
    hits = hits[hits["timeframe"].isin(RUN_TARGET_PROJECT_POINTS)].copy()
    frames = {tf: _frame_for(m1, tf) for tf in RUN_TARGET_PROJECT_POINTS}

    rows: list[dict[str, object]] = []
    skipped = 0
    for hit in hits.itertuples(index=False):
        timeframe = str(hit.timeframe)
        actual_side = str(hit.side).upper()
        frame = frames[timeframe]
        end_ts = pd.Timestamp(hit.window_end_utc)
        if end_ts not in frame.index:
            skipped += 1
            continue
        pos = frame.index.get_loc(end_ts)
        if not isinstance(pos, int):
            skipped += 1
            continue
        post_sig_pos = pos + 1
        known_at_pos = pos + 2
        horizon_boundary_pos = known_at_pos + RESEARCH_HORIZON_BARS[timeframe]
        if horizon_boundary_pos >= len(frame):
            skipped += 1
            continue

        post_sig_bar = frame.iloc[post_sig_pos]
        known_at = pd.Timestamp(frame.index[known_at_pos])
        horizon_end = pd.Timestamp(frame.index[horizon_boundary_pos]) - pd.Timedelta(minutes=1)
        target_points = RUN_TARGET_PROJECT_POINTS[timeframe]
        flipped_side = _opposite(actual_side)

        actual_hit = _score(
            m1=m1,
            side=actual_side,
            post_sig_bar=post_sig_bar,
            known_at=known_at,
            horizon_end=horizon_end,
            target_points=target_points,
        )
        flipped_hit = _score(
            m1=m1,
            side=flipped_side,
            post_sig_bar=post_sig_bar,
            known_at=known_at,
            horizon_end=horizon_end,
            target_points=target_points,
        )
        rows.append(
            {
                "timeframe": timeframe,
                "kind": str(hit.kind),
                "actual_side": actual_side,
                "flipped_side": flipped_side,
                "pattern_window_end_utc": end_ts.isoformat(),
                "post_sig_candidate_timestamp": frame.index[post_sig_pos].isoformat(),
                "known_at_utc": known_at.isoformat(),
                "actual_first_hit": actual_hit.value,
                "flipped_first_hit": flipped_hit.value,
            }
        )

    events = pd.DataFrame(rows)
    events_target = Path(events_path)
    events_target.parent.mkdir(parents=True, exist_ok=True)
    events.to_csv(events_target, index=False)

    groups: list[dict[str, object]] = []
    if not events.empty:
        for (timeframe, kind), group in events.groupby(["timeframe", "kind"]):
            actual = _summarize_first_hit(group["actual_first_hit"])
            flipped = _summarize_first_hit(group["flipped_first_hit"])
            actual_rate = actual["target_first_rate_resolved"]
            flipped_rate = flipped["target_first_rate_resolved"]
            delta = (
                float(actual_rate) - float(flipped_rate)
                if actual_rate is not None and flipped_rate is not None
                else None
            )
            groups.append(
                {
                    "timeframe": timeframe,
                    "kind": kind,
                    "events": len(group),
                    "actual_direction": actual,
                    "flipped_direction_same_times": flipped,
                    "actual_minus_flipped_rate": delta,
                }
            )

    payload: dict[str, object] = {
        "research_status": "MATCHED_DIRECTION_CONTROL_NOT_SYSTEM_WIN_RATE",
        "source_m1": str(m1_path),
        "source_hits": str(hits_path),
        "project_reference_point_size": PROJECT_REFERENCE_POINT_SIZE,
        "method": (
            "For each topology event, evaluate its stated direction and the opposite direction at the "
            "same timestamp using the same post-SIG candle. Each direction uses its corresponding wick "
            "extreme as the candidate anchor. Equal favorable/adverse barriers are applied."
        ),
        "purpose": (
            "Test whether an apparent directional first-hit advantage survives a matched opposite-direction "
            "control, rather than assuming high target reach proves strategy edge."
        ),
        "measured_events": len(events),
        "skipped": skipped,
        "groups": groups,
        "limitations": [
            "Topology events are not valid PA/SIG labels.",
            "Post-SIG anchor validity is not checked.",
            "Events overlap and are not statistically independent.",
            "This is not a randomized placebo test and does not establish causal edge.",
        ],
    }
    report_target = Path(report_path)
    report_target.parent.mkdir(parents=True, exist_ok=True)
    report_target.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--m1", required=True)
    parser.add_argument("--hits", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--events", required=True)
    args = parser.parse_args()
    result = run_control(
        m1_path=args.m1,
        hits_path=args.hits,
        report_path=args.report,
        events_path=args.events,
    )
    print(result["research_status"])
    print(f"Measured events: {result['measured_events']}")
    for row in result["groups"]:
        actual = row["actual_direction"]["target_first_rate_resolved"]
        flipped = row["flipped_direction_same_times"]["target_first_rate_resolved"]
        print(
            f"{row['timeframe']} {row['kind']}: n={row['events']} "
            f"actual={actual:.3f} flipped={flipped:.3f} delta={row['actual_minus_flipped_rate']:.3f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
