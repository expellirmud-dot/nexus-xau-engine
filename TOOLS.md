# NEXUS XAU Engine — Tooling Index

Status: ACTIVE / REUSE-BEFORE-BUILD REGISTRY

Purpose: make project-external utilities discoverable from the repository so a future NEXUS session does not assume a tool is missing and rebuild it unnecessarily.

## Operating rule

Before creating a new engineering utility for this project:

1. read this file;
2. inspect the registered tool path;
3. reuse or extend the existing tool when appropriate;
4. only create a new tool if the required capability is genuinely absent;
5. record any new reusable tool here at the same checkpoint.

Do not duplicate a working external utility inside this repository merely for discoverability. Keep one canonical implementation and store its canonical path here.

## Registered tools


### NEXUS Durable Work / Resume Ledger

Canonical path:

`D:\tools\nexus-durable-work`

Primary script:

`D:\tools\nexus-durable-work\durable_work.py`

Documentation:

`D:\tools\nexus-durable-work\README-TH.txt`

Project protocol:

`docs/LONG_TASK_RESUME_PROTOCOL_2026-09-12.md`

Purpose:

- persist ordered long-task work items outside chat/UI state;
- record `PENDING / IN_PROGRESS / DONE / AMBIGUOUS / FAILED`;
- atomic JSON state writes plus fsynced append-only event log;
- resume an interrupted item/session without restarting completed work;
- store result refs and optional Bridge job IDs;
- force uncertain STT into an explicit ambiguity state instead of silent inference.

Use this for long image/frame/audio/source batches and other expensive-to-repeat work.
For local commands, combine it with Bridge background jobs/job receipts where appropriate.
Do not bypass authentication or platform authorization prompts as a substitute for durable progress.

### NEXUS Video Evidence

Canonical path:

`D:\tools\nexus-video-evidence`

Primary script:

`D:\tools\nexus-video-evidence\extract_frames.py`

Reusable transcript context helper:

`D:\tools\nexus-video-evidence\extract_transcript_context.py`

Reusable visual crop/zoom helper:

`D:\tools\nexus-video-evidence\crop_image_region.py`

Documentation:

`D:\tools\nexus-video-evidence\README-TH.txt`

Purpose:

- open local MP4 teaching videos;
- seek to a supplied timestamp with OpenCV;
- extract nearby evidence frames;
- write a manifest with frame metadata / hashes;
- feed extracted JPG frames through the existing IE Coder image bridge for NEXUS visual inspection.

Project protocol:

`docs/VIDEO_EVIDENCE_PIPELINE_2026-09-08.md`

Current proven path:

`MP4 -> OpenCV frames -> JPG -> IE Coder image bridge -> NEXUS vision`

Planned extension:

`short synchronized evidence window -> frame sequence + original audio segment + YouTube ASR + normalized/verified transcript + common timestamps`

Do not claim audio extraction/alignment is already implemented until it is actually validated.

### IE Coder Bridge Image Patch

Canonical path:

`D:\tools\ie-coder-bridge-image-patch`

Documentation:

`D:\tools\ie-coder-bridge-image-patch\README-TH.txt`

Purpose:

- enables local JPEG/PNG reads through IE Coder Connect as agent-vision image content;
- reused by the NEXUS Video Evidence pipeline;
- avoids building a second image-transfer system.

Important: this is a bridge patch with its own apply/restore scripts. Do not re-patch or replace it merely because image-reading capability is not obvious from the research repo.

### Agent Browser CLI

Canonical executable:

`C:\Users\Expellirmud\AppData\Roaming\npm\agent-browser.cmd`

Validated version:

`0.33.2`

Purpose:

- browser automation optimized for AI agents;
- open/read/snapshot/click/find/eval YouTube and other rendered web sources;
- extract rendered YouTube `Show transcript` content with timestamps;
- inspect page metadata and accessibility-tree refs without building a second browser wrapper.

Preferred NEXUS research use:

`agent-browser -> YouTube metadata/transcript/timestamps`

For current YouTube research, the validated CDP path uses a separate NEXUS Chrome profile rather than the owner's normal Chrome profile:

- Chrome: `C:\Program Files\Google\Chrome\Application\chrome.exe`
- remote debugging: `9222`
- NEXUS profile: `D:\tools\nexus-agent-chrome-profile`
- session name used in validation: `nexus-youtube`

Validated pattern:

`Chrome --remote-debugging-port=9222 --user-data-dir=D:\tools\nexus-agent-chrome-profile -> agent-browser --cdp 9222`

Important limitation discovered on EP.5 (`oCcG3dUjrgw`): the headless YouTube page exposed the full rendered transcript successfully, but the video player itself returned a playback error and did not provide reliable visual frames. Therefore:

- use `agent-browser` as the preferred browser/transcript/metadata layer;
- use local MP4 + `nexus-video-evidence` for chart visual evidence when available;
- do not treat a failed/headless player screenshot as source visual proof.

Follow-up validated visual path for the same source:

- Chrome headed research profile: `D:\tools\nexus-agent-chrome-profile-headed`
- remote debugging: `9223`
- validated session: `nexus-youtube-headed`
- EP.5 original YouTube `<video>`: `readyState=4`, no playback error
- visual capture pattern: timestamp seek with `eval` -> `screenshot video <path>`

Current preferred split:

- `agent-browser` headless/CDP: transcript, metadata, DOM;
- `agent-browser` + separate headed CDP Chrome: original web-video visual evidence when playback works;
- local MP4 + `nexus-video-evidence`: preferred reproducible visual source when a lawful local file is already available.

Do not erase the headless failure from history; headless and headed playback are distinct validated behaviors.

Local helper/fallback experiments live under:

`D:\tools\nexus-browser-evidence`

This helper directory is NOT the canonical browser engine. Reuse `agent-browser` first and only extend helpers for bounded evidence capture/encoding needs.

### Repository Research Preflight

Canonical path:

`D:\nexus-xau-engine-repo\scripts\research_preflight.py`

Purpose:

- validate the restart-safe core file set;
- resolve the active RQ worksheet and latest checkpoint dynamically;
- summarize canonical/coverage counts and blocked claims;
- emit a SHA-256-prefixed required-read manifest for a zero-context agent.

Run from repository root:

`.venv\Scripts\python.exe scripts\research_preflight.py`

A PASS is required by `AGENTS.md` before new substantive research. The script does not replace actually reading the files; it is the deterministic gate/discovery layer.

## Local source vault

Path:

`D:\nexus-xau-engine-repo\youtube`

Status:

- local evidence only;
- gitignored;
- contains downloaded teaching MP4s, YouTube transcript exports and locally extracted evidence bundles;
- never commit MP4/media evidence to Git unless the project owner explicitly changes that policy.

## Current first video batch

The first locally available batch contains five video/transcript pairs through `ESHDuiVPJow` (Trend -> Frame -> SIG). Treat this as the current bounded source batch until the owner adds more.

## Restart rule

When resuming the project, load `TOOLS.md` before deciding that a required media/vision utility does not exist.


## Global compact project continuity

Location:

`D:\tools\nexus-project-continuity`

Purpose:

- compact reconnect/resume capsule across Projects;
- project/git/workstream/version/next-action routing;
- live durable-job reconciliation;
- shared-tool capability registry;
- prevents bulk document loading merely to recover session context.

XAU command:

```bat
py -3 D:\tools\nexus-project-continuity\continuity.py resume --project xau
```

Global shortcut:

```bat
D:\tools\NEXUS-START\RESUME_WORK.cmd --project xau
```

Use this before deep Project bootstrap on reconnect.

Do not duplicate Project-specific resume logic in the repo when the central registry can describe it.
