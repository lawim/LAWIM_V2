import { AgentAvailability, AgentHealth, type Agent } from './agent';

export interface AgentRoutingStep {
  agentId: string;
  agentName: string;
  intent: string;
  reason: string;
}

export interface AgentRegistrySnapshot {
  generatedAt: string;
  agents: Agent[];
}

export class AgentRegistry {
  private readonly agents = new Map<string, Agent>();

  register(agent: Agent) {
    this.agents.set(agent.id, agent);
    return agent;
  }

  registerMany(agents: Agent[]) {
    agents.forEach((agent) => this.register(agent));
    return this;
  }

  unregister(agentId: string) {
    const agent = this.agents.get(agentId);
    this.agents.delete(agentId);
    return agent;
  }

  update(agentId: string, patch: Partial<Agent>) {
    const current = this.agents.get(agentId);
    if (!current) {
      return undefined;
    }

    const updated = { ...current, ...patch };
    this.agents.set(agentId, updated);
    return updated;
  }

  get(agentId: string) {
    return this.agents.get(agentId);
  }

  list() {
    return [...this.agents.values()];
  }

  available() {
    return this.list().filter((agent) => agent.availability === AgentAvailability.Available);
  }

  healthy() {
    return this.list().filter((agent) => agent.health === AgentHealth.Healthy);
  }

  findByIntent(intent: string) {
    return this.list().filter((agent) => agent.supportedIntents.includes(intent) && agent.availability === AgentAvailability.Available);
  }

  findByModule(moduleName: string) {
    return this.list().filter((agent) => agent.supportedModules.includes(moduleName));
  }

  resolveIntent(intent: string, moduleName?: string) {
    const candidates = this.findByIntent(intent).filter((agent) => (moduleName ? agent.supportedModules.includes(moduleName) : true));

    return candidates.sort((left, right) => {
      const healthScore = scoreHealth(right.health) - scoreHealth(left.health);
      if (healthScore !== 0) {
        return healthScore;
      }
      return left.name.localeCompare(right.name);
    });
  }

  createRoutingPlan(intent: string, moduleName?: string): AgentRoutingStep[] {
    return this.resolveIntent(intent, moduleName).map((agent) => ({
      agentId: agent.id,
      agentName: agent.name,
      intent,
      reason: `${agent.description} • ${agent.supportedModules.join(', ')}`
    }));
  }

  snapshot(): AgentRegistrySnapshot {
    return {
      generatedAt: new Date().toISOString(),
      agents: this.list()
    };
  }
}

function scoreHealth(health: AgentHealth) {
  switch (health) {
    case AgentHealth.Healthy:
      return 3;
    case AgentHealth.Degraded:
      return 2;
    case AgentHealth.Offline:
      return 1;
    default:
      return 0;
  }
}

export function createAgentRegistry(agents: Agent[] = []) {
  return new AgentRegistry().registerMany(agents);
}
