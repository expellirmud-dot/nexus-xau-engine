# 07:00 Current-Day Input Route — 2026-10-08

Status: READY_WAITING_FOR_CHECKPOINT_DATA / READ-ONLY / ORDER SEND DISABLED

## Goal

Calculate the operational `0700_STATE_PACKET_H4_V0` for
`2026-10-08 07:00 Asia/Bangkok = 2026-10-08 00:00 UTC`
from observed real input, without fabricating future or missing data.

## MT5 route

Current terminal process is running, but MetaTrader5 initialize returns:

`(-6, "Terminal: Authorization failed")`

The MT5 journal narrows the cause to:

`authorization on Exness-MT5Trial17 failed (Invalid account)`

This is an account/session validity failure, not a calculator-logic failure.

No credential guessing, password extraction, account creation, or order send was
performed.

## Exness archive discovery

The existing Exness archive family exposes current-month daily subdirectories in
addition to the lagging monthly ZIP.

Observed at approximately 2026-10-07 23:xx UTC:

- October monthly ZIP is AVAILABLE but ends at
  `2026-10-06T23:59:59.547Z`;
- month directory contains daily subdirectory `07/`;
- `07/Exness_XAUUSDm_2026_10_07.zip` mtime was
  `2026-10-07 23:01:24 GMT`;
- validated daily ZIP contained 255,142 rows;
- first tick: `2026-10-07T00:00:00.047Z`;
- last tick at that observation: `2026-10-07T23:00:34.126Z`;
- provider mismatch: 0;
- symbol mismatch: 0;
- Ask < Bid: 0;
- timestamp regression: 0;
- exact duplicate rows: 0.

This proves the daily archive route updates intraday and is materially fresher than
the current monthly ZIP.

## Implemented runner

`scripts/exness_intraday_state_packet_0700.py`

The runner reuses existing Project components:

- Exness archive directory acquisition;
- archive ZIP validator V0.2;
- archive CSV/tick parser;
- archive Bid tick -> M1 builder;
- `0700_STATE_PACKET_H4_V0`.

It does not introduce a new market formula.

Operational epoch for this current-day archive lane:

`2026-10-01T00:00:00Z`

This is explicitly an `OPERATIONAL_EXPLICIT_EPOCH` Project engineering
convention, not source-pure historical completeness.

## Pre-checkpoint dry run

Before 07:00 Thailand, the runner acquired and validated available daily archive
snapshots for 2026-10-01 through 2026-10-07.

2026-10-03 had no remote day directory, consistent with an observed non-trading
interval; no missing ticks/bars were fabricated.

2026-10-08 daily snapshot was not yet available because the checkpoint had not
occurred.

Expected fail-closed result:

`BOUNDARY_MINUTE_NOT_AVAILABLE: checkpoint day snapshot not available`

Ruff for the runner: PASS.

## Defect found during dry run

The first draft incorrectly rejected duplicate timestamps in the tick index.

Exness archive validation already permits multiple raw ticks at the same timestamp
while preserving raw order. The runner was corrected to preserve same-timestamp
ticks and rely on the existing replay contract.

This was an engineering correctness fix; no market outcome was used.

## Post-checkpoint requirement

After 00:00 UTC:

1. refresh the Exness daily archive directory;
2. require a validated 2026-10-08 daily snapshot;
3. require at least one observed tick inside the 00:00 UTC boundary minute;
4. rebuild Bid M1 from the declared epoch through the checkpoint minute;
5. calculate the operational 07:00 State Packet;
6. keep SOURCE_PURE canonical completeness separate;
7. do not open protected holdout/economic scoring or send orders.

Until step 2/3 is satisfied, the correct result remains
`BOUNDARY_MINUTE_NOT_AVAILABLE`.
