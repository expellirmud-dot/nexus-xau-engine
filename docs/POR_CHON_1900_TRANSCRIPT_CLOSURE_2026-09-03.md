# Por Chon 19:00 Cutoff / New-High Frame Transcript Closure — 2026-09-03

Status: PRIMARY ATTRIBUTABLE YOUTUBE TRANSCRIPT WITH ASR RISK / RULE SEMANTICS SUBSTANTIALLY CLOSED

## Source

Project owner supplied the YouTube `Show transcript` text for the UNLOCK TRADER lesson titled:

`หลักการตีกรอบพ่อชลและเงื่อนไขการใช้จุดพักครึ่งพักสวิง`

Source chain:

```text
Original UNLOCK TRADER video
-> YouTube auto-generated captions / ASR
-> YouTube Show transcript with timestamps
-> this claim-level extraction
```

Therefore wording remains attributable to the original lesson but carries ASR risk. Repeated statements across many timestamps materially reduce the chance that the core 19:00 rule is a one-line ASR accident.

## Executive closure

The earlier shorthand `19:00–19:00 interval` was too vague. The transcript supports a more precise operational rule:

```text
Por Chon uses a DAILY 19:00 CUTOFF.
For each day/window, inspect H4 highs made BEFORE the 19:00 cutoff.
A new Por Chon New-High/ATH frame is created only if price exceeded the previous Por Chon high frame by MORE THAN 1,000 project points.
When that condition is met, use the highest H4 wick/high achieved before the cutoff as the new high frame.
After 19:00, additional highs belong to the next day's evaluation window rather than changing the already-selected frame for the completed cutoff.
```

Operationally this behaves like consecutive daily buckets bounded by the 19:00 cutoff, i.e. previous cutoff -> next cutoff, but the teacher's repeated phrasing is primarily `ก่อน 19:00` / `19:00 ของอีกวัน` rather than one formal mathematical sentence saying `19:00–19:00`.

## Strong timestamp evidence

### Daily clock context

- ~11:21–11:59: instructor discusses the system's daily clock and says the day closes / a new day begins around `07:00 น.เช้า` in the referenced chart environment.

This establishes that the lesson is explicitly using named operational clock times, not an abstract untimed daily frame.

### Initial Por Chon example

- ~13:35–14:08: instructor describes the day's highest H4/high around the `19:00` boundary and treats it as the first Por Chon high frame candidate.
- ~14:16–14:44: after another day passes, the instructor repeatedly says to evaluate the next day **before 19:00**.
- ~14:53–15:33: if the new day's move exceeds the prior high frame by `1,000 points` before 19:00, the new high can become the next Por Chon frame.

### More-than-1,000 requirement

- ~15:16–15:33: wording states the move can exceed by any amount but must be over `1,000` before the cutoff.
- ~17:18–17:35: example where price does not reach 1,000 points from the previous new high -> do not draw a new frame.
- ~29:10–29:35: recap explicitly says the move must exceed the prior high by more than 1,000 points and use the highest H4 wick/high before 19:00.
- ~30:39–31:02: emphatic recap: `ต้องเกิน 1,000`; if it does not reach 1,000, do not draw the new high frame.

Engineering semantic:

```text
new_high_distance > 1000 project points
```

Do not silently weaken this to `>= 1000` until source wording is audio-checked if exact equality ever matters in a labeled case.

### Highest H4 wick/high before cutoff

- ~17:43–18:07: H4 completed before the 19:00 cutoff is used to identify the relevant high.
- ~18:07–18:23: instructor says the high before the 19:00 bar/cutoff becomes the new-high criterion; later movement is evaluated into the next day.
- ~23:33–24:21: instructor re-explains using H4 as the criterion and the day's high before 19:00.
- ~26:26–26:49: explicit recap: use the **highest H4 wick tip** that exceeded the previous frame by >1,000 points before 19:00.
- ~29:10–29:35: same rule repeated again.
- ~31:40–31:52: high may happen at various times during the day; the relevant object is the highest H4 wick before 19:00.

Engineering semantic:

```text
candidate_high = max(H4.high) within the completed daily cutoff window
frame_price = candidate_high
```

The exact candle-boundary implementation must respect the lesson's `before 19:00` wording and should avoid including a candle whose information was not fully known before the cutoff.

### What happens after 19:00

- ~24:37–25:24: instructor says to count the high before 19:00 only; movement after 19:00 is not added to that completed day's high and is evaluated for the next day's cutoff.
- ~26:49–27:15: after 19:00, use the newly selected frame as the reference for standing/not-standing and later continuation.
- ~29:35–29:51: post-19:00 continuation is assigned to the next day's high evaluation.

Therefore the previous project wording `19:00–19:00` is best understood as a sequence of daily cutoff windows, not as a requirement that the high occur exactly at 19:00.

## Existing-frame persistence

- ~16:23–16:39: when price later falls back, older Por Chon frames remain usable as prior reference/stop-brake frames.
- ~1:01:39–1:02:10: instructor says prior Por Chon frames remain usable and distinguishes Por Chon large-timeframe navigation from Mae Pla frame entry/round use.

This is consistent with prior project evidence that Por Chon frames persist as long-lived references.

## Use / purpose context from this same transcript

The lesson reinforces:

```text
Por Chon frame = large-timeframe New-High / SIG-navigation reference
Mae Pla frame  = more practical entry / brake / SL context
```

- ~18:39–19:15: Por Chon is emphasized for people holding longer and evaluating large-timeframe PA/SIG standing at the frame.
- ~34:00–34:25: Por Chon can be too wide for practical SL, so Mae Pla frame is used together for tighter entry/brake/SL context.
- ~1:04:28–1:04:45: participant summary `กรอบพ่อ = SIG GPS นำทาง` is explicitly approved by instructor; Mae Pla is likened to the boarding/checkpoint location.

## Timezone status — important distinction

### Direct source fact

The transcript repeatedly establishes the operational **clock labels** `07:00`, `19:00`, `23:00`, etc. and the daily 19:00 cutoff behavior.

### What the transcript does NOT literally say

No line in the supplied transcript explicitly says:

```text
19:00 = Asia/Bangkok / UTC+7
```

Therefore do not fabricate that as a direct instructor quote.

### Contextual interpretation

The same Thai-language lesson uses ordinary Thai clock phrasing such as `07:00 น.เช้า`, discusses `19:00` as the daily change/cutoff, and later refers to the live's current clock in ordinary local conversation. Combined with the project owner's direct prior clarification that ordinary Thai lesson-time wording is interpreted as Thailand local time unless a different clock is explicitly named, the project may treat the 19:00 cutoff as the **same local operational clock context** for research.

Recommended project status:

```text
19:00 daily cutoff semantics = SOURCE-BACKED / CLOSED
19:00 clock context          = CONTEXTUALLY CONFIRMED PROJECT INTERPRETATION
19:00 Asia/Bangkok           = canonical research mapping under owner-confirmed language context
19:00 Asia/Bangkok -> 12:00 UTC
```

Do not rewrite this as though the instructor literally uttered `เวลาไทย`.

## Canonical algorithm candidate

For each completed local Por Chon day window:

```pseudo
previous_frame = latest_active_por_chon_high
window = previous_19_00_cutoff -> current_19_00_cutoff
known_h4_bars = H4 bars fully known before current cutoff
candidate = highest H4 high/wick within known_h4_bars

if candidate - previous_frame > 1000 * project_point_size:
    create_new_por_chon_frame(candidate)
else:
    keep_previous_frame()
```

For XAU research normalization under the current project interpretation:

```text
Asia/Bangkok 19:00 = UTC 12:00
```

Exact H4 bar inclusion around the cutoff should be validated against the referenced broker/chart environment before calling a production detector fully closed.

## What is now closed

- 19:00 is a **daily cutoff / change boundary**, not a requirement that the high happen exactly at 19:00.
- evaluate the relevant high **before** that cutoff.
- use H4 as the stated high-selection criterion.
- use the highest H4 wick/high in the window.
- new frame requires **more than 1,000 points** above the prior Por Chon high frame.
- if the threshold is not met, do not create a new frame.
- movement after 19:00 rolls into the next daily evaluation.
- old Por Chon frames can remain usable later.

## What remains open

1. Exact broker/chart H4 candle labeling and inclusion at the 19:00 boundary; transcript gives operational semantics but ASR alone should not decide a one-bar off-by-one implementation.
2. Exact equality behavior at precisely 1,000 points; repeated wording says `เกิน 1,000` / more than 1,000.
3. Tie behavior if two H4 bars have identical highest highs.
4. Exact replacement/retirement policy if several old Por Chon frames coexist.
5. Audio/video cross-check if any future implementation depends on a mechanically sensitive word that appears only once; the core cutoff rule itself is repeated many times and is substantially robust to ASR risk.

## Research consequence

The former blocker `Por Chon 19:00-19:00 timezone/day-window semantics` should be split:

```text
day-window/cutoff semantics -> CLOSED
local clock mapping          -> CANONICAL PROJECT INTERPRETATION, not literal instructor timezone quote
H4 boundary implementation   -> VALIDATION NEEDED
```

This allows the engine to move from a vague 19:00 parameter to an evidence-backed daily cutoff model while preserving provenance discipline.
