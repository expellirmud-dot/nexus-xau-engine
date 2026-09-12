# 07:00 Q2 Continuous Origin State and Graded MTF — Cross-Period Result — 2026-09-12

Status: DISCOVERY + REPLICATION COMPLETED / RELATIONSHIPS RECORDED / NO THRESHOLD OR RULE PROMOTION

Frozen plan:

`docs/0700_Q2_CONTINUOUS_MTF_TEST_PLAN_2026-09-12.md`

Frozen scorer commit:

`6f16900 — research: freeze 07:00 Q2 scorer`

The discovery and replication calculations used the same frozen scorer and feature definitions.

## Population

Primary variant:

`FIRST_EXPECTED_SIDE_PA_PROXY`

Primary outcome:

`PATH_REMAINING_AT_CONFIRMATION`

Resolved binary comparison:

```text
TARGET_FIRST      = 1
POINT_CHECK_FIRST = 0
```

NEITHER and AMBIGUOUS rows are retained in artifacts but excluded from the binary Spearman calculation exactly as preregistered.

### Discovery

- feature rows: 175
- contexts: 132
- resolved rows: 172
- TARGET_FIRST: 88
- POINT_CHECK_FIRST: 84
- NEITHER: 3

### Replication

- feature rows: 123
- contexts: 79
- resolved rows: 99
- TARGET_FIRST: 57
- POINT_CHECK_FIRST: 42
- NEITHER: 23
- AMBIGUOUS_SAME_BAR: 1

## Primary continuous-state associations

Spearman rho is descriptive only. No rho threshold or p-value threshold promotes a rule.

### Origin age at 07:00

Discovery:

- origin-row rho: +0.315
- context rho: +0.328
- TARGET_FIRST median age: 8h
- POINT_CHECK_FIRST median age: 4h

Replication:

- origin-row rho: +0.419
- context rho: +0.325
- TARGET_FIRST median age: 10h
- POINT_CHECK_FIRST median age: 4h

Timeframe-stratified origin-row rho:

Discovery:
- H1: +0.364
- H4: +0.304

Replication:
- H1: +0.317
- H4: +0.424

This is the cleanest Q2 directional replication.

Under the current research representation, older surviving H1/H4 origins at 07:00 are associated with a higher chance of PATH_REMAINING target-first ordering.

This does **not** justify an age threshold, expiry rule, or causal interpretation.

Current status:

`REPLICATED DIRECTIONAL RELATIONSHIP / NO THRESHOLD`

## Consumed ratio at 07:00

Combined population:

Discovery:
- origin-row rho: +0.509
- context rho: +0.525

Replication:
- origin-row rho: +0.211
- context rho: +0.248

The combined sign replicated, but magnitude weakened substantially.

Timeframe-stratified origin-row rho:

Discovery:
- H1: +0.516
- H4: +0.514

Replication:
- H1: -0.029
- H4: +0.511

H1 replication collapses to approximately zero and changes sign slightly, while H4 remains strongly positive.

Therefore the combined consumed-ratio relationship is **heterogeneous by timeframe** and may partly reflect timeframe/state composition.

Current status:

`PARTIAL / H4-STABLE / H1-NOT-REPLICATED`

No universal consumed-ratio rule is justified.

## Remaining ratio at confirmation

Combined population:

Discovery:
- origin-row rho: -0.559
- context rho: -0.571

Replication:
- origin-row rho: -0.204
- context rho: -0.281

Timeframe-stratified origin-row rho:

Discovery:
- H1: -0.539
- H4: -0.579

Replication:
- H1: +0.033
- H4: -0.623

The combined negative relation keeps the same sign across periods, but the H1 relation disappears and slightly flips sign in replication while H4 remains strongly negative.

This mirrors the consumed-ratio heterogeneity.

Current status:

`PARTIAL / H4-STABLE / H1-NOT-REPLICATED`

No universal “less remaining is better” threshold may be promoted.

## Absolute remaining points

### Remaining at 07:00

Combined rho:

Discovery:
- origin row: -0.488
- context: -0.510

Replication:
- origin row: -0.353
- context: -0.341

Timeframe-stratified:

Discovery:
- H1: -0.516
- H4: -0.514

Replication:
- H1: +0.029
- H4: -0.511

### Remaining at confirmation

Combined rho:

Discovery:
- origin row: -0.533
- context: -0.566

Replication:
- origin row: -0.361
- context: -0.367

Timeframe-stratified:

Discovery:
- H1: -0.539
- H4: -0.579

Replication:
- H1: +0.033
- H4: -0.623

The same heterogeneity appears.

Because H1 and H4 nominal runs differ and H1 replication does not preserve the negative relation, absolute remaining points must not be interpreted as one universal scalar rule.

## Exact simultaneous MTF alignment

Discovery:

- origin-row rho: -0.003
- context rho: +0.005

Replication:

- origin-row rho: +0.033
- context rho: +0.088

Observed counts remain extremely concentrated at 1 TF:

Discovery:
- count 1: 169 rows / 127 contexts
- count 2: 5 / 4
- count 3: 1 / 1

Replication:
- count 1: 118 rows / 75 contexts
- count 2: 5 / 4

This confirms Q1:

`exact same-close-time alignment is not a useful representation for graded confluence`

under the current proxy.

It is too sparse above one timeframe.

## Recent one-TF-bar agreement

Discovery:

- origin-row rho: +0.058
- context rho: +0.109

Replication:

- origin-row rho: +0.152
- context rho: +0.114

Count distributions:

Discovery:
- count 1: 125 rows, resolved target-first 49.18%
- count 2: 44 rows, 56.82%
- count 3: 5 rows, 60.00%
- count 4: 1 row, 0.00%

Replication:
- count 1: 84 rows, resolved target-first 52.86%
- count 2: 35 rows, 67.86%
- count 3: 4 rows, resolved sample only 1 TARGET_FIRST with 3 NEITHER
- count 4: none

The association sign is positive at both origin-row and context level in both periods.

However, the effect is modest and counts 3–4 are sparse.

Current status:

`DIRECTIONALLY REPLICATED WEAK RELATIONSHIP / NO MINIMUM COUNT`

## Recent two-TF-bars agreement

Discovery:

- origin-row rho: +0.067
- context rho: +0.103

Replication:

- origin-row rho: +0.280
- context rho: +0.250

Count distributions:

Discovery:
- count 1: 112 rows, resolved target-first 48.18%
- count 2: 36 rows, 60.00%
- count 3: 25 rows, 52.00%
- count 4: 2 rows, 50.00%

Replication:
- count 1: 69 rows, resolved target-first 45.61%
- count 2: 35 rows, 72.41%
- count 3: 19 rows, 76.92%
- count 4: none

The sign is positive across origin/context and both periods, with a larger magnitude in replication.

But discovery is not monotonic across every count value, and count 4 is too sparse.

Therefore the evidence supports only a graded relationship lead, not a cutoff such as “2+ TF required.”

Current status:

`DIRECTIONALLY REPLICATED RELATIONSHIP LEAD / WINDOW REMAINS RESEARCH REPRESENTATION`

The two-bar window cannot be promoted as canonical merely because replication magnitude is larger.

## Cross-period classification

### Directionally replicated without timeframe contradiction

1. **origin_age_hours_at_0700**
   - positive origin-row and context relation in both periods;
   - positive separately in H1 and H4 in both periods.

This is the most stable Q2 origin-state relationship.

### Directionally replicated but heterogeneous

2. **consumed_ratio_at_0700**
3. **remaining_ratio_at_confirmation**
4. **remaining_points_at_0700**
5. **remaining_points_at_confirmation**

Combined relations keep their direction, but H1 replication collapses near zero/sign-flips while H4 remains strong.

These cannot be generalized across H1/H4.

### Directionally replicated graded-MTF leads

6. **alignment_count_recent_1_tf_bar**
7. **alignment_count_recent_2_tf_bars**

Both remain positive at origin-row and context level across discovery and replication.

Recent-2 shows a larger replication magnitude, but Q2 is prohibited from choosing it as the canonical freshness window.

### Unsupported representation

8. **alignment_count_exact**

Near-zero relation and severe count sparsity above one TF persist.

## What Q2 falsified or weakened

Q2 weakens several tempting simplifications:

- one universal consumed-ratio rule across H1/H4;
- one universal remaining-run threshold across H1/H4;
- exact simultaneous close-time alignment as the main representation of multi-TF confluence;
- choosing a fixed TF count purely from historical performance.

It also gives no support for turning the observed medians into thresholds.

## What Q2 strengthens

The current evidence supports carrying forward these relationship hypotheses:

### Lead A — age as state

Among source-partial surviving origins, older age at 07:00 is consistently associated with PATH_REMAINING target-first ordering across both periods and both H1/H4.

This should be studied as a continuous state variable, not an age gate.

### Lead B — graded recent multi-TF agreement

Recent same-direction agreement across H1/M30/M15/M5 shows a small-to-moderate positive association across both periods, unlike exact simultaneous alignment.

This better matches the source concept of graded confluence.

The exact freshness window remains unresolved.

### Lead C — H4 run-progress state

Consumed/remaining state is strongly consistent for H4 across periods.

The same relationship does not replicate in H1.

This suggests the next study should explicitly model a timeframe × run-state interaction instead of forcing a shared formula.

## Recommended next bounded question

Do not optimize a threshold next.

Q3 should test whether the replicated features contribute distinct information or are redundant with each other.

A suitable frozen question is:

> After retaining origin timeframe explicitly, do origin age, H4 run-progress state, and recent multi-TF agreement each preserve their direction when the other state variables are controlled or stratified?

This can be studied with fixed rank/stratified comparisons rather than fitting a profit-maximizing model.

A second important branch remains unresolved from the source side:

- exact M1/M5 brake/retest/standing geometry.

Until that geometry is source-resolved, it should remain outside canonical entry logic.

## Artifact hashes

### Discovery

`Q2_ASSOCIATIONS.csv`
- bytes: 8,834
- SHA256: `30B223EAE274C7612B3FE533F691AE0DEE0D41786EB9F7A7B1C6FE29EFEFD998`

`Q2_FEATURE_EVENTS.csv`
- bytes: 112,746
- SHA256: `0BE4935CF977C25701C797C28D6543D9BF4357AE6E7D99FC0DE4C3AAA24CABD2`

`Q2_MTF_COUNT_GROUPS.csv`
- bytes: 2,006
- SHA256: `AC0B6372E92307207182BC0227C8BE4D067945B029F406E346CB37018B410983`

`REPORT.json`
- bytes: 3,411
- SHA256: `A8462C16B9BC0F73724ED16996FDB9D70F537DFE8CCC0133AC9EE20F915E05B9`

### Replication

`Q2_ASSOCIATIONS.csv`
- bytes: 8,612
- SHA256: `46CFDE87E710DFE2D129719DC643AECC15F0F81A677D34183F045ABBBE2B2C30`

`Q2_FEATURE_EVENTS.csv`
- bytes: 75,795
- SHA256: `A6733EC188F6E6A008AD5FAC0FCAC3908739572F6DC768DD1959D7D65F568D84`

`Q2_MTF_COUNT_GROUPS.csv`
- bytes: 1,603
- SHA256: `06B9ECC18C485A8C04A208C909C11DA05D0C4956549F40B346334AFB63E584A4`

`REPORT.json`
- bytes: 3,430
- SHA256: `CB4DD2767519830AED6671A49DC80FA5564AAD2409A1333A13AC724B288AE84B`

## Claim boundary

Q2 still does not establish:

- a profitable strategy;
- system/trade Win rate;
- expectancy;
- an entry threshold;
- an origin-age threshold;
- a consumed/remaining threshold;
- H1/H4 priority;
- a canonical freshness window;
- a minimum MTF count;
- canonical PA/PAT/SIG;
- exact PAT 50% denominator;
- D1 run distance;
- universal SL;
- broker execution P&L.

These remain unresolved.
