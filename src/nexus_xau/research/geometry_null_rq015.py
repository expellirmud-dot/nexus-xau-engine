from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_POINT_SIZE = 0.01
H4_RUN_POINTS = 1500.0
OUTCOME_STATES = (
    "TARGET_FIRST",
    "POINT_CHECK_FIRST",
    "NEITHER_BY_NEXT_0700",
    "AMBIGUOUS_SAME_BAR",
)
RESOLVED_STATES = ("TARGET_FIRST", "POINT_CHECK_FIRST")
FREEZE_REF = "docs/0700_RQ015_GEOMETRY_NULL_ANALYSIS_FREEZE_2026-09-13.md"


def _sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _rank(values: pd.Series) -> np.ndarray:
    return values.rank(method="average").to_numpy(dtype=float)


def _corr(x: np.ndarray, y: np.ndarray) -> float:
    if len(x) < 3 or np.std(x) == 0.0 or np.std(y) == 0.0:
        return float("nan")
    return float(np.corrcoef(x, y)[0, 1])


def spearman(values: pd.Series, outcome: pd.Series) -> float:
    return _corr(_rank(values), _rank(outcome))


def derive_geometry(events: pd.DataFrame) -> pd.DataFrame:
    required = {
        "candidate_state", "path_remaining_first_hit",
        "path_remaining_target_price", "confirmation_close",
        "origin_anchor_price", "remaining_points_at_confirmation",
        "confirmation_known_at", "next_cutoff_utc",
        "consumed_ratio_at_0700", "consumed_points_at_confirmation",
    }
    missing = sorted(required - set(events.columns))
    if missing:
        raise ValueError(f"missing required columns: {missing}")

    out = events.loc[events["candidate_state"].eq("RESEARCH_CANDIDATE")].copy()
    if out.empty:
        raise ValueError("no RESEARCH_CANDIDATE rows")

    unknown = sorted(set(out["path_remaining_first_hit"].dropna()) - set(OUTCOME_STATES))
    if unknown:
        raise ValueError(f"unexpected outcome states: {unknown}")

    out["target_distance_points"] = (
        (out["path_remaining_target_price"] - out["confirmation_close"]).abs()
        / PROJECT_POINT_SIZE
    )
    out["point_distance_points"] = (
        (out["confirmation_close"] - out["origin_anchor_price"]).abs()
        / PROJECT_POINT_SIZE
    )
    total = out["target_distance_points"] + out["point_distance_points"]
    if bool((total <= 0).any()):
        raise ValueError("non-positive geometry denominator")

    out["geometry_target_advantage"] = out["point_distance_points"] / total
    out["total_boundary_distance_points"] = total
    known = pd.to_datetime(out["confirmation_known_at"], utc=True)
    cutoff = pd.to_datetime(out["next_cutoff_utc"], utc=True)
    out["horizon_minutes"] = (cutoff - known).dt.total_seconds() / 60.0
    if bool((out["horizon_minutes"] <= 0).any()):
        raise ValueError("non-positive horizon")

    if not np.allclose(
        out["target_distance_points"].to_numpy(dtype=float),
        out["remaining_points_at_confirmation"].to_numpy(dtype=float),
        rtol=1e-9,
        atol=1e-6,
    ):
        diff = (
            out["target_distance_points"] - out["remaining_points_at_confirmation"]
        ).abs()
        raise ValueError(f"target-distance validation failed: max_abs_diff={diff.max()}")

    out["consumed_ratio_at_confirmation"] = (
        out["consumed_points_at_confirmation"] / H4_RUN_POINTS
    )
    return out


def partial_rank_residual(frame: pd.DataFrame, consumed_col: str) -> float:
    resolved = frame.loc[
        frame["path_remaining_first_hit"].isin(RESOLVED_STATES)
    ].copy()
    if len(resolved) < 5:
        return float("nan")

    outcome = resolved["path_remaining_first_hit"].eq("TARGET_FIRST").astype(float)
    controls = np.column_stack(
        [
            np.ones(len(resolved)),
            _rank(resolved["geometry_target_advantage"]),
            _rank(resolved["total_boundary_distance_points"]),
            _rank(resolved["horizon_minutes"]),
        ]
    )
    consumed_rank = _rank(resolved[consumed_col])
    outcome_rank = _rank(outcome)
    consumed_beta = np.linalg.lstsq(controls, consumed_rank, rcond=None)[0]
    outcome_beta = np.linalg.lstsq(controls, outcome_rank, rcond=None)[0]
    consumed_resid = consumed_rank - controls @ consumed_beta
    outcome_resid = outcome_rank - controls @ outcome_beta
    return _corr(consumed_resid, outcome_resid)


def summarize_period(name: str, frame: pd.DataFrame) -> dict[str, object]:
    counts_raw = frame["path_remaining_first_hit"].value_counts().to_dict()
    counts = {state: int(counts_raw.get(state, 0)) for state in OUTCOME_STATES}
    n = len(frame)
    proportions = {state: counts[state] / n for state in OUTCOME_STATES}

    numeric = [
        "consumed_ratio_at_0700",
        "consumed_ratio_at_confirmation",
        "target_distance_points",
        "point_distance_points",
        "geometry_target_advantage",
        "total_boundary_distance_points",
        "horizon_minutes",
    ]
    medians: dict[str, dict[str, float | None]] = {}
    for state in OUTCOME_STATES:
        subset = frame.loc[frame["path_remaining_first_hit"].eq(state)]
        medians[state] = {
            col: (None if subset.empty else float(subset[col].median()))
            for col in numeric
        }

    resolved = frame.loc[
        frame["path_remaining_first_hit"].isin(RESOLVED_STATES)
    ].copy()
    outcome = resolved["path_remaining_first_hit"].eq("TARGET_FIRST").astype(float)
    diagnostics = {
        "resolved_rows": len(resolved),
        "rho_consumed_0700_outcome": spearman(
            resolved["consumed_ratio_at_0700"], outcome
        ),
        "rho_geometry_outcome": spearman(
            resolved["geometry_target_advantage"], outcome
        ),
        "rho_consumed_0700_geometry": spearman(
            resolved["consumed_ratio_at_0700"],
            resolved["geometry_target_advantage"],
        ),
        "partial_rank_consumed_0700_given_geometry": partial_rank_residual(
            frame, "consumed_ratio_at_0700"
        ),
        "partial_rank_consumed_confirmation_given_geometry": partial_rank_residual(
            frame, "consumed_ratio_at_confirmation"
        ),
    }
    return {
        "period": name,
        "candidate_rows": int(n),
        "outcome_counts": counts,
        "outcome_proportions": proportions,
        "median_by_outcome": medians,
        "resolved_diagnostics": diagnostics,
    }


def classify(discovery: dict[str, object], replication: dict[str, object]) -> str:
    diagnostics = [
        discovery["resolved_diagnostics"],
        replication["resolved_diagnostics"],
    ]
    primary = [
        float(x["partial_rank_consumed_0700_given_geometry"])
        for x in diagnostics
    ]
    if all(np.isfinite(x) and x > 0 for x in primary):
        return "CONSUMED_RESIDUAL_RELATION_SURVIVES_GEOMETRY_CONTROL"

    geometry_outcome = [float(x["rho_geometry_outcome"]) for x in diagnostics]
    consumed_geometry = [
        float(x["rho_consumed_0700_geometry"]) for x in diagnostics
    ]
    if (
        all(np.isfinite(x) and x > 0 for x in geometry_outcome)
        and all(np.isfinite(x) and x > 0 for x in consumed_geometry)
        and all(np.isfinite(x) and x <= 0 for x in primary)
    ):
        return "CONSUMED_ASSOCIATION_EXPLAINED_OR_DOMINATED_BY_GEOMETRY"

    return "INDEPENDENT_EFFECT_NOT_IDENTIFIABLE_WITH_CURRENT_DATA"


def run(
    *,
    discovery_path: str | Path,
    replication_path: str | Path,
    output_root: str | Path,
) -> dict[str, object]:
    discovery_path = Path(discovery_path)
    replication_path = Path(replication_path)
    discovery = derive_geometry(pd.read_csv(discovery_path))
    replication = derive_geometry(pd.read_csv(replication_path))

    discovery_summary = summarize_period("DISCOVERY", discovery)
    replication_summary = summarize_period("REPLICATION", replication)
    classification = classify(discovery_summary, replication_summary)

    root = Path(output_root)
    root.mkdir(parents=True, exist_ok=True)
    discovery.to_csv(root / "DISCOVERY_GEOMETRY_ROWS.csv", index=False)
    replication.to_csv(root / "REPLICATION_GEOMETRY_ROWS.csv", index=False)

    report: dict[str, object] = {
        "rq": "RQ-015",
        "freeze_ref": FREEZE_REF,
        "status": "FROZEN_GEOMETRY_NULL_EXECUTED",
        "inputs": {
            "discovery": str(discovery_path),
            "discovery_sha256": _sha256(discovery_path),
            "replication": str(replication_path),
            "replication_sha256": _sha256(replication_path),
        },
        "implementation_sha256": _sha256(__file__),
        "geometry_validation": {
            "target_distance_matches_remaining_points": True,
            "positive_geometry_denominator": True,
            "positive_horizon": True,
        },
        "discovery": discovery_summary,
        "replication": replication_summary,
        "classification": classification,
        "guards": [
            "Not a pristine blind preregistration; earlier outcomes were already observed.",
            "No consumed threshold or geometry threshold.",
            "No parameter/model search after freeze.",
            "NEITHER and AMBIGUOUS are preserved in full-state output.",
            "No trade Win Rate, PnL, fill, cost, or profitability claim.",
        ],
    }
    (root / "REPORT.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--discovery", required=True)
    parser.add_argument("--replication", required=True)
    parser.add_argument("--output-root", required=True)
    args = parser.parse_args()
    report = run(
        discovery_path=args.discovery,
        replication_path=args.replication,
        output_root=args.output_root,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
