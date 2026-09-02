import type { Metadata } from 'next';
import type { Signal } from '@/lib/types';
import { AppShell } from '@/components/AppShell';
import { SignalCard } from '@/components/SignalCard';
import { EmptyState } from '@/components/EmptyState';
import { getSignalHistory } from '@/lib/api';
import { formatTimestamp } from '@/lib/format';

export const dynamic = 'force-dynamic';

export const metadata: Metadata = { title: 'Signal History' };

export default async function SignalHistoryPage() {
  const signals = await getSignalHistory(50);
  const byDate = signals.reduce<Record<string, Signal[]>>((acc, sig) => {
    const day = formatTimestamp(sig.timestamp, { year: 'numeric', month: 'long', day: 'numeric' });
    (acc[day] ??= []).push(sig);
    return acc;
  }, {});

	return (
    <AppShell title="Signal History" freshLabel={`${signals.length} signals`}>
      <div className="space-y-4">
        <p className="px-1 text-xs text-slate-500">
          Every decision logged by the Python engine, newest first。
        </p>
        {signals.length === 0 ? (
          <EmptyState title="No signals recorded" hint="Signals will appear here after the engine runs。" />
        ) : (
          Object.entries(byDate).map(([day, list]) => (
            <section key={day} aria-label={day}>
              <h2 className="px-1 text-xs font-semibold uppercase tracking-wider text-slate-500">{day}</h2>
              <div className="mt-2 grid gap-3 sm:grid-cols-2">
                {list.map((sig) => (
                  <SignalCard key={sig.id} signal={sig} />
                ))}
              </div>
            </section>
          ))
        )}
      </div>
    </AppShell>
  );
}