from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = {
    "case_id",
    "source_file",
    "source_time_range",
    "source_class",
    "timeframe",
    "pattern_label",
    "side",
    "location_label",
    "context_label",
    "alignment_status",
    "market_timestamp",
    "boundary_family",
    "boundary_low",
    "boundary_high",
    "notes",
}

TEXT_ONLY = "TEXT_LABELED_NOT_OHLC_ALIGNED"
OHLC_ALIGNED = "OHLC_ALIGNED"


@dataclass(frozen=True, slots=True)
class TruthSetReadiness:
    total_cases: int
    text_labeled_cases: int
    ohlc_aligned_cases: int
    invalid_aligned_cases: tuple[str, ...]

    @property
    def numeric_location_ready(self) -> bool:
        return self.ohlc_aligned_cases > 0 and not self.invalid_aligned_cases


def load_location_truth_set(path: str | Path) -> pd.DataFrame:
    frame = pd.read_csv(path, keep_default_na=False)
    missing = REQUIRED_COLUMNS.difference(frame.columns)
    if missing:
        raise ValueError(f"truth set missing required columns: {sorted(missing)}")
    if frame["case_id"].duplicated().any():
        duplicates = frame.loc[frame["case_id"].duplicated(), "case_id"].tolist()
        raise ValueError(f"duplicate truth-set case_id values: {duplicates}")
    return frame


def _nonempty(value: object) -> bool:
    return bool(str(value).strip())


def _numeric(value: object) -> bool:
    if not _nonempty(value):
        return False
    try:
        float(value)
    except (TypeError, ValueError):
        return False
    return True


def evaluate_truth_set_readiness(frame: pd.DataFrame) -> TruthSetReadiness:
    invalid: list[str] = []
    aligned_count = 0
    text_count = 0

    for row in frame.to_dict(orient="records"):
        case_id = str(row["case_id"])
        status = str(row["alignment_status"]).strip()
        if status == TEXT_ONLY:
            text_count += 1
            continue
        if status != OHLC_ALIGNED:
            invalid.append(f"{case_id}: unknown alignment_status={status!r}")
            continue

        aligned_count += 1
        missing_fields: list[str] = []
        for field in (
            "market_timestamp",
            "timeframe",
            "side",
            "boundary_family",
            "pattern_label",
            "location_label",
        ):
            if not _nonempty(row[field]) or str(row[field]).upper() == "UNKNOWN":
                missing_fields.append(field)
        if not _numeric(row["boundary_low"]):
            missing_fields.append("boundary_low")
        if not _numeric(row["boundary_high"]):
            missing_fields.append("boundary_high")

        if missing_fields:
            invalid.append(f"{case_id}: OHLC_ALIGNED missing {sorted(set(missing_fields))}")
            continue

        if float(row["boundary_high"]) < float(row["boundary_low"]):
            invalid.append(f"{case_id}: boundary_high < boundary_low")

    return TruthSetReadiness(
        total_cases=len(frame),
        text_labeled_cases=text_count,
        ohlc_aligned_cases=aligned_count,
        invalid_aligned_cases=tuple(invalid),
    )
