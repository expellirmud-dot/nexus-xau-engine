# Windows pytest temp permission workaround — 2026-09-05

Status: ENGINEERING CHECKPOINT / ENVIRONMENTAL FIX

## Observed runtime failure

On the project Windows PC, the V2 research runner reached pytest and reported:

- 101 tests passed;
- 7 tests errored before completing because pytest could not access the default temporary root under `%LOCALAPPDATA%\Temp\pytest-of-Expellirmud`;
- the exception was `PermissionError: [WinError 5] Access is denied`.

The failing tests were distributed across unrelated modules that all rely on pytest temporary paths. This pattern is environmental and does not identify a common research-logic defect.

## Fix

`scripts/run_path_remaining_daily_side_mtf_v2.ps1` now invokes pytest with an explicit repository-local base temp:

```text
python -m pytest --basetemp .pytest-tmp-nexus-xau
```

The repository already ignores `.pytest-tmp-*/`, so temporary test artifacts remain local and are not committed.

## Evidence discipline

This checkpoint only changes the test runtime environment. It does not modify:

- PATH_REMAINING representation;
- Daily Frame side semantics;
- MTF alignment variants;
- closure rules;
- outcome calculations;
- strategy claims.

The full test suite must be rerun on the Windows PC before the empirical V2 checkpoint can be considered validated.

## Next step

Run the same one-command research script again. If pytest and Ruff pass, continue automatically into the frozen V2 multiperiod empirical run and deterministic closure generation.
