from __future__ import annotations

from datetime import timedelta

import numpy as np
import pandas as pd

from nexus_xau.research.minimal_v2_0700 import (
    H4Origin,
    _normalize_m1_frame,
    origin_state_at,
)

CONTRACT = "PHASE1_EXNESS_PREHISTORY_FORWARD_CLOSURE_V0.1"
HYPOTHESIS = "FINITE_FORWARD_EXNESS_CAN_CLOSE_UNBOUNDED_UNKNOWN_PREHISTORY"


class PrehistoryClosureError(ValueError):
    pass


def _active_m1(frame: pd.DataFrame) -> pd.DataFrame:
    normalized = _normalize_m1_frame(frame)
    if "volume" in normalized.columns:
        normalized = normalized.loc[normalized["volume"] > 0].copy()
    if normalized.empty:
        raise PrehistoryClosureError("observed active M1 path is empty")
    return normalized


def construct_surviving_counterexamples(
    active_m1: pd.DataFrame,
) -> tuple[H4Origin, H4Origin, pd.Timestamp]:
    """Construct BUY/SELL unknown-prehistory origins outside finite observed extrema."""

    frame = _active_m1(active_m1)
    observed_max_high = float(frame["high"].max())
    observed_min_low = float(frame["low"].min())
    if not np.isfinite(observed_max_high) or not np.isfinite(observed_min_low):
        raise PrehistoryClosureError("observed extrema must be finite")
    if observed_min_low <= 0:
        raise PrehistoryClosureError("XAU closure proof expects strictly positive observed prices")

    buy_anchor = float(np.nextafter(observed_max_high, np.inf))
    sell_anchor = float(np.nextafter(observed_min_low, -np.inf))
    if sell_anchor <= 0:
        raise PrehistoryClosureError("constructed SELL anchor must remain positive")

    origin_known_at = frame.index[0] - timedelta(microseconds=1)
    pattern_known_at = origin_known_at - timedelta(hours=4)
    at = frame.index[-1] + timedelta(microseconds=1)

    buy = H4Origin(
        origin_id="HYPOTHETICAL_PREHISTORY:BUY",
        side="BUY",
        pattern_known_at=pattern_known_at,
        origin_known_at=origin_known_at,
        anchor_price=buy_anchor,
    )
    sell = H4Origin(
        origin_id="HYPOTHETICAL_PREHISTORY:SELL",
        side="SELL",
        pattern_known_at=pattern_known_at,
        origin_known_at=origin_known_at,
        anchor_price=sell_anchor,
    )
    return buy, sell, at


def evaluate_finite_forward_closure(active_m1: pd.DataFrame) -> dict[str, object]:
    frame = _active_m1(active_m1)
    buy, sell, at = construct_surviving_counterexamples(frame)
    buy_state, buy_consumed, _, buy_touch = origin_state_at(
        active_m1=frame, origin=buy, at=at
    )
    sell_state, sell_consumed, _, sell_touch = origin_state_at(
        active_m1=frame, origin=sell, at=at
    )
    counterexamples_survive = buy_state == "ACTIVE" and sell_state == "ACTIVE"
    return {
        "contract": CONTRACT,
        "hypothesis": HYPOTHESIS,
        "hypothesis_result": "FALSIFIED" if counterexamples_survive else "NOT_FALSIFIED",
        "path_start_utc": frame.index[0].isoformat(),
        "path_last_bar_utc": frame.index[-1].isoformat(),
        "observed_max_high": float(frame["high"].max()),
        "observed_min_low": float(frame["low"].min()),
        "buy_counterexample": {
            "anchor_price": buy.anchor_price,
            "state": buy_state,
            "consumed_points": buy_consumed,
            "point_check_touch_at": None if buy_touch is None else buy_touch.isoformat(),
        },
        "sell_counterexample": {
            "anchor_price": sell.anchor_price,
            "state": sell_state,
            "consumed_points": sell_consumed,
            "point_check_touch_at": None if sell_touch is None else sell_touch.isoformat(),
        },
        "finite_forward_complete_seed_authorized": False,
        "independent_anchor_domain_required": counterexamples_survive,
    }