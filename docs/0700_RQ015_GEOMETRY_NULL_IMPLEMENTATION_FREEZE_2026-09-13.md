# RQ-015 Geometry-Null Implementation Freeze - 2026-09-13

Status: IMPLEMENTATION FROZEN / REAL ARTIFACT EXECUTION PENDING

## Scope

This checkpoint freezes the implementation of the analysis specified in:

docs/0700_RQ015_GEOMETRY_NULL_ANALYSIS_FREEZE_2026-09-13.md

No Discovery or Replication result from the new analyzer has been opened before this checkpoint.

The historical V2.0 outcomes and earlier exploratory one-variable geometry diagnostic were already known, so this is not a pristine blind preregistration.

## Frozen implementation

Analyzer:

src/nexus_xau/research/geometry_null_rq015.py

SHA256:

8f0579b922d31bb762f13d38d8ac0f067b37c7d97868ce3556426e641d81cb81

Tests:

tests/test_geometry_null_rq015.py

SHA256:

42053c21e75af7b67bc51a05f5336aadb3ff656885a69124236f304be14d5d3f

Underlying frozen Minimal V2 implementation remains unchanged:

src/nexus_xau/research/minimal_v2_0700.py

SHA256:

25ccd02567e065230b7757dab73c80471c077f6419da65f3cd4c78db4d43cca7

Analysis freeze SHA256:

49f26d026ae870cc2508c8adfe2d80896a078d6dab23ff09f93c71206aa91772

## Validation before real execution

Targeted unit tests:

- tests/test_geometry_null_rq015.py
- result: 5 passed

Ruff:

- analyzer + new tests
- result: PASS

Full repository test suite:

- first default-temp attempt hit the known Windows pytest temp permission failure;
- rerun with --basetemp=.pytest-tmp-rq015-geometry-freeze;
- result: PASS across the full suite;
- only existing NumPy/Pandas deprecation warnings were emitted.

## Frozen execution contract

The next execution must:

1. read only the checkpointed V2.0 research-event CSVs;
2. not rerun minimal_v2_0700.py;
3. not change formulas, controls, thresholds, or outcome handling;
4. preserve NEITHER and AMBIGUOUS rows in the full-state output;
5. compute Discovery and Replication separately;
6. apply the classification rule exactly as frozen;
7. write row-level derived geometry and REPORT.json;
8. stop and record a failure if geometry validation fails.

## Prohibited before result checkpoint

- no alternate geometry formula;
- no feature selection;
- no threshold/bin search;
- no side-specific rescue model;
- no post-result tuning;
- no trade/PnL interpretation.

## Next action

Execute the frozen analyzer unchanged on the existing Discovery and Replication V2.0 artifacts, inspect the generated report, then reconcile RQ-015 and canonical project state.
