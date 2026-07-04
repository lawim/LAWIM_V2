import { Badge, Card, PageShell } from '@ui';

export function StorageHealthPage() {
  return (
    <PageShell
      eyebrow="Storage Health"
      title="Storage health and drive distribution"
      description="Monitor the mock OVH/Drive architecture and archive routing health."
    >
      <div className="grid gap-6 xl:grid-cols-[1.4fr_0.6fr]">
        <Card title="Drive route health" description="Drive 8 is reserved for conversation archives and index storage.">
          <div className="mt-4 space-y-3 text-sm text-slate-300">
            <div className="rounded-lg border border-slate-800 px-3 py-2">Drive 1-5: media and assets.</div>
            <div className="rounded-lg border border-slate-800 px-3 py-2">Drive 6: PostgreSQL, Media Registry, Conversation Registry.</div>
            <div className="rounded-lg border border-slate-800 px-3 py-2">Drive 8: archived conversations and archive index.</div>
          </div>
        </Card>
        <Card title="Policy snapshot" description="Storage and bandwidth policies are mock configured.">
          <div className="mt-4 text-sm text-slate-300">
            <p className="rounded-lg border border-slate-800 px-3 py-2">Bandwidth policy: throttled for archival jobs.</p>
            <p className="rounded-lg border border-slate-800 px-3 py-2">Thumbnail retention enabled for cold archives.</p>
          </div>
        </Card>
      </div>
    </PageShell>
  );
}
