# Video Source Evidence — SL / TP / Wick Re-anchor — 2026-10-08

Status: NEW FIRST-PARTY TEACHING EVIDENCE / USER-PROVIDED TRANSCRIPT + DIRECT VISUAL VERIFICATION / PRE-OUTCOME

## Source package

Two owner-supplied local videos dated 2026-09-12 were reviewed.

1. `VID_20260912_164004 (1).mp4`
   - duration: approximately 48.23 seconds;
   - SHA-256: `8ad37be975a4f204e6e0f53f113124081c5e15c2bcc85a012247631d1aeca17c`;
   - durable copy: `D:\tools\nexus-video-evidence\_incoming\2026-10-07\VID_20260912_164004 (1).mp4`.

2. `VID_20260912_163822 (1).mp4`
   - duration: approximately 91.82 seconds;
   - SHA-256: `056594f6faa4ff44f47f621892eb420cfd65090426ec7ca04423e184cf1c2293`;
   - durable copy: `D:\tools\nexus-video-evidence\_incoming\2026-10-07\VID_20260912_163822 (1).mp4`.

The SHA-256 values of the current conversation uploads and the copied local originals match exactly.

## Transcript provenance

The Thai transcript used for this checkpoint was supplied directly by the project owner with timestamps.

Local independent ASR was attempted only through pre-existing Project tooling. The current host environment no longer contains `faster_whisper`, `speech_recognition`, or OpenCV, so no new package was installed and no machine-generated transcript was substituted.

Accordingly:

- transcript wording = `USER_PROVIDED_TIMESTAMPED_TRANSCRIPT`;
- visual geometry = `DIRECT_VISUAL_REVIEW_OF_MATCHING_HASHED_VIDEO`;
- exact phonetic spelling of specialized terms remains preserved as owner transcription where uncertain;
- semantic promotion is based on the spoken relation + visible diagram, not on automatic spell correction.
## Video 1 — support/frame Buy example (`164004`)

Owner transcript summary:

- upper line = major resistance;
- middle line = minor support/resistance;
- lower line = major support;
- assume an H1 Buy-side run is still unfinished;
- price pulls back to support;
- a lower-timeframe Buy PA appears on M5 or M1;
- after a body-collection/retest behavior, the entry is taken;
- spoken SL wording: `วาง SL ใต้นี่แค่ 100 เดียวพอ`;
- first TP alternative: upper frame/resistance;
- second TP alternative: count from the referenced wick/run anchor;
- H1 example = 1,000 points;
- H4 example = 1,500 points.

Direct visual review around approximately 20–27 seconds confirms that the instructor points at/draws the lower reversal/low area while describing entry and SL, with an SL mark below the local structure.

Direct visual review around approximately 33–45 seconds confirms that the instructor gestures from the wick/run reference toward the upper target area while discussing H1/H4 point distances.

Safe source statement from this clip:

`BUY example: lower-TF reversal near support -> entry; SL is below the local low/check area, with an explicit 100-point wording in this example; TP may be the upper frame or the timeframe run target measured from the referenced wick.`

The 100-point value is explicit in this Buy example but is not yet promoted as a universal buffer for every setup/timeframe/direction.
## Video 2 — H1 confirmed-wick / check / entry / TP example (`163822`)

Owner transcript establishes the following sequence:

1. During an unfinished H1 candle, the current lower wick is described with the owner-transcribed term `ไส้อนุมาน`.
2. While the H1 candle is still open, the instructor can already discuss a provisional 1,000-point H1 TP measured from that current wick.
3. If price later extends the wick before the hour closes, the reference moves with the still-forming candle.
4. When the H1 candle closes bullish and its body closes above the indicated 50% relation, the final wick is described with the owner-transcribed term `ไส้รังซิก`.
5. The instructor explicitly calls that final wick the `จุดเช็ก SL` / `จุดวาง SL`.
6. On the next H1 candle, if price pulls back and M1/M5 shows a reversal without touching that check point, the instructor says to enter Buy and place the SL at that referenced area.
7. TP is measured from the wick reference, not from the later entry price:
   - H1 = 1,000 points;
   - H4 = 1,500 points;
   - Day = 5,000 points.

Direct visual review confirms the instructor repeatedly points to the final lower wick/check area around the 34–60 second region and later points upward from that reference while discussing the target distances.

## Semantic normalization

Because the exact specialized Thai terms may be phonetic/teaching jargon, the Project should preserve the raw owner-transcribed terms but use semantic labels in code/research:

- `PROVISIONAL_WICK_WHILE_PARENT_BAR_OPEN` = the wick can still move before the timeframe candle closes;
- `CONFIRMED_CHECK_WICK_AFTER_PARENT_BAR_CLOSE` = the final wick after the parent timeframe candle closes and the stated >50% body-close condition is satisfied.

Do not make canonical engine behavior depend on uncertain spelling of the jargon term itself.
## Decision-critical implications

### 1. Trade stop reference is no longer completely source-empty

The videos provide direct Buy-side teaching evidence that the confirmed wick/check area is an SL/invalidation reference.

However, two phrasings must be reconciled rather than collapsed:

- clip 2: `จุดเช็ก SL / จุดวาง SL` at the confirmed wick/check area;
- clip 1: place SL below the referenced low by `100` points in that example.

Current safe state:

`BUY STOP REFERENCE = SOURCE-BACKED AT CONFIRMED CHECK WICK / LOCAL LOW AREA`

`UNIVERSAL NUMERIC BUFFER = NOT YET CLOSED`

`SELL MIRROR = NOT ESTABLISHED BY THESE TWO CLIPS`

### 2. Target anchor is materially re-anchored

The videos directly state that the timeframe target distance is counted from the wick reference:

- H1: wick + 1,000 points in the shown Buy direction;
- H4: wick + 1,500 points in the shown Buy direction;
- Day: wick + 5,000 points in the shown Buy direction.

This supports the old `ORIGIN_TARGET_LEVEL` representation more directly than the V2.0 `PATH_REMAINING_AT_CONFIRMATION` formula.

The existing owner guidance that a late 07:00 entry participates only in an unfinished prior run is not contradicted. It can be reconciled as:

`original wick target remains fixed; a later entry has only the directional distance remaining to that fixed target.`

What is no longer safe is to treat outcome-ranked `PATH_REMAINING_AT_CONFIRMATION` as instructor-intent proof.

### 3. Day = 5,000 receives a stronger bounded source example

The long clip explicitly gives Day = 5,000 points in the same wick-to-TP explanation.

This strengthens `5,000` as a source-backed Day target example/stage.

It still does not prove that every Day setup universally uses only 5,000 or resolve the previously observed broader 5,000–10,000 Day run family/stage transition.

### 4. V2.0 must remain historical

`0700_MINIMAL_V2.0` was frozen and outcomes were already opened. It must not be silently edited.

If the source re-anchor is promoted after the frozen review, target/SL semantic changes require a new version.

Historical V2.0 `PATH_REMAINING_AT_CONFIRMATION` outcomes remain valid evidence about that representation, not about the newly supplied source geometry.