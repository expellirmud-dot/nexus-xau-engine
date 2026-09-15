import pandas as pd
import pytest

from nexus_xau.replay.tick_bars import BAR_REPRESENTATION, build_archive_bid_m1


def _ticks(
    rows: list[tuple[str, float, float]],
    *,
    sha: str = "abc123",
    year: int = 2026,
    month: int = 8,
) -> pd.DataFrame:
    index = (
        pd.DatetimeIndex([pd.Timestamp(row[0]) for row in rows])
        if rows
        else pd.DatetimeIndex([], tz="UTC")
    )
    return pd.DataFrame(
        {
            "bid": [row[1] for row in rows],
            "ask": [row[2] for row in rows],
            "raw_ordinal": list(range(len(rows))),
            "source_year": [year] * len(rows),
            "source_month": [month] * len(rows),
            "source_sha256": [sha] * len(rows),
            "source_local_path": ["archive.zip"] * len(rows),
            "source_validator_version": ["EXNESS_ARCHIVE_VALIDATOR_V0.2"] * len(rows),
        },
        index=index,
    )
def _build(
    ticks: pd.DataFrame,
    *,
    start: str = "2026-08-01T00:00:00Z",
    end: str = "2026-08-01T00:02:00Z",
) -> pd.DataFrame:
    return build_archive_bid_m1(
        ticks,
        requested_start=start,
        requested_end=end,
    )


def test_bid_ohlc_uses_first_max_min_last() -> None:
    ticks = _ticks(
        [
            ("2026-08-01T00:00:01Z", 100.0, 100.2),
            ("2026-08-01T00:00:20Z", 102.0, 102.2),
            ("2026-08-01T00:00:30Z", 99.0, 99.2),
            ("2026-08-01T00:00:59Z", 101.0, 101.2),
        ]
    )
    bars = _build(ticks)
    row = bars.loc[pd.Timestamp("2026-08-01T00:00:00Z")]
    assert [row["open"], row["high"], row["low"], row["close"]] == [100.0, 102.0, 99.0, 101.0]
@pytest.mark.parametrize(
    ("start", "end"),
    [
        ("2026-08-01T00:00:30Z", "2026-08-01T00:02:00Z"),
        ("2026-08-01T00:00:00Z", "2026-08-01T00:01:30Z"),
    ],
)
def test_unaligned_boundaries_are_rejected(start: str, end: str) -> None:
    ticks = _ticks([("2026-08-01T00:00:30Z", 100.0, 100.2)])
    with pytest.raises(ValueError, match="aligned"):
        _build(ticks, start=start, end=end)


def test_left_closed_right_open_minute_assignment() -> None:
    ticks = _ticks(
        [
            ("2026-08-01T00:00:59.999Z", 100.0, 100.2),
            ("2026-08-01T00:01:00Z", 101.0, 101.2),
        ]
    )
    bars = _build(ticks)
    assert list(bars.index) == [
        pd.Timestamp("2026-08-01T00:00:00Z"),
        pd.Timestamp("2026-08-01T00:01:00Z"),
    ]
    assert bars.iloc[0]["close"] == 100.0
    assert bars.iloc[1]["open"] == 101.0
def test_equal_timestamp_source_order_controls_open_and_close() -> None:
    ticks = _ticks(
        [
            ("2026-08-01T00:00:10Z", 100.0, 100.2),
            ("2026-08-01T00:00:10Z", 101.0, 101.2),
            ("2026-08-01T00:00:10Z", 99.0, 99.2),
        ]
    )
    row = _build(ticks).iloc[0]
    assert row["open"] == 100.0
    assert row["close"] == 99.0
    assert row["high"] == 101.0
    assert row["low"] == 99.0


def test_exact_duplicates_remain_in_archive_tick_count() -> None:
    ticks = _ticks(
        [
            ("2026-08-01T00:00:10Z", 100.0, 100.2),
            ("2026-08-01T00:00:10Z", 100.0, 100.2),
        ]
    )
    row = _build(ticks).iloc[0]
    assert row["archive_tick_count"] == 2
def test_empty_minute_creates_no_synthetic_bar() -> None:
    ticks = _ticks(
        [
            ("2026-08-01T00:00:10Z", 100.0, 100.2),
            ("2026-08-01T00:02:10Z", 102.0, 102.2),
        ]
    )
    bars = _build(ticks, end="2026-08-01T00:03:00Z")
    assert list(bars.index) == [
        pd.Timestamp("2026-08-01T00:00:00Z"),
        pd.Timestamp("2026-08-01T00:02:00Z"),
    ]


def test_provenance_and_raw_ordinals_survive_bar_output() -> None:
    ticks = _ticks(
        [
            ("2026-08-01T00:00:10Z", 100.0, 100.2),
            ("2026-08-01T00:00:20Z", 101.0, 101.2),
        ],
        sha="feedbeef",
    )
    row = _build(ticks).iloc[0]
    assert row["source_sha256"] == "feedbeef"
    assert row["source_year"] == 2026
    assert row["source_month"] == 8
    assert row["first_raw_ordinal"] == 0
    assert row["last_raw_ordinal"] == 1
    assert row["bar_representation"] == BAR_REPRESENTATION
def test_ask_changes_do_not_change_geometry_ohlc() -> None:
    a = _ticks(
        [
            ("2026-08-01T00:00:10Z", 100.0, 100.2),
            ("2026-08-01T00:00:20Z", 101.0, 101.2),
        ]
    )
    b = a.copy()
    b["ask"] = [100.8, 102.4]
    cols = ["open", "high", "low", "close"]
    pd.testing.assert_frame_equal(_build(a)[cols], _build(b)[cols])


def test_ticks_outside_requested_window_are_rejected() -> None:
    ticks = _ticks([("2026-08-01T00:02:00Z", 100.0, 100.2)])
    with pytest.raises(ValueError, match="outside requested"):
        _build(ticks)


def test_empty_tick_frame_returns_empty_m1_schema() -> None:
    ticks = _ticks([])
    bars = _build(ticks)
    assert bars.empty
    assert bars.index.tz is not None
    assert "archive_tick_count" in bars.columns
def test_mixed_provenance_inside_one_minute_is_rejected() -> None:
    ticks = _ticks(
        [
            ("2026-08-01T00:00:10Z", 100.0, 100.2),
            ("2026-08-01T00:00:20Z", 101.0, 101.2),
        ]
    )
    ticks.iloc[1, ticks.columns.get_loc("source_sha256")] = "different"
    with pytest.raises(ValueError, match="mixed provenance"):
        _build(ticks)
