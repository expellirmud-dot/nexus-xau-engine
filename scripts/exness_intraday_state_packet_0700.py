from __future__ import annotations

import argparse
import hashlib
import json
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from urllib.request import Request, urlopen

import pandas as pd

from nexus_xau.data.exness_tick_archive import USER_AGENT, fetch_directory
from nexus_xau.data.exness_tick_archive_download import VALIDATOR_VERSION, validate_zip
from nexus_xau.replay.archive_window import _read_month_window
from nexus_xau.replay.tick_bars import build_archive_bid_m1
from nexus_xau.research.state_packet_0700 import (
    INIT_OPERATIONAL_EXPLICIT_EPOCH,
    StatePacketError,
    build_state_packet,
    write_state_packet_json,
)

BASE_URL = "https://ticks.ex2archive.com/ticks"
SOURCE_FAMILY = "EXNESS_XAUUSDM_INTRADAY_DAILY_ARCHIVE"
BOUNDARY_MINUTE_NOT_AVAILABLE = "BOUNDARY_MINUTE_NOT_AVAILABLE"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _utc(value: str | pd.Timestamp) -> pd.Timestamp:
    timestamp = pd.Timestamp(value)
    if timestamp.tz is None:
        raise ValueError("timestamp must be timezone-aware")
    return timestamp.tz_convert("UTC")


def _iter_days(start: date, end: date) -> list[date]:
    days: list[date] = []
    current = start
    while current <= end:
        days.append(current)
        current += timedelta(days=1)
    return days


def _month_directory_url(symbol: str, year: int, month: int) -> str:
    return f"{BASE_URL}/{symbol}/{year:04d}/{month:02d}/"


def _day_directory_url(symbol: str, day: date) -> str:
    return f"{BASE_URL}/{symbol}/{day.year:04d}/{day.month:02d}/{day.day:02d}/"


def _daily_filename(symbol: str, day: date) -> str:
    return f"Exness_{symbol}_{day.year:04d}_{day.month:02d}_{day.day:02d}.zip"


def _download(url: str, target: Path, *, timeout_seconds: float) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=timeout_seconds) as response:
        temporary = target.with_suffix(target.suffix + ".tmp")
        with temporary.open("wb") as handle:
            for chunk in iter(lambda: response.read(1024 * 1024), b""):
                handle.write(chunk)
        temporary.replace(target)


def _discover_days(
    *,
    symbol: str,
    start: date,
    end: date,
    timeout_seconds: float,
) -> dict[date, dict[str, object]]:
    discovered: dict[date, dict[str, object]] = {}
    by_month: dict[tuple[int, int], list[date]] = {}
    for day in _iter_days(start, end):
        by_month.setdefault((day.year, day.month), []).append(day)

    for (year, month), days in by_month.items():
        entries = fetch_directory(
            _month_directory_url(symbol, year, month),
            timeout_seconds=timeout_seconds,
        )
        directory_names = {
            entry.name: entry
            for entry in entries
            if entry.type == "directory"
        }
        for day in days:
            day_key = f"{day.day:02d}"
            if day_key not in directory_names:
                continue
            day_entries = fetch_directory(
                _day_directory_url(symbol, day),
                timeout_seconds=timeout_seconds,
            )
            expected = _daily_filename(symbol, day)
            match = next(
                (
                    entry
                    for entry in day_entries
                    if entry.type == "file" and entry.name == expected
                ),
                None,
            )
            if match is None:
                continue
            discovered[day] = {
                "url": f"{_day_directory_url(symbol, day)}{expected}",
                "size": match.size,
                "mtime": match.mtime,
                "filename": expected,
            }
    return discovered


def acquire_daily_snapshots(
    *,
    symbol: str,
    start: date,
    end: date,
    output_root: Path,
    timeout_seconds: float,
) -> list[dict[str, object]]:
    discovered = _discover_days(
        symbol=symbol,
        start=start,
        end=end,
        timeout_seconds=timeout_seconds,
    )
    snapshots: list[dict[str, object]] = []
    for day in _iter_days(start, end):
        remote = discovered.get(day)
        if remote is None:
            snapshots.append(
                {
                    "date": day.isoformat(),
                    "status": "REMOTE_DAY_NOT_AVAILABLE",
                }
            )
            continue

        target = (
            output_root
            / symbol
            / f"{day.year:04d}"
            / f"{day.month:02d}"
            / f"{day.day:02d}"
            / str(remote["filename"])
        )
        expected_size = remote["size"]
        needs_download = (
            not target.exists()
            or expected_size is None
            or target.stat().st_size != int(expected_size)
        )
        if needs_download:
            _download(
                str(remote["url"]),
                target,
                timeout_seconds=timeout_seconds,
            )

        validation = validate_zip(target, symbol=symbol)
        snapshots.append(
            {
                "date": day.isoformat(),
                "status": "VALIDATED",
                "url": remote["url"],
                "remote_size": expected_size,
                "remote_mtime": remote["mtime"],
                "local_path": str(target),
                "sha256": _sha256(target),
                "validator_version": VALIDATOR_VERSION,
                **validation,
            }
        )
    return snapshots


def build_intraday_state_packet(
    *,
    symbol: str,
    epoch: pd.Timestamp,
    checkpoint: pd.Timestamp,
    snapshots: list[dict[str, object]],
    generated_at: pd.Timestamp | None = None,
) -> dict[str, object]:
    window_end = checkpoint + pd.Timedelta(1, unit="min")
    checkpoint_day = checkpoint.date().isoformat()
    boundary_snapshot = next(
        (
            snapshot
            for snapshot in snapshots
            if snapshot.get("date") == checkpoint_day
            and snapshot.get("status") == "VALIDATED"
        ),
        None,
    )
    if boundary_snapshot is None:
        raise StatePacketError(
            f"{BOUNDARY_MINUTE_NOT_AVAILABLE}: checkpoint day snapshot not available"
        )
    first_boundary_tick = boundary_snapshot.get("first_timestamp")
    if first_boundary_tick is None or _utc(str(first_boundary_tick)) >= window_end:
        raise StatePacketError(
            f"{BOUNDARY_MINUTE_NOT_AVAILABLE}: checkpoint minute has no observed tick"
        )

    admitted: list[dict[str, object]] = []
    source_files: list[dict[str, object]] = []

    for snapshot in snapshots:
        if snapshot.get("status") != "VALIDATED":
            continue
        path = Path(str(snapshot["local_path"]))
        sha = str(snapshot["sha256"])
        rows = _read_month_window(
            path=path,
            symbol=symbol,
            year=checkpoint.year,
            month=checkpoint.month,
            sha256=sha,
            start=epoch,
            end=window_end,
        )
        admitted.extend(rows)
        source_files.append(
            {
                "date": snapshot["date"],
                "local_path": str(path),
                "sha256": sha,
                "remote_mtime": snapshot.get("remote_mtime"),
                "first_timestamp": snapshot.get("first_timestamp"),
                "last_timestamp": snapshot.get("last_timestamp"),
            }
        )

    if not admitted:
        raise StatePacketError(
            f"{BOUNDARY_MINUTE_NOT_AVAILABLE}: no admitted Exness ticks"
        )

    ticks = pd.DataFrame(admitted).set_index("timestamp")
    ticks.index = pd.DatetimeIndex(ticks.index)
    ticks = ticks.sort_index(kind="stable")

    m1 = build_archive_bid_m1(
        ticks,
        requested_start=epoch,
        requested_end=window_end,
    )
    if checkpoint not in m1.index:
        latest = m1.index.max().isoformat() if len(m1) else None
        raise StatePacketError(
            f"{BOUNDARY_MINUTE_NOT_AVAILABLE}: checkpoint={checkpoint.isoformat()} "
            f"latest_m1={latest}"
        )

    core = m1[["open", "high", "low", "close"]].copy()
    packet = build_state_packet(
        m1=core,
        checkpoint_at=checkpoint,
        initialization_mode=INIT_OPERATIONAL_EXPLICIT_EPOCH,
        initialization_epoch=epoch,
        source_identity={
            "source_family": SOURCE_FAMILY,
            "symbol": symbol,
            "source_files": source_files,
            "bar_representation": "ARCHIVE_BID_M1_V0.1",
            "feed_boundary": (
                "Exness-branded archive family; not asserted identical to expired "
                "MT5 Trial17 account execution stream."
            ),
        },
        generated_at_utc=generated_at,
    )
    return packet


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Acquire Exness intraday daily archive snapshots and calculate the "
            "operational H4 07:00 state packet."
        )
    )
    parser.add_argument("--symbol", default="XAUUSDm")
    parser.add_argument("--epoch", required=True)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument(
        "--archive-root",
        type=Path,
        default=Path("data/raw/exness_tick_history/intraday_daily"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--acquisition-report",
        type=Path,
        required=True,
    )
    parser.add_argument("--timeout-seconds", type=float, default=60.0)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    epoch = _utc(args.epoch)
    checkpoint = _utc(args.checkpoint)
    snapshots = acquire_daily_snapshots(
        symbol=args.symbol,
        start=epoch.date(),
        end=checkpoint.date(),
        output_root=args.archive_root,
        timeout_seconds=args.timeout_seconds,
    )
    args.acquisition_report.parent.mkdir(parents=True, exist_ok=True)
    args.acquisition_report.write_text(
        json.dumps(
            {
                "schema_version": "EXNESS_INTRADAY_DAILY_ACQUISITION_V0.1",
                "observed_at_utc": datetime.now(UTC).isoformat(),
                "symbol": args.symbol,
                "epoch_utc": epoch.isoformat(),
                "checkpoint_utc": checkpoint.isoformat(),
                "snapshots": snapshots,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    try:
        packet = build_intraday_state_packet(
            symbol=args.symbol,
            epoch=epoch,
            checkpoint=checkpoint,
            snapshots=snapshots,
        )
    except StatePacketError as exc:
        print(
            json.dumps(
                {
                    "status": "BLOCKED",
                    "reason": str(exc),
                    "acquisition_report": str(args.acquisition_report),
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 3

    write_state_packet_json(packet, args.output)
    print(
        json.dumps(
            {
                "status": "CALCULATED",
                "checkpoint_thailand": packet["checkpoint_thailand"],
                "state_0700": packet["state_0700"],
                "post_0700_requirement": packet["post_0700_requirement"],
                "active_origin_count": packet["origin_summary"][
                    "active_origin_count"
                ],
                "output": str(args.output),
                "acquisition_report": str(args.acquisition_report),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
