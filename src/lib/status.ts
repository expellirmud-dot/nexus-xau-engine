import type { ConfidenceStatus, EngineState, SignalDecision, SignalSide } from './types';

export const SIDE_LABEL: Record<SignalSide, string> = {
  BUY: 'BUY',
  SELL: 'SELL',
  WAIT: 'WAIT',
};

export const SIDE_CHIP: Record<SignalSide, string> = {
  BUY: 'bg-emerald-500/15 text-emerald-300 border-emerald-400/30',
  SELL: 'bg-rose-500/15 text-rose-300 border-rose-400/30',
  WAIT:'bg-amber-500/15 text-amber-200 border-amber-400/30',
};

export const DECISION_LABEL: Record<SignalDecision, string> = {
  TAKE: 'TAKE',
  WAIT: 'WAIT',
  REJECT: 'REJECT',
};

export const CONFIDENCE_MAP: Record<ConfidenceStatus, { label: string; classes: string }> = {
  CONFIRMED: { label: 'CONFIRMED', classes: 'bg-emerald-500/15 text-emerald-300 border-emerald-400/40' },
	NEED_HUMAN_CONFIRM: { label: 'NEED HUMAN CONFIRM', classes: 'bg-amber-500/15 text-amber-200 border-amber-400/40' },
	REJECTED: { label: 'REJECTED', classes: 'bg-rose-500/15 text-rose-300 border-rose-400/40' },
};

export const ENGINE_STATE_MAP: Record<EngineState, { label: string; classes: string }> = {
  online: { label: 'ONLINE', classes: 'bg-emerald-500/15 text-emerald-300 border-emerald-400/40' },
	offline: { label: 'OFFLINE', classes: 'bg-rose-500/15 text-rose-300 border-rose-400/40' },
	degraded: { label: 'DEGRADED', classes: 'bg-amber-500/15 text-amber-200 border-amber-400/40' },
};

export function humanDecision(status: SignalDecision): string {
  switch (status) {
		case 'TAKE': return 'TAKE';
		case 'REJECT': return 'REJECT';
		case 'WAIT': return 'WAIT';
		 default: return status;
	}
}