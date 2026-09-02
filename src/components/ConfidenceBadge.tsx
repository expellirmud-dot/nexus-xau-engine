import type { ConfidenceStatus } from '@/lib/types';
import { CONFIDENCE_MAP } from '@/lib/status';

export function ConfidenceBadge({ status }: { status: ConfidenceStatus }) {
  const map = CONFIDENCE_MAP[status] ?? CONFIDENCE_MAP.NEED_HUMAN_CONFIRM;
	return (
    <span className={`inline-flex items-center rounded-md border px-2 py-0.5 text-xs font-medium tracking-wide ${map.classes}`}>
      {map.label}
    </span>
  );
}