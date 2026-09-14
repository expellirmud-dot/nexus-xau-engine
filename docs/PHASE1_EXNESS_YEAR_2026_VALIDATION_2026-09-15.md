# Phase 1 Exness Archive Annual Validation - 2026

Status: DONE / VALIDATOR V0.2 / CURRENT-COVERAGE YEAR-BATCH RECONCILED
Date: 2026-09-15
Durable job: `XAU-EXNESS-YEAR-2026-V02-20260915`
Runner revision: `ea5a2a5`

Coverage-selected months: 2026-01 through 2026-09 (9 AVAILABLE months in the current coverage map).
All 9 completed with `VALIDATED` structural status.

Observed totals:
- ZIP bytes: 667,785,227
- tick rows: 70,776,973
- provider mismatch: 0
- symbol mismatch: 0
- Ask < Bid: 0
- non-finite Bid/Ask: 0
- timestamp regression: 0
- consecutive equal timestamps: 622,490
- consecutive exact duplicate rows: 196,133

Raw equal-timestamp / exact-duplicate observations:
- 2026-01: 107,319 / 5,970
- 2026-02: 53,410 / 0
- 2026-03: 190,001 / 51,758
- 2026-04: 56,597 / 35,747
- 2026-05: 38,417 / 13,885
- 2026-06: 116,588 / 66,552
- 2026-07: 26,050 / 8,432
- 2026-08: 29,000 / 12,313
- 2026-09: 5,108 / 1,476

Boundary observations:
- 2026-09 is a partial current month in this coverage snapshot: first tick 2026-09-01T00:00:00.065Z, last tick 2026-09-13T23:59:59.824Z.
- Months 2026-10 through 2026-12 are not AVAILABLE in the current coverage map and were not fabricated or inferred.
- Raw acquisition preserves repeated/equal timestamps and exact duplicate rows.
- No causal explanation for duplicate patterns is inferred from current evidence.
- Structural validation does not prove every-tick continuity or exact equivalence to the current Exness Demo MT5 route.

Interpretation:
2026 acquisition/structural validation is complete for every month classified AVAILABLE in the current coverage map.
This closes the annual acquisition sequence for the present 2015-2026 coverage snapshot.

Next bounded action:
Perform one final archive-acquisition reconciliation across all currently AVAILABLE months from 2015-2026, preserve unresolved anomalies, then move to the pre-outcome replay engineering contract without enabling holdout scoring or order execution.
