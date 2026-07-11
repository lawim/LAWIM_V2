import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import {
  apiSdk,
  type DisasterRecoveryBundleRecord,
  type DisasterRecoveryStatusSnapshot,
  type DisasterRecoveryValidationCheck,
  type DisasterRecoveryValidationSnapshot
} from '@api-sdk';
import { Badge, Button, Card, PageShell } from '@ui';
import { useState } from 'react';

const toRecord = (value: unknown): Record<string, unknown> => (value && typeof value === 'object' && !Array.isArray(value) ? (value as Record<string, unknown>) : {});

const toText = (value: unknown, fallback = 'N/A') => {
  if (value === null || value === undefined) return fallback;
  const text = String(value).trim();
  return text || fallback;
};

const toNumber = (value: unknown, fallback = 0) => {
  if (typeof value === 'number' && Number.isFinite(value)) return value;
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : fallback;
};

const formatBytes = (value: unknown) => {
  const bytes = Math.max(0, toNumber(value, 0));
  if (bytes >= 1_000_000_000) return `${(bytes / 1_000_000_000).toFixed(2)} GB`;
  if (bytes >= 1_000_000) return `${(bytes / 1_000_000).toFixed(2)} MB`;
  if (bytes >= 1_000) return `${(bytes / 1_000).toFixed(1)} KB`;
  return `${Math.round(bytes)} B`;
};

const formatDate = (value: unknown) => {
  const text = toText(value, '');
  if (!text || text === 'N/A') return 'N/A';
  const parsed = Date.parse(text);
  if (Number.isNaN(parsed)) return text;
  return new Date(parsed).toLocaleString();
};

const statusVariant = (value: string) => {
  const normalized = value.trim().toUpperCase();
  if (normalized === 'PASS' || normalized === 'READY' || normalized === 'PROTECTED') return 'success';
  if (normalized === 'FAIL' || normalized === 'FAILED' || normalized === 'DEGRADED' || normalized === 'WATCH' || normalized === 'BLOCKED') return 'warning';
  if (normalized === 'UNKNOWN' || normalized === 'PENDING') return 'default';
  return 'info';
};

const checkVariant = (check: DisasterRecoveryValidationCheck) => (check.passed ? 'success' : 'warning');

const computeRecoveryScore = (snapshot: DisasterRecoveryStatusSnapshot | undefined): number => {
  if (!snapshot) return 0;
  const latestBundle = snapshot.latest_bundle;
  const validation = snapshot.validation;
  let score = 100;

  if (!latestBundle) score -= 35;
  if (!validation) score -= 20;
  if (validation && !validation.manifest_present) score -= 20;
  if (validation && !validation.checksum_valid) score -= 15;
  if (validation && !validation.restore_ready) score -= 15;
  if (validation && !validation.compatible) score -= 10;
  if (validation && !validation.git_ok) score -= 10;
  if (validation && !validation.docker_ok) score -= 5;
  if (validation && !validation.postgresql_ok) score -= 5;

  if (latestBundle?.created_at) {
    const ageMs = Date.now() - Date.parse(latestBundle.created_at);
    if (Number.isFinite(ageMs) && ageMs > 0) {
      const ageDays = ageMs / (1000 * 60 * 60 * 24);
      if (ageDays > 7) {
        score -= Math.min(20, Math.round(ageDays));
      }
    }
  }

  return Math.max(0, Math.min(100, Math.round(score)));
};

const downloadBundle = async (bundleId: string) => {
  const { blob, filename } = await apiSdk.downloadDisasterRecoveryBundle(bundleId);
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement('a');
  anchor.href = url;
  anchor.download = filename;
  anchor.rel = 'noopener';
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  URL.revokeObjectURL(url);
};

export function DisasterRecoveryPage() {
  const queryClient = useQueryClient();
  const [message, setMessage] = useState('');

  const statusQuery = useQuery<DisasterRecoveryStatusSnapshot>({
    queryKey: ['disaster-recovery', 'status'],
    queryFn: async () => (await apiSdk.getDisasterRecoveryStatus()).data
  });
  const bundlesQuery = useQuery<DisasterRecoveryBundleRecord[]>({
    queryKey: ['disaster-recovery', 'bundles'],
    queryFn: async () => (await apiSdk.getDisasterRecoveryBundles(12)).data
  });

  const refresh = async () => {
    await queryClient.invalidateQueries({ queryKey: ['disaster-recovery'] });
  };

  const downloadMutation = useMutation({
    mutationFn: async (bundleId: string) => downloadBundle(bundleId),
    onSuccess: async (_, bundleId) => {
      setMessage(`Bundle ${bundleId} download started`);
      await refresh();
    },
    onError: (error) => {
      setMessage(error instanceof Error ? error.message : 'Bundle download failed');
    }
  });

  const status = statusQuery.data;
  const bundles = bundlesQuery.data ?? [];
  const validation = status?.validation;
  const latestBundle = status?.latest_bundle;
  const readiness = status?.readiness;
  const readinessSignals = readiness?.signals ?? [];
  const previewScore = readiness?.score ?? computeRecoveryScore(status);
  const readinessState = readiness?.state ?? (previewScore >= 90 ? 'READY' : previewScore >= 75 ? 'WATCH' : previewScore >= 50 ? 'DEGRADED' : 'BLOCKED');
  const backup = toRecord(status?.backup);
  const backupMetrics = toRecord(backup.metrics);
  const git = toRecord(status?.git);
  const versions = toRecord(status?.versions);
  const lastRestore = toRecord(backup.last_restore);
  const lastBackup = toRecord(backup.last_backup);
  const bundleRoot = toText(status?.bundle_root, '/var/lib/lawim-backup/recovery-bundles');
  const recoveryChecks = validation?.checks ?? [];

  return (
    <PageShell
      eyebrow="Cockpit / Infrastructure / Disaster Recovery"
      title="Disaster Recovery Framework"
      description="Recovery bundles, validation evidence, Git state, versions, and isolated rebuild readiness."
      actions={
        <>
          <Button variant="secondary" onClick={() => void refresh()}>
            Refresh
          </Button>
          <Button
            onClick={() => {
              if (latestBundle?.bundle_id) {
                downloadMutation.mutate(latestBundle.bundle_id);
              }
            }}
            disabled={!latestBundle?.bundle_id || downloadMutation.isPending}
          >
            Download latest bundle
          </Button>
        </>
      }
    >
      <div className="relative overflow-hidden rounded-[2rem] border border-slate-800 bg-gradient-to-br from-slate-950 via-slate-900 to-cyan-950 p-6 text-white shadow-2xl">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(34,197,94,0.22),transparent_26%),radial-gradient(circle_at_bottom_left,rgba(56,189,248,0.16),transparent_24%)]" />
        <div className="relative grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
          <div>
            <div className="flex flex-wrap gap-2">
              <Badge variant={statusVariant(validation?.restore_ready ? 'PASS' : 'FAIL')}>{validation?.restore_ready ? 'RESTORE READY' : 'NOT READY'}</Badge>
              <Badge variant={statusVariant(readinessState)}>{readinessState}</Badge>
              <Badge variant={statusVariant(validation?.git_ok ? 'PASS' : 'FAIL')}>{git.is_clean === true ? 'Git clean' : toText(git.status, 'Git status')}</Badge>
              <Badge variant="info">{toText(status?.git?.branch, 'branch unknown')}</Badge>
              <Badge variant="default">{toText(status?.versions?.lawim, 'LAWIM')}</Badge>
            </div>
            <h2 className="mt-4 text-3xl font-semibold tracking-tight">Reconstruction cockpit for a fresh host</h2>
            <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-300">
              The dashboard surfaces the latest bundle, validation evidence, version inventory, Git state, and the current recovery checklist.
            </p>
            <div className="mt-6 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
              <Metric
                label="Recovery Score"
                value={`${previewScore}%`}
                hint={readiness ? `Backend readiness state: ${readinessState}.` : 'Preview based on bundle freshness and validation signals.'}
              />
              <Metric label="Readiness State" value={readinessState} hint="Derived from DRF bundle, validation, test, and destination signals." />
              <Metric label="Latest test" value={formatDate(validation?.validated_at)} hint="Last automated recovery validation run." />
              <Metric label="Last reconstruction" value={formatDate(lastRestore.completed_at ?? lastRestore.created_at)} hint="Most recent restoration evidence." />
              <Metric label="Bundles" value={`${bundles.length}`} hint={`Bundle root: ${bundleRoot}`} />
            </div>
          </div>
          <Card title="Health summary" description="Validation and operational state at a glance.">
            <div className="mt-4 space-y-3 text-sm text-slate-300">
              <Row label="Bundle root" value={bundleRoot} />
              <Row label="Latest bundle" value={latestBundle?.bundle_id ?? 'None'} />
              <Row label="Manifest checksum" value={validation?.checksum_valid ? 'Valid' : 'Invalid'} />
              <Row label="Compatibility" value={validation?.compatible ? 'Compatible' : 'Mismatch'} />
              <Row label="Docker" value={validation?.docker_ok ? 'Available' : 'Unavailable'} />
              <Row label="PostgreSQL" value={validation?.postgresql_ok ? 'Available' : 'Unavailable'} />
            </div>
          </Card>
        </div>
        {message ? <div className="relative mt-4 rounded-2xl border border-cyan-400/30 bg-cyan-500/10 px-4 py-3 text-sm text-cyan-100">{message}</div> : null}
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.05fr_0.95fr]">
        <Card title="Latest bundle" description="Generated bundle metadata and download control.">
          {latestBundle ? (
            <div className="mt-4 grid gap-4">
              <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
                <div className="flex flex-wrap items-start justify-between gap-3">
                  <div>
                    <div className="text-xs uppercase tracking-[0.28em] text-slate-500">{latestBundle.environment}</div>
                    <div className="mt-1 text-xl font-semibold text-white">{latestBundle.bundle_id}</div>
                    <div className="mt-2 text-sm text-slate-400">{formatDate(latestBundle.created_at)}</div>
                  </div>
                  <Badge variant={statusVariant(validation?.restore_ready ? 'PASS' : 'FAIL')}>{validation?.restore_ready ? 'READY' : latestBundle.validation_state}</Badge>
                </div>
                <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4 text-sm text-slate-300">
                  <Row label="Size" value={formatBytes(latestBundle.size_bytes)} />
                  <Row label="Files" value={`${latestBundle.file_count}`} />
                  <Row label="Checksum" value={latestBundle.checksum} />
                  <Row label="Path" value={latestBundle.path} />
                </div>
                <div className="mt-4 flex flex-wrap gap-2">
                  <Button
                    onClick={() => downloadMutation.mutate(latestBundle.bundle_id)}
                    disabled={downloadMutation.isPending}
                  >
                    Download bundle
                  </Button>
                </div>
              </div>
              <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
                <div className="text-xs uppercase tracking-[0.28em] text-slate-500">Last backup evidence</div>
                <div className="mt-3 grid gap-3 md:grid-cols-2 text-sm text-slate-300">
                  <Row label="Last backup" value={formatDate(lastBackup.completed_at ?? lastBackup.started_at)} />
                  <Row label="Last restore" value={formatDate(lastRestore.completed_at ?? lastRestore.created_at)} />
                  <Row label="RPO" value={`${Math.round(toNumber(backupMetrics.rpo_seconds, 0))} s`} />
                  <Row label="RTO" value={`${Math.round(toNumber(backupMetrics.rto_seconds, 0))} s`} />
                </div>
              </div>
            </div>
          ) : (
            <div className="mt-4 rounded-2xl border border-slate-800 px-4 py-3 text-sm text-slate-400">No recovery bundle has been generated yet.</div>
          )}
        </Card>

        <Card title="Validation checks" description="Explicit pass/fail evidence from the automated recovery validation.">
          {validation ? (
            <div className="mt-4 space-y-3">
              {recoveryChecks.map((check) => (
                <div key={check.name} className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
                  <div className="flex items-center justify-between gap-3">
                    <div>
                      <div className="text-base font-semibold text-white">{check.name}</div>
                      <div className="mt-1 text-sm text-slate-400">{check.detail}</div>
                    </div>
                    <Badge variant={checkVariant(check)}>{check.status.toUpperCase()}</Badge>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="mt-4 rounded-2xl border border-slate-800 px-4 py-3 text-sm text-slate-400">Validation data is not available yet.</div>
          )}
        </Card>
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.05fr_0.95fr]">
        <Card title="Recovery bundles" description="Bundle inventory with direct download controls.">
          <div className="mt-4 space-y-3">
            {bundles.length === 0 ? <div className="rounded-2xl border border-slate-800 px-4 py-3 text-sm text-slate-400">No bundles available.</div> : null}
            {bundles.map((bundle) => (
              <div key={bundle.bundle_id} className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
                <div className="flex flex-wrap items-start justify-between gap-3">
                  <div>
                    <div className="text-xs uppercase tracking-[0.28em] text-slate-500">{bundle.environment}</div>
                    <div className="mt-1 text-lg font-semibold text-white">{bundle.bundle_id}</div>
                    <div className="mt-1 text-sm text-slate-400">{formatDate(bundle.created_at)}</div>
                  </div>
                  <Badge variant={statusVariant(bundle.validation_state)}>{bundle.validation_state}</Badge>
                </div>
                <div className="mt-4 grid gap-3 md:grid-cols-3 text-sm text-slate-300">
                  <Row label="Size" value={formatBytes(bundle.size_bytes)} />
                  <Row label="Files" value={`${bundle.file_count}`} />
                  <Row label="Checksum" value={bundle.checksum} />
                </div>
                <div className="mt-4 flex flex-wrap gap-2">
                  <Button variant="secondary" onClick={() => downloadMutation.mutate(bundle.bundle_id)} disabled={downloadMutation.isPending}>
                    Download
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </Card>

        <Card title="Git, versions, checklist" description="Context required to rebuild LAWIM on a fresh server.">
          <div className="mt-4 grid gap-4">
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="text-xs uppercase tracking-[0.28em] text-slate-500">Git state</div>
              <div className="mt-3 grid gap-2 text-sm text-slate-300">
                <Row label="Remote" value={toText(git.remote, 'unknown')} />
                <Row label="Branch" value={toText(git.branch, 'unknown')} />
                <Row label="SHA" value={toText(git.sha, 'unknown')} />
                <Row label="Tags" value={Array.isArray(git.tags) ? git.tags.join(', ') : toText(git.tags, 'none')} />
                <Row label="Status" value={toText(git.status, 'unknown')} />
              </div>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="text-xs uppercase tracking-[0.28em] text-slate-500">Versions</div>
              <div className="mt-3 grid gap-2 md:grid-cols-2 text-sm text-slate-300">
                <Row label="LAWIM" value={toText(versions.lawim, 'unknown')} />
                <Row label="Docker" value={toText(versions.docker, 'unavailable')} />
                <Row label="Compose" value={toText(versions.docker_compose, 'unavailable')} />
                <Row label="PostgreSQL" value={toText(versions.postgresql, 'unavailable')} />
                <Row label="Python" value={toText(versions.python, 'unknown')} />
                <Row label="Git" value={toText(versions.git, 'unknown')} />
                <Row label="Node" value={toText(versions.node, 'unknown')} />
                <Row label="npm" value={toText(versions.npm, 'unknown')} />
                <Row label="systemd" value={toText(versions.systemd, 'unknown')} />
                <Row label="Kernel" value={toText(versions.kernel, 'unknown')} />
              </div>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="text-xs uppercase tracking-[0.28em] text-slate-500">Readiness signals</div>
              <div className="mt-3 space-y-3 text-sm text-slate-300">
                {readinessSignals.length > 0 ? (
                  readinessSignals.map((signal) => (
                    <div key={signal.name} className="rounded-xl border border-slate-800 bg-slate-900/80 p-3">
                      <div className="flex flex-wrap items-center justify-between gap-2">
                        <div className="font-medium text-white">{signal.name}</div>
                        <Badge variant={signal.passed ? 'success' : 'warning'}>{signal.passed ? 'PASS' : 'FAIL'}</Badge>
                      </div>
                      <div className="mt-2 text-xs uppercase tracking-[0.24em] text-slate-500">Weight {signal.weight}</div>
                      <div className="mt-2 text-sm text-slate-300">{signal.detail}</div>
                    </div>
                  ))
                ) : (
                  <div className="rounded-xl border border-slate-800 px-4 py-3 text-sm text-slate-400">No readiness signals are available yet.</div>
                )}
              </div>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="text-xs uppercase tracking-[0.28em] text-slate-500">Checklist</div>
              <pre className="mt-3 max-h-80 overflow-auto whitespace-pre-wrap rounded-xl bg-slate-900/80 p-4 text-xs leading-6 text-slate-300">
                {toText(status?.checklist, 'No checklist available.')}
              </pre>
            </div>
          </div>
        </Card>
      </div>
    </PageShell>
  );
}

function Metric({ label, value, hint }: { label: string; value: string; hint: string }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 p-4 backdrop-blur">
      <div className="text-xs uppercase tracking-[0.28em] text-slate-400">{label}</div>
      <div className="mt-2 text-2xl font-semibold text-white">{value}</div>
      <div className="mt-2 text-xs leading-5 text-slate-300">{hint}</div>
    </div>
  );
}

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <div className="text-xs uppercase tracking-[0.24em] text-slate-500">{label}</div>
      <div className="mt-1 break-words text-sm text-slate-200">{value}</div>
    </div>
  );
}
