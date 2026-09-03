import pandas as pd
import pytest

from nexus_xau.research.outcomes import FirstHit, OutcomeSpec, measure_outcome


def _bars(rows: list[tuple[float, float, float, float]]) -> pd.DataFrame:
    index = pd.date_range("2026-01-01T00:00:00Z", periods=len(rows), freq="1min")
    return pd.DataFrame(rows, columns=["open", "high", "low", "close"], index=index)


def test_buy_target_first_and_excursions() -> None:
    bars = _bars(
        [
            (100.0, 100.5, 99.8, 100.2),
            (100.2, 101.2, 100.1, 101.0),
            (101.0, 102.5, 100.9, 102.0),
        ]
    )
    outcome = measure_outcome(
        bars,
        OutcomeSpec(
            side="BUY",
            reference_price=100.0,
            known_at=bars.index[0],
            horizon_end=bars.index[-1],
            point_size=0.1,
            target_points=10,
            stop_points=5,
        ),
    )
    assert outcome.first_hit is FirstHit.TARGET_FIRST
    assert outcome.mfe_points == pytest.approx(25)
    assert outcome.mae_points == pytest.approx(2)
    assert outcome.end_return_points == pytest.approx(20)


def test_sell_stop_first() -> None:
    bars = _bars(
        [
            (100.0, 100.8, 99.8, 100.5),
            (100.5, 101.2, 100.0, 100.7),
        ]
    )
    outcome = measure_outcome(
        bars,
        OutcomeSpec(
            side="SELL",
            reference_price=100.0,
            known_at=bars.index[0],
            horizon_end=bars.index[-1],
            point_size=0.1,
            target_points=10,
            stop_points=5,
        ),
    )
    assert outcome.first_hit is FirstHit.STOP_FIRST
    assert outcome.mfe_points == pytest.approx(2)
    assert outcome.mae_points == pytest.approx(12)


def test_same_bar_target_and_stop_is_ambiguous() -> None:
    bars = _bars([(100.0, 101.5, 98.5, 100.0)])
    outcome = measure_outcome(
        bars,
        OutcomeSpec(
            side="BUY",
            reference_price=100.0,
            known_at=bars.index[0],
            horizon_end=bars.index[0],
            point_size=0.1,
            target_points=10,
            stop_points=10,
        ),
    )
    assert outcome.first_hit is FirstHit.AMBIGUOUS_SAME_BAR
    assert outcome.target_hit_at == bars.index[0]
    assert outcome.stop_hit_at == bars.index[0]


def test_bars_before_known_at_are_excluded() -> None:
    bars = _bars(
        [
            (100.0, 120.0, 80.0, 100.0),
            (100.0, 100.4, 99.7, 100.2),
            (100.2, 100.6, 100.0, 100.4),
        ]
    )
    outcome = measure_outcome(
        bars,
        OutcomeSpec(
            side="BUY",
            reference_price=100.0,
            known_at=bars.index[1],
            horizon_end=bars.index[-1],
            point_size=0.1,
        ),
    )
    assert outcome.mfe_points == pytest.approx(6)
    assert outcome.mae_points == pytest.approx(3)
    assert outcome.bars_observed == 2
