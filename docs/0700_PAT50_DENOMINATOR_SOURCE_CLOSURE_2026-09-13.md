# 07:00 PAT >50% Denominator Source Closure — PAT2 Closed / PAT3 Combined Still Open — 2026-09-13

Status: PAT2 DENOMINATOR CLOSED / PAT3 MULTI-CANDLE DENOMINATOR STILL UNRESOLVED

## Sources

### Primary PA/PAT lesson

https://youtu.be/1E_PYPor1qQ

Title:

`Part 1 : พฤติกรรมการเกิด PA ระบบเทรดแม่ปลาปากกาเขียว`

### Cross-check PA/PAT foundation

https://youtu.be/NwMl2cUMb-A

Title:

`EP.1 พื้นฐานระบบแม่ปลาปากกาเขียว #SmatTrderToSuccess #ระบบแม่ปลาปากกาเขียว`

Both sources were reviewed through NEXUS Remote Chrome / YouTube transcript.

---

## 1. Primary PAT2 wording

Around ~13:48–14:38 in `1E_PYPor1qQ`:

- PAT2 is taught as a two-candle reversal;
- full engulfing is stronger but not mandatory;
- around ~14:05 instructor states the second candle can still qualify when it closes `>50%`;
- around ~14:22–14:29 instructor explicitly says the **green candle body** is over half / 50% of the red candle.

This closes an important numerator/confirmation semantic:

```text
confirming candle BODY / close position
is what must pass the half reference
```

The source uses strict language `เกินครึ่ง` / `>50%`.

---

## 2. Cross-check source gives the denominator geometry

Around ~56:14–57:09 in `NwMl2cUMb-A`:

- PAT2 does not need full engulfing;
- the second candle may close around the 50% reference of the previous candle;
- instructor says the 50% can be judged visually or measured with Fibonacci **inside the candle**.

Immediately afterward, around ~57:43–58:14:

- instructor answers that the wick can be included:
  `นับรวมไส้ได้`;
- says to look at both wick and body of the candle;
- separately emphasizes that when reading candle **force**, body is the most important feature.

This distinction is critical:

```text
50% geometric candle range may include wick
while
force/confirmation quality is read primarily from body
```

The two concepts must not be collapsed.

---

# PAT2 source closure

For a single prior candle PAT2 midpoint reference, the safest source-backed geometry is:

```text
previous_range_mid
    = (previous.high + previous.low) / 2
```

BUY qualification:

```text
confirming candle bullish
confirming BODY / close passes above previous_range_mid
strict source semantic: > 50%
```

SELL mirrors direction:

```text
confirming candle bearish
confirming BODY / close passes below previous_range_mid
```

Full engulfing remains stronger/nicer teaching geometry but is not mandatory.

## Evidence class

`SOURCE-BACKED PAT2 MIDPOINT BASIS = FULL CANDLE RANGE (HIGH-LOW, WICK INCLUDED)`

This resolves the earlier BODY-vs-FULL_RANGE ambiguity **for PAT2 single-candle denominator**.

---

# What is NOT closed

## PAT3 combined-candle denominator

The primary source contains several PAT3 variants.

### PAT3 variant 1

Around ~15:46–15:52:

- confirming body should exceed half of the red candle.

This appears compatible with the PAT2 single-candle full-range reference, but the targeted cross-check did not independently provide a discriminating PAT3-v1 measurement example.

Safe status:

`LIKELY SAME SINGLE-CANDLE BASIS / NOT UPGRADED BEYOND PAT2 CLOSURE WITHOUT DEDICATED DISCRIMINATING CASE`

### PAT3 variant 2

Around ~16:53–17:10:

- instructor says green body should exceed half of **two red candles combined**.

Still unresolved:

What exactly does “two red candles combined” mean mathematically?

Candidates include:

- sum of two candle bodies;
- combined high-to-low envelope;
- sequential/visual aggregate geometry;
- another teacher-specific construction.

No exact formula is promoted.

### PAT3 variant 3

Around ~17:25–17:56:

- first green candle alone does not exceed half;
- third candle confirms;
- two green candles together are described as exceeding half of the red candle.

Exact multi-candle arithmetic remains unresolved.

---

# Engineering consequence

A future PAT detector may now separate:

```text
PAT2.midpoint_basis = FULL_RANGE
PAT2.midpoint = (prior.high + prior.low) / 2
PAT2.strict_pass = confirmation close beyond midpoint in direction
```

Do not silently apply the same arithmetic to all PAT3 variants.

Keep explicit parameters/state:

```text
PAT3.variant1_midpoint_basis = NEED_DEDICATED_CONFIRMATION
PAT3.variant2_combined_denominator = UNKNOWN
PAT3.variant3_combined_numerator_or_sequence = UNKNOWN
```

## Frozen research history

Existing Q1–Q4 historical work used a PAT2 BODY-midpoint proxy as an explicitly labeled research representation.

That proxy was correct to preserve as a frozen historical representation at the time.

This source closure must **not** retroactively rewrite Q1–Q4 results.

A future separately versioned dataset/detector should introduce:

`PAT2_FULL_RANGE_SOURCE_CLOSED`

and compare it prospectively / on development data without rewriting frozen history.

---

# Claim boundary

This closure does not establish:

- exact PAT3 multi-candle arithmetic;
- any PAT performance edge;
- a Win Rate;
- a trading threshold selected from outcome;
- a universal wick tolerance;
- universal PAT location by shape alone.

PAT location/frame qualification remains a separate mandatory source dimension.
