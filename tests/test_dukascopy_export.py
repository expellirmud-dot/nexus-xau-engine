from __future__ import annotations

import lzma
import struct
from datetime import date

import pytest

from nexus_xau.data.dukascopy_export import (
    decode_dukascopy_m1_bi5,
    dukascopy_m1_day_url,
    price_divisor_for_symbol,
)


def _payload(*records: tuple[int, int, int, int, int, float]) -> bytes:
    raw = b"".join(struct.pack(">5If", *record) for record in records)
    return lzma.compress(raw)


def test_dukascopy_url_uses_zero_based_month() -> None:
    url = dukascopy_m1_day_url(
        symbol="XAU/USD",
        day=date(2022, 9, 1),
        side="bid",
    )
    assert url == (
        "https://datafeed.dukascopy.com/datafeed/"
        "XAUUSD/2022/08/01/BID_candles_min_1.bi5"
    )


def test_xauusd_price_divisor_is_explicitly_registered() -> None:
    assert price_divisor_for_symbol("XAUUSD") == 1000.0


def test_unknown_symbol_requires_explicit_divisor() -> None:
    with pytest.raises(ValueError, match="No verified price divisor"):
        price_divisor_for_symbol("SOMETHING")


def test_decode_m1_candle_layout_and_price_scale() -> None:
    payload = _payload(
        (0, 1712000, 1712500, 1711500, 1713000, 12.5),
        (60, 1712500, 1712200, 1711800, 1712800, 9.25),
    )
    frame = decode_dukascopy_m1_bi5(
        payload,
        day=date(2022, 9, 1),
        price_divisor=1000.0,
    )

    assert len(frame) == 2
    assert frame.iloc[0]["timestamp"].isoformat() == "2022-09-01T00:00:00+00:00"
    assert frame.iloc[1]["timestamp"].isoformat() == "2022-09-01T00:01:00+00:00"
    assert frame.iloc[0]["open"] == 1712.0
    assert frame.iloc[0]["close"] == 1712.5
    assert frame.iloc[0]["low"] == 1711.5
    assert frame.iloc[0]["high"] == 1713.0
    assert frame.iloc[0]["volume"] == pytest.approx(12.5)


def test_decode_rejects_impossible_seconds_offset() -> None:
    payload = _payload((86_400, 1712000, 1712500, 1711500, 1713000, 1.0))
    with pytest.raises(ValueError, match="Invalid seconds"):
        decode_dukascopy_m1_bi5(
            payload,
            day=date(2022, 9, 1),
            price_divisor=1000.0,
        )
