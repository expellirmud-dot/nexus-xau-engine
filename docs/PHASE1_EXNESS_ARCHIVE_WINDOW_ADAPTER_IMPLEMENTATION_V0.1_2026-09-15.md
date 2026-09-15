# Phase 1 Exness Archive Window Adapter Implementation V0.1 — 2026-09-15

Status: IMPLEMENTED / SYNTHETIC PASS / FULL REGRESSION PASS / REAL-ARCHIVE ENGINEERING SMOKE PASS / NO STRATEGY OUTCOME OPENED

Contract:
`docs/PHASE1_EXNESS_ARCHIVE_WINDOW_ADAPTER_CONTRACT_V0.1_2026-09-15.md`

Implementation:
`src/nexus_xau/replay/archive_window.py`

Synthetic tests:
`tests/test_archive_window_replay.py`

## Purpose

Implement the frozen archive-window adapter without network download, extraction, deduplication, interpolation, or strategy scoring.
## Implemented behavior

- UTC timezone-aware half-open windows: `[start,end)`;
- month selection for every calendar month intersecting the requested interval;
- current Validator V0.2 manifest gating;
- local ZIP existence and byte-size verification;
- streaming directly from the ZIP CSV;
- exact required CSV header enforcement;
- provider/symbol/finite Bid/Ask/Ask>=Bid checks on admitted rows;
- raw row ordinal preservation within each monthly CSV;
- source year/month, SHA-256, local path and validator version provenance;
- exact duplicate rows preserved;
- equal timestamps preserved;
- source order preserved;
- timestamp regression rejected;
- known-gap ledger enforcement;
- current earliest/latest acquisition boundary enforcement;
- explicit empty-window status instead of inferring market closure or missing data.
## Synthetic validation

Targeted Ruff:
`PASS`

Targeted pytest:
`11 passed`

Covered:
- half-open boundary behavior;
- multi-month selection;
- missing/non-current validator manifest rejection;
- raw ordinal preservation;
- duplicate preservation;
- equal-timestamp preservation;
- open-interval known-gap exclusion and endpoint eligibility;
- earliest/latest coverage boundary failure;
- explicit empty-window status;
- manifest SHA/month provenance;
- local file size mismatch exclusion.
## Repository regression

Broader Ruff:
`python -m ruff check src tests scripts`

Result:
`PASS`

Full repository pytest:
`PASS`

Progress reached 100%.
Only pre-existing/deprecation-class warnings were emitted.

## Real archive engineering smoke

Source month:
`2026-08`

Requested window:
`[2026-08-02T22:01:30Z, 2026-08-02T22:01:46Z)`
Observed:
- adapter status: `OK`;
- continuity marker: `KNOWN_GAPS_ENFORCED_FULL_CONTINUITY_NOT_PROVEN`;
- admitted rows: 100;
- first timestamp: `2026-08-02T22:01:30.647Z`;
- last timestamp: `2026-08-02T22:01:45.299Z`;
- first/last raw ordinal: 0 / 99;
- source month: 2026-08;
- source SHA prefix: `baa514c5a942`;
- duplicate timestamps present and preserved: true.

This is an engineering smoke on an already-inspected representative month. It does not expose a strategy signal, target/stop result, P&L, Win Rate, or broker-fill claim.

## Interpretation

The adapter now provides bounded, provenance-preserving Bid/Ask windows to the frozen tick replay primitives while enforcing known acquisition boundaries and the explicit 2016 boundary-gap candidate.
Absence of a known-gap entry does not prove full continuity.

Automatic order sending remains disabled.
V0.1 holdout outcome scoring remains disabled.
Exact archive-to-current-MT5 feed equivalence remains unproven.

## Next bounded task

Before broad historical replay, freeze and validate the tick-to-bar reconstruction/parity layer needed to feed the existing 0700_MINIMAL_V2.0 bar/state machinery from archive Bid ticks.

The next step should first compare deterministic archive-derived bar construction against already-inspected overlapping MT5/bar evidence, without selecting rules from strategy outcomes and without opening protected holdout scoring.
