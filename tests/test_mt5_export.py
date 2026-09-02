from datetime import timezone

import pytest

from nexus_xau.data.mt5_export import parse_aware_datetime


def test_parse_aware_datetime_normalizes_to_utc() -> None:
    parsed = parse_aware_datetime("2026-08-24T07:00:00+07:00")
    assert parsed.tzinfo == timezone.utc
    assert parsed.isoformat() == "2026-08-24T00:00:00+00:00"


def test_parse_aware_datetime_refuses_naive_value() -> None:
    with pytest.raises(ValueError, match="must include timezone"):
        parse_aware_datetime("2026-08-24T00:00:00")
