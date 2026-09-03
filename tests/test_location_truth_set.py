from pathlib import Path

import pandas as pd
import pytest

from nexus_xau.research.location_truth_set import (
    OHLC_ALIGNED,
    TEXT_ONLY,
    evaluate_truth_set_readiness,
    load_location_truth_set,
)

BASE = {
    "case_id": "L001",
    "source_file": "docs/source.md",
    "source_time_range": "1:00-2:00",
    "source_class": "PRIMARY_TRANSCRIPT",
    "timeframe": "M5",
    "pattern_label": "PAT2",
    "side": "BUY",
    "location_label": "CORRECT_LOCATION",
    "context_label": "AT_SUPPORT",
    "alignment_status": OHLC_ALIGNED,
    "market_timestamp": "2026-08-03T10:00:00+00:00",
    "boundary_family": "MANUAL_SUPPORT_RESISTANCE",
    "boundary_low": "3300.0",
    "boundary_high": "3300.0",
    "notes": "test",
}


def test_text_only_seed_is_not_numeric_ready() -> None:
    row = {**BASE, "alignment_status": TEXT_ONLY, "market_timestamp": "", "boundary_low": "", "boundary_high": ""}
    readiness = evaluate_truth_set_readiness(pd.DataFrame([row]))

    assert readiness.total_cases == 1
    assert readiness.text_labeled_cases == 1
    assert readiness.ohlc_aligned_cases == 0
    assert readiness.numeric_location_ready is False


def test_valid_ohlc_aligned_case_is_numeric_ready() -> None:
    readiness = evaluate_truth_set_readiness(pd.DataFrame([BASE]))

    assert readiness.ohlc_aligned_cases == 1
    assert readiness.invalid_aligned_cases == ()
    assert readiness.numeric_location_ready is True


def test_ohlc_aligned_missing_boundary_is_invalid() -> None:
    row = {**BASE, "boundary_low": ""}
    readiness = evaluate_truth_set_readiness(pd.DataFrame([row]))

    assert readiness.numeric_location_ready is False
    assert "boundary_low" in readiness.invalid_aligned_cases[0]


def test_ohlc_aligned_unknown_timeframe_is_invalid() -> None:
    row = {**BASE, "timeframe": "UNKNOWN"}
    readiness = evaluate_truth_set_readiness(pd.DataFrame([row]))

    assert readiness.numeric_location_ready is False
    assert "timeframe" in readiness.invalid_aligned_cases[0]


def test_boundary_order_is_validated() -> None:
    row = {**BASE, "boundary_low": "3301", "boundary_high": "3300"}
    readiness = evaluate_truth_set_readiness(pd.DataFrame([row]))

    assert readiness.numeric_location_ready is False
    assert "boundary_high < boundary_low" in readiness.invalid_aligned_cases[0]


def test_loader_rejects_duplicate_case_ids(tmp_path: Path) -> None:
    path = tmp_path / "truth.csv"
    pd.DataFrame([BASE, BASE]).to_csv(path, index=False)

    with pytest.raises(ValueError, match="duplicate"):
        load_location_truth_set(path)
