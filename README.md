# NEXUS XAU Engine

Research-first reverse engineering of the Mae Pla Green Pen trading framework for XAUUSD on MetaTrader 5 / Exness.

## Purpose

This repository is the durable project record for the current research. The immediate goal is **not** live auto-trading. The goal is to convert the teaching into reproducible, testable rules for:

1. historical-data research,
2. rule detection,
3. replay testing,
4. backtesting,
5. only later, execution in MT5 if the rules survive validation.

## Evidence standard

Every rule must be tagged by evidence level:

- **A — Direct / Primary:** user-provided screenshots, transcript excerpts, direct explanation from the user's relative, or identifiable primary teaching material.
- **B — Public instructor/channel:** public videos/posts from UNLOCK TRADER / @Unlocktrader007 or other clearly attributable instructor material.
- **C — Secondary:** third-party summaries such as maeplagreenpen.com, Lemon8 posts, or other learner summaries.
- **D — Inference:** analyst interpretation that is not yet safe to code.

A deterministic rule is eligible for code only when its input, condition, output, invalidation and timeframe are sufficiently defined. If evidence is insufficient, status must remain **UNRESOLVED**.

## Current modules

- `Frame Engine` — Mae Pla statistical frame / Por Chon ATH frame / support-resistance
- `PA/PAT Engine` — PA Buy/Sell, PAT1/2/3
- `SIG Engine` — SIG confirmation and post-SIG wick anchor
- `Cycle Engine` — Sideway → SIG → TP → Retrace → Sideway
- `Multi-TF Engine` — H1/H4/D/W plus M5/M15/M30 relationship
- `Retracement Engine` — half retrace / swing retrace / Fibonacci reference
- `Entry Engine` — entry conditions, body collection, close-to-frame rules
- `Risk Engine` — SL / TP / position management
- `Replay Engine` — future-hidden event replay
- `Backtest Engine` — historical statistical validation

## Files

- `docs/RULEBOOK.md` — current rulebook, separated by evidence level
- `docs/EVIDENCE_REGISTER.md` — source index and source reliability
- `docs/OPEN_GAPS.md` — unresolved mechanical rules that block deterministic coding
- `docs/RESEARCH_LOG.md` — chronology of findings and corrections
- `docs/ENGINE_SCHEMA.md` — proposed machine-readable objects and state model

## Scope

Primary instrument: `XAUUSD`.

The exact MT5 symbol specification must be read from the actual broker/server used for testing before strict point conversion or live-equivalent calculations are trusted.