# 07:00 Route Probe Log

Purpose: record promoted state transitions from the decision-neutral 07:00 route
availability observer defined in
[`docs/0700_ROUTE_PROBE_AUTOMATION_CONTRACT_V0_1_2026-11-05.md`](0700_ROUTE_PROBE_AUTOMATION_CONTRACT_V0_1_2026-11-05.md).
Every entry below is **existence evidence only; never route authority**.

## Vocabulary

Copied verbatim from contract section 6. Free-text status strings are prohibited,
because prose is how an observer gets misread as a conclusion.

| field | allowed values |
|---|---|
| `daily_route` | `PRESENT`, `ABSENT`, `LISTING_UNREADABLE`, `NOT_PROBED` |
| `month_route` | `PRESENT_CHANGED`, `PRESENT_UNCHANGED`, `ABSENT`, `LISTING_UNREADABLE`, `NOT_PROBED` |
| `inbox` | `NO_NEW_FILES`, `NEW_FILES`, `DIR_MISSING`, `NOT_PROBED` |
| `boundary_minute_tick_count` | integer, or `null` when the scan was not performed |

`daily_route = PRESENT` means the checkpoint day appears as a **subdirectory of
the month listing**. The probe does not open that subdirectory, so `PRESENT` is
not evidence that a day ZIP exists, and it is certainly not evidence that the
day ZIP holds the boundary minute.

## Rounds

### Round 1 — first live round (implementation day)

```
at_utc: 2026-11-05T12:30:00+00:00   (05 Nov 2026 19:30 Asia/Bangkok)
daily_route: PRESENT
month_route: PRESENT_CHANGED
inbox: NEW_FILES
boundary_minute_tick_count: 0
error_class: null
forced: true
retry_count: 0
elapsed_ms: 6578
month_zip_fingerprint after: 9255481:Thu, 05 Nov 2026 01:41:16 GMT
```

Command as run (from the repository root, watch directory created first):

```
.venv\Scripts\python.exe scripts/exness_0700_route_probe.py --once --force \
  --checkpoint-day 2026-11-05 --watch-dir "D:/tools/nexus-0700-watch"
```

Machine record: `D:\tools\nexus-0700-watch\observations.ndjson`, line 1.

Source Facts established by this round, each bounded by its timestamp:

- The 2026-11-05 subdirectory **is** listed under
  `ticks/XAUUSDm/2026/11/` (mtime `Thu, 05 Nov 2026 12:21:19 GMT`), alongside
  `01`…`04`. This is a different remote layout from the one recorded for
  2026-10 in `docs/0700_CURRENT_DAY_INPUT_ROUTE_RECHECK_2026-11-05.md`, where
  the October month listing returned **no** day subdirectories at all.
- The November month ZIP exists (9,255,481 bytes, last modified 01:41:16 GMT the
  same day) and its rows stop at `2026-11-04 23:59:59.831Z`. Therefore the
  boundary minute for the **current** checkpoint day was not yet inside the
  month-ZIP object at 12:30 UTC. This does not contradict the October recheck,
  which read a boundary minute for a *past* day (2026-10-08) out of an already
  rebuilt month ZIP; the two observations are about different lags.
- `boundary_minute_tick_count: 0` is a statement about the month-ZIP object at
  that moment. It is **not** a statement that no 07:00 data existed anywhere.
- `inbox: NEW_FILES` is a first-run artifact: with no previous `inbox_newest` in
  `state.json`, any non-empty inbox reads as new. The recorded newest mtime was
  `2026-09-12T10:49:32+00:00` (2 files), i.e. the September owner drop, so this
  flip carries no information about new owner material.

### Round 2 — due-gate verification (contract acceptance criterion 2)

```
at_utc: 2026-11-05T12:32:01+00:00
status: NOT_YET_DUE
daily_route: NOT_PROBED   month_route: NOT_PROBED   inbox: NOT_PROBED
boundary_minute_tick_count: null
elapsed_ms: 0   forced: false   error_class: null
```

Command: `.venv\Scripts\python.exe scripts/exness_0700_route_probe.py --once --watch-dir
"D:/tools/nexus-0700-watch"`

Verified with zero network: no new bytes appeared in the ZIP cache and
`next_run_at` was preserved at `2026-11-05T13:00:00+00:00`.

Defect found by this round and fixed in commit
`probe: stop treating NOT_PROBED as a material transition`: the run printed
`MATERIAL_TRANSITION: daily_route PRESENT -> NOT_PROBED`. `NOT_PROBED` records
that the run stopped before the check, so it must never be reported as a flip.

### Manual verification companion to Round 1 (not produced by the probe)

One deliberate read-only check, done by hand on 2026-11-05T12:31 UTC because the
probe by design never opens the day path. It is recorded here so a later session
does not re-run it blind; it is **not** probe output and does not make the day
route "the" route.

- `ticks/XAUUSDm/2026/11/05/` lists exactly one object:
  `Exness_XAUUSDm_2026_11_05.zip`, 1,834,847 bytes, mtime
  `Thu, 05 Nov 2026 12:21:19 GMT` (about nine minutes before Round 1).
- Streaming that ZIP (cached at
  `data/raw/exness_tick_history/current_month_probe/XAUUSDm/2026/manual_day_2026_11_05.zip`,
  gitignored) gives 193,880 rows, all `XAUUSDm`, first row
  `2026-11-05 00:00:00.645Z`, last row `2026-11-05 12:16:09.061Z`, and **175
  rows inside the boundary minute** `2026-11-05 00:00`.
- Interpretation limit: one day, one symbol, one timestamp. That the day object
  was already 12:16 UTC deep shows the current-day file is being extended
  through the day, not that it is complete, stable, or validator-clean. No
  archive validation was run on these bytes.

What this does for the owner's a/b/c decision is narrow but real: the layout is
not fixed in one direction. October had no day subdirectories; November has them
and a growing current-day file. Any option chosen has to survive rotation, and
"month-only" is no longer a durable description of the remote either.

## Standing notes

- **Scheduled unattended since 2026-11-05 (contract section 11.1).** The owner
  activated a Qoder Desktop Automations card whose first step is the expected
  call `--once --cadence-minutes 25`, repeating about every 35 minutes; confirm
  the cadence and `forced` value from the newest NDJSON line, not from this
  note. Before that date the probe ran
  only when something called it, so a gap in the earlier part of this log means
  nobody called it, not that the route changed. A gap now means either the
  device slept, the automation was disabled, or the run ended `NOT_YET_DUE` —
  check `state.json` before reading a gap as absence.
- **A non-zero tick count does not mean the checkpoint is satisfied.** It says
  rows exist in the scanned object for that minute. `0700_STATE_PACKET_H4_V0`
  was not computed, M1 was not rebuilt, and the archive validator has never been
  run on the bytes behind a probe observation.
- **Absence requires a readable listing.** `LISTING_UNREADABLE` is a transport
  or parse fact, never a missing-data claim; `NOT_PROBED` is a skipped check.
- **`SUSPENDED` is human-owned.** Three consecutive error runs stop the probe.
  Clearing it means editing `status` in
  `D:\tools\nexus-0700-watch\state.json` by hand — `--force` deliberately cannot
  re-ignite a suspended observer.
- Downloaded ZIPs stay under `data/raw/` (gitignored); NDJSON and `state.json`
  stay outside the repository at `D:\tools\nexus-0700-watch\`.

## How to promote

1. Run the probe: `.venv\Scripts\python.exe scripts/exness_0700_route_probe.py
   --once --watch-dir "D:/tools/nexus-0700-watch"` (add `--force` only for a
   deliberate manual round).
2. If the run prints `MATERIAL_TRANSITION: <field> <old> -> <new>`, copy that
   line and the printed `status=` line into a new block under `Rounds`, with the
   exact command and the observation's `at_utc`.

The probe never writes this file. Promotion is a deliberate act so that no
background loop can generate repository commits by itself.
