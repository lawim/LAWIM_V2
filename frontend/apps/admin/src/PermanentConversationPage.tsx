import React from 'react';
import { Card } from '@ui';

export function PermanentConversationPage() {
  return (
    <div className="space-y-6 p-6">
      <div>
        <p className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">Program AP</p>
        <h1 className="text-3xl font-bold text-slate-900">Permanent Conversation Center</h1>
      </div>
      <Card title="Conversation Continuity" description="Long-term conversation architecture with privacy and retention controls">
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {['Long-Term Conversation Metadata','Conversation Memory Index','Conversation Continuity','Conversation Summaries Chain','Conversation Context Recovery','Conversation Privacy Controls','Conversation Retention Governance'].map((item) => (
            <div key={item} className="rounded-2xl border border-slate-200 p-4 text-sm text-slate-700">{item}</div>
          ))}
        </div>
      </Card>
    </div>
  );
}
