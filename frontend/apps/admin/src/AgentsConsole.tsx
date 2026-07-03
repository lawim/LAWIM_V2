import { Badge, Card, PageShell, Button } from '@ui';
import { AgentDashboard, createMockAgentPlatform } from '@agents';

export function AgentsConsolePage() {
  const platform = createMockAgentPlatform();

  return (
    <PageShell
      eyebrow="Intelligent Agents"
      title="LAWIM Agent Platform"
      description="The official coordination layer for proposal-driven agents, approval queues, and Brain-controlled delegation."
      actions={
        <>
          <Button>Review approvals</Button>
          <Button variant="secondary">Inspect registry</Button>
        </>
      }
    >
      <div className="grid gap-6 xl:grid-cols-[0.95fr_1.05fr]">
        <Card title="Platform contract" description="Agents coordinate only. The Brain keeps all business authority.">
          <div className="mt-4 flex flex-wrap gap-2">
            <Badge variant="info">Mock runtime enabled</Badge>
            <Badge variant="success">{platform.registry.list().length} agents</Badge>
            <Badge variant="warning">{platform.approvals.pending().length} pending approvals</Badge>
          </div>
          <p className="mt-4 text-sm leading-6 text-slate-300">
            Every agent proposal remains blocked until the LAWIM Brain authorizes execution or a human reviewer approves the delegation.
          </p>
        </Card>
        <Card title="Brain routing" description="The Brain inspects the registry before delegating work.">
          <div className="mt-4 space-y-3">
            {platform.brainRouting.map((step) => (
              <div key={step.agentId} className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4 text-sm text-slate-300">
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <span className="font-medium text-white">{step.agentName}</span>
                  <Badge variant="info">{step.intent}</Badge>
                </div>
                <p className="mt-2 text-xs text-slate-400">{step.reason}</p>
              </div>
            ))}
          </div>
        </Card>
      </div>

      <AgentDashboard platform={platform} />
    </PageShell>
  );
}
