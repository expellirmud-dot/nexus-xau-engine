from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from nexus_xau.data.csv_loader import load_ohlc_csv
from nexus_xau.data.resample import resample_ohlc
from nexus_xau.research.outcomes import FirstHit, OutcomeSpec, measure_outcome

PROJECT_REFERENCE_POINT_SIZE = 0.01
RUN_TARGET_PROJECT_POINTS = {"H1": 1000.0, "H4": 1500.0, "D1": 5000.0}
RESEARCH_HORIZON_BARS = {"H1": 24, "H4": 12, "D1": 5}


def _frame_for(m1: pd.DataFrame, timeframe: str) -> pd.DataFrame:
    if timeframe == "M1":
        return m1
    return resample_ohlc(m1, timeframe)


def _quantile(values: pd.Series, q: float) -> float | None:
    if values.empty:
        return None
    return float(values.quantile(q))


def run_baseline(
    *,
    m1_path: str | Path,
    hits_path: str | Path,
    report_path: str | Path,
    events_path: str | Path,
) -> dict[str, object]:
    """Measure topology-only post-SIG-candidate outcomes as a negative control.

    This is intentionally NOT a system win-rate backtest. It uses unqualified
    PAT2/PAT3 color-topology windows, an unvalidated post-SIG anchor candidate,
    and explicit research horizons. Its purpose is to validate the outcome
    machinery and establish a baseline before valid PA/SIG labels exist.

    A symmetric first-hit control uses the source-backed run distance as both
    the favorable and adverse barrier. This is not an SL rule; it is a neutral
    directional baseline that asks which equal-distance barrier was reached
    first after the candidate anchor became knowable.
    """

    m1 = load_ohlc_csv(m1_path)
    hits = pd.read_csv(hits_path)
    hits["window_end_utc"] = pd.to_datetime(hits["window_end_utc"], utc=True)
    hits = hits[hits["timeframe"].isin(RUN_TARGET_PROJECT_POINTS)].copy()

    frames = {tf: _frame_for(m1, tf) for tf in RUN_TARGET_PROJECT_POINTS}
    records: list[dict[str, object]] = []
    skipped = 0

    for hit in hits.itertuples(index=False):
        timeframe = str(hit.timeframe)
        side = str(hit.side).upper()
        frame = frames[timeframe]
        end_ts = pd.Timestamp(hit.window_end_utc)
        if end_ts not in frame.index:
            skipped += 1
            continue

        location = frame.index.get_loc(end_ts)
        if not isinstance(location, int):
            skipped += 1
            continue

        post_sig_pos = location + 1
        known_at_pos = location + 2
        horizon_boundary_pos = known_at_pos + RESEARCH_HORIZON_BARS[timeframe]
        if horizon_boundary_pos >= len(frame):
            skipped += 1
            continue

        post_sig_bar = frame.iloc[post_sig_pos]
        anchor_price = float(post_sig_bar["low"] if side == "BUY" else post_sig_bar["high"])
        known_at = frame.index[known_at_pos]
        horizon_end = frame.index[horizon_boundary_pos] - pd.Timedelta("1min")
        target_project_points = RUN_TARGET_PROJECT_POINTS[timeframe]

        outcome = measure_outcome(
            m1,
            OutcomeSpec(
                side=side,
                reference_price=anchor_price,
                known_at=known_at,
                horizon_end=horizon_end,
                point_size=PROJECT_REFERENCE_POINT_SIZE,
                target_points=target_project_points,
                stop_points=target_project_points,
            ),
        )
        records.append(
            {
                "timeframe": timeframe,
                "kind": str(hit.kind),
                "side": side,
                "pattern_window_end_utc": end_ts.isoformat(),
                "post_sig_candidate_timestamp": frame.index[post_sig_pos].isoformat(),
                "anchor_candidate_price": anchor_price,
                "known_at_utc": known_at.isoformat(),
                "horizon_end_utc": horizon_end.isoformat(),
                "research_horizon_bars": RESEARCH_HORIZON_BARS[timeframe],
                "target_project_points": target_project_points,
                "target_price_distance": target_project_points * PROJECT_REFERENCE_POINT_SIZE,
                "symmetric_adverse_barrier_project_points": target_project_points,
                "mfe_project_points": outcome.mfe_points,
                "mae_project_points": outcome.mae_points,
                "end_return_project_points": outcome.end_return_points,
                "target_reached_anywhere": outcome.mfe_points >= target_project_points,
                "symmetric_target_first_hit_at_utc": (
                    outcome.target_hit_at.isoformat() if outcome.target_hit_at is not None else None
                ),
                "symmetric_first_hit": outcome.first_hit.value,
            }
        )

    events = pd.DataFrame(records)
    target = Path(events_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    events.to_csv(target, index=False)

    groups: list[dict[str, object]] = []
    if not events.empty:
        for (timeframe, kind, side), group in events.groupby(["timeframe", "kind", "side"]):
            first_hits = group["symmetric_first_hit"].value_counts()
            target_first = int(first_hits.get(FirstHit.TARGET_FIRST.value, 0))
            stop_first = int(first_hits.get(FirstHit.STOP_FIRST.value, 0))
            ambiguous = int(first_hits.get(FirstHit.AMBIGUOUS_SAME_BAR.value, 0))
            neither = int(first_hits.get(FirstHit.NEITHER.value, 0))
            resolved = target_first + stop_first
            groups.append(
                {
                    "timeframe": timeframe,
                    "kind": kind,
                    "side": side,
                    "events": len(group),
                    "target_reached_anywhere": int(group["target_reached_anywhere"].sum()),
                    "target_reach_rate_anywhere": float(group["target_reached_anywhere"].mean()),
                    "symmetric_target_first": target_first,
                    "symmetric_adverse_first": stop_first,
                    "symmetric_ambiguous_same_m1_bar": ambiguous,
                    "symmetric_neither": neither,
                    "symmetric_resolved_events": resolved,
                    "symmetric_target_first_rate_resolved": (
                        target_first / resolved if resolved else None
                    ),
                    "mfe_p25": _quantile(group["mfe_project_points"], 0.25),
                    "mfe_median": _quantile(group["mfe_project_points"], 0.50),
                    "mfe_p75": _quantile(group["mfe_project_points"], 0.75),
                    "mae_p25": _quantile(group["mae_project_points"], 0.25),
                    "mae_median": _quantile(group["mae_project_points"], 0.50),
                    "mae_p75": _quantile(group["mae_project_points"], 0.75),
                }
            )

    payload: dict[str, object] = {
        "research_status": "NEGATIVE_CONTROL_TOPOLOGY_ONLY_NOT_SYSTEM_WIN_RATE",
        "source_m1": str(m1_path),
        "source_hits": str(hits_path),
        "project_reference_point_size": PROJECT_REFERENCE_POINT_SIZE,
        "broker_point_warning": (
            "Current XAUUSDm MT5 symbol point observed separately as 0.001. "
            "This report intentionally uses the project reference unit 0.01 so broker digits do not "
            "silently redefine teaching run distances."
        ),
        "anchor_policy": (
            "Candidate post-SIG candle is the first timeframe candle after the topology window; "
            "BUY anchor candidate=its low, SELL anchor candidate=its high. Anchor validity is NOT checked."
        ),
        "lookahead_policy": (
            "Forward measurement begins only after the candidate post-SIG candle has closed; "
            "movement inside that candle is excluded from outcome scoring."
        ),
        "symmetric_first_hit_policy": (
            "Favorable barrier and adverse barrier use the same distance, equal to the timeframe run target. "
            "This is a neutral direction test, not a canonical SL or strategy win/loss definition."
        ),
        "research_horizon_bars": RESEARCH_HORIZON_BARS,
        "run_target_project_points": RUN_TARGET_PROJECT_POINTS,
        "input_hits_after_timeframe_filter": len(hits),
        "measured_events": len(events),
        "skipped_insufficient_future_or_alignment": skipped,
        "overlap_policy": "retained; event rows are not statistically independent",
        "groups": groups,
        "blocked_interpretations": [
            "Do not call target_reach_rate_anywhere a strategy win rate.",
            "Do not call symmetric_target_first_rate_resolved a strategy win rate.",
            "Do not infer the canonical loss rate because system SL/invalidation is not applied.",
            "Do not optimize PAT thresholds or location rules from this negative-control outcome.",
        ],
    }
    report = Path(report_path)
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--m1", required=True)
    parser.add_argument("--hits", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--events", required=True)
    args = parser.parse_args()
    result = run_baseline(
        m1_path=args.m1,
        hits_path=args.hits,
        report_path=args.report,
        events_path=args.events,
    )
    print(result["research_status"])
    print(f"Measured events: {result['measured_events']}")
    for row in result["groups"]:
        rate = row["symmetric_target_first_rate_resolved"]
        rate_text = "n/a" if rate is None else f"{rate:.3f}"
        print(
            f"{row['timeframe']} {row['kind']} {row['side']}: "
            f"n={row['events']} reach_any={row['target_reach_rate_anywhere']:.3f} "
            f"sym_target_first={rate_text} "
            f"amb={row['symmetric_ambiguous_same_m1_bar']} "
            f"MFE50={row['mfe_median']:.1f} MAE50={row['mae_median']:.1f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
