# RQ-016 — Phase 1 Trade Construction Boundary

Status: CLOSED

## Why this matters now

Phase 1 research logic is advanced enough to distinguish state/signal behavior from actual economic execution.

RQ-007 asked whether one universal full-system trade construction was available. It was not.

RQ-016 is narrower. It asks only about the current Phase 1 H4/PAT2/M5 lane.

## Question

For each required trade tuple field, classify it as:

- SOURCE_BACKED
- ENGINEERING_CONVENTION_ALLOWED
- BLOCKING_UNKNOWN

Fields:

- setup identity
- signal knowledge time
- entry execution representation
- SL / invalidation
- TP / exit
- replacement / re-entry
- broker/feed metadata
- Bid/Ask handling
- spread/slippage/cost
- same-bar ambiguity
- position sizing / risk cap

## Evidence first

Primary evidence:

- docs/0700_MINIMAL_V2_FROZEN_SPEC_2026-09-13.md
- docs/RQ007_ENTRY_SL_INVALIDATION_SOURCE_CLOSURE_2026-09-08.md
- docs/RQ009_EXECUTION_FILL_SOURCE_BOUNDARY_2026-09-09.md
- docs/RQ009_BROKER_FEED_NORMALIZATION_BOUNDARY_2026-09-09.md
- docs/BROKER_METADATA_EXNESS_MT5TRIAL6_XAUUSDM_2026-09-02.md
- docs/WIN_LOSS_PROOF_PROTOCOL_2026-09-03.md
- docs/DIRECT_RELATIVE_REMAINING_SIG_RUN_DAILY_FRAME_2026-09-03.md

## Guards

No market outcome scoring.
No holdout access.
No threshold or fill selection from historical performance.
No PAT3 expansion.
No live autonomous execution.

## Closure

Close when every required field has evidence, classification, allowed use, blocker effect, and next safe action.

## Closure

Matrix: `docs/PHASE1_TRADE_CONSTRUCTION_MATRIX.json`

Decision:

- Project-defined Phase 1 replay is constructible after explicit pre-outcome engineering conventions are frozen.
- Exact source reconstruction remains partial for fill/stop/close/re-entry mechanics.
- Execution-side price/cost data or a declared model remains required for stronger downstream economic evaluation.
- Position sizing/risk cap is a later account/pilot requirement, not a blocker for basic state/path replay.
- No market or holdout outcomes were inspected.
