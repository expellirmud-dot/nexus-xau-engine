# Remaining Run State Test Plan — 2026-09-04

Status: FROZEN BEFORE CONFIRMATION

## Project rule being represented

Direct project guidance states that a late Daily-Frame setup can inherit only the unfinished portion of a prior H1/H4/D run rather than automatically resetting a fresh full target. Example supplied by the project owner: H4 nominal 1,500 points, 1,000 consumed before 07:00, 500 remaining.

This experiment does not attempt to prove the teacher's wording from outcomes. It tests whether a reproducible H1 research representation of `active unfinished run` adds measurable state information.

## Scope

First component test is H1 only.

- project point = 0.01
- nominal H1 run = 1,000 project points
- 07:00 Asia/Bangkok = 00:00 UTC
- PAT2 BODY midpoint-pass remains the current H1 research anchor proxy
- PAT2 post-SIG mapping uses candle #3, which is source-backed at mapping level
- BUY post-SIG anchor proxy = Low of candle #3
- SELL post-SIG anchor proxy = High of candle #3
- exact post-SIG destruction/invalidation is unresolved and therefore omitted with an explicit limitation

## Active inherited state

At each 00:00 UTC cutoff:

1. Find same-direction H1 PAT2 BODY origins whose post-SIG candle was complete before the cutoff.
2. Measure maximum favorable progress from the post-SIG anchor to the cutoff.
3. Origin is active only if favorable progress is still below 1,000 points.
4. For the first same-direction H1 PAT2 BODY candidate after the cutoff, recheck that the origin has still not completed its 1,000-point run before candidate completion.
5. If multiple origins qualify, use the latest eligible origin. This is a declared research variant, not a canonical conflict rule.

Candidate state:

- `INHERITED_REMAINING_RUN`
- `NO_ACTIVE_INHERITED_RUN`

## Primary state test

Both groups receive the same fresh-target outcome control from candidate close:

- target = 1,000 points
- adverse barrier = symmetric 1,000 points, research control only
- horizon = next 24 active H1 bars

Closure:

`SUPPORTED` only if inherited state has:

- higher resolved target-first rate,
- no-lower target-reach rate,
- no-lower median MFE,
- no-higher median MAE,

with at least 30 events in both inherited and control groups.

Reverse all four => `NOT_SUPPORTED`.
Anything else => `INCONCLUSIVE_MIXED`.

## Two remaining-target representations measured descriptively

Because project wording does not yet uniquely determine how a late entry converts old-run progress into a new target price, measure both without using outcome to claim teacher intent:

### A. PATH_REMAINING

`remaining = 1000 - maximum favorable progress already consumed from origin`

Candidate target = candidate close plus/minus this remaining number of points.

### B. ORIGIN_TARGET_LEVEL

Original target level remains fixed at:

`post_SIG_anchor +/- 1000 points`

Candidate target distance is current directional distance from candidate close to that old absolute target level.

Outcome can tell us whether one representation is operationally more useful, but cannot by itself tell us which formula is the teacher's intended rule.

## Data policy

Discovery/formulation dataset:

- Dukascopy BID cached M1 2022-09-01 through 2023-03-31
- cache complete for every date in the chosen range
- previously viewed broader period; discovery only

Fresh confirmation target:

- use a later cache period not used to formulate the equation
- missing-cache dates must be explicitly excluded from origin-to-entry state path and forward outcome horizon
- no formula changes after seeing confirmation outcomes

## Stop rule

This component closes as `SUPPORTED`, `NOT_SUPPORTED`, `INCONCLUSIVE_MIXED`, or `INCONCLUSIVE_INSUFFICIENT`.

No indefinite threshold search is allowed after closure.
