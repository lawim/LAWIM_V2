export interface DigitalTwinMilestone {
  id: string;
  title: string;
  status: 'pending' | 'in-progress' | 'complete';
  completedAt?: string;
}

export interface DigitalTwinProject {
  id: string;
  name: string;
  description: string;
  state: 'draft' | 'active' | 'paused' | 'complete';
  progress: number;
  milestones: DigitalTwinMilestone[];
  metrics: Record<string, number>;
  timeline: Array<{ id: string; title: string; timestamp: string }>;
  createdAt: string;
}

export interface DigitalTwinSnapshot {
  id: string;
  name: string;
  progress: number;
  state: string;
  metrics: Record<string, number>;
}

export interface DigitalTwinDashboardView {
  projects: DigitalTwinSnapshot[];
}

export class DigitalTwin {
  constructor(private readonly project: DigitalTwinProject) {}

  snapshot(): DigitalTwinSnapshot {
    return {
      id: this.project.id,
      name: this.project.name,
      progress: this.project.progress,
      state: this.project.state,
      metrics: this.project.metrics
    };
  }
}

export class DigitalTwinDashboard {
  constructor(private readonly twins: DigitalTwin[]) {}

  build(): DigitalTwinDashboardView {
    return { projects: this.twins.map((twin) => twin.snapshot()) };
  }
}
