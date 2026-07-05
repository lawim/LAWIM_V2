import { Badge, Card, PageShell } from '@ui';
import { badgeVariantForStatus, buildGoogleDriveSecuritySnapshot } from './storageRegistry';

export function GoogleDriveSecurityPage() {
  const snapshot = buildGoogleDriveSecuritySnapshot();

  return (
    <PageShell
      eyebrow="Google Drive Security"
      title="Credential and protected material protection"
      description="Security controls, masked monitoring, rotation policy, and audit trail for the Google Drive activation perimeter."
    >
      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
        <Card title="Active credentials" description="Credentials available for production onboarding.">
          <div className="mt-4 text-3xl font-semibold text-white">{snapshot.summary.activeCredentials}</div>
        </Card>
        <Card title="Rotation due" description="Credentials that should be rotated on the next cycle.">
          <div className="mt-4 text-3xl font-semibold text-white">{snapshot.summary.rotationDueCredentials}</div>
        </Card>
        <Card title="Expired" description="Expired credentials require intervention.">
          <div className="mt-4 text-3xl font-semibold text-white">{snapshot.summary.expiredCredentials}</div>
        </Card>
        <Card title="Invalid" description="Invalid credentials are blocked from use.">
          <div className="mt-4 text-3xl font-semibold text-white">{snapshot.summary.invalidCredentials}</div>
        </Card>
      </div>

      <div className="grid gap-6 xl:grid-cols-[1fr_1fr]">
        <Card title="Security controls" description="The protection stack is active across Git, logs, and UI surfaces.">
          <div className="mt-4 space-y-3 text-sm text-slate-300">
            {snapshot.controls.map((control) => (
              <div key={control.name} className="rounded-2xl border border-slate-800/80 bg-slate-950/70 p-4">
                <div className="flex items-center justify-between gap-3">
                  <div className="font-semibold text-white">{control.name}</div>
                  <Badge variant={badgeVariantForStatus(control.status)}>{control.status}</Badge>
                </div>
                <div className="mt-2 text-xs text-slate-500">{control.description}</div>
              </div>
            ))}
          </div>
        </Card>
        <Card title="Rotation policy" description="Rotation, expiry, masking, and audit rules are fixed for the production vault.">
          <div className="mt-4 space-y-3 text-sm text-slate-300">
            <div className="rounded-xl border border-slate-800 px-3 py-2">Rotation interval: {snapshot.policy.rotationDays} days</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Expiration interval: {snapshot.policy.expirationDays} days</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Warning window: {snapshot.policy.warningWindowDays} days</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Automatic rotation: {snapshot.policy.autoRotate ? 'enabled' : 'disabled'}</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Masked display: {snapshot.policy.maskedDisplay ? 'enabled' : 'disabled'}</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">No protected material in Git: {snapshot.policy.noProtectedMaterialInGit ? 'enforced' : 'not enforced'}</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">No protected material in logs: {snapshot.policy.noProtectedMaterialInLogs ? 'enforced' : 'not enforced'}</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">No protected material in docs: {snapshot.policy.noProtectedMaterialInDocs ? 'enforced' : 'not enforced'}</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">No protected material in frontend: {snapshot.policy.noProtectedMaterialInFrontend ? 'enforced' : 'not enforced'}</div>
          </div>
        </Card>
      </div>

      <div className="grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
        <Card title="Vault monitoring" description="Aggregated metrics are exposed without revealing protected material.">
          <div className="mt-4 space-y-3 text-sm text-slate-300">
            <div className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2">
              <span>Last access</span>
              <Badge variant="info">{snapshot.summary.lastAccess}</Badge>
            </div>
            <div className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2">
              <span>Last success</span>
              <Badge variant="success">{snapshot.summary.lastSuccess}</Badge>
            </div>
            <div className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2">
              <span>Last failure</span>
              <Badge variant={snapshot.summary.lastFailure === 'never' ? 'info' : 'warning'}>{snapshot.summary.lastFailure}</Badge>
            </div>
            <div className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2">
              <span>Alerts</span>
              <Badge variant={snapshot.summary.alerts > 0 ? 'warning' : 'success'}>{snapshot.summary.alerts}</Badge>
            </div>
            <div className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2">
              <span>Audit events</span>
              <Badge variant="info">{snapshot.summary.auditEvents}</Badge>
            </div>
          </div>
        </Card>
        <Card title="Audit trail" description="The trail remains masked, bounded, and ready for operational review.">
          <div className="mt-4 space-y-3 text-sm text-slate-300">
            <div className="rounded-xl border border-slate-800 px-3 py-2">Latest event: {snapshot.vault.auditTrail.latestEvent}</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Vault status: {snapshot.vault.status}</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Protected material remains encrypted outside the frontend and Git history.</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Scanning covers Git payloads, logs, and UI snapshots.</div>
          </div>
        </Card>
      </div>
    </PageShell>
  );
}
