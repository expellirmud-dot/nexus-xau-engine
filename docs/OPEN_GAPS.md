# Open Gaps / Coding Blockers

Last reviewed: 2026-09-01 after full EP.5 body-collection transcript review (`0:00–2:02:38`).

This file is the authoritative list of what is still missing. A missing item is more important than an invented answer.

## What EP.5 materially closed

The full transcript now provides strong direct evidence for these points:

- closed-candle evaluation is required on the timeframe being analyzed;
- body collection is a distinct H4-focused setup family;
- historical left-side candles are used as reference points;
- the demonstrated body-collection zone uses `ซอก + ไส้ + คู่`;
- search is same-TF first, with an explicit H4 -> H1 -> M30 fallback appearing in examples/Q&A;
- the first search window is described as roughly 2–4 historical candles;
- the current lesson favors two projected zones rather than three head/middle/tail entry bands;
- body collection is not based on price endings 0/5;
- at the projected zone, M1/M5 PA aligned with the H4 direction is required before the body-collection entry; M5 is the safer confirmation path in the teaching;
- used/completed body-collection zones are retired, while untouched zones may persist across days;
- body collection should not be blindly applied inside Sideway; a separate Sideway setup exists;
- in the demonstrated H4 flow, the body-collection retrace helps form the post-SIG wick before the run toward TP;
- a PAT3 Sell example states that the third candle body engulfs/closes through the previous wick; this is a partial discriminator, not a complete PAT3 formula;
- the video explicitly defers full `พักครึ่ง / พักสวิง + Fibonacci` rules to the next lesson.

Detailed timestamp evidence is stored in `docs/transcripts/EP5_BODY_COLLECTION_FULL_ANALYSIS.md`.

---

## Priority 0 — PAT definitions (still the largest blocker)

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

### New evidence from EP.5

- PAT3 Sell example: instructor rejects a PAT1 interpretation and waits for candle #3 because its body closes through / engulfs the previous wick, showing sell force.
- PAT2 Sell and PAT3 Buy are visually labeled in examples, but the transcript does not verbalize their complete formulas.
- instructor explicitly says detailed candle/PAT reading will be taught later.

Specific unresolved questions:

1. What exactly are all “5 PA forms” mentioned in public material?
2. What is the actual full PAT1 rule? The user has now mapped video `1E_PYPor1qQ` as P1/PAT1, so its transcript is highest priority.
3. What is the exact PAT2 Buy/Sell candle sequence and >50% rule, if any?
4. What exactly completes PAT3 on BUY and SELL, beyond the partial Sell example from EP.5?
5. Does wick size matter for PAT2/PAT3?
6. Which visual look-alikes are explicitly rejected?
7. What makes a SIG fake / broken?
8. Which candle supplies the post-SIG wick for PAT1 and PAT3?

Until these are answered, no production PAT detector should be written.

---

## Priority 1 — Body-collection detector geometry

Concept and workflow are now substantially stronger, but exact OHLC geometry remains missing.

Need deterministic definitions for:

- exact `ซอก` formula and price tolerance;
- exact `คู่` formula and equality/tolerance rules;
- exact geometric relation among `ซอก + ไส้ + คู่` inside one valid zone;
- how to rank/select zone 1 and zone 2 when many historical candidates exist;
- whether stated H1 300–500 / H4 500–1,000 / Day 1,000–2,000 point widths are hard bounds or examples;
- exact event that marks a zone `TOUCHED`, `COLLECTED`, and `RETIRED`;
- whether a near miss of ~100 points is generally valid or only an example;
- exact invalidation rule before entry;
- exact invalidation after entry;
- whether lower-TF PA is mandatory for every body-collection setup or whether an advanced frame-entry variant exists.

Working coding shell is now safe:

`H4 PA -> find historical zone -> H4 first, else H1, else M30 -> 1–2 zones -> wait retrace -> M1/M5 PA aligned -> break/confirm -> entry consideration -> post-SIG wick -> run`

The shell is safe; the detectors inside it are not.

---

## Priority 2 — Exact M5 break / Entry mechanics

EP.5 strengthens the role of M5 but does not fully define break geometry.

Need exact answers for:

- whether `เบรกกรอบ` requires wick breach, body breach, or candle close;
- which exact frame/reference price is broken;
- whether failure to make a new high/low is mandatory or only an example;
- whether `Zone + PA = กด` means immediate market order after closed PA or after a separate break candle;
- exact distance-to-frame tolerance;
- whether the ~100–200 point zone distance in the example is a hard threshold;
- whether the prior project rule `ชิดกรอบ <=200` applies to this body-collection setup or another setup family;
- market vs pending order conditions;
- first-entry candle/index;
- re-entry after breakeven / stop / zone remains valid.

### SL questions still open

EP.5 provides several setup-specific examples but not a universal rule:

- around 200–300 points from frame in one body-collection explanation;
- SL at wick in one example, body also discussed as possible in that setup;
- around 300 points in an M5 example;
- adding/scaling limited to around 200 points in one recap example.

Need to determine which are universal, which are setup-specific, and which are personal discretion.

---

## Priority 3 — Sideway state machine

EP.5 clarifies an important distinction but does not define Sideway fully.

Confirmed distinction:

- do not blindly apply `BODY_COLLECTION_SETUP` inside Sideway;
- a separate `SIDEWAY_SETUP` exists and can use zones under its own conditions.

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
- what ends Sideway and creates a new SIG state,
- exact rules of the separate Sideway entry method mentioned in EP.5 Q&A.

Do not use generic “2–3 swings” as a system rule without primary confirmation.

---

## Priority 4 — Half retrace / Swing retrace / Fibonacci

EP.5 does not close these; it explicitly points to the next lesson.

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

Highest-value next source: the lesson immediately after EP.5 described at `1:58:08–1:58:57` as `พักครึ่ง / พักสวิง` plus Fibonacci retracement/extension.

---

## Priority 5 — Multi-timeframe relationship

EP.5 adds examples but not a complete conflict resolver.

New evidence:

- H4 is the main setup TF in the body-collection lesson;
- M5 is used primarily for entry confirmation;
- H1 and M30 can supply historical zone structure when H4 cannot;
- one example shows H4 SIG direction eventually dominating while H1 is Sideway, with M5 confirming failure to make a higher high.

Still need exact conflict rules:

- H1 Buy vs H4 Sell,
- H4 vs D conflict,
- D vs W conflict,
- which timeframe owns the current run,
- whether smaller TF may be traded counter to higher TF,
- exact M15/M30 confirmation metric in the other entry setup: PA, candle direction, structure break, or another condition,
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

EP.5's statement that body collection itself does not use 0/5 must not be generalized to the separate Mae Pla statistical-frame method.

---

## Priority 7 — Labeled ground-truth examples

Need 20–50 real historical examples with instructor/relative labels.

Minimum desired dataset:

- PAT1 Buy/Sell positive examples,
- PAT2 Buy/Sell positive examples,
- PAT3 Buy/Sell positive examples,
- pattern look-alikes that are explicitly invalid,
- body-collection valid zones,
- body-collection near misses that are accepted/rejected,
- M5 break valid/invalid examples,
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
- frame/zone price,
- outcome only for validation, not for defining the label.

---

# Current readiness matrix after EP.5

| Module | Research status | Safe to code? |
|---|---|---|
| Broker metadata / point conversion | Good, environment-specific | Yes |
| Closed-bar evaluation framework | Strong | Yes |
| SIG event data model | Good | Yes |
| H1 run measurement | Strong | Yes |
| Run-distance config | Moderate/strong | Yes, evidence-tagged |
| Half midpoint math | Strong | Yes |
| Half classification | Partial | No |
| Swing midpoint math | Strong if anchors supplied | Yes |
| Swing anchor selection | Missing | No |
| PAT detector | Partial examples only | No |
| Body-collection state/schema | Stronger | Yes |
| Body-collection geometry detector | Missing exact OHLC rules | No |
| H4->H1->M30 zone-search shell | Strong enough | Yes |
| Zone lifecycle schema | Strong enough | Yes, geometry parameterized |
| Sideway detector | Partial concept only | No |
| M5 break detector | Partial examples | No |
| Entry engine | Partial | No |
| SL engine | Setup-specific examples only | No |
| TP measurement | Moderate | Partially |
| Multi-TF resolver | Missing conflict rules | No |
| Por Chon frame engine | Partial | No |
| Mae Pla statistical frame engine | Partial | No |
| Replay framework | Architecture ready | Yes |
| Full backtest strategy | Blocked by labels/rules | No |
| Live EA execution | Premature | No |

## Short answer: what is still missing most?

After the full EP.5 transcript, the highest-value missing pieces are now:

1. **PAT1/PAT2/PAT3 exact candle rules and invalidations** — PAT1 transcript first (`1E_PYPor1qQ`).
2. **Exact `ซอก + ไส้ + คู่` OHLC geometry and M5 break rule** — this is now the core body-collection coding blocker.
3. **Full Sideway lesson/state machine** — importantly separate from body-collection logic.
4. **Next lesson: Half/Swing + Fibonacci** — explicitly deferred by EP.5.
5. **Por Chon/Mae Pla exact frame algorithms**.
6. **20–50 labeled positive/negative examples for truth-set validation**.

With items 1–3 resolved, the project can start meaningful detector/replay backtesting without inventing the core rules.