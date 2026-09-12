from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

PRIMARY_VARIANT = "FIRST_EXPECTED_SIDE_PA_PROXY"
PATH_OUTCOME = "path_remaining_first_hit"
ORIGIN_OUTCOME = "origin_level_first_hit"
OUTCOMES = (PATH_OUTCOME, ORIGIN_OUTCOME)

FEATURES = (
    "origin_age_hours_at_0700",
    "consumed_ratio_at_0700",
    "remaining_ratio_at_confirmation",
    "remaining_points_at_0700",
    "remaining_points_at_confirmation",
    "alignment_count_exact",
    "alignment_count_recent_1_tf_bar",
    "alignment_count_recent_2_tf_bars",
)

ORIGIN_STATE_FEATURES = (
    "origin_age_hours_at_0700",
    "consumed_ratio_at_0700",
    "remaining_ratio_at_confirmation",
    "remaining_points_at_0700",
    "remaining_points_at_confirmation",
)

ALIGNMENT_FEATURES = (
    "alignment_count_exact",
    "alignment_count_recent_1_tf_bar",
    "alignment_count_recent_2_tf_bars",
)

RESOLVED = {"TARGET_FIRST": 1.0, "POINT_CHECK_FIRST": 0.0}


def _spearman(x: pd.Series, y: pd.Series) -> float | None:
    frame = pd.DataFrame({"x": x, "y": y}).dropna()
    if len(frame) < 2:
        return None
    if frame["x"].nunique(dropna=True) < 2:
        return None
    if frame["y"].nunique(dropna=True) < 2:
        return None
    xr = frame["x"].rank(method="average")
    yr = frame["y"].rank(method="average")
    value = xr.corr(yr, method="pearson")
    if pd.isna(value):
        return None
    return float(value)


def _quantiles(series: pd.Series) -> dict[str, float | None]:
    clean = pd.to_numeric(series, errors="coerce").dropna()
    if clean.empty:
        return {
            "median": None,
            "q25": None,
            "q75": None,
        }
    return {
        "median": float(clean.median()),
        "q25": float(clean.quantile(0.25)),
        "q75": float(clean.quantile(0.75)),
    }


def build_feature_events(
    *,
    q1_events: pd.DataFrame,
    confirmation_events: pd.DataFrame,
) -> pd.DataFrame:
    base = q1_events[
        q1_events["variant"].eq(PRIMARY_VARIANT)
        & q1_events["candidate_state"].eq("SCORED")
    ].copy()
    if base.empty:
        return base

    needed = [
        "event_id",
        "alignment_count_exact",
        "alignment_count_recent_1_tf_bar",
        "alignment_count_recent_2_tf_bars",
    ]
    confirmation = confirmation_events[needed].copy()
    if confirmation["event_id"].duplicated().any():
        raise ValueError("confirmation event_id must be unique")

    base = base.merge(
        confirmation,
        left_on="confirmation_event_id",
        right_on="event_id",
        how="left",
        validate="many_to_one",
        suffixes=("_q1", ""),
    )
    if base["event_id"].isna().any():
        missing = sorted(
            set(
                base.loc[
                    base["event_id"].isna(),
                    "confirmation_event_id",
                ].astype(str)
            )
        )
        raise ValueError(f"missing confirmation events: {missing[:5]}")

    base["remaining_ratio_at_confirmation"] = (
        pd.to_numeric(base["remaining_points_at_confirmation"], errors="coerce")
        / pd.to_numeric(base["nominal_run_points"], errors="coerce")
    )

    for outcome in OUTCOMES:
        base[f"{outcome}_indicator"] = base[outcome].map(RESOLVED)

    ordered = [
        "context_id",
        "day_id",
        "side",
        "origin_id",
        "origin_tf",
        "confirmation_event_id",
        "confirmation_event_tf",
        "confirmation_known_at",
        "origin_age_hours_at_0700",
        "consumed_ratio_at_0700",
        "remaining_points_at_0700",
        "remaining_points_at_confirmation",
        "remaining_ratio_at_confirmation",
        "alignment_count_exact",
        "alignment_count_recent_1_tf_bar",
        "alignment_count_recent_2_tf_bars",
        PATH_OUTCOME,
        f"{PATH_OUTCOME}_indicator",
        ORIGIN_OUTCOME,
        f"{ORIGIN_OUTCOME}_indicator",
    ]
    remaining = [column for column in base.columns if column not in ordered]
    return base[ordered + remaining].sort_values(
        ["day_id", "side", "origin_tf", "origin_id"]
    ).reset_index(drop=True)


def _origin_association(
    *,
    frame: pd.DataFrame,
    outcome: str,
    feature: str,
    stratum: str,
) -> dict[str, object]:
    indicator_col = f"{outcome}_indicator"
    resolved = frame[
        frame[indicator_col].notna()
        & pd.to_numeric(frame[feature], errors="coerce").notna()
    ].copy()
    resolved[feature] = pd.to_numeric(resolved[feature], errors="coerce")
    resolved[indicator_col] = pd.to_numeric(
        resolved[indicator_col], errors="coerce"
    )

    target = resolved[resolved[indicator_col] == 1.0][feature]
    point = resolved[resolved[indicator_col] == 0.0][feature]
    target_q = _quantiles(target)
    point_q = _quantiles(point)

    return {
        "outcome": outcome,
        "analysis_level": "ORIGIN_ROW",
        "stratum": stratum,
        "feature": feature,
        "n_rows": len(resolved),
        "n_contexts": int(resolved["context_id"].nunique()) if not resolved.empty else 0,
        "feature_unique_values": int(resolved[feature].nunique(dropna=True)),
        "rho": _spearman(resolved[feature], resolved[indicator_col]),
        "target_first_n": int((resolved[indicator_col] == 1.0).sum()),
        "point_check_first_n": int((resolved[indicator_col] == 0.0).sum()),
        "target_feature_median": target_q["median"],
        "target_feature_q25": target_q["q25"],
        "target_feature_q75": target_q["q75"],
        "point_feature_median": point_q["median"],
        "point_feature_q25": point_q["q25"],
        "point_feature_q75": point_q["q75"],
        "median_resolved_origins_per_context": None,
    }


def _context_association(
    *,
    frame: pd.DataFrame,
    outcome: str,
    feature: str,
) -> dict[str, object]:
    indicator_col = f"{outcome}_indicator"
    resolved = frame[
        frame[indicator_col].notna()
        & pd.to_numeric(frame[feature], errors="coerce").notna()
    ].copy()
    if resolved.empty:
        grouped = pd.DataFrame(
            columns=["context_feature", "context_target_first_fraction", "resolved_origins"]
        )
    else:
        resolved[feature] = pd.to_numeric(resolved[feature], errors="coerce")
        resolved[indicator_col] = pd.to_numeric(
            resolved[indicator_col], errors="coerce"
        )
        grouped = (
            resolved.groupby("context_id", as_index=False)
            .agg(
                context_feature=(feature, "median"),
                context_target_first_fraction=(indicator_col, "mean"),
                resolved_origins=(indicator_col, "size"),
            )
        )

    median_origins = (
        float(grouped["resolved_origins"].median()) if not grouped.empty else None
    )
    return {
        "outcome": outcome,
        "analysis_level": "CONTEXT",
        "stratum": "ALL",
        "feature": feature,
        "n_rows": len(grouped),
        "n_contexts": len(grouped),
        "feature_unique_values": int(
            grouped["context_feature"].nunique(dropna=True)
        )
        if not grouped.empty
        else 0,
        "rho": _spearman(
            grouped.get("context_feature", pd.Series(dtype=float)),
            grouped.get(
                "context_target_first_fraction",
                pd.Series(dtype=float),
            ),
        ),
        "target_first_n": None,
        "point_check_first_n": None,
        "target_feature_median": None,
        "target_feature_q25": None,
        "target_feature_q75": None,
        "point_feature_median": None,
        "point_feature_q25": None,
        "point_feature_q75": None,
        "median_resolved_origins_per_context": median_origins,
    }


def build_associations(feature_events: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    if feature_events.empty:
        return pd.DataFrame()

    for outcome in OUTCOMES:
        for feature in FEATURES:
            rows.append(
                _origin_association(
                    frame=feature_events,
                    outcome=outcome,
                    feature=feature,
                    stratum="ALL",
                )
            )
            rows.append(
                _context_association(
                    frame=feature_events,
                    outcome=outcome,
                    feature=feature,
                )
            )

        for origin_tf in ("H1", "H4"):
            subset = feature_events[
                feature_events["origin_tf"].eq(origin_tf)
            ]
            for feature in ORIGIN_STATE_FEATURES:
                rows.append(
                    _origin_association(
                        frame=subset,
                        outcome=outcome,
                        feature=feature,
                        stratum=origin_tf,
                    )
                )

    return pd.DataFrame(rows)


def build_mtf_count_groups(feature_events: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for outcome in OUTCOMES:
        for feature in ALIGNMENT_FEATURES:
            for value, group in feature_events.groupby(feature, dropna=False):
                counts = group[outcome].value_counts(dropna=False).to_dict()
                target = int(counts.get("TARGET_FIRST", 0))
                point = int(counts.get("POINT_CHECK_FIRST", 0))
                neither = int(counts.get("NEITHER_BEFORE_NEXT_0700", 0))
                ambiguous = int(counts.get("AMBIGUOUS_SAME_BAR", 0))
                resolved = target + point
                rows.append(
                    {
                        "outcome": outcome,
                        "alignment_feature": feature,
                        "alignment_count": (
                            None if pd.isna(value) else float(value)
                        ),
                        "origin_rows": len(group),
                        "contexts": int(group["context_id"].nunique()),
                        "target_first": target,
                        "point_check_first": point,
                        "neither_before_next_0700": neither,
                        "ambiguous_same_bar": ambiguous,
                        "resolved_target_first_fraction": (
                            target / resolved if resolved else None
                        ),
                    }
                )
    return pd.DataFrame(rows)


def _association_summary(associations: pd.DataFrame) -> list[dict[str, object]]:
    selected = associations[
        associations["outcome"].eq(PATH_OUTCOME)
        & associations["stratum"].eq("ALL")
    ].copy()
    records: list[dict[str, object]] = []
    for row in selected.itertuples(index=False):
        records.append(
            {
                "analysis_level": row.analysis_level,
                "feature": row.feature,
                "n": int(row.n_rows),
                "rho": None if pd.isna(row.rho) else float(row.rho),
            }
        )
    return records


def run(
    *,
    q1_events_path: str | Path,
    confirmation_events_path: str | Path,
    output_root: str | Path,
    period_label: str,
) -> dict[str, object]:
    q1 = pd.read_csv(q1_events_path)
    confirmation = pd.read_csv(confirmation_events_path)

    feature_events = build_feature_events(
        q1_events=q1,
        confirmation_events=confirmation,
    )
    associations = build_associations(feature_events)
    mtf_groups = build_mtf_count_groups(feature_events)

    report: dict[str, object] = {
        "research_status": "0700_Q2_CONTINUOUS_MTF_RELATIONSHIP_ONLY",
        "period_label": period_label,
        "primary_variant": PRIMARY_VARIANT,
        "primary_outcome": PATH_OUTCOME,
        "secondary_outcome": ORIGIN_OUTCOME,
        "feature_event_rows": len(feature_events),
        "contexts": (
            int(feature_events["context_id"].nunique())
            if not feature_events.empty
            else 0
        ),
        "origins": (
            int(feature_events["origin_id"].nunique())
            if not feature_events.empty
            else 0
        ),
        "path_outcome_counts": (
            {
                str(key): int(value)
                for key, value in feature_events[PATH_OUTCOME]
                .value_counts(dropna=False)
                .to_dict()
                .items()
            }
            if not feature_events.empty
            else {}
        ),
        "association_preview": _association_summary(associations),
        "guards": [
            "No feature threshold is selected.",
            "Spearman rho is descriptive; no p-value or rho cutoff promotes a rule.",
            "Origin-row and context-level associations are both required.",
            "Recent-1 and recent-2 TF windows remain research representations, not instructor thresholds.",
            "Discovery and replication must use the same frozen code.",
            "No trade P&L, system Win/Loss, expectancy, or broker execution model is computed.",
        ],
    }

    root = Path(output_root)
    root.mkdir(parents=True, exist_ok=True)
    feature_events.to_csv(root / "Q2_FEATURE_EVENTS.csv", index=False)
    associations.to_csv(root / "Q2_ASSOCIATIONS.csv", index=False)
    mtf_groups.to_csv(root / "Q2_MTF_COUNT_GROUPS.csv", index=False)
    (root / "REPORT.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q1-events", required=True)
    parser.add_argument("--confirmations", required=True)
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--period-label", required=True)
    args = parser.parse_args()
    report = run(
        q1_events_path=args.q1_events,
        confirmation_events_path=args.confirmations,
        output_root=args.output_root,
        period_label=args.period_label,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
