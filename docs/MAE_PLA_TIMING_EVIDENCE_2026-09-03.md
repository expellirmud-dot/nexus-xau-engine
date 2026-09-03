# Mae Pla 07:00 Timing Evidence — 2026-09-03

Status: SUPPORTED INFERENCE / NOT YET CANONICAL

## Primary project evidence

Primary teaching-image evidence already stored in the project supports:

- daily preparation around `07:00`;
- at that time Day, H4 and H1 candles should be completed;
- use the H4/opening-price context around 07:00;
- select a nearby statistical reference whose price ends in 0 or 5;
- upper/lower frame = reference +/- 500 project points.

The teaching source does not explicitly say whether 07:00 is Thai local time, broker/server time or another clock.

## External broker evidence checked on 2026-09-03

Current official Exness material states that MetaTrader 4 and MetaTrader 5 display synchronized server time at UTC+0 / GMT+0. Exness trading-hour material is also published on a UTC+0 basis.

External source class: current official broker documentation. This evidence can clarify broker clock behavior but cannot by itself redefine the teacher's intended clock.

## Local-data evidence

The validated XAUUSDm dataset uses UTC timestamps. Local M1 resampling matches MT5 native bars exactly across the expanded sample:

```text
M5 mismatches = 0
H1 mismatches = 0
H4 mismatches = 0
D1 mismatches = 0
```

Native/local H4 boundaries are aligned to UTC 00:00, 04:00, 08:00, ... and D1 changes at UTC 00:00 in this dataset.

## Triangulation

If teaching `07:00` means Thai local time (UTC+7):

```text
07:00 Asia/Bangkok = 00:00 UTC
```

At UTC 00:00:

- the prior D1 candle is complete;
- an H4 boundary is complete;
- an H1 boundary is complete.

This is structurally consistent with the teaching statement that Day/H4/H1 should all be completed at 07:00.

If teaching `07:00` means Exness server UTC+0:

- D1 is already complete from 00:00;
- H1 06:00–07:00 completes;
- but the native H4 bar 04:00–08:00 is still open at 07:00.

That interpretation is harder to reconcile with the source wording that H4 should be completed.

## Current inference

Research status:

```text
07:00 teaching time likely = Asia/Bangkok local time
likely UTC mapping = 00:00 UTC
status = SUPPORTED_INFERENCE, not CONFIRMED
```

Reason: primary source wording + official broker UTC+0 clock + native H4/D1 boundaries all point in the same direction.

Remaining caveats:

- the teacher/relative has not explicitly confirmed the timezone in the currently stored source;
- historical Exness/platform behavior or chart configuration could differ;
- the teaching may use a local operational convention rather than literal platform server time.

## Timing-sensitivity measurement

Research-only comparison was run on validated history 2026-05-26 through 2026-09-01 using two explicit H4 context variants: UTC00 and UTC04.

Result:

```text
compared days = 71
same nearest 0/5 reference = 4 / 71 = 5.63%
different reference = 67 / 71 = 94.37%
median minimum reference gap = $20 = 2,000 project points
p75 gap = $30 = 3,000 project points
maximum gap = $70 = 7,000 project points
```

Files:

- `src/nexus_xau/research/mae_pla_time_sensitivity.py`
- `results/XAUUSDm_MAE_PLA_TIME_SENSITIVITY_2026-05-26_2026-09-01.json`
- `results/XAUUSDm_MAE_PLA_TIME_SENSITIVITY_ROWS_2026-05-26_2026-09-01.csv`

Outcome/P&L was not used.

## Interpretation

Time mapping is not a cosmetic implementation detail. A four-hour change in the candidate context changes the selected statistical reference on about 94% of comparable days in this sample, with differences large enough to exceed normal H1/H4 run distances.

Therefore a canonical backtest must not silently choose a 07:00 timezone.

## Engineering decision

- Keep exact timing mapping explicit in all frame records.
- UTC00 may be used as the leading research interpretation because evidence triangulation supports it.
- Do not label UTC00 as canonical until direct teacher/relative evidence confirms that 07:00 means Thai time or otherwise maps to UTC00.
- Do not use outcome performance to choose between UTC00 and another time mapping.
