# EP.5 Body Collection — Full Transcript Rule Extraction

Source basis: user-supplied transcript, reviewed from `0:00` through `2:02:38`.

Evidence level: A for statements explicitly present in the supplied transcript. Performance claims, win rates, personal lot sizing, and anecdotes are preserved only as instructor claims and are not strategy facts.

## 1. High-confidence mechanical findings

### Candle close is required before interpreting the finished candle

- `17:21–18:43`: the instructor repeatedly states that the candle of the timeframe being used must finish before it is judged; M1 waits for the 1-minute close, M5 for the 5-minute close, etc. Color at close matters because an apparently green candle can reverse before close.
- Coding implication: candle-pattern evaluation should use closed bars by default unless a separate live/intrabar rule is explicitly documented.

### Historical left-side candles are reference points

- `5:37–6:19`: look left into past candles to find reference points; prior prices can flip support to resistance or resistance to support.
- Coding implication: body-collection zones are derived from historical candle structure rather than future projection or arbitrary round numbers.

## 2. `ซอก + ไส้ + คู่` zone structure

### ซอก

- `20:33–22:43`: described as a corner/junction between candle prices; the close/open junction is used as a price reference and may later act as support/resistance.
- The exact OHLC matching tolerance is not numerically specified.

### ไส้

- `23:49–25:24`: wick forms when price pushes one way and reverses before the candle closes. Wick interpretation must wait for candle completion.
- The same-timeframe principle is emphasized: H4 body collection should primarily use H4 structures; Day uses Day; M5 uses M5.

### คู่

- `26:47–30:08`: alternating-color candle pair near support/resistance; the instructor describes the paired open/close area as an equilibrium price and says it can be used as support/resistance.
- The exact equality/tolerance for body size and open/close matching is not fully deterministic from transcript text alone.

### All three components form the body-collection zone

- `31:27–32:40`: `ซอก + ไส้ + คู่` together form the zone; for H4 body collection the instructor says the three elements should be present in the zone.
- Indicative zone widths stated in the lesson:
  - H1: about 300–500 points
  - H4: about 500–1,000 points
  - Day: about 1,000–1,500 or 2,000 points depending on timeframe/context
- These are lesson guidance, not yet proven universal hard limits.

## 3. Timeframe search hierarchy

- `32:33–32:49`: if H4 structure is not found, reduce one timeframe.
- `41:35–42:09`: if same-timeframe structure cannot be found, reduce one timeframe to find the projection/reference.
- `43:06–43:49`: look back roughly 2–4 historical candles; if H4 does not provide the needed structure, H1 can be used.
- `1:19:13–1:19:37`: explicit hierarchy example: H4 missing the three conditions -> inspect H1; H1 missing them -> inspect M30.
- `1:01:43–1:02:53` and `1:56:04–1:56:34`: examples show H4 idea with H1/M30 assistance when the H4 projection is unavailable.

Working rule candidate:

`H4 setup -> search H4 zone first -> if insufficient, H1 -> if insufficient, M30`

Status: PARTIAL. The exact definition of “insufficient” still needs a visual/OHLC rule for each of ซอก/ไส้/คู่.

## 4. Body-collection setup sequence

The strongest repeated sequence in the transcript is:

1. Higher-TF PA exists, primarily H4 in this lesson.
2. Build 1–2 projected body-collection zones using historical `ซอก + ไส้ + คู่` on the same TF where possible.
3. If the structure is missing, reduce timeframe as above.
4. Price retraces opposite the original PA direction toward the projection zone.
5. At the zone, inspect M1/M5 PA in the same direction as the higher-TF idea.
6. A break/confirmation at the planned frame is used to consider entry.
7. The retrace can create the post-SIG wick; after that the higher-TF run continues toward TP if the setup works.

Primary transcript anchors:

- `39:16–40:33`: first wait for clear H4 PA. The instructor distinguishes PA from SIG and states that SIG requires PA plus the wick (`ซิก = PA + ไส้` in the spoken context). The body-collection method is taught as a way to anticipate/form the post-SIG wick before waiting until the entire move has already run.
- `40:42–42:35`: place two projected entry distances using candle body/wick and `ซอกไส้คู่`; use the same TF; when price reaches the planned area, require M1/M5 PA in the same direction as H4 and a break at the planned price frame before considering entry.
- `42:52–44:19`: summary repeats the sequence, says look back 2–4 candles, and warns that if price runs beyond the frame / no proper break occurs it may be entering Sideway.
- `1:09:33–1:09:48`: question/answer explicitly states that H4 SIG Sell commonly retraces to collect body first, forming the post-SIG wick, then proceeds toward TP; instructor confirms.
- `1:16:57–1:17:31`: body collection is described as a retrace in the opposite direction from the original H4 PA before returning to the H4 direction.

## 5. Number of zones and zone behavior

- `46:40–48:04`: current lesson favors two projected zones rather than three “head/middle/tail” entry bands because three entries can consume too much SL. This is a method preference in the lesson, not yet a universal law for every setup.
- `49:44–50:20`: example zone contains all three components (`ซอก ไส้ คู่`).
- `50:20–51:27`: price may react at zone 1, zone 2, or between them; zones are projections rather than a single fixed exact price. The instructor emphasizes waiting for PA when price enters the zone.
- `1:03:24–1:03:33`: one example falls short of the projected level by about 100 points and is still discussed as usable; this is an example of tolerance, not a universal 100-point rule.
- `1:13:16–1:13:41`: after a body-collection zone has been used/completed, it should not be reused in the same view; perspective must update.
- `2:01:22–2:02:03`: a zone may remain relevant across days depending on touches; an unused zone is described as especially responsive. This is consistent with retiring a zone after successful use, while allowing untouched zones to persist.

## 6. Entry / lower-timeframe confirmation

- `33:22–34:25`: when price reaches the zone, wait for PA; M1/M5 are mentioned for confirmation; waiting for PA is described as waiting for a break of the frame.
- `42:09–42:35`: after price reaches the projected area, M1/M5 PA should align with H4 and a break at the frame is required before considering entry.
- `56:35–59:43`: M5 example used for actual entry. The instructor describes a slowing/break set, failure to make a higher high, then a red candle engulfing the left-side candles before the sell move. M1 can be used by experienced traders; cautious traders can wait for M5 confirmation. `Zone + PA` is summarized as the actionable combination.
- `1:03:40–1:04:25`: when M5 is still Sideway at the zone, wait for the candle to close / structure to resolve before acting.
- `1:19:37–1:20:01`: if price is in the zone but there is no M5 PA, do not enter under the body-collection conditions.
- `1:26:34–1:28:03`: M1 example discusses a single opposite candle engulfing a short sequence of prior candles; exact PA taxonomy is deferred to a later candle lesson.
- `1:53:04`: instructor states M5 is used mainly to inspect the entry point in the H4-focused approach.

### Unresolved break definition

The transcript repeatedly uses `เบรกกรอบ`, but does not provide a clean deterministic statement of whether a wick breach is enough or a candle body/close is required in every entry setup. Closed-candle discipline is clear; exact break geometry is still OPEN.

## 7. Sideway interaction — important distinction

### Body-collection warning

- `44:19–46:24`: instructor repeatedly warns not to use the body-collection setup inside Sideway because alternating candles/wicks can stop out an entry even if price later returns to the intended direction.
- `1:03:40–1:04:25`: at-zone M5 Sideway is treated as a reason to wait.

### Separate Sideway setup exists

- `1:19:37–1:20:01`: instructor notes that zone conditions can also be used for a separate Sideway-style entry, but this requires knowing whether PA/SIG is genuine.
- `1:16:02–1:16:19` and `1:21:01–1:22:23`: examples show H1 Sideway interacting with a larger H4 SIG/trend context.

Conclusion: `BODY_COLLECTION_SETUP` and `SIDEWAY_SETUP` must be modeled as separate setup families. The statement “never trade Sideway” would be incorrect; the stronger supported statement is “do not blindly apply the body-collection setup inside Sideway.”

## 8. PAT findings from this transcript

### PAT3 Sell discriminator — direct teaching example

- `48:26–49:36`: instructor explicitly chooses PA Sell PAT3 rather than PAT1 because the third candle shows sufficient sell force; its body closes below / covers the previous wick. The instructor says the final candle “กลืนกินไส้เทียนแท่งก่อนหน้า”.

This is valuable but still not enough for a complete PAT3 OHLC detector because the exact prior-candle indexing, equality/tolerance, and BUY mirror conditions are not fully stated.

### PAT2 Sell examples

- `1:06:58–1:07:15`: current-work example labeled PA Sell PAT2.
- `1:12:52–1:13:16`: another PA Sell PAT2 example used to demonstrate body-collection zones.

The transcript labels these visually but does not verbalize the complete candle-by-candle PAT2 formula.

### PAT3 Buy example

- `1:12:07–1:12:45`: example labeled PA Buy PAT3 and followed by two body-collection projection points.

### Important limitation

- `1:27:04–1:28:20`: instructor explicitly says candle/PAT reading will be taught in detail later. Therefore this EP.5 transcript cannot close PAT1/PAT2/PAT3 definitions by itself.

## 9. Post-SIG wick / run / TP

- `39:25–40:11`: transcript distinguishes initial PA from completed SIG and links SIG to PA plus the post-SIG wick.
- `53:40–54:29`: price `3563` is explicitly identified as the post-SIG wick for that PA set.
- `55:02–56:20`: H4 lesson focus is a 1,500-point 100% run; practical discussion mentions capturing around 1,000–1,500 points depending entry/slippage from the ideal zone.
- `1:09:33–1:09:48`: post-SIG wick is formed through the body-collection retrace before the subsequent TP run in the discussed H4 Sell example.

## 10. SL / risk statements — setup-specific, not universal

- `37:42–38:07`: for body collection, instructor says the method does not emphasize waiting for a retest; entry at the frame is discussed with SL roughly 200–300 points from the frame (`ว่ากันไป` indicates contextual variation).
- `50:20–50:42`: example places SL at the wick; instructor says the body can also be used in that specific set, with adjustment because a second projection zone exists.
- `57:38–58:31`: M5 example uses about 300 points beyond the frame to target roughly 1,000–1,500 points.
- `1:31:58–1:32:13`: when scaling/adding in the recap example, the instructor limits the add zone to around 200 points and warns against adding farther because retrace can damage the account.
- `1:53:27–1:53:58`: breakeven after roughly 200–300 or 300–500 points is discussed as trader discretion, not a fixed system trigger.
- `1:55:08–1:55:16`: instructor personally prefers protecting capital and may re-enter if breakeven is hit while the old zone remains valid.

Do not encode personal no-SL anecdotes (`1:32:28+`) or aggressive lot-sizing/performance claims as system rules.

## 11. M5 structural example

- `57:08–58:54`: within the projected zone, the transcript describes slowing/break behavior, inability to make a new high, then a red engulfing candle and sell continuation. The lesson summarizes `Zone + PA = entry consideration` and M5 as the safer confirmation timeframe compared with M1.
- `1:21:38–1:21:58`: another example says M5 confirms that price did not make a higher high and then selected the H4 PA/SIG direction.

This suggests M5 structure (e.g. failure to make a new high/low) may be part of the break confirmation, but exact algorithm is still not complete.

## 12. Instructor claims kept separate from rules

Not to be used as truth labels without backtest evidence:

- body-collection win-rate / “90%” claims (`52:41–53:21`, `1:10:56–1:11:21`),
- backtested more than 500 times (`47:11+`),
- account-growth or daily-profit claims,
- personal lot size / capital usage,
- “100% of account” profit/risk framing.

## 13. What this transcript newly closes

Compared with the earlier project state, EP.5 materially strengthens these items:

1. Body collection is a distinct setup family centered on H4.
2. `ซอก + ไส้ + คู่` are all required components in the demonstrated H4 zone method.
3. Primary search is same timeframe, then step down when structure is unavailable; an explicit H4 -> H1 -> M30 hierarchy appears in Q&A/examples.
4. Use approximately 2–4 past candles as the first search window in the taught example.
5. Two projection zones are favored in the current lesson.
6. At the projection zone, M1/M5 PA aligned with H4 is required before body-collection entry; M5 is the safer confirmation path.
7. Body collection is not based on price ending in 0/5.
8. Completed/used body-collection zones are retired; untouched zones may persist.
9. Body collection should not be applied blindly in Sideway; separate Sideway setups exist.
10. In the demonstrated H4 flow, body collection helps form the post-SIG wick before the run to TP.
11. The transcript gives a partial PAT3 Sell discriminator: third candle body engulfs/closes through the previous wick.
12. Closed-candle evaluation is explicitly required for the timeframe being analyzed.

## 14. Remaining blockers after full transcript review

### Still blocking a deterministic body-collection detector

- OHLC/tolerance formula for detecting `ซอก`.
- OHLC/tolerance formula for detecting `คู่`.
- exact geometric relationship among ซอก/ไส้/คู่ inside a valid zone.
- how to choose zone 1 vs zone 2 when many historical candidates exist.
- exact zone-width hard limits vs examples.
- precise definition of “PA at the zone” for each PAT.
- exact `break frame` rule: wick vs body vs close, and which reference price is broken.
- exact invalidation event before/after entry.

### Still blocking PAT detector

- full PAT1 formula.
- full PAT2 Buy/Sell formula.
- full PAT3 Buy/Sell formula and candle indexing.
- invalid look-alikes.
- post-SIG wick candle mapping for PAT1/PAT3.

### Still blocking Sideway state machine

- start event.
- frame upper/lower wick selection.
- frame-complete condition.
- minimum swings, if any.
- legitimate break vs false break.
- transition to new SIG.
- exact rules of the separate Sideway setup mentioned in Q&A.

### Explicitly deferred by this video

At `1:58:08–1:58:57` the instructor says the next lesson covers `พักครึ่ง / พักสวิง` and Fibonacci retracement/extension. Therefore those rules are not recoverable in full from EP.5 and require the next lesson/transcript.

## 15. Coding readiness after EP.5

Safe now:

- body-collection event/state schema.
- historical-zone candidate objects.
- H4 -> H1 -> M30 search pipeline shell.
- two-zone candidate storage.
- zone lifecycle states: `UNUSED -> TOUCHED/ACTIVE -> COLLECTED/RETIRED` (exact transition geometry still parameterized).
- closed-bar-only evaluation mode.
- post-SIG-wick state placeholder after body collection.
- replay logging of M1/M5 PA at a zone.

Not safe yet:

- automatic `ซอกไส้คู่` detector without manual labels.
- automatic PA/PAT detector.
- automatic M5 break detector.
- automatic Sideway detector.
- live entry/SL engine.

