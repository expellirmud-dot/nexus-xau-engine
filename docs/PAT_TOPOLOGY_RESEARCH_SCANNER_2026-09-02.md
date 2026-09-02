# PAT Topology Research Scanner — 2026-09-02

Status: RESEARCH ONLY / NOT A SIGNAL

This scanner is the first historical-data use of the deterministic PAT topology layer. Its purpose is to measure how often the currently confirmed candle-color sequences occur in real XAUUSDm data before unresolved geometry and location rules are added.

## Input

A timezone-aware historical M1 OHLC CSV accepted by the project loader. The scanner builds M5, H1, H4, and D1 using the same resampler already validated exactly against MT5 for the first Exness-MT5Trial6 / XAUUSDm sample.

Historical CSV rows are treated as closed candles. This scanner is not a live-candle classifier.

## What is counted

PAT2 BUY color topology:

```text
C1 bearish -> C2 bullish
```

PAT2 SELL color topology:

```text
C1 bullish -> C2 bearish
```

PAT3 BUY color topology:

```text
C1 bearish -> C2 bullish/bearish -> C3 bullish
```

PAT3 SELL color topology:

```text
C1 bullish -> C2 bullish/bearish -> C3 bearish
```

An exact doji in PAT3 candle #2 is excluded because the direct rule states candle #2 is green or red.

Overlapping windows are retained. A region can contribute to more than one candidate window when the candle sequence supports it.

## Deliberately NOT checked

The scanner does not check:

- BUY at support / SELL at resistance;
- support/resistance proximity tolerance;
- PAT2/PAT3 >50% close rule;
- BODY versus FULL_RANGE basis for the 50% reference;
- equality/tolerance around 50%;
- PAT3 candle #2 small-body threshold;
- PAT3 SELL equal-upper/lower-wick tolerance;
- PAT1 long-wick/small-body geometry;
- SIG validity, post-SIG reference, TP/run distance, entry, stop, or outcome.

Therefore a topology hit must never be labeled a valid PAT, trade signal, win, loss, or setup frequency.

## Outputs

The CLI command `scan-pat-topology` can write:

- a JSON summary by timeframe;
- a CSV of every topology hit with timeframe, PAT kind, side, window start, and window end.

The hit CSV is intended for later visual/manual sampling and for comparing future evidence-backed parameterizations.

## Next research use

After this baseline is measured, the same hit set can be filtered under explicitly named research variants, for example BODY-midpoint versus FULL_RANGE-midpoint for the unresolved >50% rule. Neither variant should become production logic until stronger evidence resolves the measurement basis or the project explicitly adopts a tested parameterization.
