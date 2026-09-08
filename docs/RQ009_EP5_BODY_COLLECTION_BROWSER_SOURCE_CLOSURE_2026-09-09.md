# RQ-009 — EP.5 Body Collection Browser-Source Closure

Status: `SOURCE_BACKED_SEMANTIC_CLOSURE / VISUAL_GEOMETRY_STILL_OPEN`

Date: 2026-09-09 Asia/Bangkok

## Source

Primary source reviewed in this checkpoint:

- YouTube Video ID: `oCcG3dUjrgw`
- Lesson: `EP.5 วิชาเก็บบอดี้ #SmatTrderToSuccess #ระบบแม่ปลาปากกาเขียว`
- Access path: local `agent-browser` CLI -> YouTube rendered page -> `Show transcript`
- Transcript provenance: YouTube auto-caption / ASR shown by the original video page, with timestamps
- Local MP4 status: not present in the current local visual batch

Local ignored evidence created during review:

- `youtube/_evidence/oCcG3dUjrgw/agent-browser/ep5_rendered_transcript_utf8.txt`
- `youtube/_evidence/oCcG3dUjrgw/agent-browser/target_windows_utf8.json`

These local evidence files are intentionally under the gitignored `youtube/` vault and are not Git artifacts.

## Method

The source was reviewed source-first through five pre-mapped windows:

1. `20:33-32:40` — definitions of `ซอก + ไส้ + คู่` and zone construction
2. `40:42-44:19` — same-TF routing, fallback TF, lower-TF PA/brake confirmation, Sideway guard
3. `46:40-51:27` — two projected zones, actual example, SL context, zone-not-price semantics
4. `56:35-59:43` — M5 entry/brake example after H4 zone arrival
5. `1:19:13-1:20:01` — fallback H4 -> H1 -> M30, no-PA no-entry, Sideway distinction

No outcome/backtest result was used to choose source meaning in this checkpoint.

## Source-backed closure

### 1. Body Collection is a zone-construction method, not a single exact entry price

The lesson repeatedly describes `ซอก + ไส้ + คู่` as a zone/reference structure. At approximately `31:36-32:40`, the source says that H4 Body Collection requires the three elements in the zone and that `ซอกไส้คู่` becomes a zone.

At approximately `50:49-51:18`, the source explicitly explains that price may react at projected zone 1, projected zone 2, or between them, and that the zone is a forecast/reference area rather than a fixed/dead price.

Safe semantic closure:

```text
BODY_COLLECTION_OUTPUT = ZONE / FORECAST AREA
NOT = one deterministic price level
```

This materially narrows the previous blocker: a source-faithful implementation must represent an area/range plus later confirmation, not invent one exact entry price from the projection alone.

### 2. `ซอก` is a price joint between candles

Around `20:33-22:43`, the source defines `ซอก` as the joint/corner between candles and describes the prior close / next open as the same price in the shown same-color-candle relation. The source says this joint can later act as support or resistance when market side/context changes.

Safe closure:

- `ซอก` is a source-defined candle-price joint/reference;
- close/open continuity is material to its definition;
- it can serve as support/resistance context.

Still open:

- exact machine OHLC predicate for every allowed color/orientation case;
- equality/tick-normalization convention across broker feeds.

### 3. `ไส้` means candle wick and is only final after the candle closes

Around `23:49-25:24`, the source defines `ไส้` as the candle wick and explains that wick extent is not known until the relevant candle has finished. For H4 use, wait for the H4 candle to close; the method can conceptually be applied on other timeframes when used for the corresponding timeframe purpose.

Safe closure:

- wick geometry belongs to the completed source candle;
- no look-ahead partial-candle wick should be frozen as final H4 evidence.

### 4. `คู่` is a body/open-close equilibrium relation at support/resistance

Around `26:47-30:08`, the source defines `คู่` as a paired-candle relation, teaches support-side and resistance-side forms, repeatedly refers to candle bodies, and calls the paired open/close relation an equilibrium price (`ราคาดุลยภาพ`). The lesson also says the alternating-color candle relation is used at support/resistance.

Safe closure:

- `คู่` is body-sensitive;
- an open/close equilibrium relationship is source-material;
- it is interpreted in support/resistance context;
- it is not justified to substitute generic full-range overlap.

Still open:

- exact OHLC equation for all valid pair orientations;
- how much body overlap/offset is allowed in every illustrated case;
- feed equality normalization.

Because the instructor is drawing these relations on-chart, exact machine geometry still requires visual closure before promotion to a production predicate.

### 5. Same-timeframe first; only then fall back one timeframe

Around `40:58-41:51`, the source says the projection should use `ซอกไส้คู่` in the same timeframe first. For H4, search H4 first; if the structure is not found, move down one timeframe for supporting reference.

The later Q&A around `1:19:13-1:19:29` makes the fallback chain more explicit:

```text
H4 incomplete -> inspect H1
H1 incomplete -> inspect M30
```

This is source-backed routing, not analyst-selected MTF optimization.

### 6. Initial historical search is approximately 2-4 candles, then continue if absent

Around `43:06-43:16`, the source says to look back approximately `2-4` prior candles for `ซอกไส้คู่`.

Around `1:19:29`, the source clarifies that if it is not found, continue searching farther back.

Safe closure:

- `2-4` is an initial source search window, not a hard expiry of older valid structure;
- absence in the first search window does not authorize fabrication of a substitute level.

### 7. The lesson uses two projected Body Collection zones

Around `40:42-40:58` and again `46:40-47:58`, the lesson contrasts the current two-distance representation with an older three-part/head-middle-tail approach. The source explains that the older approach produced unnecessary SL exposure and explicitly presents `ซอกไส้คู่` as the more selective alternative.

Around `49:44-50:20`, the worked example builds a first forecast zone from a visible `ซอก`, `ไส้`, and `คู่`, then identifies forecast zone 1 and forecast zone 2.

Safe closure:

```text
CURRENT_LESSON_BODY_COLLECTION = two projected zones / forecast areas
```

Do not reinterpret this as two exact single prices.

### 8. Zone arrival alone is not an entry

This is one of the strongest repeated source statements in the lesson.

Around `42:17-42:35`:

- price reaches the planned area;
- lower-timeframe PA on M1/M5 should form in the same direction as the H4 thesis;
- a brake/break/confirmation at the planned frame/area is then considered before entry.

Around `51:27`, the source says that when price enters the zone, PA must be waited for.

Around `1:19:37-1:19:44`, the source again states that even if price is in the zone, if PA has not formed, do not enter.

Safe state machine:

```text
H4 PA
-> construct H4 Body Collection zone(s)
   (fallback one TF only if source structure is absent)
-> price arrives at forecast zone
-> require lower-TF PA aligned with H4
-> require the source brake/confirmation context
-> only then consider entry
```

The exact executable price inside the confirmed lower-TF structure remains open.

### 9. M1 can be used earlier; M5 is the more conservative confirmation in the shown example

Around `58:31-58:54`, the source says M1 and M5 can use the same general logic; a more experienced trader may act from M1, while a more cautious trader can wait for M5 confirmation. In the shown example, once M5 PA Sell forms at the planned area, entry can be considered.

This is source evidence for confirmation routing, not a claim that M1 or M5 is universally superior.

### 10. Body Collection is not used as the normal Body Collection entry inside Sideway

Around `42:35-44:19`, if price runs through the planned area without the expected brake/PA behavior, the lesson says Sideway may be forming and explicitly says not to use Body Collection in Sideway.

Later around `1:19:44-1:20:01`, the source says a separate Sideway-entry treatment may exist, but the trader must first determine whether the observed PA/SIG is genuinely valid in that Sideway context.

Safe closure:

```text
NORMAL_BODY_COLLECTION_ENTRY != SIDEWAY_ENTRY_METHOD
```

Do not merge the two families in replay/accounting.

## Source-stated numeric guidance: preserve, but do not universalize

The source contains several numeric ranges. They are preserved because they are genuine lesson evidence, but they are not automatically promoted to universal production constants.

### Zone-width guidance in this lesson

Around `32:04-32:33` the transcript states approximately:

- H1: `300-500` project points
- H4: `500-1,000` project points
- Day: `1,000-1,500` or `2,000` project points
- width depends on timeframe

These are source-stated teaching ranges in EP.5. Before hard-coding them as universal boundaries, visual/audio cross-check and cross-lesson consistency are still required.

### Worked-example values

The worked examples additionally contain context-specific values, including:

- approximately `300` points between two projected areas in one example (`50:20`);
- M5 brake/forecast separation around `100-200` points in one example (`57:00`);
- SL around `300` points from the shown frame in one example (`57:38`);
- TP around `1,000-1,500` points and an RR discussion in that example (`57:47-57:58`).

These remain `EXAMPLE_METADATA_ONLY` unless a separate source closure establishes universality.

## Important change from the previous project state

Before this checkpoint, the project treated Body Collection as a major unknown that might require computation to infer where an entry price should be.

After direct EP.5 review, the source itself closes the higher-level architecture:

```text
Body Collection is a forecast zone method.
The zone comes from ซอก + ไส้ + คู่.
Same-TF structure is preferred; fall back one TF when absent.
The current lesson uses two projected zones.
Price arriving at the zone is not sufficient.
Lower-TF PA aligned with H4 + brake/confirmation is required before entry consideration.
No PA -> no entry even inside the zone.
Normal Body Collection is not the Sideway entry method.
```

Therefore broad computation should NOT be used to invent the above semantics.

## What is still unknown / visually blocked

The source transcript is sufficient to close the state/routing semantics, but it is not sufficient to freeze every OHLC predicate because the instructor is drawing the geometry on screen.

Still unresolved:

1. exact OHLC predicate for every valid `ซอก` orientation;
2. exact OHLC predicate for every valid `คู่` orientation;
3. exact upper/lower boundary construction of each Body Collection zone from `ซอก + ไส้ + คู่`;
4. exact rule for choosing/prioritizing multiple valid historical candidate zones;
5. exact lower-TF brake executable price / body-wick-close predicate;
6. equality/tick-normalization across feeds;
7. whether the source-stated TF width ranges are hard limits, typical ranges, or teaching heuristics across all lessons.

These should be closed by actual EP.5 visual frames/audio before any outcome-driven threshold search.

## Browser evidence limitation

`agent-browser` successfully opened the original YouTube page and exposed the full rendered `Show transcript` content. However, the headless YouTube player returned a playback error and did not provide reliable timestamped visual frames. Therefore:

- transcript/timestamp evidence from this checkpoint is usable with ASR risk;
- browser screenshots are NOT promoted as EP.5 chart visual evidence;
- exact visual geometry remains pending the actual playable video/visual source.

## Research consequence

RQ-009 remains ACTIVE, but the Body Collection blocker is materially narrower.

The current proof boundary is now:

```text
SOURCE-BACKED STATE MACHINE: substantially closed
EXACT VISUAL OHLC/ZONE GEOMETRY: still open
FINAL DETERMINISTIC EXECUTION PRICE: still open
```

Do not run/report a canonical Win/Loss result until the remaining visual geometry and execution predicate are frozen without outcome fitting.
