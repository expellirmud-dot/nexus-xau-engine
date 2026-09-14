# Phase 1 MT5 Forward Collector Operational Start — 2026-09-14

Status: DURABLE READ-ONLY OBSERVATION RUNNING

Collector:
- version: PHASE1_MT5_FORWARD_COLLECTOR_V0.1
- mode: READ_ONLY_DATA_ORDER_SEND_DISABLED
- symbol: XAUUSDm
- local store: data/raw/mt5/XAUUSDm_ticks.sqlite3
- status: results/mt5_collector/status.json

Durable job:
- id: XAU-MT5-FORWARD-COLLECTOR-1H-20260914
- execution: D:/tools/nexus-durable-work Local Work Agent
- duration: 3600 seconds
- poll parameter: 1 second
- backfill chunk parameter: 30 seconds
- retry policy: auto_retry
- max retries: 2

Local dashboard:
- http://127.0.0.1:8765/
- read-only status surface
- no trading/execution controls

Initial live verification after durable start:
- durable job status: RUNNING
- dashboard collector state: RUNNING
- total ticks: 2358
- rows committed in current session: 1433
- gap counts: {}
- last error: none

Interpretation:
The forward collector is now operating as a durable read-only job rather than relying on the chat/Bridge process session.

This is an operational observation run, not proof of indefinite reliability.

Resume rule:
After reconnect/new session, inspect this durable job and the collector status/database before starting another collector process.

Automatic order execution remains disabled.
