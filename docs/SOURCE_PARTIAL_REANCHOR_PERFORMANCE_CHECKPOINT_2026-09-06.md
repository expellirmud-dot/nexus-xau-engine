# Source-Partial Re-Anchor Performance Checkpoint — 2026-09-06

Status: ENGINEERING OPTIMIZATION / REQUIRES LOCAL RUNTIME VALIDATION

## Trigger

Project-owner Windows runtime reached:

```text
124 passed, 116 warnings
Ruff: All checks passed!
[3/3] source-partial re-anchored remaining-run + Daily-side retest
```

but then produced no period result for several hours.

## Root cause found in implementation

The frozen re-anchor selector previously evaluated every candidate against eligible origins newest-to-oldest. For each candidate-origin pair it repeatedly sliced M1 to compute:

- consumed points at cutoff;
- consumed points at candidate;
- structural destruction before candidate.

This caused repeated large DataFrame scans and created a severe performance path. The issue is engineering/runtime complexity, not a research-result observation.

## Optimization

`source_partial_reanchored_remaining_run.py` now precomputes, once per origin:

- first nominal H1 1,000-point completion timestamp;
- first strict structural destruction timestamp;
- origin start position in active M1.

The runtime selector then tests those cached timestamps against the frozen cutoff/candidate boundaries instead of slicing M1 repeatedly for every candidate-origin pair.

The reference selector remains in the module. A test was added requiring the cached selector to return the same origin as the reference selector on the existing re-anchor fixture.

The multi-period batch also now prints progress at:

- period START;
- REANCHOR_DONE with the impact summary;
- DAILY_SIDE_DONE with the period state.

## Research semantics unchanged

This optimization does **not** change:

- H1 PAT2-BODY origin representation;
- latest-to-oldest same-direction search order;
- `anchor_known_at <= cutoff_utc` eligibility;
- nominal H1 target = 1,000 project points;
- incomplete-at-cutoff and incomplete-at-candidate conditions;
- BUY destruction: later Low < origin anchor;
- SELL destruction: later High > origin anchor;
- interval semantics `[origin_anchor_known_at, end)`;
- equality as non-destruction in this frozen representation;
- no 200-point buffer;
- no age/expiry/consumed-run threshold;
- PATH_REMAINING or Daily Frame side rules;
- frozen cross-period decision rule.

For timestamp events exactly at cutoff/candidate, cached checks use strict `< end`, preserving the original half-open interval behavior.

## Validation boundary

The earlier `124 passed` and Ruff pass occurred before this optimization. Therefore the optimized implementation is not yet claimed runtime-passing.

Next local command:

```powershell
cd D:\nexus-xau-engine-repo
git pull
.\scripts\run_source_partial_reanchored_daily_side.ps1
```

If an earlier Python process from the pre-optimization run is still active, stop that old run before starting the new one so two full research batches do not compete for CPU/RAM.
