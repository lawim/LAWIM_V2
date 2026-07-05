import { Badge, Card, PageShell } from '@ui';
import { badgeVariantForStatus, buildCredentialVaultSnapshot } from './storageRegistry';

export function CredentialVaultPage() {
  const snapshot = buildCredentialVaultSnapshot();

  return (
    <PageShell
      eyebrow="Credential Vault"
      title="Encrypted credential vault"
      description="Masked records, encrypted references, rotation windows, and audit traces for the Google Drive activation perimeter."
    >
      <div className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
        <Card title="Vault summary" description="The vault stores protected material outside Git, logs, docs, tests, and the frontend.">
          <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="text-sm text-slate-400">Records</div>
              <div className="mt-2 text-3xl font-semibold text-white">{snapshot.summary.recordCount}</div>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="text-sm text-slate-400">Active</div>
              <div className="mt-2 text-3xl font-semibold text-white">{snapshot.summary.activeCount}</div>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="text-sm text-slate-400">Rotation due</div>
              <div className="mt-2 text-3xl font-semibold text-white">{snapshot.summary.rotationDueCount}</div>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="text-sm text-slate-400">Expired</div>
              <div className="mt-2 text-3xl font-semibold text-white">{snapshot.summary.expiredCount}</div>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="text-sm text-slate-400">Invalid</div>
              <div className="mt-2 text-3xl font-semibold text-white">{snapshot.summary.invalidCount}</div>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="text-sm text-slate-400">Masked</div>
              <div className="mt-2 text-3xl font-semibold text-white">{snapshot.summary.maskedRecords}</div>
            </div>
          </div>
        </Card>
        <Card title="Protection layers" description="Credential encryption, masking, rotation, scanning, and audit trail are active.">
          <div className="mt-4 space-y-3 text-sm text-slate-300">
            {snapshot.securityControls.map((control) => (
              <div key={control.name} className="rounded-xl border border-slate-800 px-3 py-2">
                <div className="flex items-center justify-between gap-3">
                  <span className="font-medium text-white">{control.name}</span>
                  <Badge variant={badgeVariantForStatus(control.status)}>{control.status}</Badge>
                </div>
                <div className="mt-2 text-xs text-slate-500">{control.description}</div>
              </div>
            ))}
          </div>
        </Card>
      </div>

      <Card title="Vault records" description="Each record stores a logical binding, a masked reference, and secure test timestamps.">
        <div className="mt-4 grid gap-3 xl:grid-cols-2">
          {snapshot.records.map((record) => (
            <div key={record.credentialId} className="rounded-2xl border border-slate-800/80 bg-slate-950/70 p-4">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <div className="text-xs uppercase tracking-[0.3em] text-slate-500">{record.credentialId}</div>
                  <div className="mt-1 text-lg font-semibold text-white">{record.role}</div>
                </div>
                <Badge variant={badgeVariantForStatus(record.status)}>{record.status}</Badge>
              </div>
              <div className="mt-2 text-sm text-slate-400">{record.driveId} · {record.provider} · {record.scope}</div>
              <div className="mt-4 space-y-2 text-sm text-slate-300">
                <div className="rounded-xl border border-slate-800 px-3 py-2">Credential reference: {record.maskedReference}</div>
                <div className="rounded-xl border border-slate-800 px-3 py-2">Masked reference: {record.maskedValue}</div>
                <div className="rounded-xl border border-slate-800 px-3 py-2">OAuth status: {record.oauthStatus} · Credential status: {record.credentialStatus}</div>
                <div className="rounded-xl border border-slate-800 px-3 py-2">Expiration: {record.expiration} · Rotation due: {record.rotationDue}</div>
                <div className="rounded-xl border border-slate-800 px-3 py-2">Last use: {record.lastUse}</div>
                <div className="rounded-xl border border-slate-800 px-3 py-2">Connection test: {record.lastConnectionTest} · Upload test: {record.lastUploadTest} · Download test: {record.lastDownloadTest}</div>
                <div className="rounded-xl border border-slate-800 px-3 py-2">Healthcheck: {record.lastHealthcheck}</div>
              </div>
              {record.alerts.length > 0 ? (
                <div className="mt-4 space-y-2 text-xs text-amber-200">
                  {record.alerts.map((alert) => (
                    <div key={alert} className="rounded-xl border border-amber-500/30 bg-amber-500/10 px-3 py-2">
                      {alert}
                    </div>
                  ))}
                </div>
              ) : (
                <div className="mt-4 rounded-xl border border-slate-800 px-3 py-2 text-xs text-slate-500">No alert recorded.</div>
              )}
            </div>
          ))}
        </div>
      </Card>

      <div className="grid gap-6 xl:grid-cols-[0.8fr_1.2fr]">
        <Card title="Monitoring" description="Vault-wide status is exposed through masked and aggregated metrics only.">
          <div className="mt-4 space-y-3 text-sm text-slate-300">
            <div className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2">
              <span>Last access</span>
              <Badge variant="info">{snapshot.monitoring.lastAccess}</Badge>
            </div>
            <div className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2">
              <span>Last success</span>
              <Badge variant="success">{snapshot.monitoring.lastSuccess}</Badge>
            </div>
            <div className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2">
              <span>Last failure</span>
              <Badge variant={snapshot.monitoring.lastFailure === 'never' ? 'info' : 'warning'}>{snapshot.monitoring.lastFailure}</Badge>
            </div>
            <div className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2">
              <span>Alerts</span>
              <Badge variant={snapshot.monitoring.alerts.length > 0 ? 'warning' : 'success'}>{snapshot.monitoring.alerts.length}</Badge>
            </div>
            <div className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2">
              <span>Audit events</span>
              <Badge variant="info">{snapshot.auditTrail.eventCount}</Badge>
            </div>
          </div>
        </Card>
        <Card title="Audit trail" description="The audit trail records lifecycle events with masked details only.">
          <div className="mt-4 space-y-3 text-sm text-slate-300">
            <div className="rounded-xl border border-slate-800 px-3 py-2">Latest event: {snapshot.auditTrail.latestEvent}</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Event count: {snapshot.auditTrail.eventCount}</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Protected material remains masked in all UI surfaces.</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Rotation schedule: 90 days · Expiration: 365 days · Warning window: 14 days.</div>
          </div>
        </Card>
      </div>
    </PageShell>
  );
}
