from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import pandas as pd

BarHandler = Callable[[pd.Timestamp, pd.Series], None]


@dataclass(frozen=True, slots=True)
class ReplayStats:
    bars_processed: int
    first_timestamp: pd.Timestamp | None
    last_timestamp: pd.Timestamp | None


class ReplayEngine:
    """Feed historical closed bars to handlers in strict timestamp order."""

    def run(self, bars: pd.DataFrame, *handlers: BarHandler) -> ReplayStats:
        if not isinstance(bars.index, pd.DatetimeIndex) or bars.index.tz is None:
            raise ValueError("Replay bars must use a timezone-aware DatetimeIndex")
        if bars.index.has_duplicates:
            raise ValueError("Replay bars contain duplicate timestamps")
        if not bars.index.is_monotonic_increasing:
            raise ValueError("Replay bars must be sorted oldest to newest")

        first = bars.index[0] if len(bars) else None
        last = bars.index[-1] if len(bars) else None

        for timestamp, bar in bars.iterrows():
            for handler in handlers:
                handler(timestamp, bar)

        return ReplayStats(len(bars), first, last)
