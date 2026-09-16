from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from typing import Any

from nexus_xau.data.mt5_tick_collector import source_identity_from_runtime

CONTRACT = "PHASE1_MT5_COST_TREATMENT_EVIDENCE_V0.1"
SYMBOL = "XAUUSDm"
HISTORY_START_UTC = datetime(1970, 1, 1, tzinfo=UTC)


class CostEvidenceError(RuntimeError):
    pass


def _as_mapping(value: Any) -> dict[str, Any]:
    if isinstance(value, Mapping):
        return {str(key): item for key, item in value.items()}
    asdict = getattr(value, "_asdict", None)
    if callable(asdict):
        return {str(key): item for key, item in asdict().items()}
    names = getattr(value, "_fields", None)
    if names:
        return {str(name): getattr(value, name) for name in names}
    raise TypeError(f"cannot convert {type(value).__name__} to mapping")


def select_swap_metadata(symbol_info: Any) -> dict[str, Any]:
    payload = _as_mapping(symbol_info)
    result: dict[str, Any] = {"name": payload.get("name")}
    for key in sorted(key for key in payload if key.startswith("swap_")):
        result[key] = payload[key]
    return result


def _empty_component_summary() -> dict[str, Any]:
    return {
        "observed_count": 0,
        "nonzero_count": 0,
        "minimum": None,
        "maximum": None,
        "sum_observed": None,
    }


def _numeric_summary(values: Sequence[Any]) -> dict[str, Any]:
    numbers = [float(value) for value in values]
    if not numbers:
        return _empty_component_summary()
    return {
        "observed_count": len(numbers),
        "nonzero_count": sum(value != 0.0 for value in numbers),
        "minimum": min(numbers),
        "maximum": max(numbers),
        "sum_observed": sum(numbers),
    }


def summarize_deal_costs(
    deals: Sequence[Any],
    *,
    symbol: str = SYMBOL,
) -> dict[str, Any]:
    mappings = [_as_mapping(deal) for deal in deals]
    field_names = sorted({key for row in mappings for key in row})
    target = [row for row in mappings if str(row.get("symbol", "")) == symbol]
    cost_fields = ("commission", "fee", "swap")

    presence = {
        field: (field in field_names if mappings else None)
        for field in cost_fields
    }
    summaries: dict[str, dict[str, Any]] = {}
    for field in cost_fields:
        if not presence[field] or not target:
            summaries[field] = _empty_component_summary()
            continue
        values = [row[field] for row in target if row.get(field) is not None]
        summaries[field] = _numeric_summary(values)

    if not mappings:
        schema_status = "NO_DEALS_OBSERVED"
        observation_status = "NO_COST_SAMPLES_OBSERVED"
    elif not target:
        schema_status = "OBSERVED"
        observation_status = "NO_XAUUSDM_DEALS_OBSERVED"
    else:
        schema_status = "OBSERVED"
        observation_status = "XAUUSDM_COST_SAMPLES_OBSERVED"

    return {
        "schema_status": schema_status,
        "deal_count_total": len(mappings),
        "symbol_deal_count": len(target),
        "field_names": field_names,
        "cost_field_presence": presence,
        "observation_status": observation_status,
        "cost_summaries": summaries,
    }

def build_cost_evidence(
    *,
    source_identity: str,
    source_identity_payload: Mapping[str, Any],
    observed_at_utc: str,
    swap_metadata: Mapping[str, Any],
    history_status: str,
    history_last_error: Sequence[Any] | None,
    deals: Sequence[Any] | None,
) -> dict[str, Any]:
    if not source_identity:
        raise CostEvidenceError("source_identity is required")
    if not observed_at_utc:
        raise CostEvidenceError("observed_at_utc is required")
    if history_status not in {"PASS", "FAIL"}:
        raise CostEvidenceError(f"invalid history_status: {history_status}")

    if history_status == "FAIL":
        deal_evidence = {
            "schema_status": "UNKNOWN_API_FAILURE",
            "deal_count_total": None,
            "symbol_deal_count": None,
            "field_names": [],
            "cost_field_presence": {
                "commission": None,
                "fee": None,
                "swap": None,
            },
            "observation_status": "UNKNOWN_API_FAILURE",
            "cost_summaries": {
                field: _empty_component_summary()
                for field in ("commission", "fee", "swap")
            },
        }
    else:
        deal_evidence = summarize_deal_costs(deals or ())

    return {
        "contract": CONTRACT,
        "observed_at_utc": observed_at_utc,
        "source_identity": source_identity,
        "source_context": {
            "company": source_identity_payload.get("company"),
            "server": source_identity_payload.get("server"),
            "trade_mode": source_identity_payload.get("trade_mode"),
            "currency": source_identity_payload.get("currency"),
            "symbol": source_identity_payload.get("symbol"),
            "collector_version": source_identity_payload.get("collector_version"),
        },
        "current_symbol_financing_metadata": {
            "status": "KNOWN_NOW_CURRENT_RUNTIME",
            "symbol": swap_metadata.get("name"),
            "swap_fields": {
                key: value
                for key, value in sorted(swap_metadata.items())
                if key.startswith("swap_")
            },
            "interpretation_guard": (
                "CURRENT_RUNTIME_SPECIFICATION_NOT_HISTORICAL_COST_SCHEDULE"
            ),
        },
        "account_deal_cost_schema": {
            "history_api_status": history_status,
            "history_interval_start_utc": HISTORY_START_UTC.isoformat(),
            "history_interval_end_utc": observed_at_utc,
            "history_last_error": (
                None
                if history_last_error is None
                else [str(item) for item in history_last_error]
            ),
            **deal_evidence,
        },
        "historical_replay_cost_schedule": {
            "status": "UNRESOLVED_CURRENT_RUNTIME_EVIDENCE_NOT_HISTORICAL_SCHEDULE",
            "zero_cost_assumption_permitted": False,
        },
        "guards": {
            "order_send": "DISABLED",
            "holdout_scoring": "DISABLED",
            "economic_scoring": "DISABLED",
            "fill_slippage_inference": "DISABLED",
        },
    }


def probe_mt5_cost_evidence(
    mt5: Any,
    *,
    symbol: str = SYMBOL,
    observed_at: datetime | None = None,
) -> dict[str, Any]:
    observation_time = observed_at or datetime.now(UTC)
    if observation_time.tzinfo is None:
        observation_time = observation_time.replace(tzinfo=UTC)
    else:
        observation_time = observation_time.astimezone(UTC)
    observed_at_utc = observation_time.isoformat(timespec="seconds")

    if not mt5.initialize():
        code, message = mt5.last_error()
        raise CostEvidenceError(f"MT5 initialize failed: {code} {message}")

    try:
        if not mt5.symbol_select(symbol, True):
            code, message = mt5.last_error()
            raise CostEvidenceError(f"Cannot select symbol {symbol}: {code} {message}")

        source_identity, identity_payload = source_identity_from_runtime(mt5, symbol)
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            code, message = mt5.last_error()
            raise CostEvidenceError(f"symbol_info failed: {code} {message}")
        swap_metadata = select_swap_metadata(symbol_info)

        deals_payload = mt5.history_deals_get(HISTORY_START_UTC, observation_time)
        if deals_payload is None:
            history_status = "FAIL"
            last_error = mt5.last_error()
            deals = None
        else:
            history_status = "PASS"
            last_error = mt5.last_error()
            deals = list(deals_payload)

        return build_cost_evidence(
            source_identity=source_identity,
            source_identity_payload=identity_payload,
            observed_at_utc=observed_at_utc,
            swap_metadata=swap_metadata,
            history_status=history_status,
            history_last_error=last_error,
            deals=deals,
        )
    finally:
        mt5.shutdown()