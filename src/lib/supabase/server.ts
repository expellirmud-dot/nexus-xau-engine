import { createServerClient } from '@supabase/ssr';
import { cookies } from 'next/headers';

/**
 * Server-component Supabase client (SSR)。
 *
 * Uses only the anon key — RLS still applies（read-only dashboard）。 Never
 * place this import in a 'use client' module。
 */
export async function createServerSupabase() {
  const cookieStore = await cookies();
  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll();
        },
        setAll() {},
      },
    },
  );
}