# Phase 1 Exness Archive Annual Validation - 2025

Status: DONE / VALIDATOR V0.2 / YEAR-BATCH RECONCILED WITH RAW-DUPLICATE OBSERVATIONS
Date: 2026-09-15
Durable job: `XAU-EXNESS-YEAR-2025-V02-20260915`
Runner revision: `dc2a0d8`

Coverage-selected months: all 12 months.
All 12 completed with `VALIDATED` structural status.

Observed totals:
- ZIP bytes: 699,512,992
- tick rows: 76,283,540
- provider mismatch: 0
- symbol mismatch: 0
- Ask < Bid: 0
- non-finite Bid/Ask: 0
- timestamp regression: 0
- consecutive equal timestamps: 86,339
- consecutive exact duplicate rows: 68,317

Raw duplicate/equal-timestamp observations:
- 2025-05: equal timestamps 1 / exact duplicates 0
- 2025-06: 10,998 / 10,998
- 2025-07: 18,942 / 18,941
- 2025-08: 1,626 / 1,626
- 2025-09: 8,314 / 8,314
- 2025-10: 30,522 / 28,438
- 2025-11: 2,647 / 0
- 2025-12: 13,289 / 0
- raw acquisition preserves these rows.
- no causal explanation is inferred from the current evidence.
- deduplication for replay remains a separate representation decision and is not applied here.

Boundary observation:
All twelve coverage-listed monthly objects are present and structurally valid.
Observed first/last timestamps remain session-boundary observations, not proof of calendar-month or every-tick continuity.
No continuity claim is inferred from structurally valid ZIP/CSV files alone.

Interpretation:
2025 acquisition/structural validation is complete for every month classified AVAILABLE by the coverage map.
The unresolved 2016 March/April boundary gap candidate and prior raw-duplicate observations remain preserved separately.

Next bounded action:
Run the final annual archive batch for 2026 using only coverage-map months classified AVAILABLE, then perform a full acquisition reconciliation across 2015-2026 before moving to replay-contract work.
