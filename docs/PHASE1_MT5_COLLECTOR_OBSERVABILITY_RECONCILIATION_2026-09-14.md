# Phase 1 MT5 Collector Observability Reconciliation — 2026-09-14

Status: V01 FAILURE PRESERVED / V02 RUNNING AFTER FIX

## Failure observed

Durable job:

XAU-MT5-FORWARD-COLLECTOR-1H-20260914

ended FAILED after 3 attempts.

All attempts failed with Windows PermissionError while replacing:

results/mt5_collector/status.json

Root cause:

dashboard/corner readers could briefly hold status.json while the collector used atomic os.replace(). The status surface is auxiliary, but the write failure was allowed to terminate the collector.

SQLite market-data storage was not reported corrupt. The stale status file could remain RUNNING after the process died, so status freshness also needed explicit handling.

## Fix

Repo commit:

14f3239 ui: add collector corner monitor and status hardening

Changes:

- status-file os.replace retries transient Windows sharing contention;
- status-surface write failure is best-effort and no longer kills tick collection;
- corner monitor marks active-looking status as STALE when status updates stop;
- user field guide added;
- desktop corner monitor added.

Shared durable infrastructure was also corrected:

D:\tools\nexus-durable-work\job_runner.py

New child launches now include CREATE_NO_WINDOW as well as CREATE_NEW_PROCESS_GROUP.

This means new durable jobs do not require a visible Python console window.

## Replacement durable run

Durable job:

XAU-MT5-FORWARD-COLLECTOR-1H-V02-20260914

Observed after launch:

- status: RUNNING
- attempts: 1
- collector status: RUNNING
- mode: READ_ONLY_DATA_ORDER_SEND_DISABLED
- gap_counts: {}
- last_error: null
- dashboard and corner readers active concurrently
- status.json continued updating after the prior contention window
- no new visible durable child console window was observed

This is current runtime evidence, not yet proof of indefinite reliability.

## Operator surfaces

Full browser dashboard:

http://127.0.0.1:8765/

Desktop corner status:

scripts\START_MT5_COLLECTOR_CORNER.cmd

The corner status reads status.json + SQLite directly. The browser is optional.

Closing the browser or corner status does not stop the collector.

Field explanation:

docs/MT5_COLLECTOR_DASHBOARD_FIELD_GUIDE_2026-09-14.md

## Important operating rule

Do not start a second collector against the same SQLite store while V02 is active.

After reconnect, inspect the durable job and collector status before starting another process.

Automatic order execution remains disabled.
