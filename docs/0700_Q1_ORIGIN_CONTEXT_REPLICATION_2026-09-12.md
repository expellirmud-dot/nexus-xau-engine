# 07:00 Q1 Origin Context — Replication and Cross-Period Checkpoint — 2026-09-12

Status: REPLICATION COMPLETED / CROSS-PERIOD COMPARISON RECORDED / NO RULE PROMOTION

Frozen plan:

`docs/0700_Q1_ORIGIN_CONTEXT_TEST_PLAN_2026-09-12.md`

Frozen scorer commit:

`e062f79 — research: freeze 07:00 Q1 scorer`

Discovery checkpoint:

`docs/0700_Q1_ORIGIN_CONTEXT_DISCOVERY_2026-09-12.md`

The replication used the same V1 feature generator and the same frozen Q1 scorer without changing eligibility, confirmation selection, target definitions, or grouping logic.

## Replication period

Input:

`data/raw/dukascopy/chunks/XAUUSD_M1_BID_2023-09-01_2023-11-23.csv`

Source SHA256:

`f5749ffc8dc55f095fd9b1519f54a3b1fe3902a96124adf9f330e48db9d83341`

Metadata reports the cache range as complete with no missing cache dates.

Generated V1 rows:

- 07:00 day state: 60
- origin candidates: 2,805
- confirmation events: 8,876

Eligible Q1 source-partial population:

- 95 unique proxy origins
- 135 origin-day rows
- 83 day+side contexts

## Replication pre-confirmation audit

FIRST_ANY_PA_PROXY:

- origin rows: 135
- SCORED: 124
- POINT_CHECK_DESTROYED_BEFORE_CONFIRMATION: 8
- ORIGIN_COMPLETED_BEFORE_CONFIRMATION: 1
- RIGHT_CENSORED_NO_NEXT_0700: 2
- scored contexts: 80

FIRST_EXPECTED_SIDE_PA_PROXY:

- origin rows: 135
- SCORED: 123
- POINT_CHECK_DESTROYED_BEFORE_CONFIRMATION: 8
- ORIGIN_COMPLETED_BEFORE_CONFIRMATION: 1
- NO_CONFIRMATION_BEFORE_NEXT_0700: 1
- RIGHT_CENSORED_NO_NEXT_0700: 2
- scored contexts: 79

The pre-confirmation validity guard remains material in replication.

## Primary representation — PATH_REMAINING_AT_CONFIRMATION

FIRST_ANY_PA_PROXY replication:

- TARGET_FIRST: 58
- POINT_CHECK_FIRST: 42
- NEITHER_BEFORE_NEXT_0700: 23
- AMBIGUOUS_SAME_BAR: 1

Among resolved target-vs-point-check rows:

`58 / (58 + 42) = 58.00%`

Median post-confirmation:

- MFE: 921.00 project points
- MAE: 767.85 project points

This is a signal/run relationship statistic under a research representation.

It is not a trade/system Win rate.

## Alternative representation — ORIGIN_TARGET_LEVEL

Replication:

- TARGET_FIRST: 35
- POINT_CHECK_FIRST: 48
- NEITHER_BEFORE_NEXT_0700: 40
- AMBIGUOUS_SAME_BAR: 1

Resolved target-first proportion:

`35 / (35 + 48) = 42.17%`

### Cross-period result

Discovery:

- PATH_REMAINING resolved target-first: 50.87%
- ORIGIN_TARGET_LEVEL resolved target-first: 43.60%

Replication:

- PATH_REMAINING resolved target-first: 58.00%
- ORIGIN_TARGET_LEVEL resolved target-first: 42.17%

The ordering replicated:

`PATH_REMAINING_AT_CONFIRMATION > ORIGIN_TARGET_LEVEL`

under the frozen proxy/scoring definitions.

This is the strongest Q1 cross-period relationship.

It still does not identify instructor intent and does not establish a production target rule.

## H1 versus H4 origin

### Discovery

H1:
- resolved path target-first: 51.22%

H4:
- resolved path target-first: 50.55%

The two were nearly indistinguishable.

### Replication

H1:
- 80 scored origin rows
- TARGET_FIRST: 41
- POINT_CHECK_FIRST: 20
- NEITHER: 19
- resolved target-first: 67.21%
- median MFE: 970.15
- median MAE: 784.35

H4:
- 44 scored origin rows
- TARGET_FIRST: 17
- POINT_CHECK_FIRST: 22
- NEITHER: 4
- AMBIGUOUS: 1
- resolved target-first: 43.59%
- median MFE: 892.00
- median MAE: 731.00

The apparent H1 advantage in replication did **not** exist in discovery.

Therefore:

`H1 > H4`

is not a stable cross-period conclusion.

No origin-timeframe priority is promoted.

## Same-direction origin timeframe context

### Discovery resolved target-first

- H1-only: 47.83%
- H1+H4: 56.34%
- H4-only: 46.43%

### Replication resolved target-first

- H1-only: 60.53%
- H1+H4: 60.87%
- H4-only: 43.75%

The discovery lead that H1+H4 was clearly better than H1-only did not replicate as a distinct advantage.

H1+H4 remained above H4-only, but H1-only caught up in replication.

Therefore:

`H1+H4 required`

is not supported.

The useful remaining question is whether a richer state representation, rather than a hard timeframe-set rule, explains the difference.

## Opposite-direction origin conflict

### Discovery

No opposite-direction survivor:
- resolved target-first: 46.74%

Opposite-direction survivor present:
- resolved target-first: 55.56%

Discovery unexpectedly made the conflict group look better.

### Replication

No opposite-direction survivor:
- resolved target-first: 58.54%

Opposite-direction survivor present:
- resolved target-first: 57.63%

The discovery advantage disappeared.

Most importantly, the conflict group was **not materially worse** in replication.

Therefore the evidence still rejects promoting:

`OPPOSITE SURVIVING ORIGIN PRESENT -> VETO`

as a rule.

Conflict remains a state feature, not an entry veto.

## Daily Frame side

FIRST_ANY scored rows:

Discovery:
- EXPECTED_SIDE: 175
- CROSSED_SIDE: 1

Replication:
- EXPECTED_SIDE: 122
- CROSSED_SIDE: 2

The first matching-direction PA proxy is almost always already on the frozen research EXPECTED_SIDE after the source-partial origin filter.

This relationship itself replicated.

However, because the CROSSED_SIDE sample is extremely small, Q1 cannot determine whether Daily Frame side has causal/filter value versus being structurally induced by the current proxy definitions.

## First confirmation timeframe

Discovery scored rows:

- M5: 150
- M15: 17
- M30: 5
- H1: 4

Replication:

- M5: 109
- M15: 14
- M30: 1
- H1: 0

M5 being the first matching confirmation is a stable descriptive feature of this proxy system.

It is not evidence that M5 is inherently the best confirmation timeframe because lower timeframes have more opportunities to close first.

## Exact simultaneous MTF alignment

Discovery:

- count 1: 170 rows
- count 2: 5
- count 3: 1
- count 4: 0

Replication:

- count 1: 119 rows
- count 2: 5
- count 3+: 0

The same sparsity replicated.

Therefore exact same-close-time alignment is not an adequate representation for testing the source statement that more same-direction H1/M30/M15/M5 agreement is stronger confluence.

The next research representation should test graded **freshness / recent agreement**, keeping multiple fixed windows separate rather than inventing a minimum count.

## What replicated

The following cross-period observations survived replication strongly enough to carry forward as research facts about the current representation:

1. PATH_REMAINING_AT_CONFIRMATION outperformed absolute ORIGIN_TARGET_LEVEL on resolved target-vs-point-check ordering in both periods.
2. Opposite-direction surviving origin presence is not supported as a veto.
3. First confirmation is overwhelmingly M5 under the PAT2-BODY proxy.
4. Exact simultaneous multi-TF alignment above one timeframe is too sparse for the intended graded-confluence question.
5. Pre-confirmation origin revalidation is necessary because some 07:00 survivors terminate before the first usable confirmation.

These are representation-level research observations, not canonical trading rules.

## What did not replicate cleanly

The following discovery leads were unstable:

1. simple H1-versus-H4 similarity changed to an H1 advantage in replication;
2. H1+H4 context did not remain clearly superior to H1-only;
3. the apparent discovery benefit of opposite-direction conflict disappeared;
4. MFE/MAE levels shifted materially across periods.

These unstable relations must not be converted into priority, veto, or threshold rules.

## Q1 conclusion

Q1 does not justify an origin priority rule.

The strongest next step is to replace coarse context labels with variables that retain more information:

- origin age;
- consumed ratio;
- remaining run;
- exact alignment count;
- recent-one-TF-bar agreement;
- recent-two-TF-bars agreement.

These should be studied as graded/continuous relationships without selecting a cutoff from discovery.

## Replication artifacts

`results/0700_Q1_ORIGIN_CONTEXT/REPLICATION_2023_09_TO_2023_11_23/Q1_ORIGIN_CONTEXT_EVENTS.csv`

- bytes: 145,467
- SHA256: `7A4E85BF0E7106DC1423F071FC4F473AC2A9E228FC3140596321F1BAE91E4395`

`results/0700_Q1_ORIGIN_CONTEXT/REPLICATION_2023_09_TO_2023_11_23/REPORT.json`

- bytes: 20,353
- SHA256: `DE748A34CF2FC36824FD6FFA36B7531C5ED47AB36C645A0ADFB61D5E6F3233DC`

## Claim boundary

Q1 still does not establish:

- a profitable 07:00 strategy;
- trade/system Win rate;
- expectancy;
- canonical H1/H4 priority;
- conflict veto;
- MTF minimum;
- canonical PA/PAT/SIG;
- exact 50% denominator;
- D1 run distance;
- universal SL;
- broker execution P&L.

Q2 must remain feature-relationship research, not rule optimization.
