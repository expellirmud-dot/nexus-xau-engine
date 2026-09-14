# Phase 1 Progress Checkpoint — MT5 Data Route and Next Work

Date: 2026-09-14
Time: 16:57 Asia/Bangkok
Status: ACTIVE PROJECT PROGRESS CHECKPOINT
Scope: Phase 1

## Why this checkpoint exists

This document is a human-readable resume point.

It records:
- what the Project is doing now;
- what has been established;
- what remains uncertain;
- what should happen next;
- what must not be assumed.

It is not a market-rule authority and does not replace the canonical claim register.

## Current Project position

Phase 1 research logic is advanced enough that the immediate bottleneck is no longer "we do not know what information to look for."

The Project now knows many of the required information classes and can separate:

- values already known;
- values directly observable from MT5;
- values derived from observed data;
- values only available when a future/runtime condition occurs;
- structural unknowns that waiting will not resolve;
- values irrelevant to the current decision.

This means many remaining gaps are now data-acquisition, representation, and relationship-testing problems rather than completely undefined research questions.

## MT5 route — what is established

The current Exness Demo / MT5 environment is connected and readable through the MetaTrader5 Python integration.

Confirmed read-only capabilities include:

- terminal/account metadata;
- XAUUSDm symbol specification;
- live Bid/Ask;
- historical Bid/Ask ticks for multiple tested dates;
- M1/M5/H1/H4/D1 OHLC;
- current positions and pending/open orders;
- historical deals/orders;
- account-specific margin and profit calculations.

Depth of Market was not available through the current XAUUSDm market-book probe.

Primary evidence:
- docs/PHASE1_MT5_CAPABILITY_REPORT_2026-09-14.md

## Historical server/data interpretation

What is confirmed:

MT5 terminal/Python can request historical bars and historical Bid/Ask ticks that are available to the connected terminal environment.

What is NOT yet established:

- a separate direct Exness server endpoint/API that the Project can connect to independently of the MT5 terminal;
- the full retention depth of historical Bid/Ask ticks;
- continuity/completeness of every historical interval.

Therefore:

Do not describe a direct broker-server historical API as available until it is separately demonstrated.

The working route is currently:

Broker/feed -> MT5 terminal history environment -> MetaTrader5 Python API -> Project.

## Important history-depth observation

OHLC and tick-history depth are different.

Observed examples:

- historical Bid/Ask ticks returned for 2026-06-15, 2026-06-30, 2026-07-01 and 2026-08-24;
- tick probes for 2026-06-01 returned zero rows;
- M1 bars were still retrievable for older dates such as 2026-04-01 and 2025-09-15.

Therefore:

A successful OHLC history request does NOT establish execution-quality Bid/Ask tick availability for the same period.

## Forward data collector — intended role

A future collector should be READ-ONLY and separate from any execution/auto-trading layer.

Its purpose is to preserve runtime-observable market data, especially data that may not remain available indefinitely from broker history.

The collector should be restart-safe.

Minimum intended behavior:

1. read new XAUUSDm Bid/Ask ticks;
2. persist raw ticks with millisecond timestamps;
3. maintain a durable last-seen tick timestamp/checkpoint;
4. after restart, request the missing interval from MT5 history when available;
5. record any unrecoverable missing interval in an explicit gap ledger;
6. derive M1/M5 or other summaries from raw data rather than discarding raw ticks;
7. show a small status surface so the owner can tell whether collection is running.

The collector may have configurable observation windows around the Phase 1 checkpoint, but the exact pre/post window must be declared from the research need rather than invented from convenience.

If the machine is running outside the primary window, storing additional ticks can still be useful as a baseline/control dataset. That does not broaden Phase 1's decision scope by itself.

## Restart / shutdown doctrine

Closing MT5 or shutting down the PC is not automatically a data failure.

On restart:

- read the durable collector checkpoint;
- ask MT5 for ticks after the last stored time;
- append only unseen ticks;
- validate chronology and duplicates;
- record gaps that MT5 cannot recover.

This means the Project should prefer recoverable interval collection over assuming a continuously running process will never stop.

## UI boundary

A full custom trading UI is not required for Phase 1.

A minimal collector status UI may later show:

- MT5 connected/disconnected;
- collector running/stopped;
- symbol;
- latest Bid/Ask;
- latest tick time;
- rows/ticks collected;
- current configured observation window;
- last durable checkpoint;
- gap detected yes/no;
- last error;
- explicit READ-ONLY / ORDER SEND DISABLED state.

Notification and execution are separate future layers.

Automatic order placement remains deferred until research, replay, economic validation, and supervised testing are sufficiently mature.

## Current unresolved items

1. Map historical Bid/Ask tick coverage and completeness systematically.
2. Map OHLC history depth/completeness separately.
3. Determine whether any direct broker/server historical interface exists beyond the confirmed MT5 terminal route.
4. Decide the exact Phase 1 forward observation window from evidence/research dependency, not convenience.
5. Implement a restart-safe read-only collector only after inspecting/reusing existing repository data tooling.
6. Freeze the Phase 1 replay engineering contract before outcome scoring.
7. Keep holdout outcome scoring disabled unless separately authorized.

## Immediate next work

The next engineering/research sequence is:

1. build a reproducible MT5 historical coverage map for XAUUSDm;
2. record available/missing tick intervals separately from OHLC availability;
3. use that map to decide what must be collected forward and what can be recovered historically;
4. specify the read-only collector contract, including durable checkpoint and gap ledger;
5. only then implement the smallest collector/status surface needed;
6. return to Phase 1 replay-contract closure with real data capabilities now known.

## Do not regress to these older assumptions

Do not state that MT5 authorization is still failing.

Do not assume spread must be synthetic before attempting observed Bid/Ask data.

Do not equate M1/OHLC availability with Bid/Ask tick completeness.

Do not treat runtime-observable future values as structural blockers merely because their value is not known in advance.

Do not let a collector or status UI become an auto-trading system.

## Resume sentence

We are in Phase 1. MT5 read-only access and historical Bid/Ask retrieval are working. The current task is to map historical data coverage, then specify a restart-safe read-only forward collector with explicit gap recovery, before freezing the remaining replay/execution-data contract. Holdout scoring remains disabled.
