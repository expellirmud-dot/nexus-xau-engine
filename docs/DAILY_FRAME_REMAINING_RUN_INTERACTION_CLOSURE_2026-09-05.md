# Daily Frame <=200 × PATH_REMAINING Closure — 2026-09-05

Status: CLOSED — INCONCLUSIVE_DUE_RARITY

## Question

Within H1 `INHERITED_REMAINING_RUN` events, does `EXPECTED_SIDE_WITHIN_200` outperform `OUTSIDE_200_CONTROL` on PATH_REMAINING completion behavior?

## Frozen representation

The representation and closure rule are defined in `docs/DAILY_FRAME_REMAINING_RUN_INTERACTION_PLAN_2026-09-04.md`.

No threshold was changed after outcomes were inspected.

## Results

### 2022-09 -> 2023-03

- inherited measured: 285
- EXPECTED_SIDE_WITHIN_200: 60
- CROSSED_SIDE_WITHIN_200: 26
- OUTSIDE_200_CONTROL: 199
- expected target-first: 73.21%
- expected PATH_REMAINING reach: 76.67%
- expected fresh MFE median: about 1150 points
- expected fresh MAE median: about 920.45 points
- outside target-first: 63.08%
- outside PATH_REMAINING reach: 72.36%
- outside fresh MFE median: about 990.1 points
- outside fresh MAE median: about 1059 points

Period state: `SUPPORT`.

### 2024-09 -> 2024-11

- EXPECTED_SIDE_WITHIN_200: 4
- CROSSED_SIDE_WITHIN_200: 8
- OUTSIDE_200_CONTROL: 35

Period state: `INSUFFICIENT`.

### 2025-09 -> 2025-11

- EXPECTED_SIDE_WITHIN_200: 2
- CROSSED_SIDE_WITHIN_200: 2
- OUTSIDE_200_CONTROL: 25

Period state: `INSUFFICIENT`.

## Closure

Project-level decision: `INCONCLUSIVE_DUE_RARITY`.

The <=200 interaction is not rejected, but later periods do not contain enough expected-side-within-200 events to establish cross-period support. Do not widen 200 to 300/500 after seeing the result; that would be post-outcome tuning.

The result is consistent with <=200 being setup-specific rather than a universal Daily Frame location tolerance. This closure motivated the threshold-free `EXPECTED_SIDE` versus `CROSSED_SIDE` test without changing the Daily Frame construction itself.

## Non-claims

- <=200 is not a universal PAT location tolerance.
- CROSSED_SIDE is not automatically invalid.
- PATH_REMAINING remains a research representation.
- PAT2 BODY remains a research representation.
- No strategy win rate or production entry rule is established.
