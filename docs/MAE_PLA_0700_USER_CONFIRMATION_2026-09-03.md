# Mae Pla 07:00 User-Direct Clarification — 2026-09-03

Status: USER-DIRECT CONFIRMED INTERPRETATION

## Trigger

Project owner clarified that, in the Thai teaching context used by this system, the wording `เจ็ดโมงเช้า` is to be interpreted as ordinary Thailand local clock time.

## Confirmed project interpretation

```text
เจ็ดโมงเช้า = 07:00 Asia/Bangkok
Asia/Bangkok = UTC+7
07:00 Asia/Bangkok = 00:00 UTC
```

This closes the project-level operational interpretation of the Mae Pla daily preparation clock.

## Provenance distinction

This is not recorded as a claim that the instructor explicitly said the words `เวลาไทย`.

Instead the evidence chain is preserved as:

1. teaching material/source wording uses `07:00` / `เจ็ดโมงเช้า` in the Thai lesson context;
2. project owner directly confirms that `เจ็ดโมงเช้า` in this context means Thailand local time;
3. engineering normalization maps that local time to `00:00 UTC`.

Therefore:

```text
source wording: 07:00 / เจ็ดโมงเช้า
clock interpretation: USER-DIRECT CONFIRMED
canonical project timezone: Asia/Bangkok
normalized research time: 00:00 UTC
```

## Supporting consistency

This mapping is also consistent with the validated XAUUSDm data where D1/H4/H1 boundaries align at UTC 00:00, and with the teaching statement that Day, H4 and H1 are completed at the morning preparation time.

The consistency check supports the mapping but did not choose it; the project-owner clarification closes the interpretation.

## Engineering consequence

- Use `Asia/Bangkok 07:00` as the canonical Mae Pla daily-preparation clock in research/replay.
- Normalize to `UTC 00:00` for the current validated MT5 dataset.
- Keep timezone metadata explicit in generated frame/event records.
- Do not use outcome/P&L to re-select the clock.
- If a future stronger primary source explicitly states a different clock, preserve this record and review the conflict rather than silently replacing history.
