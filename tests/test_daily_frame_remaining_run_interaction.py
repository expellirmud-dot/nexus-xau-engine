from __future__ import annotations

from pathlib import Path

import pandas as pd

from nexus_xau.research import daily_frame_remaining_run_interaction as interaction
from nexus_xau.research.daily_frame_side_remaining_relation import run as run_daily_side


def test_zero_inherited_events_write_schema_and_close_insufficient(
    tmp_path: Path,
    monkeypatch,
) -> None:
    index = pd.DatetimeIndex([pd.Timestamp("2025-09-01T00:00:00Z")])
    m1 = pd.DataFrame(
        {
            "open": [3500.0],
            "high": [3500.0],
            "low": [3500.0],
            "close": [3500.0],
            "volume": [1.0],
        },
        index=index,
    )
    monkeypatch.setattr(interaction, "load_ohlc_csv", lambda _: m1)
    monkeypatch.setattr(interaction, "resample_ohlc", lambda frame, _: frame)

    remaining_path = tmp_path / "remaining.csv"
    pd.DataFrame(
        {
            "state": ["NO_ACTIVE_INHERITED_RUN"],
            "cutoff_utc": ["2025-09-01T00:00:00+00:00"],
            "candidate_known_at": ["2025-09-01T02:00:00+00:00"],
            "path_remaining_reached": [None],
        }
    ).to_csv(remaining_path, index=False)

    interaction_report_path = tmp_path / "interaction_report.json"
    interaction_events_path = tmp_path / "interaction_events.csv"
    report = interaction.run(
        m1_path=tmp_path / "unused.csv",
        remaining_events_path=remaining_path,
        report_path=interaction_report_path,
        events_path=interaction_events_path,
    )

    assert report["measured_inherited_events"] == 0
    assert report["period_state"] == "INSUFFICIENT"
    events = pd.read_csv(interaction_events_path)
    assert list(events.columns) == interaction.INTERACTION_EVENT_COLUMNS
    assert events.empty

    side_report = run_daily_side(
        interaction_events_path=interaction_events_path,
        report_path=tmp_path / "side_report.json",
    )
    assert side_report["groups"]["EXPECTED_SIDE"]["events"] == 0
    assert side_report["groups"]["CROSSED_SIDE"]["events"] == 0
    assert side_report["period_state"] == "INSUFFICIENT"
