import { describe, expect, it } from 'vitest';
import { DigitalTwin, type DigitalTwinProject, DigitalTwinDashboard } from '../packages/digital-twin/src';

describe('Digital Twin', () => {
  it('aggregates project metrics into a dashboard snapshot', () => {
    const project: DigitalTwinProject = {
      id: 'p-1',
      name: 'Luxury Launch',
      description: 'Launch a premium property campaign',
      state: 'active',
      progress: 62,
      milestones: [
        { id: 'm-1', title: 'Discovery', status: 'complete', completedAt: new Date().toISOString() },
        { id: 'm-2', title: 'Launch', status: 'in-progress', completedAt: undefined }
      ],
      metrics: {
        engagement: 90,
        readiness: 74,
        confidence: 81
      },
      timeline: [],
      createdAt: new Date().toISOString()
    };

    const twin = new DigitalTwin(project);
    const dashboard = new DigitalTwinDashboard([twin]);

    expect(dashboard.build().projects[0].name).toBe('Luxury Launch');
    expect(twin.snapshot().progress).toBe(62);
  });
});
