import 'server-only';

import type { Signal, SignalWithEvents, EngineStatus, EngineEvent } from './types';
import { createServerSupabase } from './supabase/server';

const SIGNAL_SELECT = '*, events:engine_events(*)';

export async function getLatestSignal(): Promise<Signal | null> {
	 const supabase = await createServerSupabase();
	 const { data } = await supabase
    .from('signals')
    .select(SIGNAL_SELECT)
    .order('timestamp', { ascending: false })
    .limit(1)
    .maybeSingle();
	return data ?? null;
}

export async function getSignalHistory(limit: number = 50): Promise<Signal[]> {
	 const supabase = await createServerSupabase();
	 const { data } = await supabase
    .from('signals')
    .select(SIGNAL_SELECT)
    .order('timestamp', { ascending: false })
    .limit(limit);
	return data ?? [];
}

export async function getSignalById(id: string): Promise<SignalWithEvents | null> {
	 const supabase = await createServerSupabase();
	 const { data } = await supabase
    .from('signals')
    .select(SIGNAL_SELECT)
    .eq('id', id)
    .maybeSingle();
	return (data as SignalWithEvents | null) ?? null;
}

export async function getEngineStatus(): Promise<EngineStatus | null> {
	 const supabase = await createServerSupabase();
	 const { data } = await supabase
    .from('engine_status')
    .select('*')
    .limit(1)
    .maybeSingle();
	return (data as EngineStatus | null) ?? null;
}

export async function getRecentEvents(limit: number = 25): Promise<EngineEvent[]> {
	 const supabase = await createServerSupabase();
	 const { data } = await supabase
    .from('engine_events')
    .select('*')
    .order('timestamp', { ascending: false })
    .limit(limit);
	return data ?? [];
}