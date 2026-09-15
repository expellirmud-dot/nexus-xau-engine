from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Literal

import pandas as pd

from nexus_xau.data.resample import resample_ohlc
from nexus_xau.replay.archive_window import (
    WINDOW_STATUS_NO_TICKS,
    WINDOW_STATUS_OK,
    ArchiveMonthProvenance,
)
from nexus_xau.replay.tick_bars import BAR_REPRESENTATION
from nexus_xau.research.minimal_v2_0700 import build_minimal_v2_from_frame

INTEGRATION_CONTRACT = "PHASE1_ARCHIVE_V2_INTEGRATION_V0.2"
SOURCE_FAMILY = "EXNESS_BRANDED_ARCHIVE"

SEED_SYNTHETIC_COMPLETE = "SYNTHETIC_COMPLETE"
SEED_CONTINUATION_CHECKPOINT = "CONTINUATION_CHECKPOINT"
SEED_UNSEEDED_REAL_WINDOW = "UNSEEDED_REAL_WINDOW"

DATA_EXCLUDED_ORIGIN_HISTORY_UNSEEDED = "DATA_EXCLUDED_ORIGIN_HISTORY_UNSEEDED"
DATA_EXCLUDED_CONTINUATION_CHECKPOINT_NOT_IMPLEMENTED = (
    "DATA_EXCLUDED_CONTINUATION_CHECKPOINT_NOT_IMPLEMENTED"
)
DATA_EXCLUDED_ARCHIVE_WINDOW_EMPTY = "DATA_EXCLUDED_ARCHIVE_WINDOW_EMPTY"
DATA_EXCLUDED_ARCHIVE_REPRESENTATION_MISMATCH = (
    "DATA_EXCLUDED_ARCHIVE_REPRESENTATION_MISMATCH"
)
DATA_EXCLUDED_INTEGRATION_BOUNDARY_UNALIGNED = (
    "DATA_EXCLUDED_INTEGRATION_BOUNDARY_UNALIGNED"
)
DATA_EXCLUDED_ARCHIVE_WINDOW_MISMATCH = "DATA_EXCLUDED_ARCHIVE_WINDOW_MISMATCH"
DATA_EXCLUDED_ARCHIVE_PROVENANCE_MISMATCH = (
    "DATA_EXCLUDED_ARCHIVE_PROVENANCE_MISMATCH"
)

SeedStatus = Literal[
    "SYNTHETIC_COMPLETE",
    "CONTINUATION_CHECKPOINT",
    "UNSEEDED_REAL_WINDOW",
]


class ArchiveV2IntegrationError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code


@dataclass(frozen=True, slots=True)
class PreparedArchiveV2Input:
    archive_m1: pd.DataFrame
    m5: pd.DataFrame
    h4: pd.DataFrame
    envelope: dict[str, object]


@dataclass(frozen=True, slots=True)
class ArchiveV2IntegrationResult:
    days: pd.DataFrame
    origins: pd.DataFrame
    events: pd.DataFrame
    report: dict[str, object]
    prepared: PreparedArchiveV2Input


def _utc(value: pd.Timestamp | str) -> pd.Timestamp:
    timestamp = pd.Timestamp(value)
    if timestamp.tz is None:
        raise ValueError("Timestamp must be timezone-aware")
    return timestamp.tz_convert("UTC")


def _require_h4_boundary(timestamp: pd.Timestamp, *, name: str) -> None:
    if (
        timestamp.minute != 0
        or timestamp.second != 0
        or timestamp.microsecond != 0
        or timestamp.nanosecond != 0
        or timestamp.hour % 4 != 0
    ):
        raise ArchiveV2IntegrationError(
            DATA_EXCLUDED_INTEGRATION_BOUNDARY_UNALIGNED,
            f"{name} must be an exact 4-hour UTC boundary",
        )


def _source_month_payload(
    source_months: tuple[ArchiveMonthProvenance, ...],
) -> list[dict[str, object]]:
    return [
        {
            "symbol": month.symbol,
            "year": month.year,
            "month": month.month,
            "local_path": month.local_path,
            "sha256": month.sha256,
            "actual_size": month.actual_size,
            "validator_version": month.validator_version,
        }
        for month in source_months
    ]


def prepare_archive_v2_input(
    *,
    archive_m1: pd.DataFrame,
    symbol: str,
    requested_start: pd.Timestamp | str,
    requested_end: pd.Timestamp | str,
    window_status: str,
    continuity_status: str,
    source_months: tuple[ArchiveMonthProvenance, ...],
) -> PreparedArchiveV2Input:
    """Prepare archive-derived M1 plus frozen V2 M5/H4 engineering inputs."""

    if window_status == WINDOW_STATUS_NO_TICKS or archive_m1.empty:
        raise ArchiveV2IntegrationError(
            DATA_EXCLUDED_ARCHIVE_WINDOW_EMPTY,
            "archive window contains no observed ticks/M1 bars",
        )
    if window_status != WINDOW_STATUS_OK:
        raise ArchiveV2IntegrationError(
            DATA_EXCLUDED_ARCHIVE_WINDOW_EMPTY,
            f"archive window status is not eligible: {window_status}",
        )

    start = _utc(requested_start)
    end = _utc(requested_end)
    if end <= start:
        raise ValueError("requested_end must be strictly greater than requested_start")
    _require_h4_boundary(start, name="requested_start")
    _require_h4_boundary(end, name="requested_end")

    if not isinstance(archive_m1.index, pd.DatetimeIndex) or archive_m1.index.tz is None:
        raise ValueError("archive M1 index must be timezone-aware")
    normalized_index = archive_m1.index.tz_convert("UTC")
    if (normalized_index < start).any() or (normalized_index >= end).any():
        raise ArchiveV2IntegrationError(
            DATA_EXCLUDED_ARCHIVE_WINDOW_MISMATCH,
            "archive M1 contains rows outside requested half-open window",
        )

    if "bar_representation" not in archive_m1.columns:
        raise ArchiveV2IntegrationError(
            DATA_EXCLUDED_ARCHIVE_REPRESENTATION_MISMATCH,
            "archive M1 lacks bar_representation",
        )
    representation = archive_m1["bar_representation"]
    if representation.isna().any() or not bool((representation == BAR_REPRESENTATION).all()):
        representations = sorted(set(representation.dropna().astype(str)))
        raise ArchiveV2IntegrationError(
            DATA_EXCLUDED_ARCHIVE_REPRESENTATION_MISMATCH,
            f"unexpected M1 representation(s): {representations}",
        )

    required_provenance = {"source_year", "source_month", "source_sha256"}
    missing_provenance = required_provenance - set(archive_m1.columns)
    if missing_provenance:
        raise ArchiveV2IntegrationError(
            DATA_EXCLUDED_ARCHIVE_PROVENANCE_MISMATCH,
            f"archive M1 missing provenance columns: {sorted(missing_provenance)}",
        )
    envelope_keys = {
        (month.year, month.month, month.sha256) for month in source_months
    }
    observed_keys = {
        (int(year), int(month), str(sha))
        for year, month, sha in archive_m1[
            ["source_year", "source_month", "source_sha256"]
        ].itertuples(index=False, name=None)
    }
    if not observed_keys.issubset(envelope_keys):
        raise ArchiveV2IntegrationError(
            DATA_EXCLUDED_ARCHIVE_PROVENANCE_MISMATCH,
            "observed M1 month/SHA provenance is not covered by source_months",
        )

    archive_copy = archive_m1.copy(deep=True)
    core_m1 = archive_copy[["open", "high", "low", "close"]].copy()
    m5 = resample_ohlc(core_m1, "M5")
    h4 = resample_ohlc(core_m1, "H4")

    months = _source_month_payload(source_months)
    envelope: dict[str, object] = {
        "contract": INTEGRATION_CONTRACT,
        "source_family": SOURCE_FAMILY,
        "symbol": symbol,
        "requested_start_utc": start.isoformat(),
        "requested_end_utc": end.isoformat(),
        "window_status": window_status,
        "continuity_status": continuity_status,
        "m1_representation": BAR_REPRESENTATION,
        "derived_timeframes": ["M5", "H4"],
        "source_months": months,
        "source_sha256": [str(item["sha256"]) for item in months],
        "source_validator_versions": sorted(
            {str(item["validator_version"]) for item in months}
        ),
    }

    return PreparedArchiveV2Input(
        archive_m1=archive_copy,
        m5=m5,
        h4=h4,
        envelope=envelope,
    )


def _with_integration_markers(
    frame: pd.DataFrame,
    *,
    prepared: PreparedArchiveV2Input,
    seed_status: SeedStatus,
) -> pd.DataFrame:
    result = frame.copy(deep=True)
    if result.empty:
        return result
    envelope = prepared.envelope
    result["integration_source_family"] = SOURCE_FAMILY
    result["integration_representation"] = BAR_REPRESENTATION
    result["integration_seed_status"] = seed_status
    result["integration_contract"] = INTEGRATION_CONTRACT
    result["integration_continuity_status"] = str(envelope["continuity_status"])
    result["integration_window_start_utc"] = str(envelope["requested_start_utc"])
    result["integration_window_end_utc"] = str(envelope["requested_end_utc"])
    result["integration_source_month_count"] = len(envelope["source_months"])
    return result


def run_prepared_archive_v2(
    prepared: PreparedArchiveV2Input,
    *,
    seed_status: SeedStatus,
) -> ArchiveV2IntegrationResult:
    """Run frozen V2 only when origin-history completeness is explicitly allowed."""

    if seed_status == SEED_UNSEEDED_REAL_WINDOW:
        raise ArchiveV2IntegrationError(
            DATA_EXCLUDED_ORIGIN_HISTORY_UNSEEDED,
            "real archive window has no proven complete origin-history seed",
        )
    if seed_status == SEED_CONTINUATION_CHECKPOINT:
        raise ArchiveV2IntegrationError(
            DATA_EXCLUDED_CONTINUATION_CHECKPOINT_NOT_IMPLEMENTED,
            "continuation checkpoint semantics are not implemented in V0.1",
        )
    if seed_status != SEED_SYNTHETIC_COMPLETE:
        raise ValueError(f"unsupported seed_status: {seed_status}")

    source_descriptor = (
        f"{SOURCE_FAMILY}:{prepared.envelope['symbol']}:"
        f"{prepared.envelope['requested_start_utc']}.."
        f"{prepared.envelope['requested_end_utc']}"
    )
    core_m1 = prepared.archive_m1[["open", "high", "low", "close"]].copy()
    days, origins, events, report = build_minimal_v2_from_frame(
        m1=core_m1,
        source_descriptor=source_descriptor,
        source_metadata_descriptor=INTEGRATION_CONTRACT,
        source_sha256=None,
    )

    days = _with_integration_markers(
        days, prepared=prepared, seed_status=seed_status
    )
    origins = _with_integration_markers(
        origins, prepared=prepared, seed_status=seed_status
    )
    events = _with_integration_markers(
        events, prepared=prepared, seed_status=seed_status
    )

    integrated_report = dict(report)
    integrated_report["integration_envelope"] = dict(prepared.envelope)
    integrated_report["integration_seed_status"] = seed_status
    integrated_report["integration_source_months_json"] = json.dumps(
        prepared.envelope["source_months"],
        sort_keys=True,
        separators=(",", ":"),
    )
    integrated_report["economic_scoring"] = "DISABLED"
    integrated_report["broker_fill_claim"] = "DISABLED"

    return ArchiveV2IntegrationResult(
        days=days,
        origins=origins,
        events=events,
        report=integrated_report,
        prepared=prepared,
    )
