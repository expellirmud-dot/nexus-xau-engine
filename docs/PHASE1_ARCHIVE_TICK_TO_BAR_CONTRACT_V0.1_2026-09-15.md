# Phase 1 Archive Tick-to-Bar Reconstruction Contract V0.1 — 2026-09-15

Status: FROZEN_PRE_IMPLEMENTATION / PRE_OUTCOME / NO HOLDOUT SCORING

Contract ID: `PHASE1_ARCHIVE_TICK_TO_BAR_V0.1`

Depends on:
- `docs/PHASE1_TICK_REPLAY_ENGINEERING_CONTRACT_V0.1_2026-09-15.md`
- `docs/PHASE1_EXNESS_ARCHIVE_WINDOW_ADAPTER_CONTRACT_V0.1_2026-09-15.md`
- `docs/PHASE1_EXNESS_ARCHIVE_WINDOW_ADAPTER_IMPLEMENTATION_V0.1_2026-09-15.md`
- existing `src/nexus_xau/data/resample.py`

## Purpose

Freeze deterministic construction of M1 geometry bars from validated archive Bid ticks before broad historical replay.
This contract does not change 0700_MINIMAL_V2.0 signal semantics and does not select outcomes.
## M1 source and quote

Engineering convention:
`ARCHIVE_M1_GEOMETRY_QUOTE = BID`

This inherits the frozen tick replay contract.

Ask is retained for reference-execution/spread diagnostics and is not mixed into geometry OHLC.

Archive-derived M1 bars carry archive provenance and are not relabeled as native MT5 bars.

## M1 interval semantics

Canonical minute interval:
`[minute_start_utc, minute_start_utc + 1 minute)`

- UTC;
- label left;
- closed left;
- origin `start_day`;
- canonical reconstruction requests must start and end on exact UTC minute boundaries.
For one minute:
- open = first Bid in stable source order;
- high = maximum Bid;
- low = minimum Bid;
- close = last Bid in stable source order.

Equal timestamps remain allowed.
Exact duplicate rows remain preserved in the tick layer.
Duplicate removal is not performed before bar construction.

Source order gives deterministic first/last when timestamps tie, but it is not promoted to proof of physical market micro-order.

## Empty minutes and gaps

- no forward fill;
- no interpolation;
- no synthetic OHLC bar for a minute with zero admitted archive ticks;
- known-gap and acquisition-boundary exclusions remain the responsibility of the archive-window adapter;
- absence of a known-gap record is not proof of full continuity.
## Partial boundary bars

Canonical M1 reconstruction rejects unaligned requested boundaries rather than emitting silently partial boundary bars.

A source month may itself begin/end mid-minute. Such boundary minutes must not be used as canonical parity evidence unless the requested interval contains the full minute under the frozen acquisition snapshot.

## Volume

Archive CSV has no canonical MT5 tick-volume field.

A diagnostic `archive_tick_count` may be emitted as the number of admitted raw rows in a minute.

It must not be renamed to or claimed equivalent to MT5 `tick_volume`.
It is not used to change frozen V2 geometry semantics.

## Higher timeframes

M1 -> M5/M15/M30/H1/H4/D1 construction continues to use the existing `resample_ohlc` implementation.
The existing higher-timeframe convention remains:
- label left;
- closed left;
- default origin `start_day`;
- no broker-session offset is invented by this contract.

This contract does not reopen already frozen V2 signal rules or source-derived Daily Frame semantics.

## Descriptive parity evidence before freeze

Compared already-available MT5 M1 export against archive Bid-derived M1 for:
`2026-08-02T22:02:00Z` through `2026-08-02T23:02:00Z`

Observed:
- archive ticks: 7,857;
- archive M1 bars: 60;
- common MT5 M1 timestamps: 60;
- bars with at least one exact OHLC mismatch: 50.
Exact component matches out of 60:
- open: 41;
- high: 39;
- low: 32;
- close: 35.

Maximum observed absolute component differences in this bounded sample:
- open: 0.326;
- high: 0.252;
- low: 0.127;
- close: 0.252.

Interpretation:
The bounded sample is consistent with the same UTC left-labeled minute boundary structure.
It does not establish exact feed/server/price equivalence.
No tolerance threshold is inferred from these differences.
Archive-derived bars therefore remain a separate research representation with explicit provenance.

## Required synthetic tests

Before real archive bar smoke:
1. minute-aligned boundaries accepted;
2. unaligned start/end rejected;
3. left-closed/right-open assignment;
4. Bid first/max/min/last OHLC;
5. equal-timestamp stable source-order open/close;
6. exact duplicates preserved in archive_tick_count;
7. empty minute produces no bar;
8. no forward fill/interpolation;
9. archive provenance survives bar output;
10. Ask changes alone do not alter geometry OHLC.
## Real-data validation rule

After synthetic tests pass, perform bounded engineering parity only on already-inspected archive/MT5 overlap.

Report exact timestamp/component matches and raw differences descriptively.
Do not choose or tune a tolerance from those observations.
Do not convert cross-feed disagreement into strategy outcome information.

Automatic order sending remains disabled.
V0.1 holdout outcome scoring remains disabled.

Freeze declaration:
`PHASE1_ARCHIVE_TICK_TO_BAR_V0.1 = FROZEN_PRE_IMPLEMENTATION`
