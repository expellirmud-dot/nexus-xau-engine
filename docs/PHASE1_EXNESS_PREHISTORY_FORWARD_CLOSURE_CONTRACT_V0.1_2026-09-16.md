# Phase 1 Exness Prehistory Forward-Closure Contract V0.1 — 2026-09-16

Status: FROZEN PRE-FALSIFICATION / EXNESS-ONLY / HOLDOUT UNSCORED / ORDER SEND DISABLED

## Question

Can a finite forward-only Exness replay prove that all unknown pre-archive H4 origins are terminal, without an independently justified bound on possible pre-start anchor prices and without assuming price continuity across the unobserved boundary?

## Frozen lifecycle semantics

- BUY origin target = `anchor + 1500 * 0.01`.
- SELL origin target = `anchor - 1500 * 0.01`.
- point-check destruction requires literal observed M1 range contact: `low <= anchor <= high`.
- gaps across an anchor do not count as contact unless an observed bar spans the anchor.
- origins have no fixed expiry.

These semantics already exist in `minimal_v2_0700.py`; this audit does not alter them.

## Hypothesis under test

`FINITE_FORWARD_EXNESS_CAN_CLOSE_UNBOUNDED_UNKNOWN_PREHISTORY`.

## Falsification construction

For any non-empty finite observed M1 path with finite maximum high and minimum low:

1. choose a hypothetical pre-start BUY anchor as the next representable float strictly above the observed maximum high;
2. choose a hypothetical pre-start SELL anchor as the next representable float strictly below the observed minimum low, provided the resulting price remains positive for the XAU domain;
3. place each hypothetical origin's `origin_known_at` before the observed path;
4. evaluate the frozen `origin_state_at()` through the entire finite path.

If both origins remain `ACTIVE`, the finite path alone cannot certify complete elimination of unknown prehistory.

This is a counterexample construction, not a market threshold or trading rule.

## Required tests

1. BUY counterexample above finite observed maximum remains `ACTIVE`.
2. SELL counterexample below finite observed minimum remains `ACTIVE`.
3. extending the finite path does not change the proof form: new anchors can always be constructed outside the new finite extrema.
4. no warmup duration, expiry, tolerance, P&L, Win Rate, expectancy, broker fill, holdout score, or order action is introduced.

## Interpretation

If falsified, arbitrary forward warmup cannot become a defensible COMPLETE seed under the current literal-contact semantics.

A future COMPLETE seed would then require at least one additional independently justified constraint, such as a defensible pre-start anchor domain, same-source earlier history, or a changed canonical lifecycle semantic. None is authorized by this contract.