from datetime import UTC, date, datetime

import numpy as np

from nexus_xau.data.mt5_coverage import (
    iter_probe_datetimes,
    summarize_coverage,
    summarize_m1_rates,
    summarize_ticks,
)


def test_iter_probe_datetimes_is_utc_and_stepped() -> None:
    values = list(
        iter_probe_datetimes(
            date(2026, 6, 1),
            date(2026, 6, 15),
            step_days=7,
            probe_hour_utc=12,
        )
    )
    assert [value.isoformat() for value in values] == [
        "2026-06-01T12:00:00+00:00",
        "2026-06-08T12:00:00+00:00",
        "2026-06-15T12:00:00+00:00",
    ]


def test_summarize_ticks_uses_millisecond_timestamp() -> None:
    start = datetime(2026, 6, 15, 12, tzinfo=UTC)
    end = datetime(2026, 6, 15, 12, 5, tzinfo=UTC)
    start_msc = int(start.timestamp() * 1000)
    ticks = np.array(
        [
            (start_msc, 4300.0, 4300.2),
            (start_msc + 250, 4300.1, 4300.3),
        ],
        dtype=[("time_msc", "<i8"), ("bid", "<f8"), ("ask", "<f8")],
    )

    result = summarize_ticks(
        ticks,
        symbol="XAUUSDm",
        start_utc=start,
        end_utc=end,
    )

    assert result.status == "AVAILABLE"
    assert result.rows == 2
    assert result.raw_rows == 2
    assert result.out_of_range_rows == 0
    assert result.duplicate_timestamps == 0
    assert result.non_monotonic_timestamps == 0


def test_summarize_m1_rates_reports_nominal_fraction() -> None:
    start = datetime(2026, 6, 15, 12, tzinfo=UTC)
    end = datetime(2026, 6, 15, 12, 5, tzinfo=UTC)
    epoch = int(start.timestamp())
    rates = np.array(
        [(epoch + offset * 60, 4300.0) for offset in range(4)],
        dtype=[("time", "<i8"), ("open", "<f8")],
    )

    result = summarize_m1_rates(
        rates,
        symbol="XAUUSDm",
        start_utc=start,
        end_utc=end,
        window_minutes=5,
    )

    assert result.status == "AVAILABLE"
    assert result.rows == 4
    assert result.nominal_expected_rows == 5
    assert result.nominal_row_fraction == 0.8


def test_m1_response_outside_requested_range_does_not_count_as_available() -> None:
    start = datetime(2026, 6, 1, 12, tzinfo=UTC)
    end = datetime(2026, 6, 1, 12, 5, tzinfo=UTC)
    outside = int(datetime(2026, 6, 3, 9, 5, tzinfo=UTC).timestamp())
    rates = np.array(
        [(outside, 4300.0)],
        dtype=[("time", "<i8"), ("open", "<f8")],
    )

    result = summarize_m1_rates(
        rates,
        symbol="XAUUSDm",
        start_utc=start,
        end_utc=end,
        window_minutes=5,
    )

    assert result.status == "EMPTY"
    assert result.rows == 0
    assert result.raw_rows == 1
    assert result.out_of_range_rows == 1


def test_summarize_coverage_keeps_weekday_empty_separate() -> None:
    start = datetime(2026, 6, 1, 12, tzinfo=UTC)
    end = datetime(2026, 6, 1, 12, 5, tzinfo=UTC)

    tick_empty = summarize_ticks(
        np.array([], dtype=[("time_msc", "<i8")]),
        symbol="XAUUSDm",
        start_utc=start,
        end_utc=end,
    )
    m1_empty = summarize_m1_rates(
        np.array([], dtype=[("time", "<i8")]),
        symbol="XAUUSDm",
        start_utc=start,
        end_utc=end,
        window_minutes=5,
    )

    summary = summarize_coverage([tick_empty, m1_empty])

    assert summary["MT5_HISTORICAL_TICK"]["weekday_empty"] == 1
    assert summary["MT5_OHLC_M1"]["weekday_empty"] == 1
