from __future__ import annotations

import numpy as np
import pandas as pd

from nexus_xau.research.distinct_information_q3_0700 import (
    AGE,
    CONSUMED,
    INDICATOR,
    MTF1,
    MTF2,
    _fit_logistic,
    _partial_rank_rho,
    build_feature_rows,
    build_leave_one_out,
    build_pairwise,
    build_partial,
)


def test_partial_rank_recovers_positive_feature_after_controls() -> None:
    frame = pd.DataFrame(
        {
            "feature": [1, 2, 3, 4, 5, 6],
            "outcome": [0, 0, 0, 1, 1, 1],
            "control_a": [1, 1, 1, 1, 1, 1],
            "control_b": [2, 2, 2, 2, 2, 2],
        }
    )

    rho, n = _partial_rank_rho(
        frame,
        feature="feature",
        outcome="outcome",
        controls=("control_a", "control_b"),
    )

    assert n == 6
    assert rho is not None
    assert rho > 0


def test_logistic_fit_returns_ok_for_nonseparated_sample() -> None:
    x = np.asarray(
        [
            [1.0, 1.0],
            [1.0, 1.0],
            [1.0, 2.0],
            [1.0, 2.0],
            [2.0, 1.0],
            [2.0, 1.0],
            [2.0, 2.0],
            [2.0, 2.0],
        ]
    )
    y = np.asarray([0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0])

    fit = _fit_logistic(x, y)

    assert fit.status == "OK"
    assert fit.log_loss is not None
    assert fit.coefficients is not None
    assert len(fit.coefficients) == 3


def test_logistic_fit_marks_single_class_unresolved() -> None:
    x = np.asarray([[1.0], [2.0], [3.0], [4.0]])
    y = np.asarray([1.0, 1.0, 1.0, 1.0])

    fit = _fit_logistic(x, y)

    assert fit.status == "UNSTABLE/UNRESOLVED"
    assert fit.log_loss is None


def _q2_rows() -> pd.DataFrame:
    rows = []
    outcomes = [
        "POINT_CHECK_FIRST",
        "TARGET_FIRST",
        "POINT_CHECK_FIRST",
        "TARGET_FIRST",
        "POINT_CHECK_FIRST",
        "TARGET_FIRST",
        "POINT_CHECK_FIRST",
        "TARGET_FIRST",
    ]
    for index, outcome in enumerate(outcomes):
        rows.append(
            {
                "context_id": f"c{index // 2}",
                "day_id": f"2026-01-{index + 1:02d}",
                "side": "BUY" if index % 2 == 0 else "SELL",
                "origin_id": f"o{index}",
                "origin_tf": "H4" if index < 4 else "H1",
                "confirmation_event_id": f"e{index}",
                "path_remaining_first_hit": outcome,
                "path_remaining_first_hit_indicator": (
                    1.0 if outcome == "TARGET_FIRST" else 0.0
                ),
                AGE: float(index + 1),
                CONSUMED: float(index + 1) / 10.0,
                MTF1: float(1 + (index % 2)),
                MTF2: float(1 + (index % 3)),
            }
        )
    rows.append(
        {
            "context_id": "cx",
            "day_id": "2026-01-20",
            "side": "BUY",
            "origin_id": "ox",
            "origin_tf": "H4",
            "confirmation_event_id": "ex",
            "path_remaining_first_hit": "NEITHER_BEFORE_NEXT_0700",
            "path_remaining_first_hit_indicator": np.nan,
            AGE: 9.0,
            CONSUMED: 0.9,
            MTF1: 2.0,
            MTF2: 2.0,
        }
    )
    return pd.DataFrame(rows)


def test_build_feature_rows_keeps_resolved_only() -> None:
    rows = build_feature_rows(_q2_rows())

    assert len(rows) == 8
    assert rows[INDICATOR].notna().all()
    assert set(rows["origin_tf"]) == {"H4", "H1"}


def test_pairwise_partial_and_leave_one_out_cover_both_timeframes() -> None:
    rows = build_feature_rows(_q2_rows())

    pairwise = build_pairwise(rows)
    partial = build_partial(rows)
    leave = build_leave_one_out(rows)

    assert set(pairwise["origin_tf"]) == {"H4", "H1"}
    assert len(pairwise) == 12  # 6 feature pairs x 2 TF

    assert set(partial["analysis_level"]) == {"ORIGIN_ROW", "CONTEXT"}
    assert set(partial["origin_tf"]) == {"H4", "H1"}
    assert set(partial["model_family"]) == {
        "RECENT_1_TF_BAR",
        "RECENT_2_TF_BARS",
    }

    assert set(leave["origin_tf"]) == {"H4", "H1"}
    assert set(leave["model"]) == {"FULL", "LEAVE_ONE_OUT"}
