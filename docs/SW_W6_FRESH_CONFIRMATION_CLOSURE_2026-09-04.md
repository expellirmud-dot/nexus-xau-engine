# SW W6 Frozen Confirmation Closure — 2026-09-04

Status: CLOSED / NOT_CONFIRMED

## Question

Does the previously selected exploratory Sideway proxy — `W6 Oscillation Strength` — survive a genuinely later untouched period when its window and thresholds are frozen before seeing the new outcomes?

## Frozen rule from prior round

- H1 lookback window: 6 active H1 bars strictly before the first PAT2 H1 candle.
- Feature: oscillation strength = `1 - abs(last_close - first_close) / sum(abs(close changes))`.
- Low bucket: `<= 0.3133975223863906`.
- High bucket: `>= 0.7837295932951441`.
- Anchor: H1 PAT2 BODY research variant.
- Outcome control: H1 1,000 project points over next 24 active H1 bars, with symmetric adverse barrier used only as a research control.
- No threshold tuning on the fresh period.

## Fresh dataset

Dukascopy cached BID M1:

- start: 2023-09-01
- end: 2023-11-23
- rows: 120,960
- cache range complete: yes
- missing cache dates in this chosen confirmation range: none
- data source remains research-only and distinct from Exness/MT5 execution feed

The broader 2023-09-01 to 2023-11-30 cache had missing dates 2023-11-24 and 2023-11-25, so the confirmation range was intentionally frozen to 2023-11-23 rather than silently using an incomplete range.

## Result

Measured H1 PAT2 BODY anchor events: 449

Frozen buckets:

- low oscillation: 132 events
- high oscillation: 119 events

Relationship metrics:

- Spearman vs target-first: `-0.03230`
- Spearman vs target reach: `+0.01095`
- Spearman vs MFE: `+0.03412`
- Spearman vs MAE: `-0.01843`

Low bucket:

- resolved target-first: 52.94%
- target reach anywhere: 44.70%
- median MFE: 804.0 points
- median MAE: 842.05 points

High bucket:

- resolved target-first: 51.00%
- target reach anywhere: 47.06%
- median MFE: 973.0 points
- median MAE: 774.7 points

## Closure

`NOT_CONFIRMED`

Reason: the frozen confirmation rule requires the relation to be directionally favorable across target-first, target reach, MFE and MAE, with the high bucket also beating the low bucket on both target-first and target reach. The fresh period fails because target-first relation is negative and high-bucket target-first is lower than the low bucket.

This does not prove that Sideway is useless. It rejects this specific `6 H1 + oscillation strength` standalone proxy as a robust confirmed filter under the current H1 PAT2 BODY / fresh-target representation.

## What changed

Before this checkpoint:

`W6 Oscillation Strength = EXPLORATORY_SUPPORTED_CANDIDATE`

After this checkpoint:

`W6 Oscillation Strength = NOT_CONFIRMED_ON_FRESH_PERIOD`

Therefore it must not be promoted into a production or canonical SW rule.

## Research consequence

Do not retune W6 thresholds on the 2023-09-01 to 2023-11-23 confirmation period. That would convert the confirmation set into discovery data.

The next high-value direction is not more W6 threshold search. Move to a different predeclared state equation, especially `INHERITED_REMAINING_RUN` and its interaction with Daily Frame / Location, because the project evidence explicitly states that a Daily-Frame entry can inherit only the unfinished portion of an older H1/H4/D run rather than resetting a full target.

## Engineering additions

- `src/nexus_xau/data/dukascopy_cache_export.py`: deterministic offline export from already cached daily `.bi5` files, exposing missing cache dates instead of making network availability part of a research run.
- `src/nexus_xau/research/sw_w6_frozen_confirmation.py`: frozen, no-retuning confirmation runner for the W6 candidate.

Generated research outputs remain under ignored `results/` and raw data paths.
