# PA / PAT / SIG Transcript Forensics — Primary Lesson

Date reviewed: 2026-09-01
Source class: Smart Trader To Success / Mae Pla Green Pen system, full searchable transcript supplied by project owner.
Transcript coverage inspected: approximately 0:00 through 2:37:23. No later timestamped transcript chunk was found in the supplied source during the final search pass.

Evidence class: **PRIMARY TRANSCRIPT + TIMESTAMP**.

This file supersedes weaker generic-pattern assumptions when they conflict with the timestamped lesson. It does not replace the primary visual slide evidence in `PAT_PRIMARY_VISUAL_EVIDENCE_2026-09-01.md`; the two sources should be used together.

## Evidence policy

- `FACT-TRANSCRIPT` = directly stated in the supplied timestamp transcript.
- `SUPPORTED-INTERPRETATION` = close reading of transcript plus primary slide, but still needs chart/OHLC alignment.
- `UNKNOWN` = not deterministic enough to encode without guessing.
- `QUARANTINE` = older project statement contradicted or weakened by this primary source.

---

## 1. System vocabulary and lifecycle

### FACT-TRANSCRIPT — system core

- ~17:29–18:52: the system is organized around `รอบ / กรอบ / SIG / วงจรชีวิตกราฟ`; `SIG` is based on the five PA visual forms.
- ~18:28: `กรอบ` is described as meaningful support/resistance ending in 0 or 5 in this introductory lesson.
- ~18:37–19:06: a run is measured from the post-SIG wick/reference; the next candle retraces to collect body and the post-SIG point becomes the start of the run count.
- ~29:26–31:24: broad cycle sequence is `SIG -> TP -> พักตัว -> Sideway`, while the ordering of rest and sideway can vary in practice.

### FACT-TRANSCRIPT — PA versus SIG

- ~27:13–28:32, ~1:30:48–1:32:53, ~1:52:10–1:52:42, ~2:34:53–2:35:20: **PA can occur on every timeframe**, while the term **SIG is used from H1 upward** in this teaching framework.
- The teacher repeatedly describes SIG contextually as PA plus its post-SIG wick/reference.

Engineering consequence:

```text
PA_candidate(tf = any)
SIG_candidate(tf >= H1) := valid_PA + valid_post_sig_reference
```

This is a terminology/qualification rule, not yet a complete executable detector.

---

## 2. PA family map — now directly supported

### FACT-TRANSCRIPT

- ~53:05–54:02: PA Buy is presented as five visual forms organized as:
  - PAT1
  - PAT2
  - PAT3 variant 1
  - PAT3 variant 2
  - PAT3 variant 3
- ~22:13: `PAT` refers to the **number of candles**.
- ~56:14: PAT2 is explicitly a two-candle pattern.
- ~39:12–46:46: PAT3 example is explicitly a three-candle PA set.
- ~2:34:53: final recap again says PA has five forms and occurs on every timeframe.

### QUARANTINE

Do **not** model the system as five separately numbered families `PAT1..PAT5` unless a stronger primary source later shows that nomenclature. Current primary slide + transcript support **PAT1 + PAT2 + three PAT3 variants**.

---

## 3. PAT1 — direct facts and remaining geometry

### FACT-TRANSCRIPT

- ~54:02 onward: PAT1 is the one-candle rejection/hammer-like form shown in the teaching slide.
- ~55:20–56:14: for Buy, the candle can be red or green; green is preferred as the stronger/cleaner directional expression, but red is not automatically invalid.
- Location is mandatory context: a Buy-form PAT1 belongs at support; the same shape at resistance can become a wrong-location PA.
- Sell is taught as the directional mirror at resistance.

### UNKNOWN

- exact minimum wick/body ratio;
- exact allowed body size;
- whether support must be touched by wick, body, close, or merely be within a tolerance;
- quantitative distinction between a preferred same-color PAT1 and a weaker opposite-color PAT1.

Therefore `detect_PAT1_exact()` remains unresolved even though topology and location semantics are substantially clearer.

---

## 4. PAT2 — 50% rule corrected by primary transcript

### FACT-TRANSCRIPT

- ~56:14–57:17: PAT2 is **two candles**.
- It **does not need to be a full engulfing pattern**.
- Buy example can be red candle followed by green candle.
- The teacher says candle #2 must be able to **close around 50% of candle #1**; this may be judged visually or measured with Fibonacci.
- ~57:09–57:35: candles 1+2 can already be PAT2; when candle #3 develops the pattern can evolve/overlap into PAT3.

### QUARANTINE

Older project shorthand `body2 >= 50% of body1` is not what the primary transcript actually states. The source says **candle #2 close around the 50% level of candle #1**.

### UNKNOWN

The transcript alone does not settle whether the 50% denominator is:

- full high-low range of candle #1,
- real body of candle #1,
- or a visual/Fibonacci construction shown on the chart.

Do not encode a denominator until transcript wording is aligned with the chart frame.

---

## 5. PAT3 and overlapping labels

### FACT-TRANSCRIPT

- PAT3 uses three candles and has three visual variants in the primary slide.
- ~1:10:39: teacher explicitly describes PAT3 as the strongest but slowest/wait-longest form.
- ~1:24:56–1:25:12: the same three-candle region can support overlapping parsing: the whole 1-2-3 set may be PAT3 while candles 2+3 may also form PAT2.
- ~2:29:38–2:30:03: the teacher again treats PAT grouping as potentially overlapping rather than mutually exclusive.

Engineering consequence:

```text
pattern labels must be many-to-many over candle windows;
never force one exclusive PAT label per candle region.
```

### UNKNOWN

The primary visual slide supplies color/order topology for the three PAT3 variants, but this transcript does not give enough exact OHLC ratios for:

- middle-candle size/tolerance;
- wick relation;
- close threshold;
- monotonic body-size requirements;
- exact per-variant invalidation.

---

## 6. Post-SIG reference index — CLOSED at source level

### FACT-TRANSCRIPT

~59:40–1:01:06:

- PAT1 -> count candle #2 as the post-SIG reference;
- PAT2 -> candle #3;
- PAT3 -> candle #4.

This matches the primary training slide.

### FACT-TRANSCRIPT — no-wick fallback

~1:04:06–1:04:25:

- if the counting/reference candle has no wick, use the extreme/body edge;
- Buy uses the **lowest price**;
- Sell uses the **highest price**.

Engineering candidate:

```pseudo
post_sig_index = {PAT1: 2, PAT2: 3, PAT3: 4}

if reference_has_directional_wick:
    anchor = wick_extreme
else:
    anchor = low if BUY else high
```

The exact definition of `reference_has_directional_wick` still needs an OHLC-side convention, but the fallback is source-backed.

---

## 7. Post-SIG validity and destruction

### FACT-TRANSCRIPT

- ~21:56: a SIG remains active while its post-SIG wick/reference has not been destroyed.
- ~1:12:29 onward: if the post-SIG wick extends farther than / beyond the PA, it is not a valid post-SIG wick; a good PA should not be disturbed (`กวน`) by the post-SIG wick.
- ~1:14:40: the post-SIG wick should not exceed the PA and should not exceed the relevant frame; otherwise sideway may be forming.
- ~2:01:42–2:02:14: candle #4 wick lower than candle #3 is shown as complete post-SIG-wick destruction; in the illustrated case ~200 points difference already counted as destroyed.
- ~2:29:21: when the post-SIG wick is destroyed, wait for a new candle/new setup because the market may be in sideway.

### Important caution

The ~200-point example is **example-specific evidence of destruction**, not proof that `200 points` is a universal destruction threshold.

---

## 8. Explicit positive / negative ground-truth sequence

### FACT-TRANSCRIPT — ~1:56:55–2:03:16

At support, the teacher walks through a five-candle sequence:

1. candle #1 may look like PAT1 but is not confirmed;
2. candles #1 + #2 become PA Buy PAT2;
3. candle #3 is initially the post-SIG reference, **but it extends beyond/disturbs the PA, therefore the signal is invalid**;
4. the five-candle region is treated as sideway and the upward movement is explained as `ขึ้นด้วยกรอบ`, not as the original SIG run;
5. candles #3 + #4 then form a **new PA Buy PAT2**;
6. candle #5 is the valid new post-SIG wick/reference and does not disturb the new PA.

This is the strongest labeled positive/negative sequence currently available in transcript form.

Engineering consequence: the replay engine needs **pattern replacement / re-anchoring**, not merely a binary signal flag.

Possible state model:

```text
CANDIDATE_PA -> CANDIDATE_SIG -> INVALIDATED_BY_POST_SIG
                                  -> SIDEWAY / REEVALUATE
                                  -> NEW_PA -> NEW_SIG
```

---

## 9. Location is part of PA qualification

### FACT-TRANSCRIPT

- ~1:20:40–1:26:31: PA Buy must stand on support; a visually similar Buy form at resistance is wrong-location (`หัวโหม่งต้าน`) and can reverse.
- ~1:26:31–1:28:28: higher-timeframe support/resistance can override what a small-timeframe shape appears to say.
- ~1:35 onward: Sell is mirrored — Sell PA belongs at resistance; Sell form at support is wrong-location.
- ~2:34:13–2:34:30: the phenomenon occurs on every timeframe, and larger timeframe context is stronger.

Teacher heuristic: roughly `90%` reversal / `10%` continuation is mentioned in this explanation. Treat this as **INSTRUCTOR HEURISTIC**, not project backtest statistics.

Engineering consequence:

```text
shape_match alone != valid_PA
valid_PA = shape_match + valid_location_context + closed_candle
```

Exact support/resistance tolerance remains unresolved.

---

## 10. Candle close and confirmation windows

### FACT-TRANSCRIPT

- ~1:02:44–1:03:07: wait for the candle of the working timeframe to close before confirmation.
- ~1:07:36–1:08:47: an unfinished green candle can end as a long-wick / indecision candle, therefore intrabar classification is unsafe.
- ~1:05:45–1:07:11: H1 may require observing roughly 2–4 candles; H4 and above roughly 1–3 candles while PA character develops PAT1 -> PAT2 -> PAT3.

These 2–4 / 1–3 ranges are **observation/confirmation windows**, not PAT candle counts.

---

## 11. `เบรก` semantic correction — critical

### FACT-TRANSCRIPT

~23:30–24:04:

The system's word `เบรก` in this introductory context means **stop / pause / brake at a statistical frame**, not generic English `breakout`.

- frame is associated with 0/5 levels;
- price may overshoot a frame by roughly up to ~300 points in the teaching explanation;
- M1/M5 are used to judge whether price **stops/brakes**;
- if price keeps going rather than braking, the teacher calls that behavior `เจิด`.

### QUARANTINE

Older generic rules such as:

```text
M5 break = close beyond frame + N-point penetration
```

must not be treated as system rules solely from the word `เบรก`.

The dedicated M5-break lesson is still required to define the exact `brake/stop` geometry.

---

## 12. Sideway mechanics materially improved

### FACT-TRANSCRIPT

- ~19:13–20:10: post-SIG destruction is often associated with a sideway cycle.
- `ซิกชนซิ` describes SIGs occurring inside sideway; there is no normal full run space inside that frame.
- During sideway, the teacher describes playing frame high/low until a new SIG exits the frame.
- ~48:17–48:47: rest can occur as intra-candle wick removal or an opposite-color candle, followed by sideway construction.
- ~1:12:29 onward and ~1:56:55–2:03:16: an invalid post-SIG wick that disturbs the PA can transition the interpretation to sideway.
- ~2:13:55: rest/sideway duration is not fixed; it depends on the graph.

### UNKNOWN

Still missing for deterministic state detection:

- exact sideway frame upper/lower construction;
- frame completion event;
- false-break / `เจิด` classification;
- whether a minimum candle count exists;
- exact rule for a SIG leaving sideway.

---

## 13. Run / TP facts

### FACT-TRANSCRIPT

- ~33:07 onward: the post-SIG point is the start of the run.
- H1 = 1,000 points.
- H4 = 1,500 points for the first/full round and may extend toward 3,000.
- The direct training slide remains the cleaner source for OCR-sensitive higher-TF ranges: Day 5,000–10,000; Week 15,000–30,000; Month 30,000–50,000.
- ~36:37 onward: from H4 upward the second extension is described as `ตึงรอบ` / TP2; H1 has a single run.
- ~1:11:01: the post-SIG candle itself can complete the whole run in one candle.
- ~2:29:29 onward: PAT3 TP is the same as PAT2 on the same timeframe; TP depends on timeframe/run, not PAT family.

---

## 14. Retracement / Fibonacci facts from this lesson

### FACT-TRANSCRIPT

- ~2:21:27–2:24:31: Fibonacci is purpose-dependent; the teacher often prefers support/resistance zones in the live example.
- `61.8` is directly mentioned as a possible watched zone.
- For an ambush-style entry (`จอบหลอย`), teacher says wait for `เบรก` and confirmation first.
- Fibonacci can be used on any timeframe; for a larger-timeframe trade, H4 Fibonacci should be drawn on H4.
- Before drawing Fibonacci, define the purpose: entry, exit, or countertrade.

### QUARANTINE / clarification

`61.8` is now directly evidenced as a level the teacher may watch, so it should no longer be labeled completely unsupported. It is **not** established here as a mandatory universal entry level.

The dedicated half-retrace / swing-retrace lesson remains the authority for exact anchor and entry rules.

---

## 15. Multi-timeframe facts from this lesson

### FACT-TRANSCRIPT

- H4 is repeatedly emphasized as the main practical planning timeframe.
- ~1:16:01–1:18:19: H4 setups are read with H1 relationship; H1 same-direction behavior is an important confirmation context.
- ~1:05:07 onward: larger timeframe controls context; smaller timeframe can be used for the actionable round/entry.
- ~2:34:13–2:34:30: larger timeframe PA/support-resistance context is stronger.

### UNKNOWN

Still no full deterministic conflict matrix for:

- H1 Buy vs H4 Sell;
- H4 vs D;
- D vs W;
- exact M15/M30 same-direction predicate;
- when lower-TF opposite PA is normal retrace versus thesis invalidation.

---

## 16. Example M5 entry — evidence, not universal rule

### FACT-TRANSCRIPT — ~1:46:06–1:46:30

Teacher's live example:

- wait for M5 to retrace;
- body sizes become roughly comparable (`เนื้อเทียนเท่าๆกัน`);
- ignore a fake protruding wick;
- mark the support/black line;
- if M5 comes back and **stands on that black line**, enter;
- SL is placed beyond the red wick in that example.

This is useful labeled entry evidence, but it is not enough to declare one universal M5-entry equation.

---

## 17. New engineering status after this transcript

### Safe to encode as source-backed metadata/state rules

- PA may be detected on any TF; SIG qualification is H1+.
- PAT family data model = `PAT1`, `PAT2`, `PAT3.variant={1,2,3}`.
- PAT = candle count concept.
- PAT2 has two candles and does not require full engulfing.
- PAT2 candle #2 close is evaluated around the 50% level of candle #1, with denominator still unresolved.
- post-SIG index PAT1=2, PAT2=3, PAT3=4.
- no-wick anchor fallback: Buy low / Sell high.
- overlapping PAT labels are allowed.
- closed-candle requirement.
- wrong-location PA rejection/context flag.
- post-SIG invalidation when it disturbs/exceeds the PA, at topology/state level.
- replacement/re-anchoring after invalidated signal.
- PAT type does not change TF run distance.
- `break` semantic tag must distinguish system `BRAKE/STOP` from generic breakout.

### Still candidate-only

- exact PAT1 OHLC detector;
- exact PAT2 50% denominator and equality/tolerance;
- exact PAT3 variant geometry;
- support/resistance touch tolerance;
- exact post-SIG `กวน PA` numeric predicate;
- exact sideway frame construction;
- exact M5 brake/stop detector;
- full MTF conflict resolution.

---

## 18. P0 evidence requests after analyst pass

1. **PAT3 variant geometry** — chart-aligned OHLC for all three forms, positive and negative examples.
2. **PAT2 50% denominator** — confirm whether 50% is prior candle range or body and define tolerance (`>=`, `~`, close location).
3. **PAT1 numeric wick/body qualification** and valid support/resistance touch rule.
4. **Dedicated M5 `เบรก` lesson** — exact stop/brake predicate; explicitly separate from breakout semantics.
5. **Sideway construction/completion** — frame boundaries, completion, `เจิด`, and false-break behavior.
6. **`ยืนกรอบ` candle-reading lesson** — exact body/wick/close condition.
7. **Enough labeled historical positives + negatives** to validate detector thresholds rather than learning only from schematic examples.

P1 remains: `คู่` exact geometry / body-collection completion, swing-retrace start/extreme finalization, Daily 0/5 snapping, ATH 19:00 boundary semantics, and full multi-timeframe conflict matrix.

---

## Analyst conclusion

This transcript materially changes the project. The PA/PAT blocker is no longer a blank definition problem; it is now a **geometry-finalization problem**. The family map, candle counts, PAT2 non-engulf requirement, approximate 50% close concept, post-SIG reference indexes, location qualification, overlapping-label behavior, and a real invalid/replace sequence are all source-backed.

The most important semantic correction is that the system term `เบรก` cannot be assumed to mean English `breakout`. Until the dedicated M5 lesson is processed, the engine should represent this as a separate `BRAKE_AT_FRAME` concept and quarantine old `close_beyond_frame` formulas.
