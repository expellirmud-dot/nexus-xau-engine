# Phase 1 MT5 Cost-Treatment Evidence Result V0.1 — 2026-09-17

Status: CURRENT-RUNTIME OBSERVABILITY ESTABLISHED / HISTORICAL REPLAY COST SCHEDULE UNRESOLVED / HOLDOUT UNSCORED / ORDER SEND DISABLED

Contract: `docs/PHASE1_MT5_COST_TREATMENT_EVIDENCE_CONTRACT_V0.1_2026-09-17.md`
Probe implementation: `src/nexus_xau/data/mt5_cost_evidence.py`
Runtime evidence: `results/mt5_cost_evidence/current_runtime_v01.json`
Runtime evidence SHA-256: `5b822f40c50f771e06f1a1d5e4c532ae6e06437469180551bf3c068fc36b848d`
Observed at: `2026-09-16T21:18:21+00:00`

## Current source identity

Current MT5 runtime observation:

- company: `Exness Technologies Ltd`;
- server: `Exness-MT5Trial17`;
- account currency: `USD`;
- symbol: `XAUUSDm`;
- source identity: `2017aa577e132c4e84ba5b15462e668b438f8aa0e0f96859737e855a7fe48818`.

The source identity exactly matches the existing MT5 forward-collector status and the latest collector runtime snapshot.

Collector SQLite runtime snapshot evidence:

- captured at `2026-09-14T12:33:11.343+00:00`;
- server `Exness-MT5Trial17`;
- source identity `2017aa577e132c4e84ba5b15462e668b438f8aa0e0f96859737e855a7fe48818`.

The older broker metadata document from 2026-09-02 records `Exness-MT5Trial6`. That historical evidence remains preserved and is not rewritten. The current Trial17 observation is a later runtime environment state, not proof that the earlier Trial6 record was wrong.
## Current symbol financing metadata

Observed current MT5 `symbol_info('XAUUSDm')` swap fields:

- `swap_long = -547.6`;
- `swap_short = 0.0`;
- `swap_mode = 1`;
- `swap_rollover3days = 3`.

These are current runtime specification values only. No historical generalization is made.

## Account-deal cost schema

The read-only account-history call from `1970-01-01T00:00:00Z` through the observation time succeeded.

Observed:

- total deal records returned: 1;
- `XAUUSDm` deal records: 0;
- deal schema exposes `commission`, `fee`, and `swap` fields;
- the one returned record is not an XAUUSDm market-deal sample for this cost treatment.

For XAUUSDm commission/fee/swap:

- observed sample count: 0 for each component;
- nonzero sample count: 0 because no XAUUSDm cost samples exist;
- minimum/maximum/sum remain null rather than zero.

This is deliberately **not** interpreted as zero commission, zero fee, or zero swap.

Deal record schema also exposes fields such as price/profit/type, but the evidence representation does not persist their values or use them for strategy evaluation.
## Interpretation

Current-runtime observability is now established for:

- swap-related symbol metadata;
- account-deal schema visibility for `commission`, `fee`, and `swap`;
- read-only acquisition of bounded current-account cost observations when such XAUUSDm deal records exist.

Still unresolved:

- exact historical account-specific commission schedule across replay periods;
- exact historical fee schedule across replay periods;
- exact historical swap/financing schedule across replay periods;
- actual XAUUSDm deal-cost samples for the current account/runtime;
- fill/slippage truth and stop geometry, which remain separate P1-10 dependencies.

The remaining historical schedule problem is not reduced by waiting for future runtime observations alone; future observations can add current/future samples but cannot reconstruct an exact historical schedule without additional evidence.

## Unknown-registry consequence

The generic prior dependency `U-P1-10-COST-TREATMENT` is now too coarse.

It should be preserved as superseded chronology and replaced by two explicit residuals:

1. historical replay cost schedule — `IRREDUCIBLE_OR_NOT_YET_REDUCIBLE / BLOCKING`;
2. current/future XAUUSDm deal-cost samples — `RUNTIME_OBSERVABLE / REQUIRED_LATER`.

This split prevents current schema observability from being mistaken for historical economic completeness.

## Validation

- initial pre-probe synthetic contract tests: 9/9 PASS;
- hardened cost-evidence suite including runtime-wrapper success/failure paths: 11/11 PASS;
- combined cost + governance regression: 39/39 PASS;
- targeted Ruff: PASS;
- full repository durable pytest XAU-MT5-COST-FULLPYTEST-20260917: DONE, one attempt, exit code 0, persisted progress = 411/411 tests;
- broad Ruff durable job XAU-MT5-COST-RUFF-20260917: DONE, one attempt, exit code 0, All checks passed!;
- no runtime order action was used;
- guards in the persisted evidence remain order_send=DISABLED, holdout_scoring=DISABLED, economic_scoring=DISABLED, ill_slippage_inference=DISABLED.

No Win Rate, expectancy, profitability, trade P&L, exact broker fill, or slippage result is claimed.
