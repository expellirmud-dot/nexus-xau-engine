# State Drift and Replay Provenance Audit — 2026-09-15

Status: RECONCILED / PRE-OUTCOME / HISTORY PRESERVED

Scope:
- project-current structured state;
- current Phase 1 construction/readiness surfaces;
- pre-outcome replay contracts versus implementation;
- durable-job pointer truth;
- document-reference integrity.

This audit follows `docs/STATE_AUTHORITY_CONTRACT_2026-09-13.md`.
Dated historical checkpoints are preserved and are not rewritten merely because later evidence supersedes their then-current workflow conclusions.

## Machine truth at audit start

Repository:
- branch: `main`;
- starting HEAD: `f905fa3`;
- Git state before audit edits: CLEAN.

Durable collector evidence:
- job `XAU-MT5-FORWARD-COLLECTOR-1H-V02-20260914`: `DONE`;
- attempts: 1;
- exit code: 0;
- collector status surface: `STOPPED`;
- last error: null.
Archive/replay evidence already closed before this audit:
- 134/134 current coverage-map months classified AVAILABLE have Validator V0.2 VALIDATED records;
- archive-window adapter V0.1 implemented and tested;
- archive Bid -> M1 V0.1 implemented and tested;
- automatic order execution disabled;
- holdout outcome scoring disabled.

## Drift found and corrected

### 1. Project resume instruction was stale

Before:
- told reconnecting sessions to run the 2015–2026 archive mapper and representative archive validation.

Reality:
- those tasks were already completed and reconciled.

Correction:
- `CURRENT_RESEARCH_STATE.resume_instruction` now points to the provenance-preserving archive-M1 -> existing resample -> frozen V2 integration contract as the next bounded action.

### 2. Durable pointer was stale

Before:
- project-current state marked the one-hour MT5 collector `RUNNING`.

Machine evidence:
- durable receipt = `DONE`, exit 0;
- collector status = `STOPPED`;
- continuity registry found no active jobs.
Correction:
- `active_durable_job.job_id = null`;
- status = `NONE`;
- completed collector/archive job identities remain preserved as historical/current-state references;
- reconnect now reports `durable_pointer=NONE` and `active_jobs=NONE`.

### 3. Execution-data coverage state was stale

Before:
- current state still said multi-year archive mapping was pending;
- external route status still said full coverage had not yet been mapped.

Correction:
- current state now records 134/134 AVAILABLE months validated;
- full every-tick continuity remains explicitly unproven;
- exact archive-to-current Exness Demo/MT5 equivalence remains unproven;
- continuous forward-collector mode remains not implemented.

### 4. Trade construction matrix lagged newer evidence

Updated current engineering state:
- reference entry convention is frozen as first archive tick strictly after confirmation knowledge time;
- BUY reference quote uses Ask; SELL uses Bid;
- reference fills are not broker-fill claims;
- multi-year archive spread is derivable from recorded Bid/Ask;
- historical slippage and account-specific costs remain unresolved;
- tick timestamps may resolve bar-level ordering when timestamps differ;
- conflicting first-touch states within the same timestamp remain `AMBIGUOUS_SAME_TIMESTAMP`.
## Contract-to-implementation defect found

The frozen tick replay contract requires stable source raw-row position to remain auditable.

Observed implementation defect:
- `first_reference_entry()` returned the tick's position inside the supplied replay window;
- supplied-level evaluation also generated a window-relative ordinal;
- when archive adapter rows already contained source `raw_ordinal`, that source coordinate was not propagated.

Risk:
- not a strategy/outcome error;
- provenance could become misleading after slicing a larger archive window.

Correction:
- when a `raw_ordinal` column exists, replay outputs now preserve that source archive ordinal;
- generic non-archive frames retain window-relative fallback ordinals;
- no signal/outcome data was opened to make this correction.

Targeted validation:
- Ruff: PASS;
- tick-reference synthetic tests: 12/12 PASS;
- new tests explicitly verify source raw ordinal survives reference-entry and supplied-level outputs.

## Finding-ledger reconciliation

Added `OBS-0006` under the Exness archive finding:
- bounded 2026-08 archive-derived M1 vs saved MT5 M1 comparison;
- 60/60 minute timestamps aligned;
- 50/60 bars had at least one exact OHLC mismatch;
- exact component matches: Open 41, High 39, Low 32, Close 35;
- no tolerance threshold inferred.
Interpretation remains:
- bounded timestamp/boundary compatibility observed;
- exact feed/server/price equivalence NOT established.

## Reference-integrity audit

Checked:
- Current State load-order references after linking this audit: 61;
- duplicate load-order entries: 0;
- readiness evidence references: 34;
- missing referenced files: 0.

Historical snapshots containing older statuses such as `MULTIYEAR_COVERAGE_MAPPING_PENDING` remain preserved because they were correct at their recorded time.
Only project-current pointers/status were reconciled.

## Full validation

After corrections:
- structured JSON validation: PASS;
- research preflight: PASS;
- finding ledger: PASS, 2 findings / 6 observations;
- broader Ruff `src tests scripts`: PASS;
- full repository pytest: PASS;
- `git diff --check`: PASS;
- `RESUME_WORK --project xau`: PASS with current next action;
- durable pointer from continuity capsule: NONE;
- active durable jobs: NONE.

Only pre-existing/deprecation-class warnings were emitted by the full test suite.
## Residual unknowns preserved

Still unresolved and not filled by assumption:
- full every-tick continuity beyond the explicit known-gap ledger;
- exact archive-to-current Exness Demo/MT5 feed identity;
- source-compatible exact trade-stop geometry;
- historical broker fill/slippage truth;
- account-specific commission/fee/swap treatment for economic claims;
- position sizing/risk cap for supervised execution;
- protected holdout performance.

## Next bounded action

Freeze the integration contract for:

`validated archive window -> ARCHIVE_BID_M1_V0.1 -> existing M5/H1/H4/D1 resample -> frozen 0700_MINIMAL_V2.0 state machinery`

Requirements:
- preserve source/representation/provenance identity;
- propagate DATA_EXCLUDED and unknown states;
- no silent deduplication/interpolation;
- engineering-only validation first on already-inspected windows;
- no broad historical outcome replay until the integration contract and synthetic invariants pass;
- holdout scoring and order sending remain disabled.
