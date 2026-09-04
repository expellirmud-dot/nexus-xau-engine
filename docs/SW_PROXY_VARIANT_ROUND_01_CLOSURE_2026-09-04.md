# Sideway (SW) Proxy Variant Relation — Round 01 Closure — 2026-09-04

Status: CLOSED EXPLORATORY COMPONENT ROUND / ONE CANDIDATE SURVIVES / FRESH CONFIRMATION REQUIRED

## Research question

Before an H1 PAT2 BODY research anchor, do simple pre-anchor oscillation/overlap proxies over 6/12/24 active H1 bars show a stable positive relationship with the subsequent H1 1,000-project-point fresh-target control outcome?

This round implements the user-direct bounded-search method:

```text
unknown SW duration / shape
-> candidate 1 / 2 / 3 windows
-> threshold-free measurable features
-> relationship test
-> eliminate / retain
-> fresh confirmation before promotion
```

## Evidence boundary

This round addresses only `OUTCOME USEFULNESS`.

It does NOT identify the teacher's canonical SW rule because the repository still lacks a sufficiently chart-aligned SW positive/negative truth set with exact frame-completion labels.

## Data

- Dukascopy XAUUSD BID M1 export: 2022-09-01 through 2023-08-31.
- 499,680 raw M1 rows in the current export.
- 334,596 positive-volume M1 rows used for active-market reconstruction.
- Source H1 PAT2 BODY anchors: 1,789.
- 5,297 measured `(anchor, window)` rows after history / failed-date exclusions.
- 18 known failed download dates remain in the export; pre-anchor windows crossing them were excluded.
- SW history ends strictly before the first of the two H1 PAT2 candles.

Duration variants:

```text
W6  = previous 6 active H1 bars
W12 = previous 12 active H1 bars
W24 = previous 24 active H1 bars
```

Shape features:

```text
OSCILLATION_STRENGTH = 1 - abs(net close move) / sum(abs(close-to-close moves))
DIRECTION_FLIP_RATE  = rate of sign changes in non-zero close-to-close moves
CANDLE_OVERLAP_RATE  = mean normalized consecutive H1 candle-range overlap
```

All are research proxies; none is canonical SW geometry.

## Raw within-round closures

Nine `(window, feature)` combinations were evaluated under the predeclared rule.

```text
W6  OSCILLATION_STRENGTH = SUPPORTED_POSITIVE_RELATION
W6  DIRECTION_FLIP_RATE  = INCONCLUSIVE
W6  CANDLE_OVERLAP_RATE  = INCONCLUSIVE
W12 OSCILLATION_STRENGTH = INCONCLUSIVE
W12 DIRECTION_FLIP_RATE  = INCONCLUSIVE
W12 CANDLE_OVERLAP_RATE  = INCONCLUSIVE
W24 OSCILLATION_STRENGTH = INCONCLUSIVE
W24 DIRECTION_FLIP_RATE  = INCONCLUSIVE
W24 CANDLE_OVERLAP_RATE  = INCONCLUSIVE
```

Therefore eight of nine simple candidates are eliminated from priority for the next round. `W6 OSCILLATION_STRENGTH` is retained as the sole current SW outcome-proxy candidate.

## W6 Oscillation Strength — details

DEV-derived exploratory quartile thresholds:

```text
q25 low  = 0.3133975
q75 high = 0.7837296
```

These thresholds are analysis buckets only. They are NOT a canonical SW threshold.

### Validation split

```text
n = 487
rho(target-first) = +0.0599
rho(target-reach) = +0.0726
rho(MFE)          = +0.0675
rho(MAE)          = -0.0149
```

Low vs high DEV-frozen quartiles:

```text
LOW  n=129  resolved target-first=43.97%  target-reach=48.84%
HIGH n=129  resolved target-first=55.65%  target-reach=61.24%
```

The predeclared positive-filter rule is satisfied.

### Test split

```text
n = 499
rho(target-first) = +0.0280
rho(target-reach) = +0.0308
rho(MFE)          = +0.0501
rho(MAE)          = -0.0073
```

Low vs high DEV-frozen quartiles:

```text
LOW  n=128  resolved target-first=47.42%  target-reach=41.41%
HIGH n=145  resolved target-first=48.25%  target-reach=42.76%
```

The predeclared positive-filter rule is also satisfied, but the TEST effect is small.

## Strength-of-evidence interpretation

The direction is internally consistent for W6 Oscillation Strength across VAL and TEST under the frozen rule, but continuous correlations are weak and the held-out TEST high-vs-low difference is small.

Therefore the evidence supports only this statement:

> A short pre-anchor H1 oscillation-efficiency proxy is worth carrying forward as a research candidate.

It does NOT support:

- `6 H1 bars` as the teacher's SW duration;
- `0.7837` as a SW threshold;
- a canonical SW frame detector;
- a production filter;
- a system win rate.

## Holdout contamination guard — material

The Dukascopy VAL/TEST periods used here were already inspected in MTF Alignment Round 01 before this SW proxy experiment was designed.

Although the SW proxy definitions and closure rule were frozen before viewing the SW-specific results, the underlying held-out outcome behavior was not completely untouched anymore.

Therefore project-level status is:

`EXPLORATORY_SUPPORTED_CANDIDATE / NOT FRESH CONFIRMATION`

Do not upgrade W6 Oscillation Strength to confirmed research edge from this dataset.

## What changed

Before this round:

`SW = concept known, no reproducible numeric feature`

After this round:

- three duration variants and three shape features are measurable without inventing a price tolerance;
- eight of nine simple candidates are deprioritized;
- one candidate survives for fresh testing: `W6 OSCILLATION_STRENGTH`;
- exact SW frame construction/completion remains unresolved and still requires source labels for teacher-rule identification.

## Next bounded test

Do not tune more SW thresholds on the same 2022-09 to 2023-08 outcome data.

Next confirmatory question:

> On a genuinely untouched later Dukascopy period, does pre-anchor `W6 OSCILLATION_STRENGTH` retain the same positive relationship with H1 PAT2 BODY fresh-target outcomes?

If fresh confirmation survives, then test interaction rather than standalone SW:

```text
Daily Frame / Location
+ W6 oscillation candidate
+ H1 PAT2 BODY
+ MTF alignment count
-> outcome
```

Separately, source-rule identification should continue only when chart-aligned SW labels become available.

Source outputs:

- `results/MVP_SW_PROXY_VARIANTS_DUKA_2022-09_2023-08.json`
- `results/MVP_SW_PROXY_VARIANTS_DUKA_2022-09_2023-08_EVENTS.csv`
- `docs/SW_PROXY_VARIANT_TEST_PLAN_2026-09-04.md`
