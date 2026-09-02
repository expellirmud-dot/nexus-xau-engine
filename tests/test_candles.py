import pytest

from nexus_xau.engine.candles import CandleDirection, CandleFeatures


def test_candle_features_geometry() -> None:
    candle = CandleFeatures(open=100.0, high=106.0, low=98.0, close=104.0)

    assert candle.direction is CandleDirection.BULLISH
    assert candle.range == 8.0
    assert candle.body == 4.0
    assert candle.upper_wick == 2.0
    assert candle.lower_wick == 2.0
    assert candle.body_fraction_of_range == 0.5
    assert candle.body_midpoint == 102.0
    assert candle.full_range_midpoint == 102.0


def test_zero_range_body_fraction_is_none() -> None:
    candle = CandleFeatures(open=100.0, high=100.0, low=100.0, close=100.0)

    assert candle.direction is CandleDirection.DOJI
    assert candle.body_fraction_of_range is None


def test_invalid_ohlc_is_rejected() -> None:
    with pytest.raises(ValueError):
        CandleFeatures(open=100.0, high=99.0, low=98.0, close=101.0)
