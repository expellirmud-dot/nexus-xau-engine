$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    throw "Missing .venv. Expected .\.venv\Scripts\python.exe"
}

$Python = ".\.venv\Scripts\python.exe"
$PytestTemp = ".pytest-tmp-source-partial-reanchor-$([guid]::NewGuid().ToString('N'))"
$OutputRoot = "results\SOURCE_PARTIAL_REANCHORED_REMAINING_RUN"

Write-Host "pytest basetemp: $PytestTemp"
Write-Host "[1/3] pytest"
& $Python -m pytest --basetemp $PytestTemp
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "[2/3] ruff"
& $Python -m ruff check src tests
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "[3/3] source-partial re-anchored remaining-run + Daily-side retest"
& $Python -m nexus_xau.research.source_partial_reanchored_daily_side_batch `
  --output-root $OutputRoot
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Completed."
Write-Host "Summary: $OutputRoot\CROSS_PERIOD_SUMMARY.json"
