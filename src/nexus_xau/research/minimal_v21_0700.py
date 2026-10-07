from __future__ import annotations

from pathlib import Path

import pandas as pd

from nexus_xau.data.csv_loader import load_ohlc_csv
from nexus_xau.research.minimal_v2_0700 import (
    TARGET_MODE_FIXED_ORIGIN_V2_1,
    _build_minimal_v2_core,
    _load_metadata,
    _normalize_m1_frame,
    _sha256,
)


def build_minimal_v21_from_frame(
    *,
    m1: pd.DataFrame,
    source_descriptor: str,
    source_metadata_descriptor: str | None = None,
    source_sha256: str | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, object]]:
    """Run V2.1 with the source-reanchored fixed-origin candidate target."""

    frame = _normalize_m1_frame(m1)
    active_m1 = (
        frame[frame["volume"] > 0].copy()
        if "volume" in frame.columns
        else frame.copy()
    )
    if active_m1.empty:
        raise ValueError("no active M1 rows")

    return _build_minimal_v2_core(
        active_m1=active_m1,
        source_descriptor=source_descriptor,
        source_metadata_descriptor=source_metadata_descriptor,
        source_sha256=source_sha256,
        candidate_target_mode=TARGET_MODE_FIXED_ORIGIN_V2_1,
    )


def build_minimal_v21(
    *,
    m1_path: str | Path,
    metadata_path: str | Path | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, object]]:
    """File-based entry point for 0700_MINIMAL_V2.1_FIXED_ORIGIN_TARGET."""

    m1 = load_ohlc_csv(m1_path)
    metadata = _load_metadata(metadata_path)
    return build_minimal_v21_from_frame(
        m1=m1,
        source_descriptor=str(m1_path),
        source_metadata_descriptor=str(metadata_path) if metadata_path else None,
        source_sha256=metadata.get("sha256") or _sha256(m1_path),
    )
