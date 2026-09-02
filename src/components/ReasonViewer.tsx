/**
 * Renders the engine's structured reason_json without interpreting trading
 * logic — it displays exactly what the Python engine sent。
 */

function renderValue(value: unknown, depth: number): React.ReactNode {
  if (value === null || value === undefined) return <span className="text-slate-500">—</span>;
  if (typeof value === 'boolean') return <span className="font-mono text-cyan-200">{value ? 'true' : 'false'}</span>;
  if (typeof value === 'number') return <span className="font-mono text-cyan-200">{value}</span>;
  if (typeof value === 'string') return <span className="text-slate-200">{value}</span>;
  if (Array.isArray(value)) {
    return (
      <ul className="mt-1 space-y-1 border-l border-white/10 pl-3">
        {value.map((item, i) => (
          <li key={i}>{renderValue(item, depth +  1)}</li>
        ))}
      </ul>
    );
  }
	if (typeof value === 'object') {
    return (
      <div className="mt-1 space-y-1.5 border-l border-white/10 pl-3">
        {Object.entries(value as Record<string, unknown>).map(([k, v]) => (
          <div key={k}>
            <span className="text-xs font-medium text-slate-400">{formatKey(k)}</span>
            <div>{renderValue(v, depth + 1)}</div>
          </div>
        ))}
      </div>
    );
  }
	return <span>{String(value)}</span>;
}

function formatKey(k: string): string {
  return k.replace(/_/g, ' ');
}

export function ReasonViewer({ reason }: { reason: Record<string, unknown> }) {
  const entries = Object.entries(reason);
	if (entries.length === 0) {
    return <div className="text-xs text-slate-500">No reason data provided by engine。</div>;
  }
	return (
    <div className="space-y-2 rounded-2xl border border-white/10 bg-white/[0.02] p-4 text-sm">
      {entries.map(([k, v]) => (
        <div key={k}>
          <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">{formatKey(k)}</span>
          <div className="mt-0.5">{renderValue(v, 0)}</div>
        </div>
      ))}
    </div>
  );
}