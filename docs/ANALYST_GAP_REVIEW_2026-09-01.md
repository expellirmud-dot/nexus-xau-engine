# NEXUS XAU Engine — Analyst Gap Review after full transcript pass

Date: 2026-09-01
Scope: full available transcript in project file `Markdown ที่วาง (1).md`, approximately 0:00–2:01:22, plus existing repository evidence. This document separates transcript-supported rules from unresolved items. It does **not** promote external trading heuristics into system rules.

## Evidence discipline

- `FACT-TRANSCRIPT`: stated directly in the available class transcript with timestamp.
- `SUPPORTED-INFERENCE`: derived directly from several transcript statements but still needs chart visual verification for exact OHLC geometry.
- `UNKNOWN`: not deterministically specified by available transcript.
- `CONFLICT`: existing project summary conflicts with transcript evidence or lacks timestamp-level support.

---

## 1. What the transcript closes

### 1.1 Candle-close requirement — CLOSED

**FACT-TRANSCRIPT**
- ~17:21–18:43: whichever timeframe is used, wait for that timeframe candle to finish. The teacher explicitly warns against assuming how a candle will finish while time remains.

Implementation candidate:
```pseudo
if not candle.is_closed:
    do_not_confirm_signal()
```

Confidence: HIGH.

### 1.2 Candle components and rejection — PARTIALLY CLOSED

**FACT-TRANSCRIPT**
- ~11:40–17:14: body represents open/close structure; wick reflects intra-candle rejection; body strength decreases as body shrinks and wicks become more significant; tiny centered body may indicate indecision/sideway.

**UNKNOWN**
- No deterministic numeric thresholds are given for wick/body ratios except illustrative percentages in teaching examples. Do not hard-code 80%, 60%, etc. as PAT rules yet.

### 1.3 `ซอก / ไส้ / คู่` — CONCEPT CLOSED, GEOMETRY PARTIAL

**FACT-TRANSCRIPT**
- ~19:41–25:33: three keys for body-collection analysis are `ซอก`, `ไส้`, and `คู่`.
- `ซอก`: junction/corner between close and open price where the two prices meet.
- `ไส้`: candle wick/rejection.
- Together with `คู่`, these are used to construct support/resistance zones.
- ~25:01–25:24: applies on all timeframes, but the user must know the intended purpose.

**UNKNOWN**
- Exact OHLC rule for `คู่` still needs visual-chart alignment.
- Width/tolerance around a `ซอก` price is not numerically specified.

### 1.4 Body-collection workflow — MOSTLY CLOSED

**FACT-TRANSCRIPT**
- ~39:16: first wait for PA on H4 for the H4 body-collection workflow.
- ~39:25–39:35: SIG is described as PA plus wick (`SIG = PA + ไส้`) in the teacher's wording/context.
- ~39:35 onward: body collection can be used to anticipate/create the post-SIG wick rather than waiting until all of it has already formed.
- ~42:52–43:16: explicit workflow recap:
  1. wait for PA on H4,
  2. construct projected zone using `ซอก-ไส้-คู่`, looking roughly 2–4 historical candles back,
  3. if not found on H4 / same TF, drill down one TF (H4→H1),
  4. when price reaches the projected area, wait for PA on M1/M5 in the same direction as the large/H4 signal; after frame break, consider order entry.
- ~44:26–45:27: one H4 candle contains four H1 candles; effect can appear on H1 candle 2, 3, or 4, so entry does not have to occur on the first H1 candle.

Implementation candidate (still chart-dependent):
```pseudo
on H4_close:
    if PA_H4:
        zone = find_sok_wick_pair(history=2..4 bars, tf=H4)
        if zone is None:
            zone = find_sok_wick_pair(tf=H1)

when price_enters(zone):
    wait until M1_or_M5 candle closes
    if PA_small_tf aligned with H4 direction and frame_break_confirmed:
        entry_candidate = True
```

Confidence: HIGH for workflow order; MEDIUM for exact geometry because the chart is required.

### 1.5 Sideway handling inside body collection — PARTIALLY CLOSED

**FACT-TRANSCRIPT**
- ~42:35–44:19: if there is no break, or PA moves beyond the intended frame/zone, teacher says to suspect sideway; body collection is not used in sideway in this setup.

**UNKNOWN**
- No precise OHLC definition for `sideway` is given here.
- Exact meaning of “PA เลยกรอบ” needs chart examples/tolerance.

### 1.6 Zone lifecycle — CLOSED at concept level

**FACT-TRANSCRIPT**
- ~1:13:16–1:13:47: after a body-collection zone has been used/collected, it is not reused and the perspective changes.

Implementation candidate:
```pseudo
zone.state = ACTIVE
if body_collection_completed(zone):
    zone.state = CONSUMED
    do_not_reuse(zone)
```

Confidence: HIGH for one-use lifecycle; MEDIUM for exact event that marks `body_collection_completed`.

### 1.7 Multi-timeframe interaction — PARTIALLY CLOSED

**FACT-TRANSCRIPT**
- H4 is the main context for this class.
- If H4 does not provide a usable `ซอก-ไส้-คู่`, drill one TF down to H1.
- Small TF M1/M5 supplies PA/entry confirmation in the H4 direction.
- ~1:16:57 onward: example logic shows H4 PA Sell may be temporarily opposed by an H1 PA pushing upward during a retrace/body-collection process.

**SUPPORTED-INFERENCE**
- Lower-TF opposite movement can be a retracement mechanism rather than an automatic invalidation of the H4 idea.

**UNKNOWN**
- Complete H1 vs H4 conflict matrix remains unresolved.
- D/W hierarchy is not resolved by this transcript.

### 1.8 Training/backtest requirement — CLOSED

**FACT-TRANSCRIPT**
- ~1:57:34–1:57:58: teacher explicitly says not to simply believe the rule; backtest it, observe behavior when price enters the zone, and record results.

This directly supports the NXRE research-engine design: transcript rule → detector candidate → replay/backtest → evidence table.

---

## 2. Major remaining gaps after analyst review

Priority is ranked by whether the gap blocks deterministic code/backtest.

### P0 — PAT1 / PAT2 / PAT3 / PAT4 / PAT5 definitions

Status: **BLOCKING / UNKNOWN**.

The full available transcript does not supply deterministic PAT1–PAT5 OHLC definitions. Existing project summaries that describe PAT1 as a single-bar pattern, PAT2 as 2 bars, or PAT3 as 3 bars are not sufficiently supported by this transcript and must remain unverified.

Now known from project owner: video `1E_PYPor1qQ` maps to `P1/PAT1`. We still need that video's timestamp transcript.

Required fields per PAT:
- candle count;
- required colors;
- open/close ordering;
- body overlap threshold;
- wick conditions;
- close-break vs wick-break;
- permitted distance from frame/zone;
- post-pattern confirmation;
- invalidation/cancellation;
- Buy/Sell mirror exceptions.

### P0 — exact PA definition

Status: **BLOCKING / UNKNOWN**.

Transcript repeatedly uses `PA Buy`, `PA Sell`, and H4 PA as prerequisites, but this class assumes the student already knows PA. There is no complete deterministic PA detector specification in this transcript.

Need: dedicated PA/PAT lesson transcript and chart examples.

### P0 — `คู่` exact OHLC construction

Status: **BLOCKING for zone detector / UNKNOWN**.

`ซอก` and `ไส้` are verbally described, but `คู่` needs chart/visual extraction: which two bodies, whether same/opposite color, what exact price(s) form the pair, and tolerance.

### P0 — frame-break confirmation

Status: **BLOCKING / PARTIAL**.

Transcript says wait for PA M1/M5 in same direction and then “เกิดการเบรกที่กรอบราคาที่วางไว้แล้ว” before considering entry.

Unknown:
- must candle close outside the frame?
- is wick penetration sufficient?
- exact frame price used (edge, body, wick, zone boundary)?
- minimum penetration/buffer?
- do we require retest after break?

### P0 — PAT1 transcript for `1E_PYPor1qQ`

Status: **SOURCE MISSING**.

The current environment/project has the video ID but not the timestamp transcript for this video. It must be obtained before PAT1 can be coded.

### P1 — Half-retrace / swing-retrace / Fibonacci

Status: **DEDICATED LESSON REQUIRED**.

The available transcript explicitly announces the next class at ~1:58:08–1:58:49 as `พักครึ่ง / พักสวิง / Fibonacci / retracement / extension`, including the meaning of Fibonacci levels. Therefore any detailed formulas currently in summaries should not be treated as final until that class transcript is extracted.

Still required:
- anchor selection;
- extreme termination;
- difference between half-retrace and swing-retrace;
- which Fib levels are system rules vs illustrative;
- entry after retracement;
- invalidation;
- TP/extension usage.

### P1 — SIG lifecycle / “post-SIG wick” selection

Status: **PARTIAL**.

This transcript supports `SIG = PA + wick` conceptually and says body collection anticipates the post-SIG wick. It does **not** yet specify deterministic PAT-specific wick index (e.g. candle 2/3/4), wick size threshold, or what happens with multiple candidate wicks.

### P1 — zone construction tolerance

Status: **UNKNOWN**.

Need:
- exact zone upper/lower bounds;
- whether zone uses wick tips, body edges, open/close junction, or combination;
- price tolerance by TF;
- how overlapping `ซอก/ไส้/คู่` are merged;
- how to rank multiple zones found in 2–4 historical bars.

### P1 — zone completion / consumed event

Status: **PARTIAL**.

We know a used body-collection zone is not reused. We still need an exact machine event for `CONSUMED`: first touch? body fill? close through? M1/M5 break? full zone traversal?

### P1 — sideway deterministic detector

Status: **UNKNOWN**.

Transcript says do not use body collection in sideway, but does not define sideway algorithmically. Need teacher examples or dedicated lesson.

### P1 — order execution, SL, TP

Status: **PARTIAL/UNKNOWN**.

The transcript gives “consider entry after PA small-TF alignment + frame break”, but exact execution and risk rules remain incomplete:
- market vs pending vs retest entry;
- SL anchor;
- SL buffer;
- TP frame/round distance/extension;
- scale-out/breakeven rules;
- invalidation before entry.

A source from the chat labels `UV5NijhjfJ8` as the order-entry lesson; this is high priority.

### P2 — complete timeframe authority matrix

Status: **UNKNOWN**.

Need explicit rules for:
- H1 Buy vs H4 Sell;
- D vs W conflict;
- M15/M30 “same direction” definition;
- when lower-TF counter-PA is retracement vs thesis break.

### P2 — “ช่องแม่ปลา” and “เพาะ”

Status: **UNKNOWN / TERMINOLOGY SOURCE NEEDED**.

No direct timestamp evidence in the available transcript. Do not map these terms to generic frame concepts or to PA without direct evidence.

---

## 3. Conflicts / project statements to quarantine until verified

The following types of existing claims must not be promoted to production rules without timestamp evidence:

1. PAT1 = single-bar hammer/shooting-star style detector.
2. PAT2 = exactly 2 bars with a fixed 50% body rule.
3. PAT3 = exactly 3 bars move-consolidate-confirm.
4. D/W always outranks H4/H1 by a generic higher-TF principle.
5. Fixed 500/1000/1500/3000-point values as universal hard-coded rules.
6. Fixed wick-after-SIG size such as 200–300 points.
7. Fixed pivot confirmation of two bars.
8. Fibonacci 38.2/61.8 as official system entry rules.

These may later prove correct, but the current transcript does not establish them.

---

## 4. Next transcript extraction order

1. `1E_PYPor1qQ` — P1/PAT1 (owner-confirmed mapping).
2. `UV5NijhjfJ8` — order entry / M5 break (chat-labeled).
3. the lesson immediately after the full body-collection transcript — half-retrace / swing-retrace / Fibonacci.
4. `vcdN51_OrPE` — all-system summary, used as a map only; dedicated lessons override it.
5. `ESHDuiVPJow` — trend/frame/SIG.
6. `jBEM-vWYj_o` — support/resistance/frame construction.

For each source capture:
`video_id | timestamp | teacher wording | chart object | TF | direction | condition | invalidation | exact OHLC candidate | confidence | unresolved visual dependency`.

---

## 5. Analyst conclusion

The body-collection portion is now sufficiently defined to prototype a **state-machine skeleton**, but not yet a production detector. The principal blocker is no longer general system architecture. It is **precise source extraction for PA/PAT definitions and visual geometry**.

Current implementable skeleton:

```pseudo
STATE WAIT_H4_PA
  -> when closed H4 has verified PA: FIND_REFERENCE_ZONE

STATE FIND_REFERENCE_ZONE
  -> search prior 2..4 bars for sok/wick/pair structure on H4
  -> if absent: drill down one TF to H1
  -> once zone selected: WAIT_ZONE_TOUCH

STATE WAIT_ZONE_TOUCH
  -> if context becomes sideway: CANCEL_BODY_COLLECTION
  -> if price enters projected zone: WAIT_SMALL_TF_PA

STATE WAIT_SMALL_TF_PA
  -> require closed M1/M5 PA aligned with H4 direction
  -> require frame-break confirmation
  -> then: ENTRY_CANDIDATE

STATE ZONE_ACTIVE
  -> after body collection is completed: mark zone CONSUMED and never reuse
```

However, `verified PA`, `sok/wick/pair exact geometry`, `frame-break confirmation`, `body_collection_completed`, and entry/SL/TP remain unresolved functions. These should be implemented only as interfaces/placeholders until the dedicated transcripts close them.
