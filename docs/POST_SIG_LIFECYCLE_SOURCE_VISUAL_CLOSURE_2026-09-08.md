# RQ-001 — Post-SIG Lifecycle Source + Visual Closure — 2026-09-08

Status: CLOSED / `SOURCE_SUPPORTS_OTHER_EXPLICIT_LIFECYCLE`

## Question

After a current post-SIG reference / inherited origin is destroyed, does the teaching system:

1. fully reset all inherited state;
2. automatically fall back to an older surviving same-direction origin; or
3. use another lifecycle model?

## Closure

The available first-party teaching material supports **another explicit lifecycle model**: lifecycle is attached to individual SIG/reference instances, not to one global inherited-origin slot.

Safe source-backed interpretation:

```text
SIG/reference instance
-> ACTIVE while its reference survives and its run objective is still open
-> DESTROYED / STOPPED / NOT_COUNTED when its post-SIG reference is destroyed
-> other independent still-valid SIG/reference instances are not automatically erased
-> newly confirmed PA/SIG may create a new active instance
-> a completed run objective closes that instance from further measurement even if its reference itself was not destroyed
```

The source does **not** establish a universal rule that, when the newest same-timeframe origin is destroyed, the engine must automatically reactivate the next-oldest surviving origin by chronological order.

Therefore the previous research representation `newest -> older surviving fallback` remains a research representation, not canonical teaching semantics.

## Primary transcript evidence

### vcdN51_OrPE — system summary

`00:57:57–00:58:20`

- teacher describes stopping the Sell-side operation;
- if the referenced candle is the post-SIG wick and it is destroyed, `ซิกชุดนี้ไม่นับ`;
- the explanation then moves to another PA/SIG set rather than keeping the destroyed set active.

`00:59:50–01:00:07`

- student summarizes `ไส้หลังซิกแล้วไม่นับ...คือเปลี่ยนฝั่ง`;
- teacher confirms that when it is destroyed and opposite PA collides with it, `ซิกชุดนั้นหยุดการทำงาน`;
- teacher then says `พอซิกชุดนั้นหยุดการทำงานเราก็จะมาหาซิกชุดที่มันเพิ่งเกิดล่าสุด`.

This is direct lifecycle wording: the destroyed SIG instance stops; the next analysis looks for the newly/latest formed valid SIG, not continuation of the destroyed instance.

`01:04:14–01:04:33`

- a PA/SIG can have its post-SIG wick destroyed;
- subsequent movement may then be explained by Frame conditions;
- the source says a final/new SIG becomes the actual driver of the next travel.

`01:28:37–01:30:03`

- a wick destroys the PA/SIG relation;
- `ซิกชุดนี้ไม่ได้ทำงาน`;
- movement that still occurs is attributed to Frame conditions rather than the destroyed SIG.

### 1E_PYPor1qQ — PA / post-SIG lesson

`00:59:39–00:59:56`

- when the post-SIG wick is not touched/destroyed, `ไส้นี้มันก็ยังทำงาน` and its run can continue to be counted.

`01:01:29–01:02:16`

- if the post-SIG check is destroyed but Frame still holds, price may still move from the Frame;
- teacher says to wait for a newly confirmed SIG;
- `ซิกตัวแรกเนี้ยถ้ามันทำลายไส้ก็...ไม่นับแล้ว`.

`01:19:56–01:22:09`

This passage is important because it rules out a simplistic global reset.

- teacher says one Buy-side check set has been destroyed;
- immediately says `แต่อย่าลืมว่าเค้ายังมีไส้นี้อยู่นะครับ`;
- that remaining wick has run 1,500 points but not the 3,000 extension and may still complete the H4 3,000-point round, depending on H1 confirmation;
- the following explanation explicitly distinguishes the current H1 frame from the still-open H4 round.

Safe conclusion: destruction of one check/SIG instance does not imply that every other independently valid reference in the current multi-timeframe state is erased.

This passage does **not** prove automatic same-timeframe chronological fallback to an older origin.

`02:01:54–02:02:17`

- a prior Week Buy reference had already run 15,000;
- a new Buy confirmation is not yet present because a relevant reference has just been destroyed;
- teacher waits for a new PAT/SIG confirmation.

Again the operational response is re-evaluation/new confirmation, not reuse of the destroyed SIG.

### ESHDuiVPJow — Trend -> Frame -> SIG

`00:22:43–00:23:00`

- `ซิกค้ำซิก` is described as two or more overlapping SIGs;
- a run can complete 100%, then a new SIG forms and carries continuation.

`02:23:04–02:23:28`

- after TP1, the earlier post-SIG wick is explicitly said to remain undestroyed;
- another PA Sell set then forms with its own post-SIG wick.

This demonstrates that the teaching model can contain more than one sequential/overlapping SIG instance rather than one global singleton reference.

`02:42:28–02:42:51`

Q&A directly separates **reference survival** from **run completion**:

- question asks whether a SIG that reached TP2 and retraced without touching its post-SIG wick is still relevant;
- answer says the SIG is still working, but if TP2/full round is complete then `จบแล้ว` and it is no longer measured;
- if the round is not complete, it can still be measured.

Therefore destruction and objective completion are distinct lifecycle terminal conditions.

## Visual cross-check

### vcdN51_OrPE — `00:58:11`

Local evidence bundle:

`youtube/_evidence/vcdN51_OrPE/00-58-11/`

Observed visual facts:

- whiteboard contains multiple circled red/green candle clusters connected as a cycle;
- during the destruction explanation, a blue X is drawn over the referenced central-right candle/cluster by approximately `00:58:14`;
- the visual context is a multi-stage cycle, not a single permanent signal slot.

### vcdN51_OrPE — `00:59:57`

Local evidence bundle:

`youtube/_evidence/vcdN51_OrPE/00-59-57/`

Observed visual facts:

- full whiteboard shows multiple SIG/PA/cycle stages and directional arrows;
- this is the visual context for the teacher's explanation that a destroyed SIG stops working and analysis moves to the latest newly formed SIG.

### 1E_PYPor1qQ — `01:20:04`

Local evidence bundle:

`youtube/_evidence/1E_PYPor1qQ/01-20-04/`

Observed visual facts:

- live TradingView chart shows multiple marked zones/boxes and projected levels;
- transcript in the same window explicitly discusses one destroyed Buy check alongside a still-open 1,500 -> 3,000 H4 reference and H1 confirmation.

The visual does not by itself prove chronological age ordering; that remains intentionally unresolved.

### ESHDuiVPJow — `02:42:28`

Local evidence bundle:

`youtube/_evidence/ESHDuiVPJow/02-42-28/`

Observed visual facts:

- teaching slide visibly contains several circled `Sig Buy` / `Sig Sell` instances along one broader structure;
- the slide title discusses `SIG ค้ำ SIG` / SIG interaction;
- this supports the transcript's multi-instance lifecycle framing.

## Direct fact vs interpretation

### Direct source facts

- A destroyed post-SIG reference makes that SIG stop working / not count in the demonstrated lifecycle.
- A post-SIG reference that is not destroyed can remain active and continue to support remaining-run measurement.
- A newly formed valid PA/SIG can become the current/latest signal used for subsequent travel.
- Multiple SIG instances may exist sequentially/overlap (`ซิกค้ำซิก`).
- One check can be destroyed while another independently valid reference remains relevant in multi-timeframe context.
- Full TP/run completion can end further measurement even when the post-SIG wick was not destroyed.

### Supported interpretation

The defensible engine abstraction is an **active set of identified SIG instances**, each with its own:

```text
signal_id
source_tf
pattern/source window
post_sig_reference
reference_state = ACTIVE | DESTROYED
run_state = OPEN | COMPLETE
known_at / invalidated_at / completed_at
```

A global `one active origin` variable is too lossy for the source material.

### Still unresolved

- exact numeric/geometry predicate for destruction;
- equality/tolerance behavior;
- whether an older same-timeframe, same-direction SIG automatically becomes preferred after a newer one is destroyed;
- exact priority rule when multiple simultaneously open SIGs on the same timeframe/direction coexist;
- full Sideway state construction and its interaction with SIG eligibility;
- exact selection rule across conflicting timeframes.

## Impact on the previous source-partial re-anchor

The frozen re-anchor used:

```text
newest same-direction H1 PAT2-BODY origin
-> if destroyed, search older surviving origins
```

The source review now changes its interpretation:

- destruction-aware rejection remains directionally consistent with teaching semantics;
- however `search older surviving origins newest -> oldest` is **not source-confirmed as a universal fallback algorithm**;
- the 8 events labeled `REANCHORED_TO_OLDER_VALID_ORIGIN` in the 2022/23 research run cannot be upgraded to canonical lifecycle examples solely from that algorithm;
- the prior closure remains `INCONCLUSIVE_AFTER_SOURCE_PARTIAL_REANCHOR`; it is not reversed into SUPPORT or OPPOSE by this source review.

Future remaining-run research should track explicit SIG identities / active-set state rather than assuming one inherited origin with unconditional LIFO fallback.

## Computation decision

No new broad historical computation is required to answer RQ-001's semantic question.

The primary sources directly establish enough lifecycle structure to close the question as `SOURCE_SUPPORTS_OTHER_EXPLICIT_LIFECYCLE`.

Computation will be useful later for implementation validation and population effects after the active-set representation is source-constrained, but outcome performance must not determine lifecycle semantics.

## Canonical consequence

The canonical claim register should distinguish:

1. local invalidation of the destroyed SIG instance;
2. survival of other independent valid SIG/reference instances;
3. new/latest confirmed SIG creation after re-evaluation;
4. run completion as a separate terminal condition;
5. unresolved same-timeframe older-origin priority.

## Queue consequence

RQ-001 is closed.

The next highest-value unblocked worksheet is RQ-002: exact PAT2/PAT3 geometry and the 50% measurement basis, because reliable PA geometry is upstream of a canonical SIG detector and will also improve future active-set reconstruction.
