export function PriceField({ label, value, tone = 'default' }: { label: string; value: string; tone?: 'default' | 'buy' | 'sell' }) {
  const toneClass = tone === 'buy' ? 'text-emerald-300' : tone === 'sell' ? 'text-rose-300' : 'text-slate-100';
  return (
    <div className="flex items-center justify-between rounded-xl border border-white/5 bg-white/[0.02] px-3 py-2.5">
      <span className="text-xs text-slate-500">{label}</span>
      <span className={`font-mono text-sm font-medium ${toneClass}`}>{value}</span>
    </div>
  );
}