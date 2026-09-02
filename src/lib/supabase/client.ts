import { createBrowserClient } from '@supabase/ssr';

/**
 * Browser-side Supabase client.
 *
 * SECURITY: only the anon key ships to the browser. RLS policies must grant
 * SELECT on signals/engine_events/engine_status to anon (or authenticated roles)。
 * The service-role key lives exclusively in server-admin.ts and must never be
 * imported from any client component — doing so bundles the secret into the browser。
 */
export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
  );
}