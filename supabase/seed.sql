-- Nexus XAU Engine - smoke-test seed data NOT executed against any live DB in
-- this repo; runs on `supabase db reset` local dev and serves as the smoke-test payload
-- for the dashboard. Deterministic ids make reruns idempotent (on conflict do nothing).

insert into public.signals (id, timestamp, side, symbol, status, setup, timeframe, entry, sl, tp, confidence_status, reason_json, rule_version)
values (
  '00000000-0000-4000-8000-000000000001',
  now() - interval '5 minutes',
  'BUY',
    'XAUUSD',
  'TAKE',
  'PAT bounce',
  'M5',
  2678.50,
  2652.10,
  2721.30,
  'CONFIRMED',
  '{"pattern":"PAT","support_resistance":true,"m5_break":true,"confidence":0.81}',
  '0.1.0'
)

on conflict (id) do nothing;

insert into public.engine_events (id, signal_id, timestamp, event_type, symbol, timeframe, detector, decision, reason_json, rule_version)
values (
  '00000000-0000-4000-8000-000000000002',
  '00000000-0000-4000-8000-000000000001',
  now() - interval '4 minutes',
  'signal_taken',
  'XAUUSD',
  'M5',
  'PAT',
  'TAKE',
  '{"confidence":0.81}',
  '0.1.0'
)

on conflict (id) do nothing;

insert into public.engine_status (engine_id, status, last_heartbeat, last_market_data, engine_version, rule_version)
values (
  'engine-1',
  'online',
  now() - interval '30 seconds',
  now() - interval '45 seconds',
  '0.1.0',
  '0.1.0'
)

on conflict (engine_id) do nothing;