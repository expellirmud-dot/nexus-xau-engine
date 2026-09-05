# Post-SIG Invalidation Scanner — Ruff Fix — 2026-09-05

Status: LINT-ONLY FIX AFTER LOCAL TEST PASS

## Local runtime evidence supplied by project owner

- pytest: `118 passed, 116 warnings in 3.43s`
- Ruff stopped on three `RUF100` findings in `post_sig_invalidation_conflict_scan.py`

## Fix applied

Removed three unused `# noqa: E712` directives from boolean-filter lines.

No boolean predicate, invalidation condition, threshold, source interpretation, period rule, or cross-period decision logic was changed.

The frozen scanner semantics remain:

- BUY conflict: later M1 `Low < origin_anchor_price`
- SELL conflict: later M1 `High > origin_anchor_price`
- interval: `[origin_anchor_known_at, candidate_known_at)`
- equality does not count as destroyed in this strict-beyond representation
- no 200-point destruction buffer

## Validation status

The code logic had already passed the local pytest gate before this lint-only edit. Ruff must be rerun locally after pulling this commit before claiming the lint gate is closed.
