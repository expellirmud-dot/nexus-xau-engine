'use client';

import { useRouter } from 'next/navigation';
import { useState, useTransition } from 'react';

export function RefreshButton() {
  const router = useRouter();
  const [isPending, startTransition] = useTransition();
  const [spinning, setSpinning] = useState(false);

  const handleClick = () => {
    setSpinning(true);
    startTransition(() => {
      router.refresh();
    });
    // Keep spinning until the next render settles, with a sane cap。
    window.setTimeout(() => {
      setSpinning(false);
    }, 1500);
  };

	return (
    <button
      onClick={handleClick}
      aria-label="Refresh data"
      className="inline-flex h-9 w-9 items-center justify-center rounded-full border border-white/10 bg-white/5 text-slate-300 transition-colors hover:bg-white/10 disabled:opacity-50"
      disabled={isPending}
    >
      <svg
        className={`h-4 w-4 ${spinning ? 'animate-spin' : ''}`}
        viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"
      >
        <path strokeLinecap="round" strokeLinejoin="round" d="M4 4v5h5M20 20v-5h-5M4 9a8 8 0 0114.9-3M20 15a8 8 0 01-14.9 3" />
      </svg>
    </button>
  );
}