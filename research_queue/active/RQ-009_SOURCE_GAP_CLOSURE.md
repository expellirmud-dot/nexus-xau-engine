# RQ-009 — Source Gap Closure from Current Five-Video Batch

Status: ACTIVE

## Objective

Use the five currently available local instructor video+transcript pairs to close the remaining source gaps that block a defensible first trade-family proof. Prefer source/visual closure over computation. Do not invent thresholds from outcomes.

## Primary target

Make at least one trade family — preferably `SIG_ENTRY` — sufficiently deterministic for a future bounded Win/Loss proof without silently filling unknown rules.

## Priority inside this single worksheet

1. PAT2/PAT3 `>50%` measurement basis
   - real body vs full High-Low vs another visual/Fibonacci construction;
   - combined-candle arithmetic for PAT3 where applicable;
   - equality/tolerance only if explicitly evidenced.

2. Location and post-SIG destruction geometry
   - how PA interacts with support/resistance/frame;
   - wick/body/close relation;
   - exact visual meaning of `กวน/ทำลาย` the PA/post-SIG reference;
   - do not universalize example-specific point distances.

3. SIG_ENTRY entry / SL / invalidation
   - distinguish run anchor from entry price and from SL reference;
   - determine whether a source-backed stop geometry can be frozen for at least one setup family;
   - preserve setup-specific examples instead of creating one universal SL.

4. Sideway exact frame/completion/exit geometry
   - upper/lower construction;
   - `กรอบ SW ครบ`;
   - transition/exit to new SIG;
   - false-brake/overlap/jerid handling where source supports it.

5. M1/M5 qualitative-state numeric/measurable details
   - large-force / weakening / rejection;
   - frame-standing body/wick relation;
   - only needed for a `FRAME_BRAKE_ENTRY` proof, so it is lower priority than closing `SIG_ENTRY`.

## Evidence method

For each subquestion:

```text
transcript keyword/timestamp map
-> synchronized visual evidence window
-> original audio cross-check only when ASR ambiguity is material
-> source-backed closure or explicit UNKNOWN
-> targeted computation only if more than one source-compatible measurable representation remains
```

Use the existing local tooling registered in `TOOLS.md`:

- `D:/tools/nexus-video-evidence`
- `D:/tools/ie-coder-bridge-image-patch`
- local source vault `D:/nexus-xau-engine-repo/youtube` (gitignored)

## Current source batch

- `vcdN51_OrPE` — system summary
- `1E_PYPor1qQ` — PA/PAT lesson
- `ESHDuiVPJow` — Trend / Frame / SIG
- `UV5NijhjfJ8` — EP.4 M5 brake
- `16KoS7d-koI` — EP.6 M1/M5 entry

## Guardrails

- visual meaning outranks analyst backtest convenience;
- raw YouTube transcript remains preserved;
- ASR-sensitive numbers/terms must be cross-checked when material;
- historical outcome cannot promote a representation into a source rule;
- unresolved items are recorded as `UNKNOWN` / `PARAMETERIZED`, not guessed;
- media stays local and ignored by Git.

## Done when

Either:

1. at least one complete source-backed trade family has deterministic setup -> entry -> SL/invalidation -> exit semantics suitable for a bounded proof, with any remaining non-material execution assumptions explicitly stated; or
2. the current five-video batch has been exhausted for the named blockers and every unresolved item is mapped to the specific missing source needed next.
