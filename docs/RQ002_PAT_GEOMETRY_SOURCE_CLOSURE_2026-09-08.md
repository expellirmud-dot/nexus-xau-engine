# RQ-002 — PAT2 / PAT3 Geometry Source Closure — 2026-09-08

Status: CLOSED / `SOURCE_BACKED_PARTIAL_PARAMETERIZED`

## Question

Close the source-backed PAT2/PAT3 geometry far enough to distinguish what is directly supported from what must remain parameterized, especially the >50% relation and its measurement basis.

## Source set reviewed

Primary local bounded batch:

- `1E_PYPor1qQ` — PAT1 / PA behavior lesson, transcript + synchronized visual frames.
- `vcdN51_OrPE` — system summary, transcript cross-check.

Material timestamps reviewed in `1E_PYPor1qQ`:

- 13:48–14:38 — PAT2, full engulfing versus >50% acceptance.
- 15:22–15:59 — PAT3 variant 1.
- 16:06–17:10 — PAT3 variant 2.
- 17:17–17:56 — PAT3 variant 3.
- 28:21–28:58 — SELL-side mirror / need for the third candle when PAT2 is not yet >half.

Visual evidence bundles created locally under the gitignored source vault:

- `youtube/_evidence/1E_PYPor1qQ/00-14-05`
- `youtube/_evidence/1E_PYPor1qQ/00-14-29`
- `youtube/_evidence/1E_PYPor1qQ/00-15-46`
- `youtube/_evidence/1E_PYPor1qQ/00-17-02`
- `youtube/_evidence/1E_PYPor1qQ/00-17-32`
- `youtube/_evidence/1E_PYPor1qQ/00-17-56`
- `youtube/_evidence/1E_PYPor1qQ/00-28-50`

## Direct source findings

### PAT2

The source directly states and visually demonstrates:

- PAT2 uses two candles.
- BUY example: red candle followed by green candle.
- SELL is taught as directional mirror.
- Full engulfing is stronger/cleaner but is not mandatory.
- A confirming second candle that exceeds half / exceeds 50% of the first-candle reference can still qualify as PAT2.
- A confirming candle that does **not** exceed half is explicitly described as not yet enough to call PAT2; in the demonstrated sequence the teacher waits for a third candle.

Therefore the source semantics support a **strict exceed-half relation (`>50%`)**, not an automatically inclusive `>=50%` production rule.

### PAT3 variant 1

The source demonstrates:

- first directional candle;
- small/Doji-like middle candle;
- third opposite-direction confirmation candle;
- full engulfing is shown as stronger/cleaner;
- the teacher also accepts a configuration where the confirming body exceeds half of the prior directional candle.

Exact Doji/small-body and wick-balance tolerances are not numerically defined.

### PAT3 variant 2

The source demonstrates two prior same-direction candles followed by an opposite confirmation candle.

The teacher explicitly describes the confirmation in relation to the **two prior candles combined** and says an over-half relation can qualify, while full engulfing of both prior candles is the cleaner/stronger expression.

The transcript wording does not close the exact OHLC arithmetic of “two candles combined” sufficiently to encode one canonical numeric formula without interpretation.

### PAT3 variant 3

The source demonstrates:

- one large directional candle;
- the first opposite-color reaction candle does not exceed half, so PAT2 is not yet confirmed;
- a third candle is required;
- the two opposite-color confirmation candles together must exceed half relative to the original directional candle / demonstrated combined structure.

Again, full engulfing is described as the cleaner form, but the source accepts an over-half combined confirmation.

## Measurement-basis closure

The source repeatedly uses language centered on `เนื้อ` / candle body when explaining the >half relation, which materially strengthens the case that body geometry is important.

However, the reviewed teaching schematic does **not** provide a visual measurement line that uniquely separates:

- prior real-body midpoint;
- full high-low midpoint;
- another source-specific visual/Fibonacci construction.

The same schematic can remain visually compatible with more than one denominator representation.

Therefore:

```text
>50% relation: SOURCE-BACKED
exact denominator: UNRESOLVED / PARAMETERIZED
```

Do not convert this into one canonical OHLC denominator from backtest performance.

## Equality

Because the source repeatedly says `เกินครึ่ง` / `เกิน 50%` and explicitly contrasts it with a candle that `ไม่เกินครึ่ง`, the strongest source-level semantic reading is strict `>50%`.

This does not by itself define floating-point tolerance or broker-price equality handling. Those remain implementation conventions and must be kept separate from the teaching claim.

## Safe project representation after closure

```text
PAT2:
  candles = 2
  direction topology = source-backed
  full engulfing = preferred/stronger, not mandatory
  confirmation relation = >50% source semantic
  denominator = parameterized/unresolved

PAT3:
  candles = 3
  variants = 3
  full engulfing = preferred/stronger in demonstrated forms, not universal minimum
  >50% relation = source-backed, variant-dependent
  exact combined-candle arithmetic = parameterized/unresolved
  small-body/Doji threshold = unresolved
  equal-wick tolerance = unresolved
```

## What this changes

The prior generic statement that PAT2 merely closes “around 50%” was too weak. The reviewed source provides stronger semantics: `>half` is the qualifying relation in the demonstrated teaching, while `not over half` is insufficient for PAT2.

This does **not** upgrade the current PAT2-BODY research proxy into a canonical detector because the exact denominator remains unresolved.

## What remains unknown

- whether the 50% denominator is strictly real body, full range, or another source-defined construction;
- exact Doji/small-body numeric threshold;
- exact equal-wick tolerance for middle candles where visually relevant;
- exact arithmetic for PAT3 variant-2 combined prior candles;
- exact arithmetic for PAT3 variant-3 combined confirmation candles;
- price/tick tolerance for equality at exactly 50%.

These unknowns must remain explicit. Historical performance cannot choose among them.

## Closure decision

```text
SOURCE_BACKED_PARTIAL_PARAMETERIZED
```

RQ-002 is closed because the source has been exhausted far enough to define the current boundary: topology and strict >half semantics are source-backed; the unresolved denominator/tolerances are now explicitly parameterized rather than hidden.

## Next queue item

Promote `RQ-003 — Daily Frame and Location exact construction semantics`.
