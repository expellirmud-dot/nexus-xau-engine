# Post-SIG invalidation runner — unique pytest basetemp fix — 2026-09-05

Status: ENGINEERING FIX / NO RESEARCH-LOGIC CHANGE

## Runtime evidence from project PC

The post-SIG invalidation runner produced:

```text
110 passed, 117 warnings, 8 errors
```

All eight errors were Windows `PermissionError: [WinError 5] Access is denied` failures against the fixed repository-local pytest base directory:

```text
.pytest-tmp-post-sig-invalidation
```

These were setup/infrastructure errors rather than assertion failures from the research logic.

## Fix

The runner now generates a fresh UUID-suffixed pytest basetemp on every execution:

```text
.pytest-tmp-post-sig-invalidation-<uuid>
```

This avoids pytest attempting to reuse/remove a stale directory whose Windows ACL/lock state may have become unusable.

The repository already ignores `.pytest-tmp-*/`, so these local runtime directories are not intended for Git.

## Non-change guard

This checkpoint does not change:

- BUY invalidation predicate;
- SELL invalidation predicate;
- strict-beyond equality handling;
- zero-buffer policy;
- scan interval;
- cross-period decision rule;
- any historical research result.

## Validation status

The unique-basetemp runner change has been pushed but is not yet claimed runtime-passing until rerun on the project PC.

Run:

```powershell
cd D:\nexus-xau-engine-repo
git pull
.\scripts\run_post_sig_invalidation_conflict_scan.ps1
```
