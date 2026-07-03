export interface BrainIntent {
  type: string;
  description: string;
  payload?: Record<string, unknown>;
}

export interface BrainContext {
  sessionId: string;
  userId?: string;
  mode: 'free' | 'guided' | 'business' | 'admin' | 'documentary';
  metadata?: Record<string, unknown>;
}

export interface BrainModule {
  name: string;
  description: string;
  capabilities: string[];
  supportedIntents: string[];
  priority: number;
  health: 'healthy' | 'degraded' | 'offline';
  availability: 'available' | 'unavailable';
  execute: (intent: BrainIntent, context: BrainContext) => Promise<unknown>;
}

export interface BrainExecutionPlanStep {
  module: string;
  intent: string;
  reason: string;
}

export interface BrainExecutionPlan {
  steps: BrainExecutionPlanStep[];
  summary: string;
}

export interface BrainResult {
  plan: BrainExecutionPlan;
  finalMessage: string;
  outputs: Array<{ module: string; result: unknown }>;
}

export interface BrainEvent {
  type: 'plan-built' | 'module-selected' | 'module-executed' | 'completed';
  payload?: Record<string, unknown>;
}

export interface BrainSession {
  id: string;
  createdAt: string;
  context: BrainContext;
  events: BrainEvent[];
}

export class BrainRegistry {
  private modules: BrainModule[] = [];

  register(module: BrainModule) {
    this.modules.push(module);
  }

  list() {
    return this.modules;
  }
}

export class BrainRouter {
  selectModules(intent: BrainIntent, registry: BrainRegistry, context: BrainContext) {
    const relevantModules = registry.list().filter((module) => module.supportedIntents.includes(intent.type) && module.availability === 'available');
    return relevantModules.sort((a, b) => a.priority - b.priority).map((module) => ({
      module: module.name,
      intent: intent.type,
      reason: `${module.description} • ${context.mode}`
    }));
  }
}

export class BrainOrchestrator {
  private readonly router = new BrainRouter();

  constructor(private readonly registry: BrainRegistry) {}

  async orchestrate(intent: BrainIntent, context: BrainContext): Promise<BrainResult> {
    const steps = this.router.selectModules(intent, this.registry, context);
    const plan: BrainExecutionPlan = {
      steps,
      summary: `${intent.description} routed through ${steps.length} module(s)`
    };

    const outputs = [] as Array<{ module: string; result: unknown }>;
    for (const step of steps) {
      const module = this.registry.list().find((entry) => entry.name === step.module);
      if (module) {
        outputs.push({ module: module.name, result: await module.execute(intent, context) });
      }
    }

    const mockEnabled = import.meta.env?.VITE_LAWIM_USE_MOCKS === 'true';
    const finalMessage = mockEnabled
      ? `${intent.description} executed in mock mode with ${plan.steps.length} module(s).`
      : `${intent.description} handled with ${plan.steps.length} module(s).`;

    return { plan, finalMessage, outputs };
  }
}

export class IntentEngine {
  parse(text: string): BrainIntent {
    const lowered = text.toLowerCase();
    if (lowered.includes('estimate')) return { type: 'EstimateProperty', description: 'Estimate request' };
    if (lowered.includes('search')) return { type: 'SearchProperty', description: 'Search request' };
    if (lowered.includes('document')) return { type: 'GenerateDocument', description: 'Document request' };
    if (lowered.includes('workflow')) return { type: 'CreateWorkflow', description: 'Workflow request' };
    if (lowered.includes('project')) return { type: 'AnalyzeProject', description: 'Project analysis request' };
    return { type: 'OpenConversation', description: 'General conversation request' };
  }
}

export function createDemoIntent(type: string, description: string): BrainIntent {
  return { type, description };
}

export function createDemoBrainContext(): BrainContext {
  return {
    sessionId: 'session-demo',
    mode: 'business',
    metadata: { source: 'demo' }
  };
}
