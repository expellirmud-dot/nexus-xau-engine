# 07:00 Q1 Origin Context — Discovery Result — 2026-09-12

Status: DISCOVERY RESULT RECORDED / NO RULE PROMOTION

Frozen plan:

`docs/0700_Q1_ORIGIN_CONTEXT_TEST_PLAN_2026-09-12.md`

Frozen scorer commit:

`e062f79 — research: freeze 07:00 Q1 scorer`

The plan and scorer were committed/pushed before this discovery outcome was calculated.

## Data

Discovery source:

`data/raw/dukascopy/chunks/XAUUSD_M1_BID_2022-09-01_2023-03-31.csv`

Input 07:00 feature dataset:

`results/0700_STATE_DATASET_V1/DISCOVERY_2022_09_TO_2023_03/`

Eligible starting population:

- 202 source-partial surviving proxy origins;
- 206 origin-day rows;
- 150 unique day+side contexts.

Each eligible origin is evaluated under both frozen confirmation variants.

## Pre-confirmation audit

### FIRST_ANY_PA_PROXY

206 origin rows:

- SCORED: 176
- POINT_CHECK_DESTROYED_BEFORE_CONFIRMATION: 25
- ORIGIN_COMPLETED_BEFORE_CONFIRMATION: 5

Scored unique contexts: 133

### FIRST_EXPECTED_SIDE_PA_PROXY

206 origin rows:

- SCORED: 175
- POINT_CHECK_DESTROYED_BEFORE_CONFIRMATION: 26
- ORIGIN_COMPLETED_BEFORE_CONFIRMATION: 5

Scored unique contexts: 132

This confirms that eligibility at 07:00 is not sufficient by itself: some proxy origins terminate before the first usable confirmation exists.

Those rows remain recorded and are not silently removed from the audit population.

## Primary discovery observation — PATH_REMAINING_AT_CONFIRMATION

For `FIRST_ANY_PA_PROXY`, among 176 scored origin rows:

- TARGET_FIRST: 88
- POINT_CHECK_FIRST: 85
- NEITHER_BEFORE_NEXT_0700: 3

Among rows with an observed target/point-check first hit:

`88 / (88 + 85) = 50.87%`

This is a **signal/run target-first proportion under a research representation**, not trade/system Win rate.

Median post-confirmation:

- MFE: 1,156.85 project points
- MAE: 945.00 project points

The overall discovery result is close to balanced and by itself does not support a production edge claim.

## Alternative target representation — ORIGIN_TARGET_LEVEL

For the same `FIRST_ANY_PA_PROXY` scored rows:

- TARGET_FIRST: 75
- POINT_CHECK_FIRST: 97
- NEITHER_BEFORE_NEXT_0700: 4

Resolved target-first proportion:

`75 / (75 + 97) = 43.60%`

Within this discovery representation, the absolute origin target level performs worse than the PATH_REMAINING_AT_CONFIRMATION representation.

This is evidence about the two frozen research representations only.

It does not identify instructor intent.

## H1 versus H4 origin

PATH_REMAINING_AT_CONFIRMATION, FIRST_ANY:

### H1

- 82 scored origin rows
- TARGET_FIRST: 42
- POINT_CHECK_FIRST: 40
- resolved target-first: 51.22%
- median MFE: 1,166.05
- median MAE: 952.65

### H4

- 94 scored origin rows
- TARGET_FIRST: 46
- POINT_CHECK_FIRST: 45
- neither: 3
- resolved target-first: 50.55%
- median MFE: 1,149.25
- median MAE: 945.00

Discovery does **not** show a meaningful simple H1-vs-H4 separation.

There is no basis here for inventing `H4 > H1` or `H1 > H4` priority.

## Same-direction timeframe context

PATH_REMAINING_AT_CONFIRMATION, FIRST_ANY:

### H1-only context

- 46 scored origin rows
- 45 contexts
- TARGET_FIRST: 22
- POINT_CHECK_FIRST: 24
- resolved target-first: 47.83%
- median MFE: 1,076.30
- median MAE: 1,095.50

### H4-only context

- 58 scored origin rows
- 55 contexts
- TARGET_FIRST: 26
- POINT_CHECK_FIRST: 30
- neither: 2
- resolved target-first: 46.43%
- median MFE: 1,084.05
- median MAE: 1,258.05

### H1+H4 same-side context

- 72 scored origin rows
- 33 contexts
- TARGET_FIRST: 40
- POINT_CHECK_FIRST: 31
- neither: 1
- resolved target-first: 56.34%
- median MFE: 1,208.45
- median MAE: 925.00

The H1+H4 context is directionally better than the H1-only and H4-only context in this discovery sample across target-first/MFE/MAE.

However, rows sharing the same day+side context are correlated and this is discovery data.

Therefore current status is:

`DISCOVERY LEAD — REPLICATION REQUIRED`

not a rule.

## Opposite-direction context conflict

A prior intuition could be that simultaneous opposite-direction surviving origins should invalidate entry.

The discovery data does **not** support making that assumption.

PATH_REMAINING_AT_CONFIRMATION, FIRST_ANY:

### No opposite-direction surviving origin

- 93 origin rows
- 74 contexts
- TARGET_FIRST: 43
- POINT_CHECK_FIRST: 49
- neither: 1
- resolved target-first: 46.74%
- median MFE: 1,109.60
- median MAE: 1,091.00

### Opposite-direction surviving origin present

- 83 origin rows
- 59 contexts
- TARGET_FIRST: 45
- POINT_CHECK_FIRST: 36
- neither: 2
- resolved target-first: 55.56%
- median MFE: 1,222.90
- median MAE: 945.00

In this discovery sample the conflict group is not worse; it is directionally better on these descriptive fields.

Therefore:

`OPPOSITE ORIGIN PRESENT -> VETO`

is specifically **not justified** by the current evidence.

This surprising relation may reflect confounding, proxy behavior, repeated-origin weighting, or market-state effects and must be replicated before interpretation.

## Confirmation Daily Frame variant

FIRST_ANY produced only:

- EXPECTED_SIDE: 175 scored origin rows
- CROSSED_SIDE: 1 scored origin row

FIRST_EXPECTED_SIDE produced 175 scored rows.

Therefore these two frozen variants are almost indistinguishable in discovery.

This does **not** prove Daily Frame side is unimportant.

It means that after the current source-partial origin filter, the first matching PAT2-BODY proxy is already on the research EXPECTED_SIDE in nearly every scored discovery case.

Possible explanations include real structural relation or proxy construction interaction; Q1 cannot distinguish them.

## Exact MTF alignment

FIRST_EXPECTED_SIDE scored rows:

- exact alignment count 1: 169 rows / 127 contexts
- count 2: 5 rows / 4 contexts
- count 3: 1 row / 1 context
- count 4: 0

Q1 therefore cannot meaningfully answer whether increasing exact simultaneous TF alignment improves the result.

The current exact-completion representation is too sparse above one TF for that question.

Do not convert this into a minimum-TF gate.

## Confirmation timeframe

FIRST_EXPECTED_SIDE:

- M5: 149 origin rows / 114 contexts
- M15: 17 / 14
- M30: 5 / 2
- H1: 4 / 2

The first confirmation is overwhelmingly M5 under this proxy.

Small H1/M30/M15 groups are insufficient for a trustworthy timeframe ranking.

## What discovery changes

The useful discovery lead is not a single entry rule.

It is a narrowing of the next questions:

1. simple H1-vs-H4 priority currently adds little;
2. H1+H4 same-direction context is worth replication;
3. opposite-direction surviving context must not be assumed to be a veto;
4. PATH_REMAINING_AT_CONFIRMATION currently fits the discovery data better than absolute ORIGIN_TARGET_LEVEL;
5. exact simultaneous MTF count is too sparse to answer the graded-confluence question;
6. first confirmation is mostly M5 under the current proxy representation.

## Replication decision

Run the same frozen V1 feature generator and the exact same Q1 scorer on:

`2023-09-01 -> 2023-11-23`

Reason:

- cache metadata reports complete range;
- no missing cache dates;
- later period than discovery;
- current Q1 plan named it before the discovery result was opened.

No Q1 code, target definition, eligibility rule, grouping definition, or confirmation variant may be changed before this replication.

## Local result artifacts

`results/0700_Q1_ORIGIN_CONTEXT/DISCOVERY_2022_09_TO_2023_03/Q1_ORIGIN_CONTEXT_EVENTS.csv`

- bytes: 228,769
- SHA256: `385697586031EA66F6F0C23A498D2691730310C660CAE96C80AA66FA10266C51`

`results/0700_Q1_ORIGIN_CONTEXT/DISCOVERY_2022_09_TO_2023_03/REPORT.json`

- bytes: 19,943
- SHA256: `6AC0EC0CCB31968C52C946C3E1B9CD9AF86E3BA61C58B04A2C237C70EF3987D1`

The large/local generated results remain reproducible artifacts rather than canonical claim files.

## Claim boundary

This checkpoint does not establish:

- a 07:00 profitable trading strategy;
- trade/system Win rate;
- H1/H4 priority;
- conflict veto;
- MTF minimum;
- exact PA/PAT;
- exact 50% denominator;
- universal SL;
- broker execution P&L.

Replication is required before even a research relationship is called stable.
