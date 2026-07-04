import React from 'react';
import { Card } from '@ui';
import {
  getReleaseZPackageSummary,
  getReleaseZPackageArtifacts,
  getReleaseZPackageChecklist
} from '../../../../deployment/release-z';

export function ReleaseZPackagePage() {
  return (
    <div className="space-y-6 p-6">
      <div>
        <p className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">Release Program Z</p>
        <h1 className="text-3xl font-bold text-slate-900">Production deployment package</h1>
      </div>

      <Card title="Package overview" description="Operational release package without live execution">
        <p className="text-sm text-slate-700">{getReleaseZPackageSummary()}</p>
      </Card>

      <Card title="Included artifacts" description="Runbooks, scripts, templates, and checklists">
        <div className="space-y-3">
          {getReleaseZPackageArtifacts().map((artifact) => (
            <div key={artifact.path} className="rounded-2xl border border-slate-200 p-4">
              <p className="font-medium text-slate-900">{artifact.name}</p>
              <p className="mt-1 text-sm text-slate-500">{artifact.description}</p>
            </div>
          ))}
        </div>
      </Card>

      <Card title="Execution checklist" description="Controlled preparation path for production">
        <pre className="whitespace-pre-wrap text-sm text-slate-700">{getReleaseZPackageChecklist()}</pre>
      </Card>
    </div>
  );
}
