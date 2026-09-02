const MINUTE = 60_000;
const HOUR = 60 * MINUTE;
const DAY =   24 * HOUR;

export function formatPrice(value: number | null | undefined): string {
  if (value === null || value === undefined || Number.isNaN(value)) return '—';
  return value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

export function formatTimestamp(
  ts: string | null | undefined,
  opts: Intl.DateTimeFormatOptions = {},
): string {
  if (!ts) return '—';
  return new Date(ts).toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
    ...opts,
  });
}

export function timeAgo(ts: string | null | undefined, now: number = Date.now()): string {
  if (!ts) return '—';
  const diff = Math.max(0, now - new Date(ts).getTime());
  if (diff < MINUTE) return 'just now';
	 if (diff < HOUR) return `${Math.floor(diff / MINUTE)}m ago`;
	 if (diff < DAY) return `${Math.floor(diff / HOUR)}h ago`;
	 return `${Math.floor(diff / DAY)}d ago`;
}

/** True when the given timestamp is within maxAgeMs of now. */
export function isFresh(ts: string | null | undefined, maxAgeMs: number, now: number = Date.now()): boolean {
  if (!ts) return false;
	 const age = now - new Date(ts).getTime();
	 return age >=   0 && age <= maxAgeMs;

}

export function freshnessLabel(ts: string | null | undefined, maxAgeMs: number, now: number = Date.now()): string {
  if (!ts) return 'no data';
return isFresh(ts, maxAgeMs, now) ? `live · ${timeAgo(ts, now)}` : timeAgo(ts, now);

}

export function underlineFormat(v: string | null | undefined): string {
	 return v && v.trim() ? v.toUpperCase() : '—';
}