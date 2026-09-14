from __future__ import annotations

import time
import tkinter as tk
import webbrowser
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from nexus_xau.data.mt5_collector_dashboard import read_dashboard_status

STATE_BG = {
    "RUNNING": "#153d20",
    "BACKFILLING": "#5a470f",
    "STARTING": "#23415f",
    "STOPPED": "#3a3a3a",
    "BLOCKED": "#6a2e0d",
    "ERROR": "#651b1b",
    "STALE": "#6a2e0d",
    "NO_STATUS_FILE": "#3a3a3a",
}


def summarize_corner(payload: dict[str, Any], now_ms: int | None = None) -> dict[str, str]:
    now_ms = int(time.time() * 1000) if now_ms is None else now_ms
    bid = payload.get("latest_bid")
    ask = payload.get("latest_ask")
    latest_msc = payload.get("latest_committed_tick_time_msc")

    quote = "-"
    spread = "-"
    if bid is not None and ask is not None:
        quote = f"{float(bid):.3f} / {float(ask):.3f}"
        spread = f"{float(ask) - float(bid):.3f}"

    age = "-"
    if latest_msc:
        age = f"{max(0.0, (now_ms - int(latest_msc)) / 1000):.1f}s"

    gaps = payload.get("gap_counts") or {}
    gap_text = "{}" if not gaps else ", ".join(
        f"{key}:{value}" for key, value in sorted(gaps.items())
    )

    raw_state = str(payload.get("state") or "UNKNOWN")
    status_age = "-"
    updated_at = payload.get("updated_at_utc")
    if updated_at:
        try:
            updated_ms = int(
                datetime.fromisoformat(str(updated_at))
                .astimezone(UTC)
                .timestamp()
                * 1000
            )
            age_seconds = max(0.0, (now_ms - updated_ms) / 1000)
            status_age = f"{age_seconds:.1f}s"
            if raw_state in {"RUNNING", "BACKFILLING", "STARTING"} and age_seconds > 15:
                raw_state = "STALE"
        except ValueError:
            status_age = "INVALID"

    return {
        "state": raw_state,
        "symbol": str(payload.get("symbol") or "-"),
        "quote": quote,
        "spread": spread,
        "age": age,
        "status_age": status_age,
        "ticks": str(payload.get("total_ticks", 0)),
        "gaps": gap_text,
        "error": str(payload.get("last_error") or "NONE"),
        "mode": str(payload.get("mode") or "READ_ONLY_DATA_ORDER_SEND_DISABLED"),
    }


class CollectorCorner:
    def __init__(
        self,
        *,
        status_path: str | Path,
        db_path: str | Path,
        dashboard_url: str,
        refresh_ms: int = 1000,
    ) -> None:
        self.status_path = Path(status_path)
        self.db_path = Path(db_path)
        self.dashboard_url = dashboard_url
        self.refresh_ms = refresh_ms

        self.root = tk.Tk()
        self.root.title("NEXUS XAU Collector")
        self.root.attributes("-topmost", True)
        self.root.resizable(False, False)

        self.frame = tk.Frame(self.root, padx=10, pady=8)
        self.frame.pack(fill="both", expand=True)

        self.title_label = tk.Label(
            self.frame,
            text="NEXUS XAU • DATA ONLY",
            font=("Segoe UI", 11, "bold"),
            anchor="w",
        )
        self.title_label.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.state_label = tk.Label(
            self.frame,
            text="STARTING",
            font=("Segoe UI", 15, "bold"),
            anchor="w",
        )
        self.state_label.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(3, 6))

        self.detail_label = tk.Label(
            self.frame,
            text="",
            font=("Segoe UI", 9),
            justify="left",
            anchor="w",
        )
        self.detail_label.grid(row=2, column=0, columnspan=2, sticky="ew")

        self.error_label = tk.Label(
            self.frame,
            text="",
            font=("Segoe UI", 8),
            justify="left",
            anchor="w",
            wraplength=310,
        )
        self.error_label.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(4, 4))

        tk.Button(
            self.frame,
            text="Details",
            command=lambda: webbrowser.open(self.dashboard_url),
            width=9,
        ).grid(row=4, column=0, sticky="w")
        tk.Button(
            self.frame,
            text="Close",
            command=self.root.destroy,
            width=9,
        ).grid(row=4, column=1, sticky="e")

        self.root.update_idletasks()
        self._position_bottom_right()
        self._refresh()

    def _position_bottom_right(self) -> None:
        width = 340
        height = 190
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = max(0, screen_w - width - 18)
        y = max(0, screen_h - height - 58)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _apply_background(self, state: str) -> None:
        bg = STATE_BG.get(state, "#3a3a3a")
        fg = "#ffffff"
        self.frame.configure(bg=bg)
        for label in (
            self.title_label,
            self.state_label,
            self.detail_label,
            self.error_label,
        ):
            label.configure(bg=bg, fg=fg)

    def _refresh(self) -> None:
        try:
            payload = read_dashboard_status(self.status_path, self.db_path)
            view = summarize_corner(payload)
            self._apply_background(view["state"])
            self.state_label.configure(text=view["state"])
            self.detail_label.configure(
                text=(
                    f'{view["symbol"]}   Bid/Ask {view["quote"]}\n'
                    f'Spread {view["spread"]}   Tick age {view["age"]}\n'
                    f'Status age {view["status_age"]}   Ticks {view["ticks"]}\n'
                    f'Gaps {view["gaps"]}'
                )
            )
            self.error_label.configure(
                text=f'Error: {view["error"]}\n{view["mode"]}'
            )
        except Exception as exc:  # noqa: BLE001
            self._apply_background("ERROR")
            self.state_label.configure(text="STATUS READ ERROR")
            self.detail_label.configure(text="")
            self.error_label.configure(text=str(exc))

        self.root.after(self.refresh_ms, self._refresh)

    def run(self) -> None:
        self.root.mainloop()


def run_corner(
    *,
    status_path: str | Path,
    db_path: str | Path,
    dashboard_url: str = "http://127.0.0.1:8765/",
) -> None:
    CollectorCorner(
        status_path=status_path,
        db_path=db_path,
        dashboard_url=dashboard_url,
    ).run()
