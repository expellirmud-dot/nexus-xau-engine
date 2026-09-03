# PAT Geometry Sensitivity Research — 2026-09-03

Status: RESEARCH VARIANTS / NOT A SIGNAL / NOT A WIN-RATE BACKTEST

## Purpose

Continue from the 2026-09-02 PAT color-topology scan without inventing unresolved PAT rules.

The prior scan counted 8,290 PAT2/PAT3 color-topology hit records in the 2026-08-24 to 2026-08-28 sample. This research stage asks two narrower questions:

1. How many topology candidates survive the user-direct directional `>50%` close relation if the unresolved 50% reference is tested under both explicit research variants: `BODY` midpoint and `FULL_RANGE` midpoint?
2. How sensitive PAT3 counts are to explicit research sweeps for candle #2 small-body and PAT3 SELL equal-wick tolerances.

No research variant below is promoted to a production rule.

## Data expansion and validation

A longer XAUUSDm M1 sample was exported directly from the local MT5 terminal:

```text
2026-08-03T00:00:00+00:00
-> 2026-09-01T23:59:00+00:00
M1 bars = 30,308
```

The range was deliberately aligned to complete UTC resample boundaries. Local M1 aggregation was compared with MT5 native bars:

```text
M5: local=6072 mt5=6072 mismatches=0 max_diff=0
H1: local=506  mt5=506  mismatches=0 max_diff=0
H4: local=136  mt5=136  mismatches=0 max_diff=0
D1: local=26   mt5=26   mismatches=0 max_diff=0
```

This removes the partial-boundary mismatch seen in an earlier Aug-01 to Sep-02 export attempt.

## Topology baseline — one month

```text
M1: PAT2 BUY=7684 SELL=7683 | PAT3 BUY=7556 SELL=7557
M5: PAT2 BUY=1498 SELL=1499 | PAT3 BUY=1516 SELL=1517
H1: PAT2 BUY=123  SELL=123  | PAT3 BUY=123  SELL=123
H4: PAT2 BUY=32   SELL=32   | PAT3 BUY=32   SELL=32
D1: PAT2 BUY=8    SELL=8    | PAT3 BUY=3    SELL=4
```

Total topology hit records: `37,153`.

These are overlapping research hit records, not valid PATs or trades.

## >50% midpoint sensitivity

Across all PAT2/PAT3 topology hit records in the month sample:

```text
BODY midpoint pass       = 24,240 / 37,153 = 65.24%
FULL_RANGE midpoint pass = 24,001 / 37,153 = 64.60%
```

The aggregate pass rate looks similar, but candidate-level agreement is not identical:

```text
BODY vs FULL_RANGE classification disagreement = 3,603 / 37,153 = 9.70%
```

For comparison, the original five-day sample produced:

```text
BODY midpoint pass       = 5,368 / 8,290 = 64.75%
FULL_RANGE midpoint pass = 5,326 / 8,290 = 64.25%
BODY vs FULL_RANGE disagreement = 756 / 8,290 = 9.12%
```

### Finding

The expanded month sample is directionally consistent with the five-day sample: aggregate survival is around 65%, while roughly 9–10% of individual topology records change classification depending on whether 50% means body midpoint or full-range midpoint.

Therefore the midpoint-basis gap is materially important for individual PAT labeling even though aggregate counts appear close. Historical frequency alone does not justify choosing one basis over the other.

## PAT3 small-body sensitivity

Research sweep only:

```text
small body = abs(close-open) / (high-low) <= threshold
thresholds tested = 0.10, 0.20, 0.30, 0.40, 0.50
```

Selected month result using the `BODY` midpoint research variant and a `0.30` small-body threshold:

```text
M1 PAT3 BUY: 1,713 candidates
M5 PAT3 BUY:   336 candidates
H1 PAT3 BUY:    22 candidates
H4 PAT3 BUY:     5 candidates
```

The numeric `0.30` is not a system rule. It is only one sensitivity point.

## PAT3 SELL equal-wick sensitivity

Research definition:

```text
upper_wick = high - max(open, close)
lower_wick = min(open, close) - low
equal_wick_error = abs(upper_wick - lower_wick) / full_range
```

Selected month result using `BODY` midpoint plus `small_body <= 0.30`:

```text
              wick_error <=0.10   <=0.20   <=0.30
M1 PAT3 SELL          239           481      719
M5 PAT3 SELL           50            94      144
H1 PAT3 SELL            2             8       10
H4 PAT3 SELL            2             3        3
```

### Finding

The equal-wick tolerance is a strong discriminator. Candidate counts change substantially as the tolerance moves. Therefore selecting a numeric equal-wick threshold from convenience or frequency would materially alter the detector and would be unsupported by current evidence.

## What this research now establishes

Facts measured from the validated MT5 sample:

- the original five-day topology-frequency result was not an obvious one-week anomaly;
- adding a strict >50% test removes roughly one-third of color-topology hit records under either tested midpoint basis;
- BODY and FULL_RANGE midpoint variants produce similar aggregate survival rates but disagree on about one in ten individual topology records;
- PAT3 small-body and especially SELL equal-wick thresholds can sharply change candidate counts.

## What this research does NOT establish

It does not establish:

- which midpoint basis is the true teaching rule;
- the correct small-body threshold;
- the correct equal-wick tolerance;
- support/resistance location qualification or its tolerance;
- PAT1 numeric geometry;
- SIG/post-SIG validity;
- entry, SL, TP, or trade outcome;
- win rate or profitability.

A valid strategy-result calculation is still blocked by the hard rule `BUY PA/PAT at support only / SELL PA/PAT at resistance only` because the exact support/resistance construction/tolerance required by the system is not deterministic yet. Choosing a generic local-high/local-low formula would be an analyst invention and is intentionally not done here.

## Files produced

```text
src/nexus_xau/research/pat_geometry_sensitivity.py
src/nexus_xau/research/summarize_sensitivity.py
results/XAUUSDm_PAT_geometry_sensitivity_2026-08-24_2026-08-28.json
results/XAUUSDm_PAT_geometry_sensitivity_2026-08-03_2026-09-01.json
results/XAUUSDm_PAT_topology_2026-08-03_2026-09-01.json
results/XAUUSDm_PAT_topology_hits_2026-08-03_2026-09-01.csv
results/XAUUSDm_MT5_resample_validation_2026-08-03_2026-09-01.json
data/raw/XAUUSDm_M1_MT5_2026-08-03_2026-09-01.csv
```

## Validation

- new research scanner: Ruff passed;
- existing project tests: 21/21 passed when pytest temporary output was redirected inside the approved project folder;
- month M1 resample vs native MT5: exact M5/H1/H4/D1 match, zero OHLC mismatches.

## Next evidence gate

The highest-value next step is not to optimize these numeric variants against price outcome. It is to obtain/label direct examples that resolve or constrain:

1. support/resistance location construction and tolerance;
2. PAT midpoint basis;
3. PAT3 small-body threshold;
4. PAT3 SELL equal-wick tolerance;
5. PAT1 numeric geometry.

After those are evidence-backed, the same replay pipeline can calculate valid PAT frequency and then proceed to SIG/outcome measurement without redefining the method during backtest.
