# NEXUS Long-Task Resume Protocol — 2026-09-12

Status: USER-DIRECT OPERATING STANDARD

## Problem

ChatGPT/web UI, browser sessions, remote transport, or a single model turn may end before a long review finishes.
A timeout must never force NEXUS to restart already completed evidence work.

Example invariant:

```text
700 items completed
item 701 in progress
UI/session resets
=> resume item 701
!= restart item 1
```

## Global supervisor

Before locating a per-job state file manually, query:

`py -3 D:\tools\nexus-durable-work\supervisor.py resume`

Canonical supervisor state:

- `D:\tools\nexus-durable-work\_supervisor\registry.json`
- `D:\tools\nexus-durable-work\_supervisor\events.ndjson`

The supervisor tracks the active job, deadline/priority metadata, checkpoint, next action, local process/Bridge job identity, result reference, and the per-job durable state path.

Recovery invariant:

`UI refresh / reconnect / model turn reset / new chat -> supervisor resume -> inspect existing process/job -> continue checkpoint -> never restart completed work by default`

The supervisor does not bypass platform authorization; it prevents authorization/transport/UI interruptions from destroying execution continuity.

## Machine-side executor

For deterministic/resumable local commands that should outlive a ChatGPT/Terminal request, use the NEXUS Local Work Agent:

`D:\tools\nexus-durable-work\local_work_agent.py`

Status:

`py -3 D:\tools\nexus-durable-work\local_work_agent.py status`

The agent is kept alive by a Windows-session watchdog and a user Startup launcher. Each submitted job persists its manifest, attempts, heartbeat, stdout/stderr, and result under:

`D:\tools\nexus-durable-work\_agent\jobs\<JOB-ID>\`

Recovery rule:

- RUNNING + fresh attempt heartbeat -> do not resubmit;
- DONE -> reuse the recorded result;
- interrupted + explicitly resumable/idempotent -> auto-retry is allowed;
- unknown side effects / non-idempotent work -> reconcile evidence first; never blindly replay.

This layer keeps already-submitted machine-side execution alive/recoverable. It does not keep model reasoning alive after a ChatGPT turn disappears and does not bypass platform authorization.

## Core rule

For any long or high-count task whose completed work would be expensive to repeat, progress MUST live on disk, not only in conversation context.

Use:

`D:\tools\nexus-durable-work\durable_work.py`

and its per-job JSON state + append-only NDJSON transition log.

## When mandatory

Use durable progress when any of these applies:

- many images/frames/audio windows/documents are being reviewed;
- work is likely to span multiple model turns;
- a process may continue after a ChatGPT connection disconnect;
- the user would materially lose work if the UI times out;
- source review contains manual/agent interpretation that cannot simply be recomputed instantly.

## Required state

At minimum persist:

- stable job ID/purpose;
- ordered work item IDs/source refs;
- item status: PENDING / IN_PROGRESS / DONE / AMBIGUOUS / FAILED;
- next/resume cursor;
- result reference for completed items;
- ambiguity note and timestamp/source when blocked;
- Bridge jobId/idempotency key when a local background process is involved.

## Checkpoint cadence

Prefer checkpointing every completed item for expensive evidence review.
For cheap deterministic computation, a bounded batch checkpoint is acceptable, but the batch must be small enough that timeout loss is negligible.

Never keep hundreds of completed interpretations only in chat memory waiting for one final save.

## Recovery sequence

After refresh/new chat/reconnect:

1. load normal project bootstrap/preflight;
2. locate the active durable-work state file;
3. run `durable_work.py status`;
4. resume any `IN_PROGRESS` item first;
5. otherwise continue the next `PENDING` item;
6. preserve DONE items;
7. reopen DONE only for a documented source-change/error/review trigger.

## Bridge/process rule

Current ChatGPT Web Bridge supports persistent job receipts/journal, command continuation across connection disconnect within runtime limits, and reconnect/token-refresh behavior.

For long local commands:

- prefer background process/job execution;
- preserve returned jobId/idempotency identifiers in durable state;
- after transport failure, query existing job status before re-running;
- do not duplicate a possibly still-running command just because the UI lost the response.

## STT hard rule

Speech-to-text output is evidence-assistance, not truth.

If wording could materially change a trading/system rule and is unclear, especially:

- numbers/prices/percentages/thresholds;
- clock time/date/timeframe;
- BUY/SELL direction;
- wick/body/open/close/high/low;
- named methods/proprietary terms;
- action instructions;

then:

1. do not guess;
2. mark the item `AMBIGUOUS`;
3. preserve original audio/timestamp;
4. cross-check visual + original audio + alternate ASR where useful;
5. ask the project owner if still unresolved;
6. promote only verified wording into source evidence.

Other unblocked items may continue; one ambiguity should not destroy the whole batch.

## Authentication/connect safety

Do not weaken authentication, bypass platform authorization, or persist secrets merely to avoid a Connect prompt.
If platform-level authorization requires user action, that boundary remains.
The durability solution is that a reconnect never erases completed work.
