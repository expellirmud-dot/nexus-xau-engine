# State Response Matrix — 2026-09-03

Status: EVIDENCE-BASED OPERATING MATRIX / NOT LIVE-TRADING AUTOMATION

Purpose: preserve how the research engine should react to known graph/setup states while separating confirmed response semantics from unresolved numeric triggers.

## Core principle

The engine should not ask only `Buy or Sell?`.

It should first ask:

```text
What state is the setup in?
What evidence is confirmed?
What object is still unresolved?
What action is allowed at this state?
```

## Matrix

| State / condition | Current evidence-backed response | Status | Still unresolved |
|---|---|---|---|
| Candle still open | WAIT. Do not finalize PAT/SIG from unfinished candle. | CONFIRMED | intrabar monitoring can exist separately, but not final classification |
| PAT shape appears but location unknown | WAIT / HUMAN_CONFIRM. Do not promote to valid PA. | CONFIRMED semantics | exact S/R source and touch rule |
| BUY PAT at resistance / SELL PAT at support | REJECT as valid directional PA. | CONFIRMED | higher-TF context can explain why wrong-location shapes fail, but numeric priority matrix is open |
| Correct-side S/R family identified but touch/proximity unresolved | WAIT / PARAMETERIZED. Preserve family and distance; do not invent universal tolerance. | CONFIRMED architecture | family-specific touch/penetration/body/close tolerance |
| PA valid but post-SIG reference candle not complete | WAIT. SIG/run anchor is not final yet. | SUPPORTED | exact live timing before reference candle close |
| Candidate post-SIG wick/reference does not disturb PA | Can remain candidate SIG / anchor object. | SUPPORTED concept | exact numeric `disturb/exceed PA` predicate |
| Post-SIG wick/reference extends beyond / disturbs PA | INVALIDATE original SIG interpretation; reassess Sideway/new PA rather than keep old anchor alive. | CONFIRMED topology/state semantics | exact OHLC tolerance for destruction |
| Invalid SIG followed by new PA | REPLACE / RE-ANCHOR. New PA/SIG must own the new anchor if valid. | CONFIRMED example/state behavior | exact replacement sequencing for all PAT families |
| SIG active | Count run from valid post-SIG anchor according to timeframe. | CONFIRMED high-level | exact live entry timing is separate from run counting |
| H1 run active | Source run reference = 1,000 project-reference points. | CONFIRMED project evidence | project-point vs broker-point normalization must remain explicit |
| H4 run active | First/full run reference = 1,500 project-reference points; extension references exist toward 3,000. | CONFIRMED project evidence | exact TP2 execution/management mechanics |
| Nominal TP/run complete | DO NOT automatically countertrade. Mark TP_COMPLETE and check for Over-round / reversal evidence. | CONFIRMED | exact reversal trigger after TP |
| Price continues beyond nominal run | Mark OVERRUN; do not assume immediate reversal. | CONFIRMED high-level | exact extreme finalization |
| OVERRUN + opposite PA drives retrace | Candidate HALF_RETRACE. Reference starts from parent post-SIG anchor to extreme; midpoint is reference. | SUPPORTED / PARTIAL | exact opposite-PA detector, extreme freeze, entry/invalidation |
| OVERRUN without opposite PA | Candidate SWING_RETRACE. | SUPPORTED / PARTIAL | exact qualifying swing-start candle and extreme finalization |
| Body-collection retrace toward historical zone | Search same-TF structure first; demonstrated H4 workflow can fall back H4 -> H1 -> M30. | CONFIRMED workflow | exact `ซอก+ไส้+คู่` OHLC geometry |
| Price reaches body-collection zone but lower-TF PA absent | WAIT under demonstrated body-collection conditions. | CONFIRMED example/workflow | advanced exceptions, if any |
| Body-collection setup while lower TF is Sideway | WAIT / do not blindly apply body-collection entry. Sideway is separate setup family. | CONFIRMED | exact Sideway frame-complete and entry rules |
| Sideway suspected after invalid post-SIG / disturbed PA | Switch to SIDEWAY/REEVALUATE candidate state rather than forcing old SIG continuation. | CONFIRMED high-level | deterministic Sideway start/completion detector |
| Sideway frame complete | Separate Sideway setup may become actionable only under its own PA/SIG conditions. | CONFIRMED high-level | exact two-side confirmation and break rules |
| M5/entry confirmation unresolved | WAIT. Do not convert frame proximity alone into automatic order. | CONFIRMED safety/engineering decision | exact brake/break geometry, entry candle, market/pending condition |
| Event outcome ambiguous within one M1 bar | Mark AMBIGUOUS; require tick/lower-level data to resolve. | RESEARCH-PROTOCOL CONFIRMED | tick dataset availability |

## State outcome metrics to accumulate

Once each state transition is deterministic or externally labeled before outcome review, record:

```text
state_entered_at
state_exited_at
parent_setup_id
source timeframe
location family
PAT/SIG family
anchor price
MFE
MAE
time in state
next state
invalidation reason
run target reached
trade entry/exit only if actual entry rule is active
```

This allows the project to answer questions beyond simple Win rate:

- Which states fail most often?
- How often does invalid post-SIG transition to Sideway?
- How often does TP_COMPLETE become OVERRUN instead of reversal?
- How large is adverse movement before successful run completion?
- Does H1/H4 context materially change lower-TF setup behavior?
- Which setup family produces the largest losing streak once actual trade rules are frozen?

## Handling principle by evidence status

```text
CONFIRMED rule        -> engine may enforce
PARAMETERIZED rule    -> research variant only, always tagged
HUMAN_CONFIRM         -> manual label required before canonical backtest
NOT_IMPLEMENTED       -> cannot promote setup to canonical trade
```

## What is intentionally NOT added

This matrix does not invent:

- universal SL points;
- fixed RR;
- universal 200/300-point loss threshold;
- generic trend indicator states;
- generic 2–3 swing Sideway rule;
- automatic Buy/Sell execution.

Those would change the system being researched.

## Next engineering use

The replay engine should eventually persist `state_before`, `event`, `state_after`, `reason`, and `evidence_status` for every transition. Win/Loss and risk statistics can then be conditioned on state rather than mixing Sideway, fresh SIG, Over-round, retrace, and replacement setups into one misleading average.
