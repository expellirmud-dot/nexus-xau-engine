from __future__ import annotations

import copy

import numpy as np
import pandas as pd
import pytest

from nexus_xau.research.state_packet_0700 import (
    COMPLETE_WITHIN_OPERATIONAL_EPOCH,
    INIT_OPERATIONAL_EXPLICIT_EPOCH,
    INIT_SOURCE_PURE,
    PACKET_VERSION,
    StatePacketError,
    build_state_packet,
)

START = pd.Timestamp("2026-01-01T00:00:00Z")
CHECKPOINT = pd.Timestamp("2026-01-02T00:00:00Z")
GENERATED = pd.Timestamp("2026-01-02T00:05:00Z")


def _expand_h4_blocks(
    specs: list[tuple[float, float, float, float]],
    *,
    boundary_price: float = 106.0,
) -> pd.DataFrame:
    pieces: list[pd.DataFrame] = []
    for block_number, (open_, high, low, close) in enumerate(specs):
        block_start = START + pd.Timedelta(hours=4 * block_number)
        index = pd.date_range(block_start, periods=240, freq="1min", tz="UTC")
        values = np.linspace(open_, close, len(index))
        frame = pd.DataFrame(
            {
                "open": values,
                "high": values,
                "low": values,
                "close": values,
                "volume": np.ones(len(index), dtype=float),
            },
            index=index,
        )
        frame.iloc[60, frame.columns.get_loc("high")] = high
        frame.iloc[120, frame.columns.get_loc("low")] = low
        frame.iloc[-1, frame.columns.get_loc("close")] = close
        pieces.append(frame)

    result = pd.concat(pieces).sort_index()
    result.loc[CHECKPOINT] = {
        "open": boundary_price,
        "high": boundary_price,
        "low": boundary_price,
        "close": boundary_price,
        "volume": 1.0,
    }
    return result


def _buy_frame() -> pd.DataFrame:
    return _expand_h4_blocks(
        [
            (100.0, 110.0, 80.0, 90.0),
            (90.0, 105.0, 85.0, 100.0),
            (100.0, 108.0, 98.0, 100.0),
            (105.0, 108.0, 102.0, 105.0),
            (105.0, 108.0, 102.0, 105.0),
            (105.0, 108.0, 102.0, 105.0),
        ]
    )


def _sell_frame() -> pd.DataFrame:
    return _expand_h4_blocks(
        [
            (90.0, 110.0, 85.0, 100.0),
            (100.0, 105.0, 88.0, 90.0),
            (95.0, 102.0, 90.0, 95.0),
            (95.0, 100.0, 90.0, 95.0),
            (95.0, 100.0, 90.0, 95.0),
            (95.0, 100.0, 90.0, 95.0),
        ]
    )


def _two_buy_origin_frame() -> pd.DataFrame:
    return _expand_h4_blocks(
        [
            (100.0, 110.0, 80.0, 90.0),
            (90.0, 105.0, 85.0, 100.0),
            (100.0, 108.0, 98.0, 100.0),
            (105.0, 108.0, 100.0, 101.0),
            (101.0, 110.0, 100.0, 106.0),
            (106.0, 111.0, 104.0, 106.0),
        ]
    )


def _packet(
    frame: pd.DataFrame,
    *,
    mode: str = INIT_OPERATIONAL_EXPLICIT_EPOCH,
    epoch: pd.Timestamp = START,
) -> dict[str, object]:
    return build_state_packet(
        m1=frame,
        checkpoint_at=CHECKPOINT,
        initialization_mode=mode,
        initialization_epoch=epoch,
        source_identity={
            "source_family": "SYNTHETIC_TEST_M1",
            "symbol": "XAUUSDm",
        },
        generated_at_utc=GENERATED,
    )


def _first_origin(packet: dict[str, object]) -> dict[str, object]:
    origins = packet["observed_h4_origins"]
    assert isinstance(origins, list)
    assert origins
    return origins[0]


def _all_keys(value: object) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            keys.add(str(key).lower())
            keys.update(_all_keys(item))
    elif isinstance(value, list):
        for item in value:
            keys.update(_all_keys(item))
    return keys


def test_checkpoint_must_map_to_0700_thailand() -> None:
    with pytest.raises(StatePacketError, match="07:00"):
        build_state_packet(
            m1=_buy_frame(),
            checkpoint_at="2026-01-02T01:00:00Z",
            initialization_mode=INIT_OPERATIONAL_EXPLICIT_EPOCH,
            initialization_epoch=START,
            source_identity={"source_family": "SYNTHETIC_TEST_M1"},
            generated_at_utc=GENERATED,
        )


def test_post_checkpoint_rows_cannot_change_snapshot() -> None:
    base = _buy_frame()
    future = base.copy()
    for minute in range(1, 6):
        timestamp = CHECKPOINT + pd.Timedelta(minutes=minute)
        future.loc[timestamp] = {
            "open": 500.0,
            "high": 900.0,
            "low": 1.0,
            "close": 700.0,
            "volume": 999.0,
        }
    assert _packet(base) == _packet(future)


def test_checkpoint_bar_only_open_is_knowable_at_boundary() -> None:
    base = _buy_frame()
    mutated = base.copy()
    mutated.loc[CHECKPOINT, "high"] = 900.0
    mutated.loc[CHECKPOINT, "low"] = 1.0
    mutated.loc[CHECKPOINT, "close"] = 700.0
    mutated.loc[CHECKPOINT, "volume"] = 999.0

    base_packet = _packet(base)
    mutated_packet = _packet(mutated)

    assert base_packet == mutated_packet
    assert base_packet["data_health"]["checkpoint_boundary_semantics"] == (
        "OPEN_ONLY_HLCV_SANITIZED_NOT_KNOWABLE_AT_BOUNDARY"
    )


def test_fixed_origin_target_matches_v21_geometry() -> None:
    origin = _first_origin(_packet(_buy_frame()))
    assert origin["side"] == "BUY"
    assert origin["anchor_price"] == pytest.approx(98.0)
    assert origin["fixed_origin_target_price"] == pytest.approx(113.0)
    assert origin["target_representation"] == "FIXED_ORIGIN_TARGET_V2_1"


def test_exact_point_check_touch_is_terminal() -> None:
    frame = _buy_frame()
    frame.loc[pd.Timestamp("2026-01-01T13:00:00Z"), "low"] = 98.0
    origin = _first_origin(_packet(frame))
    assert origin["lifecycle_state_0700"] == "POINT_CHECK_DESTROYED"
    assert origin["point_check_at_before_0700"] == "2026-01-01T13:00:00+00:00"


def test_point_check_near_miss_survives() -> None:
    frame = _buy_frame()
    frame.loc[pd.Timestamp("2026-01-01T13:00:00Z"), "low"] = 98.01
    origin = _first_origin(_packet(frame))
    assert origin["lifecycle_state_0700"] == "ACTIVE"


def test_target_first_maps_to_run_complete() -> None:
    frame = _buy_frame()
    frame.loc[pd.Timestamp("2026-01-01T13:00:00Z"), "high"] = 113.0
    origin = _first_origin(_packet(frame))
    assert origin["lifecycle_state_0700"] == "RUN_COMPLETE"
    assert origin["target_at_before_0700"] == "2026-01-01T13:00:00+00:00"


def test_same_bar_terminal_is_ambiguous() -> None:
    frame = _buy_frame()
    timestamp = pd.Timestamp("2026-01-01T13:00:00Z")
    frame.loc[timestamp, "high"] = 113.0
    frame.loc[timestamp, "low"] = 98.0
    origin = _first_origin(_packet(frame))
    assert origin["lifecycle_state_0700"] == "AMBIGUOUS_TERMINAL_SAME_BAR"
    assert origin["terminal_ordering"] == "AMBIGUOUS_SAME_BAR"


def test_source_pure_unknown_prehistory_fails_closed() -> None:
    packet = _packet(_buy_frame(), mode=INIT_SOURCE_PURE)
    assert packet["state_0700"] == "UNKNOWN"
    assert packet["post_0700_requirement"] == "PASS_INITIALIZATION_UNKNOWN"
    assert packet["calculation_confidence"] == (
        "FAIL_CLOSED_CANONICAL_UNKNOWN_PREHISTORY"
    )
    assert packet["initialization"]["origin_set_completeness"] == "UNKNOWN_PREHISTORY"


def test_operational_epoch_is_explicit_convention() -> None:
    packet = _packet(_buy_frame())
    assert packet["packet_version"] == PACKET_VERSION
    assert packet["initialization"]["mode"] == INIT_OPERATIONAL_EXPLICIT_EPOCH
    assert packet["initialization"]["authority"] == (
        "OWNER_DIRECT_PROJECT_ENGINEERING_CONVENTION"
    )
    assert packet["initialization"]["origin_set_completeness"] == (
        COMPLETE_WITHIN_OPERATIONAL_EPOCH
    )
    assert packet["initialization"]["historical_absence_claim"] is False
    assert packet["initialization"]["lifecycle_rule_changed"] is False


def test_operational_epoch_missing_input_fails_data_health() -> None:
    packet = _packet(
        _buy_frame(),
        epoch=pd.Timestamp("2025-12-31T20:00:00Z"),
    )
    assert packet["data_health"]["calculation_eligibility"] == "FAIL_CLOSED"
    assert packet["state_0700"] == "UNKNOWN"
    assert packet["post_0700_requirement"] == "PASS_DATA_UNKNOWN"


def test_buy_only_context_summary() -> None:
    packet = _packet(_buy_frame())
    assert packet["origin_summary"]["active_buy_count"] == 1
    assert packet["origin_summary"]["active_sell_count"] == 0
    assert packet["state_0700"] == "BULLISH_CONTEXT"
    assert packet["post_0700_requirement"] == "WAIT_POST_0700_CONFIRMATION"


def test_sell_only_context_summary() -> None:
    packet = _packet(_sell_frame())
    assert packet["origin_summary"]["active_buy_count"] == 0
    assert packet["origin_summary"]["active_sell_count"] == 1
    assert packet["state_0700"] == "BEARISH_CONTEXT"


def test_multiple_origins_fail_closed_on_conflict() -> None:
    packet = _packet(_two_buy_origin_frame())
    assert packet["origin_summary"]["active_buy_count"] >= 2
    assert packet["conflict"]["same_side_multiple"] is True
    assert packet["conflict"]["conflict_present"] is True
    assert packet["post_0700_requirement"] == "PASS_CONFLICT_UNRESOLVED"


def test_no_active_origin_is_explicit_pass() -> None:
    frame = _buy_frame()
    frame.loc[pd.Timestamp("2026-01-01T13:00:00Z"), "low"] = 98.0
    packet = _packet(frame)
    assert packet["origin_summary"]["active_origin_count"] == 0
    assert packet["state_0700"] == "NO_ACTIVE_ORIGIN"
    assert packet["post_0700_requirement"] == "PASS_NO_ACTIVE_ORIGIN"


def test_daily_frame_authority_boundary() -> None:
    packet = _packet(_buy_frame())
    daily = packet["daily_frame"]
    assert daily["authority"] == "RESEARCH_REPRESENTATION"
    assert daily["boundary_price_authority"] == (
        "RUNTIME_OBSERVATION_AT_CHECKPOINT"
    )
    assert daily["price_at_checkpoint"] == pytest.approx(106.0)
    assert daily["reference"] == pytest.approx(105.0)
    assert daily["action_qualification_state"] == (
        "UNKNOWN_SOURCE_GEOMETRY_NOT_UNIVERSAL"
    )


def test_unknown_classification_separates_downstream() -> None:
    packet = _packet(_buy_frame())
    unknowns = packet["unknowns"]
    downstream = next(
        item for item in unknowns if item["id"] == "EXECUTION-ECONOMICS-GROUP"
    )
    assert downstream["blocking_axis"] == (
        "NON_BLOCKING_0700_STATE_REQUIRED_LATER"
    )
    lower_tf = next(
        item for item in unknowns if item["id"] == "LOWER-TF-CONFIRMATION-ROUTING"
    )
    assert lower_tf["packet_effect"] == "NON_BLOCKING_0700_SNAPSHOT"


def test_packet_has_no_execution_or_outcome_fields() -> None:
    keys = _all_keys(_packet(_buy_frame()))
    forbidden = {
        "win_rate",
        "loss_rate",
        "expectancy",
        "profitability",
        "trade_pnl",
        "position_size",
        "risk_cap",
        "fill_price",
        "slippage",
        "order_send",
    }
    assert keys.isdisjoint(forbidden)


def test_packet_is_deterministic_for_same_inputs() -> None:
    frame = _buy_frame()
    first = _packet(frame)
    second = _packet(copy.deepcopy(frame))
    assert first == second
