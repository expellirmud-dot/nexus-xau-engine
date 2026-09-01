# P0-1 PA/PAT Closure Review — 2026-09-01

Source: user-supplied full timestamp transcript for the Smart Trader To Success / Mae Pla Green Pen foundation class associated in project context with `NwMl2cUMb-A`.

Evidence rank: Primary teaching transcript supplied by user. Transcript wording may contain ASR errors; geometry inferred only where the instructor states it or the project has matching primary slide evidence.

## Verdict

P0-1 is **not 100% closed**, but the unknown has narrowed materially.

Recommended status:

- PA/PAT workflow + taxonomy + pattern length + location + post-SIG indexing + major invalidation: **CLOSED / high confidence**.
- Exact numeric OHLC geometry for production detector: **PARTIAL**.
- Estimated P0-1 closure: **~80%**.

This means P0-1 should be split rather than treated as one opaque blocker.

## Newly direct-supported rules

### Taxonomy / PAT length

- PA has five taught shapes arranged as PAT1, PAT2 and three PAT3 forms.
- Instructor explicitly says `PAT` refers to number of candles.
- PAT1 = 1 candle.
- PAT2 = 2 candles.
- PAT3 = 3 candles.

### PAT1

- Described as hammer-like (`แฮมเมอร์`) in the teaching.
- BUY PAT1 must occur at support; wrong-location BUY PAT1 at resistance can reverse/fail.
- SELL mirror belongs at resistance.
- Candle color is not absolutely mandatory for PAT1, but directional color is preferred/stronger: green for BUY, red for SELL.
- Exact wick/body numeric ratio is not stated in this class.

### PAT2

- Two-candle structure.
- It does **not** have to be a full engulfing pattern.
- The second candle may qualify when it closes approximately 50% of the first candle.
- Instructor says the 50% can be judged visually or measured with Fibonacci inside the candle.
- Transcript does not unambiguously resolve whether the 50% baseline must be full High-Low range or body-only in every case; the instructor separately emphasizes reading candle force primarily from the body.
- A valid PAT2 can later be subsumed into a PAT3 when the third candle arrives (`ซิกซ้อนซิก`).

### PAT3

- Three-candle structure.
- Instructor explains that candle #3 can determine whether the structure becomes real/strong PA by `กลืนกิน` / overcoming the preceding candle.
- A separate project transcript/example states PAT3 Sell was judged because the last candle body closed below / covered the prior wick, indicating Sell force.
- Exact deterministic boundaries distinguishing PAT3 variants 1/2/3 remain unresolved.

### Location qualification

- PA can visually appear anywhere, but useful qualification depends strongly on location.
- BUY belongs at support.
- SELL belongs at resistance.
- Same visual PAT appearing at the wrong side is explicitly taught as dangerous / potentially reversing.
- Higher-timeframe support/resistance can override what looks like a lower-timeframe pattern location.
- Exact point tolerance from support/resistance remains unresolved.

### PA vs SIG timeframe semantics

- PA can occur on all TFs from M1 upward.
- The class reserves `SIG` / PA + post-SIG wick for H1 and above.
- Project-relative evidence remains that primary traded SIG TFs are H1/H4/D/W.

### Post-SIG reference candle

Directly restated in transcript:

- PAT1 -> count/reference candle #2.
- PAT2 -> candle #3.
- PAT3 -> candle #4.

The class also clarifies anchor fallback:

- if the reference candle has a wick, use the relevant wick;
- if there is effectively no wick, use the extreme price/body edge;
- BUY: lowest price;
- SELL: highest price.

### Candle completion

- Do not classify before the timeframe candle closes.
- H1 must finish H1; H4 must finish H4.

### Confirmation windows taught in this class

- H1: wait roughly 2–4 candles.
- H4 and above: wait roughly 1–3 candles.

These are teaching confirmation windows, not yet necessarily universal pattern-length rules.

### Major invalidation / Sideway clue

Strong direct rule:

- a good PA should not be `กวน` / exceeded by its post-SIG wick;
- if the post-SIG wick extends beyond the PA structure, the signal is unusable in the shown example and the sequence is identified as Sideway;
- later example: PAT2 on candles 1+2, candle 3 as post-SIG wick; candle 3 exceeds the PA -> unusable;
- a later 3+4 PAT2 with candle 5 post-SIG wick that does not disturb the PA is described as the real SIG.

Another example states that a later candle below the post-SIG wick constitutes destruction of the post-SIG wick, with a cited difference of ~200 points in that example. Do not generalize 200 points as a universal invalidation buffer without further evidence.

## Important correction for P0-2 terminology

The class explicitly states that `เบรก` in this system means **stop / brake**, not `breakout`.

- It is discussed at the statistical frame (0/5) using M1/M5.
- If price continues rather than stopping, the instructor uses the term `เจิด`.

Therefore any old project hypothesis `M5 break = close beyond frame breakout` must remain quarantined. Exact geometry of `stop/brake` still needs the dedicated M5 lesson.

## Remaining P0-1 exact detector gaps

1. PAT1 numeric wick/body threshold.
2. PAT2 exact 50% measurement basis: full High-Low candle vs body-only, including equality/tolerance rule.
3. PAT3 v1/v2/v3 exact OHLC distinction and close/engulf thresholds.
4. Support/resistance/frame qualification tolerance in points and multi-frame priority.
5. Exact interpretation of `post-SIG wick does not disturb PA` as inequalities for BUY/SELL in all PAT variants.
6. Boundary cases: doji/equal open-close, tiny wick, equal highs/lows, gaps, and broker rounding.
7. Positive and negative labeled OHLC examples sufficient to regression-test the detector.

## Where the missing rules likely live according to the instructor

The class roadmap itself points to:

- Day/EP for support-resistance: exact support/resistance, `ซอก/ไส้/คู่`.
- Final candle-reading lesson: candle body/wick/volume/size interpretation, which is directly relevant to PAT numeric geometry.
- Dedicated M5 lesson: exact meaning/implementation of system `เบรก`.

## Engineering decision

P0-1 should now be decomposed as:

- `P0-1A PAT taxonomy/count/index/location`: CLOSED.
- `P0-1B PAT2 ~50% criterion`: MOSTLY CLOSED, measurement basis still ambiguous.
- `P0-1C post-SIG invalidation`: MOSTLY CLOSED conceptually; exact inequality/tolerance pending.
- `P0-1D PAT1 numeric geometry`: OPEN.
- `P0-1E PAT3 variant exact geometry`: OPEN.
- `P0-1F ground-truth edge cases`: OPEN.

Prototype status:

- It is now justified to implement an evidence-tagged `PAT_CANDIDATE` detector and post-SIG validator.
- It is **not** yet justified to label the detector `EXACT` or use it for unattended live execution.
