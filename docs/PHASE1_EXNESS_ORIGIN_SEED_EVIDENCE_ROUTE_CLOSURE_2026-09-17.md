# Phase 1 Exness Origin-Seed Evidence Route Closure — 2026-09-17

Status: CURRENT-EVIDENCE ROUTES EXHAUSTED / STRUCTURAL BLOCKER PRESERVED / HOLDOUT UNSCORED / ORDER SEND DISABLED

Checkpoint time: `2026-09-17T03:38:11+07:00`

## Question

Does the Project already possess either:

1. same-source Exness history before the current archive boundary; or
2. an independently justified finite historical XAUUSDm anchor-price domain

that can eliminate the surviving unknown-prehistory counterexamples under the frozen literal-contact/no-expiry lifecycle?

## Same-source historical routes

Existing evidence was reused; acquisition work was not restarted.

- Exness-branded archive: earliest observed tick `2015-08-10T00:00:00Z`.
- Current MT5/Python historical tick route: earliest accessible tick `2026-03-12T00:00:00.255Z`.
- Current terminal-visible M1 history is constrained by the terminal `maxbars` window and does not establish pre-2015 same-source history.
- Existing capability audit has not established a separate direct Exness historical endpoint independent of the MT5 terminal.
- Shared `D:\tools` search found no additional Exness-specific historical-data route registered there.

Conclusion for this branch: current proven same-source routes do not extend before the 2015 archive boundary.
## Historical anchor-domain evidence

Repository search found no existing `price_min`, `price_max`, or equivalent hard XAUUSDm price-bound contract.

Existing broker metadata confirms:

- `digits = 3`;
- `point = 0.001`;
- `trade_tick_size = 0.001`.

Those values define price-grid resolution, not a finite historical price domain.

Read-only MT5 runtime probe on this checkpoint returned:

- `session_price_limit_max = 0.0`;
- `session_price_limit_min = 0.0`;
- no `price_max` field;
- no `price_min` field;
- `trade_tick_size = 0.001`.

This runtime observation does not provide a finite upper/lower historical anchor bound. It is also a current runtime observation and is not retroactively generalized to 2015 without evidence.

## Interaction with the forward-closure falsification

The prior frozen proof established that for any finite observed path, hypothetical pre-start BUY/SELL anchors can be constructed outside finite observed extrema and remain `ACTIVE` under literal-contact/no-expiry semantics.

Current evidence supplies neither:

- same-source observations before the archive start; nor
- a finite domain proven to contain every possible active pre-start anchor.

Therefore the counterexample premise remains open and the Project cannot promote seed completeness.
## Classification

- Same-source earlier Exness history: `NOT CURRENTLY AVAILABLE IN PROVEN PROJECT ROUTES`.
- Finite historical anchor domain: `NOT ESTABLISHED`.
- Waiting for more post-2015 forward data: `DOES NOT REDUCE THE STRUCTURAL UNKNOWN IN PRINCIPLE`.
- Canonical initial H4-origin state: `STRUCTURAL UNKNOWN / BLOCKING`.
- Real Exness V2 state: `DATA_EXCLUDED_ORIGIN_HISTORY_UNSEEDED`.

This is a closure of the **current evidence routes**, not a universal claim that no future external evidence can exist.

## What would reopen the blocker

Only new evidence or a separately authorized semantic change can reopen this route, for example:

- verified same-source Exness history before `2015-08-10`;
- a broker/instrument rule proven to bound every possible historical H4 origin anchor to a finite domain relevant to this lifecycle;
- a new source-backed lifecycle rule that changes survival/expiry/contact semantics and is frozen before outcome inspection.

Absent one of those, further forward replay or longer warmup is not a productive way to solve seed completeness.

## Engineering consequence

The Project should stop spending compute on attempts to derive `COMPLETE` from finite post-2015 continuation alone.

Work that does not require canonical real V2 initial state may continue independently. Any component that requires that state must remain fail-closed.

No Win Rate, expectancy, profitability, exact broker-fill, protected holdout score, or automatic order action is authorized by this closure.