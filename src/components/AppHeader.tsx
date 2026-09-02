'use client';

import { RefreshButton } from './RefreshButton';

export function AppHeader({ title, freshLabel }: { title: string; freshLabel?: string }) {
	return (
    <header className="sticky top-0 z-30 border-b border-white/10 bg-slate-950/70 backdrop-blur-xl">
      <div className="mx-auto flex max-w-2xl items-center justify-between gap-3 px-4 py-3">
        <div className="flex min-w-0 items-center gap-2">
          <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-cyan-400/20 to-violet-500/20 text-lg">
            📈
          </div>
          <div className="min-w-0">
            <h1 className="truncate text-sm font-semibold text-slate-100">{title}</h1>
            {freshLabel && (
              <p className="truncate text-xs text-slate-500">{freshLabel}</p>
            )}
          </div>
        </div>
        <RefreshButton />
      </div>
    </header>
  );
}