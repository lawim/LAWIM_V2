import React from 'react';
import { Card } from '@ui';

export function SecurityPage() {
  return (
    <div className="space-y-6 p-6">
      <div>
        <p className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">Program AB</p>
        <h1 className="text-3xl font-bold text-slate-900">Security Center</h1>
      </div>
      <Card title="Security Dashboard" description="Security hardening surfaces for LAWIM 1.x">
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {['Security Audit','Headers Validation','Permissions Audit','Protected Material Validation','JWT Validation','Rate Limit Monitor','Login Protection','Session Analyzer','CSRF Validation','XSS Validation','CSP Validation','Dependencies Audit','Security Reports'].map((item) => (
            <div key={item} className="rounded-2xl border border-slate-200 p-4 text-sm text-slate-700">{item}</div>
          ))}
        </div>
      </Card>
    </div>
  );
}
