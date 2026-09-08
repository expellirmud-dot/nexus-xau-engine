# RQ-010 — SIG Mode-2 Signal/Run V0 Implementation

Date: 2026-09-09 Asia/Bangkok
Status: `FROZEN_FULL_VALIDATION_PASS / HOLDOUT_UNOPENED`

## Objective

Implement the minimal deterministic scope selected by the RQ-009 evidence-boundary audit:

```text
SIG_MODE2_EXTERNALLY_LABELED_SIGNAL_RUN_V0
```

This module measures a pre-outcome-labeled Mode-2 SIG lifecycle. It does **not** simulate a broker trade and must not be reported as trade/system Win rate.

## Implementation

Primary module:

- `src/nexus_xau/research/sig_mode2_signal_run_v0.py`

Tests:

- `tests/test_sig_mode2_signal_run_v0.py`
- `tests/test_price_grid.py`

Existing deterministic dependency:

- `src/nexus_xau/data/price_grid.py`

Schema version:

```text
SIG_MODE2_SIGNAL_RUN_V0.1
```

## Manifest contract

The manifest contains one runtime price-grid declaration plus one or more externally labeled signal events.

```json
{
  "schema_version": "SIG_MODE2_SIGNAL_RUN_V0.1",
  "dataset_id": "<locked dataset identifier>",
  "tick_size": "<runtime-verified trade tick size>",
  "events": [
    {
      "signal_id": "<unique id>",
      "side": "BUY | SELL",
      "signal_tf": "H1 | H4",
      "pa_kind_or_source_label": "<pre-outcome source/label id>",
      "pa_confirmed_at": "<timezone-aware instant>",
      "location_label": "VALID_SUPPORT | VALID_RESISTANCE",
      "location_label_provenance": "<provenance>",
      "post_sig_closed_at": "<timezone-aware knowledge instant>",
      "point_check_price": "<exact broker-grid price>",
      "point_check_price_provenance": "<provenance>",
      "run_anchor_price": "<exact broker-grid price>",
      "run_target_price": "<target price frozen before outcome>",
      "horizon_end": "<timezone-aware frozen horizon>",
      "parent_context_tf": "<context TF>",
      "context_tags": ["<pre-outcome context tags>"],
      "source_or_label_provenance": "<provenance>",
      "label_known_before_outcome": true
    }
  ]
}
```

The loader fails closed when:

- `signal_id` is missing/duplicated;
- timeframe is outside H1/H4 V0 scope;
- BUY is not labeled at valid support or SELL is not labeled at valid resistance;
- timestamps are not timezone-aware;
- PA confirmation occurs after post-SIG knowledge time;
- label provenance is missing;
- `label_known_before_outcome` is not the literal boolean `true`;
- point-check/anchor/target are not on the manifest tick grid;
- target direction is inconsistent with BUY/SELL;
- Mode-2 point-check and run anchor are not the same normalized post-SIG reference.

## Critical timestamp convention

`post_sig_closed_at` is the **instant at which the completed post-SIG candle is knowable**.

It is not the candle's opening timestamp.

For M1 bar data whose index represents the bar-open instant, replay includes only bars satisfying:

```text
M1_bar_open_time >= post_sig_closed_at
```

Example:

```text
H1 post-SIG candle spans 09:00 -> 10:00
post_sig_closed_at = 10:00
first eligible M1 outcome bar = M1 bar opening at 10:00
```

The H1 candle's internal 09:00-09:59 M1 bars are prohibited from the Mode-2 forward outcome because the final point-check was not yet knowable.

This convention is required to avoid look-ahead.

## Price and unit convention

V0 operates on exact **broker ticks**, not course/project points.

```text
tick index = exact observed price / runtime tick_size
```

Reasons:

1. literal point-check contact is already closed on the broker grid;
2. project/course point and broker point are separate concepts;
3. V0 accepts a frozen `run_target_price`, so it does not need to invent a project-point conversion.

`mfe_ticks` and `mae_ticks` are therefore broker-grid distances only. They must not be relabeled as project/course points.

## Point-check destruction

For a known normalized point-check level:

```text
low_tick <= point_check_tick <= high_tick
```

counts as contact.

Boundary equality counts. A one-tick near miss does not.

This is chart-side Bid OHLC event detection, not broker order fill.

## Target detection

The target price is supplied by the manifest and must be frozen before outcome inspection.

BUY:

```text
high_tick >= run_target_tick
```

SELL:

```text
low_tick <= run_target_tick
```

V0 deliberately does not construct the target from an unresolved project-point conversion inside the replay module.

## Terminal result classes

```text
TARGET_FIRST
POINT_CHECK_FIRST
AMBIGUOUS_SAME_BAR
HORIZON_EXHAUSTED
```

If target and point-check occur inside the same available M1 bar, V0 records:

```text
AMBIGUOUS_SAME_BAR
```

because OHLC cannot establish intrabar order.

It never converts such a case into favorable/adverse first-hit by assumption.

## MFE / MAE

MFE and MAE are measured from the normalized Mode-2 run anchor and only over bars observed before the terminal result.

They are research path measurements, not realized trade P&L.

## Explicit exclusions

V0 contains no:

- autonomous PAT detector;
- autonomous support/resistance/location detector;
- Body Collection candidate winner;
- Sideway detector;
- Mode-1 intrabar trigger;
- M5 Brake entry;
- Por Chon entry;
- broker entry/fill price;
- Bid/Ask order execution;
- spread/slippage/commission;
- lot sizing;
- realized P&L;
- profit factor;
- drawdown;
- system/trade Win rate.

Those exclusions are deliberate evidence-boundary controls.

## Labeling rule

Every V0 event must be created and locked before viewing its forward outcome.

`label_known_before_outcome=true` is not sufficient provenance by itself; the manifest must also retain source/label references so an audit can verify when and why the label was created.

If a multi-family conflict was unresolved at label time and could materially change the SIG interpretation, the event should be excluded/flagged upstream rather than forcing a winner in V0.

## Targeted validation

Targeted validation after implementation/fixes:

```text
python -m pytest tests/test_sig_mode2_signal_run_v0.py tests/test_price_grid.py -q
=> 16 passed

python -m ruff check src/nexus_xau/research/sig_mode2_signal_run_v0.py tests/test_sig_mode2_signal_run_v0.py
=> All checks passed
```

Validated cases include:

- BUY target first;
- exact point-check contact first;
- one-tick near miss survival;
- same-bar ambiguity;
- SELL mirror;
- manifest multi-event replay;
- duplicate ID rejection;
- wrong-location rejection;
- post-outcome/non-boolean label guard;
- timezone guard;
- off-grid failure;
- target-direction guard through replay contract;
- point-check/run-anchor identity requirement.

## Holdout state

```text
PRISTINE V0 HOLDOUT = NOT OPENED
```

No new untouched outcome period is inspected during this implementation checkpoint.

Required order remains:

```text
implementation
-> full validation
-> version/data-contract freeze
-> holdout labeling/reservation protocol
-> lock manifest
-> only then outcome scoring
```

## Current decision

The V0 research engine is implemented at targeted-test level. Final RQ-010 freeze requires the full repository test suite, full Ruff check, research preflight, JSON validation, diff check, and clean Git checkpoint.


## Full-repository validation

The first unscoped pytest attempt reached `133 passed` but produced 9 setup errors because the default Windows pytest temp root under `AppData\Local\Temp` was not accessible. This was an environment/permission failure, not a code assertion failure.

The suite was rerun using a repository-local pytest base temp:

```text
python -m pytest --basetemp=.pytest-tmp-rq010-final
=> 142 passed, 116 warnings

python -m ruff check src tests
=> All checks passed
```

The 116 warnings are existing pandas/NumPy deprecation warnings and are not RQ-010 test failures.

## Freeze decision

RQ-010 implementation criteria are satisfied:

- typed V0 manifest/event contract implemented;
- H1/H4 scope enforced;
- provenance and pre-outcome labeling guard enforced;
- exact broker-grid contact and one-tick near-miss behavior tested;
- target-first / point-check-first / same-bar ambiguity / horizon-exhausted tested;
- MFE/MAE recorded in broker ticks only;
- full repository tests pass;
- full Ruff pass;
- no pristine holdout was opened or scored.

Result:

```text
SIG_MODE2_SIGNAL_RUN_V0.1 = IMPLEMENTATION_FROZEN
PRISTINE_HOLDOUT = UNOPENED
TRADE/SYSTEM WIN RATE = NOT CLAIMABLE
```

Next methodology checkpoint: `RQ-011 — Pristine V0 Holdout Labeling and Reservation Protocol`.
