/**
 * Shared domain types.
 *
 * These mirror the Supabase table columns 1:1 (snake_case) as authored
 * by the Python engine. The Python engine is the source of truth — the web app
 * only reads and renders these values and never computes trading decisions.
 */

export type SignalSide = 'BUY' | 'SELL' | 'WAIT';
export type SignalDecision = 'TAKE' | 'WAIT' | 'REJECT';
export type ConfidenceStatus = 'CONFIRMED' | 'NEED_HUMAN_CONFIRM' | 'REJECTED';
export type EngineState = 'online' | 'offline' | 'degraded';

export interface Signal {
  id: string;
  symbol: string;
  /** ISO timestamp of when the engine made this decision. */
  timestamp: string;
  /** Current status shown on the dashboard: BUY / SELL / WAIT. */
  side: SignalSide;
  /** Engine decision for this signal: TAKE / WAIT / REJECT. */
  status: SignalDecision;
  setup: string | null;
  timeframe: string | null;
  entry: number | null;
  sl: number | null;
  tp: number | null;
  confidence_status: ConfidenceStatus;
 /** Full machine-readable reason the engine sent: PAT, support/resistance, M5 brake, SIG, rejection reason, human-confirmation requirement, etc. */
  reason_json: Record<string, unknown>;
  rule_version: string | null;
  created_at: string;
}

export interface EngineEvent {
  id: string;
  timestamp: string;
  /** e.g. market_update, detector_fired, signal_taken, signal_rejected. */
  event_type: string;
  symbol: string | null;
  timeframe: string | null;
  detector: string | null;
  decision: string | null;
  reason_json: Record<string, unknown>;
  rule_version: string | null;
    signal_id: string | null;
}

export interface EngineStatus {
  engine_id: string;
  status: EngineState;
  last_heartbeat: string | null;
  last_market_data: string | null;
  engine_version: string | null;
  rule_version: string | null;
    updated_at: string;
}

export interface SignalWithEvents extends Signal {
  events: EngineEvent[];
}

export const ENGINE_MARKET_DATA_MAX_AGE_MS =  2 * 60 * 1000; // 2 min
export const ENGINE_HEARTBEAT_MAX_AGE_MS =  6 * 60 * 1000; // 6 min
export const SIGNAL_FRESH_MAX_AGE_MS =  4 * 60 * 60 * 1000; // 4 h