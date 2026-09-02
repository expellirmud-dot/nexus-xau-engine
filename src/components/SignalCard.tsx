import Link from 'next/link';
import type { Signal } from '@/lib/types';
import { formatPrice } from '@/lib/format';
import { SideBadge } from './SideBadge';
import { ConfidenceBadge } from './ConfidenceBadge';

export function SignalCard({ signal }: { signal: Signal }) {
  return (
    <Link
      href={`/signals/${signal.id}`}
      className="block rounded-2xl border border-white/10 bg-white/[0.03] p-4 transition-colors hover:border-cyan-400/30 hover:bg-white/[0.05] active:scale-[0.99]"
    >
      <div className="flex items-center justify-between gap-2">
        <div className="flex items-center gap-2">
          <SideBadge side={signal.side} size="sm" />
          <span className="text-xs text-slate-400">{signal.timeframe ?? '—'}</span>
        </div>
        <ConfidenceBadge status={signal.confidence_status} />
      </div>
      <div className="mt-3 grid grid-cols-3 gap-2 text-sm">
        <div>
          <div className="text-xs text-slate-500">ENTRY</div>
          <div className="font-mono text-slate-200">{formatPrice(signal.entry)}</div>
        </div>
        <div>
          <div className="text-xs text-slate-500">SL</div>
          <div className="font-mono text-rose-300">{formatPrice(signal.sl)}</div>
        </div>
        <div>
          <div className="text-xs text-slate-500">TP</div>
          <div className="font-mono text-emerald-300">{formatPrice(signal.tp)}</div>
        </div>
      </div>
      {signal.setup && (
        <div className="mt-2 text-xs text-slate-400">
          <span className="text-slate-500">Setup </span>{signal.setup}
        </div>
      )}
    </Link>
  );
}