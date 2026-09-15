# Phase 1 Dukascopy ↔ Exness Overlap Sensitivity V0.1 Observation + Defect — 2026-09-16

Status: HISTORICAL OBSERVATION PRESERVED / IMPLEMENTATION DEFECT FOUND / DECISION USE SUSPENDED / HOLDOUT UNSCORED / ORDER SEND DISABLED

Code freeze used for the real V0.1 runs: `ccffd9d`.

## Frozen V0.1 observed classifications

All three frozen windows completed through durable jobs with exit code 0 and classified `STATE_DIVERGENCE_OBSERVED`:

- `W2022_09`;
- `W2023_09`;
- `W2026_08_24`.

These results are retained as project history and are not deleted or rewritten.

## Runtime observation that exposed a representation defect

Dukascopy raw rows versus positive-volume rows:

- W2022_09: raw 43,200; `volume > 0` 30,089; `volume <= 0` 13,111; Exness observed M1 29,879;
- W2023_09: raw 43,200; `volume > 0` 28,658; `volume <= 0` 14,542; Exness observed M1 28,554;
- W2026_08_24: raw 1,440; `volume > 0` 1,380; `volume <= 0` 60; Exness observed M1 1,378.

Most zero/non-positive-volume rows in the month windows occur during weekends, with additional weekday rows. Positive-volume weekend rows also exist and are not assumed invalid.

## Pre-existing frozen V2 semantic

`build_minimal_v2_from_frame()` in `minimal_v2_0700.py` normalizes M1 then, when `volume` exists, passes only `volume > 0` rows into the frozen V2 core.

This rule existed before the overlap outcomes were observed.

## Defect

Overlap runner V0.1 normalized Dukascopy M1 but did not apply the pre-existing `volume > 0` active-M1 filter before H4/PAT/origin construction.

Therefore V0.1 compared a Dukascopy representation containing non-active zero-volume rows against Exness tick-derived observed M1. This can create H4 continuity/PAT differences that are representation artifacts rather than the intended frozen-V2 cross-feed sensitivity.

## Classification of V0.1 evidence

- V0.1 runtime execution: VALID engineering observation for the implementation that actually ran;
- V0.1 use as frozen-V2 feed sensitivity evidence: SUPERSEDED / NOT DECISION-ELIGIBLE due to active-M1 semantic mismatch;
- canonical Exness COMPLETE seed: NOT ESTABLISHED;
- cross-feed initialization: NOT AUTHORIZED.

No Win Rate, expectancy, profitability, holdout score, broker-fill claim, or order action was produced.