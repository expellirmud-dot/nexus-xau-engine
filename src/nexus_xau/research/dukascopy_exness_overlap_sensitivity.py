from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from typing import Literal

import pandas as pd

from nexus_xau.data.csv_loader import load_ohlc_csv
from nexus_xau.data.resample import resample_ohlc
from nexus_xau.replay.archive_window import ArchiveWindowError, load_archive_tick_window
from nexus_xau.replay.tick_bars import build_archive_bid_m1
from nexus_xau.research.minimal_v2_0700 import (
    H4Origin,
    _normalize_m1_frame,
    build_h4_origins,
    detect_pat2_full_range,
    origin_state_at,
)

CONTRACT = "PHASE1_DUKASCOPY_EXNESS_OVERLAP_SENSITIVITY_V0.2"
DUKASCOPY_SOURCE = "DUKASCOPY_BID_M1"
EXNESS_SOURCE = "EXNESS_BRANDED_ARCHIVE"

EXACT_OBSERVED_STATE_EQUIVALENCE = "EXACT_OBSERVED_STATE_EQUIVALENCE"
STRUCTURAL_STATE_EQUIVALENCE_NUMERIC_DIVERGENCE = (
    "STRUCTURAL_STATE_EQUIVALENCE_NUMERIC_DIVERGENCE"
)
STATE_DIVERGENCE_OBSERVED = "STATE_DIVERGENCE_OBSERVED"
INCOMPARABLE_INPUT_GAP = "INCOMPARABLE_INPUT_GAP"

Classification = Literal[
    "EXACT_OBSERVED_STATE_EQUIVALENCE",
    "STRUCTURAL_STATE_EQUIVALENCE_NUMERIC_DIVERGENCE",
    "STATE_DIVERGENCE_OBSERVED",
    "INCOMPARABLE_INPUT_GAP",
]


class OverlapSensitivityError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code


@dataclass(frozen=True, slots=True)
class FrozenWindow:
    window_id: str
    start: str
    end: str
    dukascopy_csv: str
    dukascopy_meta: str


FROZEN_WINDOWS = (
    FrozenWindow(
        "W2022_09",
        "2022-09-01T00:00:00Z",
        "2022-10-01T00:00:00Z",
        "data/raw/dukascopy/chunks/XAUUSD_M1_BID_2022-09-01_2023-03-31.csv",
        "data/raw/dukascopy/chunks/XAUUSD_M1_BID_2022-09-01_2023-03-31.csv.meta.json",
    ),
    FrozenWindow(
        "W2023_09",
        "2023-09-01T00:00:00Z",
        "2023-10-01T00:00:00Z",
        "data/raw/dukascopy/chunks/XAUUSD_M1_BID_2023-09-01_2023-11-30.csv",
        "data/raw/dukascopy/chunks/XAUUSD_M1_BID_2023-09-01_2023-11-30.csv.meta.json",
    ),
    FrozenWindow(
        "W2026_08_24",
        "2026-08-24T00:00:00Z",
        "2026-08-25T00:00:00Z",
        "data/raw/dukascopy/XAUUSD_M1_BID_2026-08-24.csv",
        "data/raw/dukascopy/XAUUSD_M1_BID_2026-08-24.csv.meta.json",
    ),
)

def _utc(value: pd.Timestamp | str) -> pd.Timestamp:
    timestamp = pd.Timestamp(value)
    if timestamp.tz is None:
        raise ValueError("Timestamp must be timezone-aware")
    return timestamp.tz_convert("UTC")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _iso(value: pd.Timestamp | None) -> str | None:
    return None if value is None else value.isoformat()


def _event_key(side: str, known_at: pd.Timestamp) -> str:
    return f"{side}|{known_at.isoformat()}"


def _origin_key(origin: H4Origin) -> str:
    return f"{origin.side}|{origin.origin_known_at.isoformat()}"


def _require_source_identity(
    provenance: dict[str, object], *, expected_source: str
) -> None:
    observed = provenance.get("source_family")
    if observed != expected_source:
        raise OverlapSensitivityError(
            "SOURCE_PROVENANCE_MISMATCH",
            f"expected {expected_source}, got {observed}",
        )


def _normalize_window_frame(
    frame: pd.DataFrame, *, start: pd.Timestamp, end: pd.Timestamp
) -> pd.DataFrame:
    normalized = _normalize_m1_frame(frame)
    if bool((normalized.index < start).any()) or bool((normalized.index >= end).any()):
        raise OverlapSensitivityError(
            "WINDOW_MISMATCH",
            "source M1 contains rows outside the frozen half-open window",
        )
    return normalized


def _active_m1(
    frame: pd.DataFrame, *, require_volume: bool = False
) -> tuple[pd.DataFrame, dict[str, int]]:
    raw_rows = len(frame)
    if "volume" not in frame.columns:
        if require_volume:
            raise OverlapSensitivityError(
                "DUKASCOPY_VOLUME_REQUIRED",
                "frozen Dukascopy input must preserve volume for V0.2 active-M1 normalization",
            )
        active = frame.copy()
        excluded = 0
    else:
        mask = frame["volume"] > 0
        active = frame.loc[mask].copy()
        excluded = int((~mask).sum())
    return active, {
        "raw_rows": raw_rows,
        "active_rows": len(active),
        "excluded_nonpositive_volume_rows": excluded,
    }


def _difference_stats(
    left: pd.Series, right: pd.Series
) -> dict[str, float | int | None]:
    if len(left) != len(right):
        raise ValueError("difference series must have equal length")
    if left.empty:
        return {
            "count": 0,
            "median_signed_exness_minus_dukascopy": None,
            "median_absolute": None,
            "p95_absolute": None,
            "max_absolute": None,
        }
    signed = right.to_numpy(dtype=float) - left.to_numpy(dtype=float)
    absolute = abs(signed)
    return {
        "count": len(signed),
        "median_signed_exness_minus_dukascopy": float(pd.Series(signed).median()),
        "median_absolute": float(pd.Series(absolute).median()),
        "p95_absolute": float(pd.Series(absolute).quantile(0.95)),
        "max_absolute": float(pd.Series(absolute).max()),
    }


def _ohlc_difference_stats(
    dukascopy: pd.DataFrame, exness: pd.DataFrame, common: pd.DatetimeIndex
) -> dict[str, dict[str, float | int | None]]:
    return {
        column: _difference_stats(
            dukascopy.loc[common, column],
            exness.loc[common, column],
        )
        for column in ("open", "high", "low", "close")
    }

def _derive_h4_representation(
    frame: pd.DataFrame, *, start: pd.Timestamp, end: pd.Timestamp
) -> tuple[pd.DataFrame, dict[str, object], dict[str, H4Origin]]:
    h4 = resample_ohlc(frame, "H4")
    events = [
        event
        for event in detect_pat2_full_range(h4, "H4")
        if start < event.known_at <= end
    ]
    origins = [
        origin
        for origin in build_h4_origins(h4, events)
        if start <= origin.origin_known_at < end
    ]
    event_map = {
        _event_key(event.side, event.known_at): {
            "side": event.side,
            "known_at": event.known_at.isoformat(),
            "previous_bar_start": event.previous_bar_start.isoformat(),
            "pattern_bar_start": event.pattern_bar_start.isoformat(),
            "close": event.close,
            "pattern_low": event.pattern_low,
            "pattern_high": event.pattern_high,
        }
        for event in events
    }
    origin_map = {_origin_key(origin): origin for origin in origins}
    return h4, event_map, origin_map


def _origin_state_payload(
    frame: pd.DataFrame, *, origin: H4Origin, end: pd.Timestamp
) -> dict[str, object]:
    state, consumed, remaining, touch = origin_state_at(
        active_m1=frame, origin=origin, at=end
    )
    return {
        "state": state,
        "consumed_points": consumed,
        "remaining_points": remaining,
        "point_check_touch_at": _iso(touch),
    }


def _sorted_only(left: set[str], right: set[str]) -> tuple[list[str], list[str], list[str]]:
    return sorted(left - right), sorted(right - left), sorted(left & right)


def compare_overlap_frames(
    *,
    dukascopy_m1: pd.DataFrame,
    exness_m1: pd.DataFrame,
    start: pd.Timestamp | str,
    end: pd.Timestamp | str,
    dukascopy_provenance: dict[str, object],
    exness_provenance: dict[str, object],
    window_id: str,
) -> dict[str, object]:
    """Compare frozen V2 representations across two independently sourced M1 frames."""
    start_ts = _utc(start)
    end_ts = _utc(end)
    if end_ts <= start_ts:
        raise ValueError("end must be strictly greater than start")
    _require_source_identity(dukascopy_provenance, expected_source=DUKASCOPY_SOURCE)
    _require_source_identity(exness_provenance, expected_source=EXNESS_SOURCE)
    if dukascopy_provenance["source_family"] == exness_provenance["source_family"]:
        raise OverlapSensitivityError(
            "SOURCE_PROVENANCE_COLLAPSE",
            "source families must remain distinct",
        )

    duk_raw = _normalize_window_frame(dukascopy_m1, start=start_ts, end=end_ts)
    exn_raw = _normalize_window_frame(exness_m1, start=start_ts, end=end_ts)
    if duk_raw.empty or exn_raw.empty:
        return _incomparable_report(
            window_id=window_id,
            start=start_ts,
            end=end_ts,
            dukascopy_provenance=dukascopy_provenance,
            exness_provenance=exness_provenance,
            reason="EMPTY_SOURCE_FRAME",
        )

    duk, duk_counts = _active_m1(duk_raw)
    exn, exn_counts = _active_m1(exn_raw)
    if duk.empty or exn.empty:
        return _incomparable_report(
            window_id=window_id,
            start=start_ts,
            end=end_ts,
            dukascopy_provenance=dukascopy_provenance,
            exness_provenance=exness_provenance,
            reason="EMPTY_ACTIVE_SOURCE_FRAME",
        )

    common_m1 = duk.index.intersection(exn.index)
    duk_only_m1 = duk.index.difference(exn.index)
    exn_only_m1 = exn.index.difference(duk.index)
    duk_h4, duk_events, duk_origins = _derive_h4_representation(
        duk, start=start_ts, end=end_ts
    )
    exn_h4, exn_events, exn_origins = _derive_h4_representation(
        exn, start=start_ts, end=end_ts
    )
    common_h4 = duk_h4.index.intersection(exn_h4.index)
    duk_only_h4 = duk_h4.index.difference(exn_h4.index)
    exn_only_h4 = exn_h4.index.difference(duk_h4.index)

    event_keys_duk = set(duk_events)
    event_keys_exn = set(exn_events)
    event_only_duk, event_only_exn, event_common = _sorted_only(
        event_keys_duk, event_keys_exn
    )
    origin_keys_duk = set(duk_origins)
    origin_keys_exn = set(exn_origins)
    origin_only_duk, origin_only_exn, origin_common = _sorted_only(
        origin_keys_duk, origin_keys_exn
    )
    matched_origins: list[dict[str, object]] = []
    all_states_equal = True
    all_numeric_equal = True
    for key in origin_common:
        duk_origin = duk_origins[key]
        exn_origin = exn_origins[key]
        duk_state = _origin_state_payload(duk, origin=duk_origin, end=end_ts)
        exn_state = _origin_state_payload(exn, origin=exn_origin, end=end_ts)
        state_equal = duk_state["state"] == exn_state["state"]
        anchor_equal = duk_origin.anchor_price == exn_origin.anchor_price
        consumed_equal = (
            duk_state["consumed_points"] == exn_state["consumed_points"]
        )
        touch_equal = (
            duk_state["point_check_touch_at"] == exn_state["point_check_touch_at"]
        )
        all_states_equal = all_states_equal and state_equal
        all_numeric_equal = (
            all_numeric_equal and anchor_equal and consumed_equal and touch_equal
        )
        matched_origins.append(
            {
                "origin_key": key,
                "dukascopy_anchor_price": duk_origin.anchor_price,
                "exness_anchor_price": exn_origin.anchor_price,
                "anchor_difference_exness_minus_dukascopy": (
                    exn_origin.anchor_price - duk_origin.anchor_price
                ),
                "anchor_exact_equal": anchor_equal,
                "dukascopy_state": duk_state["state"],
                "exness_state": exn_state["state"],
                "state_exact_equal": state_equal,
                "dukascopy_consumed_points": duk_state["consumed_points"],
                "exness_consumed_points": exn_state["consumed_points"],
                "consumed_difference_exness_minus_dukascopy": (
                    float(exn_state["consumed_points"])
                    - float(duk_state["consumed_points"])
                ),
                "consumed_exact_equal": consumed_equal,
                "dukascopy_point_check_touch_at": duk_state["point_check_touch_at"],
                "exness_point_check_touch_at": exn_state["point_check_touch_at"],
                "touch_exact_equal": touch_equal,
            }
        )

    structural_equal = (
        event_keys_duk == event_keys_exn
        and origin_keys_duk == origin_keys_exn
        and all_states_equal
    )
    if not structural_equal:
        classification: Classification = STATE_DIVERGENCE_OBSERVED
    elif all_numeric_equal:
        classification = EXACT_OBSERVED_STATE_EQUIVALENCE
    else:
        classification = STRUCTURAL_STATE_EQUIVALENCE_NUMERIC_DIVERGENCE

    report: dict[str, object] = {
        "contract": CONTRACT,
        "window_id": window_id,
        "window_start_utc": start_ts.isoformat(),
        "window_end_utc": end_ts.isoformat(),
        "classification": classification,
        "source_provenance": {
            "dukascopy": dict(dukascopy_provenance),
            "exness": dict(exness_provenance),
        },
        "m1": {
            "dukascopy_rows": len(duk),
            "exness_rows": len(exn),
            "dukascopy_raw_rows": duk_counts["raw_rows"],
            "dukascopy_active_rows": duk_counts["active_rows"],
            "dukascopy_excluded_nonpositive_volume_rows": duk_counts[
                "excluded_nonpositive_volume_rows"
            ],
            "exness_raw_rows": exn_counts["raw_rows"],
            "exness_active_rows": exn_counts["active_rows"],
            "exness_excluded_nonpositive_volume_rows": exn_counts[
                "excluded_nonpositive_volume_rows"
            ],
            "common_timestamp_count": len(common_m1),
            "dukascopy_only_timestamp_count": len(duk_only_m1),
            "exness_only_timestamp_count": len(exn_only_m1),
            "ohlc_difference_stats_on_common_timestamps": _ohlc_difference_stats(
                duk, exn, common_m1
            ),
        },
        "h4": {
            "dukascopy_rows": len(duk_h4),
            "exness_rows": len(exn_h4),
            "common_timestamp_count": len(common_h4),
            "dukascopy_only_timestamps": [ts.isoformat() for ts in duk_only_h4],
            "exness_only_timestamps": [ts.isoformat() for ts in exn_only_h4],
            "ohlc_difference_stats_on_common_timestamps": _ohlc_difference_stats(
                duk_h4, exn_h4, common_h4
            ),
        },
        "pat_h4": {
            "dukascopy_count": len(duk_events),
            "exness_count": len(exn_events),
            "dukascopy_only_keys": event_only_duk,
            "exness_only_keys": event_only_exn,
            "common_keys": event_common,
        },
        "origins": {
            "dukascopy_count": len(duk_origins),
            "exness_count": len(exn_origins),
            "dukascopy_only_keys": origin_only_duk,
            "exness_only_keys": origin_only_exn,
            "common_keys": origin_common,
            "matched": matched_origins,
        },
        "guards": {
            "economic_scoring": "DISABLED",
            "holdout_scoring": "DISABLED",
            "order_send": "DISABLED",
            "source_merge": "FORBIDDEN",
        },
    }
    return report

def _incomparable_report(
    *,
    window_id: str,
    start: pd.Timestamp,
    end: pd.Timestamp,
    dukascopy_provenance: dict[str, object] | None,
    exness_provenance: dict[str, object] | None,
    reason: str,
    error_code: str | None = None,
) -> dict[str, object]:
    return {
        "contract": CONTRACT,
        "window_id": window_id,
        "window_start_utc": start.isoformat(),
        "window_end_utc": end.isoformat(),
        "classification": INCOMPARABLE_INPUT_GAP,
        "incomparable_reason": reason,
        "error_code": error_code,
        "source_provenance": {
            "dukascopy": dict(dukascopy_provenance or {}),
            "exness": dict(exness_provenance or {}),
        },
        "guards": {
            "economic_scoring": "DISABLED",
            "holdout_scoring": "DISABLED",
            "order_send": "DISABLED",
            "source_merge": "FORBIDDEN",
        },
    }


def _metadata_missing_dates_in_window(
    metadata: dict[str, object], *, start: pd.Timestamp, end: pd.Timestamp
) -> list[str]:
    candidates: list[str] = []
    for key in ("missing_cache_dates", "failed_dates"):
        raw = metadata.get(key, [])
        if isinstance(raw, list):
            candidates.extend(str(value) for value in raw)
    missing: list[str] = []
    for value in candidates:
        day = pd.Timestamp(value).date()
        if start.date() <= day <= (end - timedelta(microseconds=1)).date():
            missing.append(value)
    return sorted(set(missing))


def load_dukascopy_window(
    *,
    repo_root: Path,
    csv_path: str,
    metadata_path: str,
    start: pd.Timestamp | str,
    end: pd.Timestamp | str,
) -> tuple[pd.DataFrame, dict[str, object]]:
    start_ts = _utc(start)
    end_ts = _utc(end)
    source = repo_root / csv_path
    meta_source = repo_root / metadata_path
    if not source.is_file() or not meta_source.is_file():
        raise OverlapSensitivityError(
            "DUKASCOPY_INPUT_MISSING",
            f"missing Dukascopy input or metadata: {source} / {meta_source}",
        )
    metadata = json.loads(meta_source.read_text(encoding="utf-8"))
    if metadata.get("symbol") != "XAUUSD" or str(metadata.get("side")).upper() != "BID":
        raise OverlapSensitivityError(
            "DUKASCOPY_PROVENANCE_MISMATCH",
            "expected XAUUSD BID Dukascopy metadata",
        )
    expected_sha = metadata.get("sha256")
    actual_sha = _sha256(source)
    if expected_sha is not None and str(expected_sha) != actual_sha:
        raise OverlapSensitivityError(
            "DUKASCOPY_DIGEST_MISMATCH",
            "Dukascopy CSV SHA-256 differs from metadata",
        )
    missing_dates = _metadata_missing_dates_in_window(
        metadata, start=start_ts, end=end_ts
    )
    if missing_dates:
        raise OverlapSensitivityError(
            "DUKASCOPY_INPUT_GAP",
            f"Dukascopy metadata records missing acquisition dates: {missing_dates}",
        )

    frame = load_ohlc_csv(source)
    if "volume" not in frame.columns:
        raise OverlapSensitivityError(
            "DUKASCOPY_VOLUME_REQUIRED",
            "frozen Dukascopy input must include volume for V0.2 active-M1 normalization",
        )
    frame = frame.loc[(frame.index >= start_ts) & (frame.index < end_ts)].copy()
    provenance: dict[str, object] = {
        "source_family": DUKASCOPY_SOURCE,
        "symbol": "XAUUSD",
        "side": "BID",
        "csv_path": csv_path,
        "metadata_path": metadata_path,
        "sha256": actual_sha,
        "active_m1_rule": "volume>0",
    }
    return frame, provenance

def load_exness_window(
    *,
    repo_root: Path,
    start: pd.Timestamp | str,
    end: pd.Timestamp | str,
) -> tuple[pd.DataFrame, dict[str, object]]:
    start_ts = _utc(start)
    end_ts = _utc(end)
    manifest_path = repo_root / "results/exness_tick_archive/download_validation_manifest.jsonl"
    gap_ledger_path = repo_root / "docs/PHASE1_EXNESS_ARCHIVE_GAP_LEDGER_V0.1.json"
    window = load_archive_tick_window(
        repo_root=repo_root,
        manifest_path=manifest_path,
        gap_ledger_path=gap_ledger_path,
        symbol="XAUUSDm",
        start=start_ts,
        end=end_ts,
    )
    m1 = build_archive_bid_m1(
        window.frame,
        requested_start=start_ts,
        requested_end=end_ts,
    )
    provenance: dict[str, object] = {
        "source_family": EXNESS_SOURCE,
        "symbol": "XAUUSDm",
        "side": "BID",
        "manifest_path": str(manifest_path.relative_to(repo_root)),
        "gap_ledger_path": str(gap_ledger_path.relative_to(repo_root)),
        "continuity_status": window.continuity_status,
        "window_status": window.status,
        "active_m1_rule": "all_observed_tick_derived_m1",
        "source_months": [
            {
                "year": month.year,
                "month": month.month,
                "local_path": month.local_path,
                "sha256": month.sha256,
                "validator_version": month.validator_version,
            }
            for month in window.source_months
        ],
    }
    core = m1[["open", "high", "low", "close"]].copy()
    return core, provenance


def frozen_window(window_id: str) -> FrozenWindow:
    matches = [window for window in FROZEN_WINDOWS if window.window_id == window_id]
    if len(matches) != 1:
        raise ValueError(f"unknown frozen window_id: {window_id}")
    return matches[0]


def run_frozen_window(*, repo_root: Path, window_id: str) -> dict[str, object]:
    window = frozen_window(window_id)
    start = _utc(window.start)
    end = _utc(window.end)
    duk_provenance: dict[str, object] | None = None
    exn_provenance: dict[str, object] | None = None
    try:
        duk, duk_provenance = load_dukascopy_window(
            repo_root=repo_root,
            csv_path=window.dukascopy_csv,
            metadata_path=window.dukascopy_meta,
            start=start,
            end=end,
        )
        exn, exn_provenance = load_exness_window(
            repo_root=repo_root,
            start=start,
            end=end,
        )
    except (OverlapSensitivityError, ArchiveWindowError, ValueError) as exc:
        error_code = getattr(exc, "code", type(exc).__name__)
        return _incomparable_report(
            window_id=window_id,
            start=start,
            end=end,
            dukascopy_provenance=duk_provenance,
            exness_provenance=exn_provenance,
            reason=str(exc),
            error_code=str(error_code),
        )
    return compare_overlap_frames(
        dukascopy_m1=duk,
        exness_m1=exn,
        start=start,
        end=end,
        dukascopy_provenance=duk_provenance,
        exness_provenance=exn_provenance,
        window_id=window_id,
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run frozen Dukascopy/Exness V2 representation-sensitivity windows."
    )
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument(
        "--window",
        choices=[window.window_id for window in FROZEN_WINDOWS],
        required=True,
    )
    parser.add_argument("--out", type=Path, required=True)
    return parser


def main() -> int:
    args = _parser().parse_args()
    report = run_frozen_window(
        repo_root=args.repo_root.resolve(),
        window_id=args.window,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())