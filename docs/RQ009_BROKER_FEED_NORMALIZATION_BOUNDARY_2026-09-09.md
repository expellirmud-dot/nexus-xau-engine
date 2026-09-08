# RQ-009 — Broker / Feed Price Normalization Boundary

Status: `BROKER_TICK_NORMALIZATION_CLOSED_FOR_LITERAL_EQUALITY_CONTACT / ZONE_TOLERANCE_AND_EXECUTION_OPEN`

Date: 2026-09-09 Asia/Bangkok

## Question

How can the engine implement already source-backed literal relations such as:

- `ซอก`: close/open are the same reference price in the taught form;
- `คู่`: aligned/equilibrium open-close reference;
- active post-SIG point-check: touch/contact destroys, near miss survives;

without inventing a positive price tolerance from historical outcomes?

This checkpoint is an **engineering normalization contract**, not a new instructor trading rule.

## Broker/runtime evidence

Primary broker-specific evidence:

- `docs/BROKER_METADATA_EXNESS_MT5TRIAL6_XAUUSDM_2026-09-02.md`
- `docs/DATA_PIPELINE_VALIDATION_2026-09-02.md`

Environment captured on 2026-09-02:

```text
server = Exness-MT5Trial6
symbol = XAUUSDm
digits = 3
point = 0.001
trade_tick_size = 0.001
chart_mode = Bid price
execution = market
spread_float = True
```

This metadata is environment-specific. It must not be generalized to another broker, server, account type, or production symbol without a new runtime specification check.

The validated M1 dataset is bar data from `MetaTrader5.copy_rates_range`, not Bid+Ask tick history.

## Engineering distinction

Three concepts must remain separate:

```text
SOURCE SEMANTIC
    e.g. same price / touch / near miss

BROKER GRID NORMALIZATION
    map observed chart prices to the symbol's valid tick grid

TRADE EXECUTION
    Bid/Ask, spread, slippage, order side, intrabar ordering, actual fill
```

Closing broker-grid normalization does **not** close trade execution.

## Literal equality contract

For the captured `XAUUSDm` environment, a valid quoted chart price lies on a `0.001` price grid.

For a runtime tick size `T`:

```text
tick_index(price) = exact integer price / T
```

Literal source equality is represented as:

```text
literal_same_price(a, b)
    := tick_index(a) == tick_index(b)
```

No additional `±N ticks` tolerance is introduced.

Examples for the captured environment:

```text
3563.590 == 3563.590  -> same tick
3563.590 != 3563.591  -> adjacent tick, not literal equality
```

This is the safest implementation of source wording such as `ราคาเดียวกัน` / same price without outcome-fitting a tolerance.

## Off-grid values fail closed

The normalization layer must not silently round an arbitrary off-grid computed price onto a broker tick.

Example with `tick_size = 0.001`:

```text
4373.383  -> valid broker-grid price
4373.3835 -> off-grid -> reject / explicit upstream normalization required
```

This prevents a hidden half-tick or nearest-tick tolerance from becoming a trading rule.

## Literal chart-contact contract

For a Bid-chart OHLC bar in this captured environment, a source event whose literal semantic is **touch/contact at a known price level** can be represented at bar-resolution as:

```text
bar_contains_level := low_tick <= level_tick <= high_tick
```

Boundary equality counts as contact.

Therefore a one-tick near miss remains a near miss:

```text
reference = 3340.000
bar low   = 3340.001

=> no literal contact
```

This representation is suitable for **chart-side event presence**, including research detection of source-backed post-SIG point-check contact.

## What OHLC contact does not tell us

A bar whose High-Low range contains a level proves only that the observed Bid chart reached that price sometime during the bar.

It does not prove:

- exact intrabar timestamp;
- event ordering when multiple levels are crossed in the same bar;
- Ask-side price at that instant;
- whether a BUY/SELL order would have filled;
- spread or slippage;
- whether TP or SL was reached first if both lie inside the same bar.

Existing project rule remains in force:

```text
same-bar first-hit order without tick data -> AMBIGUOUS_SAME_BAR
```

## Relations this checkpoint does close

### `ซอก` literal same-price relation

Where source geometry calls for a close/open **same-price** joint, the engine may require zero broker-tick difference after runtime grid normalization.

This does not by itself certify every candidate as a valid `ซอก`; same color, candle ordering, source context, and completed-candle requirements still apply.

### `คู่` literal equilibrium relation

Where source geometry explicitly requires the pair's open/close equilibrium reference to be the same price, the engine may require zero broker-tick difference after normalization.

This does not solve universal support/resistance certification or candidate priority.

### Post-SIG point-check touch

The source directly says touch/contact destroys while near miss survives. For bar-level Bid-chart state research, inclusion of the normalized point-check level inside the bar's normalized High-Low range is a deterministic chart-contact event.

This does not establish order execution or Bid/Ask trade fill.

## Relations this checkpoint does NOT close

Do not reuse literal same-tick equality as a universal tolerance for language such as:

- `ชิดกรอบ` / close to frame;
- `เสมอกัน` / stand at the same structural area;
- support/resistance zone grouping;
- `ตรงกัน` across different-timeframe Body Collection structures where the source may be referring to an area rather than one literal tick;
- Sideway frame membership;
- M5 retest structural hold.

Those are structural/zone relations and still require source-backed geometry or an explicitly labeled research representation.

## Broker point is not course/system point

For captured `XAUUSDm`:

```text
BROKER_POINT = 0.001 price units
BROKER_TICK_SIZE = 0.001 price units
```

Teaching statements such as `100`, `200`, `300`, `1,000` system/course points must not be converted by multiplying them by `0.001` merely because this broker uses that point size.

`SYSTEM/PROJECT POINT` and `BROKER POINT` remain separate concepts unless a source-backed/project-owner mapping is explicitly frozen.

## Runtime guard for future use

Production/research code should obtain symbol metadata at runtime and fail closed if the environment does not match the contract being invoked.

At minimum record:

```text
broker/server
symbol
digits
trade_tick_size
chart mode / price source
data modality (bar vs tick; Bid-only vs Bid+Ask)
```

Do not hardcode `0.001` as a universal XAU tick size.

## Code checkpoint

A small generic helper is added at:

- `src/nexus_xau/data/price_grid.py`

It deliberately supports only:

- exact price -> integer tick index;
- integer tick -> exact Decimal price;
- same-tick literal equality;
- OHLC bar contains/touches literal price level.

It deliberately does **not** contain:

- fuzzy tolerance;
- course-point conversion;
- Bid/Ask execution logic;
- spread/slippage model;
- trade fill logic.

Tests:

- `tests/test_price_grid.py`

## Decision

```text
LITERAL EQUALITY NORMALIZATION:
  CLOSED for a runtime broker tick grid

LITERAL BID-CHART CONTACT AT BAR RESOLUTION:
  CLOSED as High-Low inclusion on normalized tick grid

POSITIVE FUZZY TOLERANCE:
  NOT SOURCE BACKED / DO NOT INVENT

GENERIC ZONE / SAME-STRUCTURE TOLERANCE:
  STILL OPEN

ACTUAL ORDER FILL / BID-ASK EXECUTION:
  STILL OPEN
```

This closes the mechanical price-grid ambiguity for literal equality/contact without pretending that broker precision supplies missing trading geometry.

## Next decision-critical step

Use this contract to audit which remaining RQ-009 blockers are genuinely source-geometry problems versus already-solvable price-grid normalization problems. Then prioritize the largest remaining deterministic blocker, currently Sideway/structural-zone geometry and unresolved Body Collection candidate/reference selection, before any final performance proof.
