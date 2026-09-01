# Evidence Register

Last consolidation: 2026-09-01

This file tracks what sources exist, how they should be weighted, and what each source is allowed to prove.

## Evidence hierarchy

### Level A — direct project evidence

Highest practical weight for this reverse-engineering project.

Includes:

- screenshots supplied by the user from the relative / teaching material,
- direct statements from the user's relative,
- transcripts supplied by the user,
- screenshots of MetaTrader / Exness specification,
- direct examples with prices and marked candle structures.

Use Level A for deterministic coding only when the mechanical rule is explicit enough.

### Level B — attributable public instructor material

Primary public sources such as videos/posts from the teaching channel.

Known channel:

- `UNLOCK TRADER`
- YouTube handle: `@Unlocktrader007`
- public teaching description: “ระบบเทรดแม่ปลาปากกาเขียว”

Known links supplied by the user in this project:

- https://youtu.be/7RJ3zQUeZHs
- https://youtu.be/NwMl2cUMb-A
- https://youtu.be/oCcG3dUjrgw
- https://youtu.be/ESHDuiVPJow
- https://youtu.be/UV5NijhjfJ8 — user labelled this as `การเข้าออเดอร์`
- https://youtu.be/1E_PYPor1qQ — user labelled this as `P1 / PAT1`

Known / visible teaching titles from earlier research/screenshots:

- `วิเคราะห์วงจรกราฟปัจจุบัน และ Recap order 28-04-26`
- `เงื่อนไขการเทรดกรอบไซด์เวย์`
- `วงจรกราฟและความสัมพันธ์ของไทม์เฟรม (ของแท้)`
- `หลักการตีกรอบพ่อชลและเงื่อนไขการใช้จุดพักครึ่งพักสวิง`
- `พื้นฐานระบบปากกาเขียว Term5 EP2 (รีรัน)` — seen in an Unlock Trader Facebook Reel screenshot

Important limitation: direct full transcript access from YouTube was not consistently available. Do not pretend a linked video was fully transcribed unless its transcript or screenshots were actually supplied.

### Level C — secondary / third-party summaries

Use only to generate hypotheses, terminology cross-checks, or questions for the relative.

Known secondary sources:

- https://maeplagreenpen.com/th/concepts/
  - site itself states it is not officially affiliated with Mae Pla / Por Chon / coaches.
- Lemon8 summaries and learner posts surfaced by web/deep-research searches.
- public learner video `Meetingระบบปากกาเขียว 720p HD` by QooAon (public summary; not the user's relative / not primary course material).

Do not promote Level C formulas to engine rules without Level A/B confirmation.

### Level D — analyst inference

Examples:

- mirroring BUY logic into SELL when not explicitly demonstrated,
- assuming an M5 break means candle close rather than wick breach,
- assuming a Fibonacci level is mandatory because it appears on a chart,
- assuming a fixed stop distance applies to every setup.

Level D items must not be used as truth labels in backtests.

---

## Direct evidence inventory

### Platform / symbol specification

User's MT5 desktop XAUUSD Specification screenshot recorded:

- Digits = 2
- Contract size = 100
- Floating spread
- Stops level = 0
- Margin currency = USD
- Profit currency = USD
- Calculation = CFD Leverage
- Tick size = 0.01
- Tick value = 0.1
- Chart mode = Bid
- Trade = Full access
- Execution = Instant
- GTC = Good till cancelled
- Filling = Fill or Kill / Immediate or Cancel

This is the user's demo environment and should not be silently equated with the relative's Real36 Standard Cent account.

### Relative's environment

From project screenshots / messages:

- Exness Technologies Ltd
- server `Exness-MT5Real36`
- Standard Cent
- MT5
- target pair `XAUUSD`

### Relative-confirmed primary SIG TFs

Direct quote meaning preserved:

`ที่ใช้แน่ๆคือเทรดSIG h1 h4 d w`

Therefore primary SIG trading TF set is H1/H4/D/W.

### Half retrace clarification

Relative stated that 50% does not have to be touched exactly.

Relative explanation preserved conceptually:

- if a TF exceeds its own normal run, measure from the post-SIG wick of the SIG set that caused the move to the furthest wick, then divide by two.

### Swing retrace clarification

Relative explanation preserved conceptually:

- in an upward example, measure from the wick of a qualifying green candle to the highest wick, then divide by two for the swing-rest point.

### Half vs Swing distinction

Relative clarified:

- Half retrace: measure post-SIG wick → extreme and an opposite PA drives the pullback (up example: PA Sell).
- Swing retrace: measure qualifying candle wick → extreme and no opposite PA drives the pullback.

### PA location rule

User direct statement:

- PA Buy must occur at support.
- PA Sell must occur at resistance or a frame where TP run is complete.
- after a PA pattern forms, there is a body-collection process.

### PAT2 anchor clarification

User/relative direct explanation:

- in the shown PA BUY PAT2, candle #3 is the post-SIG-wick candle.
- its marked wick starts the run count and is also a check / SL reference.

### Body collection transcript findings — preliminary

Earlier review established:

- zone search terminology includes `ซอก + ไส้ + คู่`.
- H4 is emphasized; if the structure is not available, lower TFs such as H1 and sometimes M30 may be used.
- lower-TF PA such as M1/M5 may be used at the zone in the same direction as the H4 concept.
- body collection is based on prior candle structure rather than simply price-ending digits.
- completed body-collection zones are not reused in the same context.
- one transcript described looking roughly 2–4 candles back and dropping a TF if necessary.
- do not apply body collection normally inside Sideway.

---

## Full EP.5 transcript review — Level A evidence

The user-supplied transcript was reviewed end-to-end from `0:00` through `2:02:38` and saved as a timestamped rule extraction in:

`docs/transcripts/EP5_BODY_COLLECTION_FULL_ANALYSIS.md`

Directly supported additions:

- closed-candle evaluation is explicitly required on the timeframe being analyzed (`17:21–18:43`);
- body-collection zone construction in the lesson uses all three concepts `ซอก + ไส้ + คู่` (`19:41–32:40`);
- same-timeframe search is preferred, with H4 -> H1 -> M30 fallback shown in Q&A/examples (`32:33+`, `41:35+`, `1:19:13+`);
- roughly 2–4 historical candles are cited as the initial lookback (`43:06+`);
- two projected body-collection zones are preferred in the current lesson (`46:40+`);
- at the projected zone, M1/M5 PA aligned with H4 is required before body-collection entry consideration (`42:09+`, `1:19:37+`);
- the transcript repeatedly uses `เบรกกรอบ` but does not fully specify wick-vs-body-vs-close geometry, so exact M5 break remains unresolved;
- body collection is explicitly not based on 0/5 price endings (`34:31–36:11`);
- the transcript distinguishes PA from completed SIG and verbally describes SIG as PA plus the wick in context (`39:16–40:11`);
- H4 Sell example is confirmed to retrace for body collection / post-SIG wick formation before continuing toward TP (`1:09:33–1:09:48`);
- used/completed body-collection zones are retired (`1:13:16–1:13:41`), while untouched zones may persist across days (`2:01:22–2:02:03`);
- body collection is warned against inside Sideway, but a separate Sideway setup using zones is acknowledged (`44:19–46:24`, `1:19:37–1:20:01`);
- a direct PAT3 Sell example says candle #3 body closes through / engulfs the previous wick, and the instructor explicitly rejects an earlier PAT1 reading in that example (`48:26–49:36`);
- PAT2 Sell and PAT3 Buy are visually labeled in examples, but the transcript does not verbalize their full candle-by-candle formulas;
- the instructor explicitly says detailed candle/PAT reading will be taught later (`1:27:04–1:28:20`);
- the next lesson is explicitly described as `พักครึ่ง / พักสวิง` plus Fibonacci retracement/extension (`1:58:08–1:58:57`).

### Setup-specific SL/entry evidence from EP.5

These are direct transcript statements but must not be universalized without more source support:

- body-collection explanation discusses SL roughly 200–300 points from frame (`37:42+`);
- one example permits SL at wick and discusses body as an alternative in that specific structure (`50:20+`);
- one M5 example uses roughly 300 points beyond frame for a 1,000–1,500 point target (`57:38+`);
- one recap restricts adding/scaling to around 200 points and warns against wider adding (`1:31:58+`).

### Instructor claims, not system facts

Do not use as backtest truth labels:

- claimed 90% win/collection behavior,
- claimed >500 backtests,
- account-growth / daily-profit claims,
- personal lot sizing / no-SL anecdotes,
- aggressive portfolio return targets.

---

## Deep-research caution register

A deep-research run on 2026-09-01 returned many generic/secondary statements. The following must remain **UNVERIFIED** unless primary teaching later confirms them:

- Sideway requires exactly 2–3 swings.
- one should trade inside Sideway using small lots and tight stops.
- a false break is defined by exactly ≤300 points.
- SL should generally be 200–300 points.
- TP should use generic RR 1:1 then 1:2.
- add positions every 100–200 points.
- Por Chon “father” frame is simply Day/Weekly and always overrides smaller frames.
- create a new ATH/ATL frame immediately on every new extreme.

Several of those statements came from generic market explanations or learner posts, not the primary Mae Pla/Por Chon source. They are retained only so the project remembers not to accidentally re-import them later as facts.