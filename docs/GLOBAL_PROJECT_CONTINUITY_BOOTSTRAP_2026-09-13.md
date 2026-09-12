# Global Project Continuity Bootstrap — XAU Integration — 2026-09-13

Status: GLOBAL CONTINUITY TOOL INTEGRATED / COMPACT-FIRST RECONNECT / DISCOVERY RESULT UNOPENED

## Purpose

Move reconnect/session continuity out of Project-specific chat memory and into shared machine infrastructure under:

`D:\tools\nexus-project-continuity`

This is global infrastructure for all NEXUS Projects.

The XAU repo is the first registered Project.

## Problem being solved

The previous restart model could recover context, but it required loading many Project files after each reconnect.

That creates a second failure mode:

```text
session reset
-> reload large context
-> context budget fills with old Project state
-> session truncates again
-> agent loses awareness of tools/jobs/current work
```

The fix is not to remove evidence.

The fix is to separate:

- compact routing/status memory;
- deep evidence memory.

## New global reconnect path

Primary command:

```bat
py -3 D:\tools\nexus-project-continuity\continuity.py resume --project xau
```

Shortcut:

```bat
D:\tools\NEXUS-START\RESUME_WORK.cmd --project xau
```

The capsule reports only compact routing state:

- Project root;
- Git branch/head/dirty state;
- workstream;
- active RQ;
- latest checkpoint;
- current frozen version;
- next action;
- durable job pointer versus live machine job state;
- shared NEXUS tool capability IDs;
- deep-load rule.

It does not read the full Project documentation set.

## Shared tool registries

Global Project registry:

`D:\tools\nexus-project-continuity\projects.json`

Shared capability registry:

`D:\tools\nexus-project-continuity\capabilities.json`

Current registered XAU Project ID:

`xau`

Other Projects should be registered in the same global tool instead of implementing separate reconnect scripts.

## Live-machine reconciliation proof

Before reconciliation, XAU Project state said the durable Discovery job was still RUNNING.

The global continuity capsule inspected the actual machine-side durable job and reported:

```text
pointer=RUNNING_AT_CHECKPOINT
live=DONE
STALE_PROJECT_POINTER
```

This proved the capsule is doing more than remembering text: it reconciles current machine evidence.

The V2 Discovery result file exists and is non-empty:

`results/0700_MINIMAL_V2/DISCOVERY_2022_09_TO_2023_03/REPORT.json`

At this checkpoint:

`DISCOVERY EXECUTION = DONE`

`DISCOVERY OUTCOME INTERPRETATION = UNOPENED`

The result was not rerun and was not interpreted during this infrastructure checkpoint.

## Two-tier context model

### Tier 0 — compact reconnect

Use for:

- reconnect/new chat;
- job status;
- locating latest checkpoint/output;
- continuing an already-frozen deterministic task;
- discovering available shared tools.

Do not bulk-load Project docs.

### Tier 1 — deep evidence load

Escalate only when the next task requires:

- changing/interpreting a research rule;
- opening source research;
- changing semantic code;
- interpreting outcomes into conclusions;
- updating claims;
- designing a new experiment/version;
- reconciling contradictions.

Then load only the material Project pointers and supporting evidence.

## Long-task rule

Long deterministic work must not depend on ChatGPT request lifetime.

Use:

`D:\tools\nexus-durable-work`

The continuity tool inspects and reuses persisted durable job state.

Do not keep jobs alive with repeated GPT polling.

## XAU bootstrap change

`AGENTS.md` and `PROJECT_BOOTSTRAP.md` now define compact-first reconnect and deep-load-on-demand.

`TOOLS.md` records the global continuity capability.

## Current next action

The frozen V2.0 150-day Discovery job is complete.

Next research action is:

```text
open persisted REPORT once
-> interpret under frozen V2.0
-> build 150-day failure / PASS / unknown-state map
-> checkpoint before unchanged 60-day replication
```

Do not rerun the already-completed 150-day job.
