# NEXUS XAU Engine — Local Video Evidence Pipeline — 2026-09-08

Status: ENGINEERING INFRASTRUCTURE / VISUAL-EVIDENCE ACCESS ENABLED

## Purpose

Enable NEXUS to inspect what the instructor is pointing at on charts instead of relying on YouTube transcript text alone.

## Reuse-first audit

Before building a new pipeline, `D:\tools` was inspected for existing media / image bridge utilities.

Reusable existing asset found:

`D:\tools\ie-coder-bridge-image-patch`

This patch already enables local JPEG/PNG files to be returned through IE Coder Connect as agent-vision image content. Therefore no duplicate image-transfer system was created.

## New local utility

Created outside the research repo:

`D:\tools\nexus-video-evidence\extract_frames.py`

Documentation:

`D:\tools\nexus-video-evidence\README-TH.txt`

The utility uses the already-installed Python OpenCV package. System `ffmpeg` was not found in PATH, so no additional ffmpeg dependency was installed at this checkpoint.

## Pipeline

```text
local MP4
-> OpenCV timestamp seek
-> nearby JPG evidence frames
-> manifest.json + SHA256
-> IE Coder image bridge
-> NEXUS agent vision
-> transcript + visual cross-check
-> claim-level evidence only after provenance review
```

Default evidence window:

```text
-3s, -1s, 0s, +1s, +3s
```

A denser window can be used when pointer movement or rapid chart changes matter.

## Successful proof

Source video:

`youtube/EP.2 เทรน ชนะ กรอบ กรอบ ชนะ Sig#SmatTrderToSuccess #ระบบแม่ปลาปากกาเขียว.mp4`

Transcript:

`youtube/EP.2 เทรน ชนะ กรอบ กรอบ ชนะ Sig.txt`

Test timestamp:

`00:06:33`

Result:

- video opened successfully through OpenCV;
- detected 30 FPS;
- duration ~10,641.1 seconds;
- 5/5 nearby frames extracted successfully;
- frame manifest written successfully;
- the 00:06:33 JPG was returned through IE Coder Connect with `vision=agent-vision`;
- NEXUS visually inspected the frame and confirmed it showed the EP.2 title slide with the lesson title and instructor image.

Therefore the required local-media visual path is operational.

## Evidence discipline

- Frame extraction itself proves no trading rule.
- Raw YouTube ASR transcript must remain preserved separately from visual interpretation.
- When wording such as `ตรงนี้`, `แท่งนี้`, `ไส้นี้`, `กรอบนี้`, `ดูนี่`, `ยืน`, `เบรก`, `SIG`, or a numeric/time expression affects a rule, inspect multiple nearby frames and the corresponding transcript/audio context.
- Existing Thai spoken-time normalization and ASR-risk rules remain in force.
- Visual inference cannot become canonical solely because a frame appears consistent with an existing thesis.
- Outcome/backtest performance cannot upgrade source provenance.

## Local media policy

The entire `youtube/` directory is intentionally local and gitignored. It may contain large MP4s, local transcript exports, extracted frames, and manifests. Canonical research documents should reference source IDs / timestamps / local paths but should not commit the media files themselves.

## Next engineering step

Add transcript-guided candidate extraction so the system can identify high-value visual-review timestamps automatically (for example lines containing deictic chart language or mechanically important terms) and generate evidence frame bundles without manually entering every timestamp.
