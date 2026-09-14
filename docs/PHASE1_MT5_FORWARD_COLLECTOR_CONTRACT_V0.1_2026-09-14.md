# Phase 1 MT5 Forward Collector Contract V0.1 — 2026-09-14

Status: FROZEN PRE-IMPLEMENTATION ENGINEERING CONTRACT
Scope: Phase 1
Mode: READ-ONLY DATA / ORDER SEND DISABLED
Symbol: XAUUSDm

## Why collection is required

Current MT5/Python coverage evidence establishes:

- current-route historical Bid/Ask ticks begin at 2026-03-12T00:00:00.255Z;
- this window is much shorter than the Project's multi-year research horizon;
- the retention boundary may move over time;
- current Python-visible M1 depth is separately limited by terminal `maxbars=100000`.

Therefore forward collection is:

- NON-BLOCKING for current state/path research;
- REQUIRED LATER for durable broker-specific Bid/Ask/execution evidence;
- useful now because data not archived locally may become unavailable later.

Reference:

`docs/PHASE1_MT5_HISTORY_COVERAGE_MAP_2026-09-14.md`

## Observation window decision

No narrow clock window is frozen.

Reason:

Phase 1 uses information legitimately knowable before the 07:00 Asia/Bangkok checkpoint, and post-checkpoint confirmation can be event-driven. Current source authority does not establish one exact pre/post collection interval.

V0.1 storage scope is therefore:

**store all observed/recoverable XAUUSDm ticks while the collector is operating or backfilling.**

This is an engineering storage convention, not an expansion of the trading scope.

Phase 1 decision scope remains narrow and still uses only information legally available at the relevant decision time.

## Primary data

Preserve raw MT5 tick fields when present:

- `time`
- `time_msc`
- `bid`
- `ask`
- `last`
- `volume`
- `flags`
- `volume_real`

Spread is derived as `ask - bid`; it does not need to be stored as a separate source truth.

Do not replace raw ticks with M1/M5 summaries.

M1/M5/H1/H4 may be derived later with declared resampling rules.

## Storage authority

V0.1 canonical local store:

`data/raw/mt5/XAUUSDm_ticks.sqlite3`

SQLite is selected because it is available in the Python standard library and can atomically commit:

- tick rows;
- durable collector state;
- runtime/source metadata;
- gap records.

No new external database dependency is required.

Database durability settings for V0.1:

- WAL journal mode;
- foreign keys enabled;
- synchronous FULL;
- explicit transactions for every persisted batch.

The SQLite database is local data and remains gitignored.

## Tick preservation rule

Do NOT define a global UNIQUE constraint over tick values.

Reason:

Multiple legitimate feed events may share the same millisecond timestamp and may even have identical visible values. The Project does not have a broker-supplied immutable tick ID.

Raw repeated rows must not be silently collapsed.

## Restart / overlap rule

Collector state and tick writes must commit in the same SQLite transaction.

State includes at minimum:

- schema version;
- symbol;
- source identity;
- last committed `time_msc`;
- a multiset representation of raw rows at the last committed millisecond;
- last successful commit time;
- last runtime/source snapshot reference.

On restart:

1. initialize MT5;
2. verify runtime/source identity;
3. read the durable SQLite state;
4. request history beginning at the last committed millisecond inclusively;
5. compare rows at that boundary against the stored multiset;
6. skip only the multiplicity already committed;
7. preserve any additional identical rows;
8. preserve all later rows in feed order;
9. commit ticks + new state atomically.

This avoids both silent duplicates and accidental loss of multiple ticks sharing one millisecond.

## Initial startup

If no collector state exists:

- V0.1 starts forward from an explicit operator/CLI start time;
- it must not silently attempt a six-month historical archive;
- historical bulk backfill is a separate explicit durable job.

This keeps forward collection deterministic and prevents a first launch from unexpectedly downloading a very large history.

## Backfill after normal restart

If state exists:

- request the interval after the last committed boundary up to the current acquisition point;
- use bounded requests so long gaps do not require one unbounded in-memory tick response;
- persist each successful batch transactionally;
- resume forward acquisition after the gap is processed.

Exact chunk size/poll interval are implementation parameters, not market rules. They must be validated for reliability/performance before being treated as frozen operational defaults.

## Gap ledger

Gap records are durable and append-only in meaning.

Minimum fields:

- detected_at_utc;
- requested_start_msc;
- requested_end_msc;
- source identity;
- recovery attempt count;
- returned first/last tick if any;
- MT5 error code/message if any;
- status;
- note.

Allowed statuses include:

- `RECOVERED`
- `PENDING_SESSION_CONTEXT`
- `UNRECOVERABLE_CURRENT_ROUTE`
- `API_ERROR`

An empty interval is not automatically fabricated or automatically called a market-data failure. Weekend/session/holiday context may be required.

## Runtime/source provenance

On startup and whenever source identity changes, record a runtime snapshot containing non-secret fields such as:

- terminal build;
- MetaTrader5 package version when available;
- broker/company;
- server;
- Demo/Real trade mode;
- account currency;
- leverage;
- symbol;
- symbol digits/point/contract size;
- volume min/max/step;
- execution mode;
- current collector version.

Do not persist:

- password;
- API key;
- authentication token;
- private credential material.

Account login identifier is not required for the collector evidence contract.

## Source mismatch rule

If the runtime source no longer matches the expected configured source identity:

- do not silently merge data into the same provenance stream;
- set collector status to BLOCKED_SOURCE_IDENTITY_MISMATCH;
- require explicit new provenance/session handling before resuming.

## Status surface

V0.1 must expose a small machine-readable status file:

`results/mt5_collector/status.json`

Minimum fields:

- collector state: STARTING / BACKFILLING / RUNNING / STOPPED / BLOCKED / ERROR;
- explicit `READ_ONLY_DATA_ORDER_SEND_DISABLED`;
- symbol;
- source identity summary;
- latest committed tick time;
- latest observed Bid/Ask;
- total rows committed this session;
- last successful commit;
- current backfill interval if any;
- gap count by status;
- last error;
- collector version.

A later UI may read this file/database. The status surface is observability only and cannot send orders.

## Execution safety boundary

V0.1 collector:

- may initialize/read MT5;
- may select/read XAUUSDm;
- may call historical/live tick read APIs;
- may read terminal/account/symbol metadata;
- may write local collector storage/status.

V0.1 collector MUST NOT:

- call `order_send`;
- open/close/modify positions;
- place pending orders;
- change account trading settings;
- infer ENTER/BUY/SELL from collected data;
- score protected holdout outcomes.

## Validation required before operational use

Implementation must test:

1. SQLite schema creation;
2. tick insertion preserving repeated identical rows;
3. atomic tick+state transaction;
4. restart at a shared millisecond boundary;
5. multiplicity-aware boundary deduplication;
6. chronological validation;
7. timezone handling;
8. empty/API-error handling;
9. source-identity mismatch handling;
10. gap ledger persistence;
11. status file atomic update;
12. explicit absence of order-send behavior.

Then run a short supervised live Demo collection before treating the collector as operational.

## Multi-year boundary

This collector preserves future broker-specific evidence.

It does NOT solve missing broker Bid/Ask history before 2026-03-12.

Multi-year execution/economic proof remains a separate decision:

- validated external execution-quality feed; or
- an explicitly declared residual execution model with clear provenance/limitations.

Do not confuse forward collection success with multi-year economic proof.

## Next implementation step

Implement the smallest V0.1 collector against this contract, test restart behavior locally, then run a short read-only Demo pilot.

Automatic trading remains out of scope.
