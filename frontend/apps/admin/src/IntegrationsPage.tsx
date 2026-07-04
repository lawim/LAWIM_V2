import React from 'react';
import { Card } from '@ui';

export function IntegrationsPage() {
  return (
    <div className="space-y-6 p-6">
      <div>
        <p className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">Program AD</p>
        <h1 className="text-3xl font-bold text-slate-900">Integrations Center</h1>
      </div>
      <Card title="Connector Catalog" description="Official integrations for LAWIM 1.x">
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {['Google Workspace','Google Drive','Gmail','Calendar','Contacts','Rclone','WhatsApp Business','Telegram','Facebook','Instagram','LinkedIn','OpenStreetMap','SMTP','SMS','OAuth Providers'].map((item) => (
            <div key={item} className="rounded-2xl border border-slate-200 p-4 text-sm text-slate-700">{item}</div>
          ))}
        </div>
      </Card>
    </div>
  );
}
