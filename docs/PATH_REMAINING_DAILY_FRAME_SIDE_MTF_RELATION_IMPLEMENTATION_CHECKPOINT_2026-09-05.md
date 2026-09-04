# PATH_REMAINING × Daily Frame Side × Graded MTF — Implementation Checkpoint — 2026-09-05

Status: IMPLEMENTED / READY FOR LOCAL HISTORICAL EXECUTION

## Completed in this checkpoint

1. Frozen the relation-test question and closure rule before inspecting new outcomes.
2. Added `src/nexus_xau/research/path_remaining_daily_side_mtf_relation.py`.
3. Added unit tests in `tests/test_path_remaining_daily_side_mtf_relation.py`.
4. Preserved graded `alignment_count` and exact `aligned_timeframes` set; no hard aligned-TF gate is selected.
5. Reused the existing H1/M30/M15/M5 PAT2-BODY research proxy and its three frozen freshness variants.
6. Conditioned results separately by `EXPECTED_SIDE` and `CROSSED_SIDE` under existing `PATH_REMAINING` events.

## Frozen relation outputs

Per freshness variant and Daily Frame side, the engine reports:

- event count by `alignment_count`;
- target-first rate among resolved events by count;
- PATH_REMAINING reach rate by count;
- fresh MFE median by count;
- fresh MAE median by count;
- Spearman relation of alignment count against all four outcome dimensions;
- exact aligned-TF-set frequencies.

## Period interaction labels

- `SIDE_CONDITIONAL_SUPPORT`
- `GENERAL_MTF_SUPPORT_NOT_SIDE_SPECIFIC`
- `EXPECTED_SIDE_OPPOSE`
- `INCONCLUSIVE`

These are research labels only.

## Required local validation before empirical closure

The GitHub connector can persist and push source changes but cannot execute against the project's local/raw historical datasets. Therefore the next step is to run the frozen code locally on each independent period used by the preceding Daily-Frame-side checkpoint.

Minimum validation sequence:

```powershell
cd D:\nexus-xau-engine-repo
git pull
.\.venv\Scripts\Activate.ps1
pytest
ruff check src tests
```

Then run, per historical period:

```powershell
python -m nexus_xau.research.path_remaining_daily_side_mtf_relation `
  --m1 <PERIOD_M1_CSV> `
  --interaction-events <PERIOD_DAILY_FRAME_REMAINING_INTERACTION_EVENTS_CSV> `
  --report <PERIOD_MTF_RELATION_REPORT_JSON> `
  --events <PERIOD_MTF_RELATION_EVENTS_CSV>
```

Use the same positive-volume research filter as the preceding interaction work unless explicitly testing a data-quality variant.

## Empirical closure discipline

Do not alter the frozen signs, minimum group sizes, freshness variants, or relation metrics after seeing the period outputs.

After all usable periods are run:

1. record each period/variant state;
2. compare replication across periods;
3. close the checkpoint as SUPPORTED / NOT_SUPPORTED / INCONCLUSIVE / INDISTINGUISHABLE / NOT_TESTABLE_WITH_CURRENT_EVIDENCE;
4. document what changed and what remains unknown;
5. update restart-safe state;
6. commit/push closure.

## Git maintenance

This checkpoint was pushed directly to the existing branch `build/python-replay-engine` through normal non-destructive repository writes. No historical evidence was deleted or rewritten.

## Non-claims

- No production minimum aligned-TF count.
- No canonical PAT2 formula.
- No canonical freshness rule.
- No strategy win rate.
- No claim that CROSSED_SIDE is invalid.
- No claim that PATH_REMAINING is the instructor's exact formula.
