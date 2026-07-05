import { Button, Card, PageShell } from '@ui';
import { buildGoogleDriveAdminSnapshot, setupWizardFolders, setupWizardSteps, storageRoutes } from './storageRegistry';

export function StorageSetupWizardPage() {
  const snapshot = buildGoogleDriveAdminSnapshot();

  return (
    <PageShell
      eyebrow="Storage Setup Wizard"
      title="Google Drive activation wizard"
      description="A step-based activation wizard that prepares the 10 Google Drive accounts without exposing protected material."
      actions={<Button>Run setup</Button>}
    >
      <div className="grid gap-6 lg:grid-cols-[0.8fr_1.2fr]">
        <Card title="Wizard steps" description="The wizard binds the credential vault, validates access, and prepares onboarding for real accounts.">
          <ol className="mt-4 space-y-2 text-sm text-slate-300">
            {setupWizardSteps.map((step) => (
              <li key={step} className="rounded-xl border border-slate-800 px-3 py-2">{step}</li>
            ))}
          </ol>
        </Card>
        <Card title="Configuration summary" description="No protected material is stored in the frontend; all references stay logical and masked.">
          <div className="mt-4 space-y-2 text-sm text-slate-300">
            <div className="rounded-xl border border-slate-800 px-3 py-2">Architecture: OVH VPS + Backup Center + 10 Google Drive + external disk</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Drive 1 and Drive 2: videos only</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Drive 3: photos and audio</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Drive 5: conversation archives</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Drive 7: application backups</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Drive 8: overflow and critical replication</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Drive 9: strategic reserve, Drive 10: maintenance and migration</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Automatic folders: {setupWizardFolders.join(', ')}</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Validation steps: vault binding, OAuth, permissions, read, write, upload, download, folder creation, and final verification</div>
          </div>
        </Card>
      </div>

      <div className="grid gap-6 xl:grid-cols-[1fr_1fr]">
        <Card title="Activation summary" description="The setup wizard produces a safe trace with masked credential references only.">
          <div className="mt-4 grid gap-3 md:grid-cols-2">
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="text-sm text-slate-400">Declared drives</div>
              <div className="mt-2 text-2xl font-semibold text-white">10</div>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="text-sm text-slate-400">Available resources</div>
              <div className="mt-2 text-2xl font-semibold text-white">{snapshot.availableResources}</div>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="text-sm text-slate-400">Alerts</div>
              <div className="mt-2 text-2xl font-semibold text-white">{snapshot.alertCount}</div>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="text-sm text-slate-400">Last control</div>
              <div className="mt-2 text-sm font-semibold text-white">{snapshot.lastControl}</div>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="text-sm text-slate-400">Last access</div>
              <div className="mt-2 text-sm font-semibold text-white">{snapshot.lastAccess}</div>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="text-sm text-slate-400">OAuth-ready drives</div>
              <div className="mt-2 text-2xl font-semibold text-white">{snapshot.oauthReadyCount}</div>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="text-sm text-slate-400">Credential vault</div>
              <div className="mt-2 text-2xl font-semibold text-white">{snapshot.credentialVault.summary.recordCount}</div>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="text-sm text-slate-400">Latest route</div>
              <div className="mt-2 text-sm font-semibold text-white">{storageRoutes[0].route.join(' -> ')}</div>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="text-sm text-slate-400">Monitoring</div>
              <div className="mt-2 text-sm font-semibold text-white">{snapshot.monitoring.latencyMs} ms / {snapshot.monitoring.throughputMbps} Mbps</div>
            </div>
          </div>
        </Card>
        <Card title="Folder plan" description="The wizard will create these folders automatically during activation.">
          <div className="mt-4 flex flex-wrap gap-2">
            {setupWizardFolders.map((folder) => (
              <span key={folder} className="rounded-full border border-slate-700 px-3 py-1 text-xs uppercase tracking-[0.25em] text-slate-400">{folder}</span>
            ))}
          </div>
        </Card>
        <Card title="Route preview" description="The wizard exposes the official routing map before real credentials are supplied.">
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
