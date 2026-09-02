import Link from 'next/link';
import { AppShell } from '@/components/AppShell';

export default function NotFound() {
  return (
    <AppShell title="Not Found">
      <div className="flex flex-col items-center justify-center rounded-3xl border border-dashed border-white/10 px-6 py-16 text-center">
        <div className="text-5xl">🔍</div>
        <h2 className="mt-4 text-lg font-semibold text-slate-200">Page not found</h2>
        <p className="mt-2 text-sm text-slate-500">The page you are looking for does not exist</p>
        <Link href="/" className="mt-6 rounded-lg border border-white/10 bg-white/5 px-4 py-2 text-sm text-slate-300 hover:bg-white/10">
          Back to dashboard
        </Link>
      </div>
    </AppShell>
  );
}