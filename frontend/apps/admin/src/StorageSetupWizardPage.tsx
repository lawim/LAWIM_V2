import { Button, Card, PageShell } from '@ui';

const steps = [
  'Architecture overview',
  'Backup Center',
  'Google Drive x10',
  'External disk',
  'Lifecycle policies',
  'Optimization',
  'Mock connection tests',
  'Configuration summary',
];

export function StorageSetupWizardPage() {
  return (
    <PageShell
      eyebrow="Storage Setup Wizard"
      title="Mock setup for the AAC-B2 storage platform"
      description="A step-based placeholder wizard that documents the intended configuration flow."
      actions={<Button>Run setup</Button>}
    >
      <div className="grid gap-6 lg:grid-cols-[0.8fr_1.2fr]">
        <Card title="Wizard steps" description="The wizard remains fully mock-driven and uses placeholders only.">
          <ol className="mt-4 space-y-2 text-sm text-slate-300">
            {steps.map((step) => (
              <li key={step} className="rounded-lg border border-slate-800 px-3 py-2">{step}</li>
            ))}
          </ol>
        </Card>
        <Card title="Configuration summary" description="No secrets are stored; all sensitive inputs remain placeholders.">
          <div className="mt-4 space-y-2 text-sm text-slate-300">
            <div className="rounded-lg border border-slate-800 px-3 py-2">Architecture: OVH VPS + Backup Center + 10 Google Drive + external disk</div>
            <div className="rounded-lg border border-slate-800 px-3 py-2">Lifecycle: hot, warm, cold, archived</div>
            <div className="rounded-lg border border-slate-800 px-3 py-2">Optimization: compression, deduplication, bandwidth policy</div>
            <div className="rounded-lg border border-slate-800 px-3 py-2">Health checks: mock-ready placeholders only</div>
          </div>
        </Card>
      </div>
    </PageShell>
  );
}
