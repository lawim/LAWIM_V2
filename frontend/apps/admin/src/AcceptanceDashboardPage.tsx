import React from 'react';
import { Badge, Button, Card } from '@ui';
import {
  AcceptanceEngine,
  AcceptanceStatus,
  AcceptanceResult,
  exportAsJson,
  exportAsMarkdown,
  exportAsCsv,
  exportAsPdfStructure
} from '../../../../deployment/acceptance';

export function AcceptanceDashboardPage() {
  const engine = new AcceptanceEngine();
  const result = engine.run({
    environment: 'production',
    targetHost: 'lawim.internal',
    releaseTag: 'release-program-y',
    operator: 'ops-team'
  });

  const decision = result.executiveDecision.decision;
  const statusColor = decision === 'Go' ? 'success' : decision === 'No-Go' ? 'warning' : 'info';

  return (
    <div className="space-y-6 p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">Release Program Y</p>
          <h1 className="text-3xl font-bold text-slate-900">Production Acceptance</h1>
        </div>
        <Button variant="secondary">Refresh assessment</Button>
      </div>

      <Card title="Acceptance Status" description="Final readiness evaluation for production acceptance.">
        <div className="grid gap-4 md:grid-cols-3">
          <div className="rounded-2xl border border-slate-200 p-4">
            <p className="text-sm text-slate-500">Decision</p>
            <p className="mt-2 text-xl font-semibold text-slate-900">{decision}</p>
          </div>
          <div className="rounded-2xl border border-slate-200 p-4">
            <p className="text-sm text-slate-500">Readiness score</p>
            <p className="mt-2 text-xl font-semibold text-slate-900">{result.metrics.global}%</p>
          </div>
          <div className="rounded-2xl border border-slate-200 p-4">
            <p className="text-sm text-slate-500">Status</p>
            <Badge variant={statusColor as any}>{result.status}</Badge>
          </div>
        </div>
      </Card>

      <Card title="Risk Matrix" description="Critical operational and security risks for production acceptance.">
        <div className="space-y-3">
          {result.riskMatrix.map((entry) => (
            <div key={entry.domain} className="rounded-2xl border border-slate-200 p-4">
              <p className="font-semibold text-slate-900">{entry.domain}</p>
              <p className="text-sm text-slate-500">Likelihood: {entry.likelihood}, Impact: {entry.impact}</p>
              <p className="mt-2 text-sm text-slate-700">{entry.mitigation}</p>
            </div>
          ))}
        </div>
      </Card>

      <Card title="Blocking Issues & Warnings" description="Issues that affect the final Go/No-Go decision.">
        <div className="space-y-3">
          {result.blockingIssues.length > 0 ? (
            result.blockingIssues.map((issue) => (
              <div key={issue} className="rounded-2xl border border-rose-200 bg-rose-50 p-4 text-sm text-rose-800">{issue}</div>
            ))
          ) : (
            <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-800">Aucun problème bloquant détecté.</div>
          )}
          {result.warnings.map((warning) => (
            <div key={warning} className="rounded-2xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-800">{warning}</div>
          ))}
        </div>
      </Card>

      <Card title="Recommendations" description="Operational recommendations for the migration gate.">
        <ul className="list-disc space-y-2 pl-5 text-sm text-slate-700">
          {result.recommendations.map((recommendation) => (
            <li key={recommendation}>{recommendation}</li>
          ))}
        </ul>
      </Card>

      <Card title="Validation History" description="Previous acceptance assessments and score evolution.">
        <div className="space-y-3">
          {result.history.map((entry) => (
            <div key={entry.id} className="rounded-2xl border border-slate-200 p-4">
              <p className="font-semibold text-slate-900">{entry.timestamp}</p>
              <p className="text-sm text-slate-500">{entry.status} — {entry.globalScore}%</p>
            </div>
          ))}
        </div>
      </Card>

      <Card title="Exports" description="Export the acceptance result in multiple formats.">
        <div className="grid gap-4 md:grid-cols-4">
          <div className="rounded-2xl border border-slate-200 p-4 text-sm text-slate-700">JSON ready</div>
          <div className="rounded-2xl border border-slate-200 p-4 text-sm text-slate-700">Markdown ready</div>
          <div className="rounded-2xl border border-slate-200 p-4 text-sm text-slate-700">CSV ready</div>
          <div className="rounded-2xl border border-slate-200 p-4 text-sm text-slate-700">PDF structure ready</div>
        </div>
      </Card>
    </div>
  );
}
