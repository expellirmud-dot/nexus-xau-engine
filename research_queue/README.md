# NEXUS XAU Research Queue

Status: ACTIVE OPERATIONAL WORK QUEUE

Purpose: make NEXUS responsible for deciding what must be investigated next, so the project owner does not need to know in advance which video, formula, dataset, or tool is required.

## Core rule

Only one decision-critical research worksheet should be `ACTIVE` at a time unless independent work is explicitly marked as non-blocking infrastructure.

Work moves through:

```text
QUEUED -> ACTIVE -> CLOSED
                 -> BLOCKED
```

When the active worksheet closes:

1. preserve its result and evidence references;
2. re-evaluate whether new evidence changes dependencies or priority;
3. promote the highest-value unblocked queued worksheet;
4. update `QUEUE.json`, `docs/CURRENT_RESEARCH_STATE.json`, and any affected canonical claims;
5. commit/push the coherent checkpoint.

## Priority logic

Priority is not based on popularity or convenience. Prefer work that:

- blocks multiple downstream rules;
- changes the meaning/state representation used by the engine;
- can be resolved from available primary source evidence at low cost;
- prevents invalid computation or false confidence;
- reduces the largest decision-critical uncertainty.

Do not invent a numeric score if the evidence does not justify one. `QUEUE.json` keeps an explicit ordered list and the reason for that order.

## Method order for each research worksheet

Default method is source-first / visual-first:

```text
PRIMARY SOURCE / LOCAL VIDEO
-> TRANSCRIPT + TIMESTAMP
-> VISUAL EVIDENCE WINDOW
-> AUDIO CROSSCHECK only if wording matters
-> EXPLICIT KNOWN / UNKNOWN SPLIT
-> TARGETED COMPUTATION only for residual ambiguity
-> CLOSURE
```

Computation is not abandoned. It is used after source review when measurement, relationship testing, robustness, or unresolved alternatives still require it.

## Worksheet minimum fields

Every worksheet must state:

- ID and title
- status
- why this matters now
- what is already known
- what is still unknown
- dependencies / blockers
- primary sources and tools to use first
- method order
- evidence to collect
- explicit non-goals / guards
- closure criteria
- expected outputs
- next action

## Files

- `QUEUE.json` — machine-readable current order and status; operational source of truth.
- `active/` — current active research worksheet. Normally one file only.
- `queued/` — waiting worksheets in priority order.
- `blocked/` — items waiting for evidence/user/source that cannot currently be obtained.
- `closed/` — completed worksheets after closure.

## Reuse-before-build

Before creating a new tool or pipeline, read repo root `TOOLS.md` and reuse registered tooling. Tool existence and research priority are separate questions.

## Research integrity

- `INCONCLUSIVE` is a valid closure.
- Do not tune a threshold because it produces a better historical result.
- Do not let backtest performance upgrade source provenance.
- Do not promote a downstream question while an unresolved upstream state definition would make the result misleading.
- Preserve historical queue/order changes rather than silently rewriting why work was prioritized.
