import type { AgentTask } from './tasks';

export enum AgentHealth {
  Healthy = 'healthy',
  Degraded = 'degraded',
  Offline = 'offline'
}

export enum AgentStatus {
  Idle = 'idle',
  Ready = 'ready',
  Running = 'running',
  WaitingApproval = 'waiting-approval',
  Succeeded = 'succeeded',
  Failed = 'failed',
  Paused = 'paused',
  Revoked = 'revoked'
}

export enum AgentAvailability {
  Available = 'available',
  Unavailable = 'unavailable',
  Restricted = 'restricted'
}

export enum AgentPriority {
  Low = 1,
  Normal = 2,
  High = 3,
  Critical = 4
}

export interface AgentCapability {
  id: string;
  name: string;
  description: string;
  intents: string[];
  modules: string[];
  requiresApproval?: boolean;
  canDelegate?: boolean;
}

export interface AgentContext {
  brainSessionId: string;
  mode: 'free' | 'guided' | 'business' | 'admin' | 'documentary';
  userId?: string;
  conversationId?: string;
  workspaceId?: string;
  permissions: string[];
  approvedDelegations: string[];
  metadata?: Record<string, unknown>;
  now?: string;
  emit?: (event: { type: string; payload?: Record<string, unknown> }) => void;
}

export interface AgentArtifact {
  id: string;
  name: string;
  type: string;
  content: string;
  metadata?: Record<string, unknown>;
}

export interface AgentResult {
  success: boolean;
  status: AgentStatus;
  summary: string;
  recommendations: string[];
  artifacts: AgentArtifact[];
  nextSteps: string[];
  metadata: Record<string, unknown>;
}

export interface Agent {
  id: string;
  name: string;
  description: string;
  version: string;
  capabilities: AgentCapability[];
  permissions: string[];
  health: AgentHealth;
  availability: AgentAvailability;
  supportedIntents: string[];
  supportedModules: string[];
  dependencies: string[];
  execute: (task: AgentTask, context: AgentContext) => Promise<AgentResult> | AgentResult;
}

export interface CreateAgentDefinitionInput {
  id: string;
  name: string;
  description: string;
  version?: string;
  capabilities: AgentCapability[];
  permissions?: string[];
  health?: AgentHealth;
  availability?: AgentAvailability;
  supportedIntents?: string[];
  supportedModules?: string[];
  dependencies?: string[];
  execute?: (task: AgentTask, context: AgentContext) => Promise<AgentResult> | AgentResult;
}

export interface DomainAgentBlueprint {
  id: string;
  name: string;
  description: string;
  module: string;
  capabilities: string[];
  permissions?: string[];
  supportedIntents: string[];
  dependencies?: string[];
  health?: AgentHealth;
  availability?: AgentAvailability;
  version?: string;
  summary?: string;
  recommendations?: string[];
  nextSteps?: string[];
}

function createTimestamp(context: AgentContext) {
  return context.now ?? new Date().toISOString();
}

export function createAgentCapability(
  id: string,
  name: string,
  description: string,
  modules: string[],
  intents: string[],
  overrides: Partial<AgentCapability> = {}
): AgentCapability {
  return {
    id,
    name,
    description,
    modules,
    intents,
    ...overrides
  };
}

export function createAgentResult(overrides: Partial<AgentResult> & Pick<AgentResult, 'summary'>): AgentResult {
  return {
    success: overrides.success ?? true,
    status: overrides.status ?? AgentStatus.Succeeded,
    summary: overrides.summary,
    recommendations: overrides.recommendations ?? [],
    artifacts: overrides.artifacts ?? [],
    nextSteps: overrides.nextSteps ?? [],
    metadata: overrides.metadata ?? {}
  };
}

export function createAgentContext(overrides: Partial<AgentContext> = {}): AgentContext {
  return {
    brainSessionId: overrides.brainSessionId ?? 'brain-session-demo',
    mode: overrides.mode ?? 'business',
    permissions: overrides.permissions ?? [],
    approvedDelegations: overrides.approvedDelegations ?? [],
    metadata: overrides.metadata ?? {},
    now: overrides.now ?? new Date().toISOString(),
    ...overrides
  };
}

export function createAgentDefinition(input: CreateAgentDefinitionInput): Agent {
  return {
    id: input.id,
    name: input.name,
    description: input.description,
    version: input.version ?? '1.0.0',
    capabilities: input.capabilities,
    permissions: input.permissions ?? [],
    health: input.health ?? AgentHealth.Healthy,
    availability: input.availability ?? AgentAvailability.Available,
    supportedIntents: input.supportedIntents ?? input.capabilities.flatMap((capability) => capability.intents),
    supportedModules: input.supportedModules ?? input.capabilities.flatMap((capability) => capability.modules),
    dependencies: input.dependencies ?? [],
    execute: input.execute ?? ((task, context) => createAgentResult({
      summary: `${input.name} prepared coordination for ${task.intent} at ${createTimestamp(context)}`,
      recommendations: [`Review the ${input.name.toLowerCase()} recommendation before release.`],
      nextSteps: [`Confirm delegated action for ${task.title}.`],
      metadata: {
        agentId: input.id,
        taskId: task.id,
        intent: task.intent,
        module: task.agentId
      }
    }))
  };
}

export function createDomainAgent(blueprint: DomainAgentBlueprint): Agent {
  return createAgentDefinition({
    id: blueprint.id,
    name: blueprint.name,
    description: blueprint.description,
    version: blueprint.version ?? '1.0.0',
    capabilities: blueprint.capabilities.map((capability, index) =>
      createAgentCapability(
        `${blueprint.id}-capability-${index + 1}`,
        capability,
        `${blueprint.name} capability: ${capability}`,
        [blueprint.module],
        blueprint.supportedIntents
      )
    ),
    permissions: blueprint.permissions ?? [],
    health: blueprint.health ?? AgentHealth.Healthy,
    availability: blueprint.availability ?? AgentAvailability.Available,
    supportedIntents: blueprint.supportedIntents,
    supportedModules: [blueprint.module],
    dependencies: blueprint.dependencies ?? [],
    execute: (task, context) =>
      createAgentResult({
        summary: blueprint.summary ?? `${blueprint.name} prepared coordination for ${task.intent}`,
        recommendations: blueprint.recommendations ?? [
          `${blueprint.name} keeps the action in proposal mode until the Brain authorizes execution.`
        ],
        nextSteps: blueprint.nextSteps ?? [
          `Route ${task.title} through human approval if the delegation is sensitive.`,
          `Record the Brain decision before execution.`
        ],
        metadata: {
          agentId: blueprint.id,
          taskId: task.id,
          intent: task.intent,
          module: blueprint.module,
          timestamp: createTimestamp(context)
        }
      })
  });
}
