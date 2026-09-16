# Phase 1 MT5 Cost-Treatment Evidence Contract V0.1 — 2026-09-17

Status: FROZEN PRE-PROBE / READ-ONLY / NO ECONOMIC SCORING / HOLDOUT UNSCORED / ORDER SEND DISABLED

Contract ID: `PHASE1_MT5_COST_TREATMENT_EVIDENCE_V0.1`

Target registry dependency: `U-P1-10-COST-TREATMENT`.

## Question

What commission/fee/swap information is observable from the current Exness Demo / MT5 runtime and account-history API, and which parts required for historical economic replay remain unresolved?

## Existing boundary

The frozen tick-replay engineering contract already establishes:

- archive quotes do not establish exact historical account-specific commission, fee, or financing schedules;
- no zero-cost assumption is permitted;
- historical slippage/fill truth is separate and remains unresolved;
- no profitability, expectancy, or broker-fill claim is authorized.

This contract does not weaken those boundaries.

## Source identity

All observations are current-runtime/account specific.

Record the existing MT5 source identity derived from terminal/account/symbol runtime metadata.

Do not generalize evidence from `Exness-MT5Trial6 / XAUUSDm / Demo` to another server, account type, live symbol, or historical archive without separate evidence.
## Frozen current-runtime symbol metadata representation

At probe time, capture all `symbol_info('XAUUSDm')` fields whose names begin with `swap_`, plus:

- symbol name;
- account/company/server identity already present in the source-identity payload;
- current observation timestamp;
- source-identity digest.

Swap fields are reported exactly as exposed by MT5. Their units/meaning are not reinterpreted beyond the broker/runtime API field names unless separately documented.

A current zero-valued field is an observation for this runtime instant/specification, not proof of zero historical cost.

## Frozen account-deal schema representation

Read current account deal history from the MT5 history API in read-only mode.

The acquisition interval is frozen as:

`1970-01-01T00:00:00Z -> observation_time_utc`

This interval is an account-history capability/schema probe, not a market backtest window.

Persist only:

- total returned deal count;
- count of deals whose `symbol == XAUUSDm`;
- sorted field names exposed by returned deal records when any exist;
- presence/absence of the fields `commission`, `fee`, and `swap`;
- for `XAUUSDm` deals only, descriptive summaries of those three cost components: observed count, nonzero count, minimum, maximum, and sum;
- API last-error status;
- source identity and observation timestamp.

Do not persist trade profit, entry/exit price, trade direction, or use deal outcomes for strategy evaluation under this contract.

If no `XAUUSDm` deals exist, report zero observed cost samples. Do not infer zero commission/fee/swap.

## Interpretation classes

The result must keep these dimensions separate:

- `CURRENT_SYMBOL_FINANCING_METADATA`: current runtime swap-related specification;
- `ACCOUNT_DEAL_COST_SCHEMA`: whether commission/fee/swap deal fields are observable;
- `ACCOUNT_DEAL_COST_OBSERVATIONS`: bounded current-account samples, if any;
- `HISTORICAL_REPLAY_COST_SCHEDULE`: whether evidence exists for exact historical commission/fee/swap treatment across replay periods.

Current metadata or recent deal observations cannot by themselves promote `HISTORICAL_REPLAY_COST_SCHEDULE` to known.
## Fail-closed rules

- MT5 initialization failure → probe FAIL; no synthetic substitute.
- Missing symbol specification → probe FAIL.
- Account-history API failure → schema/observations UNKNOWN with recorded API error; do not assume empty history.
- Empty successful history result → zero returned deals only; cost values remain unobserved.
- Missing commission/fee/swap field in the returned schema → report field unavailable; do not substitute another field.
- No cost component is assumed zero because its current sample is empty or zero-valued.

## Prohibited calculations and claims

This probe MUST NOT calculate or emit:

- strategy P&L;
- Win Rate or Loss Rate;
- expectancy;
- profitability or profit factor;
- drawdown;
- trade-level net return;
- slippage/fill model;
- representative historical commission schedule;
- representative historical swap schedule;
- automatic order request.

Actual deal `profit` values, if present in the MT5 record schema, are not persisted in the evidence output.

## Registry reconciliation rule

Do not automatically mark `U-P1-10-COST-TREATMENT` resolved merely because current runtime swap metadata or deal cost fields are observable.

After the probe:

- current-runtime observations may become `KNOWN_NOW` evidence;
- if exact historical replay cost schedules remain unsupported, the readiness gap must be rewritten to that remaining requirement and reclassified according to the evidence;
- historical wording and this original registry dependency remain preserved as superseded/resolved chronology as appropriate.

## Required tests before runtime probe

1. symbol swap fields are selected deterministically by field name;
2. deal schema presence is reported without requiring a market deal;
3. empty successful account history does not become zero-cost evidence;
4. commission/fee/swap summaries use only `XAUUSDm` deal records;
5. output excludes deal profit/price/direction fields;
6. API failure remains UNKNOWN/FAIL-CLOSED rather than empty-success;
7. source identity is required;
8. output has fixed `order_send=DISABLED`, `holdout_scoring=DISABLED`, `economic_scoring=DISABLED` guards.

## Completion boundary

The probe may close only the **current-runtime observability** part of cost treatment.

It cannot by itself establish historical execution economics or enable P1-10 economic claims.