import { Badge, Card, PageShell } from '@ui';
import { badgeVariantForStatus, googleDriveConfigurations } from './storageRegistry';

export function GoogleDriveRegistryPage() {
  return (
    <PageShell
      eyebrow="Google Drive Registry"
      title="Google Drive functional configuration"
      description="Placeholder credentials, mock validation status, and the 10 logical Drive records ready for secure onboarding."
    >
      <div className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
        <Card title="Configuration model" description="Each logical Drive is declared without any real token or secret material.">
          <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-2">
            {googleDriveConfigurations.map((drive) => (
              <div key={drive.driveId} className="rounded-2xl border border-slate-800/80 bg-slate-950/70 p-4">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <div className="text-xs uppercase tracking-[0.3em] text-slate-500">{drive.driveId}</div>
                    <div className="mt-1 text-lg font-semibold text-white">{drive.logicalName}</div>
                  </div>
                  <Badge variant="info">{drive.provider}</Badge>
                </div>
                <div className="mt-2 text-sm text-slate-400">{drive.category}</div>
                <div className="mt-4 space-y-2 text-sm text-slate-300">
                  <div className="rounded-xl border border-slate-800 px-3 py-2">Email: {drive.emailPlaceholder}</div>
                  <div className="rounded-xl border border-slate-800 px-3 py-2">Quota: {drive.quotaGb} GB</div>
                  <div className="rounded-xl border border-slate-800 px-3 py-2">Used: {drive.usedGb.toFixed(1)} GB · Available: {drive.availableGb.toFixed(1)} GB</div>
                </div>
                <div className="mt-4 flex flex-wrap gap-2">
                  <Badge variant={badgeVariantForStatus(drive.credentialStatus === 'placeholder-configured' ? 'ready' : 'blocked')}>{drive.credentialStatus}</Badge>
                  <Badge variant={badgeVariantForStatus(drive.testStatus === 'mock-warning' ? 'blocked' : 'ready')}>{drive.testStatus}</Badge>
                </div>
              </div>
            ))}
          </div>
        </Card>
        <Card title="Safety rules" description="The registry is ready for secure onboarding of the real Google accounts.">
          <div className="mt-4 space-y-3 text-sm text-slate-300">
            <div className="rounded-xl border border-slate-800 px-3 py-2">No Google Drive URL is stored in business data.</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">No token, client secret, or refresh token is stored in this release.</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">All credentials remain placeholders until the secure assistant phase.</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Each Drive uses a logical email placeholder only.</div>
          </div>
        </Card>
      </div>
    </PageShell>
  );
}
