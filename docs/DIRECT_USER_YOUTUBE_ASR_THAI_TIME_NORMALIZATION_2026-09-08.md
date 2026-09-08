# Direct User Clarification — YouTube ASR Thai Spoken-Time Normalization — 2026-09-08

Status: USER-DIRECT METHODOLOGY / TRANSCRIPT NORMALIZATION GUARD

## Trigger

Project owner clarified a recurring YouTube transcript risk: Thai spoken time expressions may be rendered by YouTube ASR as clock-formatted numerals. The transcript text can therefore look more formal/numeric than what was actually spoken.

Examples supplied directly by the project owner:

- speaker says `9 โมง` -> YouTube may render `9:00`
- `18:00` in ordinary Thai spoken-time context corresponds to `6 โมงเย็น`
- `19:00` corresponds to `1 ทุ่ม`
- `23:00` corresponds to `5 ทุ่ม`
- `24:00` corresponds to `เที่ยงคืน`

These examples are normalization guidance for interpreting transcript time tokens. They do not mean every numeric token in every transcript is automatically a time-of-day expression.

## Required evidence handling

Never overwrite the YouTube transcript text with a normalized interpretation.

Preserve at least two layers:

```text
RAW_TRANSCRIPT
-> NORMALIZED_THAI_TIME_INTERPRETATION
```

Recommended fields:

```text
video_id
source_timestamp
raw_transcript_text
raw_time_token
spoken_time_interpretation_th
normalized_local_clock
normalization_basis
confidence
video_audio_crosscheck_status
date_rollover_if_machine_normalized
```

Example:

```text
raw_time_token                  = 19:00
spoken_time_interpretation_th   = 1 ทุ่ม
normalized_local_clock          = 19:00
normalization_basis             = USER_DIRECT_THAI_TIME_MAPPING
```

For `24:00`, preserve the source token and spoken meaning `เที่ยงคืน`. If a machine datetime later requires conversion to `00:00` on the following date, record that as a separate derived date-rollover transformation rather than silently replacing the source wording.

## ASR interpretation guard

A transcript token such as `9:00` may be YouTube's formatting of spoken `9 โมง`; it must not be treated as proof that the speaker literally said a formal 24-hour clock expression.

When time wording materially affects a trading rule:

1. preserve the raw YouTube transcript token;
2. inspect the surrounding Thai sentence;
3. normalize using Thai spoken-time semantics only when context supports it;
4. audio/video cross-check if ambiguity can change an algorithmic boundary;
5. keep timezone attribution separate from spoken-time normalization.

## Timezone separation

This clarification concerns how Thai speech may be represented by YouTube ASR. It does not by itself prove a timezone for every video.

Existing project-specific timezone mappings, such as owner-confirmed ordinary Thai lesson-time interpretation for the relevant Mae Pla/Por Chon teaching context, remain separate provenance claims and must stay traceable to their own evidence.

## Research consequence

Transcript extraction should no longer treat formatted time strings as verbatim spoken clock notation. Numeric time tokens are high-risk ASR normalization points and should retain both the raw representation and the interpreted Thai spoken-time layer.

This is especially important for research around `07:00`, `19:00`, `23:00`, `24:00`, session/cutoff windows, candle inclusion, and date-boundary logic.
