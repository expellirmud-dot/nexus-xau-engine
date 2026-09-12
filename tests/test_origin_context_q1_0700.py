from __future__ import annotations

import pandas as pd

from nexus_xau.research.origin_context_q1_0700 import (
    VARIANT_ANY,
    VARIANT_EXPECTED,
    _boundary_hit,
    _preconfirmation_state,
    _preconfirmation_terminal,
    _select_confirmation,
    build_q1_events,
)


def _m1(
    start: str,
    rows: list[tuple[float, float, float, float]],
) -> pd.DataFrame:
    index = pd.date_range(start, periods=len(rows), freq="1min", tz="UTC")
    return pd.DataFrame(
        rows,
        columns=["open", "high", "low", "close"],
        index=index,
    )


def test_select_confirmation_freezes_any_and_expected_variants() -> None:
    events = pd.DataFrame(
        [
            {
                "event_id": "a",
                "event_known_at": pd.Timestamp("2026-01-01T00:05:00Z"),
                "event_tf": "M5",
                "frame_side": "CROSSED_SIDE",
            },
            {
                "event_id": "b",
                "event_known_at": pd.Timestamp("2026-01-01T00:10:00Z"),
                "event_tf": "M5",
                "frame_side": "EXPECTED_SIDE",
            },
        ]
    )

    any_event = _select_confirmation(events=events, variant=VARIANT_ANY)
    expected_event = _select_confirmation(events=events, variant=VARIANT_EXPECTED)

    assert any_event is not None
    assert expected_event is not None
    assert any_event["event_id"] == "a"
    assert expected_event["event_id"] == "b"


def test_boundary_hit_preserves_same_bar_ambiguity() -> None:
    path = _m1(
        "2026-01-01T00:00:00",
        [
            (100.0, 100.5, 99.5, 100.0),
            (100.0, 102.0, 98.0, 100.0),
        ],
    )

    hit = _boundary_hit(
        path=path,
        side="BUY",
        target_price=101.0,
        point_check_price=99.0,
    )

    assert hit.first_hit == "AMBIGUOUS_SAME_BAR"
    assert hit.target_at == path.index[1]
    assert hit.point_check_at == path.index[1]


def test_preconfirmation_path_excludes_confirmation_timestamp() -> None:
    path = _m1(
        "2026-01-01T00:00:00",
        [
            (100.0, 100.5, 99.5, 100.0),
            (100.0, 100.6, 99.6, 100.0),
            (100.0, 110.5, 99.6, 110.0),
        ],
    )
    known_at = path.index[2]

    hit = _preconfirmation_terminal(
        active_m1=path,
        side="BUY",
        anchor=95.0,
        nominal_points=1000.0,
        cutoff=path.index[0],
        confirmation_known_at=known_at,
    )

    assert hit.first_hit == "NEITHER"
    assert _preconfirmation_state(hit) == "ACTIVE_AT_CONFIRMATION"


def test_preconfirmation_point_check_destroys_before_confirmation() -> None:
    path = _m1(
        "2026-01-01T00:00:00",
        [
            (101.0, 101.5, 100.5, 101.0),
            (101.0, 101.2, 99.8, 100.2),
            (100.2, 101.0, 100.0, 100.5),
        ],
    )

    hit = _preconfirmation_terminal(
        active_m1=path,
        side="BUY",
        anchor=100.0,
        nominal_points=1000.0,
        cutoff=path.index[0],
        confirmation_known_at=path.index[2],
    )

    assert _preconfirmation_state(hit) == "POINT_CHECK_DESTROYED_BEFORE_CONFIRMATION"


def test_build_q1_keeps_no_confirmation_rows() -> None:
    active = _m1(
        "2026-01-01T00:00:00",
        [(100.0, 100.2, 99.8, 100.0)] * (24 * 60 + 1),
    )
    day_state = pd.DataFrame(
        [
            {"day_id": "2026-01-01", "cutoff_utc": "2026-01-01T00:00:00+00:00"},
            {"day_id": "2026-01-02", "cutoff_utc": "2026-01-02T00:00:00+00:00"},
        ]
    )
    origins = pd.DataFrame(
        [
            {
                "day_id": "2026-01-01",
                "cutoff_utc": "2026-01-01T00:00:00+00:00",
                "origin_id": "H1:BUY:test",
                "origin_tf": "H1",
                "origin_side": "BUY",
                "origin_known_at": "2025-12-31T23:00:00+00:00",
                "origin_anchor_price": 100.0,
                "nominal_run_points": 1000.0,
                "origin_age_hours": 1.0,
                "consumed_ratio_at_0700": 0.0,
                "remaining_points_at_0700": 1000.0,
                "origin_validity_state": "INCOMPLETE_NOMINAL_RUN_RESEARCH_PROXY",
                "source_partial_survival_proxy": True,
            }
        ]
    )
    confirmations = pd.DataFrame(
        columns=[
            "day_id",
            "event_side",
            "event_id",
            "event_tf",
            "event_known_at",
            "pattern_close",
            "frame_side",
            "signed_distance_to_valid_frame_side_points",
            "alignment_count_exact",
            "aligned_tf_set_exact",
        ]
    )

    events = build_q1_events(
        active_m1=active,
        day_state=day_state,
        origins=origins,
        confirmations=confirmations,
    )

    assert len(events) == 2
    assert set(events["variant"]) == {VARIANT_ANY, VARIANT_EXPECTED}
    assert set(events["candidate_state"]) == {"NO_CONFIRMATION_BEFORE_NEXT_0700"}


def test_build_q1_scores_active_origin_without_selecting_winner() -> None:
    active = _m1(
        "2026-01-01T00:00:00",
        [(105.0, 105.2, 104.8, 105.0)] * (24 * 60 + 1),
    )
    # After confirmation, hit the path target before the point-check.
    active.loc[pd.Timestamp("2026-01-01T00:11:00Z"), "high"] = 115.5

    day_state = pd.DataFrame(
        [
            {"day_id": "2026-01-01", "cutoff_utc": "2026-01-01T00:00:00+00:00"},
            {"day_id": "2026-01-02", "cutoff_utc": "2026-01-02T00:00:00+00:00"},
        ]
    )
    origins = pd.DataFrame(
        [
            {
                "day_id": "2026-01-01",
                "cutoff_utc": "2026-01-01T00:00:00+00:00",
                "origin_id": "H1:BUY:test",
                "origin_tf": "H1",
                "origin_side": "BUY",
                "origin_known_at": "2025-12-31T23:00:00+00:00",
                "origin_anchor_price": 100.0,
                "nominal_run_points": 1000.0,
                "origin_age_hours": 1.0,
                "consumed_ratio_at_0700": 0.0,
                "remaining_points_at_0700": 1000.0,
                "origin_validity_state": "INCOMPLETE_NOMINAL_RUN_RESEARCH_PROXY",
                "source_partial_survival_proxy": True,
            },
            {
                "day_id": "2026-01-01",
                "cutoff_utc": "2026-01-01T00:00:00+00:00",
                "origin_id": "H4:BUY:test",
                "origin_tf": "H4",
                "origin_side": "BUY",
                "origin_known_at": "2025-12-31T20:00:00+00:00",
                "origin_anchor_price": 99.0,
                "nominal_run_points": 1500.0,
                "origin_age_hours": 4.0,
                "consumed_ratio_at_0700": 0.4,
                "remaining_points_at_0700": 900.0,
                "origin_validity_state": "INCOMPLETE_NOMINAL_RUN_RESEARCH_PROXY",
                "source_partial_survival_proxy": True,
            },
        ]
    )
    confirmations = pd.DataFrame(
        [
            {
                "day_id": "2026-01-01",
                "event_side": "BUY",
                "event_id": "M5:BUY:test",
                "event_tf": "M5",
                "event_known_at": "2026-01-01T00:10:00+00:00",
                "pattern_close": 105.0,
                "frame_side": "EXPECTED_SIDE",
                "signed_distance_to_valid_frame_side_points": 100.0,
                "alignment_count_exact": 2,
                "aligned_tf_set_exact": "M15,M5",
            }
        ]
    )

    events = build_q1_events(
        active_m1=active,
        day_state=day_state,
        origins=origins,
        confirmations=confirmations,
    )

    scored = events[events["candidate_state"] == "SCORED"]
    assert len(scored) == 4  # two origins x two frozen variants
    assert set(scored["context_origin_tf_set"]) == {"H1,H4"}
    assert set(scored["origin_tf"]) == {"H1", "H4"}
