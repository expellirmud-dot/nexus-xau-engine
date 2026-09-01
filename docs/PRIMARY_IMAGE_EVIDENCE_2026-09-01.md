# Primary Image Evidence Intake — 2026-09-01

Scope: user-uploaded teaching slides/book photos/MT5 screenshots in the current project message. This file records only what is directly visible enough to support project rules. Ambiguous text is left unresolved rather than guessed.

Evidence class: Level A when the image is a direct teaching slide/book page or relative account screenshot supplied by the user.

## 1. Core graph lifecycle — CLOSED at definition level

Direct slide: `หัวใจระบบ วงจรชีวิตกราฟ`

- `SIDEWAY`: SW is price swinging while waiting to break the frame and create a new SIG set.
- `SIG`: SIG is PA occurring at a price frame.
- `TP`: TP is the run from SIG according to the distance of its timeframe.
- `พักตัว`: rest/retrace occurs after the graph completes the run for that timeframe.

Canonical high-level cycle:

`SIDEWAY → SIG → TP → พักตัว → SIDEWAY`

What this closes: state names and teaching meanings.

What it does not close: exact OHLC/state-transition conditions.

## 2. Por Chon ATH frame — substantially stronger primary evidence

Direct slide: `กรอบ ATH พ่อชล`

Visible rules:

1. Price/graph must run `1,000 points` from the previous ATH frame.
2. Draw the frame at the highest price / High of the highest H4 candle in the stated `19:00–19:00` interval associated with creation of the new ATH from the prior frame.
3. If conditions 1 and 2 are not met, do not create a new ATH frame.
4. Once an ATH frame has been created, continue using it.

Usage statements visible on the slide:

- use as an important support/resistance frame;
- use together with the Mae Pla frame and compare which frame price is closest to;
- the Por Chon ATH frame can be retained as a long-lived reference;
- the Mae Pla statistical frame is used to seek current entry and SL-distance context;
- teaching phrase: Por Chon ATH is `SIG GPS` for large-timeframe cycle navigation, while Mae Pla statistical frame is the starting point for trade entry.

Still unresolved:

- precise timezone mapping of `19:00–19:00` to MT5 server time;
- exact candle-selection tie breakers when several H4 highs qualify;
- exact retirement/replacement behavior after later ATH events;
- exact confluence priority when Por Chon and Mae Pla frames are near each other.

## 3. Daily 1,000-point frame — formula is now materially supported

Direct book photos: `กรอบวัน 1,000 จุด` / `วิธีตีกรอบวัน`

Visible rules/concepts:

- Daily frame contains three lines: minor support/resistance, upper frame, lower frame.
- The teaching refers to the H4 candle context around `07:00`.
- Method page visibly states:
  1. use the market/opening price at `07:00`, timeframe H4;
  2. use the nearby statistical price/line whose price ending is `0` or `5` as the minor support/resistance reference;
  3. move upward `500 points` for the upper frame;
  4. move downward `500 points` for the lower frame.
- Thus the daily outer-frame spacing is `1,000 points` from lower to upper around the selected minor/statistical reference.
- Another teaching page says H4 wick-end contacts within approximately `7–14 points` mark a strong frame.

Important caution:

Some small printed fragments in the photo are not perfectly legible. Do not infer additional rounding/tie-break logic beyond the four visible numbered steps until a clearer scan is available.

Implementation candidate once timezone/rounding is verified:

```text
open_0700_h4 -> nearest valid statistical reference ending 0/5
upper = reference + 500 points
lower = reference - 500 points
```

## 4. Daily preparation / frame setup — strong primary evidence

Direct teaching slide: `การเตรียมความพร้อมในการเข้าตลาดในแต่ละวัน`

Visible rules:

- At `07:00`, Day, H4 and H1 candles should be completed.
- Draw H4 wick-end frame: upper first, then lower, using the `1,000-point` principle.
- H4 wick tips touching within `7–14 points` are described as strong-frame contact.
- Draw minor support/resistance around every `500 points` using H1 wick tips with `7–14 point` contact as well.
- Check whether the candle structure forms the system's SIG pattern.
- If there is no PA/SIG set yet, use the frame first and follow the separate entry-condition rules.
- The `1,000-point` frame is described as a directional-entry principle; `SL ตามแผน`, `TP ตามระบบ`.
- U.S. session is described as highly volatile; H4 wick frame is difficult to break; teaching emphasizes staying close to the frame, with a `200-point` proximity reference.

## 5. Entry conditions — strong primary evidence, exact break geometry still open

Direct slide: `เงื่อนไขการเข้าออเดอร์`

Visible rules:

1. `ชิดกรอบ`: distance no more than `200 points`.
2. `PA M5` breaks price first; M15 and M30 must move in the same direction — described as timeframe relationship.
3. Once M5 breaks, entry can be taken. Do not casually add orders during the run because M15 often retraces; if adding, portfolio/risk management is required. The slide warns against adding around the M5 break at `100–200 points`.
4. When M5/M15/M30 PA are in the same direction, this is a level of run confirmation.
5. If H1 completes with PA in the same direction as the smaller TFs, confidence that price will run in that direction increases.
6. When H1 forms PA in SIG form, use the post-SIG wick to count the run and define TP.

Additional visible note:

- price may pierce support/resistance but by no more than around 200 points; an M5 break may still be usable if the graph cycle supports that direction.
- each TF run is measured from the `ไส้หลัง SIG`.
- good SIG should occur as close to the frame as possible.

Still unresolved:

- whether `M5 break` is wick breach, body breach, or candle close beyond the frame;
- exact metric for M15/M30 `same direction`;
- whether the <=200-point proximity applies to every setup family or the frame-entry setup shown.

## 6. Run-distance / TP table — now directly image-supported

Direct teaching slide:

- H1 = `1,000 points`
- H4 = `1,500 points (100%)` with reference toward `3,000 points`
- Day = `5,000` to `10,000 points`
- Week = `15,000` to `30,000 points`
- MN = `30,000` to `50,000 points`

The diagram explicitly labels the run-count line at the end of the post-SIG wick (`ปลายไส้ราคาแท่งไส้หลัง Sig`).

The same diagram shows `SL 300 points` below that line for a `PA buy pat3` example at support.

Interpretation discipline:

- TP/run distances above are direct teaching evidence.
- `300-point SL` is confirmed as an example on this PAT3 illustration, but is NOT proven universal.
- PAT3 Buy is shown at support, but the image does not provide a complete deterministic PAT3 OHLC definition.

## 7. February 2569 entry slide — Sideway / over-round evidence improved

Direct teaching slide: `เงื่อนไขการเข้าออเดอร์ กุมภาพันธ์ 2569`

### Daily Range

- candle body standing above the daily frame -> consider Buy or check for pending SIG;
- candle body closing below the daily frame -> consider Sell or check for pending SIG;
- graph cycle must be considered every time.

### SIG

- wait for a clear SIG first, then find an entry only according to system conditions.

### Sideway

- wait until the SW frame has been fully formed;
- PA confirms the post-SIG wick on both sides, Buy and Sell;
- then plan orders according to the prescribed rules.

### Counter-trend prohibition / Over-round

- do NOT counter-trade merely because a timeframe completed its nominal TP/run; the chart may run beyond the normal round (`Over รอบ`).
- if counter-trading is necessary, wait for a clearly formed `แท่งเบรก = หยุด` or an opposite reversal SIG.

What this closes:

- Sideway is a distinct setup family, not simply `do nothing`;
- completion of nominal TP is not itself a reversal signal;
- opposite reversal requires additional explicit evidence.

What remains open:

- exact SW frame-construction geometry;
- exact meaning of `กรอบ SW เกิดครบ`;
- exact sequence/requirements of the two-side PA confirmations;
- exact `แท่งเบรก = หยุด` OHLC definition.

## 8. Broker / environment evidence

Direct account screenshot:

- Standard Cent
- Exness Technologies Ltd
- server `Exness-MT5Real36`

This strengthens confidence that the relative's reference environment is Exness MT5 Real36 Standard Cent. Exact XAUUSD symbol specification for that live server still must be fetched separately before point-value assumptions are treated as live-equivalent.

## 9. Public-channel evidence

Direct YouTube app screenshot:

- Channel: `UNLOCK TRADER`
- handle: `@Unlocktrader007`
- description visible: `ระบบเทรดแม่ปลาปากกาเขียว`
- visible lessons include:
  - current graph-cycle analysis + recap order;
  - sideway-frame trading conditions;
  - graph cycle and timeframe relationship;
  - Por Chon frame + half/swing retrace conditions.

This strengthens source attribution but does not replace transcript-level extraction.

## 10. Uploaded markdown summaries — QUARANTINE / hypothesis sources

Two user-uploaded markdown files were reviewed:

- `backtes-replay-engine.md`
- `PA-PAT-SIG.md`

They contain useful research hypotheses and proposed implementation structures, but also contain mixed-source / secondary claims that conflict with the project's evidence discipline. Examples that must NOT be promoted to production rules without Level A/B confirmation include:

- PAT1 body <=50% single-bar formula;
- PAT2 fixed 2-bar or 3-bar formula and fixed 50% logic as universal;
- PAT3 generic move-consolidation-confirm formula;
- generic fixed gap <=$5 for PATs;
- generic `close beyond frame` breakout definition;
- generic RR 1:1/1:2 TP management;
- 10–30 point universal SL buffer;
- midpoint values substituted for the documented run ranges;
- generic H4 HH/HL trend hierarchy replacing the system's own cycle/frame rules.

These markdowns should be used as analyst notes / candidate tests only, not truth labels.

## 11. Net effect on coding readiness

Primary-image evidence materially closes:

- core cycle definitions;
- daily-frame formula at a practical first-pass level;
- Por Chon ATH construction prerequisites;
- run-distance table;
- entry workflow around <=200-point frame proximity and M5/M15/M30/H1 relationship;
- Sideway/Over-round high-level handling;
- broker/server attribution.

Still blocking deterministic strategy implementation:

- exact PA/PAT1–PAT5 OHLC definitions;
- exact M5/frame-break geometry;
- exact Sideway frame-completion and breakout state machine;
- exact body-collection `pair` geometry and consumed event;
- exact half/swing/Fibonacci entry/invalidation mechanics;
- full multi-TF conflict matrix;
- universal-vs-setup-specific SL logic;
- ground-truth labeled examples.
