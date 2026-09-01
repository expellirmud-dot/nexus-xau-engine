# Analyst Gap Review — After M5 Brake / M1–M5 Entry Transcript

Date: 2026-09-01
Primary source: user-supplied timestamp transcript associated with video `16KoS7d-koI`, coverage approximately 0:00–1:53:52.

This review does not replace prior reviews. It records how the project state changed after the dedicated M1/M5 brake-entry lesson.

## Executive conclusion

The former P0 blockers `M5 เบรก` and `ยืนกรอบ` are no longer broad discovery problems.

They are now **threshold-finalization / validation problems**.

The source directly supports:

- brake must be searched at a preplanned zone;
- zone + pattern are prerequisite context;
- M1 and M5 use the same brake pattern logic;
- five candle-force stages: large/long → weakening → rejection → color change → retest;
- weakening/rejection/color shift may combine in one candle;
- first brake is higher-risk; preferred entry is phase 2 / retest;
- structural retest requires move away / opposite-level test / return to switched support-resistance;
- frame-standing observation starts at first touch and commonly uses 4–10 candles;
- body standing is primary; wick standing/on-line may also count;
- higher-low / lower-high and local high/low destruction are structure-confirmation features;
- false first brake / overlap exists and requires reevaluation;
- M5 brake is mainly a frame/retracement/counter-round entry method, distinct from SIG entry via post-SIG anchor;
- M1 is a higher-noise refinement using trendline/structure; M5 is the safer pattern path;
- sideway examples use equal/repeated highs/lows, PA, frame-standing and limited frame interactions;
- `ซอก + ไส้ + คู่` all three together is stronger than only two, and nearest relevant zone is preferred.

## Readiness recalibration

Recommended canonical estimate after this source:

- Workflow / conceptual coverage: **~88%**
- Deterministic coding readiness: **~78%**
- Remaining deterministic gap: **~22%**

This is not live-EA readiness and not a win-rate estimate.

The increase is driven primarily by the Entry/M5 module, frame-standing semantics, sideway execution examples, and context separation between frame-brake entry and SIG entry.

## P0 blockers remaining

### 1. PAT3 variant 1/2/3 exact OHLC geometry

Still blocking exact `detect_PAT3_*()`.

Need exact body relation, close thresholds, wick constraints and invalidation for each variant.

### 2. PAT2 50% denominator/tolerance

Need to resolve whether 50% refers to prior full range, body, or chart-specific Fib placement, plus equality/tolerance.

### 3. PAT1 quantitative wick/body geometry

Topology/location are known; exact wick/body threshold remains unknown.

### 4. Quantitative thresholds for the five M5 force steps

The logical sequence is now primary-source-backed, but exact numeric definitions are not:

- `ใหญ่ยาว` body threshold;
- `อ่อนแรง` relative-body threshold;
- `reject` minimum wick/rejection threshold;
- color-shift strength threshold.

This is now a calibration problem, not a workflow-discovery problem.

### 5. Sideway canonical frame construction/completion

This lesson materially improves sideway execution, but does not fully define the official SW upper/lower frame-construction algorithm or formal `frame complete` event.

### 6. Labeled positive + negative dataset

Need enough real chart cases to validate all thresholds and state transitions before claiming exact detector quality.

Recommended minimum:

- 20–50 labeled brake examples;
- include Brake1 success/failure, overlap, no-retest failure, retest success, frame-standing success/failure, `เจิด`, M1/M5 comparison;
- store exact OHLC + frame coordinates + teacher label.

## P1 blockers / open parameters

1. Exact frame-standing tolerance: point distance, all-vs-majority rule within 4–10 candles, treatment of straddling bodies.
2. Exact local-pivot window for higher-low/lower-high and structure destruction.
3. Exact `คู่` OHLC geometry and body-collection completion event.
4. Swing-retrace starting candle and extreme-finalization.
5. Half/Swing exact entry/invalidation and operational Fib levels.
6. Daily `.0/.5` snapping tie algorithm.
7. ATH 19:00 timezone/boundary semantics.
8. Full H1/H4/D/W conflict matrix and exact M15/M30 same-direction metric.
9. Risk model: transcript gives several context-specific SL/BE examples, but no universal fixed rule.

## Critical corrections to old assumptions

- Do not implement `M5 brake = close beyond frame`.
- Do not model brake as one candle. It is a multi-state reaction/confirmation process.
- Do not treat a single wick rejection as enough; the teacher explicitly warns against this.
- Do not require each of weakening/rejection/color-change to occupy separate candles; they can combine.
- Do not enter first reaction by default; phase 2/retest is the preferred confirmation entry in this lesson.
- Do not label every frame touch as retest. Full retest requires prior move/structure interaction and return.
- Do not universalize overlap `300 points`; teacher explicitly notes volatility can stretch it.
- Do not universalize M1 SL 50–150 or frame SL 200–300; treat as setup-specific examples.
- Do not use literal chart `45°` as a raw market invariant. If implemented, normalize slope/structure rather than screen angle.

## Recommended Entry Engine v1

```text
ZONE_ARMED
  ↓
PRICE_AT_ZONE
  ↓
FORCE_IMPULSE
  ↓
FORCE_WEAKENING
  ↓
REJECTION
  ↓
COLOR_SHIFT
  ↓
BRAKE_1
  ├─ OVERLAP / FALSE BRAKE → REEVALUATE
  └─ MOVE_AWAY
        ↓
     RETEST_PENDING
        ↓
     RETEST_AT_SWITCHED_LEVEL
        ↓
     PA_CONFIRM
        ↓
     FRAME_STAND / STRUCTURE_CONFIRM
        ↓
     ENTRY_2_READY
```

Use evidence flags rather than a single boolean:

```text
zone_ok
force_sequence_score
rejection_seen
color_shift_seen
retest_seen
pa_confirmed
frame_standing_count
structure_shift
entry_phase
```

This allows replay/backtest to test which confirmations actually matter without pretending unresolved thresholds are already known.

## Highest-value next source order

1. PAT3 detailed geometry / candle-reading close-up.
2. Dedicated Sideway frame construction/completion lesson.
3. Half-retrace / Swing-retrace / Fibonacci dedicated lesson.
4. Multi-timeframe relationship/conflict lesson.
5. Labeled replay examples and negative cases.

The M5 lesson is no longer the highest discovery priority because its workflow has now been materially extracted.

## Analyst conclusion

The project has crossed another engineering boundary: **Entry/M5 is now codeable as a research state machine.**

The remaining work is concentrated in numeric geometry and labeled validation rather than understanding what the entry method is supposed to do.
