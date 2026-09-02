import { AppShell } from '@/components/AppShell';
import { DashboardSkeleton } from '@/components/LoadingSkeleton';

export default function Loading() {
  return (
    <AppShell title="Nexus XAU Engine">
      <DashboardSkeleton />
    </AppShell>
  );
}