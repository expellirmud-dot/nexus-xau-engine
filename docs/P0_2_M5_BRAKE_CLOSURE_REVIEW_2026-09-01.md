# P0-2 M5 Brake / Entry Closure Review — 2026-09-01

Source: full user-supplied timestamp transcript for the M1/M5 entry lesson associated with `16KoS7d-koI`, plus current repository evidence.

Evidence rank: PRIMARY TEACHING TRANSCRIPT. ASR errors are possible; numerical geometry is only promoted when directly supported.

## Verdict

P0-2 is no longer a discovery-level blocker. It is now a **geometry/tolerance finalization problem**.

Recommended closure estimate:

- M5 brake workflow / sequence / purpose: **~90% closed**
- `ยืนกรอบ` concept and counting: **~80–85% closed**
- exact OHLC detector without manual thresholds: **~75–80% closed**
- overall P0-2 closure: **~80%**

This is enough to build an evidence-tagged `M5_BRAKE_CANDIDATE` detector and replay state machine, but not enough to label `confirm_m5_brake_exact()` production-deterministic.

## What is now CLOSED or strongly supported

### A. Context qualification — CLOSED

- M5/M1 brake is searched only after price reaches a prepared support/resistance/TP-complete/rest zone.
- Zone is a waiting area, not an automatic reversal price.
- Counter/retracement M5 entry requires both a prepared zone and the brake pattern.

### B. M1/M5 relationship — CLOSED

- M1 and M5 use the same broad pattern logic.
- M1 is more volatile/refined; M5 is the safer/default confirmation view.
- M1 uses trendline/local-structure support as an extra refinement.

### C. Five-step candle-force sequence — CLOSED at logical level

`ใหญ่ยาว -> อ่อนแรง -> รีเจค -> เปลี่ยนสี -> รีเทส`

- The steps are logical states, not necessarily five separate candles.
- Weakening/rejection/color-change can occur in the same bar.
- Missing retest can leave the setup incomplete.

### D. Entry timing — CLOSED at workflow level

- First reaction/brake is higher-risk and may be only a scout/test.
- Preferred entry is the second/retest opportunity after confirmation.
- Do not default to entering on the first wick reaction.

### E. Retest semantics — MOSTLY CLOSED

A true retest is structural:

- price first moves away/through local structure;
- tests the opposite side/resistance-support;
- then returns to the switched/previous level;
- the return is judged with PA, standing and local structure.

Merely sitting on the line is not automatically a full retest.

### F. `ยืนกรอบ` — MOSTLY CLOSED

- start counting from the first candle that touches the frame;
- evaluate about 4–10 closed candles on M1/M5;
- body standing is primary evidence;
- wick interaction/on-line standing may be accepted in context;
- Buy and Sell are directional mirrors;
- repeated standing is used to decide whether the frame is holding.

### G. Structure confirmation — MOSTLY CLOSED

- Buy: higher low / later break of local high supports reversal/continuation up.
- Sell: lower high / loss of support / later break of local low supports move down.
- A single color-change candle is not sufficient by itself.

### H. Overlap / false first brake — CLOSED conceptually

- first brake can be fake and sweep liquidity;
- teacher calls this `overlap` in the lesson;
- ~300 points is a normal reference in the lesson, but high volatility may extend to ~500;
- therefore overlap distance is a feature/context parameter, not a universal hard threshold.

### I. Entry-family separation — CLOSED

`M5_BRAKE_FRAME_ENTRY` and `SIG_ENTRY` are distinct:

- frame/M5 brake entry has no native SIG run anchor at the time of entry;
- manage by local frame/objective (examples mention ~500–1,000 points);
- if a SIG later forms, part of position can be managed by SIG run;
- actual SIG setup uses body collection/post-SIG reference and timeframe run table.

This is important for backtest labeling and prevents mixing setup families.

## What remains OPEN before exact detector

### 1. `ใหญ่ยาว` numeric threshold

Need exact equation based on body/range/relative history/volume. Lesson gives qualitative force reading, not a universal number.

### 2. `อ่อนแรง` numeric threshold

Need body/range shrink equation and lookback reference.

### 3. Rejection wick geometry

Need minimum wick/body ratio, correct side, and tolerance at zone.

### 4. Frame-standing exact predicate

Need exact inequalities for:

- body relative to frame;
- allowed wick penetration;
- equality at frame;
- mixed candles within 4–10 window;
- treatment if confirmation occurs after candle 10.

### 5. Exact local-structure pivot definition

Need deterministic swing/pivot selection for higher-low/lower-high and local high/low break.

### 6. Retest tolerance

Need exact price-distance or overlap tolerance to decide whether return counts as retest versus miss/overshoot/crush-through.

### 7. PA dependency

The M5 brake exact detector still depends on P0-1 exact PA/PAT geometry. PA is explicitly used to distinguish `รับ` versus `ทับ`.

### 8. Negative/positive OHLC corpus

Need enough labeled examples for:

- valid Buy sideway brake;
- valid Sell sideway brake;
- higher-low Buy;
- lower-high Sell;
- overlap false brake;
- no-retest failure;
- wrong-side frame standing;
- `เจิด` continuation through zone;
- M1 refinement versus M5 confirmation.

## Engineering state after closure review

Safe now:

```text
WAIT_ZONE
-> OBSERVE_BRAKE_1
-> READ_FORCE_STATES
-> WAIT_RETEST
-> COUNT_FRAME_STANDING
-> CHECK_PA
-> CHECK_LOCAL_STRUCTURE
-> ENTRY_2_CANDIDATE
```

Candidate interfaces:

- `detect_force_state_candidate()`
- `detect_rejection_candidate()`
- `frame_standing_candidate(window=4..10)`
- `detect_retest_candidate()`
- `detect_local_structure_shift_candidate()`
- `detect_overlap_candidate()`
- `confirm_m5_brake_candidate()`
- `confirm_m1_brake_candidate()`

Remain placeholder/exact-disabled:

- `detect_large_force_exact()`
- `detect_weakening_exact()`
- `detect_rejection_exact()`
- `frame_standing_exact()`
- `retest_exact()`
- `confirm_m5_brake_exact()`

## Analyst conclusion

P0-2 can be considered **closed for Rule Engine architecture and Candidate Detector work**, but **not closed for exact unattended backtest/live classification**. The remaining ~20% is mostly numeric geometry/tolerance and labeled edge cases, not missing workflow knowledge.

The next evidence with highest value is the final candle-reading lesson, because it may close the quantitative definitions of `ใหญ่ยาว`, `อ่อนแรง`, wick rejection and related force thresholds. A dedicated structure/sideway lesson would then close the remaining frame-standing/pivot/tolerance edges.