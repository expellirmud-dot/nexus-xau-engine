# 07:00 Route Probe Automation — Contract V0.1 (2026-11-05)

Status: FROZEN_CONTRACT / OWNER_APPROVED_DESIGN / IMPLEMENTED_V0_1_ON_2026-11-05_FIRST_LIVE_ROUND_RECORDED / LEVEL_2_TRIGGER_ACTIVE_SEE_11_1 / READ_ONLY_OBSERVER / NO_STATE_PACKET_COMPUTATION / ORDER_SEND_DISABLED

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

"Previous run" means the most recent observation **that actually probed that
field, on the same checkpoint day**, evaluated per field, not the last line in
the NDJSON. A gate-blocked or failed round records `NOT_PROBED`, which says
nothing about the route, so it can be neither a transition nor a baseline: using
it as the baseline would let a human peek blind the next scheduled round to a
real flip. A round from a different checkpoint day asks a different question, so
the daily 07:00 rollover must never read as a route change (amendment 11.2).

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

### 11.1 Amendment — Level-2 trigger activated by the owner on 2026-11-05

The paragraph above is preserved as the original design statement and is no
longer the current machine state.

Source Fact (owner action, observed in the Qoder Desktop Automations screen on
2026-11-05): the owner created the automation
**"XAU-0700 Route Probe - Every 30 Minutes"**, enabled, with *Keep device awake*
on, running the probe prompt in this repository as an independent task. The
interval the app actually reports for the card is **35 minutes**.

Consequences that a fresh session must respect:

1. The lane **is** now polled unattended. Do not install a Windows Task
   Scheduler entry, a cron job, a daemon, or a second poller for this question.
   Section 3's "no OS-level scheduling" prohibition still holds; what was
   approved is an application-level scheduler owned by the owner, not a
   machine-level scheduled task written by an agent.
2. The trigger interval (35 min) is deliberately longer than the probe's own
   cadence gate, so every scheduled round passes `compute_due` and no scheduled
   round is wasted. The scheduled invocation is the prompt text handed to the
   owner in this session: `--once --cadence-minutes 25 --watch-dir
   "D:/tools/nexus-0700-watch"`, with **no** `--force`. **Verified 2026-11-05
   from the NDJSON**, not inferred: the rounds at 14:27:48Z, 15:02:48Z,
   15:37:46Z, 16:12:50Z and 16:47:44Z each carry `forced: false`, `status=DUE`,
   and a `next_run_at` exactly 25 minutes after `at_utc`, and consecutive rounds
   are ~35 minutes apart. Cadence authority still lives in
   `D:\tools\nexus-0700-watch\state.json`, exactly as section 4 requires.
3. The automation runs a chat task, not the script alone. Its prompt restricts
   it to one bounded round plus, on a `MATERIAL_TRANSITION` hint, one appended
   block under `## Rounds` in `docs/0700_ROUTE_PROBE_LOG.md` — and that block is
   committed and pushed as the task's only repository write. The probe process
   itself still never writes or commits the log (section 5 is unchanged);
   promotion remains a deliberate act by whatever calls the probe, and the
   automation prompt is the owner's chosen way of making that act repeatable.
   If the owner prefers report-only promotion, the change is one step in the
   automation prompt, not a change to this contract.
4. Because polling is now unattended, `SUSPENDED` after three consecutive error
   runs is the mechanism that prevents a broken observer from generating a
   round every 35 minutes forever. It stays human-owned: clearing it is an owner
   or chat decision, never an automation step.
5. Verification at amendment time: the last observation line in
   `D:\tools\nexus-0700-watch\observations.ndjson` was still the 12:32:01Z
   `NOT_YET_DUE` gate check, so no scheduled round had fired yet. Five
   unattended rounds had fired by 16:47:44Z, all `error_class: null`,
   `error_streak: 0`.

### 11.2 Amendment — the gate-blocked round blinded the observer (fixed 2026-11-05)

Running the lane unattended exposed a defect that 60 offline tests had not:
`main` compared each new observation against `prior[-1]`, the literal last
NDJSON line. Because section 6 forbids `NOT_PROBED` from reading as a
transition, a `NOT_YET_DUE` line as baseline suppressed **every** field
comparison instead of only the `NOT_PROBED` one.

Evidence (Source Fact, from the NDJSON): the 12:30:00Z round recorded
`month_route=PRESENT_CHANGED` and `inbox=NEW_FILES`; the 12:32:01Z gate check
recorded `NOT_PROBED` for all three fields; the first unattended round at
14:27:48Z recorded `PRESENT_UNCHANGED` / `NO_NEW_FILES` — both fields had
genuinely moved since the last round that probed them, yet no transition was
promoted (`git log -- docs/0700_ROUTE_PROBE_LOG.md` gained no probe commit), and
the task reported no `MATERIAL_TRANSITION` line. Reverting the wiring inside the
test suite reproduces that silence exactly.

Consequence: any early manual call — which section 4 advertises as free, and
which TOOLS.md actively recommends — silently disabled transition detection for
the next scheduled round. The most interesting moment was the one most likely to
be missed.

Fix: `prior_baseline()` selects, per field, the newest value that is not
`NOT_PROBED` **and comes from the same `checkpoint_day`**, and `main` compares
against that. `NOT_PROBED` therefore remains neither a transition nor a
baseline. Vocabulary, schema, network rails, the cadence gate and the
`SUSPENDED` rule are unchanged; the promotion rule in section 5 is unchanged
apart from this clarification.

The checkpoint-day half of the rule was found while fixing the first half. The
checkpoint day is the Bangkok calendar date, so it rolls over every day at
07:00 and the new day's directory legitimately does not exist yet for a while.
Comparing across that boundary would have turned the first morning round of
every day into a reported `daily_route PRESENT -> ABSENT` — a route
disappearance that is really just a new day — and the automation would have
committed it. Verified live on 2026-11-05T17:07:00Z: with `checkpoint_day`
rolled to 2026-11-06, the round recorded `daily_route=ABSENT` while the 2026-11-05
rounds had recorded `PRESENT`, and printed **no** transition hint.
