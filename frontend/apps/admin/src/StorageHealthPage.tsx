import { Badge, Card, PageShell } from '@ui';
import { badgeVariantForStatus, buildManagerSnapshot, storageResources, storageThresholds } from './storageRegistry';

export function StorageHealthPage() {
  const snapshot = buildManagerSnapshot();
  const blocked = storageResources.filter((resource) => resource.thresholdBand === 'blocked');
  const highlighted = storageResources.filter((resource) => resource.thresholdBand !== 'normal');

  return (
    <PageShell
      eyebrow="Storage Health"
      title="Storage health and drive distribution"
      description="Monitor the mock OVH/Drive architecture, quota bands, and the latest registry test."
    >
      <div className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
        <Card title="Drive route health" description="The route model now follows the official 10-drive allocation.">
          <div className="mt-4 space-y-3 text-sm text-slate-300">
            <div className="rounded-xl border border-slate-800 px-3 py-2">Drive 1 and Drive 2 are reserved for videos.</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Drive 3 is reserved for photos and audio.</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Drive 5 is reserved for conversation archives.</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Drive 7 is reserved for application backups.</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Drive 8 handles overflow and critical replication.</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Drive 9 stays reserved and Drive 10 covers maintenance and migration.</div>
          </div>
        </Card>
        <Card title="Policy snapshot" description="Thresholds and safety gates are mock configured.">
          <div className="mt-4 space-y-3 text-sm text-slate-300">
            <div className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2">
              <span>Normal</span>
              <Badge variant="success">{storageThresholds.normalMaxPercent}%</Badge>
            </div>
            <div className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2">
              <span>Attention</span>
              <Badge variant="info">{storageThresholds.attentionMaxPercent}%</Badge>
            </div>
            <div className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2">
              <span>Slowdown</span>
              <Badge variant="warning">{storageThresholds.slowdownMaxPercent}%</Badge>
            </div>
            <div className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2">
              <span>Blocked resources</span>
              <Badge variant={blocked.length > 0 ? 'warning' : 'success'}>{blocked.length}</Badge>
            </div>
          </div>
        </Card>
      </div>

      <div className="grid gap-6 xl:grid-cols-[0.95fr_1.05fr]">
        <Card title="Latest registry state" description="Mock test results and the current health posture.">
          <div className="mt-4 grid gap-3 md:grid-cols-2">
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="text-sm text-slate-400">Last test</div>
              <div className="mt-2 text-sm font-semibold text-white">{snapshot.lastTest}</div>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="text-sm text-slate-400">Available resources</div>
              <div className="mt-2 text-2xl font-semibold text-white">{snapshot.availableResources}</div>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="text-sm text-slate-400">Alert count</div>
              <div className="mt-2 text-2xl font-semibold text-white">{snapshot.alertCount}</div>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="text-sm text-slate-400">Backup posture</div>
              <div className="mt-2 text-2xl font-semibold text-white">{snapshot.backupStatus}</div>
            </div>
          </div>
        </Card>
        <Card title="Highlighted resources" description="Attention, slowdown, and blocked drives require review in the registry.">
          <div className="mt-4 space-y-3 text-sm text-slate-300">
            {highlighted.map((drive) => (
              <div key={drive.driveId} className="rounded-xl border border-slate-800 px-3 py-2">
                <div className="flex items-center justify-between gap-3">
                  <span>{drive.driveId} {drive.role}</span>
                  <Badge variant={badgeVariantForStatus(drive.thresholdBand)}>{drive.thresholdBand}</Badge>
                </div>
                <div className="mt-2 text-xs text-slate-500">
                  {drive.usagePercent}% used · {drive.availableGb.toFixed(1)} GB available · last test {drive.lastTest}
                </div>
              </div>
            ))}
            <div className="rounded-xl border border-slate-800 px-3 py-2">
              The blocked set is currently: {snapshot.blockedResources.join(', ')}.
            </div>
          </div>
        </Card>
      </div>
    </PageShell>
  );
}
