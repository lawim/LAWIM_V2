import { Badge, Card, PageShell } from '@ui';

const panels = [
  { name: 'Brain decisions', status: 'Healthy', detail: 'Routing plans are consistent across demo and mock traffic.' },
  { name: 'Knowledge calls', status: 'Healthy', detail: 'Retrieval remains available for discovery and explainability workflows.' },
  { name: 'Agent calls', status: 'Watch', detail: 'Approval queues are active and ready for review.' },
  { name: 'Conversation pipeline', status: 'Healthy', detail: 'Intent analysis is producing stable summaries.' }
];

export function ObservabilityPage() {
  return (
    <PageShell
      eyebrow="Observability"
      title="Observability console"
      description="Visualize execution health, workflow steps, and decision traces across LAWIM modules."
    >
      <div className="grid gap-6 md:grid-cols-2">
        {panels.map((panel) => (
          <Card key={panel.name} title={panel.name} description={panel.detail}>
            <div className="mt-4 flex items-center gap-2 text-sm text-slate-300">
              <Badge variant={panel.status === 'Watch' ? 'warning' : 'success'}>{panel.status}</Badge>
            </div>
          </Card>
        ))}
      </div>
    </PageShell>
  );
}
