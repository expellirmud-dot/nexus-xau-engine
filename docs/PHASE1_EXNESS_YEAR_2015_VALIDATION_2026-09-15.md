# Phase 1 Exness Archive Annual Validation — 2015

Status: DONE / VALIDATOR V0.2 / YEAR-BATCH RECONCILED
Date: 2026-09-15
Durable job: `XAU-EXNESS-YEAR-2015-V02-20260915`
Committed runner revision: `86b2da9`

Coverage-selected months: 2015-08 through 2015-12 (5 AVAILABLE months).
All five months completed with `VALIDATED` status.

Observed totals:
- ZIP bytes: 59,106,170
- tick rows: 8,698,581
- provider mismatch: 0
- symbol mismatch: 0
- Ask < Bid: 0
- non-finite Bid/Ask: 0
- timestamp regression: 0
- consecutive exact duplicate rows: 0
- consecutive equal timestamps: 3,779,342

Boundary observations:
- earliest archive tick: 2015-08-10T00:00:00Z
- latest archive tick in this batch: 2015-12-31T22:00:04Z
- August is a partial first available month; availability does not imply Aug 1 coverage.
- repeated timestamps are preserved raw observations, not silently deduplicated.

Interpretation:
2015 acquisition/structural validation is complete for every month classified AVAILABLE by the coverage map.
This does not prove continuous market-session coverage, exact MT5 feed equivalence, fills, slippage, or profitability.

Next bounded action:
Run the same durable annual procedure for 2016, then reconcile its manifest/anomaly evidence before 2017.
