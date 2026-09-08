# RQ-010 — Minimal Deterministic SIG Mode-2 Signal/Run Replay V0

Status: ACTIVE — implementation and freeze before any new holdout outcome inspection

## Objective

Implement the smallest deterministic research replay selected by the RQ-009 evidence-boundary audit:

```text
SIG_MODE2_EXTERNALLY_LABELED_SIGNAL_RUN_V0
```

This is a signal/run research layer, not a trade simulator and not a system Win/Loss backtest.

## Why this scope

The current source evidence is sufficient to replay a Mode-2 post-SIG lifecycle when the setup/location is labeled before outcome inspection, while several autonomous detector and trade-execution rules remain source-incomplete.

V0 therefore excludes those unresolved families rather than inventing rules.

## Frozen scope target

### Included

- H1 and H4 only for the first implementation;
- externally labeled source-compatible Mode-2 SIG instance;
- pre-outcome valid-location label/provenance;
- confirmed post-SIG point-check price;
- runtime price-grid normalization;
- literal point-check touch destruction;
- no-lookahead `known_at`;
- source-backed/frozen run target construction supplied in the event manifest;
- `TARGET_FIRST`, `POINT_CHECK_FIRST`, `AMBIGUOUS_SAME_BAR`, `NEITHER/HORIZON_EXHAUSTED`;
- MFE/MAE and event timing metadata.

### Excluded

- autonomous PAT1/PAT2/PAT3 detector;
- autonomous support/resistance/location detector;
- Body Collection candidate ranking or unseen reference reduction;
- Sideway autonomous geometry;
- Mode-1 intrabar entry;
- M5 Brake trading entry;
- Por Chon trading entry;
- broker order fill;
- Bid/Ask trade execution;
- spread/slippage/commission;
- P&L, sizing, expectancy, profit factor, drawdown;
- system Win/Loss claims.

## Required event manifest

Each input event must carry, at minimum:

```text
signal_id
side
signal_tf
pa_kind_or_source_label
pa_confirmed_at
location_label
location_label_provenance
post_sig_closed_at
point_check_price
point_check_price_provenance
run_anchor_price
run_target_price
parent_context_tf
context_tags
source_or_label_provenance
label_known_before_outcome
```

The loader must fail closed when required provenance is missing or `label_known_before_outcome != true`.

## State machine

```text
LABELED_MODE2_SIG
-> POINT_CHECK_ACTIVE
-> RUN_ACTIVE
-> TARGET_FIRST
   | POINT_CHECK_FIRST
   | AMBIGUOUS_SAME_BAR
   | HORIZON_EXHAUSTED
```

A replacement/new SIG is a new `signal_id`; do not silently mutate/re-anchor an old instance.

## Implementation plan

1. Define typed V0 manifest/event schema.
2. Validate timezone-aware timestamps, side, timeframe, provenance and runtime tick-grid alignment.
3. Implement deterministic replay on M1 Bid OHLC:
   - start at `post_sig_closed_at` / frozen outcome start convention;
   - detect target and point-check contact on normalized grid;
   - preserve same-bar ambiguity;
   - calculate MFE/MAE and first-hit timestamps.
4. Add unit tests using synthetic data and already-inspected development fixtures only.
5. Document exact distinction between V0 signal/run result and future trade-level result.
6. Freeze version/checkpoint.
7. Only after freeze, define/reserve a genuinely untouched future holdout. Do not inspect new holdout outcomes during V0 implementation.

## Guardrails

- no backtest-selected thresholds;
- no auto-label derived from unresolved PAT/location geometry;
- no hidden conversion of broker tick to project/course point;
- no trade Win/Loss naming;
- no holdout peek before code + input-label protocol freeze;
- ambiguous events remain ambiguous/excluded, never forced into favorable/adverse class.

## Done when

- manifest/schema is implemented and tested;
- replay state/result is deterministic and tested;
- synthetic target-first, point-check-first, same-bar ambiguous and neither cases pass;
- provenance failure cases fail closed;
- JSON/data contract is documented;
- full test suite and Ruff pass;
- implementation checkpoint is committed/pushed;
- holdout is still unopened.
