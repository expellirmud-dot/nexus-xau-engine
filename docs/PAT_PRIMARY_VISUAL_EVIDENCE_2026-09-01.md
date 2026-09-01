# PAT Primary Visual Evidence — 2026-09-01

Source: three user-supplied screenshots from Smart Trader To Success training material showing `PA (PRICE ACTION)` entry patterns for BUY/SELL and examples of post-SIG wick counting.

Evidence class: PRIMARY VISUAL (training slide screenshot). This file records only what is directly visible or safely inferable from the slide; it does not invent body/wick percentages or close thresholds.

## Directly visible structure

The slide presents **five PA shapes total**, labeled as:

1. `Pat 1`
2. `Pat 2`
3. `Pat 3 รูปแบบที่ 1`
4. `Pat 3 รูปแบบที่ 2`
5. `Pat 3 รูปแบบที่ 3`

This is important: the primary slide does **not** show separate labels `PAT4` or `PAT5`. The visible five-pattern set is PAT1 + PAT2 + three PAT3 variants. Any project note treating `PAT1–PAT5` as five separately numbered pattern families must therefore be quarantined until another primary source proves that numbering.

## Location rule shown on slide

- BUY patterns are drawn on a dashed `แนวรับ` (support) line.
- SELL patterns are drawn on a dashed `แนวต้าน` (resistance) line.

This directly reinforces the existing relative-chat evidence: PA Buy belongs at support; PA Sell belongs at resistance / valid upper context.

## Visible BUY pattern topology

These are visual topology observations only, not full OHLC equations.

- `Pat 1`: one bullish/green rejection-style candle located at support. The label appears to describe a pin-bar-like form, but exact Thai wording is not promoted to a rule because the screenshot resolution is insufficient for a perfect transcription.
- `Pat 2`: bearish/red candle followed by bullish/green candle at support.
- `Pat 3 รูปแบบที่ 1`: bearish/red candle, then a very small middle candle/rejection structure near support, then bullish/green candle.
- `Pat 3 รูปแบบที่ 2`: bearish/red candle, then smaller bearish/red candle near support, then bullish/green candle.
- `Pat 3 รูปแบบที่ 3`: bearish/red candle, then smaller bullish/green candle, then larger bullish/green continuation/confirmation candle.

## Visible SELL pattern topology

The SELL row is the directional mirror of the BUY row at resistance:

- `Pat 1`: one bearish/red rejection-style candle at resistance.
- `Pat 2`: bullish/green candle followed by bearish/red candle.
- `Pat 3 รูปแบบที่ 1`: bullish/green candle, small middle rejection/transition candle near resistance, then bearish/red candle.
- `Pat 3 รูปแบบที่ 2`: bullish/green candle, then smaller bullish/green candle, then bearish/red candle.
- `Pat 3 รูปแบบที่ 3`: bullish/green candle, then smaller bearish/red candle, then larger bearish/red continuation/confirmation candle.

## Post-SIG wick counting — direct text on slide

The slide explicitly states:

- `Pat 1 นับแท่งที่ 2`
- `Pat 2 นับแท่งที่ 3`
- `Pat 3 นับแท่งที่ 4`

The examples titled `ตัวอย่าง การนับไส้หลัง Sig` show a dashed outline immediately after the pattern. This materially clarifies that the post-SIG wick/reference candle is counted **after** the pattern itself:

- PAT1 pattern candle(s) -> reference/post-SIG candle is candle #2.
- PAT2 -> reference/post-SIG candle is candle #3.
- PAT3 (all shown variants) -> reference/post-SIG candle is candle #4.

This is stronger and more general than the earlier single example that only established PAT2 candle #3.

## System-context text visible on slide

The lower slide text states that these are examples of PA / SIG sets for observing price movement and that, when formed at support, the context is BUY; when formed at resistance, the context is SELL. It also gives H1 = 1,000 points as a run-count example.

## What this evidence closes

- Five visible PA shapes are now identified at the topology level.
- PAT1 / PAT2 / PAT3 family structure is materially clearer.
- PAT3 has three explicit visual variants.
- BUY/SELL mirror structure is directly shown.
- Post-SIG reference-candle index is directly shown for PAT1, PAT2 and PAT3.
- Prior hypothesis `PAT1–PAT5 are five separately numbered families` is now conflicting with stronger primary visual evidence.

## What remains unresolved before deterministic OHLC coding

1. Exact body-size ratios for each pattern.
2. Exact wick-length requirements.
3. Exact close/open relations (e.g. whether Pat2 must close above/below 50% of prior body).
4. Whether engulfing of body or high/low is required.
5. Tolerance to the support/resistance line: exact touch, wick penetration, body close, or distance buffer.
6. Exact definition of the small middle candle in PAT3 variant 1.
7. Whether PAT3 variants 2/3 require monotonic body-size relationships or only color/order topology.
8. Pattern invalidation rules.
9. Whether the post-SIG reference candle itself must satisfy color/body conditions before its wick can be used.
10. Negative examples that look similar but must be rejected.

## Engineering consequence

Safe now:

- Replace generic `PAT1..PAT5` placeholders with a model that can represent `PAT1`, `PAT2`, and `PAT3.variant in {1,2,3}` while preserving backward compatibility aliases until all old notes are migrated.
- Store `post_sig_reference_index`: PAT1=2, PAT2=3, PAT3=4 as source-backed metadata.
- Build topology-only candidate detectors for replay labeling, but mark them `CANDIDATE_ONLY` until geometry thresholds are recovered.

Not safe yet:

- production `detect_PAT*()` decisions from OHLC;
- assumed 50% body formulas;
- fixed wick/body percentages;
- automatic live-entry decisions.
