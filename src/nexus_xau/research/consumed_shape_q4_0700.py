from __future__ import annotations

import argparse
import json
from itertools import pairwise
from pathlib import Path

import pandas as pd

OUTCOME = "path_remaining_first_hit"
INDICATOR = "path_remaining_first_hit_indicator"
FEATURE = "consumed_ratio_at_0700"
MFE = "post_confirmation_mfe_points"
MAE = "post_confirmation_mae_points"
ORIGIN_TFS = ("H4", "H1")
QUINTILE_LABELS = ("Q1", "Q2", "Q3", "Q4", "Q5")


def _spearman(x: pd.Series, y: pd.Series) -> float | None:
    frame = pd.DataFrame({"x": x, "y": y}).dropna()
    if len(frame) < 2:
        return None
    if frame["x"].nunique() < 2 or frame["y"].nunique() < 2:
        return None
    value = frame["x"].rank(method="average").corr(
        frame["y"].rank(method="average"),
        method="pearson",
    )
    return None if pd.isna(value) else float(value)


def build_feature_rows(q2_events: pd.DataFrame) -> pd.DataFrame:
    frame = q2_events.copy()
    required = [
        "context_id",
        "day_id",
        "side",
        "origin_id",
        "origin_tf",
        OUTCOME,
        INDICATOR,
        FEATURE,
        MFE,
        MAE,
    ]
    missing = [column for column in required if column not in frame.columns]
    if missing:
        raise ValueError(f"missing required Q2 columns: {missing}")

    frame[INDICATOR] = pd.to_numeric(frame[INDICATOR], errors="coerce")
    frame[FEATURE] = pd.to_numeric(frame[FEATURE], errors="coerce")
    frame[MFE] = pd.to_numeric(frame[MFE], errors="coerce")
    frame[MAE] = pd.to_numeric(frame[MAE], errors="coerce")

    frame = frame[
        frame["origin_tf"].isin(ORIGIN_TFS)
        & frame[INDICATOR].notna()
        & frame[FEATURE].notna()
    ].copy()

    return frame[required].sort_values(
        ["day_id", "side", "origin_tf", "origin_id"]
    ).reset_index(drop=True)


def _context_rows(frame: pd.DataFrame) -> pd.DataFrame:
    if frame.empty:
        return pd.DataFrame(
            columns=[
                "context_id",
                FEATURE,
                "context_target_first_fraction",
                "resolved_origins",
            ]
        )
    return (
        frame.groupby("context_id", as_index=False)
        .agg(
            consumed_ratio_at_0700=(FEATURE, "median"),
            context_target_first_fraction=(INDICATOR, "mean"),
            resolved_origins=(INDICATOR, "size"),
        )
    )


def _assign_quintiles(series: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce")
    if numeric.notna().sum() < 5 or numeric.nunique(dropna=True) < 5:
        raise ValueError("Q4 requires at least five non-null unique consumed values")
    return pd.qcut(
        numeric,
        q=5,
        labels=list(QUINTILE_LABELS),
        duplicates="raise",
    )


def _shape_classification(rates: list[float | None]) -> tuple[str, list[float | None]]:
    diffs: list[float | None] = []
    for left, right in pairwise(rates):
        if left is None or right is None:
            diffs.append(None)
        else:
            diffs.append(float(right - left))
    if any(value is None for value in diffs):
        return "UNRESOLVED", diffs
    return (
        "STRICT_NONDECREASING"
        if all(value >= 0 for value in diffs if value is not None)
        else "NOT_STRICT_NONDECREASING",
        diffs,
    )


def build_quintiles(feature_rows: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for origin_tf in ORIGIN_TFS:
        origin = feature_rows[feature_rows["origin_tf"].eq(origin_tf)].copy()
        if origin.empty:
            continue
        origin["quintile"] = _assign_quintiles(origin[FEATURE])

        for label in QUINTILE_LABELS:
            group = origin[origin["quintile"].astype(str).eq(label)]
            target = int((group[INDICATOR] == 1.0).sum())
            point = int((group[INDICATOR] == 0.0).sum())
            resolved = target + point
            rows.append(
                {
                    "origin_tf": origin_tf,
                    "analysis_level": "ORIGIN_ROW",
                    "quintile": label,
                    "n_rows": len(group),
                    "n_contexts": int(group["context_id"].nunique()),
                    "consumed_min": float(group[FEATURE].min()),
                    "consumed_max": float(group[FEATURE].max()),
                    "consumed_median": float(group[FEATURE].median()),
                    "target_first": target,
                    "point_check_first": point,
                    "target_first_fraction": target / resolved if resolved else None,
                    "median_mfe_points": (
                        float(group[MFE].median()) if group[MFE].notna().any() else None
                    ),
                    "median_mae_points": (
                        float(group[MAE].median()) if group[MAE].notna().any() else None
                    ),
                    "median_resolved_origins_per_context": None,
                }
            )

        context = _context_rows(origin)
        context["quintile"] = _assign_quintiles(context[FEATURE])
        for label in QUINTILE_LABELS:
            group = context[context["quintile"].astype(str).eq(label)]
            rows.append(
                {
                    "origin_tf": origin_tf,
                    "analysis_level": "CONTEXT",
                    "quintile": label,
                    "n_rows": len(group),
                    "n_contexts": len(group),
                    "consumed_min": float(group[FEATURE].min()),
                    "consumed_max": float(group[FEATURE].max()),
                    "consumed_median": float(group[FEATURE].median()),
                    "target_first": None,
                    "point_check_first": None,
                    "target_first_fraction": float(
                        group["context_target_first_fraction"].mean()
                    ),
                    "median_mfe_points": None,
                    "median_mae_points": None,
                    "median_resolved_origins_per_context": float(
                        group["resolved_origins"].median()
                    ),
                }
            )
    return pd.DataFrame(rows)


def _trim_bounds(series: pd.Series) -> tuple[float, float]:
    clean = pd.to_numeric(series, errors="coerce").dropna()
    return float(clean.quantile(0.10)), float(clean.quantile(0.90))


def _trim_variants(
    frame: pd.DataFrame,
    *,
    feature: str,
) -> list[tuple[str, pd.DataFrame, float, float]]:
    low, high = _trim_bounds(frame[feature])
    return [
        ("FULL", frame.copy(), low, high),
        ("CENTRAL_80", frame[(frame[feature] >= low) & (frame[feature] <= high)].copy(), low, high),
        ("DROP_BOTTOM_10", frame[frame[feature] >= low].copy(), low, high),
        ("DROP_TOP_10", frame[frame[feature] <= high].copy(), low, high),
    ]


def build_trim_sensitivity(feature_rows: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for origin_tf in ORIGIN_TFS:
        origin = feature_rows[feature_rows["origin_tf"].eq(origin_tf)].copy()
        if origin.empty:
            continue

        for variant, group, low, high in _trim_variants(origin, feature=FEATURE):
            rows.append(
                {
                    "origin_tf": origin_tf,
                    "analysis_level": "ORIGIN_ROW",
                    "trim_variant": variant,
                    "q10_consumed": low,
                    "q90_consumed": high,
                    "n_rows": len(group),
                    "n_contexts": int(group["context_id"].nunique()),
                    "rho": _spearman(group[FEATURE], group[INDICATOR]),
                }
            )

        context = _context_rows(origin)
        for variant, group, low, high in _trim_variants(context, feature=FEATURE):
            rows.append(
                {
                    "origin_tf": origin_tf,
                    "analysis_level": "CONTEXT",
                    "trim_variant": variant,
                    "q10_consumed": low,
                    "q90_consumed": high,
                    "n_rows": len(group),
                    "n_contexts": len(group),
                    "rho": _spearman(
                        group[FEATURE],
                        group["context_target_first_fraction"],
                    ),
                }
            )
    return pd.DataFrame(rows)


def _quintile_summary(
    quintiles: pd.DataFrame,
    *,
    origin_tf: str,
    analysis_level: str,
) -> dict[str, object]:
    subset = quintiles[
        quintiles["origin_tf"].eq(origin_tf)
        & quintiles["analysis_level"].eq(analysis_level)
    ].copy()
    lookup = {
        str(row.quintile): (
            None if pd.isna(row.target_first_fraction) else float(row.target_first_fraction)
        )
        for row in subset.itertuples(index=False)
    }
    rates = [lookup.get(label) for label in QUINTILE_LABELS]
    classification, diffs = _shape_classification(rates)
    return {
        "rates": {label: rate for label, rate in zip(QUINTILE_LABELS, rates, strict=True)},
        "adjacent_differences": {
            f"{QUINTILE_LABELS[index + 1]}-{QUINTILE_LABELS[index]}": diffs[index]
            for index in range(4)
        },
        "shape_classification": classification,
    }


def _trim_summary(
    trim: pd.DataFrame,
    *,
    origin_tf: str,
    analysis_level: str,
) -> dict[str, object]:
    subset = trim[
        trim["origin_tf"].eq(origin_tf)
        & trim["analysis_level"].eq(analysis_level)
    ]
    return {
        str(row.trim_variant): {
            "n": int(row.n_rows),
            "rho": None if pd.isna(row.rho) else float(row.rho),
            "q10": float(row.q10_consumed),
            "q90": float(row.q90_consumed),
        }
        for row in subset.itertuples(index=False)
    }


def run(
    *,
    q2_feature_events_path: str | Path,
    output_root: str | Path,
    period_label: str,
) -> dict[str, object]:
    raw = pd.read_csv(q2_feature_events_path)
    feature_rows = build_feature_rows(raw)
    quintiles = build_quintiles(feature_rows)
    trim = build_trim_sensitivity(feature_rows)

    report = {
        "research_status": "0700_Q4_H4_CONSUMED_SHAPE_DIAGNOSTIC_ONLY",
        "period_label": period_label,
        "primary_feature": FEATURE,
        "primary_population": "H4",
        "resolved_rows": len(feature_rows),
        "by_origin_tf": {
            origin_tf: {
                "rows": int((feature_rows["origin_tf"] == origin_tf).sum()),
                "contexts": int(
                    feature_rows.loc[
                        feature_rows["origin_tf"] == origin_tf,
                        "context_id",
                    ].nunique()
                ),
                "origin_quintile_shape": _quintile_summary(
                    quintiles,
                    origin_tf=origin_tf,
                    analysis_level="ORIGIN_ROW",
                ),
                "context_quintile_shape": _quintile_summary(
                    quintiles,
                    origin_tf=origin_tf,
                    analysis_level="CONTEXT",
                ),
                "origin_trim_sensitivity": _trim_summary(
                    trim,
                    origin_tf=origin_tf,
                    analysis_level="ORIGIN_ROW",
                ),
                "context_trim_sensitivity": _trim_summary(
                    trim,
                    origin_tf=origin_tf,
                    analysis_level="CONTEXT",
                ),
            }
            for origin_tf in ORIGIN_TFS
        },
        "guards": [
            "Quintile boundaries are descriptive partitions, not trading thresholds.",
            "10th/90th percentile trim values are diagnostics, not entry limits.",
            "No bin or tail is selected as an optimal consumed range.",
            "H4 is primary; H1 is predeclared sensitivity.",
            "No P&L, expectancy, trade/system Win Rate, or production decision rule is computed.",
        ],
    }

    root = Path(output_root)
    root.mkdir(parents=True, exist_ok=True)
    feature_rows.to_csv(root / "Q4_FEATURE_ROWS.csv", index=False)
    quintiles.to_csv(root / "Q4_QUINTILES.csv", index=False)
    trim.to_csv(root / "Q4_TRIM_SENSITIVITY.csv", index=False)
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
