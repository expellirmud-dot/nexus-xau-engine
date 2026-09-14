# Skill: NEXUS XAU MT5 Data Engineering

Use this skill for MT5/MetaTrader5 data acquisition, capability discovery, historical coverage mapping, runtime metadata capture, forward data collection, data-gap recovery, and small observability/status tooling.

This skill is separate from `nexus-xau-research` because the toolchain and execution contract are materially different. Research meaning remains governed by the research skill and canonical project state.

## Goal

Turn data that MT5 actually exposes into durable, restart-safe, provenance-preserving datasets without inventing unavailable values, silently filling gaps, or drifting into automatic execution.

## Trigger

Use this skill when the task involves one or more of:

- MT5 terminal/API capability inspection;
- symbol/account/runtime specification capture;
- live or historical Bid/Ask ticks;
- OHLC export/resampling;
- historical availability/coverage maps;
- spread or execution-data measurement;
- forward read-only collection;
- restart/gap recovery;
- collector health/status UI;
- deciding whether broker data or an external feed is still needed.

Do not use this skill as authority for trading rules or market interpretation. Route those questions through `nexus-xau-research`.

## Phase 0 — Current-state and tool gate

Before building or changing data tooling:

1. read `AGENTS.md`;
2. read `TOOLS.md`;
3. read `docs/CURRENT_RESEARCH_STATE.json`;
4. read the current MT5/data checkpoint reached from Current State, normally:
   - `docs/PHASE1_PROGRESS_CHECKPOINT_MT5_DATA_ROUTE_2026-09-14.md`;
   - `docs/PHASE1_MT5_CAPABILITY_REPORT_2026-09-14.md`;
5. inspect existing repository data modules before creating a new one;
6. inspect actual local tool capability before declaring the machine/repository unavailable.

For terminal work through IE Coder Connect, inspect `bridge_capabilities` / `terminal_capabilities` first as required by `AGENTS.md`.

## Phase 1 — Reuse and introspection before invention

Before constructing a synthetic value, custom downloader, or duplicate exporter, ask:

1. Does MT5 expose the value directly?
2. Does the MetaTrader5 Python API expose it?
3. Does an existing repository module already export it?
4. Does broker/terminal history expose it for the required interval?
5. Is an external source already registered in `TOOLS.md` or repository data tooling?

Preferred order:

`EXISTING TOOL -> MT5/API OBSERVATION -> HISTORICAL COVERAGE TEST -> EXTERNAL FEED -> SYNTHETIC RESIDUAL MODEL`

Do not create a constant spread or execution-cost assumption while observed Bid/Ask data can still be obtained for the required use.

## Phase 2 — Read-only execution boundary

Default mode is:

`READ-ONLY DATA / ORDER SEND DISABLED`

Normal allowed operations include:

- terminal/account info;
- symbol specification;
- symbol selection;
- live tick reads;
- historical tick/bar reads;
- positions/orders/history reads;
- calculation-only margin/profit functions;
- market-book probing;
- local file persistence and validation.

Automatic order placement is outside this skill.

Do not call or add `order_send()` as part of data acquisition, coverage mapping, collector health, or replay-data engineering.

Any future execution layer requires a separately frozen execution/risk contract and explicit project transition.

## Phase 3 — Data provenance classes

Every dataset/result should identify what it actually is.

Minimum source classes:

- `MT5_LIVE_TICK`
- `MT5_HISTORICAL_TICK`
- `MT5_OHLC`
- `BROKER_RUNTIME_METADATA`
- `ACCOUNT_RUNTIME_METADATA`
- `EXTERNAL_MARKET_DATA`
- `PROJECT_DERIVED`
- `SYNTHETIC_ENGINEERING_FIXTURE`

Keep broker-specific data separate from external-feed data.

Never silently substitute Dukascopy or another provider as Exness execution truth.

For runtime metadata, record enough environment identity to reproduce the interpretation without storing passwords or secrets.

## Phase 4 — Historical coverage mapping

Do not infer coverage from one successful date.

Map OHLC and Bid/Ask tick history separately.

A reproducible coverage scan should record at minimum:

- symbol;
- source/terminal environment;
- requested UTC interval;
- data class: tick or timeframe;
- returned row/tick count;
- first/last returned timestamp;
- expected versus observed interval where an expectation is defined;
- duplicate/non-monotonic count;
- status: `AVAILABLE / EMPTY / PARTIAL / ERROR`;
- error code/message when present.

Rules:

- `OHLC_AVAILABLE` does not imply `BID_ASK_TICKS_AVAILABLE`;
- zero rows with API success means no data returned for that request, not proof that the broker never had data;
- network/auth/path failure is a route failure, not proof the data does not exist;
- distinguish weekends/market closure from unexpected gaps;
- do not inspect protected holdout outcomes merely to map data availability.

Coverage artifacts should be deterministic and rerunnable.

## Phase 5 — Runtime-observable values

Do not classify a value as structurally missing merely because it is unknown before the event occurs.

Examples of runtime-observable values:

- Bid/Ask at a future timestamp;
- spread at the moment of observation;
- account equity/margin at runtime;
- a post-checkpoint confirmation state;
- runtime broker specification if the environment changes.

Represent the dependency as:

`known acquisition method + not-yet-arrived value`

not:

`unknown formula`.

If the value becomes available only later, the engine/collector should wait, observe, then continue.

## Phase 6 — Raw-first collection and resampling

When practical, preserve the highest-value raw observation first.

For Phase 1 execution-data work:

`raw Bid/Ask ticks -> validated chronological store -> derived M1 -> derived M5/H1/H4 as needed`

Do not throw away tick data merely because the research engine currently consumes M1/M5.

Derived bars must preserve provenance to the raw/source dataset and resampling rule.

If native broker bars are compared with derived bars, treat agreement/mismatch as a validation result rather than silently choosing one.

## Phase 7 — Restart-safe forward collector contract

A forward collector must assume that MT5, the PC, the Bridge, or the collector can stop.

Minimum durable state:

- symbol/source identity;
- last successfully persisted tick timestamp, preferably millisecond precision;
- storage partition/file identity;
- collector version/schema;
- last successful flush/checkpoint;
- gap ledger;
- error/status record.

Restart sequence:

1. load durable checkpoint;
2. initialize MT5 and verify runtime identity;
3. request the interval after the last persisted tick;
4. deduplicate by stable timestamp/data identity;
5. verify chronological order;
6. append unseen observations;
7. record any unrecoverable interval as an explicit gap;
8. resume forward collection.

Do not silently interpolate or fabricate missing ticks.

## Phase 8 — Observation window versus storage window

Research scope and storage scope are different.

Phase 1 may make a decision around one checkpoint while the collector stores a wider window or all available ticks for baseline/control purposes.

The exact high-priority observation window must come from the research dependency, not convenience.

A wider storage window does not by itself authorize broader trading decisions.

## Phase 9 — Minimal status surface

A full custom trading UI is not required.

When operational visibility becomes useful, prefer a small status surface showing:

- MT5 connected/disconnected;
- collector running/stopped;
- explicit `READ-ONLY / ORDER SEND DISABLED`;
- symbol;
- latest Bid/Ask and tick timestamp;
- latest durable checkpoint;
- rows/ticks collected;
- configured observation window;
- gap detected yes/no;
- last error;
- collector/schema version.

The status surface is observability only. It must not become an implicit execution controller.

## Phase 10 — Validation and persistence

Before checkpointing data-engineering changes:

1. validate structured output;
2. test chronology, deduplication, timezone normalization, and restart behavior;
3. test empty/partial/error paths;
4. run relevant unit tests/lint;
5. run repository research preflight when current project state/readiness changed;
6. update the current MT5 capability/progress document when evidence changed;
7. update `CURRENT_RESEARCH_STATE.json` when next action or current capability changed;
8. update readiness/construction matrices when a blocker materially changes;
9. run Git hygiene checks;
10. commit/push one coherent checkpoint.

## Hard-stop rules

Stop and record the limitation rather than inventing when:

- MT5 returns no historical ticks for a required interval and no validated alternate feed/model exists;
- source/feed identity is ambiguous;
- timezone mapping is uncertain;
- duplicate/non-monotonic data cannot be reconciled;
- runtime account/symbol identity does not match the intended environment;
- protected holdout access would be required merely to inspect outcomes;
- an execution-cost assumption would be chosen because it improves historical results;
- a proposed collector change introduces order placement.

## Output style

For MT5/data work report:

1. capability/request tested;
2. exact observed result;
3. provenance/environment;
4. what this proves;
5. what it does not prove;
6. gap/blocking impact;
7. next reproducible probe/action;
8. checkpoint status.
