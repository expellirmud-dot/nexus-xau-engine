import { createClient as createSupabaseClient } from '@supabase/supabase-js';

/**
 * SERVER-ONLY Supabase client using the SERVICE-ROLE key.
 *
 * - Bypasses RLS — meant for backend services (the Python engine ingest wrapper,
 *   admin operations, migration tooling). The web UI never uses this。
 * - SECURITY: never import this file from a client component ('use client')——
 *   the bundler would leak the service-role key into the browser. This module
 *   references process.env.SUPABASE_SERVICE_ROLE_KEY which is NOT prefixed with
 *   NEXT_PUBLIC_ and is therefore unavailable client-side。
 */
export function createAdminClient() {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
	if (!url || !key) {
    throw new Error(
      'createAdminClient: NEXT_PUBLIC_SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set (server environment only)。',
    );
  }
	return createSupabaseClient(url, key, {
    auth: {
      autoRefreshToken: false,
      persistSession: false,
    },
	});
}