'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

const TABS = [
  { href: '/', label: 'Live', icon: 'M13 2L3 14h9l-1 8 10-12h-9l1-8z' },
  { href: '/signals', label: 'Signals', icon: 'M4 19V5M9 19V9M14 19V2M19 19V13' },
  { href: '/system', label: 'System', icon: 'M12 2a10 10 0 10 0 0 4 4v1h14v-1a10 10 0 0114-4zM12 12a4 4 0 100 0-4 4 0 000 4-4z' },
] as const;

export function BottomNav() {
  const pathname = usePathname();
	return (
    <nav className="fixed inset-x-0 bottom-0 z-30 border-t border-white/10 bg-slate-950/80 pb-[env(safe-area-inset-bottom)] backdrop-blur-xl">
      <div className="mx-auto grid max-w-2xl grid-cols-3">
        {TABS.map((tab) => {
          const active = tab.href === '/' ? pathname === '/' : pathname.startsWith(tab.href)
          return (
            <Link
              key={tab.href}
              href={tab.href}
              className={`flex flex-col items-center gap-1 py-2.5 text-xs font-medium transition-colors ${
                active ? 'text-cyan-300' : 'text-slate-500 hover:text-slate-300'
              }`}
            >
              <svg className="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                <path d={tab.icon} />
              </svg>
              {tab.label}
            </Link>
          );
        })}
      </div>
    </nav>
  );
}