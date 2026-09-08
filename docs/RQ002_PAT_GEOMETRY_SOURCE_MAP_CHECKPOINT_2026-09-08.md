# RQ-002 — PAT2/PAT3 Source Map + First Visual Checkpoint — 2026-09-08

Status: ACTIVE CHECKPOINT / `SOURCE_PARTIAL_VISUAL_AMBIGUITY_REMAINS`

## Scope

Source-first review of PAT2/PAT3 geometry from the local `1E_PYPor1qQ` lesson before any historical geometry-variant computation.

Primary local transcript:

`youtube/2. PAT1  P1 — 1E_PYPor1qQ.txt`

Primary local video:

`youtube/2. Part 1 _ พฤติกรรมการเกิด PA ระบบเทรดแม่ปลาปากกาเขียว.mp4`

## PAT2 — source evidence materially improved

### `00:13:48–00:14:38`

The instructor explicitly distinguishes full engulfing from the weaker but still acceptable PAT2 form:

- red candle followed by green candle;
- full green engulfing of the red candle is described as stronger / higher significance;
- full engulfing is **not required**;
- if the green candle closes/body reaches `เกิน 50%` / `เกินครึ่ง` of the red candle, the instructor says it can still be treated as PAT2;
- wording at `00:14:22–00:14:29` specifically says `ถ้าแท่งเขียวเนื้อมันเกินครึ่ง 50% ... ของแท่งแดง`.

### Strictness evidence

`00:17:17–00:17:40` gives a negative/transition case:

- first green candle `ไม่เกินครึ่ง`;
- therefore the instructor says it cannot yet be PAT2;
- a third candle is required for confirmation into a PAT3 form.

This is direct evidence favoring **strictly beyond half (`> 50%`)**, not merely `>= 50%`, for this teaching lesson.

Caution: exact floating-point/equality handling in OHLC data still needs an implementation convention; the source language itself is strict `เกิน` / `ไม่เกิน`.

## PAT2 first visual cross-check

Evidence bundles:

- `youtube/_evidence/1E_PYPor1qQ/00-14-05/`
- `youtube/_evidence/1E_PYPor1qQ/00-14-29/`
- zoomed local crop: `youtube/_evidence/1E_PYPor1qQ/00-14-29/crop_pat2_slide.jpg`

Observed visual facts:

- slide explicitly labels `PAT 2`, `PAT 3 แบบ 1`, `PAT 3 แบบ 2`, `PAT 3 แบบ 3` under `PA BUY`;
- PAT2 drawing is red -> green at the price frame/support line;
- real bodies and wicks are drawn separately;
- the acceptable green PAT2 body/close visibly reaches beyond the approximate half region of the prior red candle;
- the schematic also shows that full engulfing is a different/stronger visual possibility, consistent with the transcript.

### What this visual does NOT yet close

The current schematic does not uniquely distinguish whether the 50% reference is mechanically:

1. midpoint of candle #1 real body;
2. midpoint of candle #1 full high-low range;
3. equivalent visual body-overlap geometry that happens to coincide in the illustrated case.

The transcript's repeated use of `เนื้อ` materially strengthens a body-based interpretation, but the current frame alone is not sufficient to declare the denominator canonical.

Therefore the denominator remains `VISUAL_AMBIGUOUS`, not guessed from prior backtest performance.

## PAT3 — direct topology from transcript

### PAT3 แบบ 1 — `00:15:12–00:15:59`

Direct wording:

- first candle red;
- middle candle described as Doji / small-body type while its body still stands on the frame;
- third candle green;
- preferred form is green engulfing/defeating the earlier red structure;
- instructor also allows the third green body to be `เกินครึ่ง` of the red candle rather than requiring full engulfing.

Open item:

- no numeric Doji/small-body threshold is stated in this passage;
- no exact equal-wick tolerance is stated.

### PAT3 แบบ 2 — `00:16:06–00:17:10`

Direct wording:

- two red candles first;
- green confirmation candle after them;
- preferred form is green engulfing both;
- instructor states that a green body beyond roughly half of the two red candles together can also be treated as PAT3.

Visual bundle:

`youtube/_evidence/1E_PYPor1qQ/00-16-53/`

Observed visual facts:

- the instructor's on-screen arrow is directed at `PAT 3 แบบ 2` during the explanation;
- the slide shows two red bodies followed by one green body at the frame.

Exact arithmetic definition of `แท่งแดง 2 แท่งรวมกัน` still needs chart/pointer confirmation before encoding a sum-of-bodies equation.

### PAT3 แบบ 3 — `00:17:17–00:17:56`

Direct wording:

- begins with a long red candle;
- first green candle does not exceed half, therefore is not yet PAT2;
- a third candle is required to confirm;
- instructor describes the two green candles together getting beyond half of the red candle as an acceptable PAT3 form;
- full engulfing is described as the cleaner/preferred form, but not the only acceptable form.

This passage still requires a synchronized close visual review before freezing the exact combined-body arithmetic.

## SELL mirror evidence

`00:28:21–00:28:58`

The instructor discusses the SELL-side counterpart:

- a red candle that does not exceed half of the prior green is not yet PAT2;
- another candle may be required;
- combined red confirmation beyond half / defeating the green structure is used for PAT3 qualification.

This supports directional mirroring at a semantic level, but exact OHLC equations should wait for visual alignment.

## Current classification

### Source-backed enough now

- PAT2 does not require full engulfing.
- PAT2 uses a strict `เกินครึ่ง / >50%` concept in this lesson.
- A candle that does not exceed half is explicitly insufficient for PAT2 in the shown transition case.
- PAT3 has three variants with distinct three-candle topologies.
- Full engulfing is preferred/stronger in several examples but not universally mandatory.
- PAT3 variants can use a >half relation when full engulfing is absent.

### Still unresolved / must not encode as canonical yet

- exact 50% denominator: prior real body vs full high-low vs source-specific overlap construction;
- exact equation for `two red candles together` / `two green candles together` in PAT3 variants;
- numeric definition of Doji/small-body middle candle;
- equal-wick tolerance, if any;
- exact floating-point equality handling at mathematically exactly 50% in data implementation, beyond the source's strict natural-language semantics.

## Computation decision

No historical price computation is justified yet.

The remaining blocker is source/visual geometry, not lack of outcome statistics. Running body-vs-range variants now and choosing the better performer would violate provenance discipline.

## Next action

1. inspect synchronized visual windows for PAT3 แบบ 1/2/3 and SELL mirror, with crops where needed;
2. search the five local source videos for any actual-chart/Fibonacci demonstration that visibly fixes the 50% anchors;
3. if no source disambiguates body-vs-range, close that field as parameterized/unknown rather than selecting it from backtest outcomes;
4. only after source geometry is frozen enough, use computation for detector validation rather than semantic discovery.
