import React from 'react';
import { Badge, Button, Card } from '@ui';
import {
  DeploymentOrchestrator,
  createDeploymentContext,
  buildDeploymentSummary,
  buildSimulationReport,
  buildReadinessReport,
  buildGoLiveReport,
  buildExecutiveSummary
} from '../../../../deployment/orchestrator';

export function DeploymentOrchestratorPage() {
  const context = createDeploymentContext();
  const orchestrator = new DeploymentOrchestrator();
  const result = orchestrator.runSimulation(context);
  const summary = buildDeploymentSummary(result);

  return (
    <div className="space-y-6 p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">Release Program X</p>
          <h1 className="text-3xl font-bold text-slate-900">Deployment Center</h1>
        </div>
        <Button variant="secondary">Run dry-run</Button>
      </div>

      <Card title="Go-Live Dashboard" description="Simulation-only deployment readiness for production">
        <div className="grid gap-4 md:grid-cols-4">
          <div className="rounded-2xl border border-slate-200 p-4">
            <p className="text-sm text-slate-500">Status</p>
            <p className="mt-2 text-xl font-semibold text-slate-900">{summary.status}</p>
          </div>
          <div className="rounded-2xl border border-slate-200 p-4">
            <p className="text-sm text-slate-500">Readiness score</p>
            <p className="mt-2 text-xl font-semibold text-slate-900">{summary.readinessScore}%</p>
          </div>
          <div className="rounded-2xl border border-slate-200 p-4">
            <p className="text-sm text-slate-500">Global score</p>
            <p className="mt-2 text-xl font-semibold text-slate-900">{summary.globalScore}%</p>
          </div>
          <div className="rounded-2xl border border-slate-200 p-4">
            <p className="text-sm text-slate-500">Environment</p>
            <p className="mt-2 text-xl font-semibold text-slate-900">{context.environment}</p>
          </div>
        </div>
      </Card>

      <Card title="Simulation Console" description="Execution timeline and validation log">
        <div className="space-y-3">
          {result.timeline.map((entry) => (
            <div key={entry} className="rounded-2xl border border-slate-200 p-4 text-sm text-slate-700">{entry}</div>
          ))}
        </div>
      </Card>

      <Card title="Risk Dashboard" description="Warnings and blocking issues">
        <div className="space-y-2">
          {result.warnings.map((warning) => (
            <div key={warning} className="rounded-2xl border border-amber-200 bg-amber-50 p-3 text-sm text-amber-800">{warning}</div>
          ))}
          {result.blockingErrors.length === 0 ? (
            <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-800">No blocking errors detected in the simulated deployment run.</div>
          ) : result.blockingErrors.map((error) => (
            <div key={error} className="rounded-2xl border border-rose-200 bg-rose-50 p-3 text-sm text-rose-800">{error}</div>
          ))}
        </div>
      </Card>

      <Card title="Validation Dashboard" description="Component-level scores">
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {[
            ['Infrastructure', result.infrastructureScore],
            ['Deployment', result.deploymentScore],
            ['Security', result.securityScore],
            ['Backup', result.backupScore],
            ['Monitoring', result.monitoringScore],
            ['Documentation', result.documentationScore]
          ].map(([label, value]) => (
            <div key={label} className="rounded-2xl border border-slate-200 p-4">
              <p className="text-sm text-slate-500">{label}</p>
              <p className="mt-2 text-2xl font-semibold text-slate-900">{value}%</p>
            </div>
          ))}
        </div>
      </Card>

      <Card title="Reports" description="Export-ready deployment summaries">
        <div className="space-y-3">
          <div className="rounded-2xl border border-slate-200 p-4">
            <p className="font-medium text-slate-900">Executive summary</p>
            <p className="mt-1 text-sm text-slate-500">{buildExecutiveSummary(result)}</p>
          </div>
          <div className="rounded-2xl border border-slate-200 p-4">
            <p className="font-medium text-slate-900">Simulation report</p>
            <p className="mt-1 text-sm text-slate-500">{buildSimulationReport(result, context)}</p>
          </div>
          <div className="rounded-2xl border border-slate-200 p-4">
            <p className="font-medium text-slate-900">Readiness report</p>
            <p className="mt-1 text-sm text-slate-500">{buildReadinessReport(result)}</p>
          </div>
          <div className="rounded-2xl border border-slate-200 p-4">
            <p className="font-medium text-slate-900">Go-live report</p>
            <p className="mt-1 text-sm text-slate-500">{buildGoLiveReport(result)}</p>
          </div>
        </div>
      </Card>
    </div>
  );
}
