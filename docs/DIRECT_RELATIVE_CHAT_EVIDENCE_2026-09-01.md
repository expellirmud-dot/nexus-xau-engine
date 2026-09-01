# Direct Relative Chat Evidence — 2026-09-01

Scope: direct chat excerpts and screenshots supplied by the project owner in the current conversation. Evidence class: Level A where the relative explicitly states system rules or environment details. This file intentionally omits account identifiers and personal data.

## 1. Target instrument / broker environment

Direct relative/user chat establishes:

- instrument in scope is `XAUUSD` only;
- `XAUUSDc` is explicitly not the intended symbol;
- platform is MT5 / Exness environment;
- relative screenshot shows Standard Cent, Exness Technologies Ltd, server `Exness-MT5Real36`;
- relative cautions that server assignment can differ between accounts because the server may be assigned at registration;
- account denomination can be USD; the relative currently uses a cent-style account.

Separate MT5 specification screenshot supplied by the project owner shows for an XAUUSD environment:

- Digits = 2
- Contract size = 100
- Tick size = 0.01
- Tick value = 0.1
- Chart mode = Bid
- Execution = Instant
- Stops level = 0

Project implication:

- in that shown specification, 1 point = 0.01 price units;
- however these values must remain broker/account-environment metadata, not universal constants for every Exness server/account.

## 2. Half retrace (`พักครึ่ง`) — direct relative rule

Relative statement, preserved conceptually:

- if a timeframe runs beyond its own normal run (example: H1 normal 1,000 points but price runs 4,000+), measure from the post-SIG wick of the SIG set that drove the move to the furthest/extreme wick, then divide the range by two.

Working formula:

```text
HALF_START = post_SIG_wick_of_driver_SIG
HALF_END   = furthest_extreme_wick
HALF_MID   = midpoint(HALF_START, HALF_END)
```

Classification condition from the same relative explanation:

- in an upward example, `พักครึ่ง` is associated with an opposite `PA Sell` driving the pullback.

Important clarification:

- the price does not have to touch the midpoint exactly; 50% is a reference/calculated level, not a mandatory exact touch.

## 3. Swing retrace (`พักสวิง`) — direct relative rule

Relative statement, preserved conceptually:

- after a timeframe overruns its own normal run, in an upward example measure from the wick of a qualifying green candle to the highest wick, then divide by two to obtain the swing-retrace point.

Working formula:

```text
SWING_START = wick_of_qualifying_same_direction_candle
SWING_END   = furthest_extreme_wick
SWING_MID   = midpoint(SWING_START, SWING_END)
```

Classification distinction supplied directly by the relative:

- `พักครึ่ง`: post-SIG wick -> extreme, with opposite PA driving the pullback;
- `พักสวิง`: qualifying candle wick -> extreme, without the opposite PA driving the pullback.

Still unresolved:

- exact rule for selecting the qualifying same-direction candle when multiple candidates exist;
- when the extreme is considered fixed;
- exact entry / invalidation / SL / TP mechanics after the reference is calculated.

## 4. Primary SIG trading timeframes

Direct relative statement:

`ที่ใช้แน่ๆคือเทรดSIG h1 h4 d w`

Therefore the primary SIG trading set is:

- H1
- H4
- D1
- W1

The relative also separately names key frame/setup families:

- Sideway frame (SW)
- ATH frame
- daily frame

M5/M15/M30 remain confirmation/break/entry-relationship timeframes unless a later primary source explicitly upgrades them to primary SIG trading timeframes.

## 5. PAT2 / post-SIG anchor — direct labeled example

Relative explanation of a supplied `PA Buy PAT2` example:

- the red-circled point is the starting point for run counting;
- candle #3 is the `แท่งไส้หลัง SIG` for that shown PAT2 example;
- that wick is used for:
  - run-count anchor,
  - check/reference point,
  - SL reference.

Canonical abstraction for the shown case:

```text
PAT2_BUY.candle_3 -> post_SIG_wick -> SIG_RUN_ANCHOR
```

Do not generalize candle #3 to PAT1, PAT3, PAT4 or PAT5 without direct evidence.

## 6. PA location / body collection prerequisites

Direct relative/user rule:

- PA Buy must occur at support;
- PA Sell must occur at resistance or at a frame/area where the TP run is complete;
- after PA forms, there is an additional body-collection process before entry logic is complete.

Current high-level sequence remains:

```text
LOCATION / FRAME
-> PA / PAT
-> BODY COLLECTION / RETEST
-> SIG / POST-SIG WICK
-> ENTRY CONDITIONS
-> RUN / TP
```

## 7. Evidence interaction with existing teaching slides

The direct chat is consistent with the previously supplied Level-A teaching images that state:

- H1 run = 1,000 points;
- H4 run = 1,500 points at 100%, with continuation references toward 3,000;
- Day = 5,000–10,000;
- Week = 15,000–30,000;
- Month = 30,000–50,000;
- run counting is anchored from the post-SIG wick;
- entry should be close to frame (<=200 points in the illustrated setup);
- M5 breaks first, with M15/M30 same-direction relationship;
- Sideway is a separate setup family and nominal TP completion alone is not a reversal signal because `Over รอบ` can occur.

## 8. What this evidence closes vs does not close

### Strongly closed / strengthened

- target instrument = XAUUSD only;
- primary SIG TF set = H1/H4/D/W;
- half vs swing conceptual classification;
- midpoint mathematics for both retrace types once anchors are supplied;
- 50% is not a mandatory exact-touch trigger;
- PAT2 Buy example: candle #3 supplies post-SIG run anchor / check / SL reference;
- PA Buy/Sell location prerequisites.

### Still open / coding blockers

- exact PA detector;
- exact PAT1–PAT5 OHLC definitions;
- exact qualifying candle selection for swing retrace;
- exact opposite-PA detector used for half classification;
- exact M5 break geometry;
- exact Sideway frame-complete / false-break rules;
- exact body-collection completion event;
- exact Fib-level usage beyond the midpoint;
- full H1/H4/D/W conflict matrix;
- universal vs setup-specific SL buffer;
- Real36 XAUUSD symbol specification verification for live-equivalent calculations.

## 9. Engineering consequence

Safe to implement now as evidence-tagged primitives:

```text
classify_retrace_candidate(overrun, opposite_pa_present)
compute_half_midpoint(post_sig_wick, extreme)
compute_swing_midpoint(qualifying_wick, extreme)
store_sig_run_anchor(pat2_buy_candle3_wick)
validate_primary_sig_tf(tf in {H1,H4,D1,W1})
```

The detector functions that create those inputs must remain placeholders until dedicated PAT/PA/Sideway/Entry source material closes them.
