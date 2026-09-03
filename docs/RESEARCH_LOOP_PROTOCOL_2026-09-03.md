# NEXUS XAU Research Loop Protocol — 2026-09-03

Status: ACTIVE OPERATING LOOP

Purpose: allow NEXUS to continue useful research while the project owner is busy and cannot answer frequent questions, without converting uncertainty into invented rules.

## Load order for every loop

Before new work, read in this order:

1. `docs/NEXUS_PROJECT_MAINTENANCE_POLICY.md`
2. `docs/CURRENT_RESEARCH_STATE.json`
3. `docs/CANONICAL_CLAIM_REGISTER_2026-09-03.json`
4. the latest checkpoint relevant to the selected puzzle
5. original/closest available source evidence for any claim being changed

Historical files are evidence/history, not automatically the current project position.

## Atomic loop

Each research loop must complete one bounded unit:

```text
LOAD STATE
-> SELECT highest-value unresolved claim
-> RECOVER / REVIEW evidence
-> SPLIT source fact from interpretation
-> CHECK provenance / ASR / STT risk
-> COMPARE against canonical claim register
-> RESOLVE if evidence is sufficient
   OR parameterize/quarantine if insufficient
-> IMPLEMENT only the portion supported by evidence
-> TEST / LINT / VALIDATE
-> UPDATE canonical register + current state + checkpoint
-> COMMIT / PUSH
-> SELECT next unresolved claim
```

## When NEXUS may continue without asking

Continue autonomously when the next step is non-destructive and does not require guessing a material rule, including:

- searching existing project evidence;
- reviewing timestamped transcript material already available;
- comparing direct evidence with historical summaries;
- identifying contradictions and marking old claims superseded;
- creating parameterized research variants without selecting a winner as canonical;
- writing tests for already-supported semantics;
- collecting threshold-free measurements/features;
- performing negative controls, replay scaffolding and provenance audits;
- improving documentation, canonical claim indexing and restart-safe checkpoints;
- routine validated commit/push under the maintenance policy.

## Mandatory human-confirmation gate

Stop the affected claim and ask the project owner only when an ambiguity can materially change system behavior and cannot be resolved from available evidence.

Examples:

- STT phrase could mean different technical words;
- ASR may have misheard a number, timeframe, must/only qualifier or proprietary term;
- two credible direct sources materially conflict;
- a missing threshold would require inventing a production value;
- a destructive repository/history action is needed;
- a source-specific discretionary judgment cannot yet be represented as measurable alternatives.

The rest of the loop may continue on independent claims while that one is blocked.

## Evidence-laundering prevention

A claim must not become stronger merely because it was copied into a newer document.

For every material claim record:

```text
claim_id
canonical_statement
status/lifecycle
source_refs
source/capture/extraction chain
risk flags (ASR/STT/etc.)
what is direct vs interpreted
engine permission
supersedes / superseded_by when relevant
```

Rules:

- old direct evidence remains evidence even when its conclusion is superseded;
- superseded conclusions have no active coding authority;
- YouTube Show transcript = attributable timestamped evidence with ASR risk, not manual verbatim transcription;
- user speech may carry STT risk; material ambiguity requires confirmation;
- analyst summaries do not inherit primary status from their inputs;
- outcome/backtest performance never upgrades source provenance;
- unknown means unknown; do not choose a threshold because it backtests better.

## Research priority queue

Current high-value order unless new evidence changes it:

1. **Por Chon 19:00–19:00** — timezone/day-window semantics and H4 selection.
2. **PAT2/PAT3 geometry** — exact 50% reference basis, equality/tolerance, small-body/equal-wick thresholds.
3. **Location interaction** — what counts as PAT standing/touching support/resistance by source family.
4. **Post-SIG invalidation** — complete measurable `กวน/ทำลาย PA` predicate beyond safe partial rejection.
5. **M5 brake/frame-standing** — turn qualitative force/standing language into threshold-free features, then labeled variants.
6. **Sideway construction/completion** — explicit frame boundaries and exit/new-SIG transition.
7. **Entry/SL/invalidation** — only after setup/state semantics are sufficiently frozen.
8. **Full-system Win/Loss proof** — only after the above are source-backed and frozen OOS.

Independent work may be reordered to exploit available evidence, but do not skip unresolved upstream rules by inventing downstream assumptions.

## Loop output discipline

Do not interrupt the user for routine progress. Surface a message when at least one of these occurs:

- a meaningful checkpoint is closed;
- a prior canonical belief changes;
- a material contradiction is discovered;
- a human confirmation is genuinely required;
- a repository/test blocker prevents further progress;
- a result materially changes what the project should investigate next.

Routine searches with no new conclusion should be checkpointed locally when useful but need not generate repeated user messages.

## Success definition

The loop is not optimized for number of rules coded or backtest win rate. It is optimized for reducing unresolved decision-critical ambiguity while preserving evidence provenance.

A puzzle is considered closed only when:

```text
source meaning is sufficiently established
+ interpretation is explicit
+ measurable representation exists
+ positive/negative examples or tests exist where applicable
+ no known stronger contradictory evidence is unresolved
+ canonical claim register is updated
```
