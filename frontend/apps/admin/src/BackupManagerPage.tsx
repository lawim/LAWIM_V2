import { Badge, Card, PageShell } from '@ui';
import { badgeVariantForStatus, buildManagerSnapshot, storageResources } from './storageRegistry';

export function BackupManagerPage() {
  const snapshot = buildManagerSnapshot();

  return (
    <PageShell
      eyebrow="Backup Manager"
      title="Simplified manager console"
      description="Global storage, alerts, control timestamps, and backup status at a glance."
    >
      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
        <Card title="Total quota" description="Theoretical Google Drive capacity across all ten resources.">
          <div className="mt-4 text-3xl font-semibold text-white">{snapshot.totalQuotaGb} GB</div>
        </Card>
        <Card title="Remaining capacity" description="Available storage in the operational registry.">
          <div className="mt-4 text-3xl font-semibold text-white">{snapshot.remainingGb} GB</div>
        </Card>
        <Card title="Alert posture" description="Resources above the normal band require review.">
          <div className="mt-4 flex items-center gap-3">
            <Badge variant={snapshot.alertCount > 0 ? 'warning' : 'success'}>{snapshot.alertCount} alerts</Badge>
            <span className="text-sm text-slate-300">{snapshot.blockedCount} blocked</span>
          </div>
        </Card>
        <Card title="Last control" description="Most recent registry control timestamp.">
          <div className="mt-4 text-sm font-semibold text-white">{snapshot.lastControl}</div>
        </Card>
      </div>

      <div className="grid gap-6 xl:grid-cols-[0.85fr_1.15fr]">
        <Card title="Backup status" description="Backup orchestration is aligned with the registry and connector readiness.">
          <div className="mt-4 space-y-3 text-sm text-slate-300">
            <div className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2">
              <span>Backup status</span>
              <Badge variant="success">{snapshot.backupStatus}</Badge>
            </div>
            <div className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2">
              <span>Available resources</span>
              <Badge variant="info">{snapshot.availableResources}</Badge>
            </div>
            <div className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2">
              <span>Global usage</span>
              <Badge variant={snapshot.usagePercent >= 85 ? 'warning' : 'info'}>{snapshot.usagePercent}%</Badge>
            </div>
            <div className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2">
              <span>OAuth-ready connectors</span>
              <Badge variant="info">{snapshot.oauthReadyCount}</Badge>
            </div>
          </div>
        </Card>
        <Card title="Route watchlist" description="The manager can inspect the drives that require follow-up.">
          <div className="mt-4 grid gap-3 md:grid-cols-2">
            {storageResources
              .filter((resource) => resource.thresholdBand !== 'normal')
              .map((resource) => (
                <div key={resource.driveId} className="rounded-xl border border-slate-800 bg-slate-950/70 p-4">
                  <div className="flex items-center justify-between gap-3">
                    <div className="font-semibold text-white">{resource.driveId}</div>
                    <Badge variant={badgeVariantForStatus(resource.thresholdBand)}>{resource.thresholdBand}</Badge>
                  </div>
                  <div className="mt-2 text-sm text-slate-400">{resource.role}</div>
                  <div className="mt-3 text-xs text-slate-500">
                    {resource.usagePercent}% used · {resource.availableGb.toFixed(1)} GB remaining
                  </div>
                </div>
              ))}
          </div>
        </Card>
      </div>
    </PageShell>
  );
}
