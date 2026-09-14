from __future__ import annotations

import json
import sqlite3
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

DASHBOARD_HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>NEXUS XAU Collector Status</title>
<style>
body { font-family: system-ui, sans-serif; margin: 2rem; background: #111; color: #eee; }
main { max-width: 880px; margin: auto; }
h1 { margin-bottom: .2rem; }
.mode { font-weight: 700; padding: .6rem .8rem; border: 1px solid #888; display: inline-block; }
.grid { display: grid; grid-template-columns: repeat(auto-fit,minmax(220px,1fr)); gap: .8rem; margin-top: 1rem; }
.card { border: 1px solid #555; border-radius: 10px; padding: 1rem; }
.label { opacity: .7; font-size: .85rem; }
.value { font-size: 1.25rem; word-break: break-word; }
.error { white-space: pre-wrap; }
small { opacity: .65; }
</style>
</head>
<body>
<main>
<h1>NEXUS XAU Data Collector</h1>
<div id="mode" class="mode">loading...</div>
<div class="grid">
  <div class="card"><div class="label">Collector</div><div id="state" class="value">-</div></div>
  <div class="card"><div class="label">Symbol</div><div id="symbol" class="value">-</div></div>
  <div class="card"><div class="label">Bid / Ask</div><div id="quote" class="value">-</div></div>
  <div class="card"><div class="label">Spread</div><div id="spread" class="value">-</div></div>
  <div class="card"><div class="label">Latest tick UTC</div><div id="tick" class="value">-</div></div>
  <div class="card"><div class="label">Tick age</div><div id="age" class="value">-</div></div>
  <div class="card"><div class="label">Ticks in DB</div><div id="total" class="value">-</div></div>
  <div class="card"><div class="label">This session</div><div id="session" class="value">-</div></div>
  <div class="card"><div class="label">Gaps</div><div id="gaps" class="value">-</div></div>
  <div class="card"><div class="label">Last commit UTC</div><div id="commit" class="value">-</div></div>
  <div class="card"><div class="label">Source</div><div id="source" class="value">-</div></div>
  <div class="card"><div class="label">Last error</div><div id="error" class="value error">-</div></div>
</div>
<p><small>Local read-only observability surface. No trading/execution controls.</small></p>
</main>
<script>
function fmtTick(ms) {
  if (!ms) return "-";
  return new Date(ms).toISOString();
}
function set(id, value) {
  document.getElementById(id).textContent = value ?? "-";
}
async function refresh() {
  try {
    const response = await fetch("/api/status", {cache: "no-store"});
    const s = await response.json();
    set("mode", s.mode);
    set("state", s.state);
    set("symbol", s.symbol);
    const bid = s.latest_bid;
    const ask = s.latest_ask;
    set("quote", bid == null || ask == null ? "-" : bid + " / " + ask);
    set("spread", bid == null || ask == null ? "-" : (ask - bid).toFixed(3));
    set("tick", fmtTick(s.latest_committed_tick_time_msc));
    if (s.latest_committed_tick_time_msc) {
      set("age", ((Date.now() - s.latest_committed_tick_time_msc) / 1000).toFixed(1) + " s");
    } else {
      set("age", "-");
    }
    set("total", s.total_ticks);
    set("session", s.rows_committed_session);
    set("gaps", JSON.stringify(s.gap_counts || {}));
    set("commit", s.last_successful_commit_utc);
    set("source", s.source_identity ? s.source_identity.slice(0, 16) + "…" : "-");
    set("error", s.last_error || "NONE");
  } catch (err) {
    set("state", "DASHBOARD_READ_ERROR");
    set("error", String(err));
  }
}
refresh();
setInterval(refresh, 1000);
</script>
</body>
</html>
"""


def read_dashboard_status(
    status_path: str | Path,
    db_path: str | Path,
) -> dict[str, Any]:
    status_file = Path(status_path)
    if status_file.exists():
        payload = json.loads(status_file.read_text(encoding="utf-8"))
    else:
        payload = {
            "state": "NO_STATUS_FILE",
            "mode": "READ_ONLY_DATA_ORDER_SEND_DISABLED",
            "last_error": None,
        }

    database = Path(db_path)
    total_ticks = 0
    if database.exists():
        uri = database.resolve().as_uri() + "?mode=ro"
        conn = sqlite3.connect(uri, uri=True)
        try:
            row = conn.execute("SELECT COUNT(*) FROM ticks").fetchone()
            total_ticks = 0 if row is None else int(row[0])
        finally:
            conn.close()

    payload["total_ticks"] = total_ticks
    payload["dashboard_read_only"] = True
    return payload


def make_handler(
    status_path: str | Path,
    db_path: str | Path,
) -> type[BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        def _headers(self, content_type: str) -> None:
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", content_type)
            self.send_header("Cache-Control", "no-store")
            self.end_headers()

        def do_GET(self) -> None:
            if self.path == "/":
                self._headers("text/html; charset=utf-8")
                self.wfile.write(DASHBOARD_HTML.encode("utf-8"))
                return

            if self.path == "/api/status":
                self._headers("application/json; charset=utf-8")
                payload = read_dashboard_status(status_path, db_path)
                self.wfile.write(
                    (json.dumps(payload, ensure_ascii=False) + "\n").encode("utf-8")
                )
                return

            self.send_error(HTTPStatus.NOT_FOUND)

        def log_message(self, format: str, *args: Any) -> None:
            return

    return Handler


def serve_dashboard(
    *,
    host: str,
    port: int,
    status_path: str | Path,
    db_path: str | Path,
) -> None:
    if host not in {"127.0.0.1", "localhost"}:
        raise ValueError("dashboard V0.1 is local-only; bind to 127.0.0.1/localhost")
    server = ThreadingHTTPServer((host, port), make_handler(status_path, db_path))
    server.serve_forever()
