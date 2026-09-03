# Direct User Clarification — Multi-Timeframe PA Alignment Strength — 2026-09-03

Status: USER-DIRECT CLARIFICATION / MVP ENTRY-CONFLUENCE SEMANTICS

## Context

Previous relative guidance said, in substance:

`พอ07.00 น. H1 30 15 5 ปิด PA buy กดเข้าออเดอร์แถวกรอบวันได้เลย`

This left a material ambiguity: whether one timeframe was enough, all listed timeframes were mandatory, or the timeframes represented a graded alignment hierarchy.

The project owner then clarified directly:

> หลายtf ไปในทางเดียวกันยิ่งดี

## Safe interpretation

For the listed entry timeframes H1 / M30 / M15 / M5:

- alignment is **graded confluence**, not an all-or-nothing requirement established by this clarification;
- more timeframes pointing in the same direction is preferable / stronger than fewer;
- this clarification does **not** establish a mandatory minimum count (for example, it does not prove that 2 TF are required, or that 1 TF is always sufficient);
- therefore the research engine should measure the count and identity of aligned timeframes rather than hard-code `all four must align`.

## Research representation

For each candidate Daily-Frame entry, record:

```text
pa_buy_or_sell_direction
aligned_h1
aligned_m30
aligned_m15
aligned_m5
aligned_tf_count   # 0..4
aligned_tf_set
```

Then compare outcomes by alignment strength, for example:

```text
1 aligned TF
2 aligned TFs
3 aligned TFs
4 aligned TFs
```

The purpose is to answer whether increasing multi-timeframe agreement materially improves the probability/quality of completing the inherited remaining run.

## Measurement-to-question mapping

```text
Measure: number of H1/M30/M15/M5 PA directions aligned with the inherited SIG direction
Compare: remaining-run completion, MFE, MAE, time-to-target and adverse excursion
Question closed: does stronger multi-timeframe alignment add useful information to the 07:00 Daily-Frame entry?
```

## Production guard

Do not promote a minimum required TF count from historical performance alone. A production threshold still requires source-backed semantics or explicit project approval. Backtest performance may rank variants but cannot turn an unsupported threshold into a canonical trading rule.

## Provenance

This is a direct clarification from the project owner in the ongoing system-decoding conversation. It resolves the prior ambiguity only to the extent stated above: **more same-direction TF alignment is better**. It does not establish an exact mandatory minimum count.
