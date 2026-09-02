import type { Metadata } from 'next';
import { AppShell } from '@/components/AppShell';
import { StatusDot } from '@/components/StatusDot';
import { EmptyState } from '@/components/EmptyState';
import { getEngineStatus, getRecentEvents } from '@/lib/api';
import { freshnessLabel, formatTimestamp, timeAgo } from '@/lib/format';
import {
  ENGINE_HEARTBEAT_MAX_AGE_MS,
  ENGINE_MARKET_DATA_MAX_AGE_MS,
} from '@/lib/types';

export const dynamic = 'force-dynamic';

export const metadata: Metadata = { title: 'System Status' };

function Row({ label, value, tone = 'default' }: { label: string; value: string; tone?: 'default' | 'ok' | 'warn' | 'bad' }) {
  const toneClass =
    tone === 'ok' ? 'text-emerald-300'
    : tone === 'warn' ? 'text-amber-300'
    : tone === 'bad' ? 'text-rose-300'
    : 'text-slate-200';
	return (
    <div className="flex items-center justify-between gap-3 rounded-xl border border-white/5 bg-white/[0.02] px-3 py-2.5 text-xs">
      <span className="text-slate-500">{label}</span>
      <span className={`font-mono text-right ${toneClass}`}>{value}</span>
    </div>
  );
}

export default async function SystemStatusPage() {
  const [status, events] = await Promise.all([getEngineStatus(), getRecentEvents(10)]);
  const generatedAt = new Date().toISOString();

	const heartbeatTone: 'ok' | 'bad' = status?.last_heartbeat
    ? (freshnessLabel(status.last_heartbeat, ENGINE_HEARTBEAT_MAX_AGE_MS).startsWith('live') ? 'ok' : 'bad')
    : 'bad';
	const marketTone: 'ok' | 'warn' = status?.last_market_data
    ? (freshnessLabel(status.last_market_data, ENGINE_MARKET_DATA_MAX_AGE_MS).startsWith('live') ? 'ok' : 'warn')
    : 'warn';
	const engineOnline = status?.status === 'online';
	const dotColor = engineOnline ? 'bg-emerald-400' : status?.status === 'degraded' ? 'bg-amber-400' : 'bg-rose-400';

	return (
    <AppShell title="System Status" freshLabel={`Updated ${timeAgo(generatedAt)}`}>
      <div className="space-y-4">
        <section aria-label="Engine connectivity" className="rounded-3xl border border-white/10 bg-white/[0.03] p-5">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-semibold text-slate-200">Engine</h2>
            <StatusDot color={dotColor} pulse={engineOnline} />
          </div>
          <div className="mt-4 space-y-2">
            <Row label="Status" value={status ? status.status : 'unknown'} tone={engineOnline ? 'ok' : 'bad'} />
            <Row label="Heartbeat" value={status ? freshnessLabel(status.last_heartbeat, ENGINE_HEARTBEAT_MAX_AGE_MS) : 'no data'} tone={heartbeatTone} />
            <Row label="Market data" value={status ? freshnessLabel(status.last_market_data, ENGINE_MARKET_DATA_MAX_AGE_MS) : 'no data'} tone={marketTone} />
            {status?.engine_version && <Row label="Engine version" value={status.engine_version} />}
            {status?.rule_version && <Row label="Rule version" value={status.rule_version} />}
            <Row label="Status record id" value={status ? status.engine_id : '—'} />
          </div>
        </section>

        <section aria-label="Data source">
          <h2 className="px-1 text-sm font-semibold text-slate-200">Data source</h2>
          <div className="mt-2 rounded-2xl border border-white/10 bg-white/[0.02] p-4 text-xs text-slate-400">
            <p>All data displayed here is read directly from Supabase, written exclusively by the Python trading engine。</p>
            <p className="mt-2">This app performs no trading, does not compute signals, and never invents rules — it only renders what the engine published。</p>
          </div>
        </section>

        <section aria-label="Recent engine events">
          <div className="flex items-center justify-between px-1">
            <h2 className="text-sm font-semibold text-slate-200">Recent events</h2>
            <span className="text-xs text-slate-500">{events.length} logged</span>
          </div>
          {events.length >  0 ? (
            <div className="mt-2 space-y-2">
              {events.map((ev) => (
                <div key={ev.id} className="flex items-center justify-between gap-3 rounded-xl border border-white/5 bg-white/[0.02] px-3 py-2.5 text-xs">
                  <div className="min-w-0">
                    <span className="font-medium text-slate-300">{ev.event_type}</span>
                    {ev.symbol && <span className="ml-2 text-slate-500">{ev.symbol}</span>}
                    {ev.detector && <span className="ml-2 text-cyan-200/70">{ev.detector}</span>}
                  </div>
                  <span className="shrink-0 font-mono text-slate-500">{formatTimestamp(ev.timestamp)}</span>
                </div>
              ))}
            </div>
          ) : (
            <EmptyState title="No events recorded" hint="Engine activity appears here once running。" />
          )}
        </section>
      </div>
    </AppShell>
  );
}