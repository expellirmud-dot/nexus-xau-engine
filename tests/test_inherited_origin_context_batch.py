from __future__ import annotations

from pathlib import Path

import pandas as pd

from nexus_xau.research.inherited_origin_context_batch import (
    discover_daily_events_file,
    discover_remaining_events_file,
    replicated_direction,
)


def _write_remaining(path: Path) -> None:
    pd.DataFrame(
        [
            {
                "state": "INHERITED_REMAINING_RUN",
                "cutoff_utc": "2024-09-02T00:00:00Z",
                "candidate_known_at": "2024-09-02T08:00:00Z",
                "side": "BUY",
                "origin_anchor_known_at": "2024-09-01T12:00:00Z",
                "remaining_at_entry_points": 600.0,
                "fresh_target_reached_anywhere": True,
                "fresh_first_hit": "TARGET_FIRST",
                "fresh_mfe_points": 1500.0,
                "fresh_mae_points": 500.0,
                "path_remaining_reached": True,
                "path_remaining_first_hit": "TARGET_FIRST",
                "origin_level_reached": False,
                "origin_level_first_hit": "STOP_FIRST",
            }
        ]
    ).to_csv(path, index=False)


def _write_daily(path: Path) -> None:
    pd.DataFrame(
        [
            {
                "candidate_known_at": "2024-09-02T08:00:00Z",
                "side": "BUY",
                "signed_valid_side_distance_points": 100.0,
            }
        ]
    ).to_csv(path, index=False)


def test_discovery_finds_parent_tables(tmp_path: Path) -> None:
    remaining = tmp_path / "remaining.csv"
    daily = tmp_path / "daily.csv"
    _write_remaining(remaining)
    _write_daily(daily)

    assert discover_remaining_events_file(
        tmp_path,
        start="2024-09-01",
        end="2024-11-30",
    ) == remaining
    assert discover_daily_events_file(
        tmp_path,
        start="2024-09-01",
        end="2024-11-30",
    ) == daily


def test_replicated_direction_requires_replication_without_opposite() -> None:
    states = ["YOUNGER_ORIGIN_FAVORED", "MIXED", "YOUNGER_ORIGIN_FAVORED"]
    assert replicated_direction(
        states,
        direction_a="YOUNGER_ORIGIN_FAVORED",
        direction_b="OLDER_ORIGIN_FAVORED",
    ) == "REPLICATED_RESEARCH_RELATION::YOUNGER_ORIGIN_FAVORED"

    conflicting = ["YOUNGER_ORIGIN_FAVORED", "OLDER_ORIGIN_FAVORED", "MIXED"]
    assert replicated_direction(
        conflicting,
        direction_a="YOUNGER_ORIGIN_FAVORED",
        direction_b="OLDER_ORIGIN_FAVORED",
    ) == "NOT_STABLE_ACROSS_PERIODS"
