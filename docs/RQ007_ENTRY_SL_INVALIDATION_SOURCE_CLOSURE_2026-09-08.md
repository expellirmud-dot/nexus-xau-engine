# RQ-007 — Entry, SL, and Invalidation Source Closure — 2026-09-08

Status: CLOSED / `SOURCE_BACKED_ENTRY_FAMILIES_SL_GEOMETRY_INCOMPLETE`

## Question

Are entry, stop-loss, and invalidation semantics sufficiently source-backed and measurable to define one complete trade construction suitable for full-system Win/Loss proof?

## Evidence basis

Primary project evidence reviewed:

- `docs/M5_BRAKE_TRANSCRIPT_FORENSICS_2026-09-01.md`
- `docs/PA_PAT_TRANSCRIPT_FORENSICS_2026-09-01.md`
- `docs/DIRECT_RELATIVE_CHAT_EVIDENCE_2026-09-01.md`
- `docs/PRIMARY_IMAGE_EVIDENCE_2026-09-01.md`
- RQ-001 through RQ-006 source closures

## Entry families must remain separate

Current source evidence does not support one universal entry algorithm. At minimum it requires separate accounting for:

```text
SIG_ENTRY
FRAME_BRAKE_ENTRY
```

### SIG_ENTRY

Source-backed components:

- valid PA/SIG context requires correct location and a valid post-SIG reference;
- post-SIG reference mapping is PAT1->candle #2, PAT2->#3, PAT3->#4;
- if the directional wick is absent, BUY uses the Low and SELL uses the High as the reference extreme;
- post-SIG reference is the run-count anchor;
- direct relative evidence for a PAT2 BUY example also uses that reference as a structural/check/SL reference;
- timeframe run/TP is measured from the post-SIG reference;
- a post-SIG reference that disturbs/exceeds the PA invalidates that identified SIG instance;
- RQ-001 closes lifecycle at the SIG-instance level rather than as a global reset.

Still incomplete for a universal SIG trade definition:

- exact PAT1 numeric detector;
- exact PAT2/PAT3 50% denominator and remaining tolerances;
- exact location touch/penetration/tolerance by source family;
- exact numeric predicate for `กวน/ทำลาย PA`;
- universal SL distance/buffer from the post-SIG reference;
- complete multi-timeframe conflict resolution.

### FRAME_BRAKE_ENTRY

Source-backed components:

```text
prepared zone
-> brake state development
-> optional first/scout reaction
-> move away / structural retest
-> PA / frame-standing / structure confirmation as applicable
-> preferred Entry #2 / retest
```

Important accounting fact:

```text
FRAME_BRAKE_ENTRY has no native SIG run anchor at entry.
```

The teaching discusses practical nearby-frame objectives and later conversion to SIG-run management if a valid SIG subsequently develops.

Still incomplete:

- exact quantitative force/rejection thresholds;
- exact frame-standing tolerance and all-vs-majority logic;
- exact source-family zone bounds in several contexts;
- universal stop placement;
- exact objective/exit rule for every frame-brake setup variant.

## SL evidence — context-specific, not universal

Source material contains several stop examples:

- M1 refinement examples around 50–150 project points;
- examples around 50/100 points emphasizing small accepted loss;
- scouting example around 300 points;
- frame-based examples around 200–300 points behind/around a frame;
- another frame example around 300 points;
- a PAT3 teaching image shows a 300-point SL below the post-SIG line;
- direct relative Por Chon over-round SELL example places SL below the ATH line, but exact buffer and universality remain unresolved.

These values belong to different setup/timeframe/context examples.

Therefore:

```text
NO UNIVERSAL 50 / 100 / 150 / 200 / 300 POINT SL RULE IS ESTABLISHED.
```

Do not choose one from historical performance.

## Invalidation semantics

Source-backed invalidation/state facts include:

- wrong-location PA is rejected;
- unfinished candles do not confirm PA/SIG;
- a post-SIG reference that disturbs/exceeds its PA invalidates that SIG instance;
- M5 first brake can fail/overlap and requires re-evaluation rather than automatic entry;
- a counter-trend setup is not justified merely because nominal TP completed; over-round is possible;
- Sideway internal SIG does not automatically imply normal full run space;
- Por Chon wick penetration alone does not prove frame failure; body relation is primary.

However, several invalidations remain non-deterministic numerically:

- exact post-SIG destruction geometry/tolerance;
- exact frame-standing/body-break geometry;
- exact Sideway frame exit/false-break geometry;
- exact PAT-to-location tolerance;
- exact multi-timeframe thesis-break rule.

## Can one complete system trade be frozen now?

No.

The project can already represent and replay **feature/state candidates** for multiple entry families, but it cannot yet define one source-faithful universal tuple:

```text
setup -> exact entry price/time -> exact SL -> exact invalidation -> exact TP/exit
```

for the full system without inserting unresolved assumptions.

A backtest that silently fills those fields would measure an analyst-created strategy, not the demonstrated system.

## Safe outcome research boundary

Allowed now:

- labeled case replay for a specifically documented setup example;
- feature/state agreement testing;
- separate research variants with explicit parameter/provenance labels;
- component relationship studies that do not claim system Win/Loss.

Not allowed yet:

- one blended full-system win rate;
- selecting universal SL/invalidation thresholds from best historical outcomes;
- merging SIG_ENTRY and FRAME_BRAKE_ENTRY into one trade family;
- treating example-specific 200/300-point values as canonical.

## Closure decision

```text
SOURCE_BACKED_ENTRY_FAMILIES_SL_GEOMETRY_INCOMPLETE
```

Entry families and many structural invalidation semantics are source-backed, but stop-loss and several exact invalidation/entry geometries remain incomplete. A full-system trade outcome is therefore not yet source-faithfully measurable.

## Consequence for RQ-008

RQ-008 may be activated only to make the final readiness decision. It must **not** run a full-system Win/Loss backtest unless all required upstream trade-construction fields are deterministically frozen without invented assumptions.
