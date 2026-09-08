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

## Canonical review unit: short Evidence Window

Project owner clarified that the useful mental model is not `single screenshot review` and not necessarily `play the whole MP4 directly inside the model`.

The preferred research unit is a short synchronized **Evidence Window**, typically around 10–20 seconds when needed:

```text
SHORT VIDEO WINDOW
├─ ordered visual frames from the MP4
├─ original audio segment from the same time range
├─ YouTube ASR transcript for the same range
├─ normalized / verified transcript layer when required
└─ shared timestamps tying every layer together
```

Example conceptual structure:

```text
15:20–15:35

VISUAL
15:20.0 frame
15:20.5 frame
15:21.0 frame
...
15:35.0 frame

AUDIO / SPEECH
15:20–15:23 original audio segment
15:23–15:27 original audio segment
...

YOUTUBE ASR
15:20 ...
15:27 ...
```

This allows NEXUS to reconstruct what happens over time rather than infer from one still image. It is especially important when the instructor:

- moves the mouse/pointer;
- circles or drags across a chart;
- moves from candle A to candle B;
- changes timeframe;
- zooms/pans the chart;
- says deictic phrases such as `ตรงนี้`, `แท่งนี้`, `ไส้นี้`, `เส้นนี้`, `กรอบนี้`, `ดูตรงนี้`.

### Vision/audio interpretation model

For this project, `video review` should be treated operationally as synchronized time-series evidence:

```text
VIDEO INFORMATION
= ordered images over time
+ audio over the same time
```

The visual side is analyzed as sequential frames. The audio side should remain preserved as original media and may be converted to text for analysis.

Preferred speech evidence chain:

```text
original audio
-> YouTube ASR transcript
-> normalized / verified transcript
```

Do not discard the original audio merely because a transcript exists. YouTube ASR can materially misrecognize numbers, clock times, timeframe names, proprietary terminology, `wick/body/close`, or Thai trading vocabulary.

If a wording affects an algorithmic rule, use the original audio/video segment to cross-check the ASR when possible.

### Important implementation boundary

At this checkpoint, the visual-frame path is proven operational. Automatic audio extraction / speech alignment into the Evidence Window is **not yet implemented** in `nexus-video-evidence`.

Therefore do not claim that NEXUS currently receives MP4 + audio as one native multimodal stream. The current proven capability is:

```text
MP4 -> timestamped frames -> NEXUS vision
```

The next extension is:

```text
MP4 -> short audio segment -> transcript/alignment
```

then combine both with common timestamps.

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
- Original audio should remain preserved separately from any ASR/normalized transcript.
- When wording such as `ตรงนี้`, `แท่งนี้`, `ไส้นี้`, `กรอบนี้`, `ดูนี่`, `ยืน`, `เบรก`, `SIG`, or a numeric/time expression affects a rule, inspect multiple nearby frames and the corresponding transcript/audio context.
- Existing Thai spoken-time normalization and ASR-risk rules remain in force.
- Visual inference cannot become canonical solely because a frame appears consistent with an existing thesis.
- Outcome/backtest performance cannot upgrade source provenance.
- A synchronized Evidence Window is preferred over a single still when pointer motion, chart transition, or temporal context can change interpretation.

## Local media policy

The entire `youtube/` directory is intentionally local and gitignored. It may contain large MP4s, local transcript exports, extracted frames, audio segments, and manifests. Canonical research documents should reference source IDs / timestamps / local paths but should not commit the media files themselves.

## Next engineering steps

1. Add transcript-guided candidate extraction so the system can identify high-value visual-review timestamps automatically (for example lines containing deictic chart language or mechanically important terms).
2. Add short audio-segment extraction aligned to the same Evidence Window.
3. Preserve `original audio -> YouTube ASR -> normalized/verified transcript` as separate provenance layers.
4. Generate one synchronized evidence bundle containing frames, transcript lines, audio locator, timestamps, hashes, and later claim-level review notes.
