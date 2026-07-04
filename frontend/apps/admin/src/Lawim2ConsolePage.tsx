import React from 'react';
import { Card } from '@ui';

export function Lawim2ConsolePage() {
  return (
    <div className="space-y-6 p-6">
      <div>
        <p className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">Program AN</p>
        <h1 className="text-3xl font-bold text-slate-900">LAWIM 2.0 Dashboard</h1>
      </div>
      <Card title="Unified Intelligence Console" description="Centralized LAWIM 2.0 foundation console with human approval loops">
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {['Memory Dashboard','Monthly Review Dashboard','Learning Dashboard','Digital Twin Intelligence Dashboard','Brain Intelligence Dashboard','Conversation Intelligence Dashboard','Governance Dashboard'].map((item) => (
            <div key={item} className="rounded-2xl border border-slate-200 p-4 text-sm text-slate-700">{item}</div>
          ))}
        </div>
      </Card>
    </div>
  );
}
