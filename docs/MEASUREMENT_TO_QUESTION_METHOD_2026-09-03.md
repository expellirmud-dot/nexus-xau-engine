# Measurement-to-Question Method — 2026-09-03

Status: ACTIVE PROJECT RESEARCH METHOD

## Origin

Project owner proposed a practical research principle from prior image-analysis work: when a system is not yet understood, do not begin by forcing a complete formula. Isolate only the observable component of interest, measure it without contamination from unrelated components, then ask what uncertainty that measurement can actually resolve.

Illustrative owner analogy:

```text
Do not measure the whole face if the question is about the painted cheek color.
Exclude eyes/hair/other regions.
Measure only the painted cheek region.
Then use that value to answer the specific color question.
```

## Canonical research principle

For every unresolved trading concept, NEXUS must build a mapping:

```text
OBSERVABLE
-> MEASURABLE FEATURE
-> COMPARISON / CALCULATION
-> QUESTION IT CAN RESOLVE
-> QUESTION IT CANNOT RESOLVE
```

Do not calculate a feature merely because it is available. Every measurement must have an explicit decision-critical question attached to it.

## Example for XAU MVP

### Daily frame at 07:00
Observable:
- price and completed higher-timeframe bars available at 07:00 local project time.

Measurable feature:
- frame center / upper / lower boundaries under the currently supported Mae Pla construction.

Can help answer:
- whether valid H1/H4 SIGs cluster near the daily frame;
- whether outcomes differ inside vs outside the frame context;
- whether daily-frame location adds information beyond PAT topology alone.

Cannot by itself answer:
- whether an entry is valid;
- whether Sideway is correctly identified;
- whether a full strategy has positive expectancy.

### H1 / H4 SIG candidate
Observable:
- candle sequence, location context, post-SIG reference, later path.

Measurable feature:
- candidate timestamp, direction, PAT family, TF, distance to frame, MFE/MAE, first-hit distance/time.

Can help answer:
- whether source-backed SIG candidates on H1/H4 tend to reach the teaching run distance;
- whether H1 and H4 behave differently;
- whether location/state filters improve outcomes versus topology-only controls.

Cannot by itself answer:
- canonical win rate until entry/SL/invalidation are frozen.

### H1 1000 / H4 1500 teaching run
Observable:
- post-SIG anchor and subsequent OHLC path.

Measurable feature:
- target distance reached/not reached, MFE, MAE, first-hit timestamps.

Can help answer:
- whether the teaching run distance is commonly achieved after valid candidates;
- how much adverse movement occurs before the run;
- whether the run distance differs by state/location.

Cannot by itself answer:
- trade profitability without entry, SL, costs and exit policy.

## Required question card before new calculations

Before a new research calculation, write or mentally establish:

1. What exactly are we measuring?
2. What unrelated information must be excluded to avoid contamination?
3. Which unresolved claim does this measurement test?
4. What result would support the claim?
5. What result would weaken/refute it?
6. What will still remain unknown even after the calculation?

If these cannot be answered, do not run the calculation yet.

## Research consequence

This method replaces broad feature accumulation with targeted uncertainty reduction.

Preferred loop:

```text
UNKNOWN
-> identify one visible/measurable component
-> isolate it
-> measure it
-> compare against a specific hypothesis/control
-> close, weaken, parameterize, or leave the claim unresolved
-> only then select the next component
```

This is compatible with the project objective `QUALITY_OF_SEQUENTIAL_DECISIONS_UNDER_UNCERTAINTY` and the evidence-first research loop.
