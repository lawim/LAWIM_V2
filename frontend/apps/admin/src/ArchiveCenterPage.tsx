import { Badge, Card, PageShell } from '@ui';

export function ArchiveCenterPage() {
  return (
    <PageShell
      eyebrow="Archive Center"
      title="Conversation archive management"
      description="Review archive manifests, restore queues, and checksum status for cold data."
    >
      <div className="grid gap-6 lg:grid-cols-[1.3fr_0.7fr]">
        <Card title="Archive index" description="Conversation archives are indexed and routed to Drive 8.">
          <div className="mt-4 space-y-3 text-sm text-slate-300">
            <div className="rounded-lg border border-slate-800 px-3 py-2">Structured JSON archives with checksum and version.</div>
            <div className="rounded-lg border border-slate-800 px-3 py-2">Media IDs are preserved for attachment resolution.</div>
            <div className="rounded-lg border border-slate-800 px-3 py-2">Restore queue is kept mock-ready and separated from active conversations.</div>
          </div>
        </Card>
        <Card title="Status" description="Archive health and integrity monitoring.">
          <div className="mt-4 space-y-3 text-sm text-slate-300">
            <div className="flex items-center justify-between rounded-lg border border-slate-800 px-3 py-2"><span>Checksum errors</span><Badge variant="success">0</Badge></div>
            <div className="flex items-center justify-between rounded-lg border border-slate-800 px-3 py-2"><span>Restore requests</span><Badge variant="info">Mock ready</Badge></div>
          </div>
        </Card>
      </div>
    </PageShell>
  );
}
