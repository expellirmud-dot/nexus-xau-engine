# 07:00 Q3 Distinct Information — Cross-Period Result — 2026-09-12

Status: DISCOVERY + REPLICATION COMPLETED / DISTINCT-INFORMATION CHECK RECORDED / NO RULE PROMOTION

Frozen plan:

`docs/0700_Q3_DISTINCT_INFORMATION_TEST_PLAN_2026-09-12.md`

Frozen scorer commit:

`855d52b — research: freeze 07:00 Q3 scorer`

The discovery and replication calculations used the same frozen scorer and feature definitions.

## Primary question

Q3 tested whether the Q2 leads:

- origin age;
- H4 consumed-run state;
- recent graded multi-TF agreement;

contain distinct information, or are redundant views of the same market state.

Primary population:

`H4 + FIRST_EXPECTED_SIDE_PA_PROXY + resolved PATH_REMAINING outcome`

H1 was retained as a predeclared sensitivity population.

## Sample sizes

### Discovery

Resolved feature rows:

- H4: 90 rows / 82 contexts
- H1: 82 rows / 75 contexts

### Replication

Resolved feature rows:

- H4: 39 rows / 36 contexts
- H1: 60 rows / 45 contexts

The replication H4 sample is materially smaller, so magnitudes must be interpreted cautiously.

## H4 redundancy map

### Age versus consumed ratio

Discovery:

`rho = +0.770`

Replication:

`rho = +0.844`

This is a strong and replicated feature-feature association.

Therefore the Q2 marginal age relationship cannot be assumed to represent independent age information.

Age and consumed state are strongly entangled in the current H4 proxy representation.

### Recent-1 versus recent-2 MTF agreement

Discovery:

`rho = +0.913`

Replication:

`rho = +0.755`

The two freshness windows are themselves strongly redundant.

Q3 therefore provides another reason not to treat recent-1 and recent-2 as two independent confluence signals.

No window is promoted as canonical.

## H4 partial relationship — origin age

After controlling for consumed ratio and recent MTF agreement:

### Recent-1 family

Discovery:

- origin-row partial rho: -0.166
- context partial rho: -0.114

Replication:

- origin-row partial rho: +0.006
- context partial rho: -0.071

### Recent-2 family

Discovery:

- origin-row partial rho: -0.166
- context partial rho: -0.115

Replication:

- origin-row partial rho: +0.007
- context partial rho: -0.052

The Q2 marginal age relation does **not** survive as a stable positive independent relation in H4.

The discovery sign becomes negative after controlling for consumed state; replication is approximately zero at origin-row level and remains slightly negative at context level.

Leave-one-out descriptive log loss tells the same story asymmetrically:

Discovery:
- removing age increases log loss by about 0.0147–0.0150

Replication:
- removing age increases log loss by only about 0.00024–0.00026

The independent contribution of age does not replicate.

Current status:

`AGE LIKELY REDUNDANT WITH H4 RUN-PROGRESS STATE / DISTINCT EFFECT NOT REPLICATED`

This does not prove age is causally irrelevant.

It means the current evidence does not support treating age as a separate H4 decision variable.

## H4 partial relationship — consumed ratio

After controlling for age and recent MTF agreement:

### Recent-1 family

Discovery:

- origin-row partial rho: +0.456
- context partial rho: +0.440

Replication:

- origin-row partial rho: +0.271
- context partial rho: +0.338

### Recent-2 family

Discovery:

- origin-row partial rho: +0.457
- context partial rho: +0.444

Replication:

- origin-row partial rho: +0.243
- context partial rho: +0.299

The sign remains positive:

- across both periods;
- at origin-row and context level;
- under both frozen MTF freshness families.

Leave-one-out log loss also preserves descriptive contribution:

### Discovery

Removing consumed ratio:

- recent-1 delta log loss: +0.1092
- recent-2 delta log loss: +0.1095

### Replication

Removing consumed ratio:

- recent-1 delta log loss: +0.0325
- recent-2 delta log loss: +0.0245

The contribution is smaller in replication but remains materially larger than removing age in the same H4 replication sample.

Current status:

`H4 CONSUMED RATIO = DISTINCT-INFORMATION RESEARCH LEAD`

This remains continuous.

No consumed-ratio threshold is justified.

## H4 partial relationship — recent MTF agreement

### Recent-1

Discovery:

- origin-row partial rho: +0.016
- context partial rho: -0.017
- leave-out delta log loss: approximately +0.00001

Replication:

- origin-row partial rho: +0.121
- context partial rho: +0.018
- leave-out delta log loss: +0.0062

The independent effect is absent in discovery and small in replication.

Current status:

`NOT DISTINCTLY REPLICATED`

### Recent-2

Discovery:

- origin-row partial rho: +0.001
- context partial rho: -0.058
- leave-out delta log loss: +0.00010

Replication:

- origin-row partial rho: +0.230
- context partial rho: +0.158
- leave-out delta log loss: +0.0217

Recent-2 shows useful independent information in replication, but that independent contribution was effectively absent in discovery.

Therefore Q3 does not permit calling recent-2 an independently replicated H4 feature.

Current status:

`REPLICATION-ONLY DISTINCT LEAD / CROSS-PERIOD DISTINCT EFFECT NOT ESTABLISHED`

This is compatible with Q2's positive marginal MTF relation while showing that much of that marginal relation may overlap with origin state.

## H4 fixed logistic descriptive check

All H4 fixed logistic fits completed with status `OK`.

### Discovery coefficient signs

Recent-1 full model:
- age: negative
- consumed: positive
- MTF: positive

Recent-2 full model:
- age: negative
- consumed: positive
- MTF: negative

### Replication coefficient signs

Recent-1 full model:
- age: positive
- consumed: positive
- MTF: positive

Recent-2 full model:
- age: positive
- consumed: positive
- MTF: positive

Only consumed ratio preserves the same positive coefficient sign across both periods and both model families.

The logistic calculations are descriptive in-sample diagnostics only and are not a trading model.

## H1 sensitivity — important heterogeneity

H1 behaves differently from H4.

### Age × consumed feature relationship

Discovery:

`rho(age, consumed) = +0.630`

Replication:

`rho(age, consumed) = -0.276`

The feature relationship itself changes sign across periods.

This makes simple H1 age/run-progress interpretation unstable.

### H1 consumed partial association

Discovery:

- recent-1 origin/context: +0.396 / +0.380
- recent-2 origin/context: +0.407 / +0.398

Replication:

- recent-1 origin/context: +0.054 / +0.007
- recent-2 origin/context: +0.013 / -0.031

The discovery consumed relation does not replicate independently in H1.

This confirms Q2's warning against one universal H1/H4 consumed-run formula.

### H1 recent-2 MTF partial association

Discovery:

- origin-row: +0.138
- context: +0.187

Replication:

- origin-row: +0.238
- context: +0.222

Leave-one-out delta log loss:

- discovery: +0.0109
- replication: +0.0287

This is directionally consistent and survives the frozen controls better in H1 than it does in H4.

However:

- recent-2 is still a research freshness window;
- recent-1/recent-2 remain highly correlated;
- the H1 origin/run representation itself is still a proxy.

Current status:

`H1 RECENT-MTF DISTINCT-INFORMATION LEAD / SOURCE WINDOW UNRESOLVED`

No minimum TF count or freshness window is promoted.

## Main Q3 correction to Q2

Q2 suggested three promising state variables:

- age;
- consumed/run-progress;
- recent MTF agreement.

Q3 shows they should **not** be treated as three independent signals.

The best supported current interpretation is:

### H4

```text
consumed/run-progress state
    = distinct replicated relationship lead

origin age
    = strongly correlated with consumed state
    = no stable independent contribution

recent MTF agreement
    = marginal Q2 relation exists
    = independent H4 contribution not cross-period replicated
```

### H1

```text
consumed/run-progress state
    = not independently replicated

age/run-progress relationship
    = unstable across periods

recent graded MTF
    = more stable distinct-information lead than H1 consumed state
```

This is timeframe heterogeneity, not a universal formula.

## What Q3 falsified or weakened

Q3 weakens:

1. treating H4 origin age as an independent signal;
2. adding age + consumed ratio as separate points in a scoring system;
3. treating recent-1 and recent-2 as independent confirmations;
4. assuming the same run-progress relationship applies to H1 and H4;
5. building a generic three-factor score from Q2 marginal associations.

No score should be built from Q2 variables.

## Strongest current relationship lead

Within the current research representations, the strongest distinct cross-period H4 lead is:

`consumed_ratio_at_0700`

It remains positive after controlling for age and recent MTF in both periods and at both origin/context levels.

This does **not** mean:

- higher is always better;
- there is a useful threshold;
- it is the instructor's intended entry rule;
- it produces profitable trades.

It means only that H4 run-progress state contains information not explained away by the other frozen Q3 variables.

## What this suggests about the original 07:00 problem

The evidence increasingly favors a state-sequence interpretation over a fixed checklist:

```text
existing source-supported run context
-> run state at 07:00
-> Daily Frame/location
-> post-07:00 confirmation sequence
-> remaining-run participation
```

For H4, the **state of the inherited run** appears more informative than simply how old that run is.

For H1, recent confirmation state currently looks more distinct than run-consumption state.

This remains research interpretation, not canonical teaching.

## Next bounded research question

The next data question should not search for a consumed-ratio threshold.

A useful next step is to test whether the H4 consumed-state relation is:

1. smooth/monotonic across the observed range; or
2. driven by a few extreme rank regions / proxy artifacts.

This should use predeclared quantile diagnostics for shape description only, without selecting an entry cutoff.

Separately, the source-side unresolved item remains high priority:

- exact M1/M5 brake/retest/frame-standing geometry from the teaching material.

The data cannot identify instructor geometry by choosing whichever historical threshold performs best.

## Artifact hashes

### Discovery

`Q3_FEATURE_ROWS.csv`
- SHA256: `0F33042CFCAD9965ABCAC4CDA74A3988D6D959EB6453E18E17E49DB80400ED5E`

`Q3_LEAVE_ONE_OUT.csv`
- SHA256: `DD592268D57AA204BD20193FB3C2B3F84714D552134027E4126870204992CC5B`

`Q3_PAIRWISE_SPEARMAN.csv`
- SHA256: `3818B230BD8BD622AE417086E2FE847967DC19209683A23DF8BBDFCCCA69A4E0`

`Q3_PARTIAL_ASSOCIATIONS.csv`
- SHA256: `0DCD6DD797C26C6FB44D11EE667553AAA47CABD9A5207E5030BE14479CA498C4`

`REPORT.json`
- SHA256: `FC33EE1DE2182043F2B34F2088F64AB014F1D4411DAF91D2264BB975F4A20B02`

### Replication

`Q3_FEATURE_ROWS.csv`
- SHA256: `AB84E90EF55C22C3F27CA926EBB1C1B306256055A8CDE721EFC9D3502F782886`

`Q3_LEAVE_ONE_OUT.csv`
- SHA256: `37069BEBF32B92BE9C09095B195A1A1FA333CE8B57155E0C1368CCEAD4C6FABF`

`Q3_PAIRWISE_SPEARMAN.csv`
- SHA256: `744713ECC7CEB3DE1BDC57230AD3211150789016C2DF5DC6710D7B211AC2C54B`

`Q3_PARTIAL_ASSOCIATIONS.csv`
- SHA256: `3ED1C0A9D6B527EE0E146A3B31709BF69A005130B08C9A00051137224BCBAFCE`

`REPORT.json`
- SHA256: `79A6AC11D44454D50DEA271689F38C3B76ECFA1DA2385AA8927813CF0BF1D809`

## Validation

Before freezing the Q3 scorer:

- targeted Q3 tests: PASS;
- full repository pytest suite: PASS with repository-local basetemp;
- Ruff `src tests`: PASS;
- research preflight: PASS.

## Claim boundary

Q3 still does not establish:

- a profitable strategy;
- a scoring model;
- trade/system Win rate;
- expectancy;
- consumed-ratio threshold;
- age threshold;
- MTF minimum;
- canonical freshness window;
- canonical PA/PAT/SIG;
- exact 50% denominator;
- exact M1/M5 brake/retest geometry;
- D1 run distance;
- universal SL;
- broker execution P&L.
