# Open Gaps / Coding Blockers

Last reviewed: 2026-09-01

This file is the authoritative list of what is still missing. A missing item is more important than an invented answer.

## Priority 0 — PAT definitions (largest blocker)

Need primary examples / explicit rules for every PA/PAT family.

Required fields per pattern:

- exact number of candles,
- candle colors if relevant,
- body relationship,
- wick relationship,
- whether close must exceed a prior body / wick / midpoint,
- completion candle,
- invalidation rule,
- BUY and SELL versions,
- location requirement,
- which candle supplies `ไส้หลัง SIG`,
- whether candle numbering differs by PAT.

Specific unresolved questions:

1. What exactly are all “5 PA forms” mentioned in public material?
2. Is PAT1 one candle or a multi-candle confirmed structure in the actual teaching?
3. Is PAT2 truly defined by a >50% prior-body close, and is that strict or approximate?
4. What exactly completes PAT3?
5. Does wick size matter for PAT2/PAT3?
6. Which visual look-alikes are explicitly rejected?
7. What makes a SIG fake / broken?

Until these are answered, no production PAT detector should be written.

---

## Priority 1 — Sideway state machine

Need exact system-specific rules for:

- event that starts Sideway,
- minimum number of swings, if any,
- timeframe used to construct the Sideway frame,
- exact upper-frame wick selection,
- exact lower-frame wick selection,
- definition of “กรอบ SW ครบ”,
- whether both Buy-side and Sell-side PA confirmations are required before the frame is considered complete,
- order / sequence of those confirmations,
- what constitutes a legitimate breakout,
- what constitutes a false breakout,
- whether break must be by wick or close,
- point tolerance outside the frame,
- required confirming TF after breakout,
- what ends Sideway and creates a new SIG state.

Do not use generic “2–3 swings” as a system rule without primary confirmation.

---

## Priority 2 — Body collection (`เก็บบอดี้`)

Need deterministic geometry:

- Which candle's body is the target?
- Is the target full body, head/middle/tail zone, or a named sub-zone?
- Does wick contact count?
- Must candle body overlap the zone?
- Must a candle close inside / through the zone?
- Is 50% penetration relevant?
- What exact event means “เก็บเสร็จ”?
- What invalidates the zone?
- Is lower-TF PA mandatory after the retest?
- Which lower TF is selected under each higher-TF setup?
- How many times can the zone be revisited before invalidation?

---

## Priority 3 — Half retrace / Swing retrace

### Half retrace

Known formula is strong; classification mechanics are incomplete.

Need:

- exact definition of the opposite PA used to classify HALF,
- when the extreme is considered final enough to measure,
- whether the reference updates as new extremes form,
- whether the midpoint is recalculated dynamically,
- entry trigger after the retrace starts,
- invalidation condition,
- SL / TP after the retrace setup.

### Swing retrace

Need:

- exact rule for selecting the qualifying starting candle when multiple green/red candles exist,
- whether candle color alone matters or another structural rule selects it,
- when the extreme is fixed,
- whether 50% is just a reference or a trigger zone,
- exact entry / invalidation rules.

### Fibonacci

Need primary confirmation of whether 23.6 / 38.2 / 61.8 / extensions are formal rules or merely chart aids. Current direct evidence only proves the arithmetic midpoint example.

---

## Priority 4 — Execution rules

Need exact answer for each setup family:

- first-entry trigger,
- market vs pending order,
- whether entry waits for candle close,
- exact role of M5 break,
- exact meaning of M15/M30 moving in the same direction,
- distance-to-frame calculation,
- whether ≤200 points is universal or setup-specific,
- whether additional positions are allowed,
- if yes, under what risk constraints,
- if no, when the “do not add” warning applies,
- exact SL anchor,
- whether SL is at wick or offset beyond it,
- whether the 300-point slide is an example or a universal buffer,
- TP timeframe selection,
- partial exit rules, if any,
- handling of Over-round / overrun,
- re-entry after stop / retrace / new SIG.

---

## Priority 5 — Multi-timeframe relationship

Need exact conflict rules:

- H1 Buy vs H4 Sell,
- H4 vs D conflict,
- D vs W conflict,
- which timeframe owns the current run,
- whether smaller TF may be traded counter to higher TF,
- exact M5 break condition,
- exact M15/M30 confirmation metric: PA, candle direction, structure break, or another condition,
- whether H1 PA must close before the setup is upgraded.

---

## Priority 6 — Por Chon / Mae Pla frame algorithms

Need primary confirmation for:

- exact 19:00–19:00 interpretation,
- Thai time vs MT5 server time,
- exact H4 candle / wick selection for ATH frame,
- exact 1,000-point condition from old ATH,
- whether new ATH must occur in a specific window,
- when the old frame remains valid,
- when it is retired,
- exact Mae Pla daily statistical-frame formula,
- exact use of price endings 0 / 5, if any,
- exact 500-point sub-frame derivation,
- role of 7–14 point wick contact,
- priority / confluence behavior when Por Chon and Mae Pla frames are close.

---

## Priority 7 — Labeled ground-truth examples

Need 20–50 real historical examples with instructor/relative labels.

Minimum desired dataset:

- PAT1 Buy positive examples,
- PAT1 Sell positive examples,
- PAT2 Buy positive examples,
- PAT2 Sell positive examples,
- PAT3 Buy positive examples,
- PAT3 Sell positive examples,
- pattern look-alikes that are explicitly invalid,
- half-retrace examples,
- swing-retrace examples,
- Sideway valid frames,
- Sideway false-break examples,
- entry examples that should be taken,
- entry examples that must be skipped,
- SL / TP examples,
- Over-round examples.

Each labeled case should ideally include:

- date/time,
- broker/server/timezone,
- symbol,
- timeframe,
- screenshot,
- teacher/relative label,
- reason,
- anchor price,
- frame price,
- outcome only for validation, not for defining the label.

---

# Current readiness matrix

| Module | Research status | Safe to code? |
|---|---|---|
| Broker metadata / point conversion | Good, environment-specific | Yes |
| SIG event data model | Good | Yes |
| H1 run measurement | Strong | Yes |
| Run-distance config | Moderate/strong | Yes, evidence-tagged |
| Half midpoint math | Strong | Yes |
| Half classification | Partial | No |
| Swing midpoint math | Strong if anchors supplied | Yes |
| Swing anchor selection | Missing | No |
| PAT detector | Missing exact rules | No |
| Body collection detector | Partial concept only | No |
| Sideway detector | Partial concept only | No |
| Entry engine | Partial | No |
| SL engine | Partial | No |
| TP measurement | Moderate | Partially |
| Multi-TF resolver | Missing conflict rules | No |
| Por Chon frame engine | Partial | No |
| Mae Pla statistical frame engine | Partial | No |
| Replay framework | Architecture ready | Yes |
| Full backtest strategy | Blocked by labels/rules | No |
| Live EA execution | Premature | No |

## Short answer: what is still missing most?

The three highest-value missing pieces remain:

1. **exact PA/PAT1-2-3 definitions and invalidations**,
2. **exact Sideway frame / breakout state rules**,
3. **exact Entry + body-collection + SL trigger rules**.

With those three resolved, the project can move from framework coding to meaningful detector/replay validation.