import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { AppShell } from '@/components/AppShell';
import { SideBadge } from '@/components/SideBadge';
import { ConfidenceBadge } from '@/components/ConfidenceBadge';
import { ReasonViewer } from '@/components/ReasonViewer';
import { PriceField } from '@/components/PriceField';
import { EmptyState } from '@/components/EmptyState';
import { getSignalById } from '@/lib/api';
import { formatPrice, formatTimestamp, timeAgo } from '@/lib/format';

export const dynamic = 'force-dynamic';

export const metadata: Metadata = { title: 'Signal Detail' };

export default async function SignalDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const signal = await getSignalById(id);
	if (!signal) notFound();

  const decisionColor =
    signal.status === 'TAKE' ? 'text-emerald-300 border-emerald-400/30 bg-emerald-500/10'
    : signal.status === 'REJECT' ? 'text-rose-300 border-rose-400/30 bg-rose-500/10'
    : 'text-amber-200 border-amber-400/30 bg-amber-500/10';

	return (
    <AppShell title="Signal Detail" freshLabel={timeAgo(signal.timestamp)}>
      <div className="space-y-4">
        <Link href="/signals" className="inline-flex items-center gap-1 text-xs text-slate-500 hover:text-slate-300">
          ← Back to signals
        </Link>

        <section className="rounded-3xl border border-white/10 bg-white/[0.03] p-5">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <div className="flex items-center gap-2">
              <SideBadge side={signal.side} />
              <span className="font-mono text-lg font-semibold text-slate-100">{signal.symbol}</span>
            </div>
            <ConfidenceBadge status={signal.confidence_status} />
          </div>
          <div className="mt-4 grid grid-cols-2 gap-2 sm:grid-cols-4">
            <PriceField label="ENTRY" value={formatPrice(signal.entry)} />
            <PriceField label="SL" value={formatPrice(signal.sl)} tone="sell" />
            <PriceField label="TP" value={formatPrice(signal.tp)} tone="buy" />
            <PriceField label="TIMEFRAME" value={signal.timeframe ?? '—'} />
          </div>
          <div className="mt-3 flex items-center justify-between text-xs text-slate-500">
            <span className={`rounded-md border px-2 py-0.5 font-semibold ${decisionColor}`}>
              {signal.status}
            </span>
            <span>Rule {signal.rule_version ?? '—'}</span>
          </div>
        </section>

        <section aria-label="Engine reason">
          <h2 className="px-1 text-sm font-semibold text-slate-200">Engine reason</h2>
          <div className="mt-2">
            <ReasonViewer reason={signal.reason_json} />
          </div>
        </section>

        <section aria-label="Event timeline">
          <h2 className="px-1 text-sm font-semibold text-slate-200">Event timeline</h2>
          {signal.events.length > 0 ? (
            <div className="mt-2 space-y-2">
              {signal.events.map((ev) => (
                <div key={ev.id} className="rounded-xl border border-white/5 bg-white/[0.02] px-3 py-2.5 text-xs">
                  <div className="flex items-center justify-between gap-2">
                    <span className="font-medium text-slate-300">{ev.event_type}</span>
                    <span className="font-mono text-slate-500">{formatTimestamp(ev.timestamp)}</span>
                  </div>
                  {ev.decision && <div className="mt-1 text-slate-400">Decision: {ev.decision}</div>}
                  {ev.detector && <div className="mt-0.5 text-slate-500">Detector: {ev.detector}</div>}
                </div>
              ))}
            </div>
          ) : (
            <EmptyState title="No linked events" hint="The engine did not log sub-events for this signal。" />
          )}
        </section>
      </div>
    </AppShell>
  );
}