# MTF Alignment Variant Relation — Round 01 Closure — 2026-09-04

Status: CLOSED COMPONENT EXPERIMENT / ALL THREE VARIANTS INCONCLUSIVE

## Question

For H1 PAT2 BODY research-variant anchors, does a larger count of same-direction H1/M30/M15/M5 PAT2 BODY alignments associate with better H1 1,000-project-point forward behavior?

This experiment implements the user-direct research method:

```text
UNKNOWN VALUE / SHAPE
-> define bounded variant 1 / 2 / 3
-> measure relation
-> close result
-> use result to choose next question
```

## Frozen variants

1. `EXACT_COMPLETION`
2. `RECENT_1_TF_BAR`
3. `RECENT_2_TF_BARS`

Alignment uses the latest PAT2 BODY research event on H1/M30/M15/M5 and counts a timeframe only when the latest event is both fresh under the tested variant and in the H1 anchor direction.

## Data and integrity handling

- Feed: Dukascopy XAUUSD BID M1.
- Export range: 2022-09-01 through 2023-08-31.
- Source export currently contains 347 downloaded dates and 18 failed download dates.
- Any anchor outcome window intersecting a failed date was excluded during event construction.
- Pre-result audit found Dukascopy daily candle files contain zero-volume flat placeholder minutes during market closure; M1 rows with `volume <= 0` were removed before resampling and forward measurement.
- Forward control horizon: next 24 active H1 bars, not 24 wall-clock hours.
- Project point: 0.01 price.
- Favorable target: H1 1,000 project points.
- Symmetric 1,000-point adverse barrier is a research control, not a canonical SL.
- Outcome model is `FRESH_TARGET_CONTROL`, not inherited remaining-run.

Chronological split frozen before outcome review:

- DEV: before 2023-02-01 UTC.
- VAL: 2023-02-01 through before 2023-05-01 UTC.
- TEST: 2023-05-01 onward.

Measured event table:

- 1,789 unique H1 anchors.
- 5,367 rows across the three alignment variants.

## Closure rule

A variant is `SUPPORTED` only when both VAL and TEST show the expected direction for all four relationship metrics:

- alignment count vs resolved target-first: positive;
- alignment count vs target-reach-anywhere: non-negative;
- alignment count vs MFE: non-negative;
- alignment count vs MAE: non-positive;

Minimum evidence per held-out split:

- >=100 events;
- at least two alignment-count levels with >=20 events each.

`NOT_SUPPORTED` requires both held-out splits to consistently oppose the expected relationship. Otherwise close `INCONCLUSIVE`.

## Results

### Variant 1 — EXACT_COMPLETION

VAL:

```text
state = OPPOSE
n = 487
rho(target-first) = -0.0214
rho(target-reach) = -0.0291
rho(MFE)          = -0.0370
rho(MAE)          = +0.0721
```

TEST:

```text
state = SUPPORT
n = 504
rho(target-first) = +0.1614
rho(target-reach) = +0.1123
rho(MFE)          = +0.0939
rho(MAE)          = -0.1098
```

Closure:

`INCONCLUSIVE`

The held-out periods disagree materially.

### Variant 2 — RECENT_1_TF_BAR

VAL:

```text
state = MIXED
n = 487
rho(target-first) = +0.0219
rho(target-reach) = +0.0336
rho(MFE)          = +0.0372
rho(MAE)          = +0.0451
```

TEST:

```text
state = SUPPORT
n = 504
rho(target-first) = +0.0252
rho(target-reach) = +0.0159
rho(MFE)          = +0.0324
rho(MAE)          = -0.0475
```

Closure:

`INCONCLUSIVE`

VAL shows mildly favorable return-side relationships but adverse excursion moves in the wrong direction.

### Variant 3 — RECENT_2_TF_BARS

VAL:

```text
state = MIXED
n = 487
rho(target-first) = +0.0421
rho(target-reach) = +0.0207
rho(MFE)          = +0.0180
rho(MAE)          = +0.0387
```

TEST:

```text
state = SUPPORT
n = 504
rho(target-first) = +0.0489
rho(target-reach) = +0.0503
rho(MFE)          = +0.0749
rho(MAE)          = -0.0737
```

Closure:

`INCONCLUSIVE`

Again the TEST period supports the expected direction while VAL does not satisfy the adverse-path requirement.

## What changed in our understanding

Before this experiment, `more aligned H1/M30/M15/M5 PA is stronger` was a direct user semantic with no measured operational proxy.

After this experiment:

1. Three bounded PAT2-BODY recency representations have been measured and closed.
2. None is robust enough to become a standalone MTF filter.
3. All three show favorable relationship direction in the TEST period, but not consistently in VAL.
4. This pattern is compatible with a **conditional / regime-dependent interaction** rather than a universal standalone MTF effect.
5. Outcome performance still cannot choose a production minimum such as 2/3/4 aligned TFs.

## What this result does NOT mean

- It does not refute the user's direct teaching semantic about true PA alignment.
- PAT2 BODY is only a research proxy; PAT1/PAT3/full PA are not represented.
- Daily Frame, Location, SW and inherited remaining-run were intentionally absent.
- These target-first rates are not strategy win rate.

## Next question chosen from the result

Do not keep searching alignment thresholds in isolation.

The next higher-value path is interaction-first:

```text
H1 PAT2 BODY
+ Daily-Frame / Location state
+ candidate SW state
+ MTF alignment count
-> compare forward behavior
```

In parallel, the major unresolved `SW` concept should be converted into a small bounded set of measurable proxy families and tested separately for source consistency and outcome usefulness.

Source outputs:

- `results/MVP_MTF_ALIGNMENT_VARIANTS_DUKA_2022-09_2023-08.json`
- `results/MVP_MTF_ALIGNMENT_VARIANTS_DUKA_2022-09_2023-08_EVENTS.csv`
- `docs/MTF_ALIGNMENT_VARIANT_TEST_PLAN_2026-09-04.md`
