import React from 'react';
import { Card } from '@ui';

export function MonthlyReviewPage() {
  return (
    <div className="space-y-6 p-6">
      <div>
        <p className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">Program AH</p>
        <h1 className="text-3xl font-bold text-slate-900">Monthly Intelligence Review Center</h1>
      </div>
      <Card title="Review Cycle Scheduler" description="Monthly review cycle with human validation queue">
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {['Observation Collector','Trend Analyzer','Anomaly Detector','Recommendation Generator','Confidence Scoring','Impact Estimation','Human Validation Queue','Review History'].map((item) => (
            <div key={item} className="rounded-2xl border border-slate-200 p-4 text-sm text-slate-700">{item}</div>
          ))}
        </div>
      </Card>
    </div>
  );
}
