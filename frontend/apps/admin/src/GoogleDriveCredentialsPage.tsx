import { Badge, Card, PageShell } from '@ui';
import { badgeVariantForStatus, buildGoogleDriveCredentialsSnapshot, setupWizardFolders, storageRoutes } from './storageRegistry';

export function GoogleDriveCredentialsPage() {
  const snapshot = buildGoogleDriveCredentialsSnapshot();

  return (
    <PageShell
      eyebrow="Google Drive Credentials"
      title="Production credential bindings"
      description="Logical bindings between the ten Google Drive resources and their masked credential references."
    >
      <div className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
        <Card title="Binding summary" description="The registry and the vault are linked through logical references only.">
          <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="text-sm text-slate-400">Bindings</div>
              <div className="mt-2 text-3xl font-semibold text-white">{snapshot.bindingCount}</div>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="text-sm text-slate-400">Vault records</div>
              <div className="mt-2 text-3xl font-semibold text-white">{snapshot.vault.summary.recordCount}</div>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="text-sm text-slate-400">Active</div>
              <div className="mt-2 text-3xl font-semibold text-white">{snapshot.vault.summary.activeCount}</div>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="text-sm text-slate-400">Rotation due</div>
              <div className="mt-2 text-3xl font-semibold text-white">{snapshot.vault.summary.rotationDueCount}</div>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="text-sm text-slate-400">Expired</div>
              <div className="mt-2 text-3xl font-semibold text-white">{snapshot.vault.summary.expiredCount}</div>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="text-sm text-slate-400">Masked</div>
              <div className="mt-2 text-3xl font-semibold text-white">{snapshot.vault.summary.maskedRecords}</div>
            </div>
          </div>
        </Card>
        <Card title="Routing and folders" description="Drive bindings inherit the official routing map and the automatic folder plan.">
          <div className="mt-4 space-y-3 text-sm text-slate-300">
            <div className="rounded-xl border border-slate-800 px-3 py-2">Drive 1 and Drive 2 are reserved for videos.</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Drive 3 is reserved for photos and audio.</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Drive 5 is reserved for conversation archives.</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Drive 8 remains the overflow target.</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Automatic folders: {setupWizardFolders.join(', ')}</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Route preview: {storageRoutes[0].route.join(' -> ')}</div>
          </div>
        </Card>
      </div>

      <Card title="Credential bindings" description="Each logical Drive carries a stable credential reference and secure test timestamps.">
        <div className="mt-4 grid gap-3 xl:grid-cols-2">
          {snapshot.secureReferences.map((credential) => (
            <div key={credential.credentialId} className="rounded-2xl border border-slate-800/80 bg-slate-950/70 p-4">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <div className="text-xs uppercase tracking-[0.3em] text-slate-500">{credential.driveId}</div>
                  <div className="mt-1 text-lg font-semibold text-white">{credential.role}</div>
                </div>
                <Badge variant={badgeVariantForStatus(credential.status)}>{credential.status}</Badge>
              </div>
              <div className="mt-2 text-sm text-slate-400">{credential.logicalName} · {credential.credentialId}</div>
              <div className="mt-4 space-y-2 text-sm text-slate-300">
                <div className="rounded-xl border border-slate-800 px-3 py-2">OAuth status: {credential.oauthStatus}</div>
                <div className="rounded-xl border border-slate-800 px-3 py-2">Last connection test: {credential.lastConnectionTest}</div>
                <div className="rounded-xl border border-slate-800 px-3 py-2">Last upload test: {credential.lastUploadTest}</div>
                <div className="rounded-xl border border-slate-800 px-3 py-2">Last download test: {credential.lastDownloadTest}</div>
                <div className="rounded-xl border border-slate-800 px-3 py-2">Last healthcheck: {credential.lastHealthcheck}</div>
              </div>
            </div>
          ))}
        </div>
      </Card>

      <div className="grid gap-6 xl:grid-cols-[0.8fr_1.2fr]">
        <Card title="Vault posture" description="The underlying vault keeps the credential material encrypted and masked.">
          <div className="mt-4 space-y-3 text-sm text-slate-300">
            <div className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2">
              <span>Vault status</span>
              <Badge variant={badgeVariantForStatus(snapshot.vault.status)}>{snapshot.vault.status}</Badge>
            </div>
            <div className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2">
              <span>Last access</span>
              <Badge variant="info">{snapshot.vault.monitoring.lastAccess}</Badge>
            </div>
            <div className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2">
              <span>Last success</span>
              <Badge variant="success">{snapshot.vault.monitoring.lastSuccess}</Badge>
            </div>
            <div className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2">
              <span>Alerts</span>
              <Badge variant={snapshot.vault.monitoring.alerts.length > 0 ? 'warning' : 'success'}>{snapshot.vault.monitoring.alerts.length}</Badge>
            </div>
          </div>
        </Card>
        <Card title="Secure reference rules" description="Only logical identifiers and masked references appear in this surface.">
          <div className="mt-4 space-y-3 text-sm text-slate-300">
            <div className="rounded-xl border border-slate-800 px-3 py-2">The Storage Resource Registry stores credential_id references only.</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">The Credential Vault remains the only place that stores encrypted protected material.</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">The Storage Orchestrator chooses the drive from the official route.</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">No Google Drive URL is stored in business data or frontend data.</div>
          </div>
        </Card>
      </div>
    </PageShell>
  );
}
