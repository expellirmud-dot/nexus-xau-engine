from nexus_xau.data.mt5_collector_corner import summarize_corner


def test_summarize_corner_market_and_pipeline_fields() -> None:
    payload = {
        "state": "RUNNING",
        "symbol": "XAUUSDm",
        "latest_bid": 4295.962,
        "latest_ask": 4296.202,
        "latest_committed_tick_time_msc": 1_000_000,
        "total_ticks": 4571,
        "gap_counts": {},
        "last_error": None,
        "mode": "READ_ONLY_DATA_ORDER_SEND_DISABLED",
        "updated_at_utc": "1970-01-01T00:16:44+00:00",
    }

    view = summarize_corner(payload, now_ms=1_004_000)

    assert view["state"] == "RUNNING"
    assert view["quote"] == "4295.962 / 4296.202"
    assert view["spread"] == "0.240"
    assert view["age"] == "4.0s"
    assert view["ticks"] == "4571"
    assert view["status_age"] == "0.0s"
    assert view["gaps"] == "{}"
    assert view["error"] == "NONE"


def test_summarize_corner_gap_summary() -> None:
    payload = {
        "state": "ERROR",
        "gap_counts": {"API_ERROR": 2},
        "last_error": "copy failed",
    }

    view = summarize_corner(payload, now_ms=0)

    assert view["state"] == "ERROR"
    assert view["gaps"] == "API_ERROR:2"
    assert view["error"] == "copy failed"


def test_summarize_corner_marks_stale_runtime_status() -> None:
    payload = {
        "state": "RUNNING",
        "updated_at_utc": "1970-01-01T00:00:00+00:00",
        "gap_counts": {},
    }

    view = summarize_corner(payload, now_ms=20_000)

    assert view["state"] == "STALE"
    assert view["status_age"] == "20.0s"
