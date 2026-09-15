# Phase 1 Dukascopy ↔ Exness Overlap Sensitivity Result V0.2 — 2026-09-16

Status: REAL OVERLAP OBSERVED / DIRECT EXACT CROSS-FEED STATE TRANSFER NOT SUPPORTED / HOLDOUT UNSCORED / ORDER SEND DISABLED

Contract: `docs/PHASE1_DUKASCOPY_EXNESS_OVERLAP_SENSITIVITY_CONTRACT_V0.2_2026-09-16.md`
Implementation freeze: `bb32e07`

V0.1 historical observations remain preserved but are superseded for decision use by the active-M1 representation defect. This checkpoint uses only the corrected V0.2 reruns.

## Durable execution

All three frozen windows completed once with exit code 0 and no retry:

- `XAU-OVERLAP-V02-W2022-09-20260916`;
- `XAU-OVERLAP-V02-W2023-09-20260916`;
- `XAU-OVERLAP-V02-W2026-08-24-20260916`.

Result namespace: `results/dukascopy_exness_overlap_v02/`.
## Frozen result summary

| Window | Classification | Duk active M1 | Exness M1 | Common M1 | Duk-only M1 | Exness-only M1 | H4 timestamps |
|---|---|---:|---:|---:|---:|---:|---|
| W2022_09 | `STATE_DIVERGENCE_OBSERVED` | 30,089 | 29,879 | 29,879 | 210 | 0 | 136 vs 136, exact timestamp set |
| W2023_09 | `STATE_DIVERGENCE_OBSERVED` | 28,658 | 28,554 | 28,504 | 154 | 50 | 130 vs 130, exact timestamp set |
| W2026_08_24 | `STATE_DIVERGENCE_OBSERVED` | 1,380 | 1,378 | 1,378 | 2 | 0 | 6 vs 6, exact timestamp set |

V0.2 removed the false H4 timestamp expansion caused by zero/non-positive-volume Dukascopy rows. All three windows now have identical H4 timestamp sets between sources.

Despite that correction, structural V2 state still diverges.
## Structural divergence

### W2022_09

- PAT H4: Dukascopy 51, Exness 52, common 49, Dukascopy-only 2, Exness-only 3.
- Origins: Dukascopy 50, Exness 50, common 48, source-only 2 on each side.
- One matched origin has a different terminal category:
  - `BUY|2022-09-16T08:00:00+00:00`;
  - Dukascopy: `POINT_CHECK_DESTROYED`;
  - Exness: `RUN_COMPLETE`.
- Matched origins also contain anchor, consumed-progress, and touch-time differences.

### W2023_09

- PAT H4: Dukascopy 39, Exness 36, common 36; three Dukascopy-only PAT events.
- Origins: Dukascopy 38, Exness 36, common 36; two Dukascopy-only origins.
- Matched lifecycle state categories are equal, but anchor/consumed/touch fields are not exactly equal across the matched set.

### W2026_08_24

- PAT H4: Dukascopy 2, Exness 1, common 1; one Dukascopy-only BUY PAT.
- Origins: Dukascopy 2, Exness 1, common 1; one Dukascopy-only BUY origin.
- The one matched origin has equal terminal category but different anchor, consumed progress, and touch timestamp.

These observations satisfy the frozen `STATE_DIVERGENCE_OBSERVED` definition without introducing any tolerance.
## Result-file integrity

- `W2022_09.json` SHA-256: `24a5dd2b6050b67566cbdbcba10575558426c12fdfc87d0c41ae2ea1375703a4`.
- `W2023_09.json` SHA-256: `be9947bf9dc6c52db497819e31fe2155123de4bc66ad691e1e12d0fbbc66a29c`.
- `W2026_08_24.json` SHA-256: `0f45b2448b838a9735112bd45367533f3971acdb02de4d3931e8817911e36cc4`.

## Decision implication

`DIRECT_EXACT_DUKASCOPY_STATE_AS_EXNESS_SEED` is `NOT_SUPPORTED` by the three frozen V0.2 overlap observations.

The reason is structural, not merely numeric price offset: PAT identity sets and/or origin identity sets differ in every frozen window, and W2022 additionally contains a matched origin with a different terminal lifecycle category.

This does not prove that every Dukascopy/Exness interval will diverge. It does prove that silent exact state relabeling is not defensible as a canonical initialization method.

Dukascopy may remain useful as a separate provenance research representation. It must not be concatenated or relabeled as Exness state.

## Remaining initialization question

A canonical Exness COMPLETE seed is still not established.

The next engineering question is whether unknown prehistory can be eliminated using an Exness-only, lifecycle-derived uncertainty/closure representation rather than an arbitrary warmup or exact cross-feed state transfer.

Real Exness V2 therefore remains `DATA_EXCLUDED_ORIGIN_HISTORY_UNSEEDED`.

Protected holdout scoring remains disabled.
Automatic order sending remains disabled.