import { describe, expect, it } from 'vitest';
import {
  AcceptanceEngine,
  exportAsJson,
  exportAsMarkdown,
  exportAsCsv,
  exportAsPdfStructure
} from '../../deployment/acceptance';

describe('acceptance engine', () => {
  it('produces a final acceptance result with a decision and global score', () => {
    const engine = new AcceptanceEngine();
    const result = engine.run({
      environment: 'production',
      targetHost: 'lawim.internal',
      releaseTag: 'release-program-y',
      operator: 'ops-team'
    });

    expect(result.metrics.global).toBeGreaterThan(0);
    expect(result.status).toBe('warning');
    expect(result.executiveDecision.decision).toBe('No-Go');
    expect(result.blockingIssues.length).toBeGreaterThan(0);
    expect(result.history.length).toBeGreaterThan(0);
  });

  it('exports acceptance results in supported formats', () => {
    const engine = new AcceptanceEngine();
    const result = engine.run({
      environment: 'production',
      targetHost: 'lawim.internal',
      releaseTag: 'release-program-y',
      operator: 'ops-team'
    });

    const json = exportAsJson(result);
    const markdown = exportAsMarkdown(result);
    const csv = exportAsCsv(result);
    const pdf = exportAsPdfStructure(result);

    expect(() => JSON.parse(json)).not.toThrow();
    expect(markdown).toContain('# Acceptance Export');
    expect(csv).toContain('category,name,status,score');
    expect(pdf).toHaveProperty('title', 'Production Acceptance Report');
  });
});
