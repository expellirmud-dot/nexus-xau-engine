from __future__ import annotations

import pandas as pd
import pytest

from nexus_xau.research.sw_proxy_variant_relation_test import _sw_shape_features


def _frame(closes: list[float], *, width: float = 2.0) -> pd.DataFrame:
    index = pd.date_range("2026-01-01T00:00:00Z", periods=len(closes), freq="1h")
    return pd.DataFrame(
        {
            "open": closes,
            "high": [value + width / 2 for value in closes],
            "low": [value - width / 2 for value in closes],
            "close": closes,
        },
        index=index,
    )


def test_oscillation_strength_is_high_for_back_and_forth_path() -> None:
    features = _sw_shape_features(_frame([100, 101, 100, 101, 100, 101]))
    assert features["oscillation_strength"] == pytest.approx(0.8)
    assert features["direction_flip_rate"] == pytest.approx(1.0)


def test_oscillation_strength_is_zero_for_one_way_path() -> None:
    features = _sw_shape_features(_frame([100, 101, 102, 103, 104, 105]))
    assert features["oscillation_strength"] == pytest.approx(0.0)
    assert features["direction_flip_rate"] == pytest.approx(0.0)


def test_candle_overlap_rate_is_normalized_and_bounded() -> None:
    features = _sw_shape_features(_frame([100.0, 100.5, 100.0], width=2.0))
    overlap = features["candle_overlap_rate"]
    assert isinstance(overlap, float)
    assert 0.0 <= overlap <= 1.0
    assert overlap == pytest.approx(0.75)


def test_flat_close_path_has_undefined_direction_features_but_valid_overlap() -> None:
    features = _sw_shape_features(_frame([100, 100, 100]))
    assert features["oscillation_strength"] is None
    assert features["direction_flip_rate"] is None
    assert features["candle_overlap_rate"] == pytest.approx(1.0)
