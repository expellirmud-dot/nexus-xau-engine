import pandas as pd
import pytest

from nexus_xau.data.price_grid import PriceGrid
from nexus_xau.research.sig_mode2_signal_run_v0 import (
    SCHEMA_VERSION,
    LocationLabel,
    SigMode2SignalRunEvent,
    SigMode2V0Manifest,
    SignalRunResult,
    SignalSide,
    SignalTimeframe,
    replay_sig_mode2_manifest_v0,
    replay_sig_mode2_signal_run_v0,
)


def _event(**overrides: object) -> SigMode2SignalRunEvent:
    raw: dict[str, object] = {
        "signal_id": "sig-1",
        "side": "BUY",
        "signal_tf": "H1",
        "pa_kind_or_source_label": "SOURCE_LABELED_PAT2",
        "pa_confirmed_at": "2026-09-01T09:00:00+00:00",
        "location_label": "VALID_SUPPORT",
        "location_label_provenance": "fixture:pre-outcome-label",
        "post_sig_closed_at": "2026-09-01T10:00:00+00:00",
        "point_check_price": "100.000",
        "point_check_price_provenance": "fixture:post-sig-low",
        "run_anchor_price": "100.000",
        "run_target_price": "101.000",
        "horizon_end": "2026-09-01T10:04:00+00:00",
        "parent_context_tf": "H4",
        "context_tags": ["TREND_UP", "FRAME_SUPPORT"],
        "source_or_label_provenance": "fixture:locked-before-outcome",
        "label_known_before_outcome": True,
    }
    raw.update(overrides)
    return SigMode2SignalRunEvent.from_mapping(raw)


def _bars(rows: list[tuple[str, float, float, float]]) -> pd.DataFrame:
    index = pd.DatetimeIndex([pd.Timestamp(ts) for ts, *_ in rows])
    return pd.DataFrame(
        {
            "high": [high for _, high, _, _ in rows],
            "low": [low for _, _, low, _ in rows],
            "close": [close for _, _, _, close in rows],
        },
        index=index,
    )


def test_buy_target_first_after_signal_known_at() -> None:
    event = _event()
    bars = _bars(
        [
            ("2026-09-01T09:59:00+00:00", 200.0, 99.0, 150.0),
            ("2026-09-01T10:00:00+00:00", 100.500, 100.100, 100.400),
            ("2026-09-01T10:01:00+00:00", 101.100, 100.200, 101.000),
            ("2026-09-01T10:02:00+00:00", 99.900, 99.500, 99.700),
        ]
    )

    outcome = replay_sig_mode2_signal_run_v0(
        bars,
        event=event,
        grid=PriceGrid.from_tick_size("0.001"),
    )

    assert outcome.result is SignalRunResult.TARGET_FIRST
    assert outcome.target_hit_at == pd.Timestamp("2026-09-01T10:01:00+00:00")
    assert outcome.point_check_hit_at is None
    assert outcome.bars_observed == 2
    assert outcome.mfe_ticks == 1100
    assert outcome.mae_ticks == 0


def test_buy_point_check_first_counts_exact_contact() -> None:
    event = _event()
    bars = _bars(
        [
            ("2026-09-01T10:00:00+00:00", 100.400, 100.001, 100.200),
            ("2026-09-01T10:01:00+00:00", 100.300, 100.000, 100.100),
            ("2026-09-01T10:02:00+00:00", 101.100, 100.200, 101.000),
        ]
    )

    outcome = replay_sig_mode2_signal_run_v0(
        bars,
        event=event,
        grid=PriceGrid.from_tick_size("0.001"),
    )

    assert outcome.result is SignalRunResult.POINT_CHECK_FIRST
    assert outcome.point_check_hit_at == pd.Timestamp("2026-09-01T10:01:00+00:00")
    assert outcome.target_hit_at is None
    assert outcome.bars_observed == 2


def test_same_bar_target_and_point_check_is_ambiguous() -> None:
    event = _event()
    bars = _bars(
        [
            ("2026-09-01T10:00:00+00:00", 101.100, 100.000, 100.500),
        ]
    )

    outcome = replay_sig_mode2_signal_run_v0(
        bars,
        event=event,
        grid=PriceGrid.from_tick_size("0.001"),
    )

    assert outcome.result is SignalRunResult.AMBIGUOUS_SAME_BAR
    assert outcome.target_hit_at == outcome.point_check_hit_at


def test_one_tick_near_miss_survives_until_horizon() -> None:
    event = _event(horizon_end="2026-09-01T10:01:00+00:00")
    bars = _bars(
        [
            ("2026-09-01T10:00:00+00:00", 100.500, 100.001, 100.300),
            ("2026-09-01T10:01:00+00:00", 100.700, 100.001, 100.600),
        ]
    )

    outcome = replay_sig_mode2_signal_run_v0(
        bars,
        event=event,
        grid=PriceGrid.from_tick_size("0.001"),
    )

    assert outcome.result is SignalRunResult.HORIZON_EXHAUSTED
    assert outcome.point_check_hit_at is None
    assert outcome.target_hit_at is None


def test_sell_mirror_target_first() -> None:
    event = _event(
        side="SELL",
        signal_tf="H4",
        location_label="VALID_RESISTANCE",
        run_target_price="99.000",
    )
    bars = _bars(
        [
            ("2026-09-01T10:00:00+00:00", 99.999, 99.500, 99.700),
            ("2026-09-01T10:01:00+00:00", 99.900, 98.900, 99.100),
        ]
    )

    outcome = replay_sig_mode2_signal_run_v0(
        bars,
        event=event,
        grid=PriceGrid.from_tick_size("0.001"),
    )

    assert outcome.side is SignalSide.SELL
    assert outcome.signal_tf is SignalTimeframe.H4
    assert outcome.result is SignalRunResult.TARGET_FIRST
    assert outcome.mfe_ticks == 1100
    assert outcome.mae_ticks == 0


def test_manifest_replays_multiple_unique_events() -> None:
    raw = {
        "schema_version": SCHEMA_VERSION,
        "dataset_id": "fixture-bid-m1",
        "tick_size": "0.001",
        "events": [
            {
                "signal_id": "buy-1",
                "side": "BUY",
                "signal_tf": "H1",
                "pa_kind_or_source_label": "SOURCE_LABELED_PAT2",
                "pa_confirmed_at": "2026-09-01T09:00:00+00:00",
                "location_label": "VALID_SUPPORT",
                "location_label_provenance": "fixture",
                "post_sig_closed_at": "2026-09-01T10:00:00+00:00",
                "point_check_price": "100.000",
                "point_check_price_provenance": "fixture",
                "run_anchor_price": "100.000",
                "run_target_price": "101.000",
                "horizon_end": "2026-09-01T10:01:00+00:00",
                "parent_context_tf": "H4",
                "context_tags": [],
                "source_or_label_provenance": "fixture",
                "label_known_before_outcome": True,
            },
            {
                "signal_id": "sell-1",
                "side": "SELL",
                "signal_tf": "H4",
                "pa_kind_or_source_label": "SOURCE_LABELED_PAT3",
                "pa_confirmed_at": "2026-09-01T09:00:00+00:00",
                "location_label": "VALID_RESISTANCE",
                "location_label_provenance": "fixture",
                "post_sig_closed_at": "2026-09-01T10:00:00+00:00",
                "point_check_price": "100.000",
                "point_check_price_provenance": "fixture",
                "run_anchor_price": "100.000",
                "run_target_price": "99.000",
                "horizon_end": "2026-09-01T10:01:00+00:00",
                "parent_context_tf": "D1",
                "context_tags": [],
                "source_or_label_provenance": "fixture",
                "label_known_before_outcome": True,
            },
        ],
    }
    manifest = SigMode2V0Manifest.from_mapping(raw)
    bars = _bars(
        [
            ("2026-09-01T10:00:00+00:00", 100.500, 99.500, 100.100),
            ("2026-09-01T10:01:00+00:00", 101.100, 98.900, 100.000),
        ]
    )

    outcomes = replay_sig_mode2_manifest_v0(bars, manifest)

    assert len(outcomes) == 2
    assert {outcome.signal_id for outcome in outcomes} == {"buy-1", "sell-1"}
    assert all(outcome.result is SignalRunResult.POINT_CHECK_FIRST for outcome in outcomes)


def test_invalid_location_or_post_outcome_label_fails_closed() -> None:
    with pytest.raises(ValueError, match="VALID_SUPPORT"):
        _event(location_label="VALID_RESISTANCE")

    with pytest.raises(ValueError, match="label_known_before_outcome"):
        _event(label_known_before_outcome=False)

    with pytest.raises(ValueError, match="boolean true"):
        _event(label_known_before_outcome="false")


def test_v0_requires_point_check_and_run_anchor_to_be_same_tick() -> None:
    event = _event(run_anchor_price="100.001")
    bars = _bars(
        [
            ("2026-09-01T10:00:00+00:00", 100.500, 100.100, 100.300),
        ]
    )

    with pytest.raises(ValueError, match="same normalized post-SIG wick"):
        replay_sig_mode2_signal_run_v0(
            bars,
            event=event,
            grid=PriceGrid.from_tick_size("0.001"),
        )


def test_off_grid_event_price_and_duplicate_signal_ids_fail_closed() -> None:
    event = _event(point_check_price="100.0005", run_anchor_price="100.0005")
    bars = _bars(
        [
            ("2026-09-01T10:00:00+00:00", 100.500, 100.100, 100.300),
        ]
    )

    with pytest.raises(ValueError, match="not aligned"):
        replay_sig_mode2_signal_run_v0(
            bars,
            event=event,
            grid=PriceGrid.from_tick_size("0.001"),
        )

    base = {
        "signal_id": "dup",
        "side": "BUY",
        "signal_tf": "H1",
        "pa_kind_or_source_label": "SOURCE_LABELED_PAT2",
        "pa_confirmed_at": "2026-09-01T09:00:00+00:00",
        "location_label": "VALID_SUPPORT",
        "location_label_provenance": "fixture",
        "post_sig_closed_at": "2026-09-01T10:00:00+00:00",
        "point_check_price": "100.000",
        "point_check_price_provenance": "fixture",
        "run_anchor_price": "100.000",
        "run_target_price": "101.000",
        "horizon_end": "2026-09-01T10:01:00+00:00",
        "parent_context_tf": "H4",
        "context_tags": [],
        "source_or_label_provenance": "fixture",
        "label_known_before_outcome": True,
    }
    with pytest.raises(ValueError, match="unique"):
        SigMode2V0Manifest.from_mapping(
            {
                "schema_version": SCHEMA_VERSION,
                "dataset_id": "fixture",
                "tick_size": "0.001",
                "events": [base, dict(base)],
            }
        )


def test_timestamp_and_manifest_version_validation() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        _event(post_sig_closed_at="2026-09-01T10:00:00")

    assert LocationLabel.VALID_SUPPORT.value == "VALID_SUPPORT"
    with pytest.raises(ValueError, match="schema_version"):
        SigMode2V0Manifest.from_mapping(
            {
                "schema_version": "wrong",
                "dataset_id": "fixture",
                "tick_size": "0.001",
                "events": [],
            }
        )
