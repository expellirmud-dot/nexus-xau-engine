# 07:00 Q4 H4 Consumed-State Shape — Discovery Checkpoint — 2026-09-12

Status: DISCOVERY COMPLETED / CHECKPOINT RECORDED / NO THRESHOLD PROMOTION

Frozen plan:

`docs/0700_Q4_H4_CONSUMED_SHAPE_TEST_PLAN_2026-09-12.md`

Pre-outcome technical amendment:

`docs/0700_Q4_QUANTILE_TIE_FAILURE_CHECKPOINT_2026-09-12.md`

Tie-safe scorer commit:

`1acd4b2 — research: make Q4 quantile bins tie-safe`

The first scorer execution failed before producing any Q4 artifact because repeated consumed-ratio zero values created duplicate qcut edges.

That failure was recorded and the tie-safe amendment was frozen before any Q4 outcome result was opened.

## Discovery population

Period:

`2022-09-01 -> 2023-03-31`

Resolved Q4 rows:

- H4: 90 rows / 82 contexts
- H1 sensitivity: 82 rows / 75 contexts

Primary feature:

`consumed_ratio_at_0700`

Primary outcome:

`PATH_REMAINING_AT_CONFIRMATION`

Resolved states:

- TARGET_FIRST = 1
- POINT_CHECK_FIRST = 0

## H4 empirical quantile shape

Target quantile count was five.

Repeated feature values caused duplicate empirical boundaries to collapse, producing four effective H4 bins.

### Origin-row level

Q1:
- consumed range: 0.0000 -> 0.3920
- median consumed: 0.0000
- rows: 36
- TARGET_FIRST: 10
- POINT_CHECK_FIRST: 26
- target-first fraction: 27.78%
- median MFE: 1,010.05 points
- median MAE: 1,354.00 points

Q2:
- consumed range: 0.4047 -> 0.5620
- median: 0.5069
- rows: 18
- TARGET_FIRST: 5
- POINT_CHECK_FIRST: 13
- target-first fraction: 27.78%
- median MFE: 602.55
- median MAE: 1,643.15

Q3:
- consumed range: 0.5653 -> 0.8089
- median: 0.6553
- rows: 18
- TARGET_FIRST: 14
- POINT_CHECK_FIRST: 4
- target-first fraction: 77.78%
- median MFE: 1,528.50
- median MAE: 617.55

Q4:
- consumed range: 0.8293 -> 0.9953
- median: 0.9069
- rows: 18
- TARGET_FIRST: 17
- POINT_CHECK_FIRST: 1
- target-first fraction: 94.44%
- median MFE: 1,358.50
- median MAE: 651.55

Adjacent target-first differences:

- Q2-Q1: +0.000
- Q3-Q2: +0.500
- Q4-Q3: +0.167

Discovery shape classification:

`STRICT_NONDECREASING`

This is descriptive shape evidence only.

The empirical bin boundaries are not entry thresholds.

## H4 context-level shape

Effective bins: 4

Target-first context fractions:

- Q1: 24.24%
- Q2: 34.38%
- Q3: 71.88%
- Q4: 88.24%

Adjacent differences:

- Q2-Q1: +0.101
- Q3-Q2: +0.375
- Q4-Q3: +0.164

Context shape classification:

`STRICT_NONDECREASING`

The context-level direction therefore agrees with the origin-row discovery shape.

## H4 trim sensitivity

### Origin-row

Full sample:
- N = 90
- rho = +0.514

Central 80%:
- N = 81
- rho = +0.426

Drop top 10%:
- N = 81
- rho = +0.426

Drop bottom 10%:
- N = 90
- rho = +0.514

The 10th percentile consumed value is exactly zero, so the fixed bottom-10% filter removes no H4 row under the inclusive boundary rule.

This is a property of the feature distribution and must not be interpreted as evidence that zero is a meaningful trading cutoff.

### Context level

Full sample:
- N = 82
- rho = +0.514

Central 80%:
- N = 73
- rho = +0.400

Drop top 10%:
- N = 73
- rho = +0.400

Again the lower 10th percentile is zero, so the inclusive bottom-tail filter removes no context.

## Discovery interpretation

The H4 consumed-state relationship is **not solely produced by the highest 10% consumed tail** in this period.

Evidence:

- full-sample rho is positive;
- central-80% rho remains positive;
- removing the top 10% still leaves a positive relation;
- origin-row and context-level quantile shapes are both nondecreasing.

However, the visible shape is not smooth in a strict linear sense.

The largest jump occurs between the second and third effective empirical bins.

This may reflect:

- a real nonlinear relationship;
- the mass at zero / irregular empirical distribution;
- proxy construction;
- period-specific state composition.

Discovery alone cannot distinguish these explanations.

No threshold is selected.

## H1 sensitivity

H1 origin-row shape is also nondecreasing across five effective bins:

- Q1: 23.53%
- Q2: 31.25%
- Q3: 43.75%
- Q4: 62.50%
- Q5: 94.12%

But context-level H1 is not strictly nondecreasing:

- 33.33%
- 25.00%
- 56.67%
- 53.33%
- 93.33%

H1 central-80% relation remains positive, but Q3 already showed that H1 consumed state does not have a stable independent contribution after controls.

Therefore this sensitivity result does not reverse the Q3 timeframe-heterogeneity conclusion.

## Discovery conclusion

Current H4 status:

`BROAD POSITIVE SHAPE LEAD / REPLICATION REQUIRED`

The strongest discovery observation is that the positive H4 consumed-state relation survives removal of the upper extreme tail and appears in both origin-row and context-level shape.

The next required step is replication with the exact same tie-safe scorer on:

`2023-09-01 -> 2023-11-23`

No Q4 binning, trimming, or outcome logic may change before replication.

## Artifact hashes

`Q4_FEATURE_ROWS.csv`
- bytes: 23,468
- SHA256: `499377CF6EEE06AE9C58D2F51B0C605036F479A78C4AA806A6DB4BE5C0FF6D2E`

`Q4_QUINTILES.csv`
- bytes: 2,324
- SHA256: `46C6AADF2998B19261445956EBCC55B5E2D5678440DCC7EDC322EF5501DC4A2B`

`Q4_TRIM_SENSITIVITY.csv`
- bytes: 1,369
- SHA256: `1D3AFD2348D1331ACD6CDF16CA63DBB543F53AC5E6211640DF0B2B48535AE7AF`

`REPORT.json`
- bytes: 5,759
- SHA256: `CC63359368BC94312A9F44D0DEE89A433E805D1174310F7A1A050F56CCF17624`

## Claim boundary

This checkpoint does not establish:

- a consumed-ratio threshold;
- an optimal consumed range;
- a profitable strategy;
- trade/system Win Rate;
- expectancy;
- H1/H4 priority;
- canonical instructor intent;
- universal SL;
- broker execution P&L.
