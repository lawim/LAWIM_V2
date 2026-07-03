import { Badge, Card } from '@ui';
import { ApprovalDashboard } from './ApprovalDashboard';
import { ApprovalStatus, ExecutionStatus, type AgentPriority, type AgentTask } from '../core';
import type { MockAgentPlatform } from '../platform';

export interface AgentDashboardProps {
  platform: MockAgentPlatform;
}

function statusVariant(status: string) {
  switch (status) {
    case 'healthy':
    case 'available':
    case ExecutionStatus.Completed:
    case ApprovalStatus.Approved:
      return 'success';
    case 'degraded':
    case 'offline':
    case 'unavailable':
    case ExecutionStatus.WaitingApproval:
    case ApprovalStatus.Pending:
      return 'warning';
    case ExecutionStatus.Failed:
    case ExecutionStatus.RolledBack:
    case ApprovalStatus.Rejected:
    case ApprovalStatus.Revoked:
    case ApprovalStatus.Expired:
      return 'warning';
    default:
      return 'default';
  }
}

function taskPriorityLabel(priority: AgentPriority) {
  return priority >= 4 ? 'critical' : priority >= 3 ? 'high' : priority >= 2 ? 'normal' : 'low';
}

function renderTask(task: AgentTask) {
  return (
    <div key={task.id} className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
      <div className="flex items-center justify-between gap-3">
        <div>
          <p className="font-medium text-white">{task.title}</p>
          <p className="text-xs text-slate-400">{task.description}</p>
        </div>
        <Badge variant={task.priority >= 3 ? 'warning' : 'default'}>{taskPriorityLabel(task.priority)}</Badge>
      </div>
      <div className="mt-3 flex flex-wrap gap-2 text-xs text-slate-400">
        <span>Agent: {task.agentId}</span>
        <span>Intent: {task.intent}</span>
        <span>Status: {task.status}</span>
      </div>
    </div>
  );
}

export function AgentDashboard({ platform }: AgentDashboardProps) {
  const registry = platform.registry.list();
  const healthy = platform.registry.healthy();
  const available = platform.registry.available();
  const metrics = platform.metrics.snapshot();
  const history = platform.history.list();
  const graph = platform.plan.graph;
  const pipeline = platform.plan.pipeline;
  const executionTimeline = history.slice(-5);
  const logs = platform.logger.list().slice(-5);
  const policies = platform.policies.describe();
  const delegations = platform.delegations.list();
  const queue = platform.queue.list();

  return (
    <div className="space-y-6">
      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
        <Card title="Agent Registry" description="Registered agents available to the Brain.">
          <div className="mt-4 text-3xl font-semibold text-white">{registry.length}</div>
          <p className="mt-2 text-sm text-slate-400">All agents coordinate only, they do not decide business outcomes.</p>
        </Card>
        <Card title="Agent Health" description="Healthy agents and availability snapshot.">
          <div className="mt-4 flex gap-2">
            <Badge variant="success">{healthy.length} healthy</Badge>
            <Badge variant="info">{available.length} available</Badge>
          </div>
          <p className="mt-3 text-sm text-slate-400">Restricted agents remain visible but cannot self-authorize.</p>
        </Card>
        <Card title="Execution Metrics" description="Observed execution performance from the mock runtime.">
          <div className="mt-4 text-3xl font-semibold text-white">{Math.round(metrics.successRate * 100)}%</div>
          <p className="mt-2 text-sm text-slate-400">Success rate with {metrics.retries} retries and {metrics.executions} executions.</p>
        </Card>
        <Card title="Approval Queue" description="Sensitive actions waiting for human oversight.">
          <div className="mt-4 text-3xl font-semibold text-white">{platform.approvals.pending().length}</div>
          <p className="mt-2 text-sm text-slate-400">Critical delegations stay blocked by policy.</p>
        </Card>
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.15fr_0.85fr]">
        <Card title="Registry" description="Detailed registry entries with supported intents and modules.">
          <div className="mt-4 grid gap-3">
            {registry.map((agent) => (
              <div key={agent.id} className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <div>
                    <p className="font-medium text-white">{agent.name}</p>
                    <p className="text-xs text-slate-400">{agent.description}</p>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    <Badge variant={statusVariant(agent.health)}>{agent.health}</Badge>
                    <Badge variant={statusVariant(agent.availability)}>{agent.availability}</Badge>
                  </div>
                </div>
                <div className="mt-3 flex flex-wrap gap-2 text-xs text-slate-400">
                  <span>Intents: {agent.supportedIntents.join(', ')}</span>
                  <span>Modules: {agent.supportedModules.join(', ')}</span>
                  <span>Dependencies: {agent.dependencies.join(', ') || 'none'}</span>
                </div>
              </div>
            ))}
          </div>
        </Card>
        <Card title="Execution Graph" description="Execution graph and pipeline generated from mock tasks.">
          <div className="mt-4 space-y-4 text-sm text-slate-300">
            <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
              <p className="font-medium text-white">Nodes</p>
              <div className="mt-2 flex flex-wrap gap-2">
                {graph.nodes.map((node) => (
                  <Badge key={node.id} variant="info">
                    {node.taskId}
                  </Badge>
                ))}
              </div>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
              <p className="font-medium text-white">Edges</p>
              <ul className="mt-2 space-y-1 text-xs text-slate-400">
                {graph.edges.map((edge) => (
                  <li key={`${edge.from}-${edge.to}`}>
                    {edge.from} → {edge.to}
                  </li>
                ))}
              </ul>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
              <p className="font-medium text-white">Pipeline stages</p>
              <div className="mt-2 space-y-2">
                {pipeline.stages.map((stage) => (
                  <div key={stage.id} className="flex flex-wrap items-center gap-2 text-xs text-slate-400">
                    <Badge variant={stage.parallel ? 'success' : 'default'}>{stage.parallel ? 'parallel' : 'sequential'}</Badge>
                    <span>{stage.name}</span>
                    <span>{stage.taskIds.join(', ')}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </Card>
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.05fr_0.95fr]">
        <Card title="Running Tasks" description="Queued tasks ready for Brain-controlled delegation.">
          <div className="mt-4 grid gap-3">{queue.map(renderTask)}</div>
        </Card>
        <Card title="Delegations and Policies" description="Delegation states and policy constraints.">
          <div className="mt-4 space-y-4 text-sm text-slate-300">
            <div className="grid gap-3">
              {delegations.map((delegation) => (
                <div key={delegation.id} className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
                  <div className="flex flex-wrap items-center justify-between gap-3">
                    <div>
                      <p className="font-medium text-white">{delegation.action.name}</p>
                      <p className="text-xs text-slate-400">{delegation.action.description}</p>
                    </div>
                    <Badge variant={delegation.status === 'approved' ? 'success' : delegation.status === 'pending' ? 'warning' : 'default'}>
                      {delegation.status}
                    </Badge>
                  </div>
                  <p className="mt-2 text-xs text-slate-500">Critical: {String(delegation.action.critical)}</p>
                </div>
              ))}
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
              <p className="font-medium text-white">Policies</p>
              <div className="mt-2 grid gap-2 text-xs text-slate-400">
                {policies.map((policy) => (
                  <div key={policy.id} className="flex flex-wrap items-center gap-2">
                    <Badge variant="info">{policy.name}</Badge>
                    <span>
                      {policy.rules} rules • {policy.constraints} constraints • {policy.businessRestrictions} restrictions
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </Card>
      </div>

      <ApprovalDashboard approvals={platform.approvals} />

      <div className="grid gap-6 xl:grid-cols-[1fr_1fr]">
        <Card title="Agent History" description="Recent executions captured by the observability layer.">
          <div className="mt-4 space-y-3">
            {executionTimeline.map((entry) => (
              <div key={entry.id} className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4 text-sm text-slate-300">
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <span className="font-medium text-white">{entry.agentId}</span>
                  <Badge variant={statusVariant(entry.status)}>{entry.status}</Badge>
                </div>
                <p className="mt-2 text-xs text-slate-400">{entry.summary}</p>
              </div>
            ))}
          </div>
        </Card>
        <Card title="Agent Metrics" description="Success, failure, and timing statistics.">
          <div className="mt-4 grid grid-cols-2 gap-3 text-sm">
            <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-3">
              <div className="text-slate-500">Success rate</div>
              <div className="mt-1 text-lg font-semibold text-emerald-300">{Math.round(metrics.successRate * 100)}%</div>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-3">
              <div className="text-slate-500">Failure rate</div>
              <div className="mt-1 text-lg font-semibold text-amber-300">{Math.round(metrics.failureRate * 100)}%</div>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-3">
              <div className="text-slate-500">Average duration</div>
              <div className="mt-1 text-lg font-semibold text-white">{Math.round(metrics.averageDurationMs)}ms</div>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-3">
              <div className="text-slate-500">Retries</div>
              <div className="mt-1 text-lg font-semibold text-white">{metrics.retries}</div>
            </div>
          </div>
        </Card>
      </div>

      <Card title="Agent Logs" description="Runtime logs emitted by the mock runtime.">
        <div className="mt-4 space-y-3">
          {logs.map((entry) => (
            <div key={entry.id} className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4 text-sm text-slate-300">
              <div className="flex flex-wrap items-center justify-between gap-3">
                <span>{entry.source}</span>
                <Badge variant={entry.level === 'error' ? 'warning' : 'info'}>{entry.level}</Badge>
              </div>
              <p className="mt-2 text-xs text-slate-400">{entry.message}</p>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
