$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    throw "Missing .venv. Expected .\.venv\Scripts\python.exe"
}

$Python = ".\.venv\Scripts\python.exe"
$PytestTemp = ".pytest-tmp-nexus-xau"
$OutputRoot = "results\INHERITED_ORIGIN_CONTEXT_RELATION"

Write-Host "[1/3] pytest"
& $Python -m pytest --basetemp $PytestTemp
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "[2/3] ruff"
& $Python -m ruff check src tests
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "[3/3] inherited origin context x Daily Frame side"
& $Python -m nexus_xau.research.inherited_origin_context_batch `
  --results-root results `
  --output-root $OutputRoot
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Completed."
Write-Host "Summary: $OutputRoot\CROSS_PERIOD_SUMMARY.json"
