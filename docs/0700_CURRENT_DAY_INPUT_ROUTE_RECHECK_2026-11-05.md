# 07:00 Current-Day Input Route Recheck — 2026-11-05

Status: RECHECK_CLOSED_DAILY_ROUTE_OBSOLETE_AT_REMOTE / MONTH_ROUTE_DATA_PRESENT / OWNER_DECISION_REQUIRED / READ-ONLY / ORDER SEND DISABLED

## Question

The frozen next action (2026-10-08) was: at/after the 2026-10-08 07:00
Asia/Bangkok checkpoint, refresh the Exness intraday daily archive and compute
the operational `0700_STATE_PACKET_H4_V0`, remaining fail-closed if the
boundary minute was absent. The checkpoint date passed without a post-window
run. This document records the targeted recheck on 2026-11-05.

No rule, threshold, geometry, or representation was changed. This is an
input-route/source-availability recheck only.

## Bootstrap evidence (Tier 0 + preflight)

- Continuity capsule and `docs/CURRENT_RESEARCH_STATE.json` agree
  (`updated_at = 2026-10-08T06:25:45+07:00`); no STATE_DRIFT.
- `scripts/research_preflight.py` -> `NEXUS_RESEARCH_PREFLIGHT=PASS`.
- `research_queue/QUEUE.json` -> `active = null`.
- Prior run evidence `results/state_packet_0700/XAUUSDm_2026-10-08_intraday_acquisition.json`
  (observed 2026-10-07T23:24 UTC, pre-window) showed 2026-10-08
  `REMOTE_DAY_NOT_AVAILABLE`, which was the correct fail-closed result at that
  time. The 2026-10-08 route document remains historical evidence and is not
  erased.

## Durable-execution recovery

- The Local Work Agent heartbeat was stale at 2026-10-10T13:06 UTC with a dead
  PID; queued work was not being picked up.
- The daemon was restarted on 2026-11-05 and the recheck was submitted as
  durable job `XAU-0700-STATEPACKET-RECHECK-20261105-R1`
  (registry: `D:/tools/nexus-durable-work/_agent/jobs/`).
- Submission-syntax failures (literal `--` token; relative interpreter path not
  resolvable by the runner) were fixed by using absolute paths. These were
  tooling failures, not research results.

## Recheck result (Source Fact, observed 2026-11-05T10:42 UTC)

The unchanged daily-route runner re-acquired the archive set and returned:

`status = BLOCKED`
`reason = BOUNDARY_MINUTE_NOT_AVAILABLE: checkpoint day snapshot not available`

Acquisition report:
`results/state_packet_0700/XAUUSDm_2026-10-08_intraday_acquisition_r20261105.json`

Every snapshot 2026-10-01..2026-10-08 returned `REMOTE_DAY_NOT_AVAILABLE`,
including days previously VALIDATED.

## Direct remote probes (Source Fact)

- `https://ticks.ex2archive.com/ticks/XAUUSDm/2026/10/` -> HTTP 200, empty
  link listing (no day subdirectories).
- `https://ticks.ex2archive.com/ticks/XAUUSDm/2026/10/08/` -> HTTP 404.
- `https://ticks.ex2archive.com/ticks/XAUUSDm/2026/10/01/Exness_XAUUSDm_2026_10_01.zip`
  -> HTTP 404 (the exact URL previously validated is gone).
- `https://ticks.ex2archive.com/ticks/XAUUSDm/2026/09/` -> month ZIP listing
  only.
- `https://ticks.ex2archive.com/ticks/XAUUSDm/2026/10/Exness_XAUUSDm_2026_10.zip`
  -> HTTP 200, 55,936,122 bytes, single entry
  `Exness_XAUUSDm_2026_10.csv`.

Derived interpretation (analyst inference, not source statement): the remote
archive family has rotated from the previously observed daily-subdirectory
layout to a month-only ZIP layout for 2026-10. This changes the factual basis
of the 2026-10-08 discovery note, which assumed daily subdirectories remain
available alongside the monthly ZIP.

## Boundary-minute verification from the month ZIP (Source Fact)

Streaming the live October month ZIP:

- ticks matching `2026-10-08 00:00 UTC` (boundary minute): 269;
- first boundary tick: `2026-10-08 00:00:00.017Z`, Bid 4108.073, Ask 4108.313.

The 2026-10-08 07:00 checkpoint input data therefore exists at the remote, but
only through the month-ZIP route, not the frozen daily-archive route.

Local cache note: `data/raw/exness_tick_history/current_month_probe/XAUUSDm/2026/Exness_XAUUSDm_2026_10.zip`
(mtime 2026-10-08 06:12 local, 10,559,958 bytes) is a stale partial snapshot of
the same month ZIP; it is not evidence of final month coverage.

## What this does and does not establish

Established:

- The daily-route runner remains correct and fails closed as designed.
- The 2026-10-08 checkpoint data is observable now, via the month ZIP.
- The prior REMOTE_DAY_NOT_AVAILABLE result was real remote-availability
  loss, not a transient network error.

NOT established / prohibited:

- No State Packet was computed for 2026-10-08.
- A month-route input path for `0700_STATE_PACKET_H4_V0` is not implemented or
  frozen; the existing month-window tooling has not been validated against
  this contract's fail-closed requirements in this recheck.
- Retroactive computation of an operational current-day checkpoint after the
  fact is a scope/representation decision reserved to the owner.
- No holdout/economic scoring, no Win/Loss, no profitability claims, no order
  send. All remain disabled.

## Next action (owner decision required)

1. Decide the route forward: (a) implement/revalidate a month-ZIP input route
   for the 07:00 state packet (source-availability reopen trigger), (b) define
   a forward current-day checkpoint procedure that tolerates remote layout
   changes, or (c) close the 2026-10-08 current-day objective as
   `DATA_ROUTE_OBSOLETE_BEFORE_POST_WINDOW_RUN` with this document as closure.
2. Until chosen, the 2026-10-08 objective stays recorded as blocked at the
   input-route layer; calculator logic status is unchanged.
3. Keep `results/` artifacts local per gitignore policy; their paths and the
   key numbers are preserved in this document.
