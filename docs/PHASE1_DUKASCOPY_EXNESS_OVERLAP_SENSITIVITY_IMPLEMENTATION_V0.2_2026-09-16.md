# Phase 1 Dukascopy ↔ Exness Overlap Sensitivity Implementation V0.2 — 2026-09-16

Status: IMPLEMENTED PRE-REAL-RERUN / ACTIVE-M1 SEMANTIC CORRECTED / HOLDOUT UNSCORED / ORDER SEND DISABLED

Contract:
`docs/PHASE1_DUKASCOPY_EXNESS_OVERLAP_SENSITIVITY_CONTRACT_V0.2_2026-09-16.md`

Superseded decision evidence retained:
`docs/PHASE1_DUKASCOPY_EXNESS_OVERLAP_SENSITIVITY_V01_OBSERVATION_DEFECT_2026-09-16.md`

Implementation:
- `src/nexus_xau/research/dukascopy_exness_overlap_sensitivity.py`
- `tests/test_dukascopy_exness_overlap_sensitivity.py`

## Correction scope

V0.2 changes only active-M1 normalization before H4/PAT/origin construction.

- Dukascopy rows with `volume > 0` are active.
- Dukascopy rows with `volume <= 0` are excluded from V2-state construction.
- Positive-volume weekend rows remain active.
- Exness archive-derived M1 bars remain active because every emitted bar is built from observed ticks.
- Frozen windows, classification categories, no-tolerance rule and no-outcome-selection rule are unchanged.
## Implementation changes

The runner contract marker is now:
`PHASE1_DUKASCOPY_EXNESS_OVERLAP_SENSITIVITY_V0.2`.

The comparison path now records both raw and active input counts and applies the same optional-volume active-M1 semantic already used by frozen Minimal V2.

The real Dukascopy loader now requires the frozen source file to preserve a `volume` column and fails closed with:
`DUKASCOPY_VOLUME_REQUIRED`.

Reports now preserve separately:
- Dukascopy raw M1 rows;
- Dukascopy active M1 rows;
- Dukascopy excluded non-positive-volume rows;
- Exness raw/active rows;
- Exness excluded non-positive-volume rows.

Source provenance remains separate. No feed merge or relabeling is introduced.
## Test traceability

The original seven V0.1 contract tests continue to pass unchanged in meaning.

V0.2 adds explicit tests that:
1. zero-volume Dukascopy rows cannot affect H4/PAT/origin classification;
2. positive-volume weekend rows remain active;
3. the real Dukascopy loader rejects frozen input lacking `volume`;
4. reports preserve raw, active and excluded-row counts separately.

Targeted V0.2 suite:
- 11/11 PASS.

Relevant regression:
- Minimal V2;
- Archive -> V2 integration;
- V2 origin-state carry;
- Dukascopy ↔ Exness overlap sensitivity;
- 70/70 PASS.

No real V0.2 overlap window was opened during implementation validation.
## Full validation

Durable full pytest job:
`XAU-OVERLAP-V02-FULLPYTEST-R2-20260916`

- status: DONE;
- attempts: 1;
- exit code: 0;
- persisted progress dots: 374/374.

An earlier durable submission `XAU-OVERLAP-V02-FULLPYTEST-20260916` failed before pytest launched because the submit command incorrectly persisted `--` as the executable. That failure is tooling syntax history, not a test failure, and is preserved.

Durable broad Ruff job:
`XAU-OVERLAP-V02-RUFF-20260916`

- scope: `src tests scripts`;
- status: DONE;
- exit code: 0.

Targeted Ruff: PASS.
`git diff --check`: PASS before this checkpoint.
## Decision boundary

V0.1 real results remain historical observations but are not decision-eligible for frozen-V2 cross-feed sensitivity because of the active-M1 representation defect.

V0.2 is now implementation-frozen before any real rerun.

Even if V0.2 later reports exact or structural equivalence:
- it does not establish universal feed identity;
- it does not establish a canonical COMPLETE Exness seed by itself;
- it does not authorize cross-feed initialization without the separately evaluated representation decision.

Real Exness V2 remains fail-closed as `DATA_EXCLUDED_ORIGIN_HISTORY_UNSEEDED`.

Protected holdout scoring remains disabled.
Automatic order sending remains disabled.

## Next bounded action

After this implementation checkpoint is committed and pushed, rerun only:
- `W2022_09`;
- `W2023_09`;
- `W2026_08_24`;

through durable jobs using the frozen V0.2 implementation, persist reports under a V0.2 result namespace, and interpret them without changing windows, tolerances or classification categories.
