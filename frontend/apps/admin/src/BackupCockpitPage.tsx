import { useEffect, useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { apiSdk, type BackupMetricsSnapshot, type BackupSnapshotRecord, type BackupStatusSnapshot } from '@api-sdk';
import { Badge, Button, Card, Input, PageShell, Select, Textarea } from '@ui';

type RestoreMode = 'postgresql' | 'media' | 'full';

type ConfigDraft = {
  timezone: string;
  backupRoot: string;
  stateRoot: string;
  logsRoot: string;
  tempRoot: string;
  googleDriveSchedule: string;
  localReplicationIntervalMinutes: string;
  retentionLocalDays: string;
  retentionGoogleDriveDays: string;
  retentionExternalMonths: string;
  retryCount: string;
  timeoutSeconds: string;
  alertsEnabled: boolean;
  verifyAfterUpload: boolean;
  automatedRestoreTests: boolean;
  restoreIsolationRequired: boolean;
};

const toRecord = (value: unknown): Record<string, unknown> => (value && typeof value === 'object' && !Array.isArray(value) ? (value as Record<string, unknown>) : {});

const toText = (value: unknown, fallback = '') => {
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

const statusVariant = (value: string) => {
  const normalized = value.trim().toUpperCase();
  if (normalized === 'PROTECTED') return 'success';
  if (normalized === 'DEGRADED' || normalized === 'WATCH') return 'warning';
  if (normalized === 'CRITICAL' || normalized === 'FAILED') return 'warning';
  if (normalized === 'AVAILABLE' || normalized === 'READY') return 'success';
  if (normalized === 'UNAVAILABLE' || normalized === 'UNKNOWN') return 'default';
  return 'info';
};

const providerVariant = (provider: Record<string, unknown>) => {
  const state = toText(provider.state, '').toUpperCase();
  if (state === 'AVAILABLE') return 'success';
  if (state === 'DEGRADED') return 'warning';
  if (state === 'UNAVAILABLE') return 'warning';
  return 'default';
};

const initialConfigDraft = (): ConfigDraft => ({
  timezone: 'Africa/Douala',
  backupRoot: '/var/backups/lawim',
  stateRoot: '/var/lib/lawim-backup',
  logsRoot: '/var/log/lawim-backup',
  tempRoot: '/var/tmp/lawim-backup',
  googleDriveSchedule: '02:00, 14:30',
  localReplicationIntervalMinutes: '5',
  retentionLocalDays: '2',
  retentionGoogleDriveDays: '30',
  retentionExternalMonths: '12',
  retryCount: '3',
  timeoutSeconds: '3600',
  alertsEnabled: true,
  verifyAfterUpload: true,
  automatedRestoreTests: true,
  restoreIsolationRequired: true
});

export function BackupCockpitPage() {
  const queryClient = useQueryClient();
  const [message, setMessage] = useState('');
  const [backupKind, setBackupKind] = useState('full');
  const [destination, setDestination] = useState('local');
  const [providerIdentifier, setProviderIdentifier] = useState('google-drive');
  const [restoreKind, setRestoreKind] = useState<RestoreMode>('postgresql');
  const [restoreTarget, setRestoreTarget] = useState('isolated');
  const [restoreBackupId, setRestoreBackupId] = useState('');
  const [configDraft, setConfigDraft] = useState<ConfigDraft>(initialConfigDraft);

  const snapshotQuery = useQuery<BackupStatusSnapshot>({
    queryKey: ['backup', 'snapshot'],
    queryFn: async () => (await apiSdk.getBackupSnapshot()).data
  });
  const historyQuery = useQuery<BackupSnapshotRecord[]>({
    queryKey: ['backup', 'history'],
    queryFn: async () => (await apiSdk.getBackupHistory(30)).data
  });
  const alertsQuery = useQuery<BackupSnapshotRecord[]>({
    queryKey: ['backup', 'alerts'],
    queryFn: async () => (await apiSdk.getBackupAlerts(30)).data
  });
  const providersQuery = useQuery<BackupSnapshotRecord[]>({
    queryKey: ['backup', 'providers'],
    queryFn: async () => (await apiSdk.getBackupProviders()).data
  });
  const metricsQuery = useQuery<BackupMetricsSnapshot>({
    queryKey: ['backup', 'metrics'],
    queryFn: async () => (await apiSdk.getBackupMetrics()).data
  });

  const refreshQueries = async () => {
    await queryClient.invalidateQueries({ queryKey: ['backup'] });
  };

  const commandMutation = useMutation({
    mutationFn: async (command:
      | { type: 'run' }
      | { type: 'test' }
      | { type: 'retry' }
      | { type: 'restore'; mode: RestoreMode }
      | { type: 'provider-test' }
      | { type: 'save-config' }) => {
      const latestBackupId = toText(snapshotQuery.data?.last_backup?.backup_id ?? historyQuery.data?.[0]?.backup_id ?? '', '');
      if (command.type === 'run') {
        return apiSdk.runBackup({
          kind: backupKind,
          destination,
          provider_name: providerIdentifier,
          trigger: 'cockpit'
        });
      }
      if (command.type === 'test') {
        return apiSdk.testBackup({
          kind: backupKind,
          destination
        });
      }
      if (command.type === 'retry') {
        return apiSdk.retryBackup();
      }
      if (command.type === 'provider-test') {
        return apiSdk.testBackupProvider({ provider_identifier: providerIdentifier });
      }
      if (command.type === 'restore') {
        const restoreId = restoreBackupId.trim() || latestBackupId;
        if (!restoreId) {
          throw new Error('Aucun backup disponible pour la restauration');
        }
        const databaseRestored = command.mode !== 'media';
        const mediaRestored = command.mode !== 'postgresql';
        return apiSdk.restoreBackup({
          backup_id: restoreId,
          kind: command.mode,
          target_environment: restoreTarget,
          database_restored: databaseRestored,
          media_restored: mediaRestored,
          notes: `Cockpit ${command.mode} restore`,
          success: true
        });
      }
      return apiSdk.patchBackupConfig({
        timezone: configDraft.timezone,
        backup_root: configDraft.backupRoot,
        state_root: configDraft.stateRoot,
        logs_root: configDraft.logsRoot,
        temp_root: configDraft.tempRoot,
        google_drive_schedule: configDraft.googleDriveSchedule.split(',').map((item) => item.trim()).filter(Boolean),
        local_replication_interval_minutes: Number.parseInt(configDraft.localReplicationIntervalMinutes, 10) || 5,
        retention_local_days: Number.parseInt(configDraft.retentionLocalDays, 10) || 2,
        retention_google_drive_days: Number.parseInt(configDraft.retentionGoogleDriveDays, 10) || 30,
        retention_external_months: Number.parseInt(configDraft.retentionExternalMonths, 10) || 12,
        retry_count: Number.parseInt(configDraft.retryCount, 10) || 3,
        timeout_seconds: Number.parseInt(configDraft.timeoutSeconds, 10) || 3600,
        alerts_enabled: configDraft.alertsEnabled,
        verify_after_upload: configDraft.verifyAfterUpload,
        automated_restore_tests: configDraft.automatedRestoreTests,
        restore_isolation_required: configDraft.restoreIsolationRequired
      });
    },
    onSuccess: async (_, command) => {
      const labels: Record<string, string> = {
        run: 'Sauvegarde lancée',
        test: 'Test de sauvegarde lancé',
        retry: 'Retry de sauvegarde lancé',
        'provider-test': 'Test provider exécuté',
        'save-config': 'Configuration sauvegardée',
        restore: `Restauration ${command.type === 'restore' ? command.mode : ''}`.trim()
      };
      setMessage(labels[command.type] ?? 'Commande exécutée');
      await refreshQueries();
    },
    onError: (error) => {
      setMessage(error instanceof Error ? error.message : 'Commande backup échouée');
    }
  });

  useEffect(() => {
    const configuration = toRecord(snapshotQuery.data?.configuration);
    if (Object.keys(configuration).length === 0) return;
    const schedule = Array.isArray(configuration.google_drive_schedule)
      ? configuration.google_drive_schedule.map((value) => toText(value)).filter(Boolean).join(', ')
      : toText(configuration.google_drive_schedule, '02:00, 14:30');
    setConfigDraft({
      timezone: toText(configuration.timezone, 'Africa/Douala'),
      backupRoot: toText(configuration.backup_root, '/var/backups/lawim'),
      stateRoot: toText(configuration.state_root, '/var/lib/lawim-backup'),
      logsRoot: toText(configuration.logs_root, '/var/log/lawim-backup'),
      tempRoot: toText(configuration.temp_root, '/var/tmp/lawim-backup'),
      googleDriveSchedule: schedule,
      localReplicationIntervalMinutes: toText(configuration.local_replication_interval_minutes, '5'),
      retentionLocalDays: toText(configuration.retention_local_days, '2'),
      retentionGoogleDriveDays: toText(configuration.retention_google_drive_days, '30'),
      retentionExternalMonths: toText(configuration.retention_external_months, '12'),
      retryCount: toText(configuration.retry_count, '3'),
      timeoutSeconds: toText(configuration.timeout_seconds, '3600'),
      alertsEnabled: Boolean(configuration.alerts_enabled ?? true),
      verifyAfterUpload: Boolean(configuration.verify_after_upload ?? true),
      automatedRestoreTests: Boolean(configuration.automated_restore_tests ?? true),
      restoreIsolationRequired: Boolean(configuration.restore_isolation_required ?? true)
    });
  }, [snapshotQuery.data]);

  useEffect(() => {
    const latestBackupId = toText(snapshotQuery.data?.last_backup?.backup_id ?? historyQuery.data?.[0]?.backup_id ?? '', '');
    if (!restoreBackupId && latestBackupId) {
      setRestoreBackupId(latestBackupId);
    }
  }, [historyQuery.data, restoreBackupId, snapshotQuery.data?.last_backup?.backup_id]);

  const snapshot = snapshotQuery.data;
  const metrics = metricsQuery.data ?? snapshot?.metrics;
  const providers = providersQuery.data ?? snapshot?.providers ?? snapshot?.destinations ?? [];
  const alerts = alertsQuery.data ?? snapshot?.alerts ?? [];
  const history = historyQuery.data ?? snapshot?.history ?? [];
  const config = toRecord(snapshot?.configuration);
  const systemd = toRecord(snapshot?.systemd);
  const version = toRecord(snapshot?.version);
  const lastBackup = toRecord(snapshot?.last_backup);
  const lastRestore = toRecord(snapshot?.last_restore);
  const nextBackup = toRecord(snapshot?.next_backup);
  const latestBackupId = toText(lastBackup.backup_id ?? history[0]?.backup_id ?? '', '');
  const globalStatus = toText(snapshot?.global_status, 'UNKNOWN');

  return (
    <PageShell
      eyebrow="Cockpit / Infrastructure / Sauvegardes"
      title="Backup Orchestrator Enterprise"
      description="Moteur d'orchestration des sauvegardes, vérification systemd, alertes, métriques, et restauration isolée."
      actions={
        <Button variant="secondary" onClick={() => void refreshQueries()}>
          Refresh
        </Button>
      }
    >
      <div className="relative overflow-hidden rounded-[2rem] border border-slate-800 bg-gradient-to-br from-slate-950 via-slate-900 to-emerald-950 p-6 text-white shadow-2xl">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(16,185,129,0.22),transparent_28%),radial-gradient(circle_at_bottom_left,rgba(56,189,248,0.18),transparent_24%)]" />
        <div className="relative grid gap-6 lg:grid-cols-[1.25fr_0.75fr]">
          <div>
            <div className="flex flex-wrap gap-2">
              <Badge variant={statusVariant(globalStatus)}>{globalStatus}</Badge>
              <Badge variant="info">LAWIM {toText(version.lawim, 'n/a')}</Badge>
              <Badge variant="default">Commit {toText(version.git_commit, 'n/a')}</Badge>
              <Badge variant={toText(systemd.active_state, '') === 'active' ? 'success' : 'warning'}>{toText(systemd.active_state, 'unknown')}</Badge>
            </div>
            <h2 className="mt-4 text-3xl font-semibold tracking-tight">Orchestration globale des sauvegardes</h2>
            <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-300">
              Le cockpit expose l’état réel du service systemd, les providers Google Drive, le stockage local, les alertes, les métriques et la restauration isolée.
            </p>
            <div className="mt-6 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
              <div className="rounded-2xl border border-white/10 bg-white/5 p-4 backdrop-blur">
                <div className="text-xs uppercase tracking-[0.28em] text-slate-400">Dernière sauvegarde</div>
                <div className="mt-2 text-lg font-semibold">{toText(lastBackup.finished_at ?? lastBackup.started_at ?? 'N/A')}</div>
              </div>
              <div className="rounded-2xl border border-white/10 bg-white/5 p-4 backdrop-blur">
                <div className="text-xs uppercase tracking-[0.28em] text-slate-400">Prochaine sauvegarde</div>
                <div className="mt-2 text-lg font-semibold">{toText(nextBackup.next_run_at ?? 'N/A')}</div>
              </div>
              <div className="rounded-2xl border border-white/10 bg-white/5 p-4 backdrop-blur">
                <div className="text-xs uppercase tracking-[0.28em] text-slate-400">RPO</div>
                <div className="mt-2 text-lg font-semibold">{Math.round(toNumber(metrics?.rpo_seconds, 0))} s</div>
              </div>
              <div className="rounded-2xl border border-white/10 bg-white/5 p-4 backdrop-blur">
                <div className="text-xs uppercase tracking-[0.28em] text-slate-400">RTO</div>
                <div className="mt-2 text-lg font-semibold">{Math.round(toNumber(metrics?.rto_seconds, 0))} s</div>
              </div>
            </div>
          </div>
          <Card title="Commandes" description="Run, test, retry, restore, provider test, configuration.">
            <div className="mt-4 space-y-4 text-sm text-slate-300">
              <Select label="Backup kind" value={backupKind} onChange={(event) => setBackupKind(event.target.value)}>
                <option value="full">Full</option>
                <option value="postgresql">PostgreSQL</option>
                <option value="media">Media</option>
              </Select>
              <Select label="Destination" value={destination} onChange={(event) => setDestination(event.target.value)}>
                <option value="local">Local</option>
                <option value="google-drive">Google Drive</option>
                <option value="external-disk">External disk</option>
              </Select>
              <Input label="Provider" value={providerIdentifier} onChange={(event) => setProviderIdentifier(event.target.value)} />
              <div className="grid gap-2 sm:grid-cols-2">
                <Button onClick={() => commandMutation.mutate({ type: 'run' })} disabled={commandMutation.isPending}>
                  Run backup
                </Button>
                <Button variant="secondary" onClick={() => commandMutation.mutate({ type: 'test' })} disabled={commandMutation.isPending}>
                  Test backup
                </Button>
                <Button variant="secondary" onClick={() => commandMutation.mutate({ type: 'retry' })} disabled={commandMutation.isPending}>
                  Retry
                </Button>
                <Button variant="secondary" onClick={() => commandMutation.mutate({ type: 'provider-test' })} disabled={commandMutation.isPending}>
                  Test provider
                </Button>
              </div>
            </div>
          </Card>
        </div>
        {message ? <div className="relative mt-4 rounded-2xl border border-emerald-400/30 bg-emerald-500/10 px-4 py-3 text-sm text-emerald-100">{message}</div> : null}
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
        <Card title="Global metrics" description="Exposition des métriques réutilisables par Grafana.">
          <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
            <MetricCard label="Temps moyen" value={`${Math.round(toNumber(metrics?.mean_duration_seconds, 0))} s`} />
            <MetricCard label="Taille moyenne" value={formatBytes(metrics?.average_size_bytes ?? metrics?.bytes_stored)} />
            <MetricCard label="Volume transféré" value={formatBytes(metrics?.transferred_bytes)} />
            <MetricCard label="Disponibilité" value={`${toNumber(metrics?.availability_percent, 0).toFixed(2)}%`} />
            <MetricCard label="Erreurs" value={`${Math.round(toNumber(metrics?.failed_jobs, 0))}`} />
            <MetricCard label="Checksum" value={`${Math.round(toNumber(metrics?.checksum_validations, 0))} ok / ${Math.round(toNumber(metrics?.checksum_failures, 0))} ko`} />
            <MetricCard label="Occupation disque" value={`${toNumber(metrics?.storage_usage_percent, 0).toFixed(2)}%`} />
            <MetricCard label="Occupation Drive" value={`${toNumber(metrics?.storage_usage_percent, 0).toFixed(2)}%`} />
          </div>
        </Card>
        <Card title="Systemd snapshot" description="Lecture fiable via `systemctl show` sans parsing de logs.">
          <div className="mt-4 space-y-3 text-sm text-slate-300">
            <InfoRow label="Dernier lancement" value={toText(systemd.last_launch_at ?? 'N/A')} />
            <InfoRow label="Prochaine exécution" value={toText(systemd.next_execution_at ?? 'N/A')} />
            <InfoRow label="Dernier retour" value={toText(systemd.last_return ?? systemd.result ?? 'unknown')} />
            <InfoRow label="Durée" value={`${Math.round(toNumber(systemd.duration_seconds, 0))} s`} />
            <InfoRow label="État" value={toText(systemd.state ?? 'unknown')} />
            <InfoRow label="Timer" value={toText(systemd.timer_state ?? 'unknown')} />
          </div>
        </Card>
      </div>

      <div className="grid gap-6 xl:grid-cols-[0.95fr_1.05fr]">
        <Card title="Providers" description="Google Drive, disque local et disque externe.">
          <div className="mt-4 space-y-3">
            {providers.map((provider) => {
              const record = toRecord(provider);
              const available = Boolean(record.available ?? false);
              return (
                <div key={toText(record.identifier, toText(record.name, 'provider'))} className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
                  <div className="flex items-center justify-between gap-3">
                    <div>
                      <div className="text-xs uppercase tracking-[0.28em] text-slate-500">{toText(record.identifier)}</div>
                      <div className="mt-1 text-lg font-semibold text-white">{toText(record.name, 'Provider')}</div>
                    </div>
                    <Badge variant={providerVariant(record)}>{toText(record.state, 'unknown')}</Badge>
                  </div>
                  <div className="mt-3 text-sm text-slate-400">{toText(record.kind)} · {toText(record.health, 'unknown')}</div>
                  <div className="mt-4 grid grid-cols-3 gap-3 text-xs text-slate-400">
                    <div>
                      <div className="text-slate-500">Free</div>
                      <div className="mt-1 text-slate-200">{formatBytes(record.free_space_bytes ?? record.available_bytes)}</div>
                    </div>
                    <div>
                      <div className="text-slate-500">Quota</div>
                      <div className="mt-1 text-slate-200">{formatBytes(record.quota_bytes ?? 0)}</div>
                    </div>
                    <div>
                      <div className="text-slate-500">Read only</div>
                      <div className="mt-1 text-slate-200">{record.read_only ? 'yes' : 'no'}</div>
                    </div>
                  </div>
                  <div className="mt-4 flex flex-wrap gap-2">
                    <Badge variant={available ? 'success' : 'warning'}>{available ? 'available' : 'offline'}</Badge>
                    <Badge variant="default">{toText(record.last_checked_at, 'n/a')}</Badge>
                  </div>
                </div>
              );
            })}
          </div>
        </Card>
        <Card title="Alertes" description="Google Drive indisponible, échec de sauvegarde, checksum, quota et restauration.">
          <div className="mt-4 space-y-3">
            {alerts.length === 0 ? <div className="rounded-2xl border border-slate-800 px-4 py-3 text-sm text-slate-400">Aucune alerte active.</div> : null}
            {alerts.map((alert) => {
              const record = toRecord(alert);
              return (
                <div key={toText(record.identifier, toText(record.code, 'alert'))} className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
                  <div className="flex items-center justify-between gap-3">
                    <div className="text-base font-semibold text-white">{toText(record.title, 'Alert')}</div>
                    <Badge variant={record.level === 'CRITICAL' ? 'warning' : 'info'}>{toText(record.level, 'INFO')}</Badge>
                  </div>
                  <div className="mt-2 text-sm text-slate-300">{toText(record.message)}</div>
                  <div className="mt-3 flex flex-wrap gap-2 text-xs text-slate-500">
                    <span>{toText(record.code, 'n/a')}</span>
                    <span>{toText(record.category, 'backup')}</span>
                    <span>{toText(record.target, 'global')}</span>
                  </div>
                </div>
              );
            })}
          </div>
        </Card>
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
        <Card title="Historique" description="Dernières opérations de sauvegarde et état d’exécution.">
          <div className="mt-4 space-y-3">
            {history.map((job) => {
              const record = toRecord(job);
              return (
                <div key={toText(record.identifier, toText(record.backup_id, 'job'))} className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
                  <div className="flex items-center justify-between gap-3">
                    <div>
                      <div className="text-sm font-semibold text-white">{toText(record.backup_id)}</div>
                      <div className="text-xs uppercase tracking-[0.28em] text-slate-500">{toText(record.kind)} · {toText(record.destination)}</div>
                    </div>
                    <Badge variant={statusVariant(toText(record.state, 'UNKNOWN'))}>{toText(record.state, 'UNKNOWN')}</Badge>
                  </div>
                  <div className="mt-3 grid gap-2 text-sm text-slate-400 md:grid-cols-3">
                    <InfoRow label="Started" value={toText(record.started_at ?? 'n/a')} />
                    <InfoRow label="Finished" value={toText(record.finished_at ?? 'n/a')} />
                    <InfoRow label="Duration" value={`${Math.round(toNumber(record.duration_seconds, 0))} s`} />
                  </div>
                </div>
              );
            })}
          </div>
        </Card>
        <Card title="Restauration" description="Test PostgreSQL, médias, complet, restauration isolée, historique et rapport.">
          <div className="mt-4 space-y-4">
            <Input label="Backup ID" value={restoreBackupId} onChange={(event) => setRestoreBackupId(event.target.value)} placeholder={latestBackupId || 'LAWIM-...'} />
            <Select label="Restore mode" value={restoreKind} onChange={(event) => setRestoreKind(event.target.value as RestoreMode)}>
              <option value="postgresql">Test PostgreSQL</option>
              <option value="media">Test médias</option>
              <option value="full">Test complet</option>
            </Select>
            <Input label="Target environment" value={restoreTarget} onChange={(event) => setRestoreTarget(event.target.value)} />
            <div className="grid gap-2 sm:grid-cols-2">
              <Button onClick={() => commandMutation.mutate({ type: 'restore', mode: restoreKind })} disabled={commandMutation.isPending}>
                Restore isolated
              </Button>
              <Button variant="secondary" onClick={() => commandMutation.mutate({ type: 'provider-test' })} disabled={commandMutation.isPending}>
                Provider test
              </Button>
            </div>
            <div className="grid gap-2 sm:grid-cols-3">
              <Button variant="secondary" onClick={() => commandMutation.mutate({ type: 'restore', mode: 'postgresql' })} disabled={commandMutation.isPending}>
                Test PostgreSQL
              </Button>
              <Button variant="secondary" onClick={() => commandMutation.mutate({ type: 'restore', mode: 'media' })} disabled={commandMutation.isPending}>
                Test médias
              </Button>
              <Button variant="secondary" onClick={() => commandMutation.mutate({ type: 'restore', mode: 'full' })} disabled={commandMutation.isPending}>
                Test complet
              </Button>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="text-xs uppercase tracking-[0.28em] text-slate-500">Rapport</div>
              <div className="mt-2 text-sm text-slate-300">{toText(lastRestore.report ? JSON.stringify(lastRestore.report) : 'Aucun rapport de restauration disponible.')}</div>
            </div>
          </div>
        </Card>
      </div>

      <Card title="Configuration" description="Patch de la configuration backup sans architecture parallèle.">
        <div className="mt-4 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          <Input label="Timezone" value={configDraft.timezone} onChange={(event) => setConfigDraft((current) => ({ ...current, timezone: event.target.value }))} />
          <Input label="Backup root" value={configDraft.backupRoot} onChange={(event) => setConfigDraft((current) => ({ ...current, backupRoot: event.target.value }))} />
          <Input label="State root" value={configDraft.stateRoot} onChange={(event) => setConfigDraft((current) => ({ ...current, stateRoot: event.target.value }))} />
          <Input label="Logs root" value={configDraft.logsRoot} onChange={(event) => setConfigDraft((current) => ({ ...current, logsRoot: event.target.value }))} />
          <Input label="Temp root" value={configDraft.tempRoot} onChange={(event) => setConfigDraft((current) => ({ ...current, tempRoot: event.target.value }))} />
          <Input label="Google Drive schedule" value={configDraft.googleDriveSchedule} onChange={(event) => setConfigDraft((current) => ({ ...current, googleDriveSchedule: event.target.value }))} />
          <Input label="Local replication interval" value={configDraft.localReplicationIntervalMinutes} onChange={(event) => setConfigDraft((current) => ({ ...current, localReplicationIntervalMinutes: event.target.value }))} />
          <Input label="Retention Google Drive days" value={configDraft.retentionGoogleDriveDays} onChange={(event) => setConfigDraft((current) => ({ ...current, retentionGoogleDriveDays: event.target.value }))} />
          <Input label="Retry count" value={configDraft.retryCount} onChange={(event) => setConfigDraft((current) => ({ ...current, retryCount: event.target.value }))} />
          <Input label="Timeout seconds" value={configDraft.timeoutSeconds} onChange={(event) => setConfigDraft((current) => ({ ...current, timeoutSeconds: event.target.value }))} />
          <div className="grid gap-3 md:col-span-2 xl:col-span-1">
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4 text-sm text-slate-300">
              <div className="flex items-center justify-between">
                <span>Alerts enabled</span>
                <Badge variant={configDraft.alertsEnabled ? 'success' : 'warning'}>{configDraft.alertsEnabled ? 'on' : 'off'}</Badge>
              </div>
              <div className="mt-3 flex flex-wrap gap-2">
                <Button variant="secondary" onClick={() => setConfigDraft((current) => ({ ...current, alertsEnabled: !current.alertsEnabled }))}>Toggle</Button>
                <Button variant="secondary" onClick={() => setConfigDraft((current) => ({ ...current, verifyAfterUpload: !current.verifyAfterUpload }))}>Verify upload</Button>
                <Button variant="secondary" onClick={() => setConfigDraft((current) => ({ ...current, automatedRestoreTests: !current.automatedRestoreTests }))}>Restore tests</Button>
              </div>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4 text-sm text-slate-300">
              <div className="flex items-center justify-between">
                <span>Restore isolation</span>
                <Badge variant={configDraft.restoreIsolationRequired ? 'success' : 'warning'}>{configDraft.restoreIsolationRequired ? 'required' : 'optional'}</Badge>
              </div>
              <div className="mt-3">
                <Button variant="secondary" onClick={() => setConfigDraft((current) => ({ ...current, restoreIsolationRequired: !current.restoreIsolationRequired }))}>Toggle isolation</Button>
              </div>
            </div>
          </div>
          <Textarea
            className="md:col-span-2 xl:col-span-3"
            label="Observed configuration"
            value={JSON.stringify({ systemd, version, config }, null, 2)}
            readOnly
          />
          <div className="md:col-span-2 xl:col-span-3 flex flex-wrap gap-3">
            <Button onClick={() => commandMutation.mutate({ type: 'save-config' })} disabled={commandMutation.isPending}>
              Save configuration
            </Button>
            <Button variant="secondary" onClick={() => void refreshQueries()}>
              Reload
            </Button>
          </div>
        </div>
      </Card>
    </PageShell>
  );
}

function MetricCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
      <div className="text-xs uppercase tracking-[0.28em] text-slate-500">{label}</div>
      <div className="mt-2 text-lg font-semibold text-white">{value}</div>
    </div>
  );
}

function InfoRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between gap-3 rounded-xl border border-slate-800 px-3 py-2">
      <span className="text-slate-500">{label}</span>
      <span className="font-medium text-slate-200">{value}</span>
    </div>
  );
}
