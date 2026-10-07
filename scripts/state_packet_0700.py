from __future__ import annotations

import argparse
import json
from pathlib import Path

from nexus_xau.data.csv_loader import load_ohlc_csv
from nexus_xau.research.state_packet_0700 import (
    INIT_OPERATIONAL_EXPLICIT_EPOCH,
    INIT_SOURCE_PURE,
    build_state_packet,
    write_state_packet_json,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Build a deterministic H4 07:00 Asia/Bangkok state packet without "
            "post-checkpoint outcome scoring or order sending."
        )
    )
    parser.add_argument("--input-csv", type=Path, required=True)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--epoch", required=True)
    parser.add_argument(
        "--mode",
        choices=[INIT_SOURCE_PURE, INIT_OPERATIONAL_EXPLICIT_EPOCH],
        required=True,
    )
    parser.add_argument("--source-family", required=True)
    parser.add_argument("--symbol", default="XAUUSDm")
    parser.add_argument("--source-ref")
    parser.add_argument("--source-timezone")
    parser.add_argument("--generated-at")
    parser.add_argument("--output", type=Path, required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    frame = load_ohlc_csv(
        args.input_csv,
        source_timezone=args.source_timezone,
    )
    source_identity = {
        "source_family": args.source_family,
        "symbol": args.symbol,
        "input_csv": str(args.input_csv),
        "source_ref": args.source_ref,
    }
    packet = build_state_packet(
        m1=frame,
        checkpoint_at=args.checkpoint,
        initialization_mode=args.mode,
        initialization_epoch=args.epoch,
        source_identity=source_identity,
        generated_at_utc=args.generated_at,
    )
    output = write_state_packet_json(packet, args.output)
    print(
        json.dumps(
            {
                "packet_version": packet["packet_version"],
                "checkpoint_thailand": packet["checkpoint_thailand"],
                "state_0700": packet["state_0700"],
                "post_0700_requirement": packet["post_0700_requirement"],
                "active_origin_count": packet["origin_summary"]["active_origin_count"],
                "calculation_confidence": packet["calculation_confidence"],
                "output": str(output),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
