-- Nexus XAU Engine - initial schema
-- Mirrors src/lib/types.ts (snake_case columns) as authored by the Python engine.
-- Web app reads via RLS-protected anon clients; engine writes via service-role backend.

-- =====================================================================
-- signals
-- =====================================================================
create table if not exists public.signals (
  id uuid primary key default gen_random_uuid(),
  timestamp timestamptz not null default now(),
  side text not null,
  status text not null,
  symbol text,
  setup text,
  timeframe text,
  entry numeric,
  sl numeric,
  tp numeric,
  confidence_status text not null default 'NEED_HUMAN_CONFIRM',
  reason_json jsonb not null default '{}'::jsonb,
  rule_version text,
  created_at timestamptz not null default now()
);

-- =====================================================================
-- engine_events
-- =====================================================================
create table if not exists public.engine_events (
  id uuid primary key default gen_random_uuid(),
  signal_id uuid references public.signals(id) on delete cascade,
  timestamp timestamptz not null default now(),
  event_type text not null,
  symbol text,
  timeframe text,
  detector text,
  decision text,
  reason_json jsonb not null default '{}'::jsonb,
  rule_version text
);

-- =====================================================================
-- engine_status
-- =====================================================================
create table if not exists public.engine_status (
  engine_id text primary key,
  status text not null,
  last_heartbeat timestamptz,
  last_market_data timestamptz,
  engine_version text,
  rule_version text,
  updated_at timestamptz not null default now()
);

-- =====================================================================
-- Indexes
-- =====================================================================
-- signals: dashboard orders by timestamp desc; filters by side/confidence; symbol drill-down.

create index if not exists signals_timestamp_idx on public.signals (timestamp desc);
create index if not exists signals_side_idx on public.signals (side);
create index if not exists signals_symbol_timestamp_idx on public.signals (symbol, timestamp desc);
create index if not exists signals_confidence_status_idx on public.signals (confidence_status);

-- engine_events: join by signal; recent-events feed;; event-type + symbol filters.
 
create index if not exists engine_events_signal_id_idx on public.engine_events (signal_id);
create index if not exists engine_events_timestamp_idx on public.engine_events (timestamp desc);
create index if not exists engine_events_event_type_idx on public.engine_events (event_type);
create index if not exists engine_events_symbol_timestamp_idx on public.engine_events (symbol, timestamp desc);

-- =====================================================================
-- Row Level Security
-- =====================================================================
alter table public.signals enable row level security;
alter table public.engine_events enable row level security;
alter table public.engine_status enable row level security;

-- TEMPORARY smoke-test read policies (SELECT only). Smoke-testing the dashboard
-- against a fresh project requires anon + authenticated SELECT. Tighten before production
-- (e.g. authenticated-only or a dedicated reader role) - these are intentionally broad.


 
drop policy if exists "signals_anon_select_smoke" on public.signals;
create policy "signals_anon_select_smoke" on public.signals
  for select to anon, authenticated using (true);
   
drop policy if exists "engine_events_anon_select_smoke" on public.engine_events;
create policy "engine_events_anon_select_smoke" on public.engine_events
  for select to anon, authenticated using (true);

drop policy if exists "engine_status_anon_select_smoke" on public.engine_status;
create policy "engine_status_anon_select_smoke" on public.engine_status
  for select to anon, authenticated using (true);