# PATH_REMAINING × Daily Frame Side × Graded MTF Alignment — Test Plan — 2026-09-05

Status: FROZEN BEFORE HISTORICAL EVALUATION

## Goal

Continue the project-owner research method for unknown/graded relationships:

```text
if X changes -> measure whether Y/Z change with it
```

Do not invent a hard threshold such as `aligned_tf_count >= N`.

## Exact question

Within events already classified as `INHERITED_REMAINING_RUN`, after conditioning on the 07:00 Daily Frame directional side, does increasing same-direction PA/PAT research-proxy alignment across H1/M30/M15/M5 relate to better completion behavior of `PATH_REMAINING`?

Secondary interaction question:

- Is the graded MTF relation visible mainly on `EXPECTED_SIDE`?
- Is it also visible on `CROSSED_SIDE`, implying a more general MTF relation rather than a Daily-Frame-side-specific interaction?

## Evidence basis

- User-direct MTF clarification: more same-direction H1/M30/M15/M5 alignment is stronger/preferable; no mandatory minimum count is established.
- Prior checkpoint: `PATH_REMAINING + Daily Frame EXPECTED_SIDE` is a `SUPPORTED_RESEARCH_REPRESENTATION` across two usable periods.
- PAT2 BODY remains a research proxy, not canonical full PA.
- `PATH_REMAINING` remains a research representation, not a proven teacher formula.

## Frozen measurable representation

For every existing Daily-Frame/remaining-run interaction event:

```text
frame_side = EXPECTED_SIDE | CROSSED_SIDE
alignment_count = 0..4
aligned_tf_set = subset(H1,M30,M15,M5)
```

Alignment is computed only from PA/PAT2-BODY proxy events that are known at or before `candidate_known_at`.

Three bounded freshness variants are retained from the existing MTF experiment:

```text
EXACT_COMPLETION
RECENT_1_TF_BAR
RECENT_2_TF_BARS
```

These are research variants. Historical performance cannot promote one into the canonical teaching rule.

## Outcomes

Use the already-produced `PATH_REMAINING` outcomes from the interaction event table:

- target-first rate among resolved events;
- `PATH_REMAINING` reach rate;
- fresh MFE median;
- fresh MAE median.

No new trade entry, SL, TP, win-rate, or production execution rule is introduced.

## Relationship measurements

For each freshness variant and each Daily Frame side:

1. count events at each `alignment_count`;
2. report outcome summary for every count level;
3. Spearman relation between `alignment_count` and:
   - target-first binary;
   - PATH_REMAINING reach;
   - fresh MFE;
   - fresh MAE;
4. retain the exact aligned-TF set for future composition analysis.

This is deliberately a graded relation test, not a threshold scan.

## Frozen minimums

- minimum side-group events: 40;
- minimum events per alignment level: 10;
- at least 2 alignment levels meeting the minimum are required for a side relation to be called usable.

## Per-side relation state

`SUPPORT` only when all are true on a usable group:

- Spearman(alignment_count, target-first) > 0;
- Spearman(alignment_count, PATH_REMAINING reach) >= 0;
- Spearman(alignment_count, fresh MFE) >= 0;
- Spearman(alignment_count, fresh MAE) <= 0.

`OPPOSE` only when all four core directions are reversed/non-supportive:

- target-first <= 0;
- reach <= 0;
- MFE <= 0;
- MAE >= 0.

Otherwise: `MIXED`.

Insufficient sample: `INSUFFICIENT`.

## Period interaction state

For each period/freshness variant:

- EXPECTED=`SUPPORT`, CROSSED!=`SUPPORT` -> `SIDE_CONDITIONAL_SUPPORT`
- EXPECTED=`SUPPORT`, CROSSED=`SUPPORT` -> `GENERAL_MTF_SUPPORT_NOT_SIDE_SPECIFIC`
- EXPECTED=`OPPOSE` -> `EXPECTED_SIDE_OPPOSE`
- otherwise -> `INCONCLUSIVE`

## Multi-period closure discipline

Run the same frozen calculation independently on the existing comparison periods used by the prior Daily-Frame-side checkpoint.

Project-level closure must not be chosen from the best-looking period. It will be based on replication across usable periods and may close as:

- `SUPPORTED_RESEARCH_REPRESENTATION`
- `NOT_SUPPORTED`
- `INCONCLUSIVE`
- `INDISTINGUISHABLE`
- `NOT_TESTABLE_WITH_CURRENT_EVIDENCE`

## Guardrails

- Do not choose a production minimum aligned-TF count from historical performance.
- Do not use outcome results to claim the instructor's exact PA geometry or freshness window.
- Do not call target-first rate strategy win rate.
- Do not reinterpret `CROSSED_SIDE` as automatically invalid.
- Do not let this test alter the already-preserved historical evidence.
