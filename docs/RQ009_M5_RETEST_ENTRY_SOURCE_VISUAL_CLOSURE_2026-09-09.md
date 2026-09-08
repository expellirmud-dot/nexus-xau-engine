# RQ-009 — M5 Retest / Entry #2 Source-Visual Closure

Status: `SOURCE_VISUAL_SIGNAL_TOPOLOGY_CLOSED / EXACT_EXECUTION_PRICE_STILL_OPEN`

Date: 2026-09-09 Asia/Bangkok

## Question

Can the M1/M5 brake family be narrowed from a qualitative state machine to a source-backed **Entry #2 signal topology** without inventing an exact broker fill price?

## Primary sources

- Video ID `UV5NijhjfJ8` — EP.4 Brake M5
- Video ID `16KoS7d-koI` — EP.6 M1/M5 entry detail
- prior closure: `docs/RQ004_M5_BRAKE_FRAME_STANDING_SOURCE_CLOSURE_2026-09-08.md`

New synchronized visual windows from the actual local EP.4 MP4:

- `38:25` — teaching diagram for rising-Low/rising-High form
- `51:04` — worked BUY retest example
- `1:29:45` — overlap BUY example

Local visual evidence lives under the gitignored `youtube/_evidence/UV5NijhjfJ8/` vault.

## Source-backed findings

### 1. Entry #2 is the retest entry; Point #1 is the structural SL reference in the taught standard form

The teaching diagram at approximately `38:25` visibly labels:

```text
Point 2 -> entry point
Point 1 -> SL point
```

The drawing shows Point #1 at the first brake/structural low and Point #2 after price has moved away and returned to the switched support area.

The SELL mirror in the transcript around `41:58-42:06` teaches the same relation: enter Point #2, SL Point #1.

This closes the **relative topology** of the preferred Entry #2 family.

It does NOT establish a universal fixed point-distance SL buffer.

### 2. A true retest is structural, not merely several candles sitting on a line

EP.6 source wording and RQ-004 already established that a full retest requires price to first move through/away from structure, encounter opposing support/resistance, and then return to the switched level.

Safe topology:

```text
prepared zone
-> first brake / Point #1
-> move away through local structure
-> encounter opposing S/R
-> return to the switched level
-> retest candidate / Point #2
-> PA / standing / structure confirmation
-> ENTRY #2 signal
```

Merely standing on a line before this move-away/return sequence is not automatically the same full retest.

### 3. Worked BUY example visually matches the topology

At approximately `51:04`, the actual EP.4 teaching image shows:

- Point `1` circled at the first structural low / SL reference;
- price moves up to resistance;
- price returns to the prior support area;
- the return is explicitly labeled `2 รีเทส`;
- source transcript says the return forms PA Buy and does not go below the left-side support.

This is direct source+visual support that the preferred Entry #2 event is a **return/retest at a switched/held structural level**, not a generic second candle.

### 4. Confirmation requires a completed candle

Around `1:08:28` in EP.4, a direct question asks whether the retest point must wait for the M1 candle to finish. The instructor answers that candles should be allowed to finish every time, regardless of timeframe.

Safe execution-event semantics:

```text
RETEST_CONFIRM_SIGNAL becomes known only after the relevant confirmation candle closes.
```

This avoids look-ahead and intrabar promotion of an unfinished PA/confirmation candle.

### 5. BUY and SELL confirmation are directional mirrors at the local structural level

Source-backed examples support:

```text
BUY retest:
  return to support / switched resistance->support
  + PA Buy / valid standing
  + does not lose the relevant left-side support

SELL retest:
  return to resistance / switched support->resistance
  + PA Sell / valid standing
  + does not reclaim/exceed the relevant resistance / prior high structure
```

The source repeatedly requires the trader to check whether a move is `retest` or `crush/overwrite` rather than assuming every return is valid.

Exact numeric tolerance around the structural line remains unresolved.

### 6. Overlap is a separate branch but preserves structural-reference logic

At approximately `1:29:45`, the actual EP.4 visual shows an overlap BUY example with:

- first brake identified;
- a later overlap/structural extreme marked as the SL reference;
- PA M5 Buy used as confirmation before continuation.

The transcript also teaches waiting for price to return and stand/equal with the first brake area before considering the order, rather than entering the initial overlap blindly.

Therefore overlap must not be flattened into the standard Point1->Point2 path without an explicit branch.

### 7. The `4-10 candles` discussion is confirmation/observation evidence, not a hard fitted gate

The source repeatedly discusses M5 confirmation by observing roughly `4-10` candles / standing behavior and warns that one changed-color candle is insufficient.

This supports:

```text
one candle alone != sufficient universal brake confirmation
multi-candle standing/structure evidence matters
```

But the source reviewed here still does not establish an exact universal formula such as:

```text
must always be >=4 and <=10 candles
```

for every setup and volatility regime.

Keep `4-10` as source-stated observation/confirmation guidance until exact hard-gate semantics are separately proven.

## What is now closed

The preferred Frame-Brake Entry #2 can now be represented source-faithfully at the **signal-event level**:

```text
ZONE_ARMED
-> BRAKE_1 / POINT_1
-> MOVE_AWAY
-> OPPOSING_STRUCTURE_TEST
-> RETURN_TO_SWITCHED_LEVEL
-> RETEST_CANDIDATE / POINT_2
-> CLOSED_CANDLE_CONFIRMATION
   + directional PA / standing / local structure hold
-> ENTRY_2_SIGNAL_READY
```

For the standard taught form:

```text
SL_STRUCTURAL_REFERENCE = POINT_1 extreme
```

with separate overlap handling where the protruding overlap/head structural extreme becomes the shown SL reference.

## What is NOT closed

### Exact broker execution price

The source identifies where/when an entry is considered and gives structural points, but it does not establish one universal broker-fill equation such as:

```text
fill exactly at confirmation close
fill exactly at next open
fill exactly N points from frame
```

Therefore:

```text
ENTRY_2_SIGNAL_TIME = source-backed after closed confirmation
EXACT_FILL_PRICE = implementation/execution assumption still open
```

A replay may evaluate multiple explicit fill conventions, but must label them `Research Representation`, not instructor rules.

### Other open details

- exact point tolerance around support/resistance;
- exact quantitative force/weakening/rejection thresholds;
- exact all-vs-majority candle-standing predicate;
- exact pivot-window arithmetic;
- universal numeric SL buffer;
- context routing when Sideway / Body Collection / multiple frames overlap.

## Research consequence

The prior blocker `lower-TF brake geometry` is materially reduced:

```text
SIGNAL TOPOLOGY: SOURCE+VISUAL CLOSED
SIGNAL KNOWLEDGE TIME: CLOSED-CANDLE SOURCE-BACKED
STRUCTURAL SL REFERENCE: SOURCE+VISUAL CLOSED FOR TAUGHT STANDARD FORM
EXACT FILL PRICE / POINT TOLERANCE: STILL OPEN
```

This is sufficient to build a non-outcome-fitted **event detector / feature state machine** for Entry #2. It is not yet sufficient to claim one canonical trade P&L without declaring an execution-price convention.
