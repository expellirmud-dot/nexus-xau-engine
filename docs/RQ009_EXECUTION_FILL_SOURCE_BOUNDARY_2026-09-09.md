# RQ-009 — Execution Fill Source Boundary

Status: `SOURCE_SIGNAL_TIMING_CLOSED / EXACT_BROKER_FILL_SOURCE_INCOMPLETE_CURRENT_BATCH`

Date: 2026-09-09 Asia/Bangkok

## Question

Does the current source batch define one exact broker-fill rule after a source-backed entry signal, or does it only define family-specific signal/knowledge timing plus structural entry context?

The required distinction is:

```text
SOURCE SIGNAL EVENT / KNOWLEDGE TIME
vs
BROKER EXECUTION FILL PRICE
```

No historical P&L or outcome performance is used to choose a fill convention.

## Sources reviewed

Primary current-batch sources:

- `1E_PYPor1qQ` — PA/PAT lesson and two SIG entry modes.
- `UV5NijhjfJ8` — EP.4 M5 brake / Entry #2.
- `16KoS7d-koI` — EP.6 M1/M5 entry detail.
- `oCcG3dUjrgw` — EP.5 Body Collection.
- `vcdN51_OrPE` — system summary.

Prior checkpoints cross-checked:

- `docs/RQ009_SIG_ENTRY_SOURCE_VISUAL_CHECKPOINT_2026-09-09.md`
- `docs/RQ009_M5_RETEST_ENTRY_SOURCE_VISUAL_CLOSURE_2026-09-09.md`
- `docs/RQ007_ENTRY_SL_INVALIDATION_SOURCE_CLOSURE_2026-09-08.md`

Targeted transcript scan artifact remains local/gitignored:

- `youtube/_evidence/rq009_execution_fill_scan_2026-09-09.txt`

## Source-backed family-specific timing

### 1. SIG Entry Mode 1 — intrabar/forming-candle entry family

`1E_PYPor1qQ` around `53:09-58:15` explicitly teaches:

```text
PA closes/confirms
-> next candle begins / prospective post-SIG candle is still forming
-> price returns to collect body
-> enter during that body-collection move
```

The source repeatedly says the entry is taken while candle #3 is becoming the post-SIG candle and before its post-SIG wick is confirmed.

Therefore Mode 1 is **not** a closed-candle-only fill family.

Source-backed:

```text
MODE1_SIGNAL_CONTEXT = PA confirmed + forming next candle returns into Body Collection context
```

Still not source-fixed:

- one exact trigger price inside the body-collection move;
- whether the broker order is filled at first qualifying tick, a selected body level, bid/ask touch, or another precise execution convention.

### 2. SIG Entry Mode 2 — post-SIG confirmed, then following-candle entry family

`1E_PYPor1qQ` around `58:15-1:06:40` explicitly teaches:

```text
PA confirmed
-> post-SIG candle closes/confirms
-> its wick becomes point-check
-> use the following candle for entry when price returns/collects body in the point-check context
```

Direct wording includes `เข้าแท่งที่ 4` / enter candle #4 and `เข้าแท่งต่อจาก...จุดเช็ค` / enter on the candle after the point-check candle.

Source-backed:

```text
MODE2_EARLIEST_ENTRY_CANDLE = candle after confirmed post-SIG / point-check candle
```

Still not source-fixed:

- exact entry tick inside candle #4;
- exact body-collection price within the allowed structural area;
- a universal formula such as confirmation close, next open, or N points from point-check.

### 3. M5 Frame-Brake Entry #2 — signal known after closed confirmation

EP.4 directly identifies Point #2 as entry and Point #1 as the structural SL reference in the standard taught form.

Around `1:08:28`, a direct question asks whether the retest point must wait for the M1 candle to finish. The instructor answers that candles should finish every time, regardless of timeframe.

Safe source event:

```text
RETURN / RETEST AT POINT2
-> relevant confirmation candle closes
-> directional PA / standing / local structure condition is confirmed
-> ENTRY_2_SIGNAL_READY
```

This closes **signal knowledge time**, not exact broker fill.

The source also uses wording such as `ค่อยพิจารณาเข้าออเดอร์`, `เข้าจุดที่ 2`, and `เข้าชิดกรอบ`, but does not define one universal equation saying the actual fill must equal:

- the confirmation close;
- the following open;
- exact Point #2 price;
- first touch after confirmation;
- a fixed point offset.

### 4. EP.5 Body Collection lower-TF confirmation

EP.5 teaches zone-first execution:

```text
forecast zone reached
-> lower-TF PA/brake confirmation
-> break/confirmation at the planned frame
-> consider / progressively enter
```

The source explicitly rejects zone presence alone as enough for entry and uses wording such as `พิจารณาเข้าออเดอร์` and `ค่อยๆทยอยเข้าออเดอร์`.

This supplies structural execution context but not one exact broker-fill price.

## Contextual examples are not universal fill rules

The current sources contain concrete live/worked prices and phrases such as:

- entry around a shown level such as `4005`;
- `เข้า 58 SL 59` in a specific M1 example;
- entry near `4205` in a specific retest example;
- entry around `3340-3341` near a point-check in a specific context;
- `เข้าชิดกรอบ` / enter close to the frame;
- trendline-touch entry in a separate M1 refinement context.

These demonstrate how the instructor executed or described particular charts. They do **not** establish one universal broker-fill equation for SIG Entry, Body Collection, and Frame-Brake Entry families.

Do not promote these example prices or point distances into a canonical source fill rule.

## Structural tolerance remains separate

The source uses relational structural language such as:

- equal / stand at the same level as Point #1;
- not below relevant support for BUY;
- not above / not through relevant resistance for SELL;
- touch a trendline in an M1-specific refinement;
- enter close to a frame.

The current batch does not state a universal broker-tick tolerance for `equal`, `same level`, `close to frame`, support hold, or resistance hold.

Therefore:

```text
STRUCTURAL RELATION = source-backed semantics
EXACT NUMERIC / TICK TOLERANCE = source-incomplete / implementation convention
```

## Closed source boundary

### Source-backed

```text
SIG MODE 1:
  PA must be confirmed first.
  Entry family can act during the forming next/post-SIG candle while it body-collects.

SIG MODE 2:
  Post-SIG / point-check candle must confirm first.
  Earliest taught entry candle is the following candle.

M5 ENTRY #2:
  Point #2 is the retest entry family.
  Relevant confirmation must be a completed candle before the signal is treated as ready.

BODY COLLECTION LOWER-TF:
  zone alone is insufficient;
  lower-TF PA/brake/structure confirmation is required in the shown workflow.
```

### Not source-fixed in the current batch

```text
one universal exact broker fill price
confirmation-close fill
next-open fill
first qualifying tick fill
fixed N-point offset fill
universal structural equality/touch tolerance
```

## Replay implication

A replay engine must keep two fields separate:

```text
signal_known_at        # source-backed where closed
execution_fill_model   # explicit research/implementation convention unless separately sourced
```

For closed-candle signal families, using a later executable convention such as next-bar open may be tested as an explicitly labeled **Research Representation**, but it must not be described as the instructor's exact fill rule.

Mode 1 requires special care because the source allows entry during a forming candle. Bar-close-only OHLC replay cannot reproduce the literal intrabar decision without an explicit intrabar trigger model or finer-grained data; silently replacing it with next-open changes the source entry family.

## Decision

```text
FAMILY-SPECIFIC SIGNAL / KNOWLEDGE TIMING: SOURCE BACKED
EXACT UNIVERSAL BROKER FILL: SOURCE INCOMPLETE IN CURRENT BATCH
UNIVERSAL STRUCTURAL POINT/TICK TOLERANCE: SOURCE INCOMPLETE IN CURRENT BATCH
```

This is a terminal source-boundary result for the current batch. Reopen exact fill only with a primary source that states execution price mechanics, direct instructor/project-owner clarification, or a source mapping correction. Do not reopen from backtest outcomes.

## Next decision-critical blocker

Proceed to broker/feed price normalization required for already source-backed equality/contact relations (`ซอก`, `คู่`, post-SIG point-check contact, same-level retest). Keep broker normalization as an implementation layer separate from instructor semantics.
