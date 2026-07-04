import React from 'react';
import { Card } from '@ui';

export function AutonomousWorkflowPreviewPage() {
  return (
    <div className="space-y-6 p-6">
      <div>
        <p className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">Program AS</p>
        <h1 className="text-3xl font-bold text-slate-900">Autonomous Workflow Preview Center</h1>
      </div>
      <Card title="Preview and Safety Gates" description="Workflow proposals remain in preview mode with explicit approval gates">
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {['Workflow Candidate','Automation Proposal','Automation Boundary','Delegation Requirement','Safety Gate','Approval Gate','Rollback Gate','Dry Run Execution'].map((item) => (
            <div key={item} className="rounded-2xl border border-slate-200 p-4 text-sm text-slate-700">{item}</div>
          ))}
        </div>
      </Card>
    </div>
  );
}
