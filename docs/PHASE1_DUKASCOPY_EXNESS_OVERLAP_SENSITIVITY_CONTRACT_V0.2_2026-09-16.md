# Phase 1 Dukascopy ↔ Exness Overlap Sensitivity Contract V0.2 — 2026-09-16

Status: FROZEN PRE-IMPLEMENTATION CORRECTION / PRE-RERUN / HOLDOUT UNSCORED / ORDER SEND DISABLED

Contract ID: `PHASE1_DUKASCOPY_EXNESS_OVERLAP_SENSITIVITY_V0.2`

Supersedes V0.1 only for active-M1 normalization before frozen V2 H4/PAT/origin construction.

All V0.1 frozen windows, source-family separation, exact classification categories, no-tolerance rule, no-outcome-selection rule, and prohibited uses remain unchanged.

## Correction basis

The frozen V2 implementation already defines active M1 as:

- if `volume` exists: rows with `volume > 0` only;
- otherwise: all normalized observed rows.

Overlap V0.1 failed to apply this existing semantic to Dukascopy before resampling.

V0.2 restores the pre-existing V2 semantic. This correction is not derived from which V0.1 classification looked preferable.

## V0.2 active-input rule

For Dukascopy BID M1:

- raw input rows and provenance remain recorded;
- `volume` is required for the real frozen Dukascopy files;
- only `volume > 0` rows are eligible for H4 resampling, PAT detection, origin construction, lifecycle state, and active-M1 timestamp comparison;
- rows with `volume <= 0` are excluded from V2-state construction but their raw/excluded counts remain reported;
- positive-volume weekend rows remain eligible; no weekday/weekend calendar rule is invented.

For Exness archive-derived BID M1:

- every emitted M1 bar is built from observed archive ticks;
- no synthetic volume column is introduced;
- all emitted bars remain active input.

## Frozen windows unchanged

- `W2022_09`: 2022-09-01T00:00:00Z → 2022-10-01T00:00:00Z;
- `W2023_09`: 2023-09-01T00:00:00Z → 2023-10-01T00:00:00Z;
- `W2026_08_24`: 2026-08-24T00:00:00Z → 2026-08-25T00:00:00Z.

Do not add, remove, shrink, or replace windows after observing V0.1 results.

## Classification categories unchanged

- `EXACT_OBSERVED_STATE_EQUIVALENCE`;
- `STRUCTURAL_STATE_EQUIVALENCE_NUMERIC_DIVERGENCE`;
- `STATE_DIVERGENCE_OBSERVED`;
- `INCOMPARABLE_INPUT_GAP`.

No numeric or timestamp tolerance is authorized.

## Additional required tests before rerun

1. zero-volume Dukascopy rows do not affect H4/PAT/origin classification;
2. positive-volume rows remain active even on weekend timestamps;
3. real Dukascopy loader rejects a frozen input that lacks `volume`;
4. report records raw row count, active row count, and excluded non-positive-volume row count separately;
5. the original seven V0.1 contract tests continue to pass unchanged in meaning.

## Decision gate

V0.1 real results remain historical but are superseded for decision use by the active-M1 defect.

Only V0.2 rerun results may be considered for the next cross-feed initialization representation decision.

Even a V0.2 exact/structural match does not by itself establish a COMPLETE Exness seed or universal feed equivalence.