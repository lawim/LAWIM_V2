import { Badge, Card, PageShell } from '@ui';

const drives = [
  { name: 'Drive 1', kind: 'Video/Audio A', used: '42%', status: 'healthy' },
  { name: 'Drive 2', kind: 'Video/Audio B', used: '37%', status: 'healthy' },
  { name: 'Drive 3', kind: 'Video/Audio C', used: '31%', status: 'healthy' },
  { name: 'Drive 4', kind: 'Original photos', used: '26%', status: 'healthy' },
  { name: 'Drive 5', kind: 'Documents', used: '19%', status: 'healthy' },
  { name: 'Drive 6', kind: 'PostgreSQL + registry', used: '14%', status: 'healthy' },
  { name: 'Drive 7', kind: 'Cold archive', used: '8%', status: 'healthy' },
  { name: 'Drive 8', kind: 'Overflow', used: '11%', status: 'warning' },
  { name: 'Drive 9', kind: 'Quarantine/restore', used: '6%', status: 'healthy' },
  { name: 'Drive 10', kind: 'Critical replication', used: '13%', status: 'healthy' },
];

export function BackupCenterPage() {
  return (
    <PageShell
      eyebrow="Backup Center"
      title="Admin backup and storage control center"
      description="Mocked operational view for the AAC-B2 storage platform."
    >
      <div className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
        <Card title="Global storage overview" description="OVH hot storage plus the distributed backup fabric.">
          <div className="mt-4 grid gap-3 md:grid-cols-2">
            <div className="rounded-xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="text-sm text-slate-400">OVH hot storage</div>
              <div className="mt-2 text-2xl font-semibold text-white">78%</div>
            </div>
            <div className="rounded-xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="text-sm text-slate-400">Backup center</div>
              <div className="mt-2 text-2xl font-semibold text-white">41%</div>
            </div>
            <div className="rounded-xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="text-sm text-slate-400">External disk</div>
              <div className="mt-2 text-2xl font-semibold text-white">24%</div>
            </div>
            <div className="rounded-xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="text-sm text-slate-400">Restore queue</div>
              <div className="mt-2 text-2xl font-semibold text-white">3 pending</div>
            </div>
          </div>
        </Card>
        <Card title="Operations" description="Restore requests, alerts, and lifecycle state.">
          <div className="mt-4 space-y-3 text-sm text-slate-300">
            <div className="flex items-center justify-between rounded-lg border border-slate-800 px-3 py-2"><span>Last backup</span><Badge variant="success">2 min ago</Badge></div>
            <div className="flex items-center justify-between rounded-lg border border-slate-800 px-3 py-2"><span>Last sync</span><Badge variant="info">7 min ago</Badge></div>
            <div className="flex items-center justify-between rounded-lg border border-slate-800 px-3 py-2"><span>Checksum alerts</span><Badge variant="warning">1</Badge></div>
            <div className="flex items-center justify-between rounded-lg border border-slate-800 px-3 py-2"><span>Hot/Warm/Cold</span><Badge variant="success">Balanced</Badge></div>
          </div>
        </Card>
      </div>

      <div className="mt-6">
        <Card title="Distributed Google Drive overview" description="Configuration placeholder for the ten drives.">
          <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
          {drives.map((drive) => (
            <div key={drive.name} className="rounded-xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="flex items-center justify-between">
                <div className="font-semibold text-white">{drive.name}</div>
                <Badge variant={drive.status === 'warning' ? 'warning' : 'success'}>{drive.status}</Badge>
              </div>
              <div className="mt-2 text-sm text-slate-400">{drive.kind}</div>
              <div className="mt-3 text-sm text-slate-300">Usage {drive.used}</div>
            </div>
          ))}
          </div>
        </Card>
      </div>
    </PageShell>
  );
}
