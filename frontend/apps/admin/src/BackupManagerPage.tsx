import { Badge, Card, PageShell } from '@ui';

export function BackupManagerPage() {
  return (
    <PageShell
      eyebrow="Backup Manager"
      title="Simplified manager console"
      description="Operational snapshot for backup and restore coordination."
    >
      <div className="grid gap-6 md:grid-cols-2">
        <Card title="Latest backup" description="The latest backup completed successfully.">
          <div className="mt-4 space-y-2 text-sm text-slate-300">
            <div className="flex items-center justify-between"><span>Backup status</span><Badge variant="success">Healthy</Badge></div>
            <div className="flex items-center justify-between"><span>Last sync</span><Badge variant="info">7 min ago</Badge></div>
          </div>
        </Card>
        <Card title="Restore requests" description="Pending restore requests are visible and prioritized.">
          <div className="mt-4 space-y-2 text-sm text-slate-300">
            <div className="flex items-center justify-between"><span>Pending</span><Badge variant="warning">3</Badge></div>
            <div className="flex items-center justify-between"><span>Critical</span><Badge variant="success">0</Badge></div>
          </div>
        </Card>
      </div>
    </PageShell>
  );
}
