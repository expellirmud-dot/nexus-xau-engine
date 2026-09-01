# NEXUS XAU Rulebook — Current Evidence State

Last consolidation: 2026-09-01

This file preserves all currently known rules without promoting weak evidence into facts.

## 1. Platform / instrument context

### Confirmed from project screenshots / relative

- Platform: MetaTrader 5.
- Broker environment discussed: Exness.
- Relative's environment shown: Exness Technologies Ltd, server `Exness-MT5Real36`, Standard Cent, MT5.
- Relative stated the target instrument is `XAUUSD`.
- User's demo MT5 specification showed: Digits 2, Contract Size 100, Tick Size 0.01, Tick Value 0.1, CFD Leverage, Bid chart mode, Instant execution.

### Point conversion in the user's demo environment only

Because Tick Size = 0.01 and Digits = 2, project calculations have used:

- 1 point = 0.01 USD
- 200 points = 2 USD
- 300 points = 3 USD
- 1,000 points = 10 USD
- 1,500 points = 15 USD
- 3,000 points = 30 USD
- 5,000 points = 50 USD
- 10,000 points = 100 USD

**Do not assume these conversions on the relative's live server until its symbol specification is verified.**

---

## 2. Core cycle

### Evidence A/B

The teaching cycle currently recorded is:

`SIDEWAY → SIG → TP → RETRACE/PULLBACK → SIDEWAY`

Working meanings:

- Sideway: price oscillates while waiting for a frame break and new SIG.
- SIG: PA occurring at a meaningful price frame.
- TP: run generated from the SIG according to its timeframe.
- Retrace / rest: behavior after a timeframe completes or exceeds its run.

### Coding status

State names are usable. Exact transition conditions are **not yet fully deterministic**.

---

## 3. Primary SIG timeframes and run distances

### Relative-confirmed primary SIG timeframes — Evidence A

The relative explicitly stated the SIG timeframes used for trading are:

- H1
- H4
- D1
- W1

M5/M15/M30 must **not** automatically be treated as primary SIG trading timeframes; current evidence suggests they are used for break / relationship / confirmation / entry timing.

### Recorded run distances

Strong project evidence currently supports:

- H1 = 1,000 points
- H4 = 1,500 points at 100%, with references to continuation toward 3,000 points
- Day = 5,000 points, with references toward 10,000
- Week = 15,000 to 30,000 points
- Month = references in project material around 30,000 to 50,000 points

These values must retain their source tags in implementation. Public secondary sources sometimes report different monthly ranges.

---

## 4. PA / PAT context

### Evidence A — direct user statement

- `PA Buy` must occur at support.
- `PA Sell` must occur at resistance **or** at a frame / area where the TP run is complete.
- Pattern shape alone is insufficient.
- After a PA pattern appears, there is an additional process called `เก็บบอดี้` (body collection / body retest).

Therefore the current high-level detector order is:

`LOCATION / FRAME → PA PATTERN → BODY COLLECTION / RETEST → SIG → RUN`

### Evidence C — public summaries, not yet authoritative

Public secondary descriptions commonly describe:

- PAT1 as a pin-bar-like rejection structure.
- PAT2 as a two-candle reversal/engulf-like structure with body close beyond roughly 50% of the prior candle.
- PAT3 as a three-candle structure with the third candle closing beyond the prior structure.

These descriptions are **not yet safe to encode as exact course rules** until verified against primary teaching examples.

---

## 5. Post-SIG wick / SIG_RUN_ANCHOR

### Evidence A — direct relative explanation and screenshot

For the shown `PA BUY PAT2` example:

- candle #3 is the `แท่งไส้หลัง SIG`.
- the relevant wick point is the beginning of the run-count measurement.
- it is also used as a check/reference point.
- it can be used as an SL reference.

Working abstraction:

`SIG_RUN_ANCHOR = post-SIG wick of the identified anchor candle`

For H1:

`target_1x = SIG_RUN_ANCHOR ± 1,000 points`

Direction depends on BUY / SELL.

### Important limitation

Do **not** generalize “candle #3” to PAT1 or PAT3 until confirmed by primary evidence. Secondary summaries claiming PAT1 #2 / PAT2 #3 / PAT3 #4 remain unverified.

---

## 6. Entry conditions currently supported

### Evidence A — teaching slide recorded in the project

- Entry should be close to the frame: distance no more than approximately 200 points in the stated setup.
- M5 breaks price first.
- M15 and M30 should move in the same direction — described as timeframe relationship.
- M5/M15/M30 PA in the same direction gives further run confirmation.
- When H1 subsequently ends with PA in the same direction as smaller TFs, confidence in the direction increases.
- A good SIG should occur as close to the frame as possible.

### Evidence A — caution on adding positions

The teaching slide states that after M5 breaks, one should not casually add orders along the way because gold M15 often retraces; if adding positions, portfolio management is important.

This conflicts with some third-party posts that encourage adding positions every 100–200 points. Therefore pyramiding is **not a confirmed system rule**.

### Exact mechanics still unresolved

- whether M5 “break” means wick breach or candle close.
- exact tolerance around the frame.
- exact order entry type and first-entry trigger.
- whether the ≤200-point rule applies to all setup families or only specific frame entries.

---

## 7. Daily preparation / frames

### Evidence A — teaching material recorded in the project

At approximately 07:00 Thai-time framing in the teaching:

- complete Day, H4 and H1 candles are checked.
- H4 wick ends are used to draw upper and lower frame references.
- a 1,000-point principle is used for the main frame.
- H4 wick tips touching within approximately 7–14 points are described as a strong frame.
- minor support / resistance may be drawn about every 500 points using H1 wick tips with similar 7–14 point contact.
- PA/SIG sets are checked around these frames.

### Daily-frame book material

Project screenshots describe a daily 1,000-point frame with three lines:

- upper frame
- lower frame
- minor support/resistance

The material appears to relate the construction to the 07:00 H4 context and statistical prices, but the exact formula is not fully readable. Do not encode an exact 0/5 rounding formula yet.

---

## 8. Por Chon ATH frame / Mae Pla frame

### Evidence A — screenshot / teaching material

Recorded concepts:

- Por Chon ATH frame acts as a large-timeframe navigation / SIG GPS concept.
- Mae Pla statistical frame is used as a starting area for trade setup.
- ATH frame construction requires conditions involving price running from the previous ATH frame and selecting the highest H4 price in a stated time window.
- A new ATH frame should not be created unless the teaching conditions are satisfied.
- once created, the ATH frame continues to be used.
- it is combined with Mae Pla frames to evaluate proximity / confluence.

### Still unresolved

- exact 19:00–19:00 window semantics and server-vs-Thai timezone handling.
- exact H4 candle selection.
- precise update/invalidation behavior.
- deterministic priority when Por Chon and Mae Pla frames are close.

---

## 9. Half retrace (`พักครึ่ง`)

### Evidence A — relative-confirmed logic

Example context: an upward run.

If a timeframe exceeds its normal run — e.g. H1 normal run 1,000 points but price runs 4,000+ — then for half retrace:

1. identify the SIG set that drove the run,
2. start from its `post-SIG wick`,
3. measure to the furthest / extreme wick reached by the run,
4. calculate the midpoint:

`half_level = (sig_anchor + extreme_price) / 2`

A key relative clarification:

- half retrace is the case where an opposite PA drives the pullback.
- in the upward example, that opposite signal is `PA Sell`.
- the price does **not** have to touch the 50% level exactly.

### Verified arithmetic from user screenshot

Example Fibonacci levels shown:

- 100.0 = 4347.377
- 0.0 = 4526.881
- 50.0 = 4437.129

`(4347.377 + 4526.881) / 2 = 4437.129`

This verifies that the shown 50% is the arithmetic midpoint.

### Not yet confirmed

- whether 23.6 / 38.2 / 61.8 are formal system rules.
- exact opposite-PA definition used to classify HALF.
- exact entry trigger after the midpoint reference exists.

---

## 10. Swing retrace (`พักสวิง`)

### Evidence A — relative-confirmed logic

For an overrun:

- in an upward example, measure from the wick of a qualifying green candle to the highest wick.
- take the midpoint to obtain the swing-retrace reference.
- unlike half retrace, **no PA Sell** drives the move down in the stated upward example.

Working distinction:

- `HALF_RETRACE`: start = post-SIG wick; opposite PA present.
- `SWING_RETRACE`: start = qualifying candle wick; opposite PA absent.

### Still unresolved

The exact rule for selecting the qualifying green candle when several candidates exist is not yet known.

---

## 11. Body collection (`เก็บบอดี้`)

### Evidence from user-provided transcript / project notes

The transcript material already reviewed supports these teaching behaviors:

- body-collection zones are identified using historical candle structures described with terminology such as `ซอก + ไส้ + คู่`.
- H4 is the primary search timeframe in the discussed method; if not found, H1 may be used, and M30 may be consulted in some H1 cases.
- once price reaches the relevant zone, lower-timeframe PA such as M1/M5 may be used in the same direction as the main H4 idea before entry.
- body collection is not simply based on prices ending in 0 or 5; it refers to prior candle structure.
- a body-collection zone, once completed, should not be reused in the same context.
- one transcript described looking roughly 2–4 candles back and dropping one timeframe if the needed structure is not present.
- body collection should not be applied blindly inside Sideway.

### Still not deterministic

- exact body segment to be collected.
- wick touch vs body overlap vs close requirement.
- minimum penetration.
- completion event.
- invalidation event.
- whether lower-TF PA is mandatory in every entry type.

---

## 12. Sideway

### Evidence A — high-level system definition

- Sideway is part of the life cycle before the next SIG.
- teaching material says to wait until the Sideway frame is complete.
- PA must confirm post-SIG wick / directional conditions before planning orders according to the system.
- project transcript material says body collection should not be used normally in Sideway.

### NOT CONFIRMED / DO NOT CODE AS SYSTEM FACT

Recent deep-research web results produced generic or third-party claims such as:

- requiring 2–3 swings,
- trading swings inside the range,
- using particular small lot / SL tactics,
- defining false breakout by a fixed 300-point threshold.

These were not established from primary Mae Pla / Por Chon evidence and must remain secondary hypotheses only.

### Missing exact Sideway state rules

See `OPEN_GAPS.md`.

---

## 13. Risk / SL / TP

### Strong evidence

- post-SIG wick is a reference for run counting and can serve as an SL reference in the shown PAT2 case.
- a project slide contains an example of `SL 300 points`, but this is not proven to be universal.
- run TP is measured from the post-SIG wick anchor according to timeframe.

### Do not treat as confirmed

Third-party statements about fixed 200-point SL, fixed 300-point breakout rules, RR 1:1 / 1:2, automatic breakeven, split TP, or pyramiding are not verified as primary-system rules.

---

## 14. Core prohibitions / cautions

### Evidence A

- Do not counter-trend only because price has completed a nominal TP/run; an over-round move can continue beyond the usual distance.
- if counter-trading is necessary, wait for a clear break/stop condition or an opposite reversal SIG.
- avoid chasing price after the move has already run away from the intended frame.

---

## 15. Coding readiness summary

Safe to implement now as data structures / measurement utilities:

- timeframe run-distance configuration with evidence tags.
- point conversion as broker-specific metadata, not a hard-coded universal.
- SIG event object.
- post-SIG anchor storage.
- H1 1,000-point measurement from anchor.
- half-retrace midpoint calculation once the correct anchor and extreme are supplied.
- swing-retrace midpoint calculation once the qualifying start candle is supplied.
- evidence/confidence fields.
- replay state framework.

Not safe to automate yet:

- full PAT detector.
- full Sideway detector.
- body-collection detector.
- exact Entry/SL engine.
- Por Chon/Mae Pla automatic frame engine.
- multi-timeframe conflict resolver.
- live execution logic.