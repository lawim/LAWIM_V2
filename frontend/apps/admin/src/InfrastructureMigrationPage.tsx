import React from 'react';
import { Badge, Button, Card } from '@ui';
import {
  buildAuditReport,
  buildDeploymentChecklist,
  buildMigrationReport,
  buildRollbackPlan,
  createSampleServerProfile
} from '../../../deployment/validator';

export function InfrastructureMigrationPage() {
  const profile = createSampleServerProfile();
  const audit = buildAuditReport(profile);
  const migration = buildMigrationReport(profile);
  const checklist = buildDeploymentChecklist();
  const rollback = buildRollbackPlan();

  return (
    <div className="space-y-6 p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">Release Program W</p>
          <h1 className="text-3xl font-bold text-slate-900">Production Migration Preparation</h1>
        </div>
        <Button variant="secondary">Run server validation</Button>
      </div>

      <Card title="Server validation" description="A validation-only assessment of the target environment">
        <div className="grid gap-4 md:grid-cols-3">
          <div className="rounded-2xl border border-slate-200 p-4">
            <p className="text-sm text-slate-500">Readiness score</p>
            <p className="mt-2 text-3xl font-semibold text-slate-900">{audit.readinessScore}%</p>
          </div>
          <div className="rounded-2xl border border-slate-200 p-4">
            <p className="text-sm text-slate-500">Critical errors</p>
            <p className="mt-2 text-3xl font-semibold text-slate-900">{audit.criticalErrors.length}</p>
          </div>
          <div className="rounded-2xl border border-slate-200 p-4">
            <p className="text-sm text-slate-500">Warnings</p>
            <p className="mt-2 text-3xl font-semibold text-slate-900">{audit.warnings.length}</p>
          </div>
        </div>
        <div className="mt-6 grid gap-3">
          {audit.validations.map((validation) => (
            <div key={validation.name} className="flex items-center justify-between rounded-2xl border border-slate-200 px-4 py-3">
              <div>
                <p className="font-medium text-slate-900">{validation.name}</p>
                <p className="text-sm text-slate-500">{validation.message}</p>
              </div>
              <Badge variant={validation.status === 'pass' ? 'success' : validation.status === 'fail' ? 'warning' : 'info'}>
                {validation.status}
              </Badge>
            </div>
          ))}
        </div>
      </Card>

      <Card title="Migration planner" description="Pre-flight migration steps and dry-run planning">
        <div className="space-y-3">
          {migration.steps.map((step) => (
            <div key={step.name} className="rounded-2xl border border-slate-200 p-4">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <p className="font-medium text-slate-900">{step.name}</p>
                  <p className="text-sm text-slate-500">{step.description}</p>
                </div>
                <Badge variant="info">~{step.estimatedMinutes} min</Badge>
              </div>
            </div>
          ))}
        </div>
        <div className="mt-6 rounded-2xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-800">
          Planned downtime: {migration.downtimeEstimate.minutes} minutes — {migration.downtimeEstimate.note}
        </div>
      </Card>

      <Card title="Deployment readiness checklist" description="Operational checklist for infrastructure and service validation">
        <div className="grid gap-3 md:grid-cols-2">
          {checklist.map((entry) => (
            <div key={`${entry.category}-${entry.title}`} className="rounded-2xl border border-slate-200 p-4">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <p className="text-sm font-semibold uppercase tracking-[0.2em] text-slate-500">{entry.category}</p>
                  <p className="text-sm text-slate-900">{entry.title}</p>
                </div>
                <Badge variant={entry.completed ? 'success' : 'warning'}>{entry.completed ? 'Ready' : 'Pending'}</Badge>
              </div>
            </div>
          ))}
        </div>
      </Card>

      <Card title="Rollback planner" description="Validation-only rollback sequence for migration incidents">
        <div className="space-y-3">
          {rollback.steps.map((step) => (
            <div key={step.name} className="rounded-2xl border border-slate-200 p-4">
              <p className="font-medium text-slate-900">{step.name}</p>
              <p className="mt-1 text-sm text-slate-500">{step.description}</p>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
