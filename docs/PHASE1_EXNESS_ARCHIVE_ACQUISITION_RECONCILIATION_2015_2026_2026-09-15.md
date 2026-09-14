# Phase 1 Exness Tick Archive Acquisition Reconciliation - 2015-2026

Status: CURRENT-COVERAGE ACQUISITION COMPLETE / VALIDATOR V0.2 / OUTCOME SCORING NOT STARTED
Date: 2026-09-15
Scope: XAUUSDm Exness-branded archive coverage snapshot for 2015-2026

## Coverage reconciliation

Coverage map:
- expected calendar-month slots: 144
- status AVAILABLE: 134
- current-validator VALIDATED: 134
- AVAILABLE months missing from current-validator manifest: 0
- current-validator months outside AVAILABLE coverage: 0

Year/month counts:
- 2015: 5 AVAILABLE months (Aug-Dec)
- 2016-2025: 12 AVAILABLE months per year
- 2026: 9 AVAILABLE months (Jan-Sep)
- total: 134 AVAILABLE months

The 10 non-AVAILABLE calendar-month slots are not fabricated. In this snapshot they correspond to the period before the earliest archive availability and the future/unavailable tail beyond the current 2026-09 coverage.

## Aggregate validated archive

Across the latest Validator V0.2 record for each AVAILABLE month:
- ZIP bytes: 3,430,625,119
- tick rows: 379,942,589
- earliest observed tick: 2015-08-10T00:00:00Z
- latest observed tick: 2026-09-13T23:59:59.824Z
- provider mismatch: 0
- symbol mismatch: 0
- Ask < Bid: 0
- non-finite Bid/Ask: 0
- timestamp regression: 0
- consecutive equal timestamps: 20,929,091
- consecutive exact duplicate rows: 289,098

These are raw archive observations. Equal timestamps and exact duplicate rows remain preserved in acquisition data and are not silently removed.

## Preserved anomalies and boundaries

1. 2015-08 is the earliest AVAILABLE month but begins on 2015-08-10, so AVAILABLE does not imply calendar-month completeness.
2. The 2016 March/April boundary remains an unresolved archive-boundary gap candidate:
   - March last observed tick: 2016-03-25T00:00:00Z
   - April first observed tick: 2016-04-01T06:52:51Z
   No missing ticks are fabricated and the interval is not explained away as market closure without evidence.
3. Raw exact-duplicate concentrations were observed in later years, including 2024, 2025, and 2026. They remain source observations; deduplication is a separate replay-representation decision.
4. 2026-09 is partial in the current snapshot and ends at 2026-09-13T23:59:59.824Z.
5. The earlier 2026-08 archive-vs-current-MT5 overlap was descriptively consistent at broker-family market-data level, but exact feed/server equivalence is NOT established.

## Closure meaning

This checkpoint closes the data-acquisition task for every month classified AVAILABLE by the frozen current coverage map.

It does NOT establish:
- continuous tick coverage across every market interval;
- exact identity with the current Exness Demo MT5 feed;
- canonical deduplication rules;
- exact broker fill, slippage, stop execution, or transaction-cost treatment;
- strategy Win rate, Loss rate, expectancy, profitability, or any outcome claim.

Automatic order sending remains disabled.
V0.1 holdout outcome scoring remains disabled.

## Next bounded engineering task

Freeze the pre-outcome Phase 1 replay engineering contract before any downstream outcome scoring. The contract must explicitly separate:
- raw archive representation from replay representation;
- duplicate/equal-timestamp handling;
- fill model;
- stop execution;
- spread/cost treatment;
- residual slippage/unknown execution effects;
- provenance between archive data and current MT5 runtime observations.

No outcome result may be used retrospectively to choose those rules.
