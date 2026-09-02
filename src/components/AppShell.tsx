import { AppHeader } from './AppHeader';
import { BottomNav } from './BottomNav';

export function AppShell({ title, freshLabel, children }: { title: string; freshLabel?: string; children: React.ReactNode }) {
  return (
    <div className="min-h-dvh bg-slate-950 text-slate-100">
      <AppHeader title={title} freshLabel={freshLabel} />
      <main className="mx-auto w-full max-w-2xl px-4 pb-24 pt-4">{children}</main>
      <BottomNav />
    </div>
  );
}