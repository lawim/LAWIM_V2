import { Badge, Button, Card, PageShell } from '@ui';

const workflowSteps = [
  { name: 'Intake', status: 'Ready', detail: 'Capture requests from web, admin, and assistant surfaces.' },
  { name: 'Brain routing', status: 'Ready', detail: 'Resolve intent and select the best execution path.' },
  { name: 'Escalation path', status: 'Ready', detail: 'Escalate to human review when confidence is below threshold.' }
];

export function WorkflowOrchestratorPage() {
  return (
    <PageShell
      eyebrow="Workflow"
      title="Workflow orchestration"
      description="Coordinate demand, approvals, and handoffs through one coherent operating layer."
      actions={
        <>
          <Button>Run preview</Button>
          <Button variant="secondary">Review playbook</Button>
        </>
      }
    >
      <div className="grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
        <Card title="Execution plan" description="The product experience now exposes the orchestration flow directly.">
          <div className="mt-4 space-y-3">
            {workflowSteps.map((step) => (
              <div key={step.name} className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4 text-sm text-slate-300">
                <div className="flex items-center justify-between gap-3">
                  <span className="font-medium text-white">{step.name}</span>
                  <Badge variant="success">Status: {step.status}</Badge>
                </div>
                <p className="mt-2 text-xs text-slate-400">{step.detail}</p>
              </div>
            ))}
          </div>
        </Card>
        <Card title="Operational context" description="Each workflow carries business intent and governance checkpoints.">
          <div className="mt-4 space-y-3 text-sm text-slate-300">
            <div className="rounded-2xl border border-slate-800 bg-slate-950/50 p-4">
              <p className="font-medium text-white">Escalation path</p>
              <p className="mt-2 text-xs text-slate-400">Low-confidence requests route to an operator queue before execution.</p>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/50 p-4">
              <p className="font-medium text-white">Governance guardrails</p>
              <p className="mt-2 text-xs text-slate-400">Every action remains observable and traceable through the admin console.</p>
            </div>
          </div>
        </Card>
      </div>
    </PageShell>
  );
}
