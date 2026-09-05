# Source-Partial Re-Anchored Daily-Side — Ruff Import Fix — 2026-09-05

Status: IMPLEMENTATION HYGIENE / RUNTIME RETEST REQUIRED

## Runtime evidence before this fix

Project-owner Windows runtime reported:

```text
124 passed, 116 warnings in 3.53s
```

The subsequent Ruff gate stopped on one `I001` import-formatting error in:

`src/nexus_xau/research/source_partial_reanchored_daily_side_batch.py`

## Change

Applied only Ruff's import-organization requirement for imports from:

`nexus_xau.research.source_partial_reanchored_remaining_run`

No research logic was changed.

Specifically unchanged:

- source-partial strict structural invalidation;
- newest-to-oldest re-anchoring selection;
- nominal H1 1,000-point incompletion checks;
- no 200-point buffer;
- no age/expiry threshold;
- Daily Frame side definition;
- PATH_REMAINING representation;
- frozen cross-period decision rule.

## Validation status

Pytest for the code immediately before this formatting-only change is locally confirmed at `124 passed`.

Ruff and the empirical three-period re-anchor batch must be rerun after pulling this commit before any empirical re-anchor conclusion is recorded.
