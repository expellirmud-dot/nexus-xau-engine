# Analyst Recalibration — Workflow Understanding vs Deterministic Coding Readiness

Date: 2026-09-01

Purpose: reconcile the latest direct relative chat, primary teaching images, MT5 XAUUSD specification, EP.5 transcript review, and prior scorecards.

## Executive conclusion

The newest evidence materially improves system understanding, but two different notions of "readiness" must be separated:

1. **Workflow / conceptual coverage** — how well the project understands the sequence and role of system components.
2. **Deterministic coding readiness** — how much can be converted into exact OHLC/state rules for backtest/replay without inventing missing mechanics.

Latest analyst estimate:

- **Workflow / conceptual coverage: ~70%**
- **Deterministic coding readiness: ~59%**

This resolves the apparent conflict between the prior ~55% score and the latest qualitative assessment of ~65–70%. The system workflow is now understood at roughly that level, but exact detector readiness remains lower because PA/PAT geometry is a central dependency for SIG, entry, Sideway confirmation, retracement classification and run anchoring.

Neither score is a win rate, profit probability, or live-EA readiness score.

---

## Directly strengthened modules

### Broker / XAUUSD

Direct MT5 specification supports the reference environment:

- `XAUUSD`
- Digits = 2
- Contract size = 100
- Tick size = 0.01
- Tick value = 0.1
- Chart mode = Bid
- Calculation = CFD Leverage

For this specification, in price-distance terms:

- 1 point = 0.01 USD
- 200 points = 2 USD
- 500 points = 5 USD
- 1,000 points = 10 USD
- 1,500 points = 15 USD
- 3,000 points = 30 USD

Relative clarified that server assignment may differ between accounts, so broker/company/server/account must be runtime metadata rather than strategy constants.

### Half retrace / Swing retrace

Direct relative evidence materially closes the classification concept.

Common prerequisite:

- the relevant TF has exceeded its own normal run.

Half retrace:

- opposite PA drives the pullback;
- upward example: PA Sell is present;
- start = post-SIG wick of the SIG set that drove the run;
- end = furthest/extreme wick;
- midpoint = reference half-retrace level.

Swing retrace:

- no opposite PA drives the pullback;
- upward example: start from the wick of a qualifying green candle;
- end = highest/extreme wick;
- midpoint = swing-retrace reference.

Critical semantic rule:

- price does **not** have to touch 50%; midpoint is a reference/forecast level, not a mandatory entry condition.

Still unresolved:

- deterministic selection of the qualifying swing-start candle when several same-direction candles exist;
- when an extreme is frozen vs updated dynamically;
- exact post-retrace entry, invalidation and SL/TP mechanics;
- whether Fib 38.2/61.8/extensions are formal rules.

### PAT2 post-SIG anchor

Direct relative example supports only the shown `PA Buy PAT2` case:

- candle #3 = post-SIG-wick candle;
- its relevant wick is the run-count anchor;
- also a check/reference point;
- also an SL reference.

Do not generalize candle #3 to other PAT families.

### Entry / Multi-TF

Primary entry slide directly supports:

`near frame <= ~200 points`
→ `PA M5 breaks price first`
→ `M15/M30 move in same direction`
→ M5/M15/M30 same-direction PA gives one level of confirmation
→ if H1 closes with PA in the same direction, confidence increases
→ if H1 forms PA in SIG form, use post-SIG wick to count run / TP

Also directly supported:

- M5 can pierce S/R by <= ~200 points and still be usable in the intended direction if graph-cycle context supports it;
- do not casually add orders after the M5 break; M15 often retraces.

Still unresolved:

- exact frame line/edge being broken;
- wick vs body vs close criterion;
- whether the PA candle itself can be the break candle;
- exact M15/M30 directional metric.

### Sideway

Primary teaching image gives stronger state semantics:

- wait for SW frame to be complete;
- PA / post-SIG confirmation is expected on both Buy and Sell sides;
- only then plan orders under the system conditions;
- do not counter merely because nominal TP/run is complete, because an Over-round move may continue;
- if countering, wait for a clearly defined break/stop candle or an opposite reversal SIG.

This is stronger than generic `no HH/LL` definitions and should override them.

Still unresolved:

- exact upper/lower frame construction;
- exact meaning of `SW frame complete`;
- sequence/count/tolerance of two-side confirmations;
- true vs false breakout geometry;
- exact `break = stop` candle definition.

### Daily frame / Por Chon ATH

Primary book/slide evidence supports:

Daily frame:

- use 07:00 H4 context;
- select nearby statistical price ending in 0/5 as minor S/R reference;
- +500 points = upper frame;
- -500 points = lower frame;
- total outer spacing = 1,000 points;
- H4/H1 wick-contact context of ~7–14 points is used for strong frame/minor S/R analysis.

Por Chon ATH:

- price must run 1,000 points from the previous ATH frame;
- use the highest H4 price in the stated 19:00–19:00 interval for the new ATH candidate;
- if conditions are not met, no new ATH frame;
- once created, the ATH frame remains in use.

Conflict handling:

- prior mixed/secondary claim of an ATH cutoff around `12:00 UTC` is **UNVERIFIED / CONFLICTING** and must not be used in code because primary teaching evidence now supports the 19:00–19:00 rule wording instead.

Still unresolved:

- exact timezone mapping of the 19:00 boundary;
- exact day-boundary interpretation;
- tie-breaks when several H4 highs qualify;
- exact 0/5 snapping/nearest-price tie rule for the daily statistical line.

### TP / SL

Direct teaching evidence supports run ranges:

- H1 = 1,000
- H4 = 1,500 (100%) toward 3,000
- Day = 5,000–10,000
- Week = 15,000–30,000
- MN = 30,000–50,000

A PAT3 Buy illustration shows SL 300 points away from the post-SIG-wick counting line. This is `example-supported`, not a universal SL rule.

---

## Deterministic coding score

Weighted coding coverage estimate:

| Module | Weight | Coding coverage | Weighted contribution |
|---|---:|---:|---:|
| Broker / symbol / data metadata | 5% | 95% | 4.75 |
| Core cycle / state model | 5% | 90% | 4.50 |
| SIG anchor / run-distance logic | 10% | 90% | 9.00 |
| PA / PAT1–PAT5 definitions | 15% | 20% | 3.00 |
| Body collection | 10% | 65% | 6.50 |
| Sideway state machine | 10% | 45% | 4.50 |
| Half / swing retrace + Fibonacci | 10% | 75% | 7.50 |
| Entry / M5 break execution | 10% | 65% | 6.50 |
| Multi-timeframe relationship | 7% | 50% | 3.50 |
| Por Chon / Mae Pla frame algorithms | 7% | 75% | 5.25 |
| SL / TP / risk mechanics | 5% | 55% | 2.75 |
| Ground-truth labeled examples | 6% | 15% | 0.90 |

Weighted total = **58.65%**

Rounded deterministic coding readiness = **59%**

Remaining deterministic gap = **41%**

---

## Why not score deterministic readiness at 65–70% yet?

Because the missing PA/PAT detector is not an isolated 15% feature. It is a dependency used by:

- SIG qualification;
- post-SIG anchor selection;
- M5 entry confirmation;
- Sideway two-side confirmation;
- half-vs-swing classification via opposite PA;
- body-collection confirmation;
- reversal / invalidation logic.

Therefore raising PA/PAT or dependent modules without exact candle geometry would double-count workflow knowledge as code readiness.

A 65–70% score is reasonable for **workflow understanding**, but not yet for exact OHLC/state implementation.

---

## P0 blockers now

1. `PA exact qualification` and `PAT1–PAT5 exact candle geometry`.
2. `M5 break exact rule` — target edge, wick/body/close, penetration, same-candle sequencing.
3. `Sideway frame construction/completion` and false-break definition.
4. `Swing retrace start-candle selection` and extreme finalization.
5. `Daily statistical 0/5 snapping` exact tie/rounding algorithm.
6. `ATH 19:00 boundary` timezone/day-window exact semantics.
7. body-collection `pair` geometry and exact `CONSUMED` event.
8. positive + negative labeled ground-truth cases.

Secondary unresolved items include universal SL buffers, partial exit/re-entry, D/W conflict rules, and formal Fib-level use.

---

## Current engineering interpretation

### Safe now

- data/broker metadata layer;
- point conversion from runtime symbol spec;
- cycle/state objects;
- run-distance config;
- daily-frame first-pass calculator with unresolved snap/timezone flags;
- Por Chon ATH candidate state machine with unresolved time-boundary flag;
- source-confirmed SIG anchor storage;
- half/swing midpoint calculators and candidate classifier when PA/swing anchor is externally supplied;
- Body Collection / Entry / Sideway state-machine shells;
- replay engine and evidence logging.

### Placeholder interfaces still required

- `detect_PA()`
- `detect_PAT1()` ... `detect_PAT5()`
- `confirm_m5_break()`
- `sideway_frame_complete()`
- `sideway_false_break()`
- `select_swing_retrace_anchor()`
- `detect_pair()`
- `body_collection_completed()`
- exact execution / universal risk logic

Current stage: **~70% workflow understanding / ~59% deterministic coding readiness**.
