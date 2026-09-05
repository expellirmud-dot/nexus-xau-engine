# Ruff Import Format Gate Fix — 2026-09-05

Status: ENGINEERING CHECKPOINT / LINT-ONLY FIX

## Runtime evidence

The Windows research runner completed the full pytest gate:

- `108 passed`
- `15 warnings`
- runtime about `3.87s`

Ruff then reported one remaining issue:

- `I001 Import block is un-sorted or un-formatted`
- file: `src/nexus_xau/research/path_remaining_daily_side_mtf_relation_v2.py`

## Fix

The existing import of `enrich_events_with_mtf_alignment` was reformatted into Ruff's parenthesized import style.

No behavior, research formula, metric, threshold, period split, or closure rule was changed.

## Evidence discipline

This checkpoint does not modify:

- `PATH_REMAINING` representation;
- Daily Frame side semantics;
- MTF alignment freshness variants;
- Spearman relationship metrics;
- event sufficiency rule;
- cross-period decision rule;
- outcome calculations;
- strategy claims.

## Next step

Pull this checkpoint and rerun `scripts/run_path_remaining_daily_side_mtf_v2.ps1`. If Ruff passes, the runner should continue directly into the frozen three-period empirical V2 run and deterministic closure generation.
