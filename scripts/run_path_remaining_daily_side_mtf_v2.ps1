$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    throw "Missing .venv. Expected .\.venv\Scripts\python.exe"
}

$Python = ".\.venv\Scripts\python.exe"
$OutputRoot = "results\PATH_REMAINING_DAILY_SIDE_MTF_V2"
$Summary = "$OutputRoot\CROSS_PERIOD_SUMMARY.json"
$Closure = "$OutputRoot\EMPIRICAL_CLOSURE.md"

Write-Host "[1/4] pytest"
& $Python -m pytest
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "[2/4] ruff"
& $Python -m ruff check src tests
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "[3/4] PATH_REMAINING x Daily Side x Graded MTF V2"
& $Python -m nexus_xau.research.path_remaining_daily_side_mtf_batch --output-root $OutputRoot
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "[4/4] deterministic empirical closure markdown"
& $Python -m nexus_xau.research.path_remaining_daily_side_mtf_closure `
  --summary $Summary `
  --out $Closure
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Completed."
Write-Host "Summary: $Summary"
Write-Host "Closure: $Closure"
