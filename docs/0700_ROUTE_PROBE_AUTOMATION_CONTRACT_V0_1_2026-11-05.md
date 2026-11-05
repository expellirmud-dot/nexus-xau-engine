# 07:00 Route Probe Automation — Contract V0.1 (2026-11-05)

Status: FROZEN_CONTRACT / OWNER_APPROVED_DESIGN / IMPLEMENTED_V0_1_ON_2026-11-05_FIRST_LIVE_ROUND_RECORDED / READ_ONLY_OBSERVER / NO_STATE_PACKET_COMPUTATION / ORDER_SEND_DISABLED

Approved by the owner on 2026-11-05 in the form **"Probe + log only"** and
**"register with the durable supervisor first"** (no Windows scheduled task).

## 1. Problem this tool exists to solve

`docs/0700_CURRENT_DAY_INPUT_ROUTE_RECHECK_2026-11-05.md` established that the
frozen daily-archive acquisition route is obsolete at the remote provider while
the month-only ZIP does expose the required boundary-minute ticks. The lane is
now blocked on an owner decision (a/b/c), and that decision needs a fact that
changes over time: **which route exposes checkpoint data, and when.**

Today that fact is only ever captured when a human opens a chat and asks. This
contract defines a cheap, decision-neutral observer that records the fact on a
cadence without interpreting it.

The tool must never decide the route, never compute the State Packet, and never
make the 07:00 objective look satisfied.

## 2. Scope

Per probe run, exactly three observations:

1. `daily_route` — is a daily subdirectory/ZIP present for the checkpoint day
   (the previously validated layout)?
2. `month_route` — does the month-only ZIP exist, and did its reported size or
   last-modified value change since the previous probe? If and only if it
   changed, stream-scan the boundary minute for the current checkpoint day.
3. `owner_inbox` — did new files appear in the owner source-drop directory since
   the previous probe?

**Definitions used literally by the code:**

- `checkpoint day` — `--checkpoint-day YYYY-MM-DD`, defaulting to the current
  Asia/Bangkok calendar date at probe time;
- `boundary minute` — the single minute `00:00 UTC` of that checkpoint day, i.e.
  `07:00 Asia/Bangkok`, matching `docs/0700_CURRENT_DAY_INPUT_ROUTE_2026-10-08.md`;
- `owner source-drop directory` — default
  `D:\tools\nexus-video-evidence\_incoming\`, overridable by `--inbox`; the probe
  counts regular files and their newest mtime, it never reads file contents.

Nothing else is observed. MT5, trading, scoring, and the canonical registers are
out of scope by construction (section 7).

## 3. Non-scope (hard)

- No `0700_STATE_PACKET_H4_V0` computation, no M1 rebuild, no validator run on
  downloaded bytes beyond the boundary-minute existence check.
- No write to `docs/CANONICAL_CLAIM_REGISTER_2026-09-03.json`,
  `docs/CURRENT_RESEARCH_STATE.json`, `docs/0700_WORKSTREAM_STATE.json`,
  `research_queue/QUEUE.json`, or `research_findings/FINDINGS.json`.
- No route implementation. If the probe reports month-ZIP availability, the a/b/c
  decision still belongs to the owner.
- No holdout, economic, Win/Loss, expectancy, or profitability work.
- No order send. No credential use, no login, no account discovery.
- No OS-level scheduling. This contract does not install a Task Scheduler entry;
  that is a separate owner-approved change if ever requested.

## 4. Identity and cadence model

Cadence belongs to a **state file, not the operating system**, because
`D:\tools\nexus-durable-work\local_work_agent.py` reconciles one-shot jobs only
and has no due-date semantics (verified against its `daemon()`/`run_once()`
implementation on 2026-11-05).

- The probe owns `next_run_at = run_started_at + cadence_minutes` and writes it
  atomically at the end of every run.
- Default cadence: 30 minutes, overridable by `--cadence-minutes`.
- `--once` is the only mode. When called before `next_run_at`, the probe must
  exit `NOT_YET_DUE` **without any network call**, printing the remaining wait.
  This is what makes "run it from any chat, any number of times" free.
- `--force` overrides the gate for a deliberate manual round and must be recorded
  in the observation as `forced: true`.

## 5. Components

| unit | file | single responsibility |
|---|---|---|
| probe CLI | `scripts/exness_0700_route_probe.py` | perform one bounded probe round; append one observation; update state |
| observation store | `D:\tools\nexus-0700-watch\observations.ndjson` | append-only machine log, one JSON object per line |
| probe state | `D:\tools\nexus-0700-watch\state.json` | last run, next run, previous month-ZIP fingerprint, previous inbox fingerprint |
| material-change log | `docs/0700_ROUTE_PROBE_LOG.md` | human-readable promotion of state transitions only |
| registration | durable supervisor job `XAU-0700-ROUTE-PROBE-<implementation-date>` | cross-session discoverability of the lane |

The probe **never** writes or commits the material-change log. When a run's
vocabulary differs from the previous run's, it prints a one-line
`MATERIAL_TRANSITION: <field> <old> -> <new>` hint; promoting that hint into
`docs/0700_ROUTE_PROBE_LOG.md` is a deliberate act by a human or a chat session,
so no process can silently accumulate repository commits from a background loop.

Reused, not rebuilt: the remote path conventions and URL builders in
`scripts/exness_intraday_state_packet_0700.py` (`BASE_URL`,
`_month_directory_url`, `_day_directory_url`, `_daily_filename`), and the existing
local cache directory `data/raw/exness_tick_history/current_month_probe/`, which
is already gitignored by `data/raw/*`.

## 6. Observation schema and state vocabulary

Every observation line carries:

`at_utc`, `symbol`, `checkpoint_day`, `daily_route`, `month_route`, `inbox`,
`boundary_minute_tick_count`, `forced`, `error_class`, `elapsed_ms`.

Result values are a closed vocabulary. Free-text status strings are prohibited,
because prose is how an observer gets misread as a conclusion:

| field | allowed values |
|---|---|
| `daily_route` | `PRESENT`, `ABSENT`, `LISTING_UNREADABLE`, `NOT_PROBED` |
| `month_route` | `PRESENT_CHANGED`, `PRESENT_UNCHANGED`, `ABSENT`, `LISTING_UNREADABLE`, `NOT_PROBED` |
| `inbox` | `NO_NEW_FILES`, `NEW_FILES`, `DIR_MISSING`, `NOT_PROBED` |
| `boundary_minute_tick_count` | integer, or `null` when the scan was not performed |

`NOT_PROBED` appears only when the run ended before reaching that check (a
transport failure on an earlier check). It is never used as a synonym for
`ABSENT`.

The `boundary_minute_tick_count` field is existence evidence only. A non-zero
value must never be reported, read, or committed as "the checkpoint is available
through the operational route" — the route is still undecided and the archive
validator has not been run on those bytes.

## 7. Safety rails

1. **Read-only network.** GET/HEAD on the same public archive host already used
   by the frozen runner. No authentication, no headers echoed, no cookies, no
   response body persisted except the ZIP cache under `data/raw/`.
2. **Bounded traffic.** At most one month-directory listing, one daily-path
   check, and one ZIP fetch per run. If the month ZIP fingerprint is unchanged,
   the fetch and scan are skipped and recorded `PRESENT_UNCHANGED`. No retry
   storm: one retry maximum, and a second failure ends the run as an error
   observation.
3. **Fail closed, never infer.** `404` on a day path plus an unreadable listing
   is `LISTING_UNREADABLE`, not `ABSENT`. Absence may only be asserted when the
   listing was successfully read.
4. **No secrets, no media in git.** NDJSON and state live outside the repository;
   the repo holds the contract, the code, the tests, and the promoted transition
   log. Raw media and downloads stay under gitignored paths.
5. **Atomic writes.** `state.json` written by temp-then-replace; NDJSON appended
   with a single write call so concurrent readers never see a partial line.
6. **Self-limiting.** If `error_class` repeats across three consecutive runs the
   probe records `SUSPENDED` in state and stops probing until a human clears the
   flag, so a broken observer cannot become background noise forever.

## 8. Testing

Offline by default; the test suite must not touch the network.

Fake remote responses cover, at minimum:

- daily layout present / day path 404 with readable listing / listing garbage;
- month ZIP new fingerprint (scan runs) / identical fingerprint (scan skipped);
- month ZIP grew but zero boundary-minute ticks in the checkpoint day;
- boundary-minute ticks found, asserting the observation still contains no
  state-packet field;
- `NOT_YET_DUE` short-circuit producing zero HTTP calls;
- transport error once then success, and error twice producing the error
  observation and the `SUSPENDED` counter;
- inbox: new file, no new file, missing directory;
- append-only integrity when a pre-existing NDJSON line is malformed (must not
  be rewritten or dropped).

One live `--force` round is executed manually during implementation and its
result is recorded as a Source Fact in the checkpoint document; live probing is
not part of the automated suite.

## 9. Registration and cross-session resume

Implementation ends with:

```
py -3 D:\tools\nexus-durable-work\supervisor.py register \
  --job-id XAU-0700-ROUTE-PROBE-<yyyymmdd> \
  --title "07:00 route availability observer" \
  --purpose DECISION_NEUTRAL_PROBE \
  --status WAITING \
  --repo D:\nexus-xau-engine-repo \
  --next-action "run scripts/exness_0700_route_probe.py --once when now >= next_run_at"
```

`supervisor.py resume --project xau` must therefore surface the lane in any new
session without conversational memory, satisfying the AGENTS.md long-task
durability invariant. Registration happens **after** the script exists, so a
resumed session can never be pointed at a missing command.

## 10. Acceptance criteria

1. `--once` on a fresh machine state performs one bounded round, appends exactly
   one observation, and sets `next_run_at`.
2. Immediate second call exits `NOT_YET_DUE` with zero HTTP requests.
3. All state values come from the closed vocabulary; the code has no other
   literals for those fields.
4. Full offline test suite passes, plus `ruff` clean, plus
   `NEXUS_RESEARCH_PREFLIGHT=PASS`.
5. One live `--force` round recorded with its observation file and line reference.
6. `git status` shows no downloaded archive, no NDJSON, no screenshot staged.
7. Nothing in `docs/CANONICAL_CLAIM_REGISTER_2026-09-03.json`,
   `docs/0700_WORKSTREAM_STATE.json`, or the Queue changed as a result of this
   tool.

## 11. Known limitation stated up front

With no OS-level scheduler, the probe runs only when something calls it — a chat
session, the durable agent given a due-date wrapper, or the owner. The observer
therefore guarantees **freshness on demand and a durable trail**, not unattended
wall-clock polling. If the owner later wants true 24-hour polling, that is the
Level-2 change (a scheduled task) and requires a separate explicit approval
because it modifies the machine, not the repository.
