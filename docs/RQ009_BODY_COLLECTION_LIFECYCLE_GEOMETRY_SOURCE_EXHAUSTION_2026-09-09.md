# RQ-009 — Body Collection Lifecycle Geometry Source Exhaustion

Status: `CURRENT_BATCH_SOURCE_INCOMPLETE / SEMANTIC_LIFECYCLE_CLOSED`

Date: 2026-09-09 Asia/Bangkok

## Question

Can the current reviewed source batch define an exact machine event for:

```text
TOUCHED / REVALIDATED
-> COLLECTED / USED
-> RETIRED / REPLAN
```

without inventing a touch count, age limit, penetration threshold, candle-close rule, or outcome-fitted tolerance?

## Sources reviewed

Primary Body Collection source:

- `oCcG3dUjrgw` — EP.5 Body Collection original YouTube rendered transcript and prior synchronized visuals.

Cross-check sources in the current bounded batch:

- `UV5NijhjfJ8` — EP.4 M5 brake.
- `16KoS7d-koI` — EP.6 M1/M5 entry.
- `vcdN51_OrPE` — system summary.

Local scan artifact remains gitignored:

- `youtube/_evidence/rq009_lifecycle_scan_2026-09-09.txt`

No market outcomes were used to choose a lifecycle rule.

## Direct source facts already closed

### Completed/used is terminal for that zone instance

EP.5 around `1:13:16-1:13:41` says that after Body Collection has been completed/used, the historical line/zone is no longer used again and the trader changes/updates the view.

Safe semantic:

```text
COLLECTED_USED -> RETIRED_REPLAN
```

### Mere touch is not terminal

EP.5 around `2:01:22-2:02:03` directly answers whether a touched `ซอก/ไส้/คู่` reference can continue to be used. The answer is conditional on whether it continues to act as support/resistance. The source also says to consider how many times the zone has been touched and that an unused zone can react well on first arrival.

Safe semantic:

```text
TOUCH != automatic retirement
```

No universal numeric maximum touch count is stated.

### Zone arrival still requires confirmation for execution

EP.5 repeatedly requires PA / lower-timeframe confirmation at the forecast zone. EP.6 around `1:28:47-1:28:55` discusses two Body Collection zones being reached while almost no PA Sell appears, reinforcing that zone arrival alone is not an executable Body Collection entry condition.

This supports:

```text
ZONE_CONTACT / ZONE_ARRIVAL != automatic executable use
```

It does not define the lifecycle transition into `COLLECTED_USED`.

## Targeted current-batch scan result

A targeted transcript scan was run across EP.5, EP.4, EP.6, and the system-summary source for language around:

- Body Collection completion/use;
- touch/contact;
- reuse / no-reuse;
- support/resistance continuation;
- completed/finished collection;
- new/replanned zone context.

The scan found repeated semantic guidance but no source statement that uniquely specifies any of the following as the universal `TOUCHED -> COLLECTED_USED` event:

- first wick touch;
- body entry into the zone;
- candle close inside or through the zone;
- reaching forecast reference 1;
- reaching forecast reference 2;
- traversing the full interval between references;
- lower-TF PA confirmation;
- order entry;
- target completion;
- a fixed number of contacts.

Likewise, the current batch does not define one exact OHLC predicate for post-touch support/resistance revalidation.

## Important non-inferences

Do **not** convert the following into canonical lifecycle rules:

- `first touch -> used`;
- `touch both forecast lines -> used`;
- `close beyond midpoint -> used`;
- `PA confirmation -> zone retired`;
- `one successful trade -> zone retired`;
- `N touches -> invalid`;
- `one day / 2-4 candles -> expired`.

Those mappings are not established by the reviewed source batch.

## Current source-faithful lifecycle representation

```text
FRESH_UNUSED
    |
    | price interaction
    v
TOUCHED_REVALIDATE_S_R
    |\
    | \ source context still treats it as S/R
    |  -> ACTIVE_TOUCH_HISTORY
    |
    | exact transition UNKNOWN in current batch
    v
COLLECTED_USED
    |
    v
RETIRED_REPLAN
```

The state labels remain valid research bookkeeping for the source semantics, but the transition into `COLLECTED_USED` must not be automated from an analyst-selected OHLC predicate.

## Decision

```text
SEMANTIC LIFECYCLE: SOURCE BACKED
EXACT TOUCHED -> COLLECTED_USED OHLC GEOMETRY: SOURCE INCOMPLETE IN CURRENT BATCH
EXACT POST-TOUCH S/R REVALIDATION OHLC GEOMETRY: SOURCE INCOMPLETE IN CURRENT BATCH
```

This is a terminal result for the current source batch unless a reopen trigger appears.

## Reopen only if

- a new primary instructor source explicitly demonstrates or states the completion event;
- a clearer synchronized visual/audio example distinguishes touch from completed collection;
- direct instructor/project-owner clarification defines the transition;
- a source/timestamp mapping error is discovered.

Historical outcomes are not a reopen trigger and cannot select the missing transition.

## Research consequence

Do not spend additional cycles re-scanning the same current source windows for this exact question. Preserve lifecycle state manually/research-only where needed and move RQ-009 to the next decision-critical blocker: exact lower-timeframe execution/fill and structural tolerance after a source-backed confirmation event.
