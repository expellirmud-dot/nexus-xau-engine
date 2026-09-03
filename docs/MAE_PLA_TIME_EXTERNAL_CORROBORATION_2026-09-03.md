# Mae Pla Time External Corroboration — 2026-09-03

Status: EXTERNAL CORROBORATION / NOT PRIMARY VIDEO CONFIRMATION

## Search objective

Search public web/YouTube-indexed material for evidence about whether the Mae Pla system's `07:00` and related frame times refer to Thai local time.

## Direct YouTube search result

Public web search did not surface an indexable UNLOCK TRADER / Mae Pla video whose transcript could be directly opened and timestamp-cited for the time-zone statement. Known YouTube URLs in the project also could not be fetched through the web cache.

Therefore this pass does NOT claim direct primary-video confirmation.

## External teaching-material corroboration

### FlipHTML5 — `เอกสาร สอนระบบแม่ปลา 2`

Attribution shown: `By: ศิษย์พี่...จ้าวคะ`.

Visible text includes:

- `เช้า 07.00 น. จบแท่ง Day H4 H1 เรียบร้อย (H4 โบรค EXNESS เท่านั้น)`

This strongly supports a morning/local operating convention and ties the 07:00 rule to Exness H4 candle completion, but it does not explicitly print `UTC+7`.

Evidence class: associated teaching/student material; not confirmed official Mae Pla primary video.

### FlipHTML5 — `E-book กรอบมหัศจรรย์`

Visible text states H4 timing referenced to Exness, including the first H4 block starting at `07.00`, and says the Mae Pla frame is drawn at `07.00` because Day/H4 have completed.

Evidence class: associated teaching/student material; not confirmed official primary source.

## Explicit UTC+7 secondary corroboration

Multiple independent public implementations/summaries explicitly interpret the Mae Pla daily frame as `07:00 UTC+7 / Thai Time`, including:

- `maeplagreenpen.com` concept page: Daily Frame at `07:00 (UTC+7)` and ATH timing at `19:00 (UTC+7)`.
- TradingView `Green Pen Indi by Wachi`: daily reference based on `07:00 AM (UTC+7 / Thai Time)`.
- TradingView community listing for related Green Pen frame tools also describes 07:00 Thai time.

These are secondary/implementation sources, not authority over the teacher, but they independently converge on the same clock interpretation.

## Historical Exness corroboration

A Thai trading forum post from 2020 describes Exness Day/H4 boundaries in Thailand local time as:

- Day changes around `07:00` Thai time;
- H4 blocks after the Monday open are `07:00–11:00`, then every four hours.

This is third-party historical broker evidence, not a system rule, but it explains why Thai traders may naturally describe the Exness H4/D1 boundary as 07:00 local time.

## Current official Exness evidence

Current Exness Help Center states:

- MetaTrader server time = `GMT+0 / UTC+0`;
- server timezone cannot be changed;
- Thailand is GMT+7.

Therefore:

```text
07:00 Thailand = 00:00 Exness server UTC
```

The validated project dataset has D1/H4/H1 boundaries at UTC00, so the current broker data structure is consistent with the external Thai-time interpretation.

## Evidence synthesis

The evidence now separates into:

```text
PRIMARY PROJECT IMAGE FACT:
  07:00; Day/H4/H1 completed.

DIRECT PRIMARY VIDEO CONFIRMATION OF TIMEZONE:
  not yet found.

ASSOCIATED TEACHING MATERIAL:
  calls it morning 07:00 and ties it to Exness H4 completion.

MULTIPLE SECONDARY IMPLEMENTATIONS:
  explicitly say UTC+7 / Thai Time.

OFFICIAL EXNESS CURRENT CLOCK:
  GMT+0, so Thai 07:00 = UTC00.

LOCAL MT5 DATA:
  UTC00 is a D1/H4/H1 boundary.
```

Research conclusion: `07:00 = Thailand local time = UTC00` is now strongly externally corroborated and is the leading research mapping. It is still not labeled PRIMARY-VIDEO-CONFIRMED until a direct Mae Pla/UNLOCK TRADER video/transcript statement is recovered.

## Engineering consequence

Use UTC00 as the preferred research timing variant for the Mae Pla daily frame, but retain provenance status in every result:

`timing_status = STRONGLY_CORROBORATED_NOT_PRIMARY_VIDEO_CONFIRMED`

Do not use outcome/P&L to upgrade this status.
