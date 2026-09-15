# Phase 1 Exness Prehistory Forward-Closure Result V0.1 — 2026-09-16

Status: HYPOTHESIS FALSIFIED / FINITE FORWARD WARMUP CANNOT PROVE COMPLETE SEED WITHOUT ANCHOR DOMAIN / HOLDOUT UNSCORED / ORDER SEND DISABLED

Contract: `docs/PHASE1_EXNESS_PREHISTORY_FORWARD_CLOSURE_CONTRACT_V0.1_2026-09-16.md`
Implementation: `src/nexus_xau/replay/prehistory_forward_closure.py`
Tests: `tests/test_exness_prehistory_forward_closure.py`

## Tested hypothesis

`FINITE_FORWARD_EXNESS_CAN_CLOSE_UNBOUNDED_UNKNOWN_PREHISTORY`

Result: `FALSIFIED`.

## Derived proof

For any non-empty finite observed M1 path:

- let `H` be the finite observed maximum high;
- let `L` be the finite observed minimum low;
- construct a hypothetical pre-start BUY anchor as the next representable float above `H`;
- construct a hypothetical pre-start SELL anchor as the next representable float below `L`.

Under frozen lifecycle semantics:

- the BUY anchor is above every observed bar, so no observed bar literally touches it and the BUY target is even higher;
- the SELL anchor is below every observed bar, so no observed bar literally touches it and the SELL target is even lower;
- both hypothetical origins therefore remain `ACTIVE` through the finite path.

Extending the path only changes finite extrema. A new pair of anchors can always be constructed outside the new finite extrema.
## Constructibility check

The counterexample is not merely an arbitrary `H4Origin` object.

A supplemental synthetic test builds frozen H4 PAT2 -> adjacent post-SIG origin sequences whose BUY/SELL anchors equal the constructed outside-range values, then confirms the same anchors are valid under the existing `build_h4_origins()` mapping.

Because pre-archive history is unobserved, a subsequent gap can place the observed Exness path wholly on the other side of the anchor without an observed bar spanning it. Under literal-contact semantics that gap does not destroy the origin.

## Test evidence

- contract falsification tests: 5/5 PASS;
- relevant regression with Minimal V2, Archive-to-V2 integration, and V2 state carry: 64/64 PASS;
- targeted Ruff: PASS;
- broader Ruff `src tests scripts`: PASS.

Full repository durable pytest `XAU-PREHISTORY-CLOSURE-FULLPYTEST-20260916`: DONE, one attempt, exit code 0, persisted progress log = 379/379 PASS.

## Decision implication

An arbitrary finite warmup duration cannot become evidence for `COMPLETE` seed state under the current frozen lifecycle semantics.

Waiting longer does not resolve this unknown in principle. Without an independent constraint on possible pre-start anchors, the unknown is therefore **STRUCTURAL / BLOCKING**, not merely runtime-observable.

The project must not use:

- arbitrary N-day/N-month/N-year warmup;
- absence of observed failures as proof of closure;
- invented origin expiry;
- assumed continuity across the unobserved archive boundary.

## What could change the conclusion

A COMPLETE seed could become defensible only if additional evidence closes at least one missing premise, for example:

- same-source Exness history extending sufficiently before the current archive boundary;
- an independently justified finite domain containing every possible active pre-start Exness anchor;
- a separately authorized change to canonical lifecycle semantics that removes the unbounded-survivor construction.

None of those premises is established by this result.

Real Exness V2 remains `DATA_EXCLUDED_ORIGIN_HISTORY_UNSEEDED`.
Protected holdout scoring remains disabled.
Automatic order sending remains disabled.