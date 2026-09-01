# NEXUS XAU Engine — Analyst Gap Review after PA/PAT primary transcript

Date: 2026-09-01
Scope: primary PA/PAT introductory lesson transcript, searchable through approximately 2:37:23, primary PAT slide evidence, and current canonical repository state.

This is a **new review**, not a replacement for earlier historical gap reviews. Earlier reviews should remain in the repository to preserve how understanding changed over time.

## Executive finding

The dominant blocker has changed.

Before this transcript, PA/PAT was still close to a definition-discovery problem. After the primary transcript, it is better described as a **geometry-finalization and state-boundary problem**.

What is now source-backed:

- PA can occur on all TF; SIG terminology/qualification is H1+.
- Five visual forms are PAT1 + PAT2 + PAT3 variants 1/2/3.
- PAT refers to candle count.
- PAT2 = two candles and does not require full engulfing.
- PAT2 candle #2 closes around 50% of candle #1, but the denominator/tolerance is still unresolved.
- PAT3 = three candles; overlapping PAT parsing is allowed.
- PAT1→post-SIG candle2, PAT2→candle3, PAT3→candle4.
- If the counting candle lacks a wick, Buy uses low / Sell uses high as fallback anchor.
- A post-SIG reference that disturbs/exceeds the PA invalidates the old setup and can force Sideway/re-evaluation.
- The transcript contains an explicit invalid PAT2/post-SIG followed by a new valid PAT2/post-SIG sequence.
- `เบรก` in this lesson means brake/stop at frame, not generic breakout.
- Larger-TF location context is part of PA qualification.

Canonical readiness after rescoring: workflow ~82%, deterministic coding ~71%.

---

## P0 — blockers that still prevent an exact non-guessing detector

### 1. PAT3 variant 1/2/3 exact OHLC geometry

Status: **BLOCKING**.

We know the topology and candle count, but still need exact equations for each variant:

- body-size relationships;
- required/optional colors versus preferred colors;
- open/close ordering;
- whether candle #3 must close above/below a prior body midpoint, prior open/close, or high/low;
- wick requirements;
- middle-candle definition for variant 1;
- exact invalidation.

This is now the largest PAT-specific coding gap.

### 2. PAT2 50% denominator and tolerance

Status: **BLOCKING**.

Primary transcript says candle #2 should close around 50% of candle #1 and that Fibonacci may be used to check it. It does **not** settle whether the 50% line is measured over:

- candle #1 high-low range;
- candle #1 real body;
- another chart-specific construction.

Need explicit equality/tolerance rule too: exact touch, >=50%, close in a band, or visually approximate.

Until resolved, a feature such as `close_near_prior_50pct` must remain parameterized/unknown-denominator.

### 3. PAT1 quantitative rejection geometry

Status: **BLOCKING**.

The transcript/slide support one-candle rejection/hammer-like topology and location rule, but no exact:

- wick/body ratio;
- minimum directional wick length;
- maximum opposite wick;
- body-position threshold;
- support/resistance touch tolerance.

### 4. Exact `M5 เบรก` = brake/stop detector

Status: **BLOCKING**.

The primary lesson creates a semantic correction: `เบรก` cannot be assumed to mean breakout. We still need the dedicated M5 lesson to determine:

- what price behavior counts as stopping/braking;
- M1 vs M5 role;
- frame edge used;
- whether wick, body, close or sequence matters;
- overshoot tolerance;
- when `เบรก` becomes `เจิด`;
- entry timing after brake confirmation.

Any old `close beyond frame` formula remains quarantined.

### 5. Exact `ยืนกรอบ` predicate

Status: **BLOCKING**.

The transcript repeatedly uses `ยืนกรอบ` and shows it as important for wrong-location PA and entry decisions, but explicitly says the detailed reading is taught later.

Need:

- body above/on line?
- minimum body percentage beyond line?
- close-only or open+close?
- wick penetration allowed?
- number of closed candles?
- tolerance by timeframe?

### 6. Sideway frame construction/completion

Status: **BLOCKING**.

Now known:

- post-SIG destruction can lead to Sideway;
- invalid post-SIG disturbing PA can turn the interpretation into Sideway;
- `ซิกชนซิ` occurs inside Sideway;
- Sideway has no fixed duration;
- frame high/low can be traded while waiting for a SIG to leave.

Still unknown:

- how upper/lower frame boundaries are created;
- when the frame becomes complete;
- minimum number of interactions/candles;
- false-brake / false-exit handling;
- deterministic `เจิด` versus genuine Sideway exit.

### 7. Labeled historical dataset

Status: **BLOCKING FOR VALIDATION**.

The explicit five-candle invalid→replace example is a major improvement, but one teaching case is not enough to learn thresholds safely.

Minimum next dataset target:

- 20–50 labeled positive and negative examples across PAT1/PAT2/PAT3 variants;
- include correct location and wrong-location examples;
- include valid post-SIG, disturbed post-SIG, destroyed post-SIG, and replacement setups;
- record TF, timestamp, OHLC, frame relation, label, invalidation reason and outcome.

---

## P1 — important but separable from first PAT detector prototype

### 8. `คู่` exact geometry and body-collection completion

We know body collection uses `ซอก / ไส้ / คู่`, historical reference candles, and one-use zone lifecycle. Exact `คู่` OHLC construction and `body_collection_completed()` remain unresolved.

### 9. Swing-retrace start candle and extreme finalization

Half/swing concept is strong enough for a candidate classifier, but exact swing start selection and when the run extreme is final are still missing.

### 10. Half/Swing entry and Fibonacci operational levels

50% remains the strongest source-backed reference. `61.8` is now directly mentioned as a possible watched zone, but this introductory lesson does not make it mandatory.

Need the dedicated retracement lesson for:

- entry after retrace;
- invalidation;
- whether 61.8 is contextual or formal in specific setups;
- extension/exit rules.

### 11. Daily 0/5 snapping algorithm

Need exact tie/rounding behavior, especially when price is equidistant from two valid 0/5 levels and how the reference interacts with session opening.

### 12. ATH 19:00 boundary semantics

Need exact timezone and boundary inclusion/exclusion for the 19:00–19:00 window.

### 13. Full multi-timeframe conflict matrix

Now clearer:

- PA every TF;
- SIG H1+;
- H4 is the main planning context in this course;
- H1 relationship is used with H4;
- higher TF location context is stronger.

Still need deterministic rules for H1 vs H4, H4 vs D, D vs W, and what M15/M30 `same direction` means.

---

## Critical corrections to old project assumptions

1. **Do not use PAT1–PAT5 as five numbered families.** Current strongest evidence is PAT1 + PAT2 + three PAT3 variants.
2. **Do not code PAT2 as `body2 >= 50% body1`.** Source wording is candle #2 **close around 50% of candle #1**; denominator still open.
3. **Do not require PAT2 full engulfing.** Teacher explicitly says it is not necessary.
4. **Do not force PAT labels to be mutually exclusive.** The teacher allows overlapping PAT2/PAT3 grouping.
5. **Do not equate `เบรก` with breakout.** In this lesson it means brake/stop at a frame.
6. **Do not promote 200 or 300 points into universal thresholds** merely because they appear in examples.
7. **Do not treat 61.8 as mandatory.** It is now directly mentioned, but only as a context-dependent watched level in this lesson.
8. **Do not classify a correct candle shape as valid PA without location context.** Wrong-location PA is a first-class failure mode.

---

## Recommended detector architecture now

The PAT engine should be split into feature extraction, qualification and state evolution rather than one monolithic boolean.

```pseudo
features = extract_candle_features(window)

candidates = detect_topology_candidates(features)
# may return PAT2 and PAT3 simultaneously

for candidate in candidates:
    candidate.closed = all_required_candles_closed(candidate)
    candidate.location = classify_location(candidate, frames)
    candidate.geometry_status = evaluate_known_geometry(candidate)
    candidate.geometry_unknowns = list_unresolved_geometry(candidate)

    if candidate.closed and candidate.location.is_valid and candidate.geometry_status != REJECTED:
        candidate.status = CANDIDATE_ONLY

on post_sig_reference(candidate):
    if reference_disturbs_pa(candidate):
        invalidate(candidate)
        transition_to(REEVALUATE_OR_SIDEWAY)
    else:
        activate_sig(candidate)

if new_PA_after_invalidation:
    replace_anchor_and_signal()
```

This architecture lets replay/backtest proceed with evidence tags while preventing unresolved geometry from silently becoming hard-coded truth.

---

## Highest-value next source order

1. Dedicated **M5 เบรก** lesson — closes the biggest semantic/execution gap.
2. Detailed **candle-reading / ยืนกรอบ** lesson — likely closes location and frame-standing geometry.
3. Source/chart segment that enlarges **PAT3 variants** and shows exact body/wick relations.
4. Dedicated **พักครึ่ง / พักสวิง / Fibonacci** lesson.
5. Dedicated **Sideway frame** construction/completion examples.
6. Multi-timeframe lesson for the full authority/conflict matrix.

For every video/source capture:

`video_id | timestamp | exact teacher wording | chart object | TF | direction | candidate PAT | frame relation | confirmation | invalidation | OHLC candidate rule | positive/negative | confidence`.

---

## Analyst conclusion

The project can now safely move from a purely conceptual PAT module to **candidate detector + replay instrumentation**, but not to a final exact detector. The main remaining work is small in number but high in importance: PAT3 exact geometry, PAT2 50% denominator, PAT1 numeric rejection geometry, M5 brake, `ยืนกรอบ`, Sideway boundaries, and enough labeled examples to test all of those rules.
