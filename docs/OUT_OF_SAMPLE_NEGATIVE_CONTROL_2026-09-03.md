# Out-of-Sample Negative Control — 2026-09-03

Status: NEGATIVE CONTROL / NOT SYSTEM WIN RATE

## Objective

Check whether the topology-only matched-direction result is stable across separate time periods rather than being an artifact of one month.

This test still does NOT use valid S/R-qualified PA/PAT/SIG labels. It is a falsification/control exercise only.

## Expanded validated dataset

MT5 history was successfully expanded in monthly chunks.

Raw availability discovered:

```text
2026-05 history actually starts: 2026-05-25 04:28 UTC
2026-06: available
2026-07: available
2026-08/early Sep: available
```

A consolidated closed-boundary dataset was built:

```text
2026-05-26T00:00:00Z -> 2026-09-01T23:59:00Z
M1 bars = 97,341
```

Native MT5 validation over the full consolidated range:

```text
M5:  local=19,500 | mt5=19,500 | mismatches=0
H1:  local=1,625  | mt5=1,625  | mismatches=0
H4:  local=438    | mt5=438    | mismatches=0
D1:  local=85     | mt5=85     | mismatches=0
```

Therefore the expanded price dataset is suitable for continued research on these timeframes.

## Expanded topology baseline

Across the consolidated period:

```text
M1 PAT2 BUY=24,908 SELL=24,910 | PAT3 BUY=24,448 SELL=24,452
M5 PAT2 BUY=4,936  SELL=4,935  | PAT3 BUY=4,896  SELL=4,895
H1 PAT2 BUY=401    SELL=401    | PAT3 BUY=418    SELL=418
H4 PAT2 BUY=108    SELL=108    | PAT3 BUY=113    SELL=113
D1 PAT2 BUY=23     SELL=23     | PAT3 BUY=20     SELL=20
```

Total topology hit records = `120,546`.

Again: these are overlapping color-topology research rows, not valid signals.

## Full-period matched opposite-direction control

Measured H1/H4/D1 events with sufficient forward horizon: `2,123`.

```text
H1 PAT2 actual=0.810 | flipped=0.815 | delta=-0.005 | n=789
H1 PAT3 actual=0.809 | flipped=0.831 | delta=-0.022 | n=823
H4 PAT2 actual=0.857 | flipped=0.886 | delta=-0.029 | n=210
H4 PAT3 actual=0.847 | flipped=0.874 | delta=-0.027 | n=222
D1 PAT2 actual=0.814 | flipped=0.721 | delta=+0.093 | n=43
D1 PAT3 actual=0.806 | flipped=0.833 | delta=-0.028 | n=36
```

Interpretation:

- H1/H4 topology direction does not beat the matched opposite-direction control on the full sample.
- D1 PAT2 is positive, but D1 sample is much smaller and PAT3 is negative; no general D1 topology claim is justified.

## Time split

The available history was separated conceptually into:

```text
DEVELOPMENT: 2026-05-26 -> 2026-06-30
VALIDATION:  2026-07-01 -> 2026-07-31
TEST:        2026-08-03 -> 2026-09-01
```

The split is for research discipline. No threshold was optimized from these controls.

### Development matched control

```text
H1 PAT2 actual=0.811 | flipped=0.835 | delta=-0.024 | n=285
H1 PAT3 actual=0.779 | flipped=0.876 | delta=-0.097 | n=299
H4 PAT2 actual=0.889 | flipped=0.931 | delta=-0.042 | n=72
H4 PAT3 actual=0.880 | flipped=0.904 | delta=-0.024 | n=83
D1 PAT2 actual=0.818 | flipped=0.727 | delta=+0.091 | n=11
D1 PAT3 actual=0.818 | flipped=0.818 | delta=0.000 | n=11
```

### Validation matched control

```text
H1 PAT2 actual=0.804 | flipped=0.775 | delta=+0.029 | n=240
H1 PAT3 actual=0.806 | flipped=0.795 | delta=+0.011 | n=263
H4 PAT2 actual=0.833 | flipped=0.848 | delta=-0.015 | n=66
H4 PAT3 actual=0.781 | flipped=0.859 | delta=-0.078 | n=64
D1 PAT2 actual=0.556 | flipped=0.556 | delta=0.000 | n=9
D1 PAT3 actual=0.667 | flipped=0.889 | delta=-0.222 | n=9
```

### Test matched control

Previously measured on 2026-08-03 -> 2026-09-01:

```text
H1 PAT2 actual=0.824 | flipped=0.841 | delta=-0.017 | n=233
H1 PAT3 actual=0.850 | flipped=0.807 | delta=+0.043 | n=233
H4 PAT2 actual=0.810 | flipped=0.897 | delta=-0.086 | n=58
H4 PAT3 actual=0.850 | flipped=0.883 | delta=-0.033 | n=60
```

## Finding

The topology-only delta is unstable across periods and is usually non-positive for H4. Small positive H1 deltas appear in some periods but reverse in others and do not survive the full-period matched control.

Therefore:

```text
COLOR TOPOLOGY ALONE = NO ROBUST EDGE ESTABLISHED
```

This is not evidence that the full system has no edge. The tested object deliberately omits the system's hard filters:

- correct support/resistance location;
- final >50% definition;
- PAT3 geometry;
- valid post-SIG behavior;
- graph-cycle state;
- entry/invalidation rules.

The correct research response is to keep these source-backed filters independent of outcome, freeze them, then rerun the same controls.

## Statistical lesson

A large apparent target-hit percentage can coexist with no directional advantage over a matched control.

Therefore any eventual Win rate claim must be accompanied by:

- control comparison;
- sample count;
- time split / out-of-sample behavior;
- event-dependence handling;
- exact Win/Loss definition;
- expectancy and adverse excursion, not only hit rate.

## Files

```text
data/raw/XAUUSDm_M1_MT5_2026-05-26_2026-09-01.csv
results/XAUUSDm_M1_audit_2026-05-26_2026-09-01.json
results/XAUUSDm_MT5_resample_validation_2026-05-26_2026-09-01.json
results/XAUUSDm_PAT_topology_2026-05-26_2026-09-01.json
results/XAUUSDm_PAT_topology_hits_2026-05-26_2026-09-01.csv
results/XAUUSDm_TOPOLOGY_OUTCOME_BASELINE_2026-05-26_2026-09-01.json
results/XAUUSDm_MATCHED_DIRECTION_CONTROL_2026-05-26_2026-09-01.json
results/DEV_MATCHED_DIRECTION_CONTROL_2026-05-26_2026-06-30.json
results/VAL_MATCHED_DIRECTION_CONTROL_2026-07-01_2026-07-31.json
results/XAUUSDm_MATCHED_DIRECTION_CONTROL_2026-08-03_2026-09-01.json
```
