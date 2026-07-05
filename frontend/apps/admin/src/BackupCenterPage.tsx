import { Badge, Card, PageShell } from '@ui';
import { badgeVariantForStatus, buildManagerSnapshot, storageResources } from './storageRegistry';

export function BackupCenterPage() {
  const snapshot = buildManagerSnapshot();

  return (
    <PageShell
      eyebrow="Backup Center"
      title="Admin backup and storage control center"
      description="Operational view for the ten Google Drive resources, routing bands, and backup readiness."
    >
      <div className="grid gap-6 xl:grid-cols-[1.15fr_0.85fr]">
        <Card title="Global storage overview" description="Capacity, alert posture, and latest control status.">
          <div className="mt-4 grid gap-3 md:grid-cols-2">
            <div className="rounded-2xl border border-slate-800/80 bg-slate-950/70 p-4">
              <div className="text-sm text-slate-400">Total used</div>
              <div className="mt-2 text-2xl font-semibold text-white">{snapshot.totalUsedGb} GB</div>
            </div>
            <div className="rounded-2xl border border-slate-800/80 bg-slate-950/70 p-4">
              <div className="text-sm text-slate-400">Remaining</div>
              <div className="mt-2 text-2xl font-semibold text-white">{snapshot.remainingGb} GB</div>
            </div>
            <div className="rounded-2xl border border-slate-800/80 bg-slate-950/70 p-4">
              <div className="text-sm text-slate-400">Alerts</div>
              <div className="mt-2 text-2xl font-semibold text-white">{snapshot.alertCount}</div>
            </div>
            <div className="rounded-2xl border border-slate-800/80 bg-slate-950/70 p-4">
              <div className="text-sm text-slate-400">Last control</div>
              <div className="mt-2 text-sm font-semibold text-white">{snapshot.lastControl}</div>
            </div>
          </div>
        </Card>
        <Card title="Operations" description="Backup posture, route health, and connector readiness.">
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
              <span>Blocked resources</span>
              <Badge variant={snapshot.blockedCount > 0 ? 'warning' : 'success'}>{snapshot.blockedCount}</Badge>
            </div>
            <div className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2">
              <span>Global usage</span>
              <Badge variant={snapshot.usagePercent >= 85 ? 'warning' : 'info'}>{snapshot.usagePercent}%</Badge>
            </div>
            <div className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2">
              <span>Route readiness</span>
              <Badge variant="info">Drive 1, 3, 5, 7 and 10 ready</Badge>
            </div>
            <div className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2">
              <span>OAuth ready</span>
              <Badge variant="info">{snapshot.oauthReadyCount}</Badge>
            </div>
          </div>
        </Card>
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
        <Card title="Distributed Google Drive overview" description="The 10 Drive registry stays aligned with the official operating model.">
          <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-2">
            {storageResources.map((drive) => (
              <div key={drive.driveId} className="rounded-2xl border border-slate-800/80 bg-slate-950/70 p-4">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <div className="text-xs uppercase tracking-[0.3em] text-slate-500">{drive.driveId}</div>
                    <div className="mt-1 text-lg font-semibold text-white">{drive.role}</div>
                  </div>
                  <Badge variant={badgeVariantForStatus(drive.state)}>{drive.state}</Badge>
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
                  <Badge variant="default">{drive.apiVersion}</Badge>
                </div>
                <div className="mt-4 text-xs text-slate-500">Route: {drive.routeHint}</div>
              </div>
            ))}
          </div>
        </Card>
        <Card title="Alert matrix" description="Drive health is scored against the four official bands.">
          <div className="mt-4 space-y-3 text-sm text-slate-300">
            {snapshot.alerts.map((alert) => (
              <div key={alert} className="rounded-xl border border-slate-800 px-3 py-2">
                {alert}
              </div>
            ))}
            <div className="rounded-xl border border-slate-800 px-3 py-2">
              Thresholds: normal 0-70%, attention 70-85%, slowdown 85-92%, blocked &gt;92%.
            </div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">
              Monitoring: {snapshot.monitoring.latencyMs} ms latency, {snapshot.monitoring.throughputMbps} Mbps throughput.
            </div>
          </div>
        </Card>
      </div>
    </PageShell>
  );
}
