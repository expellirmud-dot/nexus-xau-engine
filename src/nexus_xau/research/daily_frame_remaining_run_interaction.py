from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from nexus_xau.data.csv_loader import load_ohlc_csv
from nexus_xau.data.resample import resample_ohlc
from nexus_xau.engine.mae_pla_frame import build_mae_pla_frame_candidates

PROJECT_POINT_SIZE = 0.01
SOURCE_PROXIMITY_POINTS = 200.0
MIN_GROUP = 10


def _outcome_summary(group: pd.DataFrame) -> dict[str, float | int | None]:
    resolved = group[group["path_remaining_first_hit"].isin(["TARGET_FIRST", "STOP_FIRST"])]
    return {
        "events": len(group),
        "resolved_events": len(resolved),
        "target_first_rate_resolved": (
            float((resolved["path_remaining_first_hit"] == "TARGET_FIRST").mean())
            if not resolved.empty
            else None
        ),
        "target_reach_rate": (
            float(group["path_remaining_reached"].mean()) if not group.empty else None
        ),
        "fresh_mfe_median": (
            float(group["fresh_mfe_points"].median()) if not group.empty else None
        ),
        "fresh_mae_median": (
            float(group["fresh_mae_points"].median()) if not group.empty else None
        ),
    }


def _period_state(expected: dict[str, object], outside: dict[str, object]) -> str:
    if int(expected["events"]) < MIN_GROUP or int(outside["events"]) < MIN_GROUP:
        return "INSUFFICIENT"
    etf = expected["target_first_rate_resolved"]
    otf = outside["target_first_rate_resolved"]
    er = expected["target_reach_rate"]
    or_ = outside["target_reach_rate"]
    if not all(isinstance(value, float) for value in (etf, otf, er, or_)):
        return "INSUFFICIENT"
    if etf > otf and er >= or_:
        return "SUPPORT"
    if etf < otf and er <= or_:
        return "OPPOSE"
    return "MIXED"


def run(
    *,
    m1_path: str | Path,
    remaining_events_path: str | Path,
    report_path: str | Path,
    events_path: str | Path,
) -> dict[str, object]:
    m1 = load_ohlc_csv(m1_path)
    active = m1[m1["volume"] > 0].copy()
    h1 = resample_ohlc(active, "H1")

    remaining = pd.read_csv(remaining_events_path)
    remaining = remaining[remaining["state"] == "INHERITED_REMAINING_RUN"].copy()
    remaining["cutoff_utc"] = pd.to_datetime(remaining["cutoff_utc"], utc=True)
    remaining["candidate_known_at"] = pd.to_datetime(remaining["candidate_known_at"], utc=True)
    remaining = remaining[remaining["path_remaining_reached"].notna()].copy()

    rows: list[dict[str, object]] = []
    skipped_missing_frame_open = 0
    skipped_missing_pattern = 0

    for row in remaining.itertuples(index=False):
        cutoff = pd.Timestamp(row.cutoff_utc)
        known_at = pd.Timestamp(row.candidate_known_at)
        if cutoff not in m1.index:
            skipped_missing_frame_open += 1
            continue

        pattern_start = known_at - pd.Timedelta(hours=2)
        pattern_end = known_at - pd.Timedelta(hours=1)
        required = [pattern_start, pattern_end]
        if any(ts not in h1.index for ts in required):
            skipped_missing_pattern += 1
            continue
        pattern = h1.loc[required]

        daily = build_mae_pla_frame_candidates(float(m1.loc[cutoff, "open"]))
        side = str(row.side).upper()
        if side == "BUY":
            location_price = float(pattern["low"].min())
            lines = [candidate.lower_price for candidate in daily.candidates]
            line = min(lines, key=lambda price: abs(location_price - price))
            signed = (location_price - line) / PROJECT_POINT_SIZE
        elif side == "SELL":
            location_price = float(pattern["high"].max())
            lines = [candidate.upper_price for candidate in daily.candidates]
            line = min(lines, key=lambda price: abs(location_price - price))
            signed = (line - location_price) / PROJECT_POINT_SIZE
        else:
            continue

        absolute = abs(signed)
        if absolute <= SOURCE_PROXIMITY_POINTS and signed >= 0:
            location_group = "EXPECTED_SIDE_WITHIN_200"
        elif absolute <= SOURCE_PROXIMITY_POINTS:
            location_group = "CROSSED_SIDE_WITHIN_200"
        else:
            location_group = "OUTSIDE_200_CONTROL"

        rows.append(
            {
                "cutoff_utc": cutoff.isoformat(),
                "candidate_known_at": known_at.isoformat(),
                "side": side,
                "candidate_close": float(row.candidate_close),
                "frame_open_price": float(m1.loc[cutoff, "open"]),
                "pattern_location_price": location_price,
                "daily_frame_directional_line": line,
                "signed_valid_side_distance_points": signed,
                "absolute_distance_points": absolute,
                "location_group": location_group,
                "remaining_at_entry_points": float(row.remaining_at_entry_points),
                "path_remaining_reached": bool(row.path_remaining_reached),
                "path_remaining_first_hit": str(row.path_remaining_first_hit),
                "fresh_mfe_points": float(row.fresh_mfe_points),
                "fresh_mae_points": float(row.fresh_mae_points),
            }
        )

    events = pd.DataFrame(rows)
    Path(events_path).parent.mkdir(parents=True, exist_ok=True)
    events.to_csv(events_path, index=False)

    expected = events[events["location_group"] == "EXPECTED_SIDE_WITHIN_200"]
    crossed = events[events["location_group"] == "CROSSED_SIDE_WITHIN_200"]
    outside = events[events["location_group"] == "OUTSIDE_200_CONTROL"]
    expected_summary = _outcome_summary(expected)
    crossed_summary = _outcome_summary(crossed)
    outside_summary = _outcome_summary(outside)
    state = _period_state(expected_summary, outside_summary)

    report: dict[str, object] = {
        "research_status": "DAILY_FRAME_LOCATION_X_PATH_REMAINING_COMPONENT_TEST",
        "source_m1": str(m1_path),
        "source_remaining_events": str(remaining_events_path),
        "source_proximity_points": SOURCE_PROXIMITY_POINTS,
        "project_point_size": PROJECT_POINT_SIZE,
        "representation": (
            "BUY uses two-candle H1 PAT2-window Low relative to Daily Frame lower/support; "
            "SELL uses High relative to upper/resistance. Positive signed distance means expected/inside side."
        ),
        "measured_inherited_events": len(events),
        "skipped_missing_frame_open": skipped_missing_frame_open,
        "skipped_missing_pattern": skipped_missing_pattern,
        "groups": {
            "EXPECTED_SIDE_WITHIN_200": expected_summary,
            "CROSSED_SIDE_WITHIN_200": crossed_summary,
            "OUTSIDE_200_CONTROL": outside_summary,
        },
        "period_state": state,
        "closure_rule": (
            "SUPPORT if expected-side-within-200 has higher PATH_REMAINING target-first and no-lower reach "
            f"than outside-200 control, with >= {MIN_GROUP} events per compared group; reverse both => OPPOSE."
        ),
        "limitations": [
            "<=200 is source-backed in a demonstrated frame-entry setup but is not established as universal PAT location tolerance.",
            "CROSSED_SIDE_WITHIN_200 is descriptive and not called invalid.",
            "PAT2 BODY and PATH_REMAINING remain research representations.",
            "Daily Frame 0/5 snap tie behavior is unresolved; nearest directional candidate is used without inventing a tie preference.",
            "This is not a strategy win-rate test.",
        ],
    }
    Path(report_path).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--m1", required=True)
    parser.add_argument("--remaining-events", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--events", required=True)
    args = parser.parse_args()
    report = run(
        m1_path=args.m1,
        remaining_events_path=args.remaining_events,
        report_path=args.report,
        events_path=args.events,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
