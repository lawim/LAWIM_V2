import React from 'react';
import { Card } from '@ui';

export function Lawim3ConstitutionPage() {
  return (
    <div className="space-y-6 p-6">
      <div>
        <p className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">Program AZ</p>
        <h1 className="text-3xl font-bold text-slate-900">LAWIM 3.0 Constitution Console</h1>
      </div>
      <Card title="Ethical AI Constitution" description="Foundational principles for human control, transparency, and autonomy governance">
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {['Ethical AI Principles','Human Control Principles','Transparency Principles','Data Governance Principles','Conversation Governance Principles','Autonomy Principles','Audit Principles','Safety Principles'].map((item) => (
            <div key={item} className="rounded-2xl border border-slate-200 p-4 text-sm text-slate-700">{item}</div>
          ))}
        </div>
      </Card>
    </div>
  );
}
