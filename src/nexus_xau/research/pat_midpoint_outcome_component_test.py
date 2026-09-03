from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from nexus_xau.data.csv_loader import load_ohlc_csv
from nexus_xau.data.resample import resample_ohlc

SUPPORTED_TFS = ("H1", "H4")
BASES = ("BODY", "FULL_RANGE")
MIN_GROUP_SIZE = 20


def _split(ts: pd.Timestamp) -> str:
    if ts < pd.Timestamp("2026-07-01", tz="UTC"):
        return "DEV"
    if ts < pd.Timestamp("2026-08-01", tz="UTC"):
        return "VAL"
    return "TEST"


def _midpoint(row: pd.Series, basis: str) -> float:
    if basis == "BODY":
        return (float(row.open) + float(row.close)) / 2.0
    if basis == "FULL_RANGE":
        return (float(row.high) + float(row.low)) / 2.0
    raise ValueError(f"unsupported midpoint basis: {basis}")


def _passes(close: float, row: pd.Series, side: str, basis: str) -> bool:
    midpoint = _midpoint(row, basis)
    return close > midpoint if side == "BUY" else close < midpoint


def _rate(group: pd.DataFrame, col: str) -> float | None:
    if group.empty:
        return None
    return float(group[col].mean())


def _target_first_rate(group: pd.DataFrame) -> float | None:
    resolved = group[group["symmetric_first_hit"].isin(["TARGET_FIRST", "STOP_FIRST"])]
    if resolved.empty:
        return None
    return float((resolved["symmetric_first_hit"] == "TARGET_FIRST").mean())


def _median(group: pd.DataFrame, col: str) -> float | None:
    if group.empty:
        return None
    return float(group[col].median())


def _summary(group: pd.DataFrame) -> dict[str, float | int | None]:
    return {
        "events": len(group),
        "target_first_rate_resolved": _target_first_rate(group),
        "target_reach_rate_anywhere": _rate(group, "target_reached_anywhere"),
        "mfe_median": _median(group, "mfe_project_points"),
        "mae_median": _median(group, "mae_project_points"),
    }


def _better(passed: dict[str, float | int | None], failed: dict[str, float | int | None]) -> bool:
    p_tf = passed["target_first_rate_resolved"]
    f_tf = failed["target_first_rate_resolved"]
    p_reach = passed["target_reach_rate_anywhere"]
    f_reach = failed["target_reach_rate_anywhere"]
    if not all(isinstance(v, float) for v in (p_tf, f_tf, p_reach, f_reach)):
        return False
    return bool(p_tf > f_tf and p_reach >= f_reach)


def run_test(
    *,
    m1_path: str | Path,
    hits_path: str | Path,
    outcomes_path: str | Path,
    report_path: str | Path,
    events_path: str | Path,
) -> dict[str, object]:
    m1 = load_ohlc_csv(m1_path)
    hits = pd.read_csv(hits_path)
    hits = hits[hits["timeframe"].isin(SUPPORTED_TFS)].copy()
    hits["window_start_utc"] = pd.to_datetime(hits["window_start_utc"], utc=True)
    hits["window_end_utc"] = pd.to_datetime(hits["window_end_utc"], utc=True)

    outcomes = pd.read_csv(outcomes_path)
    outcomes = outcomes[outcomes["timeframe"].isin(SUPPORTED_TFS)].copy()
    outcomes["pattern_window_end_utc"] = pd.to_datetime(outcomes["pattern_window_end_utc"], utc=True)

    frames = {tf: resample_ohlc(m1, tf) for tf in SUPPORTED_TFS}
    rows: list[dict[str, object]] = []

    for hit in hits.itertuples(index=False):
        tf = str(hit.timeframe)
        kind = str(hit.kind)
        side = str(hit.side).upper()
        start = pd.Timestamp(hit.window_start_utc)
        end = pd.Timestamp(hit.window_end_utc)
        frame = frames[tf]
        pattern = frame.loc[(frame.index >= start) & (frame.index <= end)]
        required = 2 if kind == "PAT2" else 3 if kind == "PAT3" else None
        if required is None or len(pattern) != required:
            continue

        if kind == "PAT2":
            c1 = pattern.iloc[0]
            close = float(pattern.iloc[1].close)
            basis_pass = {basis: _passes(close, c1, side, basis) for basis in BASES}
        else:
            c1 = pattern.iloc[0]
            c2 = pattern.iloc[1]
            close = float(pattern.iloc[2].close)
            basis_pass = {
                basis: _passes(close, c1, side, basis) and _passes(close, c2, side, basis)
                for basis in BASES
            }

        match = outcomes[
            (outcomes["timeframe"] == tf)
            & (outcomes["kind"] == kind)
            & (outcomes["side"] == side)
            & (outcomes["pattern_window_end_utc"] == end)
        ]
        if len(match) != 1:
            continue
        out = match.iloc[0]

        row: dict[str, object] = {
            "split": _split(end),
            "timeframe": tf,
            "kind": kind,
            "side": side,
            "pattern_window_start_utc": start.isoformat(),
            "pattern_window_end_utc": end.isoformat(),
            "target_reached_anywhere": bool(out["target_reached_anywhere"]),
            "symmetric_first_hit": str(out["symmetric_first_hit"]),
            "mfe_project_points": float(out["mfe_project_points"]),
            "mae_project_points": float(out["mae_project_points"]),
        }
        for basis in BASES:
            row[f"midpoint_pass_{basis.lower()}"] = basis_pass[basis]
        rows.append(row)

    events = pd.DataFrame(rows)
    Path(events_path).parent.mkdir(parents=True, exist_ok=True)
    events.to_csv(events_path, index=False)

    summaries: list[dict[str, object]] = []
    decisions: dict[str, str] = {}

    for tf in SUPPORTED_TFS:
        for kind in ("PAT2", "PAT3"):
            for basis in BASES:
                key = f"{tf}_{kind}_{basis}"
                checks: list[bool | None] = []
                col = f"midpoint_pass_{basis.lower()}"
                for split_name in ("DEV", "VAL", "TEST"):
                    g = events[
                        (events["timeframe"] == tf)
                        & (events["kind"] == kind)
                        & (events["split"] == split_name)
                    ]
                    passed = g[g[col]]
                    failed = g[~g[col]]
                    passed_summary = _summary(passed)
                    failed_summary = _summary(failed)
                    summaries.append(
                        {
                            "timeframe": tf,
                            "kind": kind,
                            "basis": basis,
                            "split": split_name,
                            "all_events": len(g),
                            "geometry_pass": passed_summary,
                            "geometry_fail": failed_summary,
                        }
                    )
                    if split_name in {"VAL", "TEST"}:
                        if len(passed) < MIN_GROUP_SIZE or len(failed) < MIN_GROUP_SIZE:
                            checks.append(None)
                        else:
                            checks.append(_better(passed_summary, failed_summary))

                if len(checks) != 2 or any(value is None for value in checks):
                    decisions[key] = "INCONCLUSIVE: at least one held-out pass/fail group is too small."
                elif all(checks):
                    decisions[key] = (
                        "SUPPORTED: >50% midpoint-qualified candidates outperform midpoint-fail controls "
                        "on both held-out splits by the frozen two-metric rule."
                    )
                elif not any(checks):
                    decisions[key] = (
                        "NOT_SUPPORTED: >50% midpoint qualification does not improve both frozen metrics "
                        "on either held-out split."
                    )
                else:
                    decisions[key] = "INCONCLUSIVE: held-out splits disagree."

    supported = [key for key, value in decisions.items() if value.startswith("SUPPORTED")]
    not_supported = [key for key, value in decisions.items() if value.startswith("NOT_SUPPORTED")]
    inconclusive = [key for key, value in decisions.items() if value.startswith("INCONCLUSIVE")]

    report: dict[str, object] = {
        "research_question": (
            "Does adding the source-backed >50% midpoint relation to H1/H4 PAT2/PAT3 color topology "
            "improve forward outcome behavior?"
        ),
        "research_status": "Q4A_PAT_MIDPOINT_COMPONENT_TEST_NOT_CANONICAL_SIG_RULE",
        "source_m1": str(m1_path),
        "source_hits": str(hits_path),
        "source_outcomes": str(outcomes_path),
        "variants": {
            "BODY": "midpoint of candle open/close",
            "FULL_RANGE": "midpoint of candle high/low",
        },
        "pat2_rule": "candle #2 close must pass candle #1 midpoint in PAT direction",
        "pat3_partial_rule": (
            "candle #3 close must pass both candle #1 and candle #2 midpoints; small-body/equal-wick "
            "requirements intentionally remain excluded because thresholds are unresolved"
        ),
        "minimum_group_size": MIN_GROUP_SIZE,
        "decision_rule": (
            "SUPPORTED per TF/kind/basis only when geometry-pass has higher resolved target-first rate "
            "and no-lower target-reach rate than geometry-fail on BOTH VAL and TEST."
        ),
        "limitations": [
            "This is a component test, not a valid SIG count or strategy win rate.",
            "Outcome performance cannot decide which midpoint basis is the true teaching definition.",
            "PAT3 small-body and SELL equal-wick thresholds remain unresolved and are not applied.",
            "Daily-Frame Location, SW and inherited remaining-run are not included in this Q4a test.",
            "The symmetric adverse barrier in the source outcome table is a research control, not a canonical SL.",
        ],
        "measured_events": len(events),
        "summaries": summaries,
        "decisions": decisions,
        "supported_variants": supported,
        "not_supported_variants": not_supported,
        "inconclusive_variants": inconclusive,
    }
    Path(report_path).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--m1", required=True)
    parser.add_argument("--hits", required=True)
    parser.add_argument("--outcomes", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--events", required=True)
    args = parser.parse_args()
    result = run_test(
        m1_path=args.m1,
        hits_path=args.hits,
        outcomes_path=args.outcomes,
        report_path=args.report,
        events_path=args.events,
    )
    print(json.dumps(result["decisions"], ensure_ascii=False, indent=2))
    print("SUPPORTED", result["supported_variants"])
    print("NOT_SUPPORTED", result["not_supported_variants"])
    print("INCONCLUSIVE", result["inconclusive_variants"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
