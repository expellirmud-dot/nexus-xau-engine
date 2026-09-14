# Phase 1 MT5 Forward Collector Pilot — 2026-09-14

Status: IMPLEMENTED / SHORT DEMO RESTART VALIDATED
Mode: READ-ONLY DATA / ORDER SEND DISABLED
Symbol: XAUUSDm

## Contract and implementation

Contract:
- docs/PHASE1_MT5_FORWARD_COLLECTOR_CONTRACT_V0.1_2026-09-14.md
- docs/PHASE1_MT5_FORWARD_COLLECTOR_CONTRACT_V0.1.json
- commit 697e4d0

Implementation:
- src/nexus_xau/data/mt5_tick_collector.py
- scripts/mt5_tick_collector.py
- tests/test_mt5_tick_collector.py

Relevant commits:
- 57427dd implement collector
- 3824cfc stop treating empty tick response as automatic gap
- b7f6ad6 expose BLOCKED source mismatch and API ERROR states

## Storage

Local canonical store:
- data/raw/mt5/XAUUSDm_ticks.sqlite3

Status:
- results/mt5_collector/status.json

Observed:
- SQLite integrity_check = ok
- journal_mode = wal
- synchronous = FULL
- runtime snapshots contain non-secret metadata only
- no login/password/token/API-key fields persisted

## Failed pilot preserved

The first pilot incorrectly recorded an empty tick response as PENDING_SESSION_CONTEXT.

That was a representation error: zero ticks does not prove a gap.

The pre-fix pilot was preserved locally:
- data/raw/mt5/pilot_archive/XAUUSDm_ticks_pre_empty_gap_fix.sqlite3
- results/mt5_collector/pilot_archive/status_pre_empty_gap_fix.json

## Validation

Final MT5 data suite:
- 20 tests PASS
- Ruff PASS

Validated behavior includes:
- raw repeated tick preservation
- atomic tick + state commit
- shared-millisecond multiplicity-aware restart handling
- chronology rejection
- source mismatch -> BLOCKED
- API failure -> API_ERROR + ERROR status
- empty tick response does not create false gap
- atomic status.json
- no order-send call

## Clean live Demo pilot

Run 1, fresh store:
- 67 ticks committed
- gaps: none
- final boundary: 1789386709415

Run 2, restart without start time:
- 93 ticks committed
- total: 160
- prior boundary remained exactly 1 row
- gaps: none

Run 3, later restart/backfill:
- 765 ticks committed
- total: 925
- prior boundaries 1789386709415 and 1789386739778 remained exactly 1 row each
- gaps: none
- source identity unchanged across 3 runtime snapshots
- SQLite integrity: ok
- final time_msc: 1789386971170

Interpretation:
The collector resumed from durable SQLite state and backfilled the stopped interval without duplicating prior checkpoint boundaries.

## Current conclusion

Forward Collector V0.1 status:

IMPLEMENTED_SHORT_DEMO_RESTART_VALIDATED

This does not prove indefinite 24/7 reliability, full historical recoverability, multi-year execution data, economic performance, or execution readiness.

Automatic order execution remains disabled.

## Next

- optionally run a longer read-only durable collection
- build a minimal status surface from status.json / SQLite
- resolve the multi-year execution-quality data path separately
- continue toward the pre-outcome Phase 1 replay engineering contract
