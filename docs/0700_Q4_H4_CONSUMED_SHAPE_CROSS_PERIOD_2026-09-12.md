# 07:00 Q4 H4 Consumed-State Shape — Cross-Period Checkpoint — 2026-09-12

Status: DISCOVERY + REPLICATION COMPLETED / SHAPE DIAGNOSTIC RECORDED / NO THRESHOLD PROMOTION

Frozen plan:

`docs/0700_Q4_H4_CONSUMED_SHAPE_TEST_PLAN_2026-09-12.md`

Pre-outcome failure/amendment checkpoint:

`docs/0700_Q4_QUANTILE_TIE_FAILURE_CHECKPOINT_2026-09-12.md`

Tie-safe scorer commit:

`1acd4b2 — research: make Q4 quantile bins tie-safe`

Discovery checkpoint:

`docs/0700_Q4_H4_CONSUMED_SHAPE_DISCOVERY_2026-09-12.md`

The same tie-safe scorer was used unchanged for Discovery and Replication.

## Primary question

Q4 asked whether the replicated H4 `consumed_ratio_at_0700` relationship:

- persists across the observed range;
- is approximately monotonic;
- survives removal of extreme high/low observations; or
- is mostly an extreme-tail artifact.

This was a descriptive shape study only.

No bin boundary, percentile, or observed transition was eligible for promotion into a trading threshold.

## H4 full-sample relation

### Discovery

Origin-row:

- N = 90
- rho = +0.514

Context:

- N = 82
- rho = +0.514

### Replication

Origin-row:

- N = 39
- rho = +0.511

Context:

- N = 36
- rho = +0.500

The broad positive rank relationship is almost unchanged in magnitude across the two periods.

Current status:

`BROAD POSITIVE H4 CONSUMED-STATE RELATIONSHIP REPLICATED`

This does not imply a linear effect, threshold, or causal rule.

## H4 central-80% sensitivity

The fixed 10th/90th percentile trim was frozen before outcome.

### Discovery

Origin-row:
- N = 81
- rho = +0.426

Context:
- N = 73
- rho = +0.400

### Replication

Origin-row:
- N = 35
- rho = +0.393

Context:
- N = 32
- rho = +0.343

The positive relationship remains after removing the upper extreme tail in both periods.

The lower 10th percentile equals exactly zero in both H4 periods, so the inclusive lower-bound trim removes no H4 row.

Therefore Q4 can evaluate top-tail dependence, but cannot cleanly remove a "bottom 10%" while preserving the frozen inclusive rule because of the point mass at zero.

This is a feature-distribution fact, not a trading implication.

## H4 empirical shape — Discovery

Repeated zero values collapsed five target quantiles into four effective bins.

Origin-row target-first fractions:

- Q1: 27.78%
- Q2: 27.78%
- Q3: 77.78%
- Q4: 94.44%

Context target-first fractions:

- Q1: 24.24%
- Q2: 34.38%
- Q3: 71.88%
- Q4: 88.24%

Both levels were strictly nondecreasing.

The largest discovery transition occurred between the second and third effective bins.

Discovery alone could have tempted a threshold interpretation.

Q4 replication prevents that conclusion.

## H4 empirical shape — Replication

Again four effective bins.

### Origin-row

Q1:
- consumed range: 0.0000 -> 0.2413
- median: 0.0000
- rows: 16
- TARGET_FIRST: 4
- POINT_CHECK_FIRST: 12
- target-first fraction: 25.00%
- median MFE: 1,439.35
- median MAE: 951.35

Q2:
- consumed range: 0.2633 -> 0.3180
- median: 0.2833
- rows: 7
- TARGET_FIRST: 1
- POINT_CHECK_FIRST: 6
- target-first fraction: 14.29%
- median MFE: 839.30
- median MAE: 1,025.10

Q3:
- consumed range: 0.3567 -> 0.7951
- median: 0.6213
- rows: 8
- TARGET_FIRST: 4
- POINT_CHECK_FIRST: 4
- target-first fraction: 50.00%
- median MFE: 870.00
- median MAE: 877.65

Q4:
- consumed range: 0.8047 -> 0.9642
- median: 0.9182
- rows: 8
- TARGET_FIRST: 8
- POINT_CHECK_FIRST: 0
- target-first fraction: 100.00%
- median MFE: 1,392.30
- median MAE: 139.00

Adjacent differences:

- Q2-Q1: -0.107
- Q3-Q2: +0.357
- Q4-Q3: +0.500

Replication classification:

`NOT_STRICT_NONDECREASING`

### Context level

Target-first fractions:

- Q1: 20.00%
- Q2: 14.29%
- Q3: 42.86%
- Q4: 100.00%

Adjacent differences:

- Q2-Q1: -0.057
- Q3-Q2: +0.286
- Q4-Q3: +0.571

Context classification:

`NOT_STRICT_NONDECREASING`

The small Q1 -> Q2 decline appears at both origin-row and context level.

Therefore exact monotonicity did not replicate.

## Cross-period interpretation

Two statements must be separated.

### Supported

The broad rank relationship between H4 consumed state and PATH_REMAINING target-first ordering is positive and highly similar across Discovery and Replication.

It also survives removal of the top 10% consumed tail.

Therefore the H4 relationship is not explained solely by a handful of highest-consumed observations.

### Not supported

A claim that every increase in consumed ratio produces a stepwise improvement is false under the replication shape.

The empirical bins are not strictly monotonic in replication.

Therefore Q4 explicitly rejects using the Discovery jump or any observed bin boundary as an entry threshold.

Current interpretation:

`BROAD POSITIVE / NONLINEAR-OR-IRREGULAR SHAPE / NO THRESHOLD`

## Why this matters for the original 07:00 problem

Q3 already showed that H4 run-progress state carries information distinct from origin age.

Q4 now adds that this information is not merely a top-tail artifact.

However, the relationship should be represented as a **continuous market/run state**, not as:

```text
consumed > X -> enter
```

The data currently supports "state matters" more strongly than "there is a magic cutoff."

This matches the project's research principle of studying how values change together before forcing threshold rules.

## H1 sensitivity

H1 does not replicate the H4 relationship.

### Discovery H1

Origin-row full rho:

`+0.516`

Central 80%:

`+0.355`

### Replication H1

Origin-row full rho:

`-0.029`

Central 80%:

`-0.183`

Context full rho:

`-0.007`

Context central 80%:

`-0.207`

Replication H1 quantile shape is also non-monotonic.

Therefore Q4 strengthens the timeframe-heterogeneity conclusion from Q2/Q3:

`DO NOT APPLY ONE CONSUMED-RATIO RELATIONSHIP TO BOTH H1 AND H4`

No H1 consumed-state rule is supported.

## What Q4 changes

Before Q4:

- H4 consumed ratio was a distinct-information lead;
- shape was unknown.

After Q4:

1. the broad positive H4 relationship replicates;
2. it persists after removing the upper extreme tail;
3. it is visible at both origin-row and context levels;
4. exact monotonicity does not replicate;
5. Discovery empirical jumps must not be converted into thresholds;
6. H1 remains heterogeneous and fails replication.

## Strongest current H4 state conclusion

Within the current research proxy:

```text
H4 inherited run exists and survives source-partial point-check logic
        ↓
its consumed/run-progress state at 07:00 contains replicated information
        ↓
but the relation is broad and irregular, not a proven cutoff rule
```

This remains a representation-level research result.

It is not yet canonical teaching or a live entry rule.

## Recommended next bounded question

Do not search for a consumed threshold.

The next useful data-side question is whether the H4 consumed-state relationship remains visible after separating major context states that may be confounding it, especially:

- direction BUY vs SELL;
- opposite-direction surviving origin present vs absent;
- Daily Frame / confirmation context already carried by the frozen dataset;
- recent MTF state as a stratification rather than an additive score.

This should be a fixed stratified robustness test, not an optimization.

Separately, source-side work remains important for:

- exact M1/M5 brake/retest/frame-standing geometry;
- exact PAT 50% denominator;
- exact D1 run distance.

Historical data must not invent those teaching definitions.

## Discovery artifact hashes

`Q4_FEATURE_ROWS.csv`
- SHA256: `499377CF6EEE06AE9C58D2F51B0C605036F479A78C4AA806A6DB4BE5C0FF6D2E`

`Q4_QUINTILES.csv`
- SHA256: `46C6AADF2998B19261445956EBCC55B5E2D5678440DCC7EDC322EF5501DC4A2B`

`Q4_TRIM_SENSITIVITY.csv`
- SHA256: `1D3AFD2348D1331ACD6CDF16CA63DBB543F53AC5E6211640DF0B2B48535AE7AF`

`REPORT.json`
- SHA256: `CC63359368BC94312A9F44D0DEE89A433E805D1174310F7A1A050F56CCF17624`

## Replication artifact hashes

`Q4_FEATURE_ROWS.csv`
- bytes: 13,566
- SHA256: `52D62CCDCD9EEF8AE3D26FC3E720C4D1686D59C6DED624B5FD24F4B12A6370F9`

`Q4_QUINTILES.csv`
- bytes: 2,072
- SHA256: `84363BE3992F1CC61D1BFFB1FDE3775ED79E4829C703F8C03D834221D5FB53B6`

`Q4_TRIM_SENSITIVITY.csv`
- bytes: 1,263
- SHA256: `68A16E4204F49D3AD8CA9AD505043EF6FC187DD7C040DBA738705E0907595113`

`REPORT.json`
- bytes: 5,620
- SHA256: `98022AAE67EED32E8FAFF5017703D2B2F91BDCE426E62A50FA67A7B204707549`

## Validation history

Initial Q4 scorer:

- targeted tests passed;
- Ruff passed after a style-only correction;
- full suite passed;
- preflight passed;
- scorer frozen at `238b38a`.

First Discovery execution then failed before outcome artifact creation because empirical qcut edges were duplicated at zero.

That failure was checkpointed at `b1fac06`.

Tie-safe amendment:

- targeted Q4 tests: 7/7 passed;
- Ruff: PASS;
- full pytest suite: exit code 0;
- research preflight: PASS;
- tie-safe scorer frozen at `1acd4b2`.

Discovery was then opened and checkpointed at `cb16496`.

Replication used `1acd4b2` unchanged.

## Claim boundary

Q4 does not establish:

- a consumed-ratio threshold;
- an optimal consumed range;
- a profitable strategy;
- trade/system Win Rate;
- expectancy;
- canonical H1/H4 priority;
- canonical MTF window;
- exact PA/PAT/SIG;
- exact 50% denominator;
- D1 run distance;
- universal SL;
- broker execution P&L.


## YouTube source navigation

For fast source lookup, video timestamps, and unresolved-source routing, use:

`docs/0700_YOUTUBE_SOURCE_GAP_MAP_2026-09-13.md`

That report is restricted to YouTube sources already recorded in the repository and separates:

- topics already source-backed;
- partially closed geometry;
- source-exhausted but unresolved items;
- unmapped YouTube links that remain candidates for missing 07:00 teaching material.

Current source-critical gaps highlighted there include:

- exact PAT >50% denominator;
- Daily Frame exact selector/tolerance;
- universal Sideway auto-geometry;
- exact D1 inherited-run distance;
- universal multi-family conflict resolver;
- exact fill convention if it exists as instructor-defined teaching;
- universal Body Collection candidate priority.

Consult the map before re-watching sources so already exhausted source questions are not restarted from zero.
