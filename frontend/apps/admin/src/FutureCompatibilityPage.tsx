import React from 'react';
import { Card } from '@ui';

export function FutureCompatibilityPage() {
  return (
    <div className="space-y-6 p-6">
      <div>
        <p className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">Program AY</p>
        <h1 className="text-3xl font-bold text-slate-900">Future Compatibility Center</h1>
      </div>
      <Card title="Compatibility and Evolution" description="Feature flags, preview modes, and upgrade planning for LAWIM evolution">
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {['Feature Flags','Preview Modes','Experimental Modules','Capability Registry','Version Compatibility Matrix','Deprecation Planner','Migration Path Registry','Upgrade Assistant'].map((item) => (
            <div key={item} className="rounded-2xl border border-slate-200 p-4 text-sm text-slate-700">{item}</div>
          ))}
        </div>
      </Card>
    </div>
  );
}
