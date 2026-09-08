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
