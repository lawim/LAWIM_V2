import React from 'react';
import { Card } from '@ui';

export function AdvancedDigitalTwinPage() {
  return (
    <div className="space-y-6 p-6">
      <div>
        <p className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">Program AQ</p>
        <h1 className="text-3xl font-bold text-slate-900">Advanced Digital Twin Center</h1>
      </div>
      <Card title="Twin Scenario Models" description="Human-reviewed scenario modeling for projects and decisions">
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {['Scenario Model','Project Simulation Model','Risk Scenario','Budget Scenario','Timeline Scenario','Decision Scenario','Twin Comparison','Twin Evolution History'].map((item) => (
            <div key={item} className="rounded-2xl border border-slate-200 p-4 text-sm text-slate-700">{item}</div>
          ))}
        </div>
      </Card>
    </div>
  );
}
