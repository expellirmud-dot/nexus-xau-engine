# Outcome Negative Control — 2026-09-03

Status: RESEARCH BASELINE / NOT SYSTEM WIN RATE

## Question

Before valid S/R-qualified PAT/SIG labels are available, can the project build a no-lookahead outcome engine and determine whether apparently high target-hit rates are merely a consequence of gold volatility / anchor construction?

## Data

Validated MT5 sample:

```text
symbol: XAUUSDm
UTC: 2026-08-03 -> 2026-09-01
M1 bars: 30,308
resample validation: M5/H1/H4/D1 = 0 OHLC mismatches vs MT5 native bars
```

Input event set:

```text
PAT2/PAT3 COLOR TOPOLOGY ONLY
37,153 total topology rows across all TFs
H1/H4/D1 rows eligible for the run-distance baseline are used here
```

No S/R qualification, final midpoint basis, final PAT3 geometry, or post-SIG-validity rule is applied.

## Unit correction discovered

Local MT5 query on 2026-09-03:

```text
XAUUSDm digits = 3
MT5 point = 0.001
trade_tick_size = 0.001
trade_tick_value = 0.1
contract_size = 100
```

The existing project teaching-reference arithmetic uses `0.01 USD` per project point in the earlier documented XAUUSD environment. The negative-control research therefore keeps the two units separate and uses:

```text
project_reference_point = 0.01 USD
```

for teaching-run comparisons. It does NOT redefine the teaching run as `1000 * 0.001` merely because this broker symbol has three digits.

## Outcome engine created

File:

`src/nexus_xau/research/outcomes.py`

It measures:

- MFE;
- MAE;
- end-of-horizon directional return;
- target first;
- adverse barrier first;
- same-M1-bar ambiguity;
- neither barrier;
- explicit `known_at` to prevent look-ahead.

If one M1 OHLC bar touches both barriers, it is classified `AMBIGUOUS_SAME_BAR`; the engine does not invent an intrabar order.

Full test suite after the outcome engine: `30/30 passed`.

## Candidate post-SIG baseline policy

For this negative control only:

- first timeframe candle after the topology window is treated as a **candidate** post-SIG candle;
- BUY candidate anchor = that candle low;
- SELL candidate anchor = that candle high;
- anchor validity is NOT checked;
- forward scoring begins only after that candidate post-SIG candle has closed;
- movement inside the candidate anchor candle is not scored as future trade movement.

Research horizons are explicit experiment choices, not system rules:

```text
H1: 24 H1 bars
H4: 12 H4 bars
D1: 5 D1 bars
```

Run-distance references use current project evidence:

```text
H1 = 1,000 project points = $10 reference distance
H4 = 1,500 project points = $15 reference distance
D1 = 5,000 project points = $50 reference distance
```

## Result 1 — raw target reach is misleadingly high

Examples from 600 measurable H1/H4/D1 topology events:

```text
H1 PAT2 BUY  reach-any = 98.3%
H1 PAT2 SELL reach-any = 91.4%
H1 PAT3 BUY  reach-any = 94.9%
H1 PAT3 SELL reach-any = 94.0%

H4 PAT2 BUY  reach-any = 96.6%
H4 PAT2 SELL reach-any = 82.8%
H4 PAT3 BUY  reach-any = 100.0%
H4 PAT3 SELL reach-any = 93.3%
```

This is NOT evidence of a 90%+ trading Win rate.

MFE and MAE show why: gold frequently traverses large distances in both directions within these horizons. For example:

```text
H1 PAT2 BUY median MFE = 5,379.8 project points
H1 PAT2 BUY median MAE = 2,269.6 project points

H1 PAT2 SELL median MFE = 4,001.4
H1 PAT2 SELL median MAE = 4,088.3
```

Therefore `target was touched sometime` cannot define Win/Loss.

## Result 2 — symmetric first-hit control

To avoid inventing an SL, a neutral adverse barrier equal to the favorable run distance was added.

This asks:

`Does +run distance get hit before -the same distance?`

It is a directional control, not a trading rule.

Resolved target-first rates:

```text
H1 PAT2 BUY  0.855
H1 PAT2 SELL 0.793
H1 PAT3 BUY  0.872
H1 PAT3 SELL 0.828

H4 PAT2 BUY  0.931
H4 PAT2 SELL 0.690
H4 PAT3 BUY  0.933
H4 PAT3 SELL 0.767
```

These still look high, but the next control shows that anchor construction/time selection can explain much of that apparent success.

## Result 3 — matched opposite-direction control

For every topology event, the same timestamp and same candidate post-SIG candle were evaluated twice:

1. stated topology direction;
2. opposite direction;

Each side used its corresponding wick extreme and the same equal-distance first-hit test.

Results:

```text
H1 PAT2: actual 0.824 | flipped 0.841 | delta -0.017 | n=233
H1 PAT3: actual 0.850 | flipped 0.807 | delta +0.043 | n=233
H4 PAT2: actual 0.810 | flipped 0.897 | delta -0.086 | n=58
H4 PAT3: actual 0.850 | flipped 0.883 | delta -0.033 | n=60
```

D1 results were positive for actual direction but sample size was only 13 PAT2 and 3 PAT3 events, so they are not decision-grade.

## Interpretation

The current evidence does **not** support claiming that PAT2/PAT3 color topology alone creates a robust directional edge.

In three of the four H1/H4 pattern groups above, the matched opposite direction performed similarly or better. H1 PAT3 showed only a small positive difference in this short sample.

This is valuable negative evidence: it demonstrates that a high apparent hit rate can arise even before the hard S/R/PAT/SIG rules are applied.

Therefore the system proof must require the missing qualification layers rather than optimizing color topology against outcome.

## Files produced

```text
src/nexus_xau/research/outcomes.py
src/nexus_xau/research/topology_outcome_baseline.py
src/nexus_xau/research/matched_direction_control.py
tests/test_outcomes.py
results/XAUUSDm_TOPOLOGY_OUTCOME_BASELINE_2026-08-03_2026-09-01.json
results/XAUUSDm_TOPOLOGY_OUTCOME_EVENTS_2026-08-03_2026-09-01.csv
results/XAUUSDm_MATCHED_DIRECTION_CONTROL_2026-08-03_2026-09-01.json
results/XAUUSDm_MATCHED_DIRECTION_CONTROL_EVENTS_2026-08-03_2026-09-01.csv
```

## What this checkpoint proves

- the project can measure future outcome without obvious look-ahead;
- MFE/MAE and first-hit ordering are necessary;
- target reach alone is not Win rate;
- apparent topology-only success does not survive a simple matched control consistently;
- post-SIG run success and realized Trade Win rate must be kept separate;
- exact valid-location / valid-PAT / valid-post-SIG / entry-invalidation rules remain necessary before a system Win rate can be claimed.

## Next checkpoint

1. freeze/expand historical price dataset in monthly chunks if MT5 history is available;
2. continue source-backed PAT-at-S/R interaction research;
3. generate valid-location labels/detectors without looking at outcome;
4. rerun the same outcome/control framework only after labels are frozen;
5. add random-time / shuffled-side and non-overlap controls;
6. once entry + SL/invalidation is closed, calculate actual trade Win/Loss/expectancy by system state.
