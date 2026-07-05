import { Button, Card, PageShell } from '@ui';
import { buildManagerSnapshot, setupWizardSteps, storageRoutes } from './storageRegistry';

export function StorageSetupWizardPage() {
  const snapshot = buildManagerSnapshot();

  return (
    <PageShell
      eyebrow="Storage Setup Wizard"
      title="Mock setup for the AAC-B2 storage platform"
      description="A step-based placeholder wizard that documents the official configuration flow."
      actions={<Button>Run setup</Button>}
    >
      <div className="grid gap-6 lg:grid-cols-[0.8fr_1.2fr]">
        <Card title="Wizard steps" description="The wizard remains fully mock-driven and uses placeholders only.">
          <ol className="mt-4 space-y-2 text-sm text-slate-300">
            {setupWizardSteps.map((step) => (
              <li key={step} className="rounded-xl border border-slate-800 px-3 py-2">{step}</li>
            ))}
          </ol>
        </Card>
        <Card title="Configuration summary" description="No secrets are stored; all sensitive inputs remain placeholders.">
          <div className="mt-4 space-y-2 text-sm text-slate-300">
            <div className="rounded-xl border border-slate-800 px-3 py-2">Architecture: OVH VPS + Backup Center + 10 Google Drive + external disk</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Drive 1 and Drive 2: videos only</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Drive 3: photos and audio</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Drive 5: conversation archives</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Drive 7: application backups</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Drive 8: overflow and critical replication</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Drive 9: strategic reserve, Drive 10: maintenance and migration</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Mock checks: read, write, video upload, conversation archive, and backup simulation</div>
          </div>
        </Card>
      </div>

      <div className="grid gap-6 xl:grid-cols-[1fr_1fr]">
        <Card title="Mock execution summary" description="The setup wizard produces a safe trace without any real Google secret material.">
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
              <div className="text-sm text-slate-400">Latest route</div>
              <div className="mt-2 text-sm font-semibold text-white">{storageRoutes[0].route.join(' -> ')}</div>
            </div>
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
