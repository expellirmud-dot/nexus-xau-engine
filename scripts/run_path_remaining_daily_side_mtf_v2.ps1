$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    throw "Missing .venv. Expected .\.venv\Scripts\python.exe"
}

$Python = ".\.venv\Scripts\python.exe"

Write-Host "[1/3] pytest"
& $Python -m pytest
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "[2/3] ruff"
& $Python -m ruff check src tests
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "[3/3] PATH_REMAINING x Daily Side x Graded MTF V2"
& $Python -m nexus_xau.research.path_remaining_daily_side_mtf_batch
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Completed. Summary: results\PATH_REMAINING_DAILY_SIDE_MTF_V2\CROSS_PERIOD_SUMMARY.json"
