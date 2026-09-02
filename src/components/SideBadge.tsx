import type { SignalSide } from '@/lib/types';
import { SIDE_CHIP, SIDE_LABEL } from '@/lib/status';

export function SideBadge({ side, size = 'md' }: { side: SignalSide; size?: 'sm' | 'md' | 'lg' }) {
  const textSize = size === 'lg' ? 'text-lg px-4 py-1.5' : size === 'sm' ? 'text-xs px-2 py-0.5' : 'text-sm px-3 py-1';
	return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full border font-semibold tracking-wider ${SIDE_CHIP[side]} ${textSize}`}
    >
      {SIDE_LABEL[side]}
    </span>
  );
}