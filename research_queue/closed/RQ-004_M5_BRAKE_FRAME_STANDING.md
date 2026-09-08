# RQ-004 — M5 brake and frame-standing state machine

Status: CLOSED / SOURCE_BACKED_STATE_MACHINE_PARAMETERIZED

## Why this matters

Existing evidence describes a zone-first stopping/reversal process with weakening force, rejection, color shift, and retest/confirmation. The qualitative sequence must be converted into defensible measurable states before entry logic can rely on it.

## Primary method when activated

Review EP.4 / EP.6 and system-summary visual windows first. Identify state transitions from what the instructor points to, then encode threshold-free features before considering labeled variants.

## Done when

The transition/state representation is source-backed enough to replay, or explicitly closed as partial/inconclusive with unresolved geometry listed.

## Current source position

`docs/M5_BRAKE_TRANSCRIPT_FORENSICS_2026-09-01.md` already provides a timestamped state-machine shell from EP.6. Current task is to classify which transitions are source-backed versus threshold-parameterized and close the worksheet without turning example values into universal thresholds.

## Closure — 2026-09-08

See `docs/RQ004_M5_BRAKE_FRAME_STANDING_SOURCE_CLOSURE_2026-09-08.md`. Replayable state/features are source-backed; exact numeric gates remain parameterized.
