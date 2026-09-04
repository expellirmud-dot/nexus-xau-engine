from __future__ import annotations

import argparse
import json
from pathlib import Path


def _pct(value: object) -> str:
    if isinstance(value, (int, float)):
        return f"{float(value) * 100:.2f}%"
    return "n/a"


def _num(value: object) -> str:
    if isinstance(value, (int, float)):
        return f"{float(value):.4f}"
    return "n/a"


def render_closure(summary: dict[str, object]) -> str:
    periods = summary.get("periods", [])
    cross = summary.get("cross_period_by_variant", {})

    lines: list[str] = [
        "# PATH_REMAINING × Daily Frame Side × Graded MTF V2 — Empirical Closure",
        "",
        "Status: GENERATED FROM FROZEN RESULT JSON / RESEARCH ONLY",
        "",
        "## Research question",
        "",
        (
            "Within inherited `PATH_REMAINING` events, after conditioning on Daily Frame "
            "`EXPECTED_SIDE` versus `CROSSED_SIDE`, does increasing same-direction "
            "H1/M30/M15/M5 PAT2-BODY proxy alignment relate to better remaining-run behavior?"
        ),
        "",
        "## Frozen guards",
        "",
        "- Alignment remains graded; no production minimum aligned-TF count is selected.",
        "- PAT2 BODY is a research proxy, not canonical full PA.",
        "- PATH_REMAINING is a research representation, not a proven teacher formula.",
        "- Historical outcome cannot identify the instructor's canonical freshness rule.",
        "- Target-first rates below are not strategy win rate.",
        "- These periods were previously used in project research; this is replication/interaction evidence, not untouched final-holdout confirmation.",
        "",
        "## Cross-period decisions",
        "",
        "| Freshness variant | Cross-period decision | Period states |",
        "| --- | --- | --- |",
    ]

    if isinstance(cross, dict):
        for variant, detail in cross.items():
            if not isinstance(detail, dict):
                continue
            decision = detail.get("decision", "n/a")
            states = detail.get("period_states", [])
            states_text = " / ".join(str(value) for value in states) if isinstance(states, list) else str(states)
            lines.append(f"| `{variant}` | `{decision}` | {states_text} |")

    lines.extend(["", "## Period detail", ""])

    if isinstance(periods, list):
        for period in periods:
            if not isinstance(period, dict):
                continue
            label = str(period.get("label", "UNKNOWN_PERIOD"))
            lines.extend(
                [
                    f"### {label}",
                    "",
                    f"Range: `{period.get('start', 'n/a')}` → `{period.get('end', 'n/a')}`",
                    "",
                    f"M1 source: `{period.get('m1', 'n/a')}`",
                    "",
                    f"Interaction events: `{period.get('interaction_events', 'n/a')}`",
                    "",
                    "Period states:",
                    "",
                ]
            )
            states = period.get("period_states", {})
            if isinstance(states, dict):
                for variant, state in states.items():
                    lines.append(f"- `{variant}` → `{state}`")
            lines.append("")

            report_path = period.get("report")
            if isinstance(report_path, str) and Path(report_path).exists():
                report = json.loads(Path(report_path).read_text(encoding="utf-8"))
                variant_reports = report.get("variant_reports", {})
                if isinstance(variant_reports, dict):
                    for variant, variant_detail in variant_reports.items():
                        if not isinstance(variant_detail, dict):
                            continue
                        lines.extend([f"#### {variant}", ""])
                        sides = variant_detail.get("sides", {})
                        if not isinstance(sides, dict):
                            continue
                        lines.extend(
                            [
                                "| Frame side | State | Events | rho target-first | rho reach | rho MFE | rho MAE |",
                                "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
                            ]
                        )
                        for side_name in ("EXPECTED_SIDE", "CROSSED_SIDE"):
                            side = sides.get(side_name, {})
                            if not isinstance(side, dict):
                                continue
                            relation = side.get("relation", {})
                            if not isinstance(relation, dict):
                                relation = {}
                            lines.append(
                                "| "
                                f"{side_name} | {side.get('relation_state', 'n/a')} | "
                                f"{relation.get('events', 'n/a')} | "
                                f"{_num(relation.get('spearman_alignment_vs_target_first'))} | "
                                f"{_num(relation.get('spearman_alignment_vs_path_remaining_reach'))} | "
                                f"{_num(relation.get('spearman_alignment_vs_fresh_mfe'))} | "
                                f"{_num(relation.get('spearman_alignment_vs_fresh_mae'))} |"
                            )

                        lines.extend(["", "Outcome levels (descriptive only):", ""])
                        for side_name in ("EXPECTED_SIDE", "CROSSED_SIDE"):
                            side = sides.get(side_name, {})
                            if not isinstance(side, dict):
                                continue
                            by_count = side.get("by_alignment_count", {})
                            if not isinstance(by_count, dict):
                                continue
                            lines.append(f"**{side_name}**")
                            lines.append("")
                            lines.append("| Aligned TF count | Events | Target-first | PATH_REMAINING reach | MFE median | MAE median |")
                            lines.append("| ---: | ---: | ---: | ---: | ---: | ---: |")
                            for count, metrics in by_count.items():
                                if not isinstance(metrics, dict):
                                    continue
                                lines.append(
                                    "| "
                                    f"{count} | {metrics.get('events', 'n/a')} | "
                                    f"{_pct(metrics.get('target_first_rate_resolved'))} | "
                                    f"{_pct(metrics.get('path_remaining_reach_rate'))} | "
                                    f"{metrics.get('fresh_mfe_median', 'n/a')} | "
                                    f"{metrics.get('fresh_mae_median', 'n/a')} |"
                                )
                            lines.append("")

    lines.extend(
        [
            "## Interpretation discipline",
            "",
            "The cross-period decision above is copied from the frozen batch decision rule. "
            "This document does not upgrade evidence provenance, choose a freshness variant as canonical, "
            "or convert any historical relationship into a production entry threshold.",
            "",
        ]
    )
    return "\n".join(lines)


def render_from_summary(*, summary_path: str | Path, output_path: str | Path) -> Path:
    source = Path(summary_path)
    summary = json.loads(source.read_text(encoding="utf-8"))
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_closure(summary), encoding="utf-8")
    return target


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    target = render_from_summary(summary_path=args.summary, output_path=args.out)
    print(f"Closure markdown: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
