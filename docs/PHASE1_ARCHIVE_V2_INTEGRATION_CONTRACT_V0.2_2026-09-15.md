# Phase 1 Archive -> 0700 Minimal V2 Integration Contract V0.2 — 2026-09-15

Status: FROZEN_PRE_IMPLEMENTATION / PRE_OUTCOME / HOLDOUT UNSCORED / ORDER SEND DISABLED

Contract ID: `PHASE1_ARCHIVE_V2_INTEGRATION_V0.2`

Depends on:
- `docs/PHASE1_TICK_REPLAY_ENGINEERING_CONTRACT_V0.1_2026-09-15.md`
- `docs/PHASE1_EXNESS_ARCHIVE_WINDOW_ADAPTER_CONTRACT_V0.1_2026-09-15.md`
- `docs/PHASE1_EXNESS_ARCHIVE_WINDOW_ADAPTER_IMPLEMENTATION_V0.1_2026-09-15.md`
- `docs/PHASE1_ARCHIVE_TICK_TO_BAR_CONTRACT_V0.1_2026-09-15.md`
- `docs/PHASE1_ARCHIVE_TICK_TO_BAR_IMPLEMENTATION_V0.1_2026-09-15.md`
- `docs/0700_MINIMAL_V2_FROZEN_SPEC_2026-09-13.md`
- `docs/0700_MINIMAL_V2_PRE_OUTCOME_IMPLEMENTATION_FREEZE_2026-09-13.md`

## Purpose

Define the engineering boundary that allows validated Exness archive data to enter the already-frozen `0700_MINIMAL_V2.0` state machinery without silently changing V2 semantics or converting archive provenance into MT5 identity.

This contract is integration engineering only.
It does not authorize broad historical outcome scoring, holdout reveal, Win Rate, P&L, or order execution.


## V0.2 pre-outcome corrections

V0.2 supersedes V0.1 before any real V2 state replay.

The correction was triggered by interface inspection and synthetic integration work, not by historical strategy outcomes.

Additional frozen invariants:
1. canonical archive->V2 integration requests must start and end on exact 4-hour UTC boundaries;
2. the 4-hour alignment is required because current V2 derives both H4 and M5 from the supplied M1 frame, and a truncated request boundary can otherwise create a partial higher-timeframe bar that looks structurally complete;
3. every supplied archive M1 row must fall inside the requested half-open integration window;
4. every observed M1 source year/month/SHA tuple must be represented by the supplied archive source-month provenance envelope;
5. every M1 row must carry the exact `ARCHIVE_BID_M1_V0.1` representation marker.

No session offset, market tolerance, or warmup duration is introduced by this correction.

## 1. Actual current V2 input graph

The current `build_minimal_v2` implementation consumes normalized M1 OHLC.

Inside the frozen V2 implementation it derives:
- M5 via existing `resample_ohlc(..., "M5")`;
- H4 via existing `resample_ohlc(..., "H4")`.

Current V2 does NOT consume H1, M15, M30 or D1 bars in `build_minimal_v2`.

Therefore this contract must not invent additional timeframe dependencies merely because the project has other MTF research code.

Frozen archive integration graph:

`validated archive window -> ARCHIVE_BID_M1_V0.1 -> existing V2 M5/H4 resample -> frozen 0700_MINIMAL_V2.0`

## 2. M1 input representation

Allowed archive M1 representation:

`ARCHIVE_BID_M1_V0.1`

Required M1 semantics remain those already frozen:
- UTC;
- exact minute labels;
- left-closed/right-open minute intervals;
- Bid OHLC;
- no synthetic empty bars;
- no interpolation;
- no silent deduplication of raw ticks before bar construction.

The V2 integration must not relabel archive-derived M1 as native MT5 M1.

## 3. Frame-based V2 entry point

The existing file-based `build_minimal_v2(m1_path, metadata_path)` must remain behaviorally compatible.

Implementation may add a frame-based entry point so archive M1 can enter without writing a temporary CSV.

Required rule:
- the file-based path becomes a thin loader/metadata wrapper over the same frame-based V2 core;
- existing V2 synthetic/regression results must remain unchanged;
- no detector threshold, PAT rule, target rule, point-check rule, daily-frame rule, action-state rule or 07:00 timing rule may change.

## 4. Provenance envelope

Archive integration outputs must preserve an explicit integration envelope containing at least:
- source family: `EXNESS_BRANDED_ARCHIVE`;
- symbol;
- archive requested start/end UTC;
- archive window status;
- continuity status;
- M1 representation version;
- integration contract version;
- source month list;
- source ZIP SHA-256 list;
- source validator version list;
- origin-history seed status.

Because one integration window may span multiple source ZIPs, a single scalar SHA must not be used to imply a one-file source identity.

Per-row V2 outputs may carry normalized integration metadata columns, while the full source-month/SHA set may live in the report envelope.

## 5. Data-exclusion propagation

The archive-window adapter remains authoritative for:
- known gap intersection;
- earliest coverage boundary;
- incomplete requested horizon;
- missing/non-current validated month;
- invalid/missing local archive file;
- invalid admitted CSV rows.

The integration layer must not catch those exclusions and silently convert them into empty V2 state.

If the archive adapter returns `NO_TICKS_OBSERVED_IN_WINDOW`, the integration must fail closed with an explicit no-data status rather than fabricate M1 or a 07:00 state.

## 6. Origin-history seed problem

Runtime observation from the current frozen V2 implementation:

- H4 origins are created from H4 PAT2 and can remain `ACTIVE` until target completion or point-check destruction.
- There is no frozen fixed expiry horizon for an active origin.
- Therefore no finite `N-day warmup` is currently proven sufficient for a replay window that starts in the middle of history.

Classification:

`STRUCTURAL UNKNOWN / BLOCKING FOR CANONICAL WINDOW-START STATE`

This contract forbids inventing a warmup duration.

Allowed seed states:

### A. SYNTHETIC_COMPLETE

Used only for synthetic/invariant fixtures where the entire relevant origin history is known by construction.

May run the V2 core.

### B. CONTINUATION_CHECKPOINT

A future persisted replay-state checkpoint whose provenance and semantic version are explicitly compatible with the current V2/integration versions.

Not implemented or authorized by this contract yet.

### C. UNSEEDED_REAL_WINDOW

Any real archive window without a compatible prior state checkpoint or independently proven complete origin history.

Must fail closed before producing canonical V2 day/candidate state:

`DATA_EXCLUDED_ORIGIN_HISTORY_UNSEEDED`

Engineering-only bar/resample parity checks are still allowed.

## 7. Earliest archive boundary

The archive begins at the earliest currently observed tick `2015-08-10T00:00:00Z`.

Starting at the earliest archive tick does NOT prove that no H4 origin created before that timestamp was still active.

Therefore the earliest archive boundary is not automatically a valid canonical V2 state reset.

No implicit `NO_PRIOR_ORIGIN` assumption is allowed.

## 8. 07:00 checkpoint handling

Frozen V2 mapping remains:

`07:00 Asia/Bangkok = 00:00 UTC`

The integration does not synthesize an M1 bar at 00:00 UTC if the archive has no observed ticks for that minute.

The existing V2 core may only evaluate cutoffs represented in supplied M1 data.

Absence of a cutoff bar must not be interpreted as a trading signal.

## 9. Higher-timeframe behavior

The integration reuses the existing `resample_ohlc` implementation unchanged for M5/H4 inside V2.

Canonical archive integration request boundaries must be exact 4-hour UTC boundaries. Because 4 hours is also divisible by the current 5-minute rule, this prevents request-edge truncation from creating partial M5 or H4 clock bars.

This is a request-window integrity rule. It is not a claim that every H4 interval contains continuous trading or a tick in every minute.

No new broker-session offset is introduced.

No H4/D1 session-offset inference is made from the bounded archive-vs-MT5 parity sample.

The existing V2 bar-boundary convention remains an engineering representation, not exact broker feed equivalence.

## 10. Bar-level versus tick-level ordering

The V2 core remains bar-based.

Its existing:
- `TARGET_FIRST`;
- `POINT_CHECK_FIRST`;
- `AMBIGUOUS_SAME_BAR`;
- `NEITHER_BY_NEXT_0700`

semantics are not rewritten by this integration.

Tick-level `AMBIGUOUS_SAME_TIMESTAMP` and reference-execution mechanics remain a separate replay lane.

This V0.1 integration must not silently use post hoc tick information to rewrite the frozen V2 bar-state result.

## 11. Output claim boundary

Allowed after synthetic integration tests pass:
- deterministic archive M1 -> V2 input plumbing;
- provenance preservation;
- M5/H4 resample identity relative to the same M1 input;
- V2 state-machine execution on `SYNTHETIC_COMPLETE` fixtures;
- engineering-only parity on already-inspected real windows up to the bar/resample boundary.

Not allowed:
- canonical real-window V2 states from `UNSEEDED_REAL_WINDOW`;
- broad multi-year V2 outcome replay;
- holdout scoring;
- Win Rate / expectancy / profitability;
- broker-fill claims;
- automatic orders.

## 12. Required synthetic/invariant tests

Before any real V2 integration run:
1. file-based and frame-based V2 entry points produce identical outputs on the same synthetic M1 input;
2. archive integration rejects `UNSEEDED_REAL_WINDOW`;
3. archive integration accepts `SYNTHETIC_COMPLETE`;
4. archive window `NO_TICKS_OBSERVED_IN_WINDOW` fails closed;
5. non-`ARCHIVE_BID_M1_V0.1` representation is rejected;
6. unaligned 4-hour request boundaries are rejected;
7. M1 rows outside the requested window are rejected;
8. observed M1 month/SHA provenance must match the source-month envelope;
9. integration envelope preserves source months and all source SHA values;
10. V2 outputs retain integration source/representation/seed-status markers;
11. M5/H4 bars derived through the integration match direct `resample_ohlc` from the same M1 input;
12. no H1/D1 dependency is introduced into current V2;
13. no P&L/Win Rate/broker-fill field is added by integration;
14. existing V2 test suite remains unchanged/pass;
15. archive M1 input is not mutated by V2 integration.

## 13. Real-data engineering validation rule

After synthetic tests pass, real archive validation is limited to already-inspected windows and only up to:
- archive window eligibility;
- archive Bid -> M1;
- M5/H4 deterministic resample/provenance envelope.

Because real archive origin history is currently unseeded, V2 canonical day/candidate state must remain blocked.

## 14. Next unresolved engineering problem

To enable real historical V2 state replay without inventing warmup:

one of the following must be closed pre-outcome:
- a provenance-compatible continuation checkpoint/state-carry mechanism; or
- independently justified complete origin-history initialization.

A fixed arbitrary warmup duration is not an acceptable substitute.

Freeze declaration:

`PHASE1_ARCHIVE_V2_INTEGRATION_V0.2 = FROZEN_PRE_IMPLEMENTATION`
