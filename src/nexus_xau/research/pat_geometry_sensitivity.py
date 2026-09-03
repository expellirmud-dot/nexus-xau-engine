from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from nexus_xau.data.csv_loader import load_ohlc_csv
from nexus_xau.data.resample import resample_ohlc

MIDPOINT_BASES = ("BODY", "FULL_RANGE")
SMALL_BODY_THRESHOLDS = (0.10, 0.20, 0.30, 0.40, 0.50)
EQUAL_WICK_THRESHOLDS = (0.05, 0.10, 0.20, 0.30)


def _frames_from_m1(m1: pd.DataFrame) -> dict[str, pd.DataFrame]:
    return {
        "M1": m1,
        "M5": resample_ohlc(m1, "M5"),
        "H1": resample_ohlc(m1, "H1"),
        "H4": resample_ohlc(m1, "H4"),
        "D1": resample_ohlc(m1, "D1"),
    }


def _direction(row: pd.Series) -> str:
    if float(row.close) > float(row.open):
        return "BULL"
    if float(row.close) < float(row.open):
        return "BEAR"
    return "DOJI"


def _midpoint(row: pd.Series, basis: str) -> float:
    if basis == "BODY":
        return (float(row.open) + float(row.close)) / 2.0
    if basis == "FULL_RANGE":
        return (float(row.high) + float(row.low)) / 2.0
    raise ValueError(f"Unsupported midpoint basis: {basis}")


def _passes_midpoint(close: float, row: pd.Series, side: str, basis: str) -> bool:
    midpoint = _midpoint(row, basis)
    return close > midpoint if side == "BUY" else close < midpoint


def _body_fraction(row: pd.Series) -> float | None:
    full_range = float(row.high) - float(row.low)
    if full_range <= 0:
        return None
    return abs(float(row.close) - float(row.open)) / full_range


def _equal_wick_error_fraction(row: pd.Series) -> float | None:
    full_range = float(row.high) - float(row.low)
    if full_range <= 0:
        return None
    upper = float(row.high) - max(float(row.open), float(row.close))
    lower = min(float(row.open), float(row.close)) - float(row.low)
    return abs(upper - lower) / full_range


def _agreement_counts(body_flags: list[bool], full_flags: list[bool]) -> dict[str, int]:
    return {
        "both": sum(b and f for b, f in zip(body_flags, full_flags, strict=True)),
        "body_only": sum(b and not f for b, f in zip(body_flags, full_flags, strict=True)),
        "full_range_only": sum((not b) and f for b, f in zip(body_flags, full_flags, strict=True)),
        "neither": sum((not b) and (not f) for b, f in zip(body_flags, full_flags, strict=True)),
    }


def _scan_timeframe(frame: pd.DataFrame, timeframe: str) -> dict[str, object]:
    directions = [_direction(frame.iloc[i]) for i in range(len(frame))]

    pat2: dict[str, object] = {}
    for side in ("BUY", "SELL"):
        candidates: list[int] = []
        expected = ("BEAR", "BULL") if side == "BUY" else ("BULL", "BEAR")
        for i in range(1, len(frame)):
            if (directions[i - 1], directions[i]) == expected:
                candidates.append(i)

        basis_flags: dict[str, list[bool]] = {basis: [] for basis in MIDPOINT_BASES}
        equality_counts = {basis: 0 for basis in MIDPOINT_BASES}
        for i in candidates:
            c1 = frame.iloc[i - 1]
            c2 = frame.iloc[i]
            close = float(c2.close)
            for basis in MIDPOINT_BASES:
                midpoint = _midpoint(c1, basis)
                basis_flags[basis].append(_passes_midpoint(close, c1, side, basis))
                if close == midpoint:
                    equality_counts[basis] += 1

        pat2[side] = {
            "topology_candidates": len(candidates),
            "midpoint_pass": {
                basis: sum(basis_flags[basis]) for basis in MIDPOINT_BASES
            },
            "midpoint_exact_equality": equality_counts,
            "basis_agreement": _agreement_counts(
                basis_flags["BODY"], basis_flags["FULL_RANGE"]
            ),
        }

    pat3: dict[str, object] = {}
    for side in ("BUY", "SELL"):
        candidates: list[int] = []
        expected_c1 = "BEAR" if side == "BUY" else "BULL"
        expected_c3 = "BULL" if side == "BUY" else "BEAR"
        for i in range(2, len(frame)):
            if directions[i - 1] == "DOJI":
                continue
            if directions[i - 2] == expected_c1 and directions[i] == expected_c3:
                candidates.append(i)

        basis_flags: dict[str, list[bool]] = {basis: [] for basis in MIDPOINT_BASES}
        c2_body_fractions: list[float | None] = []
        c2_wick_errors: list[float | None] = []
        equality_counts = {basis: 0 for basis in MIDPOINT_BASES}

        for i in candidates:
            c1 = frame.iloc[i - 2]
            c2 = frame.iloc[i - 1]
            c3 = frame.iloc[i]
            close = float(c3.close)
            c2_body_fractions.append(_body_fraction(c2))
            c2_wick_errors.append(_equal_wick_error_fraction(c2))
            for basis in MIDPOINT_BASES:
                mid1 = _midpoint(c1, basis)
                mid2 = _midpoint(c2, basis)
                passed = _passes_midpoint(close, c1, side, basis) and _passes_midpoint(
                    close, c2, side, basis
                )
                basis_flags[basis].append(passed)
                if close == mid1 or close == mid2:
                    equality_counts[basis] += 1

        threshold_rows: list[dict[str, object]] = []
        for basis in MIDPOINT_BASES:
            for small_body_max in SMALL_BODY_THRESHOLDS:
                base_count = 0
                for passed, body_fraction in zip(
                    basis_flags[basis], c2_body_fractions, strict=True
                ):
                    if passed and body_fraction is not None and body_fraction <= small_body_max:
                        base_count += 1

                if side == "BUY":
                    threshold_rows.append(
                        {
                            "basis": basis,
                            "small_body_max_range_fraction": small_body_max,
                            "count": base_count,
                        }
                    )
                else:
                    for equal_wick_max in EQUAL_WICK_THRESHOLDS:
                        count = 0
                        for passed, body_fraction, wick_error in zip(
                            basis_flags[basis],
                            c2_body_fractions,
                            c2_wick_errors,
                            strict=True,
                        ):
                            if (
                                passed
                                and body_fraction is not None
                                and body_fraction <= small_body_max
                                and wick_error is not None
                                and wick_error <= equal_wick_max
                            ):
                                count += 1
                        threshold_rows.append(
                            {
                                "basis": basis,
                                "small_body_max_range_fraction": small_body_max,
                                "equal_wick_max_range_fraction": equal_wick_max,
                                "count": count,
                            }
                        )

        pat3[side] = {
            "topology_candidates": len(candidates),
            "midpoint_pass": {
                basis: sum(basis_flags[basis]) for basis in MIDPOINT_BASES
            },
            "midpoint_exact_equality_to_c1_or_c2": equality_counts,
            "basis_agreement": _agreement_counts(
                basis_flags["BODY"], basis_flags["FULL_RANGE"]
            ),
            "threshold_sensitivity": threshold_rows,
        }

    return {
        "timeframe": timeframe,
        "bars": len(frame),
        "PAT2": pat2,
        "PAT3": pat3,
    }


def run_pat_geometry_sensitivity(
    csv_path: str | Path,
    *,
    report_path: str | Path | None = None,
) -> dict[str, object]:
    m1 = load_ohlc_csv(csv_path)
    if m1.empty:
        raise ValueError("Dataset is empty")

    timeframe_results = [
        _scan_timeframe(frame, timeframe)
        for timeframe, frame in _frames_from_m1(m1).items()
    ]

    report: dict[str, object] = {
        "research_status": "PARAMETER_SENSITIVITY_NOT_A_SIGNAL",
        "source_csv": str(csv_path),
        "start_utc": m1.index[0].isoformat(),
        "end_utc": m1.index[-1].isoformat(),
        "confirmed_logic_applied": [
            "PAT2 candle-color topology",
            "PAT3 candle-color topology with exact doji excluded for candle #2",
            "strict directional >50% test under each explicitly named midpoint basis",
        ],
        "research_variants_not_system_rules": {
            "midpoint_bases": list(MIDPOINT_BASES),
            "pat3_small_body_max_range_fraction": list(SMALL_BODY_THRESHOLDS),
            "pat3_sell_equal_wick_max_range_fraction": list(EQUAL_WICK_THRESHOLDS),
        },
        "still_omitted": [
            "support_resistance_location_and_tolerance",
            "PAT1_numeric_geometry",
            "final_choice_of_PAT_midpoint_basis",
            "final_equality_or_point_tolerance_around_50pct",
            "final_PAT3_small_body_threshold",
            "final_PAT3_SELL_equal_wick_tolerance",
            "SIG/post_SIG qualification",
            "entry_stop_target_and_trade_outcome",
        ],
        "timeframes": timeframe_results,
    }

    if report_path is not None:
        target = Path(report_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="PAT geometry sensitivity research")
    parser.add_argument("--input", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()
    report = run_pat_geometry_sensitivity(args.input, report_path=args.report)
    print("PAT geometry sensitivity: RESEARCH VARIANTS / NOT A SIGNAL")
    print(f"UTC range: {report['start_utc']} -> {report['end_utc']}")
    for item in report["timeframes"]:
        tf = item["timeframe"]
        for kind in ("PAT2", "PAT3"):
            for side in ("BUY", "SELL"):
                node = item[kind][side]
                print(
                    f"{tf} {kind} {side}: topology={node['topology_candidates']} "
                    f"BODY50={node['midpoint_pass']['BODY']} "
                    f"FULL50={node['midpoint_pass']['FULL_RANGE']}"
                )
    print(f"Report: {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
