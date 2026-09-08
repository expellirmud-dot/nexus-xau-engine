# RQ-009 — PAT 50% Denominator Visual Diagnostic

Status: `DIAGNOSTIC_COMPLETE / DENOMINATOR_STILL_UNRESOLVED`

Date: 2026-09-09 Asia/Bangkok

## Question

Can the current PAT teaching slide visually distinguish whether the source's `เกินครึ่ง / >50%` condition is measured against:

1. the prior candle **real body**, or
2. the prior candle **full High-Low range including wicks**?

This diagnostic is deliberately source-first. It does not use market outcomes or Win/Loss to select a formula.

## Source evidence

Primary local source:

- Video ID: `1E_PYPor1qQ`
- teaching window around `14:22-14:29`
- local visual crop: `youtube/_evidence/1E_PYPor1qQ/00-14-29/crop_pat2_slide.jpg`

Relevant source wording includes:

- `มันเกิน 50% ก็มองว่าเป็น PAT 2 ได้`
- `ถ้าแท่งเขียวเนื้อมันเกินครึ่ง 50%`
- `เกินครึ่ง 50% ของแท่งแดง ... มองว่าเป็น PAT 2`

Other reviewed PAT3 wording repeatedly uses `เนื้อ` and, for one variant, explicitly describes a confirming green body exceeding half of two prior red candles combined.

## Analyst image measurement

This section is an **analyst calculation from the source image**, not an instructor-stated numeric measurement.

A simple color-component diagnostic on the PAT2 teaching schematic measured approximately:

- red candle body height: `48 px`
- green confirming body height: `32 px`
- green close/body-top penetrates about `33 px` into the red body

Approximate body reclaim fraction:

```text
33 / 48 ~= 0.6875 ~= 69%
```

Therefore the shown example is clearly consistent with a `>50% of prior BODY` interpretation.

## Why this still does NOT close the denominator

The same teaching schematic also places the confirming green close far enough into the prior red candle that it appears to pass the midpoint of the prior candle's full visible High-Low range as well.

Therefore the current image is **non-discriminating** between the two candidate denominators:

```text
BODY midpoint test      -> passes
FULL-RANGE midpoint test -> also appears to pass
```

A source example that passes both formulas cannot prove which denominator is canonical.

The Sell/PAT3 schematic reviewed around `28:50` likewise reinforces the source's `not over half -> not yet PAT2` / later-candle confirmation semantics, but it does not provide a visual midpoint construction that cleanly separates body from full-range arithmetic.

## Decision

```text
SOURCE SEMANTICS:
  body-specific wording = strong evidence
  strict >half semantics = strong evidence

EXACT MACHINE DENOMINATOR:
  STILL UNRESOLVED
```

Do not upgrade `PAT2_GEOMETRY` or `PAT3_GEOMETRY` to a hard body-only OHLC formula from this schematic alone.

## What would close it

A defensible closure requires at least one source case where:

- body-midpoint and full-range-midpoint give different classifications, and
- the instructor explicitly labels the pattern valid/invalid or visibly draws/measures the relevant half relation.

Until then, body-vs-full-range must remain an explicit research parameter / unresolved source geometry, not an outcome-fitted threshold.

## Local tooling used

Local diagnostic helper:

- `D:/tools/nexus-video-evidence/measure_pat_slide_geometry.py`
- `D:/tools/nexus-video-evidence/measure_pat_wicks.py`

These scripts are diagnostic only and do not encode a trading rule.
