export function SignalListSkeleton({ count = 4 }: { count?: number }) {
  return (
    <div className="space-y-3">
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="animate-pulse rounded-2xl border border-white/5 bg-white/[0.02] p-4">
          <div className="flex items-center justify-between">
            <div className="h-5 w-20 rounded-full bg-white/10" />
            <div className="h-5 w-28 rounded-md bg-white/10" />
          </div>
          <div className="mt-3 grid grid-cols-3 gap-2">
            <div className="h-6 rounded bg-white/10" />
            <div className="h-6 rounded bg-white/10" />
            <div className="h-6 rounded bg-white/10" />
          </div>
        </div>
      ))}
    </div>
  );
}

export function DashboardSkeleton() {
  return (
    <div className="space-y-4">
      <div className="animate-pulse rounded-3xl border border-white/10 bg-white/[0.03] p-6">
        <div className="h-10 w-32 rounded-full bg-white/10" />
        <div className="mt-4 h-8 w-40 rounded bg-white/10" />
        <div className="mt-4 grid grid-cols-2 gap-2">
          <div className="h-10 rounded bg-white/10" />
          <div className="h-10 rounded bg-white/10" />
        </div>
      </div>
      <SignalListSkeleton />
    </div>
  );
}