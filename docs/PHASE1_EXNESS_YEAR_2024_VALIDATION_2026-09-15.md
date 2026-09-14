# Phase 1 Exness Archive Annual Validation - 2024

Status: DONE / VALIDATOR V0.2 / YEAR-BATCH RECONCILED WITH RAW-DUPLICATE OBSERVATION
Date: 2026-09-15
Durable job: `XAU-EXNESS-YEAR-2024-V02-20260915`
Runner revision: `50e5faa`

Coverage-selected months: all 12 months.
All 12 completed with `VALIDATED` structural status.

Observed totals:
- ZIP bytes: 368,856,675
- tick rows: 39,715,935
- provider mismatch: 0
- symbol mismatch: 0
- Ask < Bid: 0
- non-finite Bid/Ask: 0
- timestamp regression: 0
- consecutive equal timestamps: 24,648
- consecutive exact duplicate rows: 24,648

Raw duplicate observation:
- 2024-05: 10,804 consecutive exact duplicates
- 2024-06: 1,106
- 2024-07: 3,699
- 2024-08: 6,702
- 2024-09: 2,337
- total: 24,648
- in these months, the equal-timestamp count equals the exact-duplicate count.
- raw acquisition preserves these rows.
- no explanation for the duplicate pattern is inferred from the current evidence.
- deduplication for replay remains a separate representation decision and is not applied here.

Boundary observation:
All twelve coverage-listed monthly objects are present and structurally valid.
Observed first/last timestamps remain session-boundary observations, not proof of calendar-month or every-tick continuity.
No continuity claim is inferred from structurally valid ZIP/CSV files alone.

Interpretation:
2024 acquisition/structural validation is complete for every month classified AVAILABLE by the coverage map.
The unresolved 2016 March/April boundary gap candidate remains preserved separately.

Next bounded action:
Run the same durable annual procedure for 2025, then reconcile its manifest/anomaly evidence before 2026.
