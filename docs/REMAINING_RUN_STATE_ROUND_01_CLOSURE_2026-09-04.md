# Remaining Run State Round 01 Closure — 2026-09-04

Status: CLOSED / STATE EFFECT INCONCLUSIVE; PATH_REMAINING RETAINED AS RESEARCH REPRESENTATION

## Primary question

Does an H1 `INHERITED_REMAINING_RUN` state at the 07:00 preparation boundary add measurable information versus `NO_ACTIVE_INHERITED_RUN` for the first same-direction H1 PAT2 BODY candidate after the cutoff?

## Representation

- 07:00 Asia/Bangkok = 00:00 UTC.
- H1 PAT2 BODY is the research origin/candidate proxy.
- PAT2 post-SIG mapping uses candle #3.
- BUY post-SIG anchor = Low of candle #3; SELL = High.
- Active origin = latest same-direction pre-cutoff origin whose nominal H1 1,000-point run is incomplete both at the cutoff and at candidate completion.
- First post-cutoff H1 PAT2 BODY candidate per side per day is used.
- Primary comparison uses the same fresh 1,000-point target control for inherited and no-active groups over the next 24 active H1 bars.
- Symmetric 1,000-point adverse barrier remains a research control, not canonical SL.

## Frozen closure rule

Minimum 30 events in both groups.

`SUPPORTED` only if inherited state has all four:

1. higher resolved target-first rate,
2. no-lower target-reach rate,
3. no-lower median MFE,
4. no-higher median MAE.

Reverse all four => `NOT_SUPPORTED`.
Otherwise => `INCONCLUSIVE_MIXED` or `INCONCLUSIVE_INSUFFICIENT`.

## Period results

### Discovery: 2022-09-01 through 2023-03-31

Cache-complete range.

- inherited events: 285
- control events: 15
- decision: `INCONCLUSIVE_INSUFFICIENT`

Inherited fresh-1000:

- target-first resolved: 47.18%
- target reach: 50.18%
- median MFE: 1,001.0 points
- median MAE: 1,036.7 points

Control fresh-1000:

- target-first resolved: 33.33%
- target reach: 33.33%
- median MFE: 685.0 points
- median MAE: 1,380.0 points

The direction looks favorable for inherited state, but control n=15 is below the frozen minimum. No upgrade is allowed.

### Later period: 2024-09-01 through 2024-11-30

Cache has missing dates; event paths/horizons crossing missing dates were excluded.

- inherited events: 47
- control events: 24
- decision: `INCONCLUSIVE_INSUFFICIENT`

Inherited fresh-1000:

- target-first resolved: 43.48%
- target reach: 59.57%
- median MFE: 1,144.0
- median MAE: 1,568.9

Control:

- target-first resolved: 59.09%
- target reach: 66.67%
- median MFE: 1,858.55
- median MAE: 857.15

Direction here favors control, so the state effect is not stable across regimes.

### Later period: 2025-09-01 through 2025-11-30

Cache has missing dates; event paths/horizons crossing missing dates were excluded.

- inherited events: 29
- control events: 45
- decision: `INCONCLUSIVE_INSUFFICIENT`

Inherited fresh-1000:

- target-first resolved: 51.72%
- target reach: 89.66%
- median MFE: 3,752.0
- median MAE: 3,211.7

Control:

- target-first resolved: 33.33%
- target reach: 77.78%
- median MFE: 3,669.0
- median MAE: 4,216.7

All four primary metrics favor inherited state in this period, but inherited n=29 is one below the frozen minimum 30. The threshold is not lowered after seeing the result.

## Primary closure

`INCONCLUSIVE / REGIME-DEPENDENT`

The current H1 inherited-run proxy is not established as a robust standalone state filter. Discovery and 2025 point in a favorable direction, while 2024 points the other way. Sample sufficiency also fails in every tested period under the frozen rule.

This does not reject the project rule that unfinished runs exist. It says the current state representation by itself is not enough to prove a stable outcome advantage.

## Target representation comparison

Two inherited-target formulas were measured descriptively without using outcome to claim teacher intent.

### PATH_REMAINING

`remaining = 1000 - maximum favorable progress already consumed from the origin`

Candidate target = candidate close +/- remaining points.

Reach rates:

- 2022-09 to 2023-03: 72.63%
- 2024-09 to 2024-11: 82.98%
- 2025-09 to 2025-11: 96.55%

### ORIGIN_TARGET_LEVEL

Original target remains fixed at post-SIG anchor +/-1,000 points.

Reach rates:

- 2022-09 to 2023-03: 45.61%
- 2024-09 to 2024-11: 42.55%
- 2025-09 to 2025-11: 44.83%

## Research representation decision

Carry `PATH_REMAINING` forward as the preferred **research representation** because:

1. it directly operationalizes the project-owner example: nominal run minus consumed run equals remaining run;
2. it is deterministic and no-lookahead once origin and cutoff are known;
3. it produces a materially distinct outcome representation across all tested periods.

Important guard:

This is NOT a claim that outcome performance proves teacher intent or closes the canonical formula. `ORIGIN_TARGET_LEVEL` remains preserved as a comparator until source evidence explicitly distinguishes the two.

## What this round appears to have solved

Not the standalone edge of Remaining Run.

The useful closure is architectural:

`Remaining Run should be modeled as a path/state variable, not automatically as a reset full target and not silently as a fixed old target level.`

The next hypothesis should test interaction rather than state alone:

`Daily Frame / Location + PATH_REMAINING state + qualifying H1 PAT2 BODY`

MTF alignment should be reintroduced only after the state/location interaction is measured, because standalone MTF already closed inconclusive.

## Limitations

- PAT2 BODY remains a proxy.
- Exact post-SIG destruction/invalidation is not applied.
- Latest eligible origin is a research conflict-resolution variant, not canonical hierarchy.
- Daily Frame/Location is deliberately absent from this component round.
- Missing-date exclusions reduce later-period sample sizes.
- Research feed is Dukascopy BID, distinct from Exness/MT5 execution feed.
