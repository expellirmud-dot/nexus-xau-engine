from __future__ import annotations

import inspect

import pandas as pd

from nexus_xau.research.dukascopy_exness_overlap_sensitivity import (
    DUKASCOPY_SOURCE,
    EXACT_OBSERVED_STATE_EQUIVALENCE,
    EXNESS_SOURCE,
    INCOMPARABLE_INPUT_GAP,
    STATE_DIVERGENCE_OBSERVED,
    STRUCTURAL_STATE_EQUIVALENCE_NUMERIC_DIVERGENCE,
    compare_overlap_frames,
)

START = pd.Timestamp("2026-01-01T00:00:00Z")
END = pd.Timestamp("2026-01-03T00:00:00Z")


def _expand_h4_bar(
    start: str,
    *,
    open_price: float,
    high_price: float,
    low_price: float,
    close_price: float,
) -> pd.DataFrame:
    index = pd.date_range(start, periods=240, freq="1min")
    prices = [open_price + (close_price - open_price) * i / 239.0 for i in range(240)]
    prices[60] = high_price
    prices[120] = low_price
    prices[-1] = close_price
    return pd.DataFrame(
        {"open": prices, "high": prices, "low": prices, "close": prices},
        index=index,
    )


def _frame() -> pd.DataFrame:
    specs = [
        ("2026-01-01T00:00:00Z", 110.0, 112.0, 99.0, 100.0),
        ("2026-01-01T04:00:00Z", 100.0, 112.0, 100.0, 108.0),
        ("2026-01-01T08:00:00Z", 108.0, 111.0, 101.0, 109.0),
        ("2026-01-01T12:00:00Z", 109.0, 113.0, 108.0, 112.0),
        ("2026-01-01T16:00:00Z", 112.0, 113.0, 108.0, 109.0),
        ("2026-01-01T20:00:00Z", 109.0, 114.0, 108.0, 112.0),
        ("2026-01-02T00:00:00Z", 112.0, 114.0, 109.0, 113.0),
        ("2026-01-02T04:00:00Z", 113.0, 115.0, 110.0, 114.0),
        ("2026-01-02T08:00:00Z", 114.0, 116.2, 111.0, 115.0),
        ("2026-01-02T12:00:00Z", 115.0, 117.0, 112.0, 116.0),
        ("2026-01-02T16:00:00Z", 116.0, 118.0, 113.0, 117.0),
        ("2026-01-02T20:00:00Z", 117.0, 119.0, 114.0, 118.0),
    ]
    return pd.concat(
        [
            _expand_h4_bar(
                start,
                open_price=open_price,
                high_price=high_price,
                low_price=low_price,
                close_price=close_price,
            )
            for start, open_price, high_price, low_price, close_price in specs
        ]
    ).sort_index()


def _duk_provenance() -> dict[str, object]:
    return {"source_family": DUKASCOPY_SOURCE, "fixture": "synthetic"}


def _exn_provenance() -> dict[str, object]:
    return {"source_family": EXNESS_SOURCE, "fixture": "synthetic"}


def _compare(duk: pd.DataFrame, exn: pd.DataFrame):
    return compare_overlap_frames(
        dukascopy_m1=duk,
        exness_m1=exn,
        start=START,
        end=END,
        dukascopy_provenance=_duk_provenance(),
        exness_provenance=_exn_provenance(),
        window_id="SYNTHETIC",
    )

def test_identical_synthetic_feeds_are_exact_state_equivalence() -> None:
    frame = _frame()
    report = _compare(frame, frame.copy())
    assert report["classification"] == EXACT_OBSERVED_STATE_EQUIVALENCE


def test_constant_price_offset_preserves_structure_but_changes_numeric_state() -> None:
    duk = _frame()
    exn = duk.copy()
    exn[["open", "high", "low", "close"]] += 0.25
    report = _compare(duk, exn)
    assert (
        report["classification"]
        == STRUCTURAL_STATE_EQUIVALENCE_NUMERIC_DIVERGENCE
    )
    origins = report["origins"]
    assert origins["common_keys"]
    assert any(not row["anchor_exact_equal"] for row in origins["matched"])


def test_pat_structure_change_is_state_divergence() -> None:
    duk = _frame()
    exn = duk.copy()
    block = exn.loc[
        (exn.index >= pd.Timestamp("2026-01-01T04:00:00Z"))
        & (exn.index < pd.Timestamp("2026-01-01T08:00:00Z"))
    ].copy()
    exn.loc[block.index, ["open", "high", "low", "close"]] = 100.0
    report = _compare(duk, exn)
    assert report["classification"] == STATE_DIVERGENCE_OBSERVED
    assert (
        report["pat_h4"]["dukascopy_only_keys"]
        or report["pat_h4"]["exness_only_keys"]
        or report["origins"]["dukascopy_only_keys"]
        or report["origins"]["exness_only_keys"]
    )


def test_empty_source_frame_is_incomparable_input_gap() -> None:
    frame = _frame()
    empty = frame.iloc[0:0].copy()
    report = _compare(empty, frame)
    assert report["classification"] == INCOMPARABLE_INPUT_GAP


def test_source_provenance_stays_separate() -> None:
    frame = _frame()
    report = _compare(frame, frame.copy())
    provenance = report["source_provenance"]
    assert provenance["dukascopy"]["source_family"] == DUKASCOPY_SOURCE
    assert provenance["exness"]["source_family"] == EXNESS_SOURCE
    assert provenance["dukascopy"]["source_family"] != provenance["exness"]["source_family"]


def test_no_tolerance_is_accepted_or_emitted() -> None:
    assert "tolerance" not in inspect.signature(compare_overlap_frames).parameters
    report = _compare(_frame(), _frame())
    assert "tolerance" not in str(report).lower()


def test_no_trade_performance_or_execution_claim_fields_are_produced() -> None:
    report = _compare(_frame(), _frame())
    serialized = str(report).lower()
    forbidden = (
        "win_rate",
        "win rate",
        "expectancy",
        "profitability",
        "broker_fill",
        "broker-fill",
        "pnl",
        "p&l",
    )
    assert not [token for token in forbidden if token in serialized]
    assert report["guards"]["economic_scoring"] == "DISABLED"
    assert report["guards"]["holdout_scoring"] == "DISABLED"
    assert report["guards"]["order_send"] == "DISABLED"