import pandas as pd
import pytest

from nexus_xau.replay.tick_reference import (
    DATA_EXCLUDED_ARCHIVE_GAP,
    DATA_EXCLUDED_INCOMPLETE_HORIZON,
    DATA_EXCLUDED_INSUFFICIENT_WARMUP,
    DATA_EXCLUDED_NO_POST_CONFIRMATION_QUOTE,
    REFERENCE_FILL_STATUS,
    SLIPPAGE_STATUS,
    GapInterval,
    evaluate_supplied_levels,
    first_reference_entry,
    spread,
    validate_tick_frame,
    window_exclusion_reason,
)


def _ticks(rows: list[tuple[str, float, float]]) -> pd.DataFrame:
    return pd.DataFrame(
        {"bid": [r[1] for r in rows], "ask": [r[2] for r in rows]},
        index=pd.DatetimeIndex([pd.Timestamp(r[0]) for r in rows]),
    )


def test_reference_entry_uses_first_tick_strictly_after_known_at() -> None:
    ticks = _ticks(
        [
            ("2026-01-01T00:00:00Z", 100.0, 100.2),
            ("2026-01-01T00:00:01Z", 100.1, 100.3),
        ]
    )
    buy = first_reference_entry(
        ticks, known_at="2026-01-01T00:00:00Z", side="BUY", source_id="archive"
    )
    sell = first_reference_entry(
        ticks, known_at="2026-01-01T00:00:00Z", side="SELL", source_id="archive"
    )
    assert buy.timestamp == pd.Timestamp("2026-01-01T00:00:01Z")
    assert buy.price == pytest.approx(100.3)
    assert sell.price == pytest.approx(100.1)
    assert buy.fill_status == REFERENCE_FILL_STATUS
    assert buy.slippage_status == SLIPPAGE_STATUS


def test_reference_entry_without_post_confirmation_quote_is_excluded() -> None:
    ticks = _ticks([("2026-01-01T00:00:00Z", 100.0, 100.2)])
    with pytest.raises(LookupError, match=DATA_EXCLUDED_NO_POST_CONFIRMATION_QUOTE):
        first_reference_entry(
            ticks, known_at="2026-01-01T00:00:00Z", side="BUY", source_id="archive"
        )


def test_exact_duplicate_rows_do_not_create_multiple_level_outcomes() -> None:
    ticks = _ticks(
        [
            ("2026-01-01T00:00:01Z", 101.0, 101.2),
            ("2026-01-01T00:00:01Z", 101.0, 101.2),
        ]
    )
    outcome = evaluate_supplied_levels(
        ticks,
        start_after="2026-01-01T00:00:00Z",
        side="BUY",
        stop_level=99.0,
        target_level=101.0,
        source_id="archive",
    )
    assert outcome.outcome == "TARGET_FIRST"
    assert outcome.timestamp == pd.Timestamp("2026-01-01T00:00:01Z")


def test_equal_timestamp_conflicting_first_touch_is_ambiguous() -> None:
    ticks = _ticks(
        [
            ("2026-01-01T00:00:01Z", 98.5, 98.7),
            ("2026-01-01T00:00:01Z", 101.5, 101.7),
        ]
    )
    outcome = evaluate_supplied_levels(
        ticks,
        start_after="2026-01-01T00:00:00Z",
        side="BUY",
        stop_level=99.0,
        target_level=101.0,
        source_id="archive",
    )
    assert outcome.outcome == "AMBIGUOUS_SAME_TIMESTAMP"
    assert outcome.price is None


def test_long_stop_gap_uses_observed_bid_not_ideal_stop() -> None:
    ticks = _ticks([("2026-01-01T00:00:01Z", 98.4, 98.6)])
    outcome = evaluate_supplied_levels(
        ticks,
        start_after="2026-01-01T00:00:00Z",
        side="BUY",
        stop_level=99.0,
        target_level=101.0,
        source_id="archive",
    )
    assert outcome.outcome == "STOP_FIRST"
    assert outcome.price == pytest.approx(98.4)


def test_short_target_and_stop_use_ask() -> None:
    target_ticks = _ticks([("2026-01-01T00:00:01Z", 97.7, 97.9)])
    target = evaluate_supplied_levels(
        target_ticks,
        start_after="2026-01-01T00:00:00Z",
        side="SELL",
        stop_level=101.0,
        target_level=98.0,
        source_id="archive",
    )
    assert target.outcome == "TARGET_FIRST"
    assert target.price == pytest.approx(97.9)

    stop_ticks = _ticks([("2026-01-01T00:00:01Z", 101.0, 101.2)])
    stop = evaluate_supplied_levels(
        stop_ticks,
        start_after="2026-01-01T00:00:00Z",
        side="SELL",
        stop_level=101.0,
        target_level=98.0,
        source_id="archive",
    )
    assert stop.outcome == "STOP_FIRST"
    assert stop.price == pytest.approx(101.2)


def test_spread_is_ask_minus_bid() -> None:
    assert spread(100.0, 100.25) == pytest.approx(0.25)
    with pytest.raises(ValueError, match="Ask"):
        spread(100.2, 100.1)


def test_window_gap_and_boundary_exclusions_are_explicit() -> None:
    gap = GapInterval(
        start=pd.Timestamp("2026-01-02T00:00:00Z"),
        end=pd.Timestamp("2026-01-03T00:00:00Z"),
        label="known-gap",
    )
    assert (
        window_exclusion_reason(
            required_start="2026-01-01T12:00:00Z",
            required_end="2026-01-03T12:00:00Z",
            available_start="2026-01-01T00:00:00Z",
            available_end="2026-01-04T00:00:00Z",
            gaps=(gap,),
        )
        == DATA_EXCLUDED_ARCHIVE_GAP
    )
    assert (
        window_exclusion_reason(
            required_start="2025-12-31T23:00:00Z",
            required_end="2026-01-01T12:00:00Z",
            available_start="2026-01-01T00:00:00Z",
            available_end="2026-01-04T00:00:00Z",
        )
        == DATA_EXCLUDED_INSUFFICIENT_WARMUP
    )
    assert (
        window_exclusion_reason(
            required_start="2026-01-01T12:00:00Z",
            required_end="2026-01-05T00:00:00Z",
            available_start="2026-01-01T00:00:00Z",
            available_end="2026-01-04T00:00:00Z",
        )
        == DATA_EXCLUDED_INCOMPLETE_HORIZON
    )


def test_validation_allows_equal_timestamps_but_rejects_regression_and_bad_spread() -> None:
    equal = _ticks(
        [
            ("2026-01-01T00:00:00Z", 100.0, 100.2),
            ("2026-01-01T00:00:00Z", 100.1, 100.3),
        ]
    )
    validate_tick_frame(equal)

    unsorted = _ticks(
        [
            ("2026-01-01T00:00:01Z", 100.0, 100.2),
            ("2026-01-01T00:00:00Z", 100.1, 100.3),
        ]
    )
    with pytest.raises(ValueError, match="oldest to newest"):
        validate_tick_frame(unsorted)

    bad = _ticks([("2026-01-01T00:00:00Z", 100.2, 100.1)])
    with pytest.raises(ValueError, match="Ask < Bid"):
        validate_tick_frame(bad)


def test_replay_primitives_do_not_mutate_raw_frame_or_expose_pnl_fields() -> None:
    ticks = _ticks(
        [
            ("2026-01-01T00:00:00Z", 100.0, 100.2),
            ("2026-01-01T00:00:01Z", 100.1, 100.3),
        ]
    )
    before = ticks.copy(deep=True)
    fill = first_reference_entry(
        ticks, known_at="2026-01-01T00:00:00Z", side="BUY", source_id="archive"
    )
    pd.testing.assert_frame_equal(ticks, before)
    assert "pnl" not in fill.__dataclass_fields__
    assert "win_rate" not in fill.__dataclass_fields__


def test_reference_entry_preserves_archive_source_raw_ordinal() -> None:
    ticks = _ticks(
        [
            ("2026-01-01T00:00:00Z", 100.0, 100.2),
            ("2026-01-01T00:00:01Z", 100.1, 100.3),
        ]
    )
    ticks["raw_ordinal"] = [40, 41]
    fill = first_reference_entry(
        ticks, known_at="2026-01-01T00:00:00Z", side="BUY", source_id="archive"
    )
    assert fill.raw_ordinal == 41


def test_supplied_level_outcome_preserves_archive_source_raw_ordinal() -> None:
    ticks = _ticks(
        [
            ("2026-01-01T00:00:01Z", 100.0, 100.2),
            ("2026-01-01T00:00:02Z", 101.2, 101.4),
        ]
    )
    ticks["raw_ordinal"] = [900, 901]
    outcome = evaluate_supplied_levels(
        ticks,
        start_after="2026-01-01T00:00:00Z",
        side="BUY",
        stop_level=99.0,
        target_level=101.0,
        source_id="archive",
    )
    assert outcome.outcome == "TARGET_FIRST"
    assert outcome.raw_ordinal == 901
