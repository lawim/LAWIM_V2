import React from 'react';
import { Card } from '@ui';

export function CognitiveCorePage() {
  return (
    <div className="space-y-6 p-6">
      <div>
        <p className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">Program AO</p>
        <h1 className="text-3xl font-bold text-slate-900">Cognitive Core Center</h1>
      </div>
      <Card title="Cognitive Core" description="Controlled cognitive foundation with explainability and risk guardrails">
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {['Cognitive State','Cognitive Context','Cognitive Session','Cognitive Plan','Cognitive Trace','Cognitive Reasoning Log','Cognitive Explainability','Cognitive Risk Guard'].map((item) => (
            <div key={item} className="rounded-2xl border border-slate-200 p-4 text-sm text-slate-700">{item}</div>
          ))}
        </div>
      </Card>
    </div>
  );
}
