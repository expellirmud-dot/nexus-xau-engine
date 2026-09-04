# PATH_REMAINING × Daily Frame Side × Graded MTF V2 — Autoclosure Checkpoint — 2026-09-05

Status: IMPLEMENTED / READY FOR LOCAL EMPIRICAL EXECUTION

## Purpose

Continue the user-directed equation-proof workflow without changing the frozen research rule after outcomes are observed.

The V2 batch runner now performs four stages in one command:

1. pytest;
2. ruff;
3. frozen multi-period V2 relation batch;
4. deterministic Markdown closure rendering from the generated JSON.

## New component

`src/nexus_xau/research/path_remaining_daily_side_mtf_closure.py`

This renderer does not make a second research decision. It copies the already-frozen cross-period decision and period states from `CROSS_PERIOD_SUMMARY.json`, then exposes period/side relation metrics and descriptive outcome levels in a restart-safe Markdown artifact.

Generated local artifact:

`results/PATH_REMAINING_DAILY_SIDE_MTF_V2/EMPIRICAL_CLOSURE.md`

## Research-integrity effect

This reduces post-result narrative flexibility:

- no new threshold is introduced while rendering;
- no freshness variant is promoted to canonical from outcome performance;
- no aligned-TF production minimum is chosen;
- PAT2 BODY remains a research proxy;
- PATH_REMAINING remains a research representation;
- target-first is not labeled strategy win rate;
- previously used periods remain replication/interaction evidence, not untouched final-holdout confirmation.

## Validation added

`tests/test_path_remaining_daily_side_mtf_closure.py`

The tests verify that the renderer preserves the frozen cross-period decision, carries research guards into the Markdown, and writes a deterministic closure artifact.

## One-command execution

```powershell
cd D:\nexus-xau-engine-repo
git pull
.\scripts\run_path_remaining_daily_side_mtf_v2.ps1
```

Expected final artifacts:

- `results/PATH_REMAINING_DAILY_SIDE_MTF_V2/CROSS_PERIOD_SUMMARY.json`
- `results/PATH_REMAINING_DAILY_SIDE_MTF_V2/EMPIRICAL_CLOSURE.md`
- one report JSON and enriched event CSV per frozen historical period.

## Checkpoint boundary

This engineering checkpoint is complete and pushed. Empirical closure is still pending local execution because the raw Dukascopy research datasets and prior interaction event tables are intentionally gitignored/local. No empirical result is claimed by this checkpoint.

## Next action after local execution

Read the generated cross-period state without changing the frozen rule. Then persist the empirical closure in project documentation, update restart-safe research state, commit and push. If the result is unstable/inconclusive, move to the pre-existing next bounded family: origin expiry/invalidation, origin age, consumed-run ratio, and same-day versus older inherited-origin relations.
