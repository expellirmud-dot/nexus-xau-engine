from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import pandas as pd

from nexus_xau.data.csv_loader import load_ohlc_csv
from nexus_xau.data.resample import resample_ohlc
from nexus_xau.engine.mae_pla_frame import build_mae_pla_frame_candidates


@dataclass(frozen=True, slots=True)
class DailyTimingComparison:
    date_utc: str
    utc00_open: float
    utc04_open: float
    utc00_references: tuple[float, ...]
    utc04_references: tuple[float, ...]
    reference_sets_equal: bool
    minimum_reference_gap_price: float


@dataclass(frozen=True, slots=True)
class MaePlaTimingSensitivityResult:
    source_csv: str
    start_utc: str
    end_utc: str
    compared_days: int
    equal_reference_days: int
    different_reference_days: int
    equal_reference_rate: float
    median_minimum_reference_gap_price: float
    p75_minimum_reference_gap_price: float
    max_minimum_reference_gap_price: float
    comparisons: tuple[DailyTimingComparison, ...]


def _refs(open_price: float) -> tuple[float, ...]:
    frame = build_mae_pla_frame_candidates(open_price)
    return tuple(candidate.reference_price for candidate in frame.candidates)


def run_mae_pla_time_sensitivity(
    csv_path: str | Path,
    *,
    report_path: str | Path | None = None,
    rows_path: str | Path | None = None,
) -> MaePlaTimingSensitivityResult:
    """Compare two explicit UTC H4 context variants without selecting a winner.

    This is a timing-sensitivity study only. UTC00 and UTC04 are alternative
    observable H4 contexts in the validated dataset; neither is asserted to be
    the teacher's intended 07:00 mapping.
    """

    m1 = load_ohlc_csv(csv_path)
    h4 = resample_ohlc(m1, "H4")

    by_date: dict[str, dict[int, pd.Series]] = {}
    for timestamp, row in h4.iterrows():
        if timestamp.hour not in {0, 4}:
            continue
        date_key = timestamp.date().isoformat()
        by_date.setdefault(date_key, {})[timestamp.hour] = row

    comparisons: list[DailyTimingComparison] = []
    for date_key in sorted(by_date):
        contexts = by_date[date_key]
        if 0 not in contexts or 4 not in contexts:
            continue

        open00 = float(contexts[0]["open"])
        open04 = float(contexts[4]["open"])
        refs00 = _refs(open00)
        refs04 = _refs(open04)
        equal = set(refs00) == set(refs04)
        minimum_gap = min(abs(a - b) for a in refs00 for b in refs04)
        comparisons.append(
            DailyTimingComparison(
                date_utc=date_key,
                utc00_open=open00,
                utc04_open=open04,
                utc00_references=refs00,
                utc04_references=refs04,
                reference_sets_equal=equal,
                minimum_reference_gap_price=minimum_gap,
            )
        )

    if not comparisons:
        raise ValueError("No days contain both UTC00 and UTC04 H4 contexts")

    gaps = pd.Series([item.minimum_reference_gap_price for item in comparisons], dtype=float)
    equal_count = sum(item.reference_sets_equal for item in comparisons)
    result = MaePlaTimingSensitivityResult(
        source_csv=str(csv_path),
        start_utc=m1.index[0].isoformat(),
        end_utc=m1.index[-1].isoformat(),
        compared_days=len(comparisons),
        equal_reference_days=equal_count,
        different_reference_days=len(comparisons) - equal_count,
        equal_reference_rate=equal_count / len(comparisons),
        median_minimum_reference_gap_price=float(gaps.median()),
        p75_minimum_reference_gap_price=float(gaps.quantile(0.75)),
        max_minimum_reference_gap_price=float(gaps.max()),
        comparisons=tuple(comparisons),
    )

    if report_path is not None:
        path = Path(report_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            **asdict(result),
            "research_status": "TIMING_SENSITIVITY_NOT_CANONICAL",
            "variant_warning": (
                "UTC00 and UTC04 are explicit research contexts only. "
                "The teacher's exact 07:00 timezone/server mapping remains unresolved."
            ),
            "outcome_used": False,
        }
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    if rows_path is not None:
        path = Path(rows_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame([asdict(item) for item in comparisons]).to_csv(path, index=False)

    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--report", default=None)
    parser.add_argument("--rows", default=None)
    args = parser.parse_args()

    result = run_mae_pla_time_sensitivity(
        args.input,
        report_path=args.report,
        rows_path=args.rows,
    )
    print("MAE_PLA TIMING SENSITIVITY / NOT CANONICAL")
    print(f"Compared days: {result.compared_days}")
    print(
        f"Equal statistical reference: {result.equal_reference_days}/{result.compared_days} "
        f"({result.equal_reference_rate:.2%})"
    )
    print(
        "Minimum reference gap price: "
        f"median={result.median_minimum_reference_gap_price:.3f} "
        f"p75={result.p75_minimum_reference_gap_price:.3f} "
        f"max={result.max_minimum_reference_gap_price:.3f}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
