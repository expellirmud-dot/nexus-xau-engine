from __future__ import annotations

import pandas as pd

from nexus_xau.research.remaining_run_state_relation_test import OriginRun
from nexus_xau.research.source_partial_reanchored_remaining_run import (
    _impact_label,
    _origin_destroyed_before,
    select_source_partial_origin,
)


def _m1_frame() -> pd.DataFrame:
    idx = pd.date_range("2026-01-01T00:00:00Z", periods=181, freq="min")
    lows = [100.5 if ts < pd.Timestamp("2026-01-01T01:00:00Z") else 104.5 for ts in idx]
    return pd.DataFrame(
        {
            "open": [105.0] * len(idx),
            "high": [106.0] * len(idx),
            "low": lows,
            "close": [105.5] * len(idx),
            "volume": [1.0] * len(idx),
        },
        index=idx,
    )


def test_reanchors_from_destroyed_newer_origin_to_older_valid_origin() -> None:
    m1 = _m1_frame()
    older = OriginRun(
        "BUY",
        pd.Timestamp("2025-12-31T23:00:00Z"),
        pd.Timestamp("2026-01-01T00:00:00Z"),
        100.0,
    )
    newer = OriginRun(
        "BUY",
        pd.Timestamp("2026-01-01T00:00:00Z"),
        pd.Timestamp("2026-01-01T01:00:00Z"),
        105.0,
    )

    selected = select_source_partial_origin(
        active_m1=m1,
        origins=[older, newer],
        side="BUY",
        cutoff_utc=pd.Timestamp("2026-01-01T02:00:00Z"),
        candidate_known_at=pd.Timestamp("2026-01-01T03:00:00Z"),
    )

    assert selected == older
    assert _impact_label(
        old_state="INHERITED_REMAINING_RUN",
        old_anchor_known_at=newer.anchor_known_at,
        new_origin=selected,
    ) == "REANCHORED_TO_OLDER_VALID_ORIGIN"


def test_strict_equality_does_not_destroy_origin() -> None:
    idx = pd.date_range("2026-01-01T01:00:00Z", periods=60, freq="min")
    m1 = pd.DataFrame(
        {
            "open": [105.5] * len(idx),
            "high": [106.0] * len(idx),
            "low": [105.0] * len(idx),
            "close": [105.5] * len(idx),
            "volume": [1.0] * len(idx),
        },
        index=idx,
    )
    origin = OriginRun(
        "BUY",
        pd.Timestamp("2026-01-01T00:00:00Z"),
        pd.Timestamp("2026-01-01T01:00:00Z"),
        105.0,
    )

    assert (
        _origin_destroyed_before(
            m1,
            origin,
            pd.Timestamp("2026-01-01T02:00:00Z"),
        )
        is False
    )
