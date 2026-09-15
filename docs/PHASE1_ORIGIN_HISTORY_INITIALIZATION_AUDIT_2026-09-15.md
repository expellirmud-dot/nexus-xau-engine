# Phase 1 Origin-History Initialization Audit — 2026-09-15

Status: CHECKPOINT / PRE-OUTCOME / HOLDOUT UNSCORED / ORDER SEND DISABLED

## Purpose

Audit the existing pre-2015 historical-source/tooling route for a defensible initialization of the frozen `0700_MINIMAL_V2.0` H4-origin state.

This checkpoint does not authorize historical outcome scoring and does not change any V2 market rule.

## Starting authority

Reconnect state before this audit:

- repo: `main@9a27a84`, clean;
- workstream: `0700_METHOD_COMPLETION`;
- no active durable job;
- current blocker: `DATA_EXCLUDED_ORIGIN_HISTORY_UNSEEDED`;
- Exness archive earliest observed tick: `2015-08-10T00:00:00Z`.

Research preflight passed before checkpointing this audit.

## Existing tooling reused

The repository already contains:

- `src/nexus_xau/data/dukascopy_export.py`;
- `src/nexus_xau/data/dukascopy_cache_export.py`;
- `docs/DUKASCOPY_MULTIYEAR_DATA_PIPELINE_2026-09-03.md`.

No new downloader was created.
## Dukascopy pre-2015 bounded probes

The existing BID M1 downloader has no code-level 2022 start restriction. The prior 2022 start was local acquired coverage, not a downloader boundary.

Decoded one-day probes succeeded with 1,440 M1 rows and zero acquisition failures on:

- `2015-08-07`;
- `2014-01-02`;
- `2010-01-04`;
- `2005-01-03`;
- `2004-01-05`;
- `2003-06-02`.

Therefore a real pre-Exness-archive Dukascopy XAUUSD BID M1 route is runtime-proven at least as far back as `2003-06-02` in this bounded audit.

Additional older probes must be classified carefully:

- `2003-01-06`: acquisition FAILED, not NO_DATA;
- `2002-01-07`: one direct HTTP probe returned HTTP 200 with bytes, but repeated pipeline acquisition/decoding still ended FAILED;
- network timeout/failure is not a historical no-data boundary.

Safe classification for `2002-01-07` is `AVAILABILITY_HINTED_ACQUISITION_UNRESOLVED`, not validated coverage.

## Cross-feed boundary

Dukascopy remains a separate research feed from the Exness-branded archive and current MT5 route.

A pre-2015 Dukascopy history must not be concatenated with Exness and silently represented as one feed.

Any future cross-feed initialization requires explicit provenance and a representation-sensitivity check for whether feed differences change H4 PAT detection, origin anchors, or active-origin state at the Exness boundary.
## Why pre-2015 history does not yet solve initialization

Frozen V2 source/implementation semantics were rechecked.

- H4 origins are multi-instance and may remain active independently.
- There is no frozen age expiry or newest-wins rule.
- An origin terminates when its nominal run completes first, its literal M1 point-check contact occurs first, or same-bar terminal ordering is ambiguous.
- The source closure does not authorize automatically falling back from a destroyed newest origin to an older same-timeframe origin as a canonical winner rule.

Starting Dukascopy earlier therefore moves the unknown initial-state boundary backward; it does not by itself prove that no still-active origin predates the new start.

## Rejected shortcut: arbitrary or range-based reset

No fixed `N-day` warmup is introduced.

A possible cumulative-range reset was examined but not promoted.

Reason: frozen point-check semantics require literal M1 price-range contact with the anchor. A price gap that jumps across an anchor without an M1 bar whose range contains that anchor is not equivalent to a point-check contact under V2. Therefore a simple observed-range-width condition is not a proven complete-state reset.

Classification:

- pre-2015 Dukascopy source route: `KNOWN NOW / NON-BLOCKING`; 
- exact earliest reliable Dukascopy acquisition boundary: `UNRESOLVED / NON-BLOCKING FOR CURRENT AUDIT`;
- complete initial active H4-origin state: `STRUCTURAL UNKNOWN / BLOCKING FOR CANONICAL REAL V2 STATE`.

## Checkpoint conclusion

`DATA_EXCLUDED_ORIGIN_HISTORY_UNSEEDED` remains the correct fail-closed result for canonical real archive V2 state.

No real V2 strategy outcome was opened, no holdout score was revealed, and automatic order send remains disabled.
## Next bounded action

Do not bulk-download Dukascopy yet.

Next engineering/research step:

1. determine whether a provenance-compatible state-carry representation can be constructed from explicitly observed origin instances without assuming a clean initial boundary;
2. if cross-feed Dukascopy initialization is still considered, first design a bounded sensitivity test comparing Dukascopy-derived versus Exness-derived H4 PAT/origin state on their overlapping period;
3. freeze that initialization/state-carry contract before any canonical real V2 state or strategy outcome is produced;
4. if no defensible initialization route closes the recursion, preserve `DATA_EXCLUDED_ORIGIN_HISTORY_UNSEEDED` rather than inventing a warmup.

Evidence classification remains source/observation/derived separated. Successful historical probes establish source availability only; they do not establish feed equivalence or strategy validity.
## Validation

- `scripts/research_preflight.py`: PASS after Current State update.
- `docs/CURRENT_RESEARCH_STATE.json`: JSON parse PASS.
- `git diff --check`: PASS.
- targeted `test_archive_v2_integration.py + test_minimal_v2_0700.py`: 30/30 PASS when rerun with repository-local `--basetemp`.
- the first targeted pytest invocation had one fixture setup error from Windows `%TEMP%` access (`WinError 5`); 29 tests had otherwise run. This was an environment temp-directory failure, not a V2 logic failure.

Checkpoint timestamp: `2026-09-15T18:29:53+07:00`.