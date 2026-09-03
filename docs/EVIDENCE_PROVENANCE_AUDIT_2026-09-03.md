# Evidence Provenance Audit — 2026-09-03

Status: METHODOLOGY CORRECTION / PRESERVE OLD RECORDS

## Trigger

Project owner identified a serious research risk: evidence may pass through several extraction/summarization layers and later be stored without preserving which layer produced which wording. A later analyst can then mistake a rewritten statement for a direct instructor fact.

This is a provenance-loss / evidence-laundering risk.

## Important clarification from project owner — corrected

The YouTube transcripts used in this project are **YouTube-provided transcripts generated from the video's captions**, not a human manually transcribing word-for-word and not an AI analyst watching the video and writing a summary.

The correct source chain is:

```text
Original instructor YouTube live/video
-> YouTube automatic speech recognition / auto-generated captions
-> YouTube Show transcript text with timestamps
-> later analyst extraction / rule synthesis
```

Therefore these transcript lines are classified as **primary attributable transcript evidence with ASR risk** when the original video and timestamp remain traceable.

Suggested provenance fields:

```text
source_origin = ORIGINAL_INSTRUCTOR_VIDEO
capture_method = YOUTUBE_SHOW_TRANSCRIPT
extraction_method = YOUTUBE_AUTO_CAPTION_ASR
interpretation_level = DIRECT_TRANSCRIPT
source_locator = timestamp
```

They may support `CONFIRMED` rules when wording is mechanically explicit, but high-impact wording should be cross-checked against audio/video when ASR could materially change meaning.

High-risk ASR items include:

- numbers and decimals;
- Thai trading jargon / proprietary vocabulary;
- words such as wick/body/close;
- must/only/approximately/no more than;
- timeframe names;
- 07:00 / 19:00 and other time expressions.

Later analyst summaries remain derived evidence even when their input was a YouTube transcript.

## Audit finding: 07:00 case

The claim must be split into separate statements.

### Claim A

`The teaching material references 07:00.`

Status: PRIMARY IMAGE SUPPORTED.

### Claim B

`At 07:00 Day, H4 and H1 should be completed.`

Status: PRIMARY IMAGE SUPPORTED according to the existing image-intake record.

### Claim C

`07:00 means Thai time.`

Status: NOT DIRECTLY SUPPORTED by the currently recorded image/transcript evidence.

Later project documents introduced wording such as `07:00 Thai-time` / `Thai-time context`. That added timezone wording cannot inherit PRIMARY status unless a direct image, YouTube transcript timestamp, or direct user/relative statement explicitly establishes it.

### Corrected status

```text
07:00                        = PRIMARY IMAGE FACT
07:00 + Day/H4/H1 completed  = PRIMARY IMAGE FACT
07:00 timezone               = UNKNOWN
07:00 = Asia/Bangkok         = SUPPORTED/ANALYST INFERENCE ONLY
07:00 Thai -> 00:00 UTC      = DERIVED RESEARCH CANDIDATE
```

## Methodological correction

Evidence rank follows the complete source chain, not merely the file containing the statement.

Required claim provenance should include:

```text
claim_id
claim_text
source_origin
source_id
source_locator
source_actor
capture_method
extraction_method
transformation_chain
interpretation_level
verbatim_available
source_media_available
crosscheck_status
coding_permission
notes
```

## Transcript rule — corrected

### YouTube auto transcript

```text
original instructor video/live
+ YouTube auto-generated captions/ASR
+ timestamp/source locator
```

This is strong attributable source evidence, but not error-free verbatim transcription. ASR risk must be retained.

### Derived forms

- script extracting rules from the YouTube transcript: derived unless exact wording/timestamp remains attached;
- AI summary of transcript: derived;
- analyst paraphrase without timestamp: derived;
- unknown extraction chain: quarantine.

## Coding permission rule

- DIRECT IMAGE / DIRECT USER statement: may be considered for CONFIRMED if mechanically explicit.
- DIRECT YOUTUBE_ASR + traceable timestamp: may be considered for CONFIRMED, but high-impact ambiguous wording should be audio/video cross-checked.
- PARAPHRASE: requires source cross-check.
- SUPPORTED_INFERENCE: research only.
- ANALYST_INFERENCE: hypothesis only.
- UNKNOWN chain: quarantine.

## Immediate project consequence

1. Do not label the YouTube transcripts as manual verbatim transcripts.
2. Preserve their value as timestamped, attributable transcript evidence.
3. Retain an explicit `ASR_RISK` flag.
4. Do not treat later analyst synthesis as primary merely because its input was a YouTube transcript.
5. Do not treat `07:00 Thai-time` as confirmed unless a direct source explicitly says so.
6. Preserve historical documents and corrections rather than silently rewriting research history.

This correction changes the provenance label, not the underlying transcript content already extracted from YouTube.
