# RQ-011 — Pristine V0 Holdout Labeling and Reservation Protocol

Status: ACTIVE — protocol design only; holdout outcomes remain unopened

## Objective

Define and freeze the prospective holdout protocol for:

```text
SIG_MODE2_EXTERNALLY_LABELED_SIGNAL_RUN_V0.1
```

without inspecting or scoring future holdout outcomes.

RQ-011 is a methodology checkpoint, not an outcome run.

## Dependency

Requires frozen RQ-010 implementation:

- `src/nexus_xau/research/sig_mode2_signal_run_v0.py`
- schema version `SIG_MODE2_SIGNAL_RUN_V0.1`
- RQ-010 full tests/Ruff pass
- implementation commit/version hash recorded before holdout begins

## Questions to close

1. What exact clock/date boundary makes a price period prospective and untouched relative to V0 freeze?
2. Who/what may label a Mode-2 event, and what evidence is visible at label time?
3. How is `label_known_before_outcome=true` independently auditable rather than self-asserted?
4. How are labels locked so they cannot be changed after future bars are observed?
5. How are unresolved multi-family conflicts excluded/flagged before scoring?
6. What dataset/symbol/server/tick-grid metadata must be locked with the manifest?
7. How should missing data, off-grid prices, duplicate events, and retrospective corrections be handled?
8. What statistical stopping/reporting protocol can be preregistered without choosing a threshold from observed holdout outcomes?
9. How is the one-time scoring step separated from labeling and data collection?

## Non-negotiable guardrails

```text
NO_HOLDOUT_OUTCOME_PEEK
NO_LABEL_AFTER_OUTCOME
NO_THRESHOLD_TUNING_ON_HOLDOUT
NO_EVENT_DELETION_BECAUSE_RESULT_IS_BAD
NO_RECLASSIFICATION_AFTER_RESULT
NO_SYSTEM_WIN_RATE_LABEL
```

Permitted post-lock corrections must be limited to documented data/provenance defects that can be established independently of outcome direction. Every correction requires an append-only audit record; original manifest identity must remain recoverable.

## Candidate protocol architecture

```text
V0 CODE FREEZE
-> freeze commit hash + schema + environment contract
-> prospective observation window begins after freeze boundary
-> identify/labeled event using only data visible through event known_at
-> append event to locked manifest/audit log
-> quarantine forward outcome from labeler/research decision path
-> continue until preregistered stopping/reporting condition
-> seal manifest
-> one scoring run with frozen V0
-> report SIGNAL/RUN OUTCOMES with ambiguity/exclusions preserved
```

## Evidence separation

### Source-backed / engineering facts already frozen

- Mode-2 point-check knowledge time;
- literal broker-tick contact destruction;
- no-lookahead replay;
- same-bar ambiguity;
- H1/H4 V0 scope;
- manifest provenance requirements.

### RQ-011 research conventions to preregister

- prospective start boundary;
- label-lock storage mechanism;
- correction policy;
- stopping/reporting condition;
- data completeness rules;
- scorer separation / one-run procedure.

These conventions must never be described as instructor rules.

## Holdout remains closed until

- RQ-010 implementation commit is final and pushed;
- this RQ-011 protocol is itself frozen and pushed;
- prospective boundary is recorded before data after that boundary is scored;
- label/audit storage mechanism is ready;
- stopping/reporting rule is preregistered.

## Done when

A versioned protocol states exactly how a future event becomes eligible, locked, corrected/excluded, sealed, and scored, with no parameter selected from holdout outcomes. Only then may a separate RQ authorize actual prospective holdout collection/scoring.
