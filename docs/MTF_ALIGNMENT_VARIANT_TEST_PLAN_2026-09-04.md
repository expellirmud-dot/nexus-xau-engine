# MTF Alignment Variant Relation Test Plan — 2026-09-04

Status: PREDECLARED BEFORE RESULT REVIEW

## Question

For H1 PAT2 BODY research-variant anchors, does a larger count of same-direction H1/M30/M15/M5 PAT2 BODY alignments associate with better H1 1,000-project-point forward behavior?

This is a component test only. It does not claim to represent the complete canonical PA/SIG system.

## Anchor

- H1 PAT2 BODY midpoint-pass research variant.
- BUY = bearish candle then bullish candle, with candle #2 close above candle #1 body midpoint.
- SELL = bullish candle then bearish candle, with candle #2 close below candle #1 body midpoint.
- Anchor known_at is after the second H1 candle closes.
- Fresh-target control reference price = completed anchor close.

## Alignment proxy

For each of H1/M30/M15/M5, find the latest PAT2 BODY event known at or before the H1 anchor known_at. Count it as aligned only if:

1. the latest event side matches the H1 anchor side; and
2. it is fresh under the tested lookback definition.

## Frozen lookback variants

1. `EXACT_COMPLETION` — PAT2 BODY completes at the same known_at timestamp as the H1 anchor.
2. `RECENT_1_TF_BAR` — latest PAT2 BODY event is within one completed bar duration of that timeframe.
3. `RECENT_2_TF_BARS` — latest PAT2 BODY event is within two completed bar durations of that timeframe.

The resulting aligned-timeframe count is 0–4 in principle; H1 anchor construction should usually make H1 itself aligned.

## Data

Primary first run:

- Dukascopy XAUUSD BID M1
- 2022-09-01 through 2023-08-31 available cache/export
- Failed download dates from metadata are explicitly excluded when an anchor's forward outcome window intersects them.

Chronological split frozen before result review:

- DEV: before 2023-02-01 UTC
- VAL: 2023-02-01 through before 2023-05-01 UTC
- TEST: 2023-05-01 onward

## Data-quality amendments before outcome review

A pre-result audit found that each downloaded Dukascopy day contains exactly 1,440 M1 rows, including market-closed periods. Example: 2023-01-01 begins with flat candles and `volume=0`. Therefore the first experiment will use only M1 rows with `volume > 0` before resampling and forward measurement. This prevents zero-volume placeholder minutes from manufacturing artificial PA/topology during closed periods.

The first attempted run then stopped before producing an outcome report because some anchors had no active M1 bars in the next 24 wall-clock hours across market closure. To keep the control consistent with the project's earlier H1 horizon concept, the frozen forward horizon is amended to the **next 24 active H1 bars** after anchor known_at, not 24 wall-clock hours. This change was made after an execution/data-availability failure and before any MTF-alignment outcome result was produced.

These amendments are data/horizon integrity corrections, not performance-tuned parameters.

## Outcome control

- H1 target = 1,000 project points.
- Project point = 0.01 price.
- Horizon = next 24 active H1 bars after anchor known_at.
- Symmetric 1,000-point adverse barrier = research control only, not canonical SL.
- This is `FRESH_TARGET_CONTROL`, not inherited remaining-run.

## Relationship metrics

Per alignment variant and chronological split:

- count distribution 0/1/2/3/4;
- resolved target-first rate by count;
- target-reach-anywhere rate by count;
- median MFE / MAE by count;
- Spearman relation of alignment count with target-first, target reach, MFE and MAE.

## Frozen closure rule

Held-out evidence requires at least 100 measured events and at least two alignment-count levels with at least 20 events each.

Per lookback variant:

- `SUPPORTED` only when both VAL and TEST show positive/non-negative relationship for target-first, target reach and MFE, and non-positive relationship for MAE.
- `NOT_SUPPORTED` only when both VAL and TEST consistently oppose those directions.
- Otherwise `INCONCLUSIVE`.

## Interpretation guard

- PAT2 BODY is a research proxy, not canonical full PA.
- A weak result does not refute the user's direct statement that more true PA alignment is stronger; it can instead reject this proxy/recency representation.
- Historical outcomes cannot select a production minimum aligned-TF count.
- Result does not establish strategy win rate.
