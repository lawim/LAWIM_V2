import React from 'react';
import { Card } from '@ui';

export function DigitalTwinIntelligencePage() {
  return (
    <div className="space-y-6 p-6">
      <div>
        <p className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">Program AJ</p>
        <h1 className="text-3xl font-bold text-slate-900">Digital Twin Intelligence Layer</h1>
      </div>
      <Card title="Project Intelligence" description="Human-supervised digital twin intelligence for projects">
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {['Project State Aggregator','Project Progress Model','Project Timeline','Project Milestones','Project Health','Project Risks','Project Blockers','Project Recommendations','Project Snapshot History'].map((item) => (
            <div key={item} className="rounded-2xl border border-slate-200 p-4 text-sm text-slate-700">{item}</div>
          ))}
        </div>
      </Card>
    </div>
  );
}
