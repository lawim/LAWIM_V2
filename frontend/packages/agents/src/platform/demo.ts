import {
  AgentAuthorization,
  AgentEventBus,
  AgentHistory,
  AgentLogger,
  AgentMemory,
  AgentMetrics,
  AgentPriority,
  AgentQueue,
  AgentRegistry,
  AgentScheduler,
  ApprovalQueue,
  ApprovalStatus,
  DelegationManager,
  DelegationStatus,
  ExecutionStatus,
  PolicyEngine,
  TaskMode,
  createApprovalRequest,
  createDefaultPolicies,
  createDelegationRequest,
  createTask,
  createAgentContext,
  type AgentContext,
  type AgentExecution,
  type AgentResult,
  type AgentTask,
  type ExecutionGraph,
  type ExecutionPipeline
} from '../core';
import { createAnalyticsAgent } from '../analytics';
import { createCommunicationAgent } from '../communication';
import { createCrmAgent } from '../crm';
import { createDeploymentAgent, createBackupAgent, createOperationsAgent } from '../operations';
import { createDocumentsAgent } from '../documents';
import { createKnowledgeAgent } from '../knowledge';
import { createMarketplaceAgent } from '../marketplace';
import { createMapAgent } from '../map';
import { createSecurityAgent } from '../security';
import { createWorkflowAgent } from '../workflow';

export interface MockAgentPlatform {
  context: AgentContext;
  eventBus: AgentEventBus;
  logger: AgentLogger;
  history: AgentHistory;
  metrics: AgentMetrics;
  audit: { record: (entry: { id: string; actor: string; action: string; target: string; outcome: string; timestamp: string; metadata?: Record<string, unknown> }) => void; list: () => Array<{ id: string; actor: string; action: string; target: string; outcome: string; timestamp: string; metadata?: Record<string, unknown> }> };
  memory: AgentMemory;
  policies: PolicyEngine;
  approvals: ApprovalQueue;
  delegations: DelegationManager;
  registry: AgentRegistry;
  queue: AgentQueue;
  tasks: AgentTask[];
  plan: { graph: ExecutionGraph; pipeline: ExecutionPipeline };
  executions: AgentExecution[];
  brainRouting: ReturnType<AgentRegistry['createRoutingPlan']>;
}

interface AuditStore {
  entries: Array<{ id: string; actor: string; action: string; target: string; outcome: string; timestamp: string; metadata?: Record<string, unknown> }>;
  record: (entry: { id: string; actor: string; action: string; target: string; outcome: string; timestamp: string; metadata?: Record<string, unknown> }) => void;
  list: () => Array<{ id: string; actor: string; action: string; target: string; outcome: string; timestamp: string; metadata?: Record<string, unknown> }>;
}

const DEMO_BASE = '2026-07-03T09:00:00.000Z';

function timestamp(offsetMinutes: number) {
  return new Date(Date.parse(DEMO_BASE) + offsetMinutes * 60_000).toISOString();
}

function createDemoTasks(): AgentTask[] {
  return [
    createTask({
      id: 'task-create-lead',
      title: 'Prepare CRM lead',
      description: 'Prepare a lead package for human approval.',
      agentId: 'agent-crm',
      intent: 'CreateLead',
      priority: AgentPriority.High,
      mode: TaskMode.Sequential,
      metadata: { sensitive: true, approvalReferenceId: 'approval-create-lead' }
    }),
    createTask({
      id: 'task-classify-document',
      title: 'Classify document set',
      description: 'Prepare a document classification proposal.',
      agentId: 'agent-documents',
      intent: 'ClassifyDocument',
      priority: AgentPriority.Normal,
      mode: TaskMode.Parallel,
      dependencies: ['task-create-lead'],
      metadata: { sensitive: true, approvalReferenceId: 'approval-classify-documents' }
    }),
    createTask({
      id: 'task-send-reminder',
      title: 'Prepare reminders',
      description: 'Prepare reminder content for approval.',
      agentId: 'agent-communication',
      intent: 'SendReminder',
      priority: AgentPriority.Normal,
      mode: TaskMode.Parallel,
      dependencies: ['task-create-lead'],
      approvedDelegations: ['delegation-send-reminder'],
      metadata: { sensitive: false, approvalReferenceId: 'approval-send-reminder' }
    }),
    createTask({
      id: 'task-create-backup',
      title: 'Prepare backup',
      description: 'Prepare a backup proposal for operations approval.',
      agentId: 'agent-backup',
      intent: 'CreateBackup',
      priority: AgentPriority.Critical,
      mode: TaskMode.Sequential,
      dependencies: ['task-classify-document'],
      metadata: { sensitive: true, approvalReferenceId: 'approval-create-backup' }
    }),
    createTask({
      id: 'task-generate-report',
      title: 'Generate analytics report',
      description: 'Prepare operational analytics for review.',
      agentId: 'agent-analytics',
      intent: 'GenerateReport',
      priority: AgentPriority.Normal,
      mode: TaskMode.Sequential,
      dependencies: ['task-create-backup'],
      metadata: { sensitive: false, approvalReferenceId: 'approval-generate-report' }
    }),
    createTask({
      id: 'task-knowledge-sync',
      title: 'Sync knowledge brief',
      description: 'Prepare a knowledge brief for dependent agents.',
      agentId: 'agent-knowledge',
      intent: 'RetrieveKnowledge',
      priority: AgentPriority.Low,
      mode: TaskMode.Conditional,
      dependencies: ['task-generate-report'],
      metadata: { sensitive: false, approvalReferenceId: 'approval-knowledge-sync' }
    }),
    createTask({
      id: 'task-route-map',
      title: 'Prepare route map',
      description: 'Prepare a spatial summary for a location decision.',
      agentId: 'agent-map',
      intent: 'PlanRoute',
      priority: AgentPriority.Low,
      mode: TaskMode.Conditional,
      dependencies: ['task-knowledge-sync'],
      metadata: { sensitive: false, approvalReferenceId: 'approval-route-map' }
    })
  ];
}

function createAuditStore(): AuditStore {
  const entries: AuditStore['entries'] = [];
  return {
    entries,
    record(entry) {
      entries.push(entry);
    },
    list() {
      return [...entries];
    }
  };
}

export function createMockAgentPlatform(): MockAgentPlatform {
  const eventBus = new AgentEventBus();
  const logger = new AgentLogger();
  const history = new AgentHistory();
  const metrics = new AgentMetrics();
  const audit = createAuditStore();
  const memory = new AgentMemory();
  const policies = new PolicyEngine(createDefaultPolicies());
  const approvals = new ApprovalQueue();
  const delegations = new DelegationManager();
  const registry = new AgentRegistry().registerMany([
    createCrmAgent(),
    createMarketplaceAgent(),
    createDocumentsAgent(),
    createCommunicationAgent(),
    createAnalyticsAgent(),
    createSecurityAgent(),
    createOperationsAgent(),
    createDeploymentAgent(),
    createBackupAgent(),
    createKnowledgeAgent(),
    createMapAgent(),
    createWorkflowAgent()
  ]);
  const queue = new AgentQueue();
  const authorization = new AgentAuthorization({ policyEngine: policies, approvals, delegations });
  const context = createAgentContext({
    brainSessionId: 'brain-session-demo',
    mode: 'business',
    permissions: [
      'crm:prepare',
      'crm:follow-up',
      'documents:classify',
      'documents:prepare',
      'communication:prepare',
      'communication:send',
      'analytics:read',
      'analytics:prepare',
      'security:review',
      'security:prepare',
      'operations:coordinate',
      'operations:prepare',
      'deployment:prepare',
      'backup:prepare',
      'knowledge:read',
      'knowledge:prepare',
      'maps:read',
      'maps:prepare',
      'workflow:prepare'
    ],
    approvedDelegations: ['delegation-send-reminder'],
    metadata: { brainControlled: true, source: 'mock-runtime' },
    now: DEMO_BASE
  });
  const tasks = createDemoTasks();
  queue.enqueueMany(tasks);
  const scheduler = new AgentScheduler();
  const plan = scheduler.buildPlan(tasks, 'lawim-agent-demo');
  const executions: AgentExecution[] = [];

  const approvalsToSeed = [
    createApprovalRequest({
      id: 'approval-create-lead',
      referenceId: 'approval-create-lead',
      title: 'Approve CRM lead preparation',
      description: 'Allow the CRM agent to prepare a lead proposal.',
      requestedBy: 'lawim-brain',
      targetAgentId: 'agent-crm',
      sensitive: true,
      createdAt: timestamp(0),
      updatedAt: timestamp(0)
    }),
    createApprovalRequest({
      id: 'approval-classify-documents',
      referenceId: 'approval-classify-documents',
      title: 'Approve document classification',
      description: 'Allow the Documents agent to classify incoming files.',
      requestedBy: 'lawim-brain',
      targetAgentId: 'agent-documents',
      sensitive: true,
      createdAt: timestamp(1),
      updatedAt: timestamp(1)
    }),
    createApprovalRequest({
      id: 'approval-create-backup',
      referenceId: 'approval-create-backup',
      title: 'Approve backup preparation',
      description: 'Allow the Backup agent to prepare a recovery plan.',
      requestedBy: 'lawim-brain',
      targetAgentId: 'agent-backup',
      sensitive: true,
      createdAt: timestamp(2),
      updatedAt: timestamp(2)
    }),
    createApprovalRequest({
      id: 'approval-marketplace-publish',
      referenceId: 'approval-marketplace-publish',
      title: 'Approve marketplace publication',
      description: 'A publication proposal waiting in the queue for human review.',
      requestedBy: 'lawim-brain',
      targetAgentId: 'agent-marketplace',
      sensitive: false,
      createdAt: timestamp(3),
      updatedAt: timestamp(3)
    })
  ];
  approvalsToSeed.forEach((approval, index) => {
    approvals.request(approval);
    if (index < 3) {
      approvals.approve(approval.id, 'lawim-brain', 'Approved for mock runtime');
    }
  });

  const delegationsToSeed = [
    createDelegationRequest({
      id: 'delegation-send-reminder',
      action: {
        id: 'delegation-action-send-reminder',
        name: 'Send automatic reminders',
        description: 'Prepare reminders for human approval.',
        targetAgentId: 'agent-communication',
        intent: 'SendReminder',
        critical: false
      },
      requestedBy: 'lawim-brain',
      status: DelegationStatus.Pending,
      requestedAt: timestamp(3)
    }),
    createDelegationRequest({
      id: 'delegation-critical-release',
      action: {
        id: 'delegation-action-critical-release',
        name: 'Critical deployment delegation',
        description: 'Forbidden critical action.',
        targetAgentId: 'agent-deployment',
        intent: 'PrepareRelease',
        critical: true
      },
      requestedBy: 'lawim-brain',
      status: DelegationStatus.Inactive,
      requestedAt: timestamp(4)
    }),
    createDelegationRequest({
      id: 'delegation-marketplace-publication',
      action: {
        id: 'delegation-action-marketplace-publication',
        name: 'Marketplace publication',
        description: 'A non-critical publication proposal waiting for human approval.',
        targetAgentId: 'agent-marketplace',
        intent: 'PublishOffer',
        critical: false
      },
      requestedBy: 'lawim-brain',
      status: DelegationStatus.Pending,
      requestedAt: timestamp(5)
    })
  ];
  delegationsToSeed.forEach((delegation) => {
    const created = delegations.request(delegation);
    if (created.status === DelegationStatus.Pending) {
      delegations.approve(created.id, 'lawim-brain', 'Approved for mock runtime');
    }
  });

  for (const [index, task] of tasks.entries()) {
    const agent = registry.get(task.agentId);
    if (!agent) {
      continue;
    }

    const decision = authorization.authorize(agent, task, context);
    if (!decision.allowed && decision.requiresApproval && decision.approvalReferenceId) {
      const approval = approvals.findByReference(decision.approvalReferenceId);
      if (approval && approval.status !== ApprovalStatus.Approved) {
        approvals.approve(approval.id, 'lawim-brain', 'Approved in mock runtime');
      }
    }

    const result = agent.execute(task, context) as AgentResult;
    const startedAt = timestamp(10 + index * 5);
    const endedAt = timestamp(11 + index * 5);
    const execution: AgentExecution = {
      id: `execution-${task.id}`,
      agentId: agent.id,
      taskId: task.id,
      status: ExecutionStatus.Completed,
      startedAt,
      endedAt,
      attempts: 1,
      timeline: [
        { at: startedAt, event: 'execution-started', detail: task.intent },
        { at: endedAt, event: 'execution-completed', detail: result.summary }
      ],
      result
    };

    executions.push(execution);
    history.record({
      id: execution.id,
      agentId: execution.agentId,
      taskId: execution.taskId,
      status: execution.status,
      summary: result.summary,
      startedAt: execution.startedAt,
      endedAt: execution.endedAt ?? endedAt,
      durationMs: 60,
      retries: 0,
      metadata: { intent: task.intent }
    });
    metrics.recordExecution(execution.status, 60, 0);
    logger.info(agent.id, result.summary, { taskId: task.id, intent: task.intent });
    audit.record({
      id: `audit-${execution.id}`,
      actor: 'lawim-brain',
      action: 'seed-execution',
      target: task.id,
      outcome: execution.status,
      timestamp: endedAt,
      metadata: { intent: task.intent }
    });
    memory.rememberExecution({
      id: execution.id,
      agentId: execution.agentId,
      taskId: execution.taskId,
      status: execution.status,
      summary: result.summary,
      timestamp: endedAt
    });
    memory.rememberSuccess(result.summary);
    memory.rememberRecommendation(result.recommendations[0] ?? `${agent.name} proposal stored for review.`);
  }

  logger.info('lawim-brain', 'Mock agent platform seeded', {
    agents: registry.list().length,
    tasks: tasks.length
  });

  return {
    context,
    eventBus,
    logger,
    history,
    metrics,
    audit,
    memory,
    policies,
    approvals,
    delegations,
    registry,
    queue,
    tasks,
    plan,
    executions,
    brainRouting: registry.createRoutingPlan('CreateLead')
  };
}

export function createMockBrainContext() {
  return createAgentContext({
    brainSessionId: 'brain-session-demo',
    mode: 'business',
    permissions: [],
    approvedDelegations: [],
    metadata: { brainControlled: true }
  });
}
