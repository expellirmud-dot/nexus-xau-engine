from __future__ import annotations

import json
from pathlib import Path

from nexus_xau.research.path_remaining_daily_side_mtf_closure import (
    render_closure,
    render_from_summary,
)


def _summary() -> dict[str, object]:
    return {
        "periods": [
            {
                "label": "P1",
                "start": "2022-09-01",
                "end": "2023-03-31",
                "m1": "data.csv",
                "interaction_events": "events.csv",
                "report": "missing-report.json",
                "period_states": {"EXACT_COMPLETION": "SIDE_CONDITIONAL_SUPPORT"},
            }
        ],
        "cross_period_by_variant": {
            "EXACT_COMPLETION": {
                "period_states": ["SIDE_CONDITIONAL_SUPPORT", "INCONCLUSIVE"],
                "decision": "INCONCLUSIVE",
            }
        },
    }


def test_render_closure_preserves_frozen_decision_and_guards() -> None:
    text = render_closure(_summary())
    assert "`INCONCLUSIVE`" in text
    assert "SIDE_CONDITIONAL_SUPPORT" in text
    assert "no production minimum aligned-TF count" in text
    assert "not strategy win rate" in text


def test_render_from_summary_writes_markdown(tmp_path: Path) -> None:
    summary_path = tmp_path / "summary.json"
    output_path = tmp_path / "closure.md"
    summary_path.write_text(json.dumps(_summary()), encoding="utf-8")

    target = render_from_summary(summary_path=summary_path, output_path=output_path)

    assert target == output_path
    assert output_path.exists()
    assert "Empirical Closure" in output_path.read_text(encoding="utf-8")
