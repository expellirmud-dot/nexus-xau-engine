# PATH_REMAINING × Daily Frame Side × Graded MTF — V2 Pre-Execution Freeze — 2026-09-05

Status: FROZEN BEFORE EMPIRICAL MTF-INTERACTION OUTPUT REVIEW

## Why V2 exists

The first implementation checkpoint introduced two new sufficiency gates:

- 40 events per Daily-Frame side;
- 10 events per exact alignment-count level.

Those values were not source rules and were not inherited from the parent Daily-Frame-side experiment. More importantly, the parent checkpoint had already shown later-period `EXPECTED_SIDE` counts of 22 and 9, so a 40-event side gate would structurally make those periods unusable before any new MTF-interaction outcome was inspected.

This V2 correction is therefore made **before empirical output review** for the new interaction equation. V1 is preserved in Git history and is not silently rewritten.

## Research-method alignment

User-direct operating guidance is relation-first:

```text
UNKNOWN
-> bounded variants
-> measure reproducibly
-> study how variables move together
-> compare periods / source consistency
-> close SUPPORTED / NOT_SUPPORTED / INCONCLUSIVE / INDISTINGUISHABLE
```

The test therefore treats `alignment_count` as a graded variable rather than inventing a production threshold such as `>=2` or `>=3`.

## Frozen equation under study

```text
PATH_REMAINING state
+ Daily Frame directional side
+ graded same-direction MTF alignment
-> PATH_REMAINING completion behavior
```

MTF set:

```text
H1 / M30 / M15 / M5
```

Existing bounded freshness variants remain unchanged:

1. `EXACT_COMPLETION`
2. `RECENT_1_TF_BAR`
3. `RECENT_2_TF_BARS`

No outcome may be used to choose one of these as the instructor's canonical freshness rule.

## V2 sufficiency rule

- Minimum events per Daily-Frame side = **10**, inherited from the already-frozen parent Daily-Frame-side checkpoint.
- At least two distinct `alignment_count` values must be observed.
- There is **no new minimum event threshold per exact alignment-count bin**.
- Exact-count bins remain descriptive; the primary graded relation is measured with Spearman correlation.

This is not a claim that 10 is a universal statistical standard. It is continuity with the parent interaction experiment so the child equation does not introduce a new post-hoc gate.

## Outcome dimensions

For each freshness variant and each Daily-Frame side:

- alignment count vs resolved target-first;
- alignment count vs PATH_REMAINING reach;
- alignment count vs fresh MFE;
- alignment count vs fresh MAE.

Expected directional relation:

```text
higher alignment
-> target-first rho > 0
-> PATH_REMAINING reach rho >= 0
-> MFE rho >= 0
-> MAE rho <= 0
```

Per-side state:

- `SUPPORT`
- `OPPOSE`
- `MIXED`
- `INSUFFICIENT`
- `INDISTINGUISHABLE`

## Period interaction state

- `SIDE_CONDITIONAL_SUPPORT`: EXPECTED_SIDE supports the graded relation while CROSSED_SIDE does not also support it.
- `GENERAL_MTF_SUPPORT_NOT_SIDE_SPECIFIC`: both sides support the graded relation.
- `EXPECTED_SIDE_OPPOSE`: EXPECTED_SIDE consistently moves opposite the expected relation.
- `EXPECTED_SIDE_INDISTINGUISHABLE`: expected-side data cannot distinguish alignment levels / outcome relation.
- otherwise `INCONCLUSIVE`.

## Cross-period freeze

Periods already used by the parent checkpoint are retained for consistency testing:

1. 2022-09-01 -> 2023-03-31
2. 2024-09-01 -> 2024-11-30
3. 2025-09-01 -> 2025-11-30

These are **not untouched final holdouts**.

Per freshness variant:

- >=2 `SIDE_CONDITIONAL_SUPPORT`, with no GENERAL and no EXPECTED_SIDE_OPPOSE -> `SUPPORTED_SIDE_CONDITIONAL_REPLICATION`
- >=2 `GENERAL_MTF_SUPPORT_NOT_SIDE_SPECIFIC`, with no SIDE and no OPPOSE -> `SUPPORTED_GENERAL_MTF_NOT_SIDE_SPECIFIC`
- >=2 total SIDE/GENERAL support periods, no OPPOSE -> `SUPPORTED_MTF_RELATION_SPECIFICITY_MIXED`
- >=2 `EXPECTED_SIDE_OPPOSE` -> `NOT_SUPPORTED_EXPECTED_SIDE`
- otherwise -> `INCONCLUSIVE`

The rule is frozen here before the batch output is inspected.

## Restart-safe batch execution

New modules:

```text
src/nexus_xau/research/path_remaining_daily_side_mtf_relation_v2.py
src/nexus_xau/research/path_remaining_daily_side_mtf_batch.py
```

The batch runner searches local gitignored research storage for:

- an `XAUUSD` / `M1` / `BID` CSV covering each period;
- the parent Daily-Frame/PATH_REMAINING interaction event table, identified by required columns and excluding already-enriched MTF tables.

It then writes period reports/events plus:

```text
results/PATH_REMAINING_DAILY_SIDE_MTF_V2/CROSS_PERIOD_SUMMARY.json
```

Run locally:

```powershell
cd D:\nexus-xau-engine-repo
git pull
.\.venv\Scripts\Activate.ps1
pytest
ruff check src tests
python -m nexus_xau.research.path_remaining_daily_side_mtf_batch
```

If auto-discovery cannot resolve an input unambiguously, stop and report the concrete missing/ambiguous path rather than guessing.

## Non-claims

- No production aligned-TF minimum.
- No canonical PAT2 formula.
- No canonical MTF freshness rule.
- No strategy win rate.
- No claim that CROSSED_SIDE is invalid.
- No claim that PATH_REMAINING is the instructor's exact formula.
- Historical outcomes cannot upgrade source provenance or define teacher intent.

## Checkpoint discipline

After local execution:

1. preserve raw output reports/events locally;
2. summarize each period and variant without changing the frozen rule;
3. close the equation with an allowed terminal state;
4. record what changed and what remains unknown;
5. update restart-safe project state;
6. commit and push the empirical closure checkpoint.
