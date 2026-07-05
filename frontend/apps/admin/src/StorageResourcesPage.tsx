import { Badge, Card, PageShell } from '@ui';
import { badgeVariantForStatus, buildManagerSnapshot, storageResources } from './storageRegistry';

export function StorageResourcesPage() {
  const snapshot = buildManagerSnapshot();

  return (
    <PageShell
      eyebrow="Admin Storage Registry"
      title="Storage Resource Registry"
      description="The ten Google Drive resources, their quota bands, and the mock health posture used by the Storage Orchestrator."
    >
      <div className="grid gap-6 xl:grid-cols-[1.25fr_0.75fr]">
        <Card title="Registry summary" description="Ten logical resources, 13 GB theoretical quota each, and mock validation status.">
          <div className="mt-4 grid gap-3 md:grid-cols-2">
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="text-sm text-slate-400">Total quota</div>
              <div className="mt-2 text-2xl font-semibold text-white">{snapshot.totalQuotaGb} GB</div>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="text-sm text-slate-400">Total used</div>
              <div className="mt-2 text-2xl font-semibold text-white">{snapshot.totalUsedGb} GB</div>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="text-sm text-slate-400">Available resources</div>
              <div className="mt-2 text-2xl font-semibold text-white">{snapshot.availableResources}</div>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="text-sm text-slate-400">Blocked resources</div>
              <div className="mt-2 text-2xl font-semibold text-white">{snapshot.blockedCount}</div>
            </div>
          </div>
        </Card>
        <Card title="Threshold bands" description="The registry keeps the four operational bands explicit.">
          <div className="mt-4 space-y-3 text-sm text-slate-300">
            <div className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2">
              <span>Normal</span>
              <Badge variant="success">0-70%</Badge>
            </div>
            <div className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2">
              <span>Attention</span>
              <Badge variant="info">70-85%</Badge>
            </div>
            <div className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2">
              <span>Slowdown</span>
              <Badge variant="warning">85-92%</Badge>
            </div>
            <div className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2">
              <span>Blocked</span>
              <Badge variant="warning">&gt;92%</Badge>
            </div>
          </div>
        </Card>
      </div>

      <Card title="Drive inventory" description="Roles, quotas, occupation, last test, and the official route hint.">
        <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-2">
          {storageResources.map((drive) => (
            <div key={drive.driveId} className="rounded-2xl border border-slate-800/80 bg-slate-950/70 p-4">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <div className="text-xs uppercase tracking-[0.3em] text-slate-500">{drive.driveId}</div>
                  <div className="mt-1 text-lg font-semibold text-white">{drive.role}</div>
                </div>
                <Badge variant={badgeVariantForStatus(drive.status)}>{drive.status}</Badge>
              </div>
              <div className="mt-2 text-sm text-slate-400">{drive.logicalName} · {drive.category}</div>
              <div className="mt-4 h-2 rounded-full bg-slate-800">
                <div
                  className={`h-2 rounded-full ${
                    drive.thresholdBand === 'normal'
                      ? 'bg-emerald-400'
                      : drive.thresholdBand === 'attention'
                        ? 'bg-amber-400'
                        : drive.thresholdBand === 'slowdown'
                          ? 'bg-orange-400'
                          : 'bg-rose-500'
                  }`}
                  style={{ width: `${drive.usagePercent}%` }}
                />
              </div>
              <div className="mt-4 grid grid-cols-3 gap-3 text-xs text-slate-400">
                <div>
                  <div className="text-slate-500">Quota</div>
                  <div className="mt-1 text-slate-200">{drive.quotaGb} GB</div>
                </div>
                <div>
                  <div className="text-slate-500">Used</div>
                  <div className="mt-1 text-slate-200">{drive.usedGb.toFixed(1)} GB</div>
                </div>
                <div>
                  <div className="text-slate-500">Available</div>
                  <div className="mt-1 text-slate-200">{drive.availableGb.toFixed(1)} GB</div>
                </div>
              </div>
              <div className="mt-4 flex flex-wrap gap-2">
                <Badge variant={badgeVariantForStatus(drive.thresholdBand)}>{drive.thresholdBand}</Badge>
                <Badge variant={badgeVariantForStatus(drive.health)}>{drive.health}</Badge>
                <Badge variant="default">{drive.lastTest}</Badge>
              </div>
              <div className="mt-4 text-xs text-slate-500">Route hint: {drive.routeHint}</div>
            </div>
          ))}
        </div>
      </Card>
    </PageShell>
  );
}
