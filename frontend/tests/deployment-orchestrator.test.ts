import { describe, expect, it } from 'vitest';
import {
  DeploymentOrchestrator,
  createDeploymentContext,
  buildDeploymentSummary,
  buildSimulationReport,
  buildReadinessReport,
  buildGoLiveReport,
  buildExecutiveSummary,
  exportResultAsJson,
  exportResultAsMarkdown,
  preparePdfStructure
} from '../../deployment/orchestrator';

describe('deployment orchestrator', () => {
  it('runs a simulation and returns a readiness score', () => {
    const result = new DeploymentOrchestrator().runSimulation(createDeploymentContext());
    expect(result.globalScore).toBeGreaterThan(0);
    expect(result.readinessScore).toBeGreaterThan(0);
    expect(result.timeline.length).toBeGreaterThan(0);
  });

  it('builds a deployment summary with ready status', () => {
    const result = new DeploymentOrchestrator().runSimulation(createDeploymentContext());
    const summary = buildDeploymentSummary(result);
    expect(summary.status).toBe('ready');
  });

  it('builds export-ready reports', () => {
    const result = new DeploymentOrchestrator().runSimulation(createDeploymentContext());
    const context = createDeploymentContext();
    expect(buildSimulationReport(result, context)).toContain('Deployment Simulation Report');
    expect(buildReadinessReport(result)).toContain('Readiness Report');
    expect(buildGoLiveReport(result)).toContain('Go-Live Report');
    expect(buildExecutiveSummary(result)).toContain('Global production score');
  });

  it('exports JSON, Markdown, and PDF-friendly structures', () => {
    const result = new DeploymentOrchestrator().runSimulation(createDeploymentContext());
    const context = createDeploymentContext({ environment: 'staging' });
    const json = exportResultAsJson(result, context);
    const markdown = exportResultAsMarkdown(result, context);
    const pdf = preparePdfStructure(result, context);

    expect(() => JSON.parse(json)).not.toThrow();
    expect(markdown).toContain('Deployment Orchestrator Export');
    expect(pdf).toHaveProperty('title', 'Deployment Orchestrator Simulation Report');
    expect(pdf.meta.environment).toBe('staging');
  });
});
