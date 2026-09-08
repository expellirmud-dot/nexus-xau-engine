# RQ-009 — EP.5 Two-Reference Method Rationale and Question Reframing

Date: 2026-09-09 Asia/Bangkok
Source: original YouTube EP.5 `oCcG3dUjrgw` rendered Show transcript
Status: `SOURCE_SEMANTIC_CLOSURE / EXACT TWO-REFERENCE SELECTION GEOMETRY OPEN`

## Why this checkpoint exists

Earlier RQ-009 checkpoints framed one unresolved question as a possible deterministic transform:

```text
three component prices (ซอก / ไส้ / คู่) -> two forecast references
```

A direct full-keyword scan of the EP.5 transcript found a materially important teaching block around `46:40-48:04` that changes the safest framing of that question.

The source does not say that the method arithmetically reduces three component prices to two. It contrasts an older generic three-part placement method with the current Body Collection method that uses historical `ซอก + ไส้ + คู่` structure as reference authority.

This checkpoint therefore corrects the research question without deleting the earlier checkpoints that motivated it.

No outcome data is used to choose the interpretation.

## Direct source sequence

### Current method explicitly uses two forecast distances

Around `40:42-40:58`, the instructor teaches:

- step 2 is placing `2 ระยะคาดการณ์` for order-entry reference;
- the placement uses candle body/wick and `ซอกไส้คู่` on the same timeframe.

Around `42:59-43:16`, the source again says to place forecast distance by finding `ซอกไส้คู่` in historical candles.

### Why only two — explicit contrast with the older method

Around `46:40-48:04`, the instructor asks why the current method places only two distances.

The source contrasts:

```text
older placement method:
  divide the area into three parts — head / middle / tail

current Body Collection method:
  use two forecast distances
  using historical candle reference through ซอก / ไส้ / คู่
```

The instructor's stated practical reason is that the three-distance approach consumes/widens SL handling and still does not provide a reliable structural reason for where price should brake/stop. The Body Collection method is presented instead as being anchored to historical candle structure rather than arbitrary partitioning.

This is a method-design rationale, not a machine formula.

### Worked example immediately follows

Around `49:44-51:27`, the instructor then demonstrates a PA Sell case, identifies `ซอก`, `ไส้`, and `คู่`, says the three are complete, and labels forecast references `1` and `2`. Price may react at reference 1, reference 2, or between them, so the resulting area is explicitly not a dead/fixed price.

The worked visual already established one example where `ซอก` and `คู่` share one level while a distinct wick-derived level supplies another. That example is valid evidence for the shown assembly, but it does not prove that every valid Body Collection construction is produced by a generic arithmetic collapse of three independent prices.

## Important research correction

The prior open question:

```text
What is the universal three-component-price -> two-reference reduction formula?
```

is **not source-stated** and risks smuggling an analyst assumption into the research.

The safer source-faithful question is now:

```text
Given source-valid historical ซอก / ไส้ / คู่ structure,
how does the instructor select/assemble the two forecast references in each valid setup family?
```

This distinction matters:

- `ซอก / ไส้ / คู่` are structural qualification/reference ingredients.
- `2 ระยะคาดการณ์` is the current placement method.
- The source reviewed so far does not state that each of the three component types must always contribute one independent price that is later mathematically merged into two.
- Therefore a generic `3 -> 2 reduction` must not be assumed as canonical architecture.

## Source performance claims are not project proof

The same teaching sequence includes instructor statements about extensive backtesting and later performance-rate language. Those are source claims/context, not a project-verified system Win/Loss result.

They do not upgrade unresolved geometry, do not establish a project win rate, and must not be used to select a reference rule or tolerance.

## Current safe representation

For research-only implementation:

1. Detect/source-tag valid shown forms of `ซอก`, `ไส้`, and `คู่`.
2. Preserve every component reference price and provenance.
3. Preserve the source/worked-example grouping into a Body Collection candidate zone.
4. When a source-defined or source-reviewed example yields two forecast references, retain that exact shown topology.
5. If an unseen candidate contains several valid component prices and no source-backed two-reference selection rule resolves them, mark `UNRESOLVED_REFERENCE_SELECTION`.
6. Do **not** force `min/max`, nearest/farthest, newest/oldest, averaging, or a generic 3->2 merge because those rules are not established by the reviewed source.

## What is now closed

- Current EP.5 method intentionally uses two forecast distances/references.
- The source explicitly contrasts this with an older generic three-part `หัว-กลาง-ท้าย` placement method.
- Body Collection references are justified from historical candle structure via `ซอก/ไส้/คู่`, not by arbitrary equal spatial partition.
- The research should not presume that “three component types” means “three independent prices that must be mathematically reduced to two.”

## What remains open

- Exact source rule that selects the two forecast references when several valid component/reference prices coexist.
- Whether there are setup families with three distinct component prices and, if so, how the instructor handles them.
- Equality/feed normalization.
- Same-timeframe multi-cluster priority.
- Universal wick selection.
- Exact touched-to-used transition and exact lower-timeframe broker fill.

## Visual status for this teaching block

A fresh headed-browser seek/capture attempt at the `46:48` comparison block returned a bridge/upstream `502` during this checkpoint. No new visual claim from that failed attempt is used here.

The semantic conclusion above is based on the original rendered YouTube transcript. Visual inspection should be added later if the source player becomes reachable again, especially to see whether the `หัว-กลาง-ท้าย` comparison diagram contains additional selection geometry not represented in speech.

## Decision

Result: `SOURCE_SEMANTIC_CLOSURE / QUESTION_REFRAMED`.

The decision-critical unknown is no longer phrased as an assumed universal `3->2 arithmetic transform`. It is now `EXACT_TWO_REFERENCE_SELECTION/ASSEMBLY_FROM_SOURCE_VALID_STRUCTURE`. This avoids manufacturing a formula that the instructor has not stated and preserves the possibility that component types are qualifications of one or more historical structural references rather than three mandatory independent prices.
