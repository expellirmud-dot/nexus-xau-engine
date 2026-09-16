from __future__ import annotations

import pytest

from nexus_xau.data.mt5_cost_evidence import (
    CostEvidenceError,
    build_cost_evidence,
    select_swap_metadata,
    summarize_deal_costs,
)


def _identity_payload():
    return {
        "company": "Exness Technologies Ltd",
        "server": "Exness-MT5Trial6",
        "trade_mode": 0,
        "currency": "USD",
        "symbol": "XAUUSDm",
        "collector_version": "PHASE1_MT5_FORWARD_COLLECTOR_V0.1",
    }


def _build(**overrides):
    values = {
        "source_identity": "a" * 64,
        "source_identity_payload": _identity_payload(),
        "observed_at_utc": "2026-09-17T00:00:00+00:00",
        "swap_metadata": {
            "name": "XAUUSDm",
            "swap_long": -534.9,
            "swap_short": 0.0,
            "swap_mode": 1,
        },
        "history_status": "PASS",
        "history_last_error": (1, "Success"),
        "deals": [],
    }
    values.update(overrides)
    return build_cost_evidence(**values)


def test_swap_metadata_selection_is_deterministic_by_field_name() -> None:
    selected = select_swap_metadata(
        {
            "swap_short": 0.0,
            "name": "XAUUSDm",
            "trade_tick_size": 0.001,
            "swap_long": -534.9,
            "swap_mode": 1,
        }
    )
    assert list(selected) == ["name", "swap_long", "swap_mode", "swap_short"]


def test_deal_schema_is_visible_without_market_deal() -> None:
    result = summarize_deal_costs(
        [
            {
                "symbol": "",
                "commission": 0.0,
                "fee": 0.0,
                "swap": 0.0,
                "profit": 500.0,
            }
        ]
    )
    assert result["schema_status"] == "OBSERVED"
    assert result["symbol_deal_count"] == 0
    assert result["cost_field_presence"] == {
        "commission": True,
        "fee": True,
        "swap": True,
    }
    assert result["observation_status"] == "NO_XAUUSDM_DEALS_OBSERVED"


def test_empty_successful_history_is_not_zero_cost_evidence() -> None:
    report = _build(deals=[])
    schema = report["account_deal_cost_schema"]
    assert schema["schema_status"] == "NO_DEALS_OBSERVED"
    assert schema["cost_field_presence"] == {
        "commission": None,
        "fee": None,
        "swap": None,
    }
    for summary in schema["cost_summaries"].values():
        assert summary["observed_count"] == 0
        assert summary["sum_observed"] is None
    assert report["historical_replay_cost_schedule"]["zero_cost_assumption_permitted"] is False


def test_cost_summaries_use_xauusdm_deals_only() -> None:
    result = summarize_deal_costs(
        [
            {"symbol": "XAUUSDm", "commission": -0.1, "fee": 0.0, "swap": -1.5},
            {"symbol": "EURUSDm", "commission": -9.0, "fee": -3.0, "swap": -99.0},
            {"symbol": "XAUUSDm", "commission": -0.2, "fee": -0.05, "swap": 0.0},
        ]
    )
    assert result["symbol_deal_count"] == 2
    assert result["cost_summaries"]["commission"] == {
        "observed_count": 2,
        "nonzero_count": 2,
        "minimum": -0.2,
        "maximum": -0.1,
        "sum_observed": pytest.approx(-0.3),
    }
    assert result["cost_summaries"]["fee"]["sum_observed"] == pytest.approx(-0.05)
    assert result["cost_summaries"]["swap"]["sum_observed"] == pytest.approx(-1.5)


def test_output_does_not_persist_trade_outcome_values() -> None:
    report = _build(
        deals=[
            {
                "symbol": "XAUUSDm",
                "commission": -0.1,
                "fee": 0.0,
                "swap": 0.0,
                "profit": 1234.0,
                "price": 9999.0,
                "type": 1,
            }
        ]
    )
    schema = report["account_deal_cost_schema"]
    assert "deal_records" not in schema
    assert set(schema["cost_summaries"]) == {"commission", "fee", "swap"}
    serialized = repr(report)
    assert "1234.0" not in serialized
    assert "9999.0" not in serialized


def test_history_api_failure_remains_unknown_not_empty_success() -> None:
    report = _build(
        history_status="FAIL",
        history_last_error=(-1, "history failed"),
        deals=None,
    )
    schema = report["account_deal_cost_schema"]
    assert schema["schema_status"] == "UNKNOWN_API_FAILURE"
    assert schema["deal_count_total"] is None
    assert schema["symbol_deal_count"] is None
    assert schema["cost_field_presence"]["commission"] is None


def test_source_identity_is_required() -> None:
    with pytest.raises(CostEvidenceError, match="source_identity is required"):
        _build(source_identity="")


def test_fixed_guards_disable_execution_holdout_and_economic_scoring() -> None:
    report = _build()
    assert report["guards"] == {
        "order_send": "DISABLED",
        "holdout_scoring": "DISABLED",
        "economic_scoring": "DISABLED",
        "fill_slippage_inference": "DISABLED",
    }


def test_current_swap_metadata_never_promotes_historical_schedule() -> None:
    report = _build()
    assert report["current_symbol_financing_metadata"]["status"] == (
        "KNOWN_NOW_CURRENT_RUNTIME"
    )
    assert report["historical_replay_cost_schedule"]["status"] == (
        "UNRESOLVED_CURRENT_RUNTIME_EVIDENCE_NOT_HISTORICAL_SCHEDULE"
    )

class _FakeMT5:
    def __init__(self, *, history_result):
        from collections import namedtuple
        from types import SimpleNamespace

        self._history_result = history_result
        self._shutdown = False
        self._terminal = SimpleNamespace(build=6182)
        self._account = SimpleNamespace(
            company="Exness Technologies Ltd",
            server="Exness-MT5Trial17",
            trade_mode=0,
            currency="USD",
            leverage=500,
        )
        SymbolInfo = namedtuple(
            "SymbolInfo",
            [
                "name",
                "digits",
                "point",
                "trade_contract_size",
                "volume_min",
                "volume_max",
                "volume_step",
                "trade_exemode",
                "swap_long",
                "swap_short",
                "swap_mode",
                "swap_rollover3days",
            ],
        )
        self._symbol = SymbolInfo(
            "XAUUSDm",
            3,
            0.001,
            100.0,
            0.01,
            200.0,
            0.01,
            2,
            -547.6,
            0.0,
            1,
            3,
        )

    def initialize(self):
        return True

    def symbol_select(self, symbol, selected):
        return symbol == "XAUUSDm" and selected

    def terminal_info(self):
        return self._terminal

    def account_info(self):
        return self._account

    def symbol_info(self, symbol):
        return self._symbol if symbol == "XAUUSDm" else None

    def history_deals_get(self, start, end):
        return self._history_result

    def last_error(self):
        return (-1, "history failed") if self._history_result is None else (1, "Success")

    def shutdown(self):
        self._shutdown = True


def test_runtime_probe_success_uses_read_only_schema_path() -> None:
    from datetime import UTC, datetime

    from nexus_xau.data.mt5_cost_evidence import probe_mt5_cost_evidence

    mt5 = _FakeMT5(
        history_result=(
            {"symbol": "", "commission": 0.0, "fee": 0.0, "swap": 0.0},
        )
    )
    result = probe_mt5_cost_evidence(
        mt5, observed_at=datetime(2026, 9, 17, tzinfo=UTC)
    )
    assert result["account_deal_cost_schema"]["history_api_status"] == "PASS"
    assert result["account_deal_cost_schema"]["symbol_deal_count"] == 0
    assert result["source_context"]["server"] == "Exness-MT5Trial17"
    assert mt5._shutdown is True


def test_runtime_probe_api_failure_is_preserved_and_shutdown_occurs() -> None:
    from datetime import UTC, datetime

    from nexus_xau.data.mt5_cost_evidence import probe_mt5_cost_evidence

    mt5 = _FakeMT5(history_result=None)
    result = probe_mt5_cost_evidence(
        mt5, observed_at=datetime(2026, 9, 17, tzinfo=UTC)
    )
    schema = result["account_deal_cost_schema"]
    assert schema["history_api_status"] == "FAIL"
    assert schema["schema_status"] == "UNKNOWN_API_FAILURE"
    assert schema["deal_count_total"] is None
    assert mt5._shutdown is True