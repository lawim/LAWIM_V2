import { Badge, Card, PageShell } from '@ui';
import { badgeVariantForStatus, buildGoogleDriveAdminSnapshot, setupWizardFolders, storageRoutes } from './storageRegistry';

export function GoogleDriveRegistryPage() {
  const snapshot = buildGoogleDriveAdminSnapshot();

  return (
    <PageShell
      eyebrow="Google Drive Admin Center"
      title="Google Drive operational control center"
      description="Placeholder credentials, OAuth state, quota, routing, and the 10 logical Drive records ready for secure onboarding."
    >
      <div className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
        <Card title="Drive fleet" description="Capacity, health, OAuth state, last transfer, and incident trace for each Drive.">
          <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-2">
            {snapshot.connectors.map((drive) => (
              <div key={drive.driveId} className="rounded-2xl border border-slate-800/80 bg-slate-950/70 p-4">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <div className="text-xs uppercase tracking-[0.3em] text-slate-500">{drive.driveId}</div>
                    <div className="mt-1 text-lg font-semibold text-white">{drive.logicalName}</div>
                  </div>
                  <Badge variant={badgeVariantForStatus(drive.oauthStatus)}>{drive.oauthStatus}</Badge>
                </div>
                <div className="mt-2 text-sm text-slate-400">{drive.category} · {drive.provider} · {drive.resourceType}</div>
                <div className="mt-4 space-y-2 text-sm text-slate-300">
                  <div className="rounded-xl border border-slate-800 px-3 py-2">Email: {`${drive.driveId}@placeholder.lawim.invalid`}</div>
                  <div className="rounded-xl border border-slate-800 px-3 py-2">Quota: {drive.quotaGb} GB · Used: {drive.usedGb.toFixed(1)} GB · Free: {drive.availableGb.toFixed(1)} GB</div>
                  <div className="rounded-xl border border-slate-800 px-3 py-2">OAuth: {drive.oauthStatus} · API: {drive.apiVersion}</div>
                </div>
                <div className="mt-4 flex flex-wrap gap-2">
                  <Badge variant={badgeVariantForStatus(drive.state)}>{drive.state}</Badge>
                  <Badge variant={badgeVariantForStatus(drive.health)}>{drive.health}</Badge>
                  <Badge variant={badgeVariantForStatus(drive.lastIncident === 'none' ? 'ready' : 'blocked')}>{drive.lastIncident === 'none' ? 'No incident' : drive.lastIncident}</Badge>
                </div>
                <div className="mt-4 space-y-2 text-xs text-slate-500">
                  <div>Last control: {drive.lastControl}</div>
                  <div>Last access: {drive.lastAccess}</div>
                  <div>Last upload: {drive.lastUpload}</div>
                  <div>Last download: {drive.lastDownload}</div>
                  <div>Folders: {drive.folders.join(', ')}</div>
                  <div>Route hint: {drive.routeHint}</div>
                </div>
                {drive.alerts.length > 0 ? (
                  <div className="mt-4 space-y-2 text-xs text-amber-200">
                    {drive.alerts.map((alert) => (
                      <div key={alert} className="rounded-xl border border-amber-500/30 bg-amber-500/10 px-3 py-2">{alert}</div>
                    ))}
                  </div>
                ) : (
                  <div className="mt-4 rounded-xl border border-slate-800 px-3 py-2 text-xs text-slate-500">No incident recorded.</div>
                )}
              </div>
            ))}
          </div>
        </Card>
        <Card title="Operational rules" description="The registry is ready for secure onboarding of the real Google accounts.">
          <div className="mt-4 space-y-3 text-sm text-slate-300">
            <div className="rounded-xl border border-slate-800 px-3 py-2">No Google Drive URL is stored in business data.</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">No token, client secret, or refresh token is stored in this release.</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">All credentials remain placeholders until the secure assistant phase.</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Each Drive uses a logical email placeholder only.</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Automatic folders: {setupWizardFolders.join(', ')}</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Drive 1 and Drive 2 reserve video traffic; Drive 3 covers photos and audio; Drive 5 covers conversation archives.</div>
          </div>
        </Card>
      </div>
      <div className="grid gap-6 xl:grid-cols-[0.8fr_1.2fr]">
        <Card title="Monitoring" description="Quota, latency, throughput, API state, and alert posture.">
          <div className="mt-4 space-y-3 text-sm text-slate-300">
            <div className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2">
              <span>Quota usage</span>
              <Badge variant={badgeVariantForStatus(snapshot.usagePercent >= 85 ? 'blocked' : 'ready')}>{snapshot.usagePercent}%</Badge>
            </div>
            <div className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2">
              <span>Latency</span>
              <Badge variant="info">{snapshot.monitoring.latencyMs} ms</Badge>
            </div>
            <div className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2">
              <span>Throughput</span>
              <Badge variant="info">{snapshot.monitoring.throughputMbps} Mbps</Badge>
            </div>
            <div className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2">
              <span>OAuth state</span>
              <Badge variant={badgeVariantForStatus(snapshot.oauthState)}>{snapshot.oauthState}</Badge>
            </div>
            <div className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2">
              <span>Alerts</span>
              <Badge variant={snapshot.alertCount > 0 ? 'warning' : 'success'}>{snapshot.alertCount}</Badge>
            </div>
          </div>
        </Card>
        <Card title="Routing and folders" description="Drive routing remains ordered and the folder plan is fixed for future activation.">
          <div className="mt-4 space-y-3 text-sm text-slate-300">
            {storageRoutes.map((route) => (
              <div key={route.category} className="rounded-xl border border-slate-800 px-3 py-2">
                <div className="flex items-center justify-between gap-3">
                  <span className="font-medium text-white">{route.label}</span>
                  <span className="text-xs uppercase tracking-[0.3em] text-slate-500">{route.category}</span>
                </div>
                <div className="mt-2 text-xs text-slate-500">{route.route.join(' -> ')}</div>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </PageShell>
  );
}
