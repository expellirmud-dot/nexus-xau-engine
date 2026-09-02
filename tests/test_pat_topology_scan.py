from pathlib import Path

import pandas as pd

from nexus_xau.research.pat_topology_scan import (
    run_pat_topology_research,
    scan_pat_color_topology,
)


def _m1_frame() -> pd.DataFrame:
    index = pd.date_range("2026-01-01T00:00:00Z", periods=6, freq="1min")
    # Directions: BEAR, BULL, BULL, BULL, BEAR, BEAR
    return pd.DataFrame(
        {
            "open": [10.0, 9.0, 10.0, 11.0, 12.0, 11.0],
            "high": [10.5, 10.5, 11.5, 12.5, 12.5, 11.5],
            "low": [8.5, 8.5, 9.5, 10.5, 10.5, 9.5],
            "close": [9.0, 10.0, 11.0, 12.0, 11.0, 10.0],
        },
        index=index,
    )


def test_scan_counts_m1_color_topology_without_promoting_signal() -> None:
    summaries, hits = scan_pat_color_topology(_m1_frame())
    m1 = next(item for item in summaries if item.timeframe == "M1")

    assert m1.bars == 6
    assert m1.pat2_windows_tested == 5
    assert m1.pat2_buy_color_candidates == 1
    assert m1.pat2_sell_color_candidates == 1
    assert m1.pat3_windows_tested == 4
    assert m1.pat3_buy_color_candidates == 1
    assert m1.pat3_sell_color_candidates == 2
    assert any(hit.timeframe == "M1" and hit.kind == "PAT3" for hit in hits)


def test_run_writes_research_report_and_hits(tmp_path: Path) -> None:
    source = tmp_path / "m1.csv"
    frame = _m1_frame().reset_index().rename(columns={"index": "timestamp"})
    frame.to_csv(source, index=False)

    report = tmp_path / "report.json"
    hits = tmp_path / "hits.csv"
    result = run_pat_topology_research(source, report_path=report, hits_path=hits)

    assert result.total_hits > 0
    assert report.exists()
    assert hits.exists()
    text = report.read_text(encoding="utf-8")
    assert "COLOR_TOPOLOGY_ONLY_NOT_A_SIGNAL" in text
    assert "support_resistance_location" in text
