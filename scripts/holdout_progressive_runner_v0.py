from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from nexus_xau.research.holdout_progressive_runner_v0 import (
    DEFAULT_ACTIVATION_LOCK,
    append_progressive_checkpoint,
    holdout_runner_status,
)


def _now(value: str | None) -> datetime:
    if value is None:
        return datetime.now().astimezone()
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError("--now must be timezone-aware")
    return parsed


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fail-closed V0.1 holdout progressive-reveal runner."
    )
    parser.add_argument(
        "--activation-lock",
        default=str(DEFAULT_ACTIVATION_LOCK),
        help="Tracked activation-lock JSON path.",
    )
    parser.add_argument(
        "--now",
        help="Timezone-aware ISO clock override for deterministic validation/tests.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("status", help="Validate lock/ledger and show activation state.")

    append = sub.add_parser(
        "append-packet",
        help="Validate and append one blinded Stage-B checkpoint packet.",
    )
    append.add_argument("packet", help="JSON packet path.")

    args = parser.parse_args()
    now = _now(args.now)

    if args.command == "status":
        result = holdout_runner_status(
            activation_lock_path=args.activation_lock,
            now=now,
        )
    else:
        raw = json.loads(Path(args.packet).read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            raise ValueError("packet JSON must be an object")
        result = append_progressive_checkpoint(
            activation_lock_path=args.activation_lock,
            now=now,
            checkpoint_time=raw.get("checkpoint_time"),
            visible_data_until=raw.get("visible_data_until"),
            record_type=raw.get("record_type", ""),
            payload=raw.get("payload", {}),
        )

    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
