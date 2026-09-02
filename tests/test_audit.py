from __future__ import annotations

from pathlib import Path

import pandas as pd

from nexus_xau.data.audit import audit_ohlc_csv


def test_audit_reports_gaps_and_resample_counts(tmp_path: Path) -> None:
    path = tmp_path / "sample.csv"
    frame = pd.DataFrame(
        {
            "timestamp": [
                "2026-01-01T00:00:00+00:00",
                "2026-01-01T00:01:00+00:00",
                "2026-01-01T00:03:00+00:00",
                "2026-01-01T00:04:00+00:00",
                "2026-01-01T00:05:00+00:00",
            ],
            "open": [100, 101, 102, 103, 104],
            "high": [102, 103, 104, 105, 106],
            "low": [99, 100, 101, 102, 103],
            "close": [101, 102, 103, 104, 105],
            "volume": [1, 1, 1, 1, 1],
        }
    )
    frame.to_csv(path, index=False)

    report = tmp_path / "audit.json"
    processed = tmp_path / "processed"
    result = audit_ohlc_csv(path, processed_dir=processed, report_path=report)

    assert result.rows == 5
    assert result.one_minute_steps == 3
    assert result.gaps_over_one_minute == 1
    assert result.largest_gap_seconds == 120
    assert len(result.gap_records) == 1
    assert result.gap_records[0].previous_utc == "2026-01-01T00:01:00+00:00"
    assert result.gap_records[0].next_utc == "2026-01-01T00:03:00+00:00"
    assert result.gap_records[0].missing_m1_slots == 1
    assert result.m5_bars == 2
    assert result.h1_bars == 1
    assert result.h4_bars == 1
    assert result.d1_bars == 1
    assert report.exists()
    assert (processed / "sample_M5.csv").exists()
    assert (processed / "sample_H1.csv").exists()
    assert (processed / "sample_H4.csv").exists()
    assert (processed / "sample_D1.csv").exists()
