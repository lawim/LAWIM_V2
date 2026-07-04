import React from 'react';
import { Card } from '@ui';

export function ConversationIntelligencePage() {
  return (
    <div className="space-y-6 p-6">
      <div>
        <p className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">Program AL</p>
        <h1 className="text-3xl font-bold text-slate-900">Conversation Intelligence</h1>
      </div>
      <Card title="Conversation Governance" description="Persistent conversation intelligence with human review controls">
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {['Persistent Conversation Metadata','Conversation Summary','Intent Extraction','Action Extraction','Decision Extraction','Preference Extraction','Conversation-to-Project Linking','Conversation Timeline','Conversation Governance'].map((item) => (
            <div key={item} className="rounded-2xl border border-slate-200 p-4 text-sm text-slate-700">{item}</div>
          ))}
        </div>
      </Card>
    </div>
  );
}
