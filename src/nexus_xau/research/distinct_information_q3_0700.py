from __future__ import annotations

import argparse
import itertools
import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

OUTCOME = "path_remaining_first_hit"
INDICATOR = "path_remaining_first_hit_indicator"
RESOLVED = {"TARGET_FIRST": 1.0, "POINT_CHECK_FIRST": 0.0}

AGE = "origin_age_hours_at_0700"
CONSUMED = "consumed_ratio_at_0700"
MTF1 = "alignment_count_recent_1_tf_bar"
MTF2 = "alignment_count_recent_2_tf_bars"
FEATURES = (AGE, CONSUMED, MTF1, MTF2)
MODEL_FAMILIES = {
    "RECENT_1_TF_BAR": (AGE, CONSUMED, MTF1),
    "RECENT_2_TF_BARS": (AGE, CONSUMED, MTF2),
}


@dataclass(frozen=True, slots=True)
class LogisticFit:
    status: str
    coefficients: tuple[float, ...] | None
    log_loss: float | None
    iterations: int


def _rank(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").rank(method="average")


def _rho(x: pd.Series, y: pd.Series) -> float | None:
    frame = pd.DataFrame({"x": x, "y": y}).dropna()
    if len(frame) < 2:
        return None
    if frame["x"].nunique() < 2 or frame["y"].nunique() < 2:
        return None
    value = frame["x"].rank(method="average").corr(
        frame["y"].rank(method="average"), method="pearson"
    )
    return None if pd.isna(value) else float(value)


def _residualize(target: np.ndarray, controls: np.ndarray) -> np.ndarray:
    if controls.ndim == 1:
        controls = controls.reshape(-1, 1)
    design = np.column_stack([np.ones(len(target)), controls])
    beta, *_ = np.linalg.lstsq(design, target, rcond=None)
    return target - design @ beta


def _partial_rank_rho(
    frame: pd.DataFrame,
    *,
    feature: str,
    outcome: str,
    controls: tuple[str, ...],
) -> tuple[float | None, int]:
    columns = [feature, outcome, *controls]
    data = frame[columns].apply(pd.to_numeric, errors="coerce").dropna()
    if len(data) < 3:
        return None, len(data)

    ranked = data.rank(method="average")
    if ranked[feature].nunique() < 2 or ranked[outcome].nunique() < 2:
        return None, len(ranked)

    x = ranked[feature].to_numpy(dtype=float)
    y = ranked[outcome].to_numpy(dtype=float)
    z = ranked[list(controls)].to_numpy(dtype=float)
    x_resid = _residualize(x, z)
    y_resid = _residualize(y, z)
    if float(np.std(x_resid)) == 0.0 or float(np.std(y_resid)) == 0.0:
        return None, len(ranked)
    value = float(np.corrcoef(x_resid, y_resid)[0, 1])
    if not math.isfinite(value):
        return None, len(ranked)
    return value, len(ranked)


def _sigmoid(values: np.ndarray) -> np.ndarray:
    clipped = np.clip(values, -35.0, 35.0)
    return 1.0 / (1.0 + np.exp(-clipped))


def _log_loss(y: np.ndarray, p: np.ndarray) -> float:
    clipped = np.clip(p, 1e-12, 1.0 - 1e-12)
    return float(-np.mean(y * np.log(clipped) + (1.0 - y) * np.log(1.0 - clipped)))


def _fit_logistic(
    x: np.ndarray,
    y: np.ndarray,
    *,
    max_iter: int = 100,
    tol: float = 1e-9,
) -> LogisticFit:
    if len(y) < 4 or len(np.unique(y)) < 2:
        return LogisticFit("UNSTABLE/UNRESOLVED", None, None, 0)

    design = np.column_stack([np.ones(len(y)), x])
    beta = np.zeros(design.shape[1], dtype=float)

    for iteration in range(1, max_iter + 1):
        p = _sigmoid(design @ beta)
        weights = p * (1.0 - p)
        if float(weights.max()) < 1e-12:
            return LogisticFit("UNSTABLE/UNRESOLVED", None, None, iteration)

        gradient = design.T @ (y - p)
        hessian = design.T @ (weights[:, None] * design)
        try:
            step = np.linalg.solve(hessian, gradient)
        except np.linalg.LinAlgError:
            return LogisticFit("UNSTABLE/UNRESOLVED", None, None, iteration)

        if not np.all(np.isfinite(step)):
            return LogisticFit("UNSTABLE/UNRESOLVED", None, None, iteration)

        beta = beta + step
        if float(np.max(np.abs(beta))) > 50.0:
            return LogisticFit("UNSTABLE/UNRESOLVED", None, None, iteration)

        if float(np.max(np.abs(step))) < tol:
            p_final = _sigmoid(design @ beta)
            return LogisticFit(
                "OK",
                tuple(float(value) for value in beta),
                _log_loss(y, p_final),
                iteration,
            )

    return LogisticFit("UNSTABLE/UNRESOLVED", None, None, max_iter)


def _rank_matrix(frame: pd.DataFrame, features: tuple[str, ...]) -> np.ndarray:
    ranked = frame[list(features)].rank(method="average")
    return ranked.to_numpy(dtype=float)


def _context_frame(frame: pd.DataFrame) -> pd.DataFrame:
    return (
        frame.groupby("context_id", as_index=False)
        .agg(
            context_target_first_fraction=(INDICATOR, "mean"),
            origin_age_hours_at_0700=(AGE, "median"),
            consumed_ratio_at_0700=(CONSUMED, "median"),
            alignment_count_recent_1_tf_bar=(MTF1, "median"),
            alignment_count_recent_2_tf_bars=(MTF2, "median"),
            resolved_origins=(INDICATOR, "size"),
        )
    )


def build_feature_rows(q2_events: pd.DataFrame) -> pd.DataFrame:
    frame = q2_events.copy()
    if INDICATOR not in frame.columns:
        frame[INDICATOR] = frame[OUTCOME].map(RESOLVED)

    keep = frame[frame[INDICATOR].notna()].copy()
    for column in (INDICATOR, *FEATURES):
        keep[column] = pd.to_numeric(keep[column], errors="coerce")
    keep = keep.dropna(subset=[INDICATOR, *FEATURES]).copy()

    columns = [
        "context_id",
        "day_id",
        "side",
        "origin_id",
        "origin_tf",
        "confirmation_event_id",
        OUTCOME,
        INDICATOR,
        *FEATURES,
    ]
    return keep[columns].sort_values(
        ["day_id", "side", "origin_tf", "origin_id"]
    ).reset_index(drop=True)


def build_pairwise(frame: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for origin_tf in ("H4", "H1"):
        subset = frame[frame["origin_tf"].eq(origin_tf)]
        for a, b in itertools.combinations(FEATURES, 2):
            pair = subset[[a, b]].dropna()
            rows.append(
                {
                    "origin_tf": origin_tf,
                    "feature_a": a,
                    "feature_b": b,
                    "n_rows": len(pair),
                    "rho": _rho(pair[a], pair[b]),
                }
            )
    return pd.DataFrame(rows)


def build_partial(frame: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for origin_tf in ("H4", "H1"):
        origin = frame[frame["origin_tf"].eq(origin_tf)].copy()
        context = _context_frame(origin)

        for family_name, family in MODEL_FAMILIES.items():
            for feature in family:
                controls = tuple(item for item in family if item != feature)
                rho, n_rows = _partial_rank_rho(
                    origin,
                    feature=feature,
                    outcome=INDICATOR,
                    controls=controls,
                )
                rows.append(
                    {
                        "origin_tf": origin_tf,
                        "analysis_level": "ORIGIN_ROW",
                        "model_family": family_name,
                        "feature": feature,
                        "controls": ",".join(controls),
                        "n_rows": n_rows,
                        "n_contexts": int(origin["context_id"].nunique()),
                        "partial_rho": rho,
                        "median_resolved_origins_per_context": None,
                    }
                )

                context_outcome = "context_target_first_fraction"
                rho_ctx, n_ctx = _partial_rank_rho(
                    context,
                    feature=feature,
                    outcome=context_outcome,
                    controls=controls,
                )
                rows.append(
                    {
                        "origin_tf": origin_tf,
                        "analysis_level": "CONTEXT",
                        "model_family": family_name,
                        "feature": feature,
                        "controls": ",".join(controls),
                        "n_rows": n_ctx,
                        "n_contexts": n_ctx,
                        "partial_rho": rho_ctx,
                        "median_resolved_origins_per_context": (
                            float(context["resolved_origins"].median())
                            if not context.empty
                            else None
                        ),
                    }
                )
    return pd.DataFrame(rows)


def build_leave_one_out(frame: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for origin_tf in ("H4", "H1"):
        subset = frame[frame["origin_tf"].eq(origin_tf)].copy()
        for family_name, family in MODEL_FAMILIES.items():
            data = subset[[INDICATOR, *family]].dropna().copy()
            y = data[INDICATOR].to_numpy(dtype=float)
            if data.empty:
                full = LogisticFit("UNSTABLE/UNRESOLVED", None, None, 0)
            else:
                full = _fit_logistic(_rank_matrix(data, family), y)

            full_coeff = full.coefficients
            if full_coeff is None:
                coefficient_signs = None
            else:
                coefficient_signs = {
                    feature: (
                        "POSITIVE"
                        if full_coeff[index + 1] > 0
                        else "NEGATIVE"
                        if full_coeff[index + 1] < 0
                        else "ZERO"
                    )
                    for index, feature in enumerate(family)
                }

            rows.append(
                {
                    "origin_tf": origin_tf,
                    "model_family": family_name,
                    "model": "FULL",
                    "removed_feature": None,
                    "features": ",".join(family),
                    "n_rows": len(data),
                    "n_contexts": int(subset.loc[data.index, "context_id"].nunique())
                    if len(data)
                    else 0,
                    "fit_status": full.status,
                    "iterations": full.iterations,
                    "log_loss": full.log_loss,
                    "delta_log_loss_vs_full": 0.0 if full.log_loss is not None else None,
                    "coefficient_signs": (
                        json.dumps(coefficient_signs, sort_keys=True)
                        if coefficient_signs is not None
                        else None
                    ),
                }
            )

            for removed in family:
                retained = tuple(feature for feature in family if feature != removed)
                reduced = (
                    _fit_logistic(_rank_matrix(data, retained), y)
                    if not data.empty
                    else LogisticFit("UNSTABLE/UNRESOLVED", None, None, 0)
                )
                delta = (
                    reduced.log_loss - full.log_loss
                    if reduced.log_loss is not None and full.log_loss is not None
                    else None
                )
                rows.append(
                    {
                        "origin_tf": origin_tf,
                        "model_family": family_name,
                        "model": "LEAVE_ONE_OUT",
                        "removed_feature": removed,
                        "features": ",".join(retained),
                        "n_rows": len(data),
                        "n_contexts": int(subset.loc[data.index, "context_id"].nunique())
                        if len(data)
                        else 0,
                        "fit_status": reduced.status,
                        "iterations": reduced.iterations,
                        "log_loss": reduced.log_loss,
                        "delta_log_loss_vs_full": delta,
                        "coefficient_signs": None,
                    }
                )
    return pd.DataFrame(rows)


def _preview(partial: pd.DataFrame) -> list[dict[str, object]]:
    rows = partial[
        partial["origin_tf"].eq("H4")
        & partial["analysis_level"].eq("ORIGIN_ROW")
    ]
    return [
        {
            "model_family": row.model_family,
            "feature": row.feature,
            "n": int(row.n_rows),
            "partial_rho": (
                None if pd.isna(row.partial_rho) else float(row.partial_rho)
            ),
        }
        for row in rows.itertuples(index=False)
    ]


def run(
    *,
    q2_feature_events_path: str | Path,
    output_root: str | Path,
    period_label: str,
) -> dict[str, object]:
    raw = pd.read_csv(q2_feature_events_path)
    feature_rows = build_feature_rows(raw)
    pairwise = build_pairwise(feature_rows)
    partial = build_partial(feature_rows)
    leave_one_out = build_leave_one_out(feature_rows)

    report = {
        "research_status": "0700_Q3_DISTINCT_INFORMATION_RELATIONSHIP_ONLY",
        "period_label": period_label,
        "resolved_feature_rows": len(feature_rows),
        "contexts": int(feature_rows["context_id"].nunique()) if not feature_rows.empty else 0,
        "by_origin_tf": {
            origin_tf: {
                "rows": int((feature_rows["origin_tf"] == origin_tf).sum()),
                "contexts": int(
                    feature_rows.loc[
                        feature_rows["origin_tf"] == origin_tf, "context_id"
                    ].nunique()
                ),
            }
            for origin_tf in ("H4", "H1")
        },
        "h4_partial_preview": _preview(partial),
        "guards": [
            "No score, cutoff, probability threshold, or production rule is created.",
            "H4 is the primary population because Q2 run-progress replication was H4-stable; H1 is sensitivity.",
            "Recent-1 and recent-2 model families are kept separate and neither may be promoted as canonical from Q3.",
            "Partial associations use frozen rank-residual representation.",
            "Leave-one-out logistic models are descriptive in-sample diagnostics only.",
            "UNSTABLE/UNRESOLVED fit status must be retained rather than changing the model.",
        ],
    }

    root = Path(output_root)
    root.mkdir(parents=True, exist_ok=True)
    feature_rows.to_csv(root / "Q3_FEATURE_ROWS.csv", index=False)
    pairwise.to_csv(root / "Q3_PAIRWISE_SPEARMAN.csv", index=False)
    partial.to_csv(root / "Q3_PARTIAL_ASSOCIATIONS.csv", index=False)
    leave_one_out.to_csv(root / "Q3_LEAVE_ONE_OUT.csv", index=False)
    (root / "REPORT.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q2-feature-events", required=True)
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--period-label", required=True)
    args = parser.parse_args()

    report = run(
        q2_feature_events_path=args.q2_feature_events,
        output_root=args.output_root,
        period_label=args.period_label,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
