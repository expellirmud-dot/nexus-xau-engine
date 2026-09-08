# RQ-009 — Sideway Exit / False-Break Source Boundary

Status: `EXIT_CONFIRMATION_SHELL_SOURCE_BACKED / EXACT_FALSE_BREAK_AND_FRAME_COMPLETE_GEOMETRY_SOURCE_INCOMPLETE`

Date: 2026-09-09 Asia/Bangkok

## Question

Can the current source batch distinguish a Sideway **internal excursion / false-looking break** from a source-supported Sideway exit far enough to build a safe state machine, without inventing an exact autonomous frame detector or outcome-fitted breakout threshold?

## Sources reviewed

Primary current-batch sources:

- `vcdN51_OrPE` — system summary / lifecycle and frame behavior.
- `ESHDuiVPJow` — EP.2 Trend > Frame > SIG.
- `UV5NijhjfJ8` — EP.4 M5 brake / Sideway and retest behavior.
- `16KoS7d-koI` — EP.6 M1/M5 entry context.
- `1E_PYPor1qQ` — body-primary Sideway frame preference.

Prior checkpoints:

- `docs/RQ005_SIDEWAY_LIFECYCLE_SOURCE_CLOSURE_2026-09-08.md`
- `docs/RQ009_SIDEWAY_FRAME_SOURCE_METHOD_AUDIT_2026-09-09.md`
- `docs/RQ009_EP5_BODY_COLLECTION_SIDEWAY_ROUTING_RECONCILIATION_2026-09-09.md`

Targeted transcript scan remains local/gitignored:

- `youtube/_evidence/rq009_sideway_transition_scan_2026-09-09.txt`

No historical outcome performance was used to choose an exit threshold.

## 1. Internal SIG / PA does not automatically end Sideway

The source repeatedly teaches that Sideway can contain PA/SIG on both sides (`SIG ชน SIG`) and that traders should not identify the carrying SIG in advance.

`vcdN51_OrPE` around `1:31:30-1:34:21` states in substance:

```text
Sideway continues while the market is still choosing a direction.
Wait until a real SIG carries price out.
We do not know beforehand which SIG will be the one that exits the frame.
After price actually breaks out, we can identify the SIG that carried the exit.
```

Safe state rule:

```text
INTERNAL_SIG != SIDEWAY_EXIT
```

and:

```text
CARRYING_SIG_ID is retrospective / evidence-after-exit,
not a look-ahead label assigned to an internal SIG.
```

## 2. Wick-only excursion is not sufficient for a clean confirmed exit in the demonstrated higher-TF example

EP.2 around `1:32:42-1:34:09` reviews a multi-month Week Sideway frame. The instructor describes an apparent excursion where the candle went out **only by wick** while the body did not go with it; after the week closed, price was pulled back into the old frame area.

Direct teaching substance:

```text
went out by wick only;
the body did not go with it;
after the week ended, price was pulled back into the old area/frame.
```

This is strong source evidence that:

```text
wick excursion outside a Sideway frame
!= automatically confirmed directional exit
```

It also agrees with the separately reviewed body-primary / body-core Sideway framing evidence.

This does **not** establish a universal formula such as `close > frame + N points`.

## 3. Frame standing/failure is body-sensitive but not yet a universal numeric predicate

`vcdN51_OrPE` around `58:55-59:10` directly contrasts:

```text
stand at the frame
vs
cannot stand at the frame -> frame is broken
```

Other reviewed sources repeatedly use candle body relation as the primary standing evidence, while wick probes can occur.

Current source boundary:

```text
body/standing relation is material to exit confirmation
```

but the batch still does not uniquely define:

- exact close-vs-body formula;
- minimum body fraction outside;
- number of completed candles outside;
- one universal timeframe-independent standing count;
- one numeric distance beyond the boundary.

Counts such as H1 `2-4` or M1/M5 `4-10` occur in teaching contexts but are not established as a universal Sideway-exit gate for every timeframe/setup.

## 4. Preferred breakout/retest handoff is source-backed

EP.2 around `1:51:08-1:51:35` teaches the post-break role-flip workflow:

```text
if price breaks upward out of the Sideway frame:
    wait for pullback/retest;
    old resistance may become support;
    then consider BUY.

if price breaks downward out of the Sideway frame:
    wait for pullback/retest;
    old support may become resistance;
    then consider SELL.
```

EP.4 independently reinforces the break -> move away -> return/retest -> old support/resistance role-change logic.

This closes a **post-exit confirmation/entry route**, not the autonomous detection of the original frame bounds.

## 5. Sideway exit shell

For an already externally/source-family identified Sideway frame:

```text
SIDEWAY_ACTIVE
-> INTERNAL_PA_SIG              # may remain inside; not exit
-> EXIT_CANDIDATE               # price probes / attempts boundary
-> BODY_STANDING_EVIDENCE       # source says body/standing matters
-> ACTUAL_FRAME_ESCAPE          # carrying SIG becomes identifiable only now/afterward
-> OPTIONAL_PREFERRED_RETEST
-> OLD_BOUNDARY_ROLE_FLIP
-> SIDEWAY_EXIT_CONFIRMED_ROUTE
```

A wick-only excursion that returns inside remains:

```text
EXIT_CANDIDATE / INSUFFICIENT_EXIT_EVIDENCE
```

not automatically `SIDEWAY_EXITED`.

## 6. What is still source-incomplete

The current batch does **not** provide one universal deterministic formula for:

```text
sideway_frame_complete()
sideway_breakout_confirmed()
sideway_false_break()
```

because these remain unresolved:

- exact frame upper/lower construction and candle-selection start/end;
- routing between BODY_PRIMARY and BODY_CORE+WICK_LAYER source methods;
- exact body/close geometry required outside the frame;
- exact number of confirming candles;
- exact retest contact/zone tolerance;
- simultaneous/multiple-frame priority across timeframes;
- exact handling when breakout and retest-like events occur inside the same OHLC bar.

The broker tick-grid checkpoint closes only **literal known-level contact/equality**. It does not supply the missing structural zone tolerance.

## 7. Important non-inferences

Do not encode from this checkpoint:

```text
one wick outside = breakout
one close outside = universal breakout
2 candles outside = universal breakout
4-10 candles = universal Sideway exit
N broker ticks beyond frame = valid breakout
retest must touch the exact same tick
```

None of those universal rules is established by the current source batch.

## 8. Decision

```text
SIDEWAY INTERNAL SIG != EXIT:
  SOURCE BACKED

CARRYING SIG IDENTIFIED ONLY AFTER ACTUAL ESCAPE:
  SOURCE BACKED

WICK-ONLY OUTSIDE + BODY NOT OUT + RETURN INSIDE:
  SOURCE-SHOWN INSUFFICIENT CLEAN EXIT EVIDENCE

BREAK -> RETEST -> ROLE FLIP ROUTE:
  SOURCE BACKED

EXACT UNIVERSAL FRAME-COMPLETE / FALSE-BREAK / BREAKOUT OHLC PREDICATE:
  SOURCE INCOMPLETE IN CURRENT BATCH
```

## 9. Engine permission

Safe implementation is limited to a state shell around **externally/source-family identified frame boundaries**. Do not make Sideway fully autonomous yet.

The engine may record:

- frame method/provenance;
- internal SIGs without declaring exit;
- wick-only probe / returned-inside evidence;
- body-standing/escape evidence as externally/source-labeled features;
- breakout/retest/role-flip state.

It must fail closed or require source-family/human confirmation for exact frame-complete and breakout predicates.

## 10. Next decision-critical blocker

With literal broker-grid equality/contact and the Sideway exit shell separated from unresolved structural geometry, the next high-value blocker is Body Collection candidate/reference selection for unseen configurations. The current source has already shown a two-reference method and one cross-TF alignment topology, but not a universal winner/reducer across all valid candidate sets.
