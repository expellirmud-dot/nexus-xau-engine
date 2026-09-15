from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd
import pytest

from nexus_xau.data.csv_loader import load_ohlc_csv
from nexus_xau.data.exness_tick_archive_download import VALIDATOR_VERSION
from nexus_xau.data.resample import resample_ohlc
from nexus_xau.replay.archive_window import (
    CONTINUITY_STATUS,
    WINDOW_STATUS_NO_TICKS,
    WINDOW_STATUS_OK,
    ArchiveMonthProvenance,
)
from nexus_xau.replay.tick_bars import BAR_REPRESENTATION
from nexus_xau.replay.v2_integration import (
    DATA_EXCLUDED_ARCHIVE_PROVENANCE_MISMATCH,
    DATA_EXCLUDED_ARCHIVE_REPRESENTATION_MISMATCH,
    DATA_EXCLUDED_ARCHIVE_WINDOW_EMPTY,
    DATA_EXCLUDED_ARCHIVE_WINDOW_MISMATCH,
    DATA_EXCLUDED_CONTINUATION_CHECKPOINT_NOT_IMPLEMENTED,
    DATA_EXCLUDED_INTEGRATION_BOUNDARY_UNALIGNED,
    DATA_EXCLUDED_ORIGIN_HISTORY_UNSEEDED,
    INTEGRATION_CONTRACT,
    SEED_CONTINUATION_CHECKPOINT,
    SEED_SYNTHETIC_COMPLETE,
    SEED_UNSEEDED_REAL_WINDOW,
    SOURCE_FAMILY,
    ArchiveV2IntegrationError,
    prepare_archive_v2_input,
    run_prepared_archive_v2,
)
from nexus_xau.research.minimal_v2_0700 import (
    build_minimal_v2,
    build_minimal_v2_from_frame,
)


def _plain_m1(
    *,
    periods: int = 20,
    start: str = "2026-08-01T00:00:00Z",
) -> pd.DataFrame:
    index = pd.date_range(start, periods=periods, freq="1min")
    base = pd.Series(range(periods), index=index, dtype=float) / 100.0 + 100.0
    return pd.DataFrame(
        {
            "open": base,
            "high": base + 0.2,
            "low": base - 0.2,
            "close": base + 0.05,
        },
        index=index,
    )


def _archive_m1(*, periods: int = 20) -> pd.DataFrame:
    frame = _plain_m1(periods=periods)
    frame["archive_tick_count"] = 3
    frame["source_year"] = 2026
    frame["source_month"] = 8
    frame["source_sha256"] = "abc123"
    frame["source_local_path"] = "archive.zip"
    frame["source_validator_version"] = VALIDATOR_VERSION
    frame["first_raw_ordinal"] = range(0, periods * 3, 3)
    frame["last_raw_ordinal"] = range(2, periods * 3 + 2, 3)
    frame["bar_representation"] = BAR_REPRESENTATION
    return frame


def _source_months() -> tuple[ArchiveMonthProvenance, ...]:
    return (
        ArchiveMonthProvenance(
            symbol="XAUUSDm",
            year=2026,
            month=8,
            local_path="archive.zip",
            sha256="abc123",
            actual_size=123,
            validator_version=VALIDATOR_VERSION,
        ),
    )


def _prepare(
    archive_m1: pd.DataFrame,
    *,
    window_status: str = WINDOW_STATUS_OK,
):
    return prepare_archive_v2_input(
        archive_m1=archive_m1,
        symbol="XAUUSDm",
        requested_start="2026-08-01T00:00:00Z",
        requested_end="2026-08-01T04:00:00Z",
        window_status=window_status,
        continuity_status=CONTINUITY_STATUS,
        source_months=_source_months(),
    )


def test_file_and_frame_v2_entry_points_are_behaviorally_identical(
    tmp_path: Path,
) -> None:
    frame = _plain_m1()
    path = tmp_path / "m1.csv"
    exported = frame.reset_index(names="timestamp")
    exported.to_csv(path, index=False)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()

    file_days, file_origins, file_events, file_report = build_minimal_v2(
        m1_path=path
    )
    loaded = load_ohlc_csv(path)
    frame_days, frame_origins, frame_events, frame_report = (
        build_minimal_v2_from_frame(
            m1=loaded,
            source_descriptor=str(path),
            source_sha256=digest,
        )
    )

    pd.testing.assert_frame_equal(file_days, frame_days)
    pd.testing.assert_frame_equal(file_origins, frame_origins)
    pd.testing.assert_frame_equal(file_events, frame_events)
    assert file_report == frame_report


def test_prepare_preserves_archive_input_and_derives_only_m5_h4() -> None:
    archive_m1 = _archive_m1()
    before = archive_m1.copy(deep=True)
    prepared = _prepare(archive_m1)

    pd.testing.assert_frame_equal(archive_m1, before)
    direct = archive_m1[["open", "high", "low", "close"]]
    pd.testing.assert_frame_equal(prepared.m5, resample_ohlc(direct, "M5"))
    pd.testing.assert_frame_equal(prepared.h4, resample_ohlc(direct, "H4"))
    assert prepared.envelope["derived_timeframes"] == ["M5", "H4"]
    assert "H1" not in prepared.envelope["derived_timeframes"]
    assert "D1" not in prepared.envelope["derived_timeframes"]


def test_unseeded_real_window_fails_closed_before_v2_state() -> None:
    prepared = _prepare(_archive_m1())
    with pytest.raises(ArchiveV2IntegrationError) as exc:
        run_prepared_archive_v2(
            prepared,
            seed_status=SEED_UNSEEDED_REAL_WINDOW,
        )
    assert exc.value.code == DATA_EXCLUDED_ORIGIN_HISTORY_UNSEEDED


def test_continuation_checkpoint_is_explicitly_not_implemented() -> None:
    prepared = _prepare(_archive_m1())
    with pytest.raises(ArchiveV2IntegrationError) as exc:
        run_prepared_archive_v2(
            prepared,
            seed_status=SEED_CONTINUATION_CHECKPOINT,
        )
    assert exc.value.code == DATA_EXCLUDED_CONTINUATION_CHECKPOINT_NOT_IMPLEMENTED


def test_synthetic_complete_runs_v2_and_marks_outputs() -> None:
    prepared = _prepare(_archive_m1())
    result = run_prepared_archive_v2(
        prepared,
        seed_status=SEED_SYNTHETIC_COMPLETE,
    )

    assert result.report["integration_seed_status"] == SEED_SYNTHETIC_COMPLETE
    assert result.report["integration_envelope"]["source_family"] == SOURCE_FAMILY
    assert result.report["integration_envelope"]["contract"] == INTEGRATION_CONTRACT
    assert result.report["economic_scoring"] == "DISABLED"
    assert result.report["broker_fill_claim"] == "DISABLED"

    assert not result.days.empty
    assert set(result.days["integration_seed_status"]) == {
        SEED_SYNTHETIC_COMPLETE
    }
    assert set(result.days["integration_representation"]) == {
        BAR_REPRESENTATION
    }


def test_no_tick_window_fails_closed() -> None:
    archive_m1 = _archive_m1().iloc[0:0].copy()
    with pytest.raises(ArchiveV2IntegrationError) as exc:
        _prepare(archive_m1, window_status=WINDOW_STATUS_NO_TICKS)
    assert exc.value.code == DATA_EXCLUDED_ARCHIVE_WINDOW_EMPTY


def test_wrong_archive_m1_representation_is_rejected() -> None:
    archive_m1 = _archive_m1()
    archive_m1["bar_representation"] = "OTHER"
    with pytest.raises(ArchiveV2IntegrationError) as exc:
        _prepare(archive_m1)
    assert exc.value.code == DATA_EXCLUDED_ARCHIVE_REPRESENTATION_MISMATCH


def test_integration_envelope_preserves_source_month_and_sha() -> None:
    prepared = _prepare(_archive_m1())
    months = prepared.envelope["source_months"]
    assert len(months) == 1
    assert months[0]["year"] == 2026
    assert months[0]["month"] == 8
    assert months[0]["sha256"] == "abc123"
    assert prepared.envelope["source_sha256"] == ["abc123"]
    assert prepared.envelope["source_validator_versions"] == [VALIDATOR_VERSION]


def test_integration_does_not_add_economic_outcome_fields() -> None:
    prepared = _prepare(_archive_m1())
    result = run_prepared_archive_v2(
        prepared,
        seed_status=SEED_SYNTHETIC_COMPLETE,
    )
    forbidden = {"pnl", "win_rate", "expectancy", "profit"}
    assert forbidden.isdisjoint(result.days.columns)
    assert forbidden.isdisjoint(result.origins.columns)
    assert forbidden.isdisjoint(result.events.columns)


def test_unaligned_integration_boundary_is_rejected() -> None:
    archive_m1 = _archive_m1()
    with pytest.raises(ArchiveV2IntegrationError) as exc:
        prepare_archive_v2_input(
            archive_m1=archive_m1,
            symbol="XAUUSDm",
            requested_start="2026-08-01T00:01:00Z",
            requested_end="2026-08-01T04:00:00Z",
            window_status=WINDOW_STATUS_OK,
            continuity_status=CONTINUITY_STATUS,
            source_months=_source_months(),
        )
    assert exc.value.code == DATA_EXCLUDED_INTEGRATION_BOUNDARY_UNALIGNED


def test_archive_m1_rows_outside_requested_window_are_rejected() -> None:
    archive_m1 = _archive_m1()
    shifted = archive_m1.copy()
    shifted.index = shifted.index + pd.Timedelta(hours=4)
    with pytest.raises(ArchiveV2IntegrationError) as exc:
        _prepare(shifted)
    assert exc.value.code == DATA_EXCLUDED_ARCHIVE_WINDOW_MISMATCH


def test_observed_m1_provenance_must_be_covered_by_source_envelope() -> None:
    archive_m1 = _archive_m1()
    archive_m1["source_sha256"] = "not-in-envelope"
    with pytest.raises(ArchiveV2IntegrationError) as exc:
        _prepare(archive_m1)
    assert exc.value.code == DATA_EXCLUDED_ARCHIVE_PROVENANCE_MISMATCH


def test_missing_m1_provenance_column_is_rejected() -> None:
    archive_m1 = _archive_m1().drop(columns=["source_sha256"])
    with pytest.raises(ArchiveV2IntegrationError) as exc:
        _prepare(archive_m1)
    assert exc.value.code == DATA_EXCLUDED_ARCHIVE_PROVENANCE_MISMATCH


def test_null_bar_representation_is_rejected() -> None:
    archive_m1 = _archive_m1()
    archive_m1.iloc[0, archive_m1.columns.get_loc("bar_representation")] = None
    with pytest.raises(ArchiveV2IntegrationError) as exc:
        _prepare(archive_m1)
    assert exc.value.code == DATA_EXCLUDED_ARCHIVE_REPRESENTATION_MISMATCH
