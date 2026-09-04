# Sideway (SW) Proxy Variant Relation Test Plan — 2026-09-04

Status: PREDECLARED BEFORE RESULT REVIEW

## Purpose

Apply the project owner's bounded unknown-variant method to the unresolved Sideway detector without inventing a canonical SW frame formula.

Project evidence supports the high-level semantics:

- Sideway is price oscillating while waiting for a frame break / new SIG.
- Sideway duration is not fixed.
- repeated/equal highs/lows appear in examples.
- `กรอบ SW ครบ`, exact upper/lower construction, breakout and false-break geometry remain unresolved.

Therefore this experiment tests measurable **shape proxies**, not a canonical SW detector.

## Research question

Before an H1 PAT2 BODY research-anchor forms, do measurable oscillation/overlap characteristics over recent active H1 bars show a stable relationship with the subsequent H1 1,000-project-point fresh-target outcome?

This is `OUTCOME USEFULNESS` only. No source-labeled SW truth set currently exists in sufficient chart-aligned form to answer `SOURCE-RULE IDENTIFICATION`.

## Anchor and outcome source

Reuse the already-built MTF Round-01 event table and deduplicate to one row per H1 PAT2 BODY anchor.

- Anchor = H1 PAT2 BODY research variant.
- Outcome = same fresh-target H1 1,000-point control already measured in MTF Round 01.
- Symmetric 1,000-point adverse barrier remains a research control, not canonical SL.
- This avoids recomputing outcomes and preserves exact sample consistency with the previous component experiment.

## Pre-anchor state boundary

PAT2 uses two H1 candles. For an anchor known at time `T`, SW proxy features must use only active H1 bars **strictly before the first PAT2 candle**.

Thus the SW lookback ends before `T - 2 hours`.

This keeps the candidate PAT2 itself out of the SW-state measurement.

## Duration variants — the bounded 1 / 2 / 3 search

Because source evidence says SW duration is not fixed, test three explicit research windows:

1. `SW_W6` = previous 6 active H1 bars.
2. `SW_W12` = previous 12 active H1 bars.
3. `SW_W24` = previous 24 active H1 bars.

These are research variants only. Historical performance cannot make one of them the teacher's canonical SW duration.

## Threshold-free shape features

For every duration variant, calculate three dimensionless features where larger values mean "more sideway-like" under that proxy.

### A. Oscillation strength

```text
path = sum(abs(close_t - close_t-1))
net  = abs(last_close - first_close)
oscillation_strength = 1 - net/path
```

- near 0 = mostly one-directional path;
- near 1 = much of the path cancels out / oscillates.

If path is zero, the feature is undefined and that event is excluded for this feature.

### B. Direction-flip rate

Using non-zero close-to-close changes:

```text
flip_rate = sign changes between consecutive non-zero close changes
            / possible sign-change pairs
```

Higher = more back-and-forth direction changes.

### C. Consecutive-candle overlap

For each adjacent pair of H1 candles:

```text
overlap = max(0, min(high1, high2) - max(low1, low2))
normalized_overlap = overlap / min(range1, range2)
```

Average normalized overlap across the window.

Higher = more repeated occupation of the same price area.

## Data-quality rules

- Dukascopy XAUUSD BID research feed.
- Use the same positive-volume-only H1 reconstruction used in MTF Round 01.
- Do not bridge synthetic market-closed zero-volume minutes.
- Exclude an anchor/window if the pre-anchor SW lookback crosses one of the currently known failed Dukascopy dates.
- Keep Dukascopy distinct from Exness/MT5 execution feed.

## Chronological split

Reuse the frozen MTF Round-01 split:

- DEV: before 2023-02-01 UTC.
- VAL: 2023-02-01 through before 2023-05-01 UTC.
- TEST: 2023-05-01 onward.

## Metrics

For each `(window, feature)` and split:

- event count;
- Spearman relation vs resolved target-first;
- Spearman relation vs target-reach-anywhere;
- Spearman relation vs MFE;
- Spearman relation vs MAE;
- DEV q25/q75 feature thresholds;
- held-out bottom-quartile vs top-quartile outcome summaries for interpretability.

Spearman is implemented as Pearson correlation of average ranks, avoiding an unnecessary SciPy dependency.

## Frozen closure rule

For each `(window, feature)`:

- require >=100 events on each of VAL and TEST;
- require >=20 events in both DEV-frozen low/high quartile groups on each held-out split;
- `SUPPORTED_POSITIVE_RELATION` only if VAL and TEST both show:
  - target-first correlation > 0;
  - target-reach correlation >= 0;
  - MFE correlation >= 0;
  - MAE correlation <= 0;
  - and the high-proxy quartile has higher resolved target-first and no-lower target reach than the low-proxy quartile;
- `NOT_SUPPORTED_POSITIVE_RELATION` only if both held-out splits consistently oppose the expected positive-filter direction;
- otherwise `INCONCLUSIVE`.

A negative or inconclusive result rejects only that proxy as a standalone positive SW filter. It does **not** refute the teaching concept of a completed SW frame, because the proxy does not encode exact frame completion/breakout.

## Interpretation guard

- No result from this experiment may be called canonical SW geometry.
- No result may be called strategy win rate.
- Outcome usefulness cannot identify teacher intent.
- If all simple proxies fail, next step is not endless threshold tuning; move to interaction tests with Daily-Frame/Location and/or seek chart-aligned SW labels.
