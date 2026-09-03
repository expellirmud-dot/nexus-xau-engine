# Win/Loss Proof Protocol — NEXUS XAU Research — 2026-09-03

Status: ACTIVE RESEARCH PROTOCOL

Purpose: define a reproducible path from historical XAU price data to defensible Win rate / Loss rate / expectancy and state-specific handling without silently converting incomplete PAT/SIG rules into trading claims.

## 1. Two different questions must never be merged

### A. SIGNAL/RUN SUCCESS

Question:

`After a valid SIG exists, does price complete the source-defined run from the post-SIG anchor?`

Examples of source-backed run references currently recorded:

- H1 = 1,000 project-reference points;
- H4 = 1,500 project-reference points at the first/full round;
- D1 = 5,000 project-reference points for the first documented distance.

This is a signal-behavior statistic. It is NOT a trade win rate unless entry, stop/invalidation, costs, and execution timing are also defined.

### B. TRADE WIN/LOSS

Question:

`If the system would actually enter at a source-backed entry event, what happens before the source-backed exit/invalidation event?`

A canonical trade win rate requires all of these to be frozen before outcome is inspected:

1. valid setup label;
2. entry time and price;
3. SL/invalidation rule;
4. TP/exit rule;
5. re-entry / replacement rules;
6. spread/slippage/cost model;
7. handling when TP and SL are touched inside the same available OHLC bar.

Current project evidence is not yet sufficient to claim canonical trade Win/Loss because exact entry/SL/invalidation remains incomplete.

## 2. Unit normalization — critical

Current local MT5 query on 2026-09-03 returned for `XAUUSDm`:

```text
digits = 3
MT5 point = 0.001
trade_tick_size = 0.001
trade_tick_value = 0.1
contract_size = 100
```

Existing project teaching examples use a reference interpretation of `0.01 USD` per project point in the earlier XAUUSD environment. Therefore:

```text
BROKER_POINT_XAUUSDm = 0.001
PROJECT_REFERENCE_POINT = 0.01
```

These must not be silently substituted for each other.

Research reports should prefer absolute price distance in USD and, when useful, convert to explicitly named `project_reference_points` using 0.01. Broker P/L calculations must use runtime symbol specification separately.

## 3. No-lookahead rule

Every event must store:

```text
reference_price
reference_source
known_at
outcome_start
```

The engine may use a historical reference only after the time it became knowable.

Example for a post-SIG wick candidate:

- pattern completes;
- next timeframe candle is the post-SIG reference candidate;
- its final low/high is known only after that candle closes;
- forward trade-style scoring must not use future data before `known_at`.

Signal-run research may separately reconstruct what happened inside the post-SIG candle, but this must be reported separately from trade-after-confirmation results.

## 4. OHLC ambiguity rule

If the same available M1 bar touches both the favorable barrier and adverse barrier, the order is unknown without tick data.

Required classification:

```text
TARGET_FIRST
STOP_FIRST
AMBIGUOUS_SAME_BAR
NEITHER
```

Never force an ambiguous bar into Win or Loss.

If later tick data is available, ambiguous cases can be re-resolved under a new dataset version.

## 5. Outcome measurements required per event

The outcome engine now supports:

- MFE = maximum favorable excursion;
- MAE = maximum adverse excursion;
- end-of-horizon directional return;
- first target touch;
- first adverse/stop touch;
- same-bar ambiguity;
- no-lookahead `known_at` boundary.

Future canonical trade records should additionally store:

- entry price;
- spread at entry;
- SL price;
- TP price(s);
- exit reason;
- realized points/USD/R;
- time to TP/SL;
- MFE before exit;
- MAE before exit;
- setup/state tags.

## 6. Why target-reach rate alone is invalid as Win rate

A negative-control baseline on the current one-month sample showed that topology-only events often reached the source run distance within the research horizon in both BUY and SELL directions.

This occurs because gold can travel through large distances in both directions during the horizon. Therefore:

```text
"target was touched sometime" != "trade won"
```

At minimum, first-hit ordering relative to an adverse/invalidation level is required.

## 7. Negative controls are mandatory

Before claiming edge, every candidate rule must beat controls that preserve market volatility but remove the claimed informational content.

Current controls:

### Topology-only control

Uses PAT2/PAT3 candle-color topology with no valid S/R, no final 50% basis, no PAT3 final thresholds, and no post-SIG validity.

Purpose: prove that the outcome pipeline itself can run and show how misleading raw target reach can be.

### Matched opposite-direction control

For the exact same event timestamp and post-SIG candle:

- evaluate stated topology direction;
- evaluate opposite direction;
- use corresponding wick extreme for each direction;
- compare equal-distance first-hit behavior.

Current one-month result does not show a consistent topology-only directional advantage: H1 PAT2 and H4 PAT2/PAT3 are similar to or worse than the matched opposite direction, while H1 PAT3 shows only a small positive difference. This is evidence against treating topology-only frequency as proof of edge.

Required future controls:

- randomly sampled matched timestamps;
- shuffled direction labels;
- non-overlapping-event sensitivity;
- day/week clustered resampling;
- out-of-sample period.

## 8. Event dependence / overlap

PAT windows overlap by design. Therefore 100 overlapping events are not necessarily 100 independent observations.

Required reporting layers:

1. raw event-level rate;
2. non-overlapping-event sensitivity;
3. cluster by trading day/week;
4. confidence intervals using clustered or block bootstrap where appropriate.

Do not report a narrow confidence interval from overlapping rows as if they were independent Bernoulli trials.

## 9. Train / validation / test separation

Numeric rules must not be chosen by maximizing outcome on the same period used to report performance.

Recommended research sequence:

```text
Evidence rules frozen first
-> development/train period
-> parameter sensitivity only where source leaves a parameter open
-> validation period
-> final untouched test period
-> walk-forward / regime checks
```

If a threshold is selected because it produced the best historical Win rate, it becomes an analyst-fitted rule and must not be presented as the original teaching rule.

## 10. Minimum metrics for a defensible result

### Signal/run layer

- number of valid SIGs;
- run target completion rate;
- time-to-run distribution;
- MFE / MAE distributions;
- invalidated post-SIG rate;
- replacement/re-anchor rate;
- Over-round frequency;
- state after failed SIG.

### Trade layer

- trades;
- wins;
- losses;
- ambiguous/unresolved;
- Win rate;
- Loss rate;
- average win;
- average loss;
- expectancy;
- profit factor;
- median and tail MAE;
- median and tail MFE;
- maximum consecutive losses;
- drawdown under a fixed sizing model;
- performance by timeframe/setup/state;
- confidence interval / out-of-sample consistency.

A high Win rate alone is not sufficient if average loss dominates average win.

## 11. State-specific handling framework

Only source-backed system states should be used as canonical labels.

Current high-level state map:

```text
CANDIDATE_PA
-> VALID_PA or WRONG_LOCATION/INVALID
-> CANDIDATE_SIG
-> SIG_ACTIVE or INVALIDATED_BY_POST_SIG
-> RUNNING
-> TP_COMPLETE
-> OVERRUN or RETRACING
-> HALF_RETRACE / SWING_RETRACE / SIDEWAY / NEW_SIG
```

Current evidence-backed handling principles:

- Wrong-location PA: reject as valid PA.
- Open candle: wait for close.
- Invalid post-SIG wick that disturbs/exceeds PA: invalidate original SIG, reassess sideway/new PA; do not keep counting the original signal as active.
- TP complete: do not automatically countertrade; Over-round can continue.
- Overrun + opposite PA: candidate HALF retrace classification.
- Overrun without opposite PA: candidate SWING retrace classification, but swing-anchor selection remains open.
- Body-collection setup inside Sideway: do not apply blindly; Sideway is a separate setup family.
- New valid PA after invalidation: replacement/re-anchor is required rather than retaining the dead anchor.

Exact algorithmic triggers for several transitions remain unresolved and must stay HUMAN_CONFIRM/PARAMETERIZED until primary evidence closes them.

## 12. Current data status

Validated price dataset available in repo:

```text
XAUUSDm M1
2026-08-03T00:00:00Z -> 2026-09-01T23:59:00Z
30,308 M1 bars
M5/H1/H4/D1 resample vs native MT5 = 0 mismatches
```

Current repo contains price data and research event files. It does not currently contain a saved broker deal/order-history dataset for this period.

Therefore current work can prove price/event behavior, but canonical realized trade Win/Loss requires either:

- fully source-backed replay entry/exit rules, or
- verified historical deal records generated by the same system rules.

## 13. Claim standard

A result may be called `SYSTEM WIN RATE` only when:

1. setup rules are source-backed and version-frozen;
2. S/R/location qualification is deterministic or externally labeled before outcome review;
3. post-SIG validity is deterministic;
4. entry and loss/invalidation rules are fixed;
5. execution/cost assumptions are stated;
6. ambiguous bars are handled explicitly;
7. sufficient sample exists by relevant timeframe/state;
8. result survives an out-of-sample or walk-forward check;
9. matched/random controls do not explain the apparent edge.

Until then, report only named research statistics such as `target_reach`, `symmetric_first_hit`, `MFE`, `MAE`, or `candidate_run_completion`.
