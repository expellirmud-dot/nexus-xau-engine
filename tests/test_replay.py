import pandas as pd
import pytest

from nexus_xau.replay.engine import ReplayEngine


def _bars() -> pd.DataFrame:
    index = pd.date_range("2026-01-01T00:00:00Z", periods=3, freq="1min")
    return pd.DataFrame(
        {
            "open": [1.0, 2.0, 3.0],
            "high": [2.0, 3.0, 4.0],
            "low": [0.5, 1.5, 2.5],
            "close": [1.5, 2.5, 3.5],
        },
        index=index,
    )


def test_replay_preserves_order() -> None:
    seen = []
    stats = ReplayEngine().run(_bars(), lambda timestamp, _bar: seen.append(timestamp))
    assert stats.bars_processed == 3
    assert seen == sorted(seen)


def test_replay_rejects_unsorted_input() -> None:
    bars = _bars().sort_index(ascending=False)
    with pytest.raises(ValueError, match="oldest to newest"):
        ReplayEngine().run(bars)
