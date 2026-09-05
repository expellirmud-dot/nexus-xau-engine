# Windows pytest temp permission workaround — 2026-09-05

Status: CLOSED / RUNTIME VERIFIED ENVIRONMENTAL FIX

## Observed runtime failure

On the project Windows PC, the V2 research runner initially reached pytest and reported:

- 101 tests passed;
- 7 tests errored before completing because pytest could not access the default temporary root under `%LOCALAPPDATA%\Temp\pytest-of-Expellirmud`;
- the exception was `PermissionError: [WinError 5] Access is denied`.

The failing tests were distributed across unrelated modules that all rely on pytest temporary paths. This pattern was environmental and did not identify a common research-logic defect.

## Fix

`scripts/run_path_remaining_daily_side_mtf_v2.ps1` invokes pytest with an explicit repository-local base temp:

```text
python -m pytest --basetemp .pytest-tmp-nexus-xau
```

The repository already ignores `.pytest-tmp-*/`, so temporary test artifacts remain local and are not committed.

## Runtime verification

After applying the repository-local base temp, the project owner reran the suite on the Windows research PC and reported:

```text
108 passed in 6.61s
```

No pytest errors were reported in that rerun.

Decision: the Windows pytest temp-permission blocker is CLOSED for the current environment.

## Evidence discipline

This checkpoint only changes and validates the test runtime environment. It does not modify:

- PATH_REMAINING representation;
- Daily Frame side semantics;
- MTF alignment variants;
- closure rules;
- outcome calculations;
- strategy claims.

The passing test suite validates the current code test gate only. It does not itself validate the empirical trading hypothesis or produce a strategy win rate.

## Next step

Continue the same one-command research runner through Ruff, the frozen V2 multiperiod empirical run, and deterministic closure generation. If Ruff or the empirical stage fails, treat that as a separate checkpoint and preserve this environmental closure.
