# Nexus XAU Engine Dashboard

Mobile-first Next.js web app / PWA that **displays** the output of the Nexus XAU Python trading engine.

**Display-only.** This app does not trade, does not compute BUY/SELL decisions, does not guess rules, and never writes signals. The Python engine is the single source of truth — the dashboard only reads what the engine publishes (via Supabase).

## Stack

- **Next.js 16** (App Router, React 19, TypeScript, Tailwind CSS v4)
- **Supabase** — the engine writes signals / engine status / events; this app reads them through RLS-protected clients.
- **PWA** — web manifest + safe-area viewport theming (installable on mobile when icons/worker added)

## Environment

Copy `.env.example` → `.env.local`:

| Variable | Client | Purpose |
|---|---|---|
| `NEXT_PUBLIC_SUPABASE_URL` | browser + server | Project URL |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | browser + server | RLS-restricted anon key |
| `SUPABASE_SERVICE_ROLE_KEY` | server-only | Service-role key (only for server-admin routes; never shipped to the browser |

## Routes

| Route | What it shows |
|---|---|
| `/` | Live dashboard — latest signal hero, engine status freshness, recent engine events |
| `/signals` | Signal history grouped by day |
| `/signals/[id]` | Signal detail — entry/SL/TP, engine reason (JSON), linked event timeline |
| `/system` | System status — engine connectivity, heartbeat / market-data freshness, recent events |

## Data flow

```
Python trading engine → Supabase (signals, engine_status, engine_events) → this app (server-side reads) → UI
```

All queries run server-side (`getSignalHistory`, `getEngineStatus`, `getRecentEvents`, `getSignalById` in `src/lib/api.ts`) through RLS-protected Supabase clients. The browser layer never holds a service-role credential.

## Development

```bash
npm install
cp .env.example .env.local  # add real keys
npm run dev
```

```bash
npm run build && npm run start
```

## Layout notes

- Views are server-rendered (dynamic) and refresh on navigation; a `RefreshButton` revalidates the current route in place.
- Freshness thresholds live in `src/lib/types.ts` (`ENGINE_HEARTBEAT_MAX_AGE_MS`, `ENGINE_MARKET_DATA_MAX_AGE_MS`)
- Safe areas: sticky header + bottom nav respect `env(safe-area-inset-bottom)`; theme-color matches the app background for full-bleed PWAs.