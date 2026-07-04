import React from 'react';
import { Card } from '@ui';

export function QualityPage() {
  return (
    <div className="space-y-6 p-6">
      <div>
        <p className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">Program AE</p>
        <h1 className="text-3xl font-bold text-slate-900">Quality Center</h1>
      </div>
      <Card title="Quality Dashboard" description="Quality controls and release assurance for LAWIM 1.x">
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {['Coverage Dashboard','Architecture Validation','Dependency Validation','Dead Code Detection','Documentation Coverage','API Compatibility','Regression Analyzer','Code Quality Reports','Automated Review','Release Quality Score'].map((item) => (
            <div key={item} className="rounded-2xl border border-slate-200 p-4 text-sm text-slate-700">{item}</div>
          ))}
        </div>
      </Card>
    </div>
  );
}
