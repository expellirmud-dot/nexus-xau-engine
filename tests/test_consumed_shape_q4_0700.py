from __future__ import annotations

import pandas as pd

from nexus_xau.research.consumed_shape_q4_0700 import (
    FEATURE,
    INDICATOR,
    _assign_quintiles,
    _shape_classification,
    build_feature_rows,
    build_quintiles,
    build_trim_sensitivity,
)


def _rows() -> pd.DataFrame:
    records = []
    for tf, offset in (("H4", 0), ("H1", 20)):
        for index in range(10):
            consumed = (index + 1) / 10.0
            target = 1.0 if index >= 5 else 0.0
            records.append(
                {
                    "context_id": f"{tf}-c{index // 2}",
                    "day_id": f"2026-01-{index + 1:02d}",
                    "side": "BUY",
                    "origin_id": f"{tf}-o{index}",
                    "origin_tf": tf,
                    "path_remaining_first_hit": (
                        "TARGET_FIRST" if target == 1.0 else "POINT_CHECK_FIRST"
                    ),
                    "path_remaining_first_hit_indicator": target,
                    "consumed_ratio_at_0700": consumed,
                    "post_confirmation_mfe_points": 100.0 + offset + index,
                    "post_confirmation_mae_points": 50.0 + offset + index,
                }
            )
    records.append(
        {
            "context_id": "drop",
            "day_id": "2026-01-20",
            "side": "BUY",
            "origin_id": "drop",
            "origin_tf": "H4",
            "path_remaining_first_hit": "NEITHER_BEFORE_NEXT_0700",
            "path_remaining_first_hit_indicator": None,
            "consumed_ratio_at_0700": 0.55,
            "post_confirmation_mfe_points": 0.0,
            "post_confirmation_mae_points": 0.0,
        }
    )
    return pd.DataFrame(records)


def test_feature_rows_keep_resolved_h1_h4_only() -> None:
    rows = build_feature_rows(_rows())

    assert len(rows) == 20
    assert set(rows["origin_tf"]) == {"H1", "H4"}
    assert rows[INDICATOR].notna().all()


def test_assign_quintiles_returns_five_groups() -> None:
    series = pd.Series([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

    result = _assign_quintiles(series)

    assert list(result.astype(str).value_counts().sort_index().index) == [
        "Q1",
        "Q2",
        "Q3",
        "Q4",
        "Q5",
    ]
    assert set(result.astype(str).value_counts()) == {2}


def test_shape_classification_detects_monotonic_and_reversal() -> None:
    status, diffs = _shape_classification([0.1, 0.2, 0.2, 0.5, 0.8])
    assert status == "STRICT_NONDECREASING"
    assert diffs[0] > 0

    status2, diffs2 = _shape_classification([0.1, 0.4, 0.3, 0.5, 0.8])
    assert status2 == "NOT_STRICT_NONDECREASING"
    assert diffs2[1] < 0


def test_quintiles_report_origin_and_context_levels() -> None:
    rows = build_feature_rows(_rows())
    quintiles = build_quintiles(rows)

    h4_origin = quintiles[
        quintiles["origin_tf"].eq("H4")
        & quintiles["analysis_level"].eq("ORIGIN_ROW")
    ]
    h4_context = quintiles[
        quintiles["origin_tf"].eq("H4")
        & quintiles["analysis_level"].eq("CONTEXT")
    ]

    assert len(h4_origin) == 5
    assert len(h4_context) == 5
    assert h4_origin["n_rows"].sum() == 10
    assert h4_context["n_rows"].sum() == 5
    assert h4_origin.loc[h4_origin["quintile"].eq("Q5"), "target_first_fraction"].iloc[0] == 1.0


def test_trim_sensitivity_includes_all_frozen_variants() -> None:
    rows = build_feature_rows(_rows())
    trim = build_trim_sensitivity(rows)

    subset = trim[
        trim["origin_tf"].eq("H4")
        & trim["analysis_level"].eq("ORIGIN_ROW")
    ]

    assert set(subset["trim_variant"]) == {
        "FULL",
        "CENTRAL_80",
        "DROP_BOTTOM_10",
        "DROP_TOP_10",
    }
    assert subset.loc[subset["trim_variant"].eq("FULL"), "n_rows"].iloc[0] == 10
    assert subset.loc[subset["trim_variant"].eq("CENTRAL_80"), "n_rows"].iloc[0] < 10
    assert subset.loc[subset["trim_variant"].eq("FULL"), "rho"].iloc[0] > 0


def test_feature_name_is_consumed_ratio() -> None:
    assert FEATURE == "consumed_ratio_at_0700"
