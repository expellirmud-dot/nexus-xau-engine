export function ErrorState({ title, message, onRetry }: { title: string; message?: string; onRetry?: () => void }) {
  return (
    <div className="flex flex-col items-center justify-center rounded-2xl border border-rose-500/20 bg-rose-500/5 px-6 py-10 text-center">
      <div className="text-3xl">⚠️</div>
      <div className="mt-3 text-sm font-medium text-rose-200">{title}</div>
      {message && <div className="mt-2 max-w-sm break-words text-xs text-slate-500">{message}</div>}
      {onRetry && (
        <button
          onClick={onRetry}
          className="mt-4 rounded-lg border border-white/10 bg-white/5 px-4 py-2 text-xs font-medium text-slate-300 transition-colors hover:bg-white/10"
        >
          Retry
        </button>
      )}
    </div>
  );
}