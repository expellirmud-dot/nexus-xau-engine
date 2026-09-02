# NEXUS XAU — PC-First / Android-Independent Plan

Date: 2026-09-02
Status: NEW ARCHITECTURE PLAN

This plan preserves the prior cloud/dashboard work but changes the primary execution model for real use.

## 1. Core principle

The notebook/PC is the optional intelligence and automation layer.

Android MT5 must remain independently usable even when the PC is off, disconnected, rebooting, or the NEXUS program is not running.

Therefore:

```text
Android MT5 = independent manual trading client
PC NEXUS XAU = optional analysis / alert / automation layer
```

No Android trading capability may depend on the PC being online.

---

## 2. User experience target

The normal PC user should never need to open CMD or manually run Python.

Target flow:

```text
Turn on notebook
→ double-click NEXUS XAU
→ program checks/launches MT5 Desktop
→ connects to XAUUSD data
→ rebuilds current market context
→ user selects mode
→ engine runs until NEXUS is closed
```

The application should eventually be packaged as a normal Windows executable/installer.

---

## 3. Operating modes

### OFF

- Engine does not evaluate trade decisions.
- MT5 remains available normally.

### ALERT

- Read current XAUUSD market data from MT5 Desktop.
- Evaluate the same NEXUS rule engine used by replay/backtest.
- Produce `BUY / SELL / WAIT / REJECT` candidate decisions as supported by evidence.
- Never place orders.
- Show local PC alert.
- Optionally send a notification to Android while the PC engine is running.

### AUTO

- Uses the same market data and same rule engine as ALERT.
- Adds an execution adapter capable of sending orders through MT5 Desktop.
- AUTO must remain disabled until detector correctness, historical replay/backtest, demo testing, risk controls, and failure handling are validated.
- No unresolved rule may be silently converted into an autonomous trading condition.

Architecture rule:

```text
ALERT and AUTO share one engine.
AUTO = ALERT + explicitly enabled execution layer.
```

---

## 4. Live architecture

Primary live path:

```text
MT5 Desktop / Exness
        ↓
NEXUS Windows App
        ↓
MT5 Data Adapter
        ↓
Timeframe / Context Builder
        ↓
Trading Rule Engine
        ↓
Decision
   ┌────┴───────────────┐
   ↓                    ↓
ALERT                AUTO
   ↓                    ↓
PC notification      MT5 order adapter
   ↓
optional Android push
```

MT5 Desktop is the intended live data and execution environment because it provides a direct integration path unavailable in the same form on MT5 Android.

---

## 5. Android behavior

Android is not an engine dependency.

### PC OFF

```text
Android MT5
→ works normally
→ user may inspect charts
→ user may trade manually
→ no NEXUS analysis/automation/push from the PC
```

### PC ON + NEXUS running

```text
NEXUS detects event
→ optional push channel
→ Android notification
→ user may open MT5 Android
```

Android notification is an enhancement, not a prerequisite for Android MT5.

A failure of PC, NEXUS, local network, cloud notification channel, Supabase, or Vercel must not prevent normal MT5 Android use.

---

## 6. Historical replay / backtest architecture

Backtest does not require MT5 to be live and does not require Vercel or Supabase.

```text
Historical XAUUSD data
→ Historical Data Adapter
→ same Timeframe / Context Builder
→ same Trading Rule Engine
→ Replay / Backtest
→ local results/logs
```

This is the first validation path for strategy logic.

Critical engineering requirement:

```text
Historical replay and live mode must share the same core rule implementation.
```

Only the data source and execution/output adapters should differ.

---

## 7. Local-first storage

The PC application must be able to operate without Supabase/Vercel.

Minimum local storage should cover:

- engine configuration;
- current/rebuilt state where useful;
- signals;
- rejected candidates;
- reasons;
- errors;
- rule version;
- engine version;
- historical replay results;
- order/execution audit when AUTO is eventually enabled.

A lightweight local database such as SQLite is suitable for the first implementation unless testing proves another requirement.

Do not store broker passwords or secrets in source control.

---

## 8. Cloud role after this architecture change

Supabase and Vercel are no longer required for the core trading engine.

They remain optional extensions for:

- remote dashboard;
- centralized history;
- multi-device viewing;
- Android/web notifications or message relay;
- remote engine health/status;
- research result sharing.

Cloud outage must not stop local analysis or MT5 Android manual use.

---

## 9. Engine startup behavior

The engine does not need to have watched the market continuously before startup.

When NEXUS starts it should:

1. connect to MT5 Desktop;
2. verify the intended symbol specification;
3. request current and sufficient recent/higher-timeframe history;
4. rebuild the market context required by current rules;
5. identify the latest relevant states/anchors/frames that can be derived deterministically;
6. mark unresolved context as `NEED_HUMAN_CONFIRM` rather than inventing it;
7. enter live evaluation mode.

Long historical datasets are for research/backtest and for any context that genuinely requires long history; they are not to be recalculated in full on every tick.

---

## 10. Notification behavior

Notification is separate from trading decision logic.

Potential outputs:

```text
PRE-ALERT
CONFIRMED SIGNAL
WAIT / NEED HUMAN CONFIRM
ENGINE ERROR / DATA STALE
AUTO EXECUTION RESULT
```

The notification adapter may later use Android push, web push, or another delivery service. The rule engine must not depend on which notification provider is selected.

---

## 11. Failure and safety model

Fail-safe behavior is mandatory.

Examples:

- MT5 disconnected → no AUTO order.
- stale/insufficient market data → no AUTO order.
- ambiguous rule/context → `NEED_HUMAN_CONFIRM` or `WAIT`.
- engine exception → execution disabled until healthy.
- duplicate signal/event → execution adapter must prevent duplicate order submission.
- PC shutdown → Android MT5 remains unaffected.
- notification failure → must not alter trading decision or corrupt state.

AUTO must default to fail-closed.

---

## 12. Development phases

### Phase 1 — Rule consolidation and replay core

- Freeze current evidence snapshot.
- Implement data models and deterministic utilities.
- Implement historical data adapter.
- Build replay engine.
- Log candidates, rejects, reasons, and outcomes.
- Do not enable live execution.

### Phase 2 — First detector validation

- Implement only rules supported strongly enough to code.
- Keep unresolved thresholds parameterized.
- Compare detector output against labeled examples/manual review.
- Establish first genuine historical statistics; do not call readiness scores a win rate.

### Phase 3 — Windows NEXUS application

- One-click executable UX.
- MT5 detection/launch/connect.
- Local status screen.
- Mode selector `OFF / ALERT / AUTO`, with AUTO locked initially.
- Local log/history.

### Phase 4 — Live ALERT

- Read live XAUUSD from MT5 Desktop.
- Rebuild current context at startup.
- Run engine while NEXUS is open.
- Local alerts.
- No autonomous order placement.

### Phase 5 — Android notification extension

- Add optional remote notification adapter.
- Android remains independent.
- PC-on enables NEXUS notifications; PC-off only removes NEXUS notifications.

### Phase 6 — Demo AUTO

Only after replay/backtest and live ALERT are validated:

- add MT5 execution adapter;
- risk limits;
- duplicate-order protection;
- disconnect/stale-data guards;
- demo account testing;
- detailed audit log.

### Phase 7 — Production decision

Decide whether real-money AUTO is justified from evidence. It is not assumed to be the end state.

---

## 13. Current priority change

Previous priority emphasized Supabase/Vercel dashboard integration before the engine was proven.

New priority:

```text
1. Rule source of truth
2. Historical data + replay/backtest
3. Core engine correctness
4. Windows one-click app
5. Live ALERT through MT5 Desktop
6. Android notification extension
7. AUTO only after validation
8. Cloud dashboard remains optional
```

This prioritizes proving the trading logic before adding infrastructure around it.

---

## 14. Non-negotiable architecture rules

1. Android MT5 must work independently of the PC.
2. PC is optional intelligence/automation, not an Android dependency.
3. One core engine must power backtest, ALERT, and eventual AUTO.
4. No CMD/Python knowledge should be required from the normal end user.
5. Historical replay must happen before claiming win rate or enabling AUTO.
6. Unknown trading rules remain unknown/parameterized; do not guess.
7. Local engine operation must not depend on Supabase/Vercel.
8. Cloud components are extensions, not the source of trading truth.
9. AUTO must fail closed.
10. Existing evidence/history must remain preserved; this plan changes architecture priority, not historical research records.
