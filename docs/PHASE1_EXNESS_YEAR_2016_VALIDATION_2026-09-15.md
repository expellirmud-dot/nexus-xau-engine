# Phase 1 Exness Archive Annual Validation — 2016

Status: DONE / VALIDATOR V0.2 / YEAR-BATCH RECONCILED WITH BOUNDARY ANOMALY
Date: 2026-09-15
Durable job: `XAU-EXNESS-YEAR-2016-V02-20260915`
Runner revision: `4c0306c`

Coverage-selected months: all 12 months.
All 12 completed with `VALIDATED` structural status.

Observed totals:
- ZIP bytes: 192,457,140
- tick rows: 29,582,383
- provider mismatch: 0
- symbol mismatch: 0
- Ask < Bid: 0
- non-finite Bid/Ask: 0
- timestamp regression: 0
- consecutive exact duplicate rows: 0
- consecutive equal timestamps: 15,158,888

Boundary anomaly:
- March file last tick: 2016-03-25T00:00:00Z
- April file first tick: 2016-04-01T06:52:51Z
- the apparent interval between those observations is not explained by the current validation evidence.
- classify as OBSERVED_ARCHIVE_BOUNDARY_GAP_CANDIDATE / UNRESOLVED.
- do not fabricate ticks or silently infer market closure for the full interval.

Interpretation:
All coverage-listed 2016 monthly objects were downloaded and structurally validated, but year-level tick continuity is NOT established because of the observed March/April boundary.
This anomaly is non-blocking for continuing archive acquisition; it is required-later evidence for the dedicated continuity audit.

Next bounded action:
Run 2017 as the next annual durable batch, while preserving the 2016 boundary anomaly for later cross-source investigation.
