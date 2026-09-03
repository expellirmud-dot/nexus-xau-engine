# Location Truth Set Seed — 2026-09-03

Status: TEXT-LABELED SEED / NOT OHLC GROUND TRUTH

## Purpose

Create a durable evidence queue for PAT/location qualification without using future price outcome to invent a tolerance.

Seed file:

`results/LOCATION_TRUTH_SET_SEED_2026-09-03.csv`

## Current seed cases

The current repository supports five text-labeled cases/teaching examples:

- Buy-form PA at resistance -> wrong location.
- Sell-form PA at support -> wrong location.
- PA Buy PAT2 at support where the first post-SIG reference later invalidates the first setup, followed by a replacement PAT2/post-SIG sequence.
- M5 live example where price returns and stands on a marked support/black line.
- M1/M5 frame-standing teaching: start count at first frame touch; observe roughly 4–10 candles; bodies are primary standing evidence and wick-on-line is secondary.

## Critical limitation

These cases are currently `TEXT_LABELED_NOT_OHLC_ALIGNED`.

The repository does not contain the original teaching images/video frames as local image files with a recoverable market timestamp and exact frame price. Therefore these cases cannot yet provide numeric truth for:

- exact support/resistance price;
- wick/body/close distance;
- penetration allowance;
- tolerance in project points;
- exact candle OHLC against the teacher-drawn boundary.

They are valid semantic labels, not numeric OHLC labels.

## Promotion rule

A seed case may be promoted to `OHLC_ALIGNED` only when the following are known before outcome review:

```text
market timestamp / bar ids
symbol + broker/timezone
working timeframe
PAT label + side
boundary source family
boundary line or zone prices
teacher/relative valid-vs-invalid label
source timestamp/screenshot reference
```

Once aligned, `src/nexus_xau/engine/location_interaction.py` can extract threshold-free geometry and the project can compare positive and negative labels.

## Research discipline

Do not use later MFE/MAE/P&L to decide which boundary distance should have counted as valid. The location label/rule must be frozen from source evidence first, then outcome may score it.

## Next acquisition target

Highest-value new evidence is a chart/screenshot or video-frame extraction for the existing L001–L005 teaching cases that exposes enough price/time information to align them with OHLC data. If exact market time is unavailable, a clearly readable candle OHLC/frame price annotation can also close individual geometric questions manually.
