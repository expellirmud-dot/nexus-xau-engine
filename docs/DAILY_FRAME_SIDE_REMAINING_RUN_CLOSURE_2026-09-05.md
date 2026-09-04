# Daily Frame Side × PATH_REMAINING Closure — 2026-09-05

Status: CLOSED — SUPPORTED_RESEARCH_REPRESENTATION

## Question

Within H1 events already classified as `INHERITED_REMAINING_RUN`, does being on the direction-correct side of the 07:00 Daily Frame relate to better `PATH_REMAINING` completion behavior than being on the crossed side, without using the 200-point proximity gate?

## Representation

- 07:00 Asia/Bangkok = 00:00 UTC.
- H1 PAT2 BODY remains a research representation, not canonical full PA/SIG.
- `PATH_REMAINING` remains the working research target representation, not proven teacher formula.
- BUY location uses the two-candle PAT2-window Low relative to Daily Frame lower/support.
- SELL location uses the two-candle PAT2-window High relative to Daily Frame upper/resistance.
- `EXPECTED_SIDE`: signed directional frame distance >= 0.
- `CROSSED_SIDE`: signed directional frame distance < 0.
- No 200-point tolerance is used in this test.
- Minimum group size = 10 events.

## Results

### 2022-09-01 -> 2023-03-31

EXPECTED_SIDE:
- events: 195
- resolved: 188
- target-first: 65.96%
- PATH_REMAINING reach: 74.36%
- fresh MFE median: 1068.8 points
- fresh MAE median: 1032.0 points

CROSSED_SIDE:
- events: 90
- resolved: 88
- target-first: 63.64%
- PATH_REMAINING reach: 68.89%
- fresh MFE median: 944.5 points
- fresh MAE median: 1078.0 points

Period state: `SUPPORT`.

### 2024-09-01 -> 2024-11-30

EXPECTED_SIDE:
- events: 22
- resolved: 22
- target-first: 68.18%
- PATH_REMAINING reach: 95.45%
- fresh MFE median: 1266.7 points
- fresh MAE median: 1269.45 points

CROSSED_SIDE:
- events: 25
- resolved: 25
- target-first: 56.00%
- PATH_REMAINING reach: 72.00%
- fresh MFE median: 1128.0 points
- fresh MAE median: 1945.9 points

Period state: `SUPPORT`.

### 2025-09-01 -> 2025-11-30

EXPECTED_SIDE:
- events: 9
- resolved: 9
- target-first: 77.78%
- PATH_REMAINING reach: 100.00%
- fresh MFE median: 3673.0 points
- fresh MAE median: 1634.3 points

CROSSED_SIDE:
- events: 20
- resolved: 20
- target-first: 70.00%
- PATH_REMAINING reach: 95.00%
- fresh MFE median: 4333.65 points
- fresh MAE median: 3314.85 points

Period state: `INSUFFICIENT` because EXPECTED_SIDE has 9 events, below the frozen minimum of 10. The observed target-first/reach direction is nevertheless consistent with the two usable periods and is retained only as descriptive context.

## Closure

Two usable periods independently meet the frozen minimum and both show higher target-first and no-lower PATH_REMAINING reach for `EXPECTED_SIDE` versus `CROSSED_SIDE`. The third period is formally insufficient but does not reverse the observed target-first/reach direction.

Project-level decision: `SUPPORTED_RESEARCH_REPRESENTATION`.

This supports carrying Daily Frame directional-side state forward as a conditional research feature under inherited `PATH_REMAINING` state. It does **not** establish a production rule, universal penetration invalidation rule, canonical Daily Frame tolerance, canonical PAT2 formula, strategy win rate, or teacher formula.

## What changed from the <=200 interaction

The prior <=200 interaction was `INCONCLUSIVE_DUE_RARITY` because later-period samples were too sparse. Removing the proximity gate without inventing a replacement threshold produced usable expected-vs-crossed groups in two periods and a consistent directional relation in the third insufficient period.

The evidence therefore currently favors **which side of the Daily Frame** over the exact <=200 proximity as the more useful research representation.

## Next bounded question

Carry forward:

`PATH_REMAINING + Daily Frame directional side + graded MTF alignment`

MTF alignment must remain a graded feature (`aligned_tf_count` / aligned set), not a newly invented hard gate. If that interaction is unstable, move next to bounded origin expiry/invalidation, age, consumed-run ratio, and same-day-vs-older inherited-origin variants.
