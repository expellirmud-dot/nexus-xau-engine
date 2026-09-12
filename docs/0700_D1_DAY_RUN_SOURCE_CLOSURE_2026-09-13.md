# 07:00 D1 / Day Run Source Closure — EP.2 Targeted Re-review — 2026-09-13

Status: CLOSED AT STAGED-RUN LEVEL / NOT A SINGLE UNIVERSAL MAXIMUM

## Source

YouTube:

https://youtu.be/ESHDuiVPJow

Repository title:

`EP.2 เทรน ชนะ กรอบ กรอบ ชนะ Sig #SmatTrderToSuccess #ระบบแม่ปลาปากกาเขียว`

Evidence used:

- local MP4;
- old repository transcript as timestamp locator only;
- fresh targeted Google Speech Recognition from the actual audio;
- existing direct-relative / teaching-slide evidence already preserved in the project.

The old transcript file contains encoding corruption. Numeric/source closure below relies on re-transcribed audio plus cross-check against existing project evidence, not on the corrupted characters.

## Targeted windows reviewed

### ~1:31:05–1:31:51

Fresh audio transcription supports:

- Day example has already run about `7,000` points;
- speaker says it has not yet run the `10,000` reference;
- nearby explanation states `100%` / full round at `5,000`;
- H4 and H1 are separately reiterated as approximately `1,500` and `1,000`.

This strongly separates:

```text
D1 first/full nominal round ≈ 5,000
D1 continuation / extended reference toward 10,000
```

rather than defining one universal `D1 = 10,000` constant.

### ~1:34:21–1:35:00

The teacher discusses Day Sideway width in the rough `3,000–5,000` region and explains that H1/H4 can still complete their own runs inside larger-timeframe Sideway space.

These values describe Sideway/frame space, not a replacement D1 native run constant.

### ~1:36:02–1:36:38

Fresh audio contains explicit wording that price can complete approximately:

`Time Frame Day 10,000 points`

The continuation then discusses multi-SIG / multi-set behavior inside Day.

A later phrase describes approximately:

- first set around `10,000`;
- second set around `5,000`;
- combined movement around `15,000`.

This is evidence that Day can contain sequential run/set extensions.

It is **not** evidence that the single native Day nominal run is universally 15,000.

### ~1:41:18–1:42:24

The visible example is described as roughly `7,000` points in Time Frame Day / Day Sideway space, with lower-timeframe H4 sets considered inside that area.

This is an example measurement, not the canonical D1 nominal constant.

### ~2:56:55–2:57:09

Teacher states conceptually:

`Day target complete, while H4 is still working`

This closes an important lifecycle property:

```text
higher-timeframe target completion
does not imply every lower-timeframe active run is simultaneously complete
```

The engine/research representation must preserve per-origin/per-timeframe lifecycle rather than globally zeroing all lower-TF origins when Day completes.

## Cross-check with existing project evidence

Earlier direct-relative / teaching-slide evidence already preserved:

```text
H1 = 1,000
H4 = 1,500 at 100%, continuation references toward 3,000
Day = 5,000–10,000
Week = 15,000–30,000
Month = 30,000–50,000
```

The targeted EP.2 re-review is consistent with that table and adds stage semantics for Day.

## Source-backed D1 staged representation

Safe source representation for future research versions:

```text
D1_PRIMARY_RUN_POINTS = 5,000
D1_CONTINUATION_REFERENCE_POINTS = 10,000
```

Interpretation:

- `5,000` = nominal first/full round / 100% reference supported by the reviewed teaching context;
- `10,000` = extended/continuation completion reference repeatedly discussed for Day;
- movement can exceed 10,000 through multiple SIG/set sequences;
- do not interpret 10,000 as a universal hard cap.

## Important distinction: native run vs Sideway width

Do not merge these quantities:

```text
Day native nominal run      ≈ 5,000
Day continuation reference ≈ 10,000
Day Sideway example width   ≈ 3,000–5,000 in reviewed passage
multi-set Day movement      can extend beyond 10,000
```

They are different source concepts.

## 07:00 research implication

The earlier `0700_STATE_DATASET_V1` deliberately stored:

`D1 nominal_run_points = UNKNOWN`

That was correct for the evidence state at the time.

This closure does **not** retroactively modify Q1–Q4 or frozen holdout semantics.

For a future separately versioned 07:00 dataset/research engine, D1 can now be represented as a staged source-backed run family:

```text
primary nominal = 5,000
continuation reference = 10,000
```

Remaining research question:

When a 07:00 inherited D1 origin has already passed 5,000 but not 10,000, should remaining-run participation be represented as:

- continuation from the same SIG origin;
- a new/secondary SIG-set lifecycle;
- or a separately classified OVER_RUN / continuation state?

The source clearly supports the staged distances but the exact state-transition rule between the 5,000 and 10,000 stages still requires bounded source/state analysis.

## Lifecycle closure

Source-backed:

```text
Day completion != H4 completion
```

Track active runs independently by timeframe/origin.

Do not globally invalidate H4 merely because the Day target has completed.

## Claim boundary

This closure does not claim:

- D1 always stops at 5,000;
- D1 always reaches 10,000;
- 10,000 is a hard cap;
- 15,000 is the universal D1 run;
- every Day Sideway is 3,000–5,000;
- a new trading threshold;
- profitability or Win Rate.

It closes the staged run-distance interpretation only.
