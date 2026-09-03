# Por Chon Visual Standing-Frame Evidence — 2026-09-03

Status: FIRST-PARTY POR CHON VIDEO VISUAL + YOUTUBE TRANSCRIPT CONTEXT / PARTIAL RULE CLOSURE

## Source package

Project owner supplied a screenshot from the first-party Por Chon lesson `หลักการตีกรอบพ่อชลและเงื่อนไขการใช้จุดพักครึ่งพักสวิง` while the video, H4 chart and YouTube Show transcript were visible together.

Relevant visible transcript window is approximately 19:34–20:41, with the H4 chart displayed at the same time.

Project-owner clarification already establishes that the speaker in this video is Por Chon himself. Exact subtitle wording remains subject to YouTube ASR risk, but the visual chart and repeated spoken/transcript context materially strengthen the interpretation.

## What the screenshot materially clarifies

### 1. `ยืนกรอบ` is body-sensitive, not wick-touch-only

Visible transcript around ~20:00 says, in substance:

```text
กลับมายืนกรอบได้ต่อ
เนื้อแท่ง...
ตอน 23:00...
ก่อนตอน 19:00...ไม่หลุดกรอบ
```

The full supplied transcript around the same passage also repeatedly uses wording equivalent to:

```text
เนื้อไม่หลุดกรอบ
```

The chart visibly contains H4 candles whose wicks interact with / pierce reference levels while the discussion still treats the setup in terms of whether the candle **body stands / does not break the frame**.

Safe semantic closure:

```text
wick penetration by itself is NOT sufficient to declare Por Chon frame failure;
candle-body relation to the frame is a primary standing/break criterion.
```

This is stronger than the previous generic `standing` shell and should prevent the engine from rejecting a frame merely because `low < frame` or `high > frame` on wick alone.

Still unresolved:

- whether the canonical pass condition requires both open and close to remain on the valid side of the line;
- whether body intersection with the line is accepted;
- whether close alone can rescue a body that crossed the line earlier in the bar;
- exact directional symmetry for every Buy/Sell setup.

Therefore do NOT yet encode `close > frame => STAND` as a universal final rule.

### 2. The 19:00 -> 23:00 H4 sequence is operationally meaningful

The passage explicitly compares `19:00` and `23:00` while discussing the same H4 standing/retest behavior.

Interpretation supported by the lesson context:

```text
19:00 = Por Chon daily cutoff / change boundary
19:00->23:00 H4 bar = first post-cutoff H4 evaluation bar in the shown clock schedule
23:00 = a fully closed H4 checkpoint used to assess whether price/body has returned to / maintained the frame
```

This materially reduces the prior off-by-one ambiguity around the cutoff.

For frame CONSTRUCTION, the earlier source-backed rule remains:

```text
use the highest eligible H4 high made in the completed pre-19:00 window;
post-19:00 movement belongs to the next cutoff window.
```

For frame USAGE after the cutoff, the new visual/audio context shows that the post-19:00 H4 candle can interact with the frame and be evaluated at the later H4 close (23:00 in this schedule).

### 3. `หลุดกรอบ` and `ยืนกรอบ` are state decisions, not mere line touches

The screenshot visually reinforces that Por Chon frame usage is not a simple detector:

```text
if wick touches/breaches frame -> break
```

Instead the state depends on candle-body behavior, PA/SIG context and the completed H4 checkpoint.

Safe engine consequence:

```text
PorChonFrameInteraction raw features should preserve:
- wick_cross
- body_cross
- open_side
- close_side
- body_entirely_above/below
- H4 bar close time relative to cutoff
- PA/SIG state

Do not collapse these to a single touch boolean.
```

## What this does NOT yet close

1. Exact body geometry for `ยืนกรอบ`.
2. Exact body geometry for `หลุดกรอบ`.
3. Whether the 23:00 example is a universal required confirmation or simply the next completed H4 checkpoint in that example.
4. Exact broker/chart timezone label mechanics beyond the project's already confirmed local-clock mapping.
5. Direction-specific standing rules when the frame is approached from below versus above.

## Best next audio check

The most valuable exact-audio pass is still ~19:15–20:50, specifically phrases around:

```text
พ่อนับที่เนื้อเทียน
19:00 หลุดกรอบ
23:00 ถอดไส้กลับขึ้นมา
ยืนกรอบได้
เนื้อไม่หลุดกรอบ
```

If the audio confirms those exact semantics, the project can likely close a measurable `PorChonFrameStanding` rule around body-vs-wick interaction and H4 close checkpoints without guessing.
