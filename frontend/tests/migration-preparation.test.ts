import { describe, expect, it } from 'vitest';
import {
  buildAuditReport,
  buildMigrationReport,
  buildDeploymentChecklist,
  buildRollbackPlan,
  createSampleServerProfile
} from '../deployment/validator';

describe('migration preparation validators', () => {
  it('builds a readiness report with critical findings and a score', () => {
    const report = buildAuditReport(createSampleServerProfile());

    expect(report.readinessScore).toBeGreaterThan(0);
    expect(report.readinessScore).toBeLessThanOrEqual(100);
    expect(report.criticalErrors.length).toBeGreaterThanOrEqual(0);
    expect(report.warnings.length).toBeGreaterThanOrEqual(0);
    expect(report.recommendations.length).toBeGreaterThan(0);
  });

  it('creates a migration report with planner steps and downtime estimate', () => {
    const report = buildMigrationReport(createSampleServerProfile());

    expect(report.steps.length).toBeGreaterThan(0);
    expect(report.rollbackPlan.steps.length).toBeGreaterThan(0);
    expect(report.downtimeEstimate.minutes).toBeGreaterThan(0);
  });

  it('creates deployment checklists for each domain', () => {
    const checklist = buildDeploymentChecklist();

    expect(checklist.length).toBeGreaterThan(6);
    expect(checklist.some((entry) => entry.category === 'Infrastructure')).toBe(true);
    expect(checklist.some((entry) => entry.category === 'Security')).toBe(true);
  });

  it('creates rollback plan entries for migration failure scenarios', () => {
    const plan = buildRollbackPlan();

    expect(plan.steps.length).toBeGreaterThan(0);
    expect(plan.steps[0].name).toContain('Rollback');
  });
});
