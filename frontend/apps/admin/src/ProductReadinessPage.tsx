import { Badge, Card, PageShell } from '@ui';

const metrics = [
  { label: 'Routes', value: '24', detail: 'Core business and admin paths are linked.' },
  { label: 'Packages', value: '11', detail: 'Shared packages cover the full experience stack.' },
  { label: 'Test coverage', value: 'Focused', detail: 'Critical shell, SDK, and agent journeys are covered.' },
  { label: 'Build status', value: 'Healthy', detail: 'The frontend build remains production-ready.' }
];

export function ProductReadinessPage() {
  return (
    <PageShell
      eyebrow="Readiness"
      title="Product readiness"
      description="Summarize the current state of the product experience, modules, and delivery confidence."
    >
      <div className="grid gap-6 md:grid-cols-2">
        {metrics.map((metric) => (
          <Card key={metric.label} title={metric.label} description={metric.detail}>
            <div className="mt-4 flex items-center gap-2 text-sm text-slate-300">
              <Badge variant="info">{metric.value}</Badge>
            </div>
          </Card>
        ))}
      </div>
    </PageShell>
  );
}
