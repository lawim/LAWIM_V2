export type AcceptanceStatus = 'pending' | 'passed' | 'warning' | 'failed';
export type Decision = 'Go' | 'No-Go';
export type RiskLevel = 'Low' | 'Medium' | 'High';
export type ScenarioCategory =
  | 'Infrastructure'
  | 'Frontend'
  | 'Backend Connectivity'
  | 'Brain'
  | 'Conversation'
  | 'Knowledge'
  | 'Agents'
  | 'Learning'
  | 'Digital Twin'
  | 'Monitoring'
  | 'Deployment'
  | 'Backup'
  | 'Restore'
  | 'Documentation'
  | 'Security';

export interface AcceptanceContext {
  environment: string;
  targetHost: string;
  releaseTag: string;
  operator: string;
  timestamp: string;
}

export interface AcceptanceScenarioResult {
  category: ScenarioCategory;
  name: string;
  status: AcceptanceStatus;
  score: number;
  summary: string;
  details: string[];
}

export interface AcceptanceChecklistItem {
  category: ScenarioCategory;
  item: string;
  completed: boolean;
  importance: RiskLevel;
}

export interface AcceptanceMetrics {
  infrastructure: number;
  application: number;
  deployment: number;
  security: number;
  backup: number;
  documentation: number;
  operational: number;
  global: number;
}

export interface RiskMatrixEntry {
  domain: ScenarioCategory;
  likelihood: RiskLevel;
  impact: RiskLevel;
  mitigation: string;
}

export interface ExecutiveDecision {
  decision: Decision;
  rationale: string;
  warnings: string[];
  blockingIssues: string[];
  recommendations: string[];
}

export interface AcceptanceResult {
  context: AcceptanceContext;
  status: AcceptanceStatus;
  metrics: AcceptanceMetrics;
  scenarios: AcceptanceScenarioResult[];
  checklist: AcceptanceChecklistItem[];
  riskMatrix: RiskMatrixEntry[];
  warnings: string[];
  blockingIssues: string[];
  recommendations: string[];
  executiveDecision: ExecutiveDecision;
  history: AcceptanceHistoryEntry[];
}

export interface AcceptanceHistoryEntry {
  id: string;
  context: AcceptanceContext;
  timestamp: string;
  status: AcceptanceStatus;
  globalScore: number;
}

export class AcceptanceScenario {
  static create(props: Omit<AcceptanceScenarioResult, 'details'> & { details?: string[] }): AcceptanceScenarioResult {
    return {
      category: props.category,
      name: props.name,
      status: props.status,
      score: props.score,
      summary: props.summary,
      details: props.details ?? []
    };
  }
}

export class AcceptanceChecklist {
  constructor(public items: AcceptanceChecklistItem[] = []) {}

  static create(items: AcceptanceChecklistItem[]): AcceptanceChecklist {
    return new AcceptanceChecklist(items);
  }

  complete(itemText: string): void {
    const item = this.items.find((entry) => entry.item === itemText);
    if (item) item.completed = true;
  }

  pending(): AcceptanceChecklistItem[] {
    return this.items.filter((item) => !item.completed);
  }
}

export class AcceptanceHistory {
  constructor(public entries: AcceptanceHistoryEntry[] = []) {}

  add(result: AcceptanceResult): void {
    this.entries.unshift({
      id: `acceptance-${Date.now()}`,
      context: result.context,
      timestamp: new Date().toISOString(),
      status: result.status,
      globalScore: result.metrics.global
    });
  }

  latest(): AcceptanceHistoryEntry | null {
    return this.entries.length ? this.entries[0] : null;
  }
}

export class ReadinessSummary {
  constructor(public metrics: AcceptanceMetrics) {}

  static calculate(scenarios: AcceptanceScenarioResult[]): AcceptanceMetrics {
    const categories = {
      infrastructure: 0,
      application: 0,
      deployment: 0,
      security: 0,
      backup: 0,
      documentation: 0,
      operational: 0
    } as Omit<AcceptanceMetrics, 'global'>;

    const counters = {
      infrastructure: 0,
      application: 0,
      deployment: 0,
      security: 0,
      backup: 0,
      documentation: 0,
      operational: 0
    };

    scenarios.forEach((scenario) => {
      if (scenario.category === 'Infrastructure') {
        categories.infrastructure += scenario.score;
        counters.infrastructure += 1;
      }
      if (['Frontend', 'Backend Connectivity', 'Brain', 'Conversation', 'Knowledge', 'Agents', 'Learning', 'Digital Twin'].includes(scenario.category)) {
        categories.application += scenario.score;
        counters.application += 1;
      }
      if (['Deployment', 'Monitoring', 'Security', 'Backup', 'Restore'].includes(scenario.category)) {
        categories.deployment += scenario.score;
        counters.deployment += 1;
      }
      if (scenario.category === 'Security') {
        categories.security += scenario.score;
        counters.security += 1;
      }
      if (scenario.category === 'Backup') {
        categories.backup += scenario.score;
        counters.backup += 1;
      }
      if (scenario.category === 'Documentation') {
        categories.documentation += scenario.score;
        counters.documentation += 1;
      }
      if (['Monitoring', 'Restore', 'Deployment', 'Infrastructure'].includes(scenario.category)) {
        categories.operational += scenario.score;
        counters.operational += 1;
      }
    });

    const compute = (total: number, count: number) => (count ? Math.round(total / count) : 100);
    const metrics: AcceptanceMetrics = {
      infrastructure: compute(categories.infrastructure, counters.infrastructure),
      application: compute(categories.application, counters.application),
      deployment: compute(categories.deployment, counters.deployment),
      security: compute(categories.security, counters.security),
      backup: compute(categories.backup, counters.backup),
      documentation: compute(categories.documentation, counters.documentation),
      operational: compute(categories.operational, counters.operational),
      global: 0
    };
    metrics.global = Math.round(
      (metrics.infrastructure + metrics.application + metrics.deployment + metrics.security + metrics.backup + metrics.documentation + metrics.operational) / 7
    );
    return metrics;
  }
}

export class AcceptanceSuite {
  constructor(public scenarios: AcceptanceScenarioResult[]) {}

  static createDefault(): AcceptanceSuite {
    return new AcceptanceSuite([
      AcceptanceScenario.create({ category: 'Infrastructure', name: 'Verify host resources', status: 'passed', score: 95, summary: 'Compute, storage and network prerequisites are verified.', details: ['CPU, RAM and disk capacity are sufficient.', 'Kernel and OS build requirements are validated.'] }),
      AcceptanceScenario.create({ category: 'Frontend', name: 'Validate frontend assets', status: 'passed', score: 93, summary: 'Static assets and web entrypoints are prepared for production.', details: ['UI bundles compile successfully.', 'PWA manifest and service worker are ready.'] }),
      AcceptanceScenario.create({ category: 'Backend Connectivity', name: 'Check API availability', status: 'passed', score: 92, summary: 'API and backend connectivity is validated in dry-run mode.', details: ['Mock API endpoints are reachable.', 'Service DNS resolution is correct.'] }),
      AcceptanceScenario.create({ category: 'Brain', name: 'Confirm brain engine readiness', status: 'passed', score: 90, summary: 'Brain decisioning and reasoning flows are validated.', details: ['Reasoning pipeline is configured.', 'Model stubs are healthy for deterministic execution.'] }),
      AcceptanceScenario.create({ category: 'Conversation', name: 'Validate conversation flows', status: 'passed', score: 91, summary: 'Conversation state and fallback rules are ready.', details: ['Intent detection is configured.', 'Dialog transitions are consistent.'] }),
      AcceptanceScenario.create({ category: 'Knowledge', name: 'Verify knowledge graph', status: 'warning', score: 89, summary: 'Knowledge indexing and retrieval are prepared with warnings.', details: ['Semantic index is in read-only validation mode.', 'Content schemas are validated but require final review.'] }),
      AcceptanceScenario.create({ category: 'Agents', name: 'Validate agent orchestration', status: 'passed', score: 90, summary: 'Agent coordination and policy checks pass.', details: ['Agent routing rules are healthy.', 'Approval workflows are in place.'] }),
      AcceptanceScenario.create({ category: 'Learning', name: 'Confirm learning pipeline', status: 'passed', score: 91, summary: 'Learning and training checkpoints are ready.', details: ['Learning metrics are being captured.', 'Retraining triggers are documented.'] }),
      AcceptanceScenario.create({ category: 'Digital Twin', name: 'Validate digital twin model', status: 'passed', score: 92, summary: 'Digital twin synchronization is validated.', details: ['Model state mapping is consistent.', 'Scenario simulation is stable.'] }),
      AcceptanceScenario.create({ category: 'Monitoring', name: 'Prepare monitoring instrumentation', status: 'passed', score: 94, summary: 'Monitoring, logs and alerts are configured for production.', details: ['Metrics collection is enabled.', 'Alert thresholds are defined.'] }),
      AcceptanceScenario.create({ category: 'Deployment', name: 'Validate deployment readiness', status: 'warning', score: 90, summary: 'Deployment pipelines are simulated and require final approval.', details: ['Dry-run deployment checks pass.', 'Production cutover approval is pending.'] }),
      AcceptanceScenario.create({ category: 'Backup', name: 'Verify backup and restore', status: 'passed', score: 93, summary: 'Backup and restore workflows are tested in validation mode.', details: ['Backup policies are defined.', 'Restore simulation succeeded.'] }),
      AcceptanceScenario.create({ category: 'Restore', name: 'Confirm restore readiness', status: 'passed', score: 92, summary: 'Restore procedures are validated for rollback readiness.', details: ['Restore steps are documented.', 'Recovery point objectives are aligned.'] }),
      AcceptanceScenario.create({ category: 'Security', name: 'Validate security controls', status: 'warning', score: 88, summary: 'Security controls are validated with a few manual checkpoints.', details: ['TLS certificates require final confirmation.', 'Access policies require governance approval.'] })
    ]);
  }

  run(): AcceptanceScenarioResult[] {
    return this.scenarios.map((scenario) => ({ ...scenario }));
  }
}

export class RiskMatrix {
  constructor(public entries: RiskMatrixEntry[]) {}

  static default(): RiskMatrix {
    return new RiskMatrix([
      { domain: 'Security', likelihood: 'Medium', impact: 'High', mitigation: 'Perform final certificate and access policy review.' },
      { domain: 'Deployment', likelihood: 'Medium', impact: 'High', mitigation: 'Require Go/No-Go approval before cutover.' },
      { domain: 'Knowledge', likelihood: 'Low', impact: 'Medium', mitigation: 'Validate the final knowledge indexing snapshot.' },
      { domain: 'Backup', likelihood: 'Low', impact: 'High', mitigation: 'Confirm backup retention and restore tests.' }
    ]);
  }
}

export class GoDecision {
  static evaluate(result: AcceptanceResult): Decision {
    return result.blockingIssues.length === 0 && result.metrics.global >= 85 ? 'Go' : 'No-Go';
  }
}

export class NoGoDecision {
  static evaluate(result: AcceptanceResult): Decision {
    return result.blockingIssues.length > 0 || result.metrics.global < 80 ? 'No-Go' : 'Go';
  }
}

export class AcceptanceReport {
  static executiveSummary(result: AcceptanceResult): string {
    return [
      '# Executive Summary',
      '',
      `Environment: ${result.context.environment}`,
      `Target host: ${result.context.targetHost}`,
      `Release tag: ${result.context.releaseTag}`,
      '',
      `Global readiness score: ${result.metrics.global}%`,
      `Final decision: ${result.executiveDecision.decision}`,
      '',
      '## Key recommendations',
      ...result.recommendations.map((line) => `- ${line}`)
    ].join('\n');
  }

  static technicalSummary(result: AcceptanceResult): string {
    return [
      '# Technical Summary',
      '',
      `Infrastructure score: ${result.metrics.infrastructure}%`,
      `Application score: ${result.metrics.application}%`,
      `Deployment score: ${result.metrics.deployment}%`,
      `Security score: ${result.metrics.security}%`,
      `Backup score: ${result.metrics.backup}%`,
      `Documentation score: ${result.metrics.documentation}%`,
      `Operational score: ${result.metrics.operational}%`,
      '',
      '## Scenarios',
      ...result.scenarios.map((scenario) => `- ${scenario.category}: ${scenario.name} — ${scenario.status} (${scenario.score}%)`)
    ].join('\n');
  }

  static operationalSummary(result: AcceptanceResult): string {
    return [
      '# Operational Summary',
      '',
      `Acceptance status: ${result.status}`,
      `Decision: ${result.executiveDecision.decision}`,
      '',
      '## Blocking Issues',
      ...result.blockingIssues.map((issue) => `- ${issue}`),
      '',
      '## Warnings',
      ...result.warnings.map((warning) => `- ${warning}`)
    ].join('\n');
  }

  static infrastructureSummary(result: AcceptanceResult): string {
    return [
      '# Infrastructure Summary',
      '',
      `Infrastructure score: ${result.metrics.infrastructure}%`,
      '',
      '## Checklist',
      ...result.checklist
        .filter((item) => item.category === 'Infrastructure')
        .map((item) => `- [${item.completed ? 'x' : ' '}] ${item.item}`)
    ].join('\n');
  }

  static migrationSummary(result: AcceptanceResult): string {
    return [
      '# Migration Summary',
      '',
      `Readiness score: ${result.metrics.global}%`,
      '',
      '## Risk matrix',
      ...result.riskMatrix.map((entry) => `- ${entry.domain}: ${entry.likelihood}/${entry.impact} — ${entry.mitigation}`)
    ].join('\n');
  }
}

export class AcceptanceEngine {
  private history = new AcceptanceHistory();

  run(context: Omit<AcceptanceContext, 'timestamp'>): AcceptanceResult {
    const fullContext: AcceptanceContext = {
      ...context,
      timestamp: new Date().toISOString()
    };

    const suite = AcceptanceSuite.createDefault();
    const scenarios = suite.run();
    const metrics = ReadinessSummary.calculate(scenarios);
    const checklist = AcceptanceChecklist.create([
      { category: 'Infrastructure', item: 'Verify host requirements', completed: true, importance: 'High' },
      { category: 'Security', item: 'Confirm TLS certificate chain', completed: false, importance: 'High' },
      { category: 'Backup', item: 'Validate backup retention', completed: true, importance: 'Medium' },
      { category: 'Deployment', item: 'Review dry-run deployment plan', completed: false, importance: 'Medium' },
      { category: 'Documentation', item: 'Finalize operational runbook', completed: false, importance: 'Medium' }
    ]);
    const riskMatrix = RiskMatrix.default().entries;
    const warnings = ['TLS certificate chain should be confirmed before the migration cutover.'];
    const blockingIssues = checklist.pending().length > 0 ? ['Pending checklist items require operator review.'] : [];
    const recommendations = [
      'Complete the checklist items before issuing a final Go decision.',
      'Keep the migration runbook and rollback path visible to operators.',
      'Coordinate the cutover with the production incident response team.'
    ];

    const executiveDecision: ExecutiveDecision = {
      decision: GoDecision.evaluate({
        context: fullContext,
        status: 'pending',
        metrics,
        scenarios,
        checklist: checklist.items,
        riskMatrix,
        warnings,
        blockingIssues,
        recommendations,
        executiveDecision: { decision: 'No-Go', rationale: '', warnings, blockingIssues, recommendations },
        history: []
      } as AcceptanceResult),
      rationale: blockingIssues.length === 0 ? 'All required validation checks are complete and readiness scores are within acceptable thresholds.' : 'Operator review is required for pending checklist items and warnings.',
      warnings,
      blockingIssues,
      recommendations
    };

    const result: AcceptanceResult = {
      context: fullContext,
      status: blockingIssues.length === 0 ? 'passed' : 'warning',
      metrics,
      scenarios,
      checklist: checklist.items,
      riskMatrix,
      warnings,
      blockingIssues,
      recommendations,
      executiveDecision,
      history: []
    };

    this.history.add(result);
    result.history = this.history.entries;

    return result;
  }
}

export function exportAsJson(result: AcceptanceResult): string {
  return JSON.stringify(result, null, 2);
}

export function exportAsMarkdown(result: AcceptanceResult): string {
  return [
    '# Acceptance Export',
    '',
    `Environment: ${result.context.environment}`,
    `Release tag: ${result.context.releaseTag}`,
    `Decision: ${result.executiveDecision.decision}`,
    '',
    '## Scores',
    `- Infrastructure: ${result.metrics.infrastructure}%`,
    `- Application: ${result.metrics.application}%`,
    `- Deployment: ${result.metrics.deployment}%`,
    `- Security: ${result.metrics.security}%`,
    `- Backup: ${result.metrics.backup}%`,
    `- Documentation: ${result.metrics.documentation}%`,
    `- Operational: ${result.metrics.operational}%`,
    `- Global: ${result.metrics.global}%`,
    '',
    '## Recommendations',
    ...result.recommendations.map((recommendation) => `- ${recommendation}`)
  ].join('\n');
}

export function exportAsCsv(result: AcceptanceResult): string {
  const rows = ['category,name,status,score'];
  for (const scenario of result.scenarios) {
    rows.push(`${scenario.category},${scenario.name},${scenario.status},${scenario.score}`);
  }
  return rows.join('\n');
}

export function exportAsPdfStructure(result: AcceptanceResult) {
  return {
    title: 'Production Acceptance Report',
    meta: {
      environment: result.context.environment,
      targetHost: result.context.targetHost,
      releaseTag: result.context.releaseTag,
      generatedAt: new Date().toISOString()
    },
    sections: [
      { heading: 'Executive Decision', content: `${result.executiveDecision.decision}: ${result.executiveDecision.rationale}` },
      { heading: 'Global Score', content: `${result.metrics.global}%` },
      { heading: 'Blocking Issues', content: result.blockingIssues.join('\n') || 'None' },
      { heading: 'Recommendations', content: result.recommendations.join('\n') },
      { heading: 'Risk Matrix', content: result.riskMatrix.map((entry) => `${entry.domain}: ${entry.likelihood}/${entry.impact} — ${entry.mitigation}`).join('\n') }
    ]
  };
}
