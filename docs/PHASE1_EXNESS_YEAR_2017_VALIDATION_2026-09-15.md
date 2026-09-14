# Phase 1 Exness Archive Annual Validation — 2017

Status: DONE / VALIDATOR V0.2 / YEAR-BATCH RECONCILED
Date: 2026-09-15
Durable job: `XAU-EXNESS-YEAR-2017-V02-20260915`
Runner revision: `5bc1686`

Coverage-selected months: all 12 months.
All 12 completed with `VALIDATED` structural status.

Observed totals:
- ZIP bytes: 177,962,017
- tick rows: 20,773,662
- provider mismatch: 0
- symbol mismatch: 0
- Ask < Bid: 0
- non-finite Bid/Ask: 0
- timestamp regression: 0
- consecutive exact duplicate rows: 0
- consecutive equal timestamps: 1,257,352

Boundary observation:
All twelve coverage-listed monthly objects are present and structurally valid.
The first/last timestamps reflect trading-session boundaries rather than calendar-month completeness.
This annual pass does not by itself prove continuous tick coverage across every intra-month or month-boundary interval.

Interpretation:
2017 acquisition/structural validation is complete for every month classified AVAILABLE by the coverage map.
No market-fill, slippage, profitability, or exact MT5-feed equivalence claim is made.

Next bounded action:
Run the same durable annual procedure for 2018, then reconcile its manifest/anomaly evidence before 2019.
