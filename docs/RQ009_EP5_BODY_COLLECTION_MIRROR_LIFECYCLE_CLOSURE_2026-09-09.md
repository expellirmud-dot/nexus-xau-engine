# RQ-009 — EP.5 Body Collection BUY/SELL Mirror + Zone Lifecycle Closure

Status: `SOURCE+VISUAL_LIFECYCLE_CLOSURE / EXACT TOUCH-COUNT AND COMPLETION GEOMETRY OPEN`

Date: 2026-09-09 Asia/Bangkok

## Source

Primary source:

- YouTube Video ID: `oCcG3dUjrgw`
- Lesson: `EP.5 วิชาเก็บบอดี้ #SmatTrderToSuccess #ระบบแม่ปลาปากกาเขียว`
- Original YouTube video reviewed through the validated headed NEXUS Chrome CDP path (`9223`)
- YouTube `Show transcript` / auto-caption ASR retained with normal ASR risk

Local ignored visual evidence:

- `youtube/_evidence/oCcG3dUjrgw/visual_ep5/mirror_lifecycle/`

The media evidence remains under the gitignored local source vault and is not committed to Git.

## Evidence guard

This checkpoint does not use Win/Loss outcomes to infer lifecycle rules. The closure comes from direct instructor wording plus synchronized source visuals.

Where the instructor gives qualitative guidance such as “ดูว่ามาสัมผัสกี่รอบ”, this document preserves it as qualitative state information and does not invent a numeric touch threshold.

---

## 1. Two Body Collection forecast levels are not SELL-only

### BUY example — source + visual

Around `1:12:15-1:12:52`, the instructor identifies the setup as `PA Buy PAT3` and says to place two Body Collection forecast points/levels.

Direct source sequence:

- `1:12:15`: identifies the example as PA Buy / PAT3;
- `1:12:35`: says the first Body Collection point is here and another point is here;
- `1:12:45`: explicitly refers to forecast distances/levels `1` and `2`.

The synchronized source visual shows the BUY cluster boxed on chart with two horizontal lines explicitly numbered `1` and `2`.

### SELL example — source + visual

Immediately after, around `1:12:52-1:13:16`, the instructor switches to a `PA Sell PAT2` example and again marks two forecast points/levels.

The visual shows the same two-level concept on the opposite direction.

### Safe closure

```text
EP5_TWO_FORECAST_LEVEL_CONCEPT = applies to both demonstrated BUY and SELL examples
```

This closes directional availability of the two-level concept.

It does **not** prove that every BUY and SELL variant uses identical candle indexing or identical `ซอก/ไส้/คู่` assembly.

---

## 2. `2-4` historical candles is an initial search window, not a zone expiry rule

Earlier in the lesson (`43:06-43:16`), the instructor says to inspect approximately `2-4` candles in the past for the historical reference.

Later Q&A around `1:19:29` clarifies that if the required structure is not found, continue looking farther back.

Safe closure:

```text
2-4 candles = initial search guidance
NOT = hard maximum age
NOT = automatic expiry after 4 candles
```

No source-backed fixed candle-age expiry is established.

---

## 3. A Body Collection zone can remain relevant across multiple days

At approximately `2:01:55-2:02:03`, a direct question asks whether the zone is only for one day.

The instructor states that it can be used for multiple days and says the trader must inspect how many times it has been touched. She then states that a zone that has never been used can work especially well when price first reaches it.

Safe closure:

- zone lifetime is not capped at one trading day;
- a fresh/unused zone can persist into later days;
- freshness/touch history matters to the source interpretation;
- no universal numeric maximum age or maximum touch count is stated.

Therefore a date change alone must not automatically retire an otherwise valid Body Collection zone.

---

## 4. Touch alone does not automatically equal retirement

At approximately `2:01:22-2:01:40`, the source addresses whether a `ซอก/ไส้/คู่` zone that has been touched can continue to be used.

The answer is conditional: the trader must see whether that structure will continue to become/act as support or resistance in the future.

Safe closure:

```text
TOUCH != automatic retirement
```

A touched zone may remain relevant if its support/resistance role remains valid in the source context.

Still open:

- exact OHLC predicate for “still acts as support/resistance” after touch;
- exact number of touches that weakens or retires the zone;
- exact distinction between a shallow touch, PA-confirmed reaction, partial collection and completed collection.

Do not convert the qualitative “ดูว่ามาสัมผัสกี่รอบ” statement into a fitted numeric threshold.

---

## 5. Completed / used Body Collection is explicitly retired

This is one of the strongest lifecycle statements in EP.5.

Around `1:13:16-1:13:41`, the instructor directly answers that:

- a projection line can be used historically;
- **after body collection has completed, it cannot be used again**;
- once the graph has used/completed the Body Collection structure, the trader should no longer reuse it and should change/update the perspective.

Repeated wording occurs at approximately:

- `1:13:16`
- `1:13:33`
- `1:13:41`

Safe lifecycle closure:

```text
COMPLETED / USED BODY COLLECTION
-> RETIRE THAT ZONE INSTANCE
-> UPDATE / REPLAN CURRENT VIEW
```

This is stronger than the prior generic `TOUCHED/ACTIVE` placeholder.

Important distinction:

```text
mere touch != necessarily completed collection
completed/used collection => retire
```

The exact price-path event that converts a touched zone into `COLLECTED/USED` remains not fully machine-deterministic from this lesson alone.

---

## 6. Fresh zones are distinct from already-used zones

At `2:02:03`, the source says a zone that has not yet been used is especially responsive when price reaches it.

This supports storing zone freshness/history explicitly rather than treating all historical levels as interchangeable forever.

Safe source state information:

```text
FRESH / UNUSED
TOUCHED / REVALIDATION_REQUIRED
COLLECTED / USED
RETIRED
```

This state vocabulary is a research representation of the direct source semantics; exact transition geometry remains parameterized where the source is qualitative.

---

## 7. New PA / current context leads to a new plan

Around `1:14:40-1:15:04`, the instructor describes updating the current work after PA formation and, if the later H4 close still gives PA Sell, placing a new Body Collection plan for that new/current setup.

Combined with the explicit “used zone -> change perspective” statement, the safe interpretation is:

```text
new/current valid PA context
-> construct/update the relevant Body Collection plan
```

This does not establish a universal newest-zone-wins priority when several independently valid zones coexist.

---

## 8. Relationship to the prior worked-zone visual closure

Prior checkpoint:

`docs/RQ009_EP5_BODY_COLLECTION_VISUAL_GEOMETRY_CLOSURE_2026-09-09.md`

That checkpoint visually closed the shown `ซอก`/`คู่` forms and one worked PA Sell zone assembly.

This checkpoint adds:

- two forecast levels are demonstrated on both BUY and SELL;
- zone instances have explicit freshness/use history;
- zone can survive across days;
- touch is not automatically terminal;
- completed/used Body Collection is terminal for that zone instance;
- new PA/current context triggers re-planning.

Together these materially reduce the previous lifecycle ambiguity without inventing a universal zone-ranking formula.

---

## 9. Safe research state machine

The minimum source-faithful lifecycle representation is now:

```text
FRESH_UNUSED
    |
    | price interaction
    v
TOUCHED_REVALIDATE_S_R
    |\
    | \ still valid as support/resistance
    |  -> ACTIVE_TOUCH_HISTORY
    |
    | completed / used for Body Collection
    v
COLLECTED_USED
    |
    v
RETIRED_REPLAN
```

Notes:

- `FRESH_UNUSED` may survive across calendar days.
- `TOUCHED_REVALIDATE_S_R` is not an automatic rejection state.
- touch count is recorded, but no hard max-touch threshold is canonical.
- exact `COLLECTED_USED` OHLC transition is still open.
- a later/new PA may create a new Body Collection plan/zone instance.

---

## 10. What remains unresolved

1. Exact OHLC transition from `TOUCHED` to `COLLECTED_USED`.
2. Exact support/resistance revalidation geometry after touch.
3. Any universal numeric max-touch rule — none is source-backed yet.
4. Candidate priority when several fresh/active zones coexist.
5. Universal `ซอก/ไส้/คู่` assembly across all BUY/SELL pattern variants.
6. Exact broker fill/tolerance after lower-TF confirmation.
7. PAT2/PAT3 `>50%` denominator/arithmetic.
8. Sideway/cross-timeframe priority and final pristine holdout.

## Decision

`SOURCE+VISUAL LIFECYCLE CLOSURE` with parameterized completion/revalidation geometry.

RQ-009 remains ACTIVE. The Body Collection blocker is now concentrated on **candidate priority, universal assembly and exact state-transition geometry**, rather than basic zone lifetime semantics.
