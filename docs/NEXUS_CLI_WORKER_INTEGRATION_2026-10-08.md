# NEXUS CLI Worker Integration — 2026-10-08

Status: SHARED TOOLING REGISTERED / XAU PROFILE AVAILABLE / RESEARCH SEMANTICS UNCHANGED

## Purpose

Provide a reusable bounded CLI-worker layer for Nexus-XAU-Engine without copying another project's runner assumptions into XAU.

Global tool:

`D:\tools\nexus-cli-worker\nexus_cli_worker.py`

Machine registries:

- `D:\tools\nexus-project-continuity\capabilities.json`
- `D:\tools\nexus-project-continuity\agent_orchestration.json`
- human-readable index: `D:\tools\TOOLS.md`

XAU profile:

`D:\tools\nexus-cli-worker\profiles\xau.json`

## Worker guarantees

The adapter injects XAU-specific guards into every derived packet and preserves the exact declared engine/model/route in a per-run receipt.

Defaults:

- no automatic Hermes `--yolo`;
- no automatic Hermes `--ignore-rules`;
- no OpenCode `--auto`;
- OpenCode uses `--pure`;
- OpenCode `--variant` is omitted unless explicitly selected;
- Hermes requires an explicit `--run-budget` and `--max-turns`;
- write mode requires explicit `--allow-write`;
- contributor-tier OpenCode routes require explicit `--allow-contributor`;
- packets outside the configured XAU roots are rejected unless explicitly allowed;
- Windows timeout cleanup terminates the complete child-process tree;
- every run persists a derived packet, manifest, stdout/stderr and receipt.

For disconnect-sensitive or expensive work, the worker itself should be launched through `nexus-durable-work`.

## Hermes / Nous LongCat 2.5 observation

Exact local direct-CLI model ID is confirmed as:

`meituan/longcat-2.5-preview:free`

Evidence surfaces included the current Hermes config and context/model cache.

Hermes runtime observations during integration:

- initial binary: v0.19.0+31623;
- interrupted update state existed with `.hermes-update-in-progress` and `.update_exit_code=120`;
- Nexus did not delete update markers and did not invoke `hermes update`;
- Hermes later self-reported v0.21.5+8877 during its own startup/recovery path;
- latest LongCat 2.5 smoke still did not reach model output; it timed out while Hermes reported completing source-update dependencies.

Therefore:

`LONGCAT_2_5_EXACT_ID = CONFIRMED`

`LONGCAT_2_5_LIVE_INFERENCE = NOT_YET_PROVEN`

The worker's live Hermes dispatch is fail-closed against an observed interrupted-update marker with non-zero update exit code, and a runtime doctor is required before each live dispatch.

The worker must never substitute LongCat 2.0 and call it LongCat 2.5.

## OpenCode observation

Live direct OpenCode verification on 2026-10-08:

- binary version: `1.18.34`;
- agents present: `plan`, `code-worker`, `code-review`, `docs-worker`;
- model present: `opencode/muse-spark-1.3-contributor-free`;
- model inventory reports reasoning, tool calling, and text/audio/image/video/pdf input capabilities.

The inventory is capability evidence, not task-quality or native-vision acceptance.

Because this route is a contributor tier, XAU/project data is not dispatched to it without explicit data-use opt-in.

## Validation

- NEXUS CLI worker unit tests: 8/8 PASS;
- Windows process-tree timeout test: PASS;
- OpenCode doctor: PASS;
- Hermes identity/basic startup probes: PASS when startup state allowed;
- LongCat 2.5 live inference smoke: NOT PROVEN, timeout during Hermes source-update dependency completion;
- global continuity registry JSON validation: PASS;
- `nexus-project-continuity/selftest.py`: PASS;
- `RESUME_WORK --project xau` discovers `nexus_cli_worker:OK`.

## Project boundary

This tooling checkpoint does not change:

- `0700_MINIMAL_V2.0` historical semantics;
- video trade-geometry re-anchor claims;
- unknown classifications;
- holdout state;
- economic scoring state;
- automatic order-send state.

The active research checkpoint remains the video trade-geometry re-anchor contract until that research loop is reconciled.
