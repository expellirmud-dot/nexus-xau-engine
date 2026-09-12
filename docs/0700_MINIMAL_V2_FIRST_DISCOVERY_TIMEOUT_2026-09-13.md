# 07:00 MINIMAL V2 — First Discovery Run Timeout Checkpoint — 2026-09-13

Status: PRE-OUTCOME PERFORMANCE FAILURE / NO DISCOVERY OUTCOME OPENED

## Attempt

Frozen implementation:

`src/nexus_xau/research/minimal_v2_0700.py`

Frozen checkpoint:

`docs/0700_MINIMAL_V2_PRE_OUTCOME_IMPLEMENTATION_FREEZE_2026-09-13.md`

Discovery input:

`data/raw/dukascopy/chunks/XAUUSD_M1_BID_2022-09-01_2023-03-31.csv`

Expected scaffold:

`150 07:00 days`

## Observed result

The first full discovery run exceeded the execution timeout (~3 minutes) and terminated before writing the configured output directory.

Observed process state:

`timeout / exit code 1`

Output directory:

`results/0700_MINIMAL_V2/DISCOVERY_2022_09_TO_2023_03`

did not exist after the failed run.

Therefore:

`NEW V2 DISCOVERY OUTCOMES OPENED = NO`

No day-state counts, target-first counts, PASS counts, failure map, or outcome percentage was produced or inspected.

## Verified execution-layer cause

The failed Bridge job metadata shows:

- started at `2026-09-12T23:17:03Z`;
- explicit Bridge `expiresAt` at `2026-09-12T23:20:03Z`;
- termination exactly at the configured `180000 ms` request timeout;
- `heartbeatAt = null` for that synchronous Bridge process;
- no V2 output directory was produced.

Therefore the first failure demonstrates a **synchronous Bridge execution timeout**.

It does **not** establish that the V2 calculation itself requires more than three minutes, and it does not justify changing research semantics or optimizing the algorithm from outcome evidence.

## Durable execution fix

Existing global infrastructure was found and reused:

`D:\tools\nexus-durable-work`

Relevant components:

- `local_work_agent.py`
- `job_runner.py`
- machine-side agent heartbeat
- per-attempt child heartbeat/result/stdout/stderr persisted to disk.

The infrastructure is explicitly designed to survive ChatGPT/UI timeout, refresh, reconnect, turn loss, and new chat for deterministic/resumable local work.

The frozen 150-day discovery replay was resubmitted as durable job:

`XAU-0700-MINIMAL-V2-DISCOVERY-20260913`

The Local Work Agent accepted it and launched:

- agent job status: `RUNNING`;
- runner PID: `1568`;
- child PID: `10820`;
- child heartbeat persisted every approximately 2 seconds.

Success probe:

`results/0700_MINIMAL_V2/DISCOVERY_2022_09_TO_2023_03/REPORT.json`

This execution no longer depends on one 180-second synchronous Bridge request remaining open.

## Operational rule going forward

Long deterministic replay/test jobs must prefer:

`Local Work Agent / durable execution`

rather than one blocking `run_command` request with a short timeout.

Chat/Bridge requests become the **control and inspection channel**, not the lifetime of the computation.

Do not add artificial GPT polling merely to keep machine-side work alive.

## Earlier performance hypothesis — not established

The current implementation repeatedly scans/slices the full M1 DataFrame for each H4 origin and each 07:00 cutoff, including:

- origin lifecycle state at cutoff;
- point-check contact;
- favorable excursion;
- origin state again at confirmation;
- post-confirmation boundary scans.

This is semantically acceptable but computationally inefficient for the complete 305,280-row discovery input.

The performance problem is implementation complexity, not evidence insufficiency.

## Allowed fix boundary

Because no V2 discovery outcome has been opened, a pre-outcome performance refactor would still be allowed if independently needed, but it is **not currently justified by the timeout event alone**. First let the unchanged frozen implementation run through the durable execution path.

Allowed:

- replace repeated DataFrame slicing with pre-indexed NumPy arrays / searchsorted;
- precompute immutable per-origin first terminal/contact timestamps;
- use indexed M5 confirmation lookup;
- reduce repeated scans;
- add equivalence/contract tests.

Not allowed:

- change PAT2 geometry;
- change origin eligibility;
- add/remove consumed threshold;
- change location semantics;
- change confirmation timeframe;
- choose a different origin;
- alter target representation;
- inspect partial historical outcomes to guide logic changes.

## Required before retry

1. optimize implementation without semantic change;
2. rerun targeted V2 synthetic contract;
3. run full repository tests;
4. checkpoint/commit/push the performance refactor;
5. rerun the 150-day discovery unchanged.


## Current durable rerun state

At this checkpoint:

`DURABLE DISCOVERY JOB = RUNNING`

`NEW V2 DISCOVERY OUTCOMES OPENED = NO`

The implementation remains the committed frozen V2.0 code from `8ac9f6a`.

No semantic or performance code change was made in response to the timeout before the durable rerun.
