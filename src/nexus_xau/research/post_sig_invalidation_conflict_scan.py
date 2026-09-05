from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from nexus_xau.data.csv_loader import load_ohlc_csv
from nexus_xau.research.mtf_alignment_variant_relation_test import PROJECT_POINT_SIZE

REQUIRED_EVENT_COLUMNS = {
    "state",
    "candidate_known_at",
    "side",
    "origin_anchor_known_at",
    "origin_anchor_price",
}


def selected_origin_conflict(
    *,
    m1: pd.DataFrame,
    side: str,
    origin_anchor_known_at: pd.Timestamp,
    origin_anchor_price: float,
    candidate_known_at: pd.Timestamp,
) -> dict[str, object]:
    side = side.upper()
    if side not in {"BUY", "SELL"}:
        raise ValueError(f"unsupported side: {side}")
    if candidate_known_at <= origin_anchor_known_at:
        return {
            "evaluable": False,
            "destroyed_before_candidate": None,
            "first_destruction_at": None,
            "max_anchor_exceed_points": None,
        }

    path = m1.loc[
        (m1.index >= origin_anchor_known_at) & (m1.index < candidate_known_at)
    ]
    if path.empty:
        return {
            "evaluable": False,
            "destroyed_before_candidate": None,
            "first_destruction_at": None,
            "max_anchor_exceed_points": None,
        }

    if side == "BUY":
        mask = path["low"].astype(float) < origin_anchor_price
        extreme = float(path["low"].min())
        exceed_points = max(0.0, (origin_anchor_price - extreme) / PROJECT_POINT_SIZE)
    else:
        mask = path["high"].astype(float) > origin_anchor_price
        extreme = float(path["high"].max())
        exceed_points = max(0.0, (extreme - origin_anchor_price) / PROJECT_POINT_SIZE)

    destroyed = bool(mask.any())
    first_at = path.index[mask][0].isoformat() if destroyed else None
    return {
        "evaluable": True,
        "destroyed_before_candidate": destroyed,
        "first_destruction_at": first_at,
        "max_anchor_exceed_points": exceed_points,
    }


def scan_events(
    *,
    m1: pd.DataFrame,
    events: pd.DataFrame,
) -> pd.DataFrame:
    missing = REQUIRED_EVENT_COLUMNS.difference(events.columns)
    if missing:
        raise ValueError(f"remaining-run events missing columns: {sorted(missing)}")

    frame = events[events["state"] == "INHERITED_REMAINING_RUN"].copy()
    frame["candidate_known_at"] = pd.to_datetime(frame["candidate_known_at"], utc=True)
    frame["origin_anchor_known_at"] = pd.to_datetime(
        frame["origin_anchor_known_at"], utc=True, errors="coerce"
    )

    rows: list[dict[str, object]] = []
    for row in frame.itertuples(index=False):
        if pd.isna(row.origin_anchor_known_at) or pd.isna(row.origin_anchor_price):
            result = {
                "evaluable": False,
                "destroyed_before_candidate": None,
                "first_destruction_at": None,
                "max_anchor_exceed_points": None,
            }
        else:
            result = selected_origin_conflict(
                m1=m1,
                side=str(row.side),
                origin_anchor_known_at=pd.Timestamp(row.origin_anchor_known_at),
                origin_anchor_price=float(row.origin_anchor_price),
                candidate_known_at=pd.Timestamp(row.candidate_known_at),
            )

        rows.append(
            {
                "candidate_known_at": pd.Timestamp(row.candidate_known_at).isoformat(),
                "side": str(row.side).upper(),
                "origin_anchor_known_at": (
                    pd.Timestamp(row.origin_anchor_known_at).isoformat()
                    if not pd.isna(row.origin_anchor_known_at)
                    else None
                ),
                "origin_anchor_price": (
                    float(row.origin_anchor_price)
                    if not pd.isna(row.origin_anchor_price)
                    else None
                ),
                **result,
            }
        )
    return pd.DataFrame(rows)


def summarize_scan(scan: pd.DataFrame) -> dict[str, object]:
    if scan.empty:
        return {
            "inherited_events": 0,
            "evaluable_events": 0,
            "destroyed_events": 0,
            "intact_events": 0,
            "destroyed_fraction": None,
            "period_state": "NOT_TESTABLE_WITH_CURRENT_EVIDENCE",
        }

    evaluable = scan[scan["evaluable"] == True]
    destroyed = evaluable[evaluable["destroyed_before_candidate"] == True]
    intact = evaluable[evaluable["destroyed_before_candidate"] == False]
    if evaluable.empty:
        state = "NOT_TESTABLE_WITH_CURRENT_EVIDENCE"
        fraction = None
    else:
        state = "CONFLICT_OBSERVED" if not destroyed.empty else "NO_CONFLICT_OBSERVED"
        fraction = float(len(destroyed) / len(evaluable))

    return {
        "inherited_events": len(scan),
        "evaluable_events": len(evaluable),
        "destroyed_events": len(destroyed),
        "intact_events": len(intact),
        "destroyed_fraction": fraction,
        "period_state": state,
    }


def _slice_period(
    events: pd.DataFrame,
    *,
    period_start: pd.Timestamp | None,
    period_end: pd.Timestamp | None,
) -> pd.DataFrame:
    if period_start is None and period_end is None:
        return events
    if period_start is None or period_end is None:
        raise ValueError("period_start and period_end must be supplied together")
    start = pd.Timestamp(period_start)
    end = pd.Timestamp(period_end)
    if start.tzinfo is None or end.tzinfo is None:
        raise ValueError("period bounds must be timezone-aware")
    known_at = pd.to_datetime(events["candidate_known_at"], utc=True)
    return events[(known_at >= start.tz_convert("UTC")) & (known_at < end.tz_convert("UTC") + pd.Timedelta(days=1))].copy()


def run(
    *,
    m1_path: str | Path,
    remaining_events_path: str | Path,
    report_path: str | Path,
    scan_path: str | Path,
    period_start: pd.Timestamp | None = None,
    period_end: pd.Timestamp | None = None,
) -> dict[str, object]:
    m1 = load_ohlc_csv(m1_path)
    if "volume" in m1.columns:
        m1 = m1[m1["volume"] > 0].copy()
    events = pd.read_csv(remaining_events_path)
    events = _slice_period(events, period_start=period_start, period_end=period_end)
    scan = scan_events(m1=m1, events=events)

    target_scan = Path(scan_path)
    target_scan.parent.mkdir(parents=True, exist_ok=True)
    scan.to_csv(target_scan, index=False)

    summary = summarize_scan(scan)
    report: dict[str, object] = {
        "research_status": "POST_SIG_SOURCE_PARTIAL_INVALIDATION_CONFLICT_SCAN",
        "source_m1": str(m1_path),
        "source_remaining_events": str(remaining_events_path),
        "source_claim": "POST_SIG_INVALIDATION = ACTIVE_PARTIAL",
        "representation": {
            "BUY": "destroyed if any later M1 Low < selected origin_anchor_price",
            "SELL": "destroyed if any later M1 High > selected origin_anchor_price",
            "interval": "[origin_anchor_known_at, candidate_known_at)",
            "equality": "not destroyed in this frozen strict-beyond representation",
            "buffer": "none; the transcript's ~200-point case is example-specific",
        },
        "summary": summary,
        "guardrails": [
            "This scans only the currently selected origin; it does not perform full re-anchoring.",
            "SELL is a directional-mirror research representation; exact source geometry remains partial.",
            "No time expiry or distance threshold is selected.",
            "Historical performance is not used to identify teacher intent.",
        ],
    }
    target_report = Path(report_path)
    target_report.parent.mkdir(parents=True, exist_ok=True)
    target_report.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report


def _parse_bound(value: str | None) -> pd.Timestamp | None:
    if value is None:
        return None
    ts = pd.Timestamp(value)
    if ts.tzinfo is None:
        ts = ts.tz_localize("UTC")
    return ts.tz_convert("UTC")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--m1", required=True)
    parser.add_argument("--remaining-events", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--scan", required=True)
    parser.add_argument("--period-start", default=None)
    parser.add_argument("--period-end", default=None)
    args = parser.parse_args()
    report = run(
        m1_path=args.m1,
        remaining_events_path=args.remaining_events,
        report_path=args.report,
        scan_path=args.scan,
        period_start=_parse_bound(args.period_start),
        period_end=_parse_bound(args.period_end),
    )
    print(json.dumps(report["summary"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
