$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    throw "Missing .venv. Expected .\.venv\Scripts\python.exe"
}

$Python = ".\.venv\Scripts\python.exe"
$PytestTemp = ".pytest-tmp-post-sig-invalidation"
$OutputRoot = "results\POST_SIG_INVALIDATION_CONFLICT_SCAN"

Write-Host "[1/3] pytest"
& $Python -m pytest --basetemp $PytestTemp
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "[2/3] ruff"
& $Python -m ruff check src tests
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "[3/3] source-partial post-SIG invalidation conflict scan"
& $Python -m nexus_xau.research.post_sig_invalidation_conflict_batch `
  --output-root $OutputRoot
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Completed."
Write-Host "Summary: $OutputRoot\CROSS_PERIOD_SUMMARY.json"
