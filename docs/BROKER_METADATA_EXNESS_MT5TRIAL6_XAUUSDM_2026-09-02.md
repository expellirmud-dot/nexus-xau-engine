# Broker Metadata Evidence — Exness-MT5Trial6 / XAUUSDm

Date captured: 2026-09-02
Source class: USER-DIRECT RUNTIME OUTPUT + MT5 SPECIFICATION SCREENSHOT
Environment: Exness demo account, server `Exness-MT5Trial6`
Symbol: `XAUUSDm`

This is broker/environment-specific metadata. It must not be generalized to another Exness server, another account type, or production `XAUUSD` without runtime verification.

## Confirmed runtime values

Python `MetaTrader5.symbol_info("XAUUSDm")` returned:

- `name = XAUUSDm`
- `description = Gold vs US Dollar`
- `path = Standard\\Forex\\XAUUSDm`
- `digits = 3`
- `point = 0.001`
- `trade_tick_size = 0.001`
- `trade_tick_value = 0.1`
- `trade_tick_value_profit = 0.1`
- `trade_tick_value_loss = 0.1`
- `trade_contract_size = 100.0`
- `volume_min = 0.01`
- `volume_max = 200.0`
- `volume_step = 0.01`
- `spread_float = True`
- `trade_stops_level = 0`
- `trade_freeze_level = 0`
- `currency_base = XAU`
- `currency_profit = USD`
- `currency_margin = XAU`
- `chart_mode = Bid price` (also visible in MT5 Specification)
- `trade_mode = full access`
- `execution = market` (visible in MT5 Specification)

At the captured runtime instant:

- bid = `4373.383`
- ask = `4373.643`
- reported spread field = `260` broker points

The instantaneous bid/ask difference was therefore `0.260` USD/oz. This is a single runtime observation and must not be used as a representative or fixed spread assumption.

## First real M1 export

The local research machine successfully exported:

- requested UTC range: `2026-08-24T00:00:00+00:00` to `2026-08-29T00:00:00+00:00`
- symbol: `XAUUSDm`
- rows: `6,770` M1 bars
- local raw file: `data/raw/XAUUSDm_M1_MT5_2026-08-24_2026-08-28.csv`
- local metadata file: `data/raw/XAUUSDm_M1_MT5_2026-08-24_2026-08-28.csv.meta.json`

Raw files remain local and gitignored.

## Point-unit warning

The teaching/project run distances use a system/course point convention that must not be silently equated to MT5 `symbol_info.point`.

For this symbol:

```text
BROKER_POINT = 0.001 price units
```

Project/course statements such as `H1 = 1,000 points` require a separately verified `SYSTEM_POINT` convention before implementation. Do not multiply the teaching point count by this broker point without evidence.

## Current engineering consequence

Safe now:

- MT5 IPC access on this machine/environment;
- live symbol/tick metadata inspection;
- M1 historical bar export;
- pipeline/timezone/resample validation.

Not established by this evidence:

- equivalence between `XAUUSDm` and the eventual target live symbol;
- representative spread;
- production execution/slippage quality;
- course/system point conversion;
- final backtest data-source quality (M1 bars are not Bid+Ask tick history).
