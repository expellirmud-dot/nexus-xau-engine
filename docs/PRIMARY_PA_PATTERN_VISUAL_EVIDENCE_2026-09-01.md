# Primary PA Pattern Visual Evidence — 2026-09-01

Scope: three user-supplied screenshots from a Smart Trader To Success / PA (PRICE ACTION) teaching slide showing BUY and SELL PA structures, support/resistance context, and examples of counting the post-SIG wick.

Evidence class: Level A project evidence because the images are direct teaching-material screenshots supplied by the user. This document records only what is visually explicit enough to support the research engine. It does not invent missing OHLC thresholds.

## 1. Major nomenclature correction: “PA 5 รูปแบบ” is not PAT1–PAT5

The teaching slide visually shows exactly five PA forms on each side, but they are labeled as:

1. `PAT1`
2. `PAT2`
3. `PAT3 รูปแบบที่ 1`
4. `PAT3 รูปแบบที่ 2`
5. `PAT3 รูปแบบที่ 3`

Therefore the strongest current interpretation is:

`PA 5 รูปแบบ = PAT1 + PAT2 + PAT3(variant 1, variant 2, variant 3)`

This materially changes the previous open question about PAT4/PAT5. Until a primary source explicitly introduces PAT4/PAT5, the engine must NOT assume PAT4 or PAT5 exist as separate families.

## 2. Pattern candle counts are now directly supported

The slide contains an explicit post-SIG counting note:

- `PAT1 นับแท่งที่ 2`
- `PAT2 นับแท่งที่ 3`
- `PAT3 นับแท่งที่ 4`

Combined with the drawn structures, this supports the family lengths:

- PAT1 = one pattern candle; next/post-SIG reference is candle #2.
- PAT2 = two pattern candles; next/post-SIG reference is candle #3.
- PAT3 = three pattern candles; next/post-SIG reference is candle #4.

This directly confirms the earlier relative explanation for the shown PAT2 Buy example and extends the pattern-index mapping to PAT1/PAT3 at the teaching-slide level.

Implementation-safe abstraction:

```text
pattern_family  pattern_length  post_sig_reference_index
PAT1            1               2
PAT2            2               3
PAT3            3               4
```

Important: this closes the candle index used to locate the post-SIG reference candle, but not yet the exact wick-side/tolerance/invalidation rule for every context.

## 3. BUY location and visual structures

The BUY section is explicitly drawn on a dashed `แนวรับ` (support) line.

### PAT1 BUY — visual fact

- one green candle;
- long lower wick reaches / rejects the support line;
- body is above the support line.

The exact numeric wick/body ratio is NOT given in the image.

### PAT2 BUY — visual fact

- two candles;
- first candle red and reaches the support area;
- second candle green and reverses upward from the support area;
- the drawn green candle closes above the red body in the schematic.

The image does NOT provide a numeric `>50%` threshold. Do not hard-code a 50% PAT2 rule from this image alone.

### PAT3 BUY — three visible variants

All are three-candle structures around support:

- Variant 1: red first candle -> very small/indecision-like middle candle at support -> strong green third candle.
- Variant 2: red first candle -> smaller red second candle near support -> strong green third candle.
- Variant 3: red first candle -> green second candle -> stronger/continuing green third candle.

These are visual color/order facts from the schematic. Exact OHLC overlap/engulf/close thresholds remain unresolved.

## 4. SELL location and visual structures

The SELL section is explicitly drawn on a dashed `แนวต้าน` (resistance) line.

### PAT1 SELL — visual fact

- one red candle;
- long upper wick reaches / rejects the resistance line;
- body is below the resistance line.

Exact numeric wick/body ratio is not stated.

### PAT2 SELL — visual fact

- two candles;
- first candle green into resistance;
- second candle red reverses downward from resistance;
- the schematic shows a strong red follow-through candle.

No numeric `>50%` threshold is printed on this slide.

### PAT3 SELL — three visible variants

All are three-candle structures around resistance:

- Variant 1: green first candle -> very small/indecision-like middle candle near resistance -> strong red third candle.
- Variant 2: green first candle -> green second candle near resistance -> strong red third candle.
- Variant 3: green first candle -> red second candle -> stronger/continuing red third candle.

Again, these are schematic color/order observations, not yet exact OHLC formulas.

## 5. Post-SIG wick examples — major closure

The slide explicitly labels `ตัวอย่าง การนับไส้หลัง Sig` and places a dashed outline after each completed pattern. The accompanying text states:

- PAT1 uses/counts candle #2;
- PAT2 uses/counts candle #3;
- PAT3 uses/counts candle #4.

This is primary evidence supporting the generic anchor-candle index mapping for the three pattern families.

Working engine interface can now become:

```pseudo
post_sig_candle_index(PAT1) = 2
post_sig_candle_index(PAT2) = 3
post_sig_candle_index(PAT3) = 4
```

Still unresolved before a full anchor detector:

- exact wick selected on the reference candle for BUY vs SELL in all cases;
- whether a minimum wick length is required;
- whether the post-SIG candle must have a specific color;
- invalidation if that candle has no meaningful wick;
- whether a later wick may replace the original anchor in special cases.

## 6. Location rule is visually reinforced

The slide explicitly presents:

- BUY PA patterns at support (`แนวรับ`);
- SELL PA patterns at resistance (`แนวต้าน`).

A lower note also describes PA / SIG forms as price-run signals when they occur in the correct support/resistance location and references H1 run counting of 1,000 points.

This reinforces existing direct project evidence:

- PA Buy belongs at support.
- PA Sell belongs at resistance / appropriate completed-run context.
- pattern shape without correct location is not sufficient for the engine.

## 7. What is now CLOSED vs still UNKNOWN

### CLOSED / high confidence

- the teaching set contains five PA forms arranged as PAT1, PAT2 and three PAT3 variants;
- do not assume separate PAT4/PAT5 from the phrase “PA 5 รูปแบบ”;
- PAT1 is a one-candle pattern family;
- PAT2 is a two-candle pattern family;
- PAT3 is a three-candle pattern family;
- post-SIG reference-candle mapping: PAT1 #2, PAT2 #3, PAT3 #4;
- BUY schematics are located at support;
- SELL schematics are located at resistance;
- BUY/SELL color-order examples shown for PAT1/PAT2/PAT3 variants.

### PARTIAL / not deterministic yet

- exact body-percentage conditions;
- exact engulf/overlap requirement;
- whether close must cross a prior body midpoint, body edge, wick, high/low;
- exact wick/body ratio for PAT1;
- exact distinction between PAT3 variant 1 vs 2 when middle candle geometry is borderline;
- pattern invalidation/fake-SIG rules;
- exact frame-distance tolerance specific to PA qualification;
- exact post-SIG wick side/minimum geometry.

## 8. Engineering consequence

The previous placeholder family model:

`detect_PAT1() ... detect_PAT5()`

should be changed conceptually to:

```text
detect_PAT1()
detect_PAT2()
detect_PAT3_variant1()
detect_PAT3_variant2()
detect_PAT3_variant3()
```

or a parameterized `detect_PAT3(variant)` implementation.

A production detector still must wait for transcript/chart evidence giving exact OHLC thresholds and invalidation rules, but the pattern taxonomy, pattern length, location context and post-SIG candle index are now materially closed.
