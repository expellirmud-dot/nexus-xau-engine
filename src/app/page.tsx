import type { Metadata } from 'next';
import Link from 'next/link';
import { AppShell } from '@/components/AppShell';
import { SideBadge } from '@/components/SideBadge';
import { ConfidenceBadge } from '@/components/ConfidenceBadge';
import { StatusDot } from '@/components/StatusDot';
import { EmptyState } from '@/components/EmptyState';
import { PriceField } from '@/components/PriceField';
import { getEngineStatus, getLatestSignal, getRecentEvents } from '@/lib/api';
import { isFresh, formatPrice, freshnessLabel, timeAgo, formatTimestamp } from '@/lib/format';
import {
  ENGINE_HEARTBEAT_MAX_AGE_MS,
  ENGINE_MARKET_DATA_MAX_AGE_MS,
  Signal,
} from '@/lib/types';

export const dynamic = 'force-dynamic';

export const metadata: Metadata = { title: 'Live Dashboard' };

function LatestSignalHero({ signal }: { signal: Signal }) {
  return (
    <Link
      href={`/signals/${signal.id}`}
      className="block rounded-3xl border border-cyan-400/20 bg-gradient-to-br from-cyan-500/10 via-slate-900/60 to-violet-500/10 p-6 transition-transform active:scale-[0.99]"
    >
      <div className="flex items-center justify-between gap-2">
        <SideBadge side={signal.side} size="lg" />
        <ConfidenceBadge status={signal.confidence_status} />
      </div>
      <div className="mt-4 flex items-baseline gap-2">
        <span className="font-mono text-4xl font-bold tracking-tight text-slate-50">
          {signal.symbol}
        </span>
        <span className="text-xs text-slate-500">{signal.timeframe ?? '—'}</span>
      </div>
      <div className="mt-2 flex items-center justify-between">
        <span className="font-mono text-2xl font-semibold text-slate-100">
          {formatPrice(signal.entry)}
        </span>
        <span className="text-xs text-slate-500">{timeAgo(signal.timestamp)}</span>
      </div>
      <div className="mt-4 grid grid-cols-2 gap-2">
        <PriceField label="SL" value={formatPrice(signal.sl)} tone="sell" />
        <PriceField label="TP" value={formatPrice(signal.tp)} tone="buy" />
      </div>
      {signal.setup && (
        <div className="mt-3 text-xs text-slate-400">
          <span className="text-slate-600">Setup · </span>{signal.setup}
        </div>
      )}
    </Link>
  );
}

function EngineStateCard({
  status,
}: {
  status: Awaited<ReturnType<typeof getEngineStatus>>;
}) {
  if (!status) {
    return (
      <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-4">
        <div className="flex items-center justify-between">
          <span className="text-sm font-medium text-slate-300">Engine</span>
          <StatusDot color="bg-slate-500" />
        </div>
        <p className="mt-1 text-xs text-slate-500">No status record from the engine yet.</p>
      </div>
    );
  }
	const heartbeatOk = isFresh(status.last_heartbeat, ENGINE_HEARTBEAT_MAX_AGE_MS);
	const marketOk =isFresh(status.last_market_data, ENGINE_MARKET_DATA_MAX_AGE_MS);
	const color = heartbeatOk ? 'bg-emerald-400' : 'bg-rose-400';
	return (
    <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-4">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-slate-300">Engine status</span>
        <StatusDot color={color} pulse={heartbeatOk} />
      </div>
      <div className="mt-3 space-y-2 text-xs">
        <div className="flex items-center justify-between">
          <span className="text-slate-500">Heartbeat</span>
          <span className={`font-mono ${heartbeatOk ? 'text-emerald-300' : 'text-rose-300'}`}>
            {freshnessLabel(status.last_heartbeat, ENGINE_HEARTBEAT_MAX_AGE_MS)}
          </span>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-slate-500">Market data</span>
          <span className={`font-mono ${marketOk ? 'text-emerald-300' : 'text-amber-300'}`}>
            {freshnessLabel(status.last_market_data, ENGINE_MARKET_DATA_MAX_AGE_MS)}
          </span>
        </div>
        {status.rule_version && (
          <div className="flex items-center justify-between">
            <span className="text-slate-500">Rules</span>
            <span className="font-mono text-slate-300">{status.rule_version}</span>
          </div>
        )}
      </div>
    </div>
  );
}

export default async function LiveDashboardPage() {
  const [latest, status, recentEvents] = await Promise.all([
    getLatestSignal(),
    getEngineStatus(),
    getRecentEvents(6),
  ]);

	return (
    <AppShell title="Nexus XAU Engine" freshLabel={latest ? `Signal ${timeAgo(latest.timestamp)}` : 'Awaiting first signal'}>
      <div className="space-y-4">
        <section aria-label="Latest signal">
          {latest ? <LatestSignalHero signal={latest} /> : (
            <EmptyState
              title="No signals yet"
              hint="When the engine fires a signal, it will appear here instantly."
            />
          )}
        </section>

        <section aria-label="Engine status">
          <EngineStateCard status={status} />
        </section>

        <section aria-label="Recent engine events">
          <div className="flex items-center justify-between px-1">
            <h2 className="text-sm font-semibold text-slate-200">Engine events</h2>
            <Link href="/signals" className="text-xs text-cyan-300 hover:text-cyan-200">Signals →</Link>
          </div>
          {recentEvents.length > 0 ? (
            <div className="space-y-2">
              {recentEvents.map((ev) => (
                <div key={ev.id} className="flex items-center justify-between gap-3 rounded-xl border border-white/5 bg-white/[0.02] px-3 py-2.5 text-xs">
                  <div className="min-w-0">
                    <span className="font-medium text-slate-300">{ev.event_type}</span>
                    {ev.symbol && <span className="ml-2 text-slate-500">{ev.symbol}</span>}
                  </div>
                  <span className="shrink-0 font-mono text-slate-500">{formatTimestamp(ev.timestamp)}</span>
                </div>
              ))}
            </div>
          ) : (
            <EmptyState title="No engine events" hint="Engine activity appears here once running." />
          )}
        </section>
      </div>
    </AppShell>
  );
}