export interface ApiResponse<T> {
  data: T;
  message?: string;
}

export interface PropertySummary {
  id: string;
  title: string;
  location: string;
  price: number;
  type: string;
  status?: string;
}

export interface PropertyDetail extends PropertySummary {
  description: string;
  surface: string;
  bedrooms: number;
  bathrooms: number;
}

export interface ProjectSummary {
  id: number;
  title: string;
  status: string;
  project_type: string;
  objective: string;
  location_city?: string;
  budget_min?: number | null;
  budget_max?: number | null;
}

export interface MarketListing {
  id: string;
  title: string;
  category: string;
  price: number;
  status: string;
}

export interface UserProfile {
  id: string;
  name: string;
  role: string;
  email: string;
  full_name?: string;
  username?: string;
  phone_e164?: string;
  preferred_language?: string;
}

export interface DashboardSummary {
  properties: number;
  opportunities: number;
  communications: number;
  pendingTasks: number;
}

export interface BackupStatusCard {
  label: string;
  value: string;
}

export interface BackupSnapshotRecord extends Record<string, unknown> {
  identifier: string;
}

export interface BackupMetricsSnapshot extends Record<string, unknown> {
  total_jobs: number;
  successful_jobs: number;
  failed_jobs: number;
  mean_duration_seconds: number;
  max_duration_seconds: number;
  bytes_stored: number;
  storage_usage_percent: number;
  last_success_at?: string | null;
  last_failed_at?: string | null;
  average_size_bytes: number;
  total_size_bytes: number;
  transferred_bytes: number;
  upload_time_seconds: number;
  restore_time_seconds: number;
  alert_count: number;
  checksum_validations: number;
  checksum_failures: number;
  availability_percent: number;
  rpo_seconds: number;
  rto_seconds: number;
  last_backup_age_seconds: number;
  calculated_at: string;
}

export interface BackupStatusSnapshot extends Record<string, unknown> {
  global_status: string;
  policy: Record<string, unknown>;
  configuration: Record<string, unknown>;
  destinations: BackupSnapshotRecord[];
  providers: BackupSnapshotRecord[];
  alerts: BackupSnapshotRecord[];
  events: BackupSnapshotRecord[];
  history: BackupSnapshotRecord[];
  jobs: BackupSnapshotRecord[];
  restores: BackupSnapshotRecord[];
  last_backup: BackupSnapshotRecord | null;
  last_failed_backup: BackupSnapshotRecord | null;
  next_backup: BackupSnapshotRecord | null;
  last_restore: BackupSnapshotRecord | null;
  metrics: BackupMetricsSnapshot;
  systemd: Record<string, unknown>;
  version: Record<string, unknown>;
  counts: Record<string, number>;
}

export interface DisasterRecoveryBundleRecord extends Record<string, unknown> {
  bundle_id: string;
  created_at: string;
  size_bytes: number;
  checksum: string;
  file_count: number;
  environment: string;
  validation_state: string;
  path: string;
}

export interface DisasterRecoveryValidationCheck {
  name: string;
  passed: boolean;
  status: string;
  detail: string;
}

export interface DisasterRecoveryValidationSnapshot extends Record<string, unknown> {
  bundle_id: string;
  manifest_present: boolean;
  checksum_valid: boolean;
  compatible: boolean;
  git_ok: boolean;
  docker_ok: boolean;
  postgresql_ok: boolean;
  restore_ready: boolean;
  missing_files: string[];
  warnings: string[];
  checks: DisasterRecoveryValidationCheck[];
  duration_seconds: number;
  validated_at: string;
}

export interface DisasterRecoveryReadinessSignal {
  name: string;
  passed: boolean;
  weight: number;
  detail: string;
}

export interface DisasterRecoveryReadinessSnapshot extends Record<string, unknown> {
  score: number;
  maximum_score: number;
  state: string;
  bundle_id: string;
  bundle_age_days: number | null;
  rpo_seconds: number;
  rto_seconds: number;
  signals: DisasterRecoveryReadinessSignal[];
  reasons: string[];
  calculated_at: string;
}

export interface DisasterRecoveryStatusSnapshot extends Record<string, unknown> {
  bundle_root: string;
  latest_bundle: DisasterRecoveryBundleRecord | null;
  validation: DisasterRecoveryValidationSnapshot | null;
  readiness: DisasterRecoveryReadinessSnapshot | null;
  git: Record<string, unknown>;
  versions: Record<string, unknown>;
  backup: Record<string, unknown>;
  checklist: string | null;
}

export interface FavoriteItem {
  id: string;
  title: string;
  type: string;
  score: number;
}

export interface NotificationItem {
  id: string;
  title: string;
  message: string;
  read: boolean;
}

export interface RequestItem {
  id: string;
  title: string;
  status: string;
}

export interface DocumentItem {
  id: string;
  title: string;
  kind: string;
}

export interface FinancialLine extends Record<string, unknown> {
  description: string;
  quantity: number;
  unit_price_minor: number;
  total_minor?: number;
}

export interface FinancialProduct extends Record<string, unknown> {
  id: number;
  code: string;
  name: string;
  description: string;
  category: string;
  status: string;
  unit: string;
  default_price_minor: number;
  currency: string;
  tax_rate_bps: number;
}

export interface PricingBreakdown extends Record<string, unknown> {
  subtotal_minor: number;
  discount_minor: number;
  fee_minor: number;
  tax_minor: number;
  total_minor: number;
  currency: string;
  lines: FinancialLine[];
}

export interface Quote extends Record<string, unknown> {
  id: number;
  number: string;
  status: string;
  currency: string;
  total_minor: number;
  lines: FinancialLine[];
  breakdown?: PricingBreakdown;
}

export interface Invoice extends Record<string, unknown> {
  id: number;
  number: string;
  status: string;
  currency: string;
  total_minor: number;
  balance_minor: number;
  amount_paid_minor: number;
  lines: FinancialLine[];
}

export interface Receipt extends Record<string, unknown> {
  id: number;
  number: string;
  status: string;
  currency: string;
  amount_minor: number;
  invoice_id?: number | null;
  payment_intent_id?: number | null;
}

export interface PaymentProvider extends Record<string, unknown> {
  id: number;
  code: string;
  name: string;
  status: string;
  environment: string;
  supported_currencies?: string[];
  supported_channels?: string[];
  supports_collection?: boolean;
  supports_refund?: boolean;
  supports_status_query?: boolean;
  supports_webhook?: boolean;
  supports_payout?: boolean;
  priority?: number;
}

export interface PaymentIntent extends Record<string, unknown> {
  id: number;
  number: string;
  status: string;
  amount_minor: number;
  currency: string;
  provider_code: string;
  phone_number_e164?: string | null;
  idempotency_key?: string | null;
}

export interface PaymentAttempt extends Record<string, unknown> {
  id: number;
  status: string;
  provider_code: string;
  provider_reference?: string | null;
  idempotency_key?: string | null;
}

export interface PaymentTransaction extends Record<string, unknown> {
  id: number;
  status: string;
  type: string;
  direction: string;
  amount_minor: number;
  currency: string;
  provider_reference?: string | null;
}

export interface ProviderEvent extends Record<string, unknown> {
  id: number;
  provider_code: string;
  event_type: string;
  provider_event_id: string;
  status: string;
}

export interface Refund extends Record<string, unknown> {
  id: number;
  number: string;
  status: string;
  amount_minor: number;
  currency: string;
  payment_transaction_id?: number | null;
}

export interface SubscriptionPlan extends Record<string, unknown> {
  id: number;
  code: string;
  name: string;
  status: string;
  currency: string;
  price_minor: number;
  frequency: string;
}

export interface Subscription extends Record<string, unknown> {
  id: number;
  status: string;
  customer_user_id?: number | null;
  plan_id?: number | null;
  renewal_mode?: string | null;
}

export interface SubscriptionCycle extends Record<string, unknown> {
  id: number;
  status: string;
  subscription_id?: number | null;
  amount_minor: number;
  currency: string;
}

export interface CommissionRule extends Record<string, unknown> {
  id: number;
  code: string;
  name: string;
  status: string;
}

export interface Commission extends Record<string, unknown> {
  id: number;
  status: string;
  amount_minor: number;
  currency: string;
  beneficiary_user_id?: number | null;
}

export interface Payout extends Record<string, unknown> {
  id: number;
  status: string;
  amount_minor: number;
  currency: string;
  beneficiary_user_id?: number | null;
}

export interface LedgerAccount extends Record<string, unknown> {
  id: number;
  code: string;
  name: string;
  status: string;
}

export interface LedgerEntry extends Record<string, unknown> {
  id: number;
  status: string;
  amount_minor: number;
  currency: string;
  source_type: string;
  transaction_id?: number | null;
}

export interface ReconciliationRecord extends Record<string, unknown> {
  id: number;
  status: string;
  conflict_type: string;
  currency: string;
}

export interface FinancialAuditEvent extends Record<string, unknown> {
  id: number;
  action: string;
  object_type: string;
  status: string;
}

export interface FinancialDashboardSummary extends Record<string, unknown> {
  invoice_count: number;
  payment_count: number;
  receipt_count: number;
  refund_count: number;
  subscription_count: number;
  commission_count: number;
  payout_count: number;
  reconciliation_conflict_count: number;
  total_factured_minor: number;
  total_paid_minor: number;
  outstanding_minor: number;
}

export interface ProviderHealth extends Record<string, unknown> {
  code: string;
  name: string;
  status: string;
  environment: string;
  available: boolean;
  details: Record<string, unknown>;
}

export interface AuthCredentials {
  identifier?: string;
  email?: string;
  password: string;
}

export interface RegisterPayload {
  full_name: string;
  email: string;
  username: string;
  phone_e164: string;
  password: string;
  password_confirmation: string;
  preferred_language: string;
  accept_terms: boolean;
}

export interface RegisterResponse {
  user: UserProfile;
  token: string;
  roles: string[];
}

export interface AuthSession {
  user: UserProfile;
  token: string;
  roles: string[];
}

export interface EstimationPayload {
  address: string;
  surface: string;
  type: string;
  expectedPrice: string;
  notes?: string;
}

export interface EstimationResult {
  estimate: string;
  confidence: string;
}

export interface AssistantMessagePayload {
  message: string;
  project_id?: number;
  session_id?: number;
  agent_key?: string;
}

export interface AssistantChatPayload extends AssistantMessagePayload {
  project_id: number;
}

export interface AssistantReply {
  reply: string;
  suggestions: string[];
  session_id?: number;
  agent_key?: string;
  mode?: string;
  provider?: string;
  context_snapshot_key?: string;
  project_id?: number;
  raw?: Record<string, unknown>;
}

/* ── Maintenance mode types ─────────────────────────────────── */

export interface MaintenanceMessagePayload {
  channel: string;
  message: string;
  channel_identity_id?: number;
  delivery_metadata?: Record<string, unknown>;
  handover_requested?: boolean;
}

export interface MaintenanceStatus {
  maintenance_mode: boolean;
  message: string;
  flags: Record<string, boolean>;
  services: Record<string, string>;
}

export interface MaintenanceMessageResult {
  message: Record<string, unknown>;
  response: string;
  automated_processing: 'blocked';
  handover_requested: boolean;
}

export interface CreatePropertyPayload {
  title: string;
  summary: string;
  city: string;
  country: string;
  latitude?: number | null;
  longitude?: number | null;
  price_min?: number | null;
  price_max?: number | null;
  currency?: string;
  status?: string;
  availability?: string;
  property_type?: string;
  owner_organization_id?: number | null;
  address_line?: string | null;
  region?: string | null;
  postal_code?: string | null;
  metadata?: Record<string, unknown> | string | null;
  bedrooms?: number;
  bathrooms?: number;
  area_sqm?: number;
  listing_code?: string | null;
}

const mockDelay = () => Promise.resolve();
const env = (import.meta as ImportMeta & { env?: Record<string, string | boolean | undefined> }).env ?? {};
let useMocks = env.VITE_LAWIM_USE_MOCKS === 'true';
let apiBaseOverride: string | null = null;

export function setApiBaseForTesting(value: string | null) {
  apiBaseOverride = value ? value.replace(/\/$/, '') || '/api' : null;
}

export function setMockModeForTesting(value: boolean | null) {
  useMocks = value ?? env.VITE_LAWIM_USE_MOCKS === 'true';
}

const getApiBase = () => apiBaseOverride ?? (String(env.VITE_LAWIM_API_URL ?? '').replace(/\/$/, '') || '/api');

const readStorageToken = () => {
  if (typeof window === 'undefined') return null;
  return window.localStorage.getItem('lawim_token');
};

const normalizePayload = <T>(payload: unknown, fallback: T): T => {
  if (payload == null) return fallback;
  if (Array.isArray(payload)) return payload as T;
  if (typeof payload === 'object') {
    const record = payload as Record<string, unknown>;
    if (Object.prototype.hasOwnProperty.call(record, 'data') && record.data !== undefined) {
      return record.data as T;
    }
    if (Array.isArray(record.data)) return record.data as T;
    if (Object.prototype.hasOwnProperty.call(record, 'user') || Object.prototype.hasOwnProperty.call(record, 'token') || Object.prototype.hasOwnProperty.call(record, 'session')) {
      return payload as T;
    }
    if (Array.isArray(record.items)) return record.items as T;
    if (Array.isArray(record.results)) return record.results as T;
    if (Array.isArray(record.properties)) return record.properties as T;
    if (Array.isArray(record.projects)) return record.projects as T;
    if (Array.isArray(record.agents)) return record.agents as T;
    if (Array.isArray(record.prompts)) return record.prompts as T;
    if (Array.isArray(record.contacts)) return record.contacts as T;
    if (Array.isArray(record.marketplace)) return record.marketplace as T;
    if (Array.isArray(record.notifications)) return record.notifications as T;
    if (Array.isArray(record.documents)) return record.documents as T;
    if (Array.isArray(record.requests)) return record.requests as T;
    if (Array.isArray(record.favorites)) return record.favorites as T;
    if (Array.isArray(record.users)) return record.users as T;
    if (Array.isArray(record.roles)) return record.roles as T;
    if (Array.isArray(record.messages)) return record.messages as T;
    if (Array.isArray(record.matches)) return record.matches as T;
    if (Array.isArray(record.workflows)) return record.workflows as T;
    if (Array.isArray(record.analytics)) return record.analytics as T;
    if (Array.isArray(record.security)) return record.security as T;
  }
  return payload as T;
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

const buildQuery = (params: Record<string, unknown>) => {
  const query = new URLSearchParams();
  for (const [key, value] of Object.entries(params)) {
    if (value === undefined || value === null || value === '') continue;
    query.set(key, String(value));
  }
  return query.toString();
};

const joinLocation = (...parts: Array<unknown>) => parts.map((part) => toText(part)).filter(Boolean).join(' • ');

const mapPropertySummary = (value: unknown): PropertySummary => {
  const record = toRecord(value);
  const property = toRecord(record.property ?? record);
  const geo = toRecord(property.geo);
  const price = toRecord(property.price);
  const listing = toRecord(record.listing);
  const profile = toRecord(record.profile);
  const location = joinLocation(geo.city ?? property.city ?? property.location ?? record.city ?? record.location, geo.region ?? property.region ?? record.region);
  const priceValue = toNumber(price.min ?? price.max ?? property.price_min ?? property.price_max ?? record.price_min ?? record.price_max);
  const type = toText(property.property_type ?? profile.property_type ?? property.type ?? listing.title ?? record.property_type ?? record.type, 'Bien');
  const status = toText(property.status ?? listing.status ?? record.status ?? 'draft', 'draft');

  return {
    id: toText(property.id ?? record.id ?? record.property_id ?? ''),
    title: toText(property.title ?? listing.title ?? record.title ?? 'Property'),
    location: location || toText(geo.country ?? property.country ?? record.country ?? 'Cameroon'),
    price: priceValue,
    type,
    status
  };
};

const mapPropertyDetail = (value: unknown): PropertyDetail | null => {
  const record = toRecord(value);
  const property = toRecord(record.property ?? record);
  if (Object.keys(property).length === 0) {
    return null;
  }
  const summary = mapPropertySummary(value);
  const metrics = toRecord(property.metrics);
  const surfaceValue = property.surface ?? metrics.area_sqm ?? property.area_sqm ?? record.surface ?? null;
  const bedroomsValue = metrics.bedrooms ?? property.bedrooms ?? record.bedrooms ?? 0;
  const bathroomsValue = metrics.bathrooms ?? property.bathrooms ?? record.bathrooms ?? 0;

  return {
    ...summary,
    description: toText(property.summary ?? record.summary ?? toRecord(record.listing).title ?? summary.title, summary.title),
    surface: surfaceValue == null || surfaceValue === '' ? 'N/A' : `${toText(surfaceValue)}${String(surfaceValue).includes('m²') ? '' : ' m²'}`,
    bedrooms: Math.max(0, Math.round(toNumber(bedroomsValue))),
    bathrooms: Math.max(0, Math.round(toNumber(bathroomsValue)))
  };
};

const mapProjectSummary = (value: unknown): ProjectSummary => {
  const record = toRecord(value);
  return {
    id: Math.round(toNumber(record.id ?? 0)),
    title: toText(record.title ?? record.name ?? 'Project'),
    status: toText(record.status ?? 'draft'),
    project_type: toText(record.project_type ?? record.type ?? 'project'),
    objective: toText(record.objective ?? record.description ?? ''),
    location_city: record.location_city ? toText(record.location_city) : undefined,
    budget_min: record.budget_min === undefined || record.budget_min === null ? null : toNumber(record.budget_min),
    budget_max: record.budget_max === undefined || record.budget_max === null ? null : toNumber(record.budget_max)
  };
};

const mapBackupCards = (snapshot: BackupStatusSnapshot): BackupStatusCard[] => {
  const lastBackup = toRecord(snapshot.last_backup);
  const nextBackup = toRecord(snapshot.next_backup);
  const policy = toRecord(snapshot.policy);
  const retention = toRecord(policy.retention);
  const metrics = snapshot.metrics ?? {
    rpo_seconds: 0,
    rto_seconds: 0,
    availability_percent: 0
  };
  return [
    { label: 'Global status', value: toText(snapshot.global_status, 'unknown') },
    { label: 'Last backup', value: toText(lastBackup.finished_at ?? lastBackup.started_at ?? 'N/A') },
    { label: 'Retention', value: `${Math.max(1, Math.round(toNumber(retention.google_drive_days ?? 30)))} days` },
    { label: 'Next backup', value: toText(nextBackup.next_run_at ?? 'N/A') },
    { label: 'RPO', value: `${Math.round(toNumber(metrics.rpo_seconds, 0))} s` },
    { label: 'RTO', value: `${Math.round(toNumber(metrics.rto_seconds, 0))} s` },
    { label: 'Availability', value: `${toNumber(metrics.availability_percent, 0).toFixed(2)}%` }
  ];
};

const buildMockBackupSnapshot = (): BackupStatusSnapshot => ({
  global_status: 'PROTECTED',
  policy: {
    google_drive: { time: ['02:00', '14:30'], timezone: 'Africa/Douala' },
    local_replication_interval_minutes: 5,
    external_backup_weekday: 'sunday',
    retention: { local_days: 2, google_drive_days: 30, external_months: 12 },
    retry_count: 3,
    timeout_seconds: 3600,
    verify_after_upload: true,
    automated_restore_tests: true
  },
  configuration: {
    enabled: true,
    timezone: 'Africa/Douala',
    backup_root: '/var/backups/lawim',
    state_root: '/var/lib/lawim-backup',
    logs_root: '/var/log/lawim-backup',
    temp_root: '/var/tmp/lawim-backup'
  },
  destinations: [
    { identifier: 'local', name: 'Local disk', kind: 'local_disk', state: 'AVAILABLE', available: true, free_space_bytes: 1024, last_checked_at: '2026-07-11T00:00:00+00:00' },
    { identifier: 'google-drive', name: 'Google Drive', kind: 'google_drive', state: 'AVAILABLE', available: true, free_space_bytes: 2048, last_checked_at: '2026-07-11T00:00:00+00:00' },
    { identifier: 'external-disk', name: 'External disk', kind: 'external_disk', state: 'UNKNOWN', available: false, free_space_bytes: 0, last_checked_at: '2026-07-11T00:00:00+00:00' }
  ],
  providers: [
    { identifier: 'local', name: 'Local disk', kind: 'local_disk', state: 'AVAILABLE', available: true, free_space_bytes: 1024, last_checked_at: '2026-07-11T00:00:00+00:00' },
    { identifier: 'google-drive', name: 'Google Drive', kind: 'google_drive', state: 'AVAILABLE', available: true, free_space_bytes: 2048, last_checked_at: '2026-07-11T00:00:00+00:00' },
    { identifier: 'external-disk', name: 'External disk', kind: 'external_disk', state: 'UNKNOWN', available: false, free_space_bytes: 0, last_checked_at: '2026-07-11T00:00:00+00:00' }
  ],
  alerts: [],
  events: [],
  history: [
    {
      identifier: 'job-1',
      backup_id: 'LAWIM-20260711-020000',
      kind: 'full',
      state: 'COMPLETED',
      destination: 'local',
      provider: 'local',
      trigger: 'scheduler',
      created_at: '2026-07-11T00:00:00+00:00',
      started_at: '2026-07-11T00:00:00+00:00',
      finished_at: '2026-07-11T00:05:00+00:00',
      duration_seconds: 300,
      checksum: 'mock',
      encrypted: false,
      validation_result: 'verified',
      systemd_unit: 'lawim-backup.service',
      attempt: 1,
      notes: '',
      source: 'backup',
      artifact_count: 1,
      alert_count: 0,
      size_bytes: 1024
    }
  ],
  jobs: [
    {
      identifier: 'job-1',
      backup_id: 'LAWIM-20260711-020000',
      kind: 'full',
      state: 'COMPLETED',
      destination: 'local',
      provider: 'local',
      trigger: 'scheduler',
      created_at: '2026-07-11T00:00:00+00:00',
      started_at: '2026-07-11T00:00:00+00:00',
      finished_at: '2026-07-11T00:05:00+00:00',
      duration_seconds: 300,
      checksum: 'mock',
      encrypted: false,
      validation_result: 'verified',
      systemd_unit: 'lawim-backup.service',
      attempt: 1,
      notes: '',
      source: 'backup',
      artifact_count: 1,
      alert_count: 0,
      size_bytes: 1024
    }
  ],
  restores: [],
  last_backup: {
    identifier: 'job-1',
    backup_id: 'LAWIM-20260711-020000',
    kind: 'full',
    state: 'COMPLETED',
    destination: 'local',
    provider: 'local',
    trigger: 'scheduler',
    created_at: '2026-07-11T00:00:00+00:00',
    started_at: '2026-07-11T00:00:00+00:00',
    finished_at: '2026-07-11T00:05:00+00:00',
    duration_seconds: 300,
    checksum: 'mock',
    encrypted: false,
    validation_result: 'verified',
    systemd_unit: 'lawim-backup.service',
    attempt: 1,
    notes: '',
    source: 'backup',
    artifact_count: 1,
    alert_count: 0,
    size_bytes: 1024
  },
  last_failed_backup: null,
  next_backup: {
    identifier: 'schedule-1',
    name: 'Google Drive backup',
    calendar: 'TZ=Africa/Douala *-*-* 02:00:00',
    timezone: 'Africa/Douala',
    source: 'google-drive',
    enabled: true,
    status: 'TARGET',
    next_run_at: '2026-07-11T02:00:00+00:00',
    last_run_at: '2026-07-11T00:00:00+00:00',
    provider: 'systemd',
    description: '',
    details: {}
  },
  last_restore: null,
  metrics: {
    total_jobs: 1,
    successful_jobs: 1,
    failed_jobs: 0,
    mean_duration_seconds: 300,
    max_duration_seconds: 300,
    bytes_stored: 1024,
    storage_usage_percent: 50,
    last_success_at: '2026-07-11T00:05:00+00:00',
    last_failed_at: null,
    average_size_bytes: 1024,
    total_size_bytes: 1024,
    transferred_bytes: 1024,
    upload_time_seconds: 300,
    restore_time_seconds: 0,
    alert_count: 0,
    checksum_validations: 1,
    checksum_failures: 0,
    availability_percent: 100,
    rpo_seconds: 3600,
    rto_seconds: 0,
    last_backup_age_seconds: 3600,
    calculated_at: '2026-07-11T00:05:00+00:00'
  },
  systemd: {
    unit: 'lawim-backup.service',
    active_state: 'active',
    sub_state: 'running',
    result: 'success',
    exec_main_status: '0',
    exec_main_code: 'exited',
    exec_main_pid: '1234',
    last_launch_at: '2026-07-11T00:00:00+00:00',
    last_exit_at: '2026-07-11T00:05:00+00:00',
    next_execution_at: '2026-07-11T02:00:00+00:00',
    last_trigger_at: '2026-07-11T00:00:00+00:00'
  },
  version: {
    lawim: '0.0.0',
    git_commit: 'mock'
  },
  counts: {
    jobs: 1,
    alerts: 0,
    restores: 0,
    providers: 3,
    destinations: 3
  }
});

const resolveUrl = (path: string) => {
  if (path.startsWith('http://') || path.startsWith('https://')) return path;
  const apiBase = getApiBase();
  const apiRoot = apiBase.endsWith('/api') ? apiBase : `${apiBase}/api`;
  const normalizedPath = path.startsWith('/') ? path : `/${path}`;
  if (normalizedPath.startsWith('/api/')) {
    return apiBase.endsWith('/api') ? `${apiBase}${normalizedPath.slice(4)}` : `${apiBase}${normalizedPath}`;
  }
  return `${apiRoot}${normalizedPath}`;
};

const requestJson = async <T>(path: string, init: RequestInit = {}, fallback: T): Promise<ApiResponse<T>> => {
  if (useMocks) {
    await mockDelay();
    return { data: fallback, message: 'mock' };
  }

  try {
    const token = readStorageToken();
    const response = await fetch(resolveUrl(path), {
      ...init,
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...(init.headers || {})
      }
    });

    const text = await response.text();
    const payload = text ? JSON.parse(text) : null;
    if (!response.ok) {
      const errorPayload = payload as { error?: { message?: string; code?: string }; message?: string } | null;
      const message = errorPayload?.error?.message || errorPayload?.message || `Request failed with ${response.status}`;
      return { data: fallback, message };
    }
    return { data: normalizePayload<T>(payload, fallback), message: 'ok' };
  } catch (error) {
    return { data: fallback, message: error instanceof Error ? error.message : 'Unknown error' };
  }
};

const requestBlob = async (path: string, init: RequestInit = {}, fallbackFilename = 'download.bin'): Promise<{ blob: Blob; filename: string }> => {
  if (useMocks) {
    await mockDelay();
    return { blob: new Blob(['mock'], { type: 'application/octet-stream' }), filename: fallbackFilename };
  }

  const token = readStorageToken();
  const response = await fetch(resolveUrl(path), {
    ...init,
    headers: {
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(init.headers || {})
    }
  });

  if (!response.ok) {
    const text = await response.text().catch(() => '');
    throw new Error(text || `Request failed with ${response.status}`);
  }

  const blob = await response.blob();
  const disposition = response.headers.get('Content-Disposition') || '';
  const match = disposition.match(/filename="?([^"]+)"?/i);
  const filename = match?.[1] || fallbackFilename;
  return { blob, filename };
};

const mockProperties: PropertySummary[] = [
  { id: 'p1', title: 'Maison Bellevue', location: 'Lyon', price: 420000, type: 'House', status: 'Available' },
  { id: 'p2', title: 'Appartement Lumière', location: 'Paris', price: 610000, type: 'Apartment', status: 'Reserved' }
];

const mockProfile: UserProfile = {
  id: 'u1',
  name: 'Alicia Dubois',
  role: 'admin',
  email: 'alicia@lawim.example'
};

export const apiSdk = {
  async login(credentials: AuthCredentials): Promise<ApiResponse<AuthSession>> {
    if (useMocks) {
      await mockDelay();
      return { data: { user: mockProfile, token: 'mock-token', roles: ['admin'] }, message: 'mock' };
    }
    return requestJson<AuthSession>('/auth/login', { method: 'POST', body: JSON.stringify(credentials) }, {
      user: mockProfile,
      token: 'mock-token',
      roles: ['admin']
    });
  },

  async register(payload: RegisterPayload): Promise<ApiResponse<RegisterResponse>> {
    if (useMocks) {
      await mockDelay();
      return {
        data: {
          user: {
            id: 'u2',
            name: payload.full_name,
            full_name: payload.full_name,
            role: 'user',
            email: payload.email,
            username: payload.username,
            phone_e164: payload.phone_e164,
            preferred_language: payload.preferred_language
          },
          token: 'mock-token',
          roles: ['user']
        },
        message: 'mock'
      };
    }
    return requestJson<RegisterResponse>('/auth/register', { method: 'POST', body: JSON.stringify(payload) }, {
      user: mockProfile,
      token: 'mock-token',
      roles: ['user']
    });
  },

  async logout(): Promise<ApiResponse<{ success: boolean }>> {
    if (useMocks) {
      await mockDelay();
      return { data: { success: true }, message: 'mock' };
    }
    return requestJson<{ success: boolean }>('/auth/logout', { method: 'POST' }, { success: true });
  },

  async refreshToken(): Promise<ApiResponse<{ token: string }>> {
    if (useMocks) {
      await mockDelay();
      return { data: { token: 'mock-token' }, message: 'mock' };
    }
    return requestJson<{ token: string }>('/auth/refresh', { method: 'POST' }, { token: 'mock-token' });
  },

  async getSession(): Promise<ApiResponse<AuthSession | null>> {
    if (useMocks) {
      const token = readStorageToken();
      return { data: token ? { user: mockProfile, token, roles: ['admin'] } : null, message: 'mock' };
    }
    return requestJson<AuthSession | null>('/auth/session', { method: 'GET' }, null);
  },

  async getProfile(): Promise<ApiResponse<UserProfile>> {
    if (useMocks) {
      await mockDelay();
      return { data: mockProfile, message: 'mock' };
    }
    return requestJson<UserProfile>('/v2/users/me', { method: 'GET' }, mockProfile);
  },

  async getProjects(): Promise<ApiResponse<ProjectSummary[]>> {
    if (useMocks) {
      await mockDelay();
      return {
        data: [
          {
            id: 1,
            title: 'LAWIM Demo Project',
            status: 'active',
            project_type: 'purchase',
            objective: 'Acquire a property in Yaounde',
            location_city: 'Yaounde',
            budget_min: 25000000,
            budget_max: 50000000
          }
        ],
        message: 'mock'
      };
    }
    const response = await requestJson<unknown[]>('/v2/projects', { method: 'GET' }, []);
    return {
      ...response,
      data: Array.isArray(response.data) ? response.data.map((item) => mapProjectSummary(item)) : []
    };
  },

  async getUsers(): Promise<ApiResponse<UserProfile[]>> {
    if (useMocks) {
      await mockDelay();
      return { data: [mockProfile], message: 'mock' };
    }
    return requestJson<UserProfile[]>('/v2/users', { method: 'GET' }, [mockProfile]);
  },

  async getProperties(params?: { search?: string; page?: number; pageSize?: number }): Promise<ApiResponse<PropertySummary[]>> {
    if (useMocks) {
      await mockDelay();
      const search = params?.search?.toLowerCase() ?? '';
      const filtered = mockProperties.filter((property) => property.title.toLowerCase().includes(search) || property.location.toLowerCase().includes(search));
      return { data: filtered.slice(0, params?.pageSize ?? 10), message: 'mock' };
    }
    const query = new URLSearchParams();
    if (params?.search) query.set('q', params.search);
    if (params?.page) query.set('page', String(params.page));
    if (params?.pageSize) query.set('limit', String(params.pageSize));
    const path = params?.search ? `/v2/properties/search${query.toString() ? `?${query.toString()}` : ''}` : `/v2/properties${query.toString() ? `?${query.toString()}` : ''}`;
    const response = await requestJson<unknown[]>(path, { method: 'GET' }, []);
    return {
      ...response,
      data: Array.isArray(response.data) ? response.data.map((item) => mapPropertySummary(item)) : []
    };
  },

  async getProperty(id: string): Promise<ApiResponse<PropertyDetail | null>> {
    if (useMocks) {
      await mockDelay();
      const property = mockProperties.find((item) => item.id === id);
      return { data: property ? { ...property, description: 'Beautiful property with strong yield.', surface: '120 m²', bedrooms: 3, bathrooms: 2 } : null, message: 'mock' };
    }
    const response = await requestJson<unknown>(`/v2/properties/${id}`, { method: 'GET' }, null);
    return {
      ...response,
      data: response.data ? mapPropertyDetail(response.data) : null
    };
  },

  async getDashboardSummary(): Promise<ApiResponse<DashboardSummary>> {
    if (useMocks) {
      await mockDelay();
      return { data: { properties: 12, opportunities: 6, communications: 18, pendingTasks: 4 }, message: 'mock' };
    }
    return requestJson<DashboardSummary>('/v2/dashboard', { method: 'GET' }, { properties: 0, opportunities: 0, communications: 0, pendingTasks: 0 });
  },

  async getFavorites(): Promise<ApiResponse<FavoriteItem[]>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ id: 'f1', title: 'Maison Bellevue', type: 'Property', score: 94 }], message: 'mock' };
    }
    return requestJson<FavoriteItem[]>('/v2/favorites', { method: 'GET' }, []);
  },

  async getNotifications(): Promise<ApiResponse<NotificationItem[]>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ id: 'n1', title: 'Inspection confirmed', message: 'The inspection is scheduled for Thursday', read: false }], message: 'mock' };
    }
    return requestJson<NotificationItem[]>('/v2/notifications', { method: 'GET' }, []);
  },

  async getRequests(): Promise<ApiResponse<RequestItem[]>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ id: 'r1', title: 'Document review', status: 'Pending' }], message: 'mock' };
    }
    return requestJson<RequestItem[]>('/v2/requests', { method: 'GET' }, []);
  },

  async getDocuments(): Promise<ApiResponse<DocumentItem[]>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ id: 'd1', title: 'Listing memo', kind: 'PDF' }], message: 'mock' };
    }
    return requestJson<DocumentItem[]>('/v2/documents', { method: 'GET' }, []);
  },

  async getMarketListings(): Promise<ApiResponse<MarketListing[]>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ id: 'm1', title: 'Audit immobilier', category: 'Services', price: 1800, status: 'Open' }, { id: 'm2', title: 'Campagne de prospection', category: 'Marketing', price: 3200, status: 'In review' }], message: 'mock' };
    }
    return requestJson<MarketListing[]>('/v2/marketplace/providers', { method: 'GET' }, []);
  },

  async getWorkflowInstances(): Promise<ApiResponse<Array<{ id: string; title: string; status: string }>>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ id: 'w1', title: 'Lead nurture', status: 'Ready' }], message: 'mock' };
    }
    return requestJson<Array<{ id: string; title: string; status: string }>>('/v2/workflows/instances', { method: 'GET' }, []);
  },

  async getCommunicationItems(): Promise<ApiResponse<Array<{ id: string; title: string; channel: string }>>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ id: 'c1', title: 'Follow-up', channel: 'Email' }], message: 'mock' };
    }
    return requestJson<Array<{ id: string; title: string; channel: string }>>('/v2/communication/messages', { method: 'GET' }, []);
  },

  async getAnalytics(): Promise<ApiResponse<Array<{ label: string; value: number }>>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ label: 'Conversion', value: 82 }, { label: 'Engagement', value: 71 }], message: 'mock' };
    }
    return requestJson<Array<{ label: string; value: number }>>('/v2/analytics/dashboard', { method: 'GET' }, []);
  },

  async getSecuritySummary(): Promise<ApiResponse<Array<{ label: string; value: string }>>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ label: 'Audit', value: 'Complete' }, { label: 'Risk', value: 'Low' }], message: 'mock' };
    }
    return requestJson<Array<{ label: string; value: string }>>('/v2/security/stats', { method: 'GET' }, []);
  },

  async getOperations(): Promise<ApiResponse<Array<{ id: string; title: string; status: string }>>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ id: 'o1', title: 'Deployment health', status: 'Healthy' }], message: 'mock' };
    }
    return requestJson<Array<{ id: string; title: string; status: string }>>('/v2/operations', { method: 'GET' }, []);
  },

  async getDeploymentStatus(): Promise<ApiResponse<Array<{ label: string; value: string }>>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ label: 'Environment', value: 'Production' }, { label: 'Status', value: 'Online' }], message: 'mock' };
    }
    return requestJson<Array<{ label: string; value: string }>>('/v2/deployment/status', { method: 'GET' }, []);
  },

  async getBackupSnapshot(): Promise<ApiResponse<BackupStatusSnapshot>> {
    if (useMocks) {
      await mockDelay();
      return { data: buildMockBackupSnapshot(), message: 'mock' };
    }
    return requestJson<BackupStatusSnapshot>('/v2/backup/status', { method: 'GET' }, buildMockBackupSnapshot());
  },

  async getBackupStatus(): Promise<ApiResponse<BackupStatusCard[]>> {
    const response = useMocks
      ? { data: buildMockBackupSnapshot(), message: 'mock' }
      : await requestJson<BackupStatusSnapshot>('/v2/backup/status', { method: 'GET' }, buildMockBackupSnapshot());
    return {
      ...response,
      data: mapBackupCards(response.data)
    };
  },

  async getBackupHistory(limit = 50): Promise<ApiResponse<BackupSnapshotRecord[]>> {
    if (useMocks) {
      await mockDelay();
      return { data: buildMockBackupSnapshot().history, message: 'mock' };
    }
    return requestJson<BackupSnapshotRecord[]>(`/v2/backup/history?limit=${limit}`, { method: 'GET' }, buildMockBackupSnapshot().history);
  },

  async getBackupJobs(limit = 50): Promise<ApiResponse<BackupSnapshotRecord[]>> {
    if (useMocks) {
      await mockDelay();
      return { data: buildMockBackupSnapshot().jobs, message: 'mock' };
    }
    return requestJson<BackupSnapshotRecord[]>(`/v2/backup/jobs?limit=${limit}`, { method: 'GET' }, buildMockBackupSnapshot().jobs);
  },

  async getBackupProviders(): Promise<ApiResponse<BackupSnapshotRecord[]>> {
    if (useMocks) {
      await mockDelay();
      return { data: buildMockBackupSnapshot().providers, message: 'mock' };
    }
    return requestJson<BackupSnapshotRecord[]>('/v2/backup/providers', { method: 'GET' }, buildMockBackupSnapshot().providers);
  },

  async getBackupAlerts(limit = 50): Promise<ApiResponse<BackupSnapshotRecord[]>> {
    if (useMocks) {
      await mockDelay();
      return { data: buildMockBackupSnapshot().alerts, message: 'mock' };
    }
    return requestJson<BackupSnapshotRecord[]>(`/v2/backup/alerts?limit=${limit}`, { method: 'GET' }, buildMockBackupSnapshot().alerts);
  },

  async getBackupMetrics(): Promise<ApiResponse<BackupMetricsSnapshot>> {
    if (useMocks) {
      await mockDelay();
      return { data: buildMockBackupSnapshot().metrics, message: 'mock' };
    }
    return requestJson<BackupMetricsSnapshot>('/v2/backup/metrics', { method: 'GET' }, buildMockBackupSnapshot().metrics);
  },

  async runBackup(payload: {
    kind?: string;
    destination?: string;
    provider_name?: string;
    trigger?: string;
    metadata?: Record<string, unknown>;
    backup_id?: string;
    attempt?: number;
  } = {}): Promise<ApiResponse<BackupSnapshotRecord>> {
    if (useMocks) {
      await mockDelay();
      return { data: buildMockBackupSnapshot().last_backup as BackupSnapshotRecord, message: 'mock' };
    }
    return requestJson<BackupSnapshotRecord>('/v2/backup/run', { method: 'POST', body: JSON.stringify(payload) }, buildMockBackupSnapshot().last_backup as BackupSnapshotRecord);
  },

  async testBackup(payload: {
    kind?: string;
    destination?: string;
    metadata?: Record<string, unknown>;
  } = {}): Promise<ApiResponse<BackupSnapshotRecord>> {
    if (useMocks) {
      await mockDelay();
      return { data: buildMockBackupSnapshot().last_backup as BackupSnapshotRecord, message: 'mock' };
    }
    return requestJson<BackupSnapshotRecord>('/v2/backup/test', { method: 'POST', body: JSON.stringify(payload) }, buildMockBackupSnapshot().last_backup as BackupSnapshotRecord);
  },

  async retryBackup(identifier?: string): Promise<ApiResponse<BackupSnapshotRecord>> {
    if (useMocks) {
      await mockDelay();
      return { data: buildMockBackupSnapshot().last_backup as BackupSnapshotRecord, message: 'mock' };
    }
    return requestJson<BackupSnapshotRecord>('/v2/backup/retry', { method: 'POST', body: JSON.stringify({ identifier }) }, buildMockBackupSnapshot().last_backup as BackupSnapshotRecord);
  },

  async restoreBackup(payload: {
    backup_id: string;
    kind: string;
    target_environment?: string;
    database_restored?: boolean;
    media_restored?: boolean;
    notes?: string;
    success?: boolean;
  }): Promise<ApiResponse<Record<string, unknown>>> {
    if (useMocks) {
      await mockDelay();
      return {
        data: {
          restore_job: buildMockBackupSnapshot().last_restore,
          restore_result: {
            identifier: 'restore-result-1',
            restore_job_id: 'restore-job-1',
            backup_id: payload.backup_id,
            kind: payload.kind,
            state: 'COMPLETED',
            success: true,
            created_at: '2026-07-11T00:10:00+00:00',
            completed_at: '2026-07-11T00:12:00+00:00',
            duration_seconds: 120,
            checksum_verified: true,
            media_restored: payload.media_restored ?? false,
            database_restored: payload.database_restored ?? false,
            report: {},
            notes: payload.notes ?? ''
          }
        },
        message: 'mock'
      };
    }
    return requestJson<Record<string, unknown>>('/v2/backup/restore', { method: 'POST', body: JSON.stringify(payload) }, {});
  },

  async testBackupProvider(payload: { provider_identifier?: string; provider?: string; identifier?: string }): Promise<ApiResponse<Record<string, unknown>>> {
    if (useMocks) {
      await mockDelay();
      return { data: buildMockBackupSnapshot().providers[0], message: 'mock' };
    }
    return requestJson<Record<string, unknown>>('/v2/backup/provider/test', { method: 'POST', body: JSON.stringify(payload) }, {});
  },

  async patchBackupConfig(payload: Record<string, unknown>): Promise<ApiResponse<Record<string, unknown>>> {
    if (useMocks) {
      await mockDelay();
      const snapshot = buildMockBackupSnapshot();
      return { data: { ...snapshot.configuration, ...payload }, message: 'mock' };
    }
    return requestJson<Record<string, unknown>>('/v2/backup/config', { method: 'PATCH', body: JSON.stringify(payload) }, {});
  },

  async getDisasterRecoveryStatus(): Promise<ApiResponse<DisasterRecoveryStatusSnapshot>> {
    if (useMocks) {
      await mockDelay();
      const snapshot = buildMockBackupSnapshot();
      return {
        data: {
          bundle_root: '/var/lib/lawim-backup/recovery-bundles',
          latest_bundle: {
            bundle_id: 'LAWIM-DRF-MOCK',
            created_at: '2026-07-11T00:00:00+00:00',
            size_bytes: 1024,
            checksum: 'mock-checksum',
            file_count: 10,
            environment: 'test',
            validation_state: 'generated',
            path: '/var/lib/lawim-backup/recovery-bundles/LAWIM-DRF-MOCK'
          },
          validation: {
            bundle_id: 'LAWIM-DRF-MOCK',
            manifest_present: true,
            checksum_valid: true,
            compatible: true,
            git_ok: true,
            docker_ok: true,
            postgresql_ok: true,
            restore_ready: true,
            missing_files: [],
            warnings: [],
            checks: [
              { name: 'manifest-present', passed: true, status: 'pass', detail: 'Manifest available' },
              { name: 'restore-ready', passed: true, status: 'pass', detail: 'Ready' }
            ],
            duration_seconds: 0.25,
            validated_at: '2026-07-11T00:00:00+00:00'
          },
          readiness: {
            score: 92,
            maximum_score: 100,
            state: 'READY',
            bundle_id: 'LAWIM-DRF-MOCK',
            bundle_age_days: 2,
            rpo_seconds: 300,
            rto_seconds: 900,
            signals: [
              { name: 'latest-bundle-present', passed: true, weight: 0, detail: 'Latest bundle LAWIM-DRF-MOCK is available' },
              { name: 'bundle-freshness', passed: true, weight: 0, detail: 'Latest bundle age is 2.0 days' },
              { name: 'validation-available', passed: true, weight: 0, detail: 'Recovery validation snapshot is available' }
            ],
            reasons: [],
            calculated_at: '2026-07-11T00:00:00+00:00'
          },
          git: snapshot.version,
          versions: snapshot.version,
          backup: { last_backup: snapshot.last_backup, last_restore: snapshot.last_restore },
          checklist: '# Recovery Checklist\n'
        },
        message: 'mock'
      };
    }
    return requestJson<DisasterRecoveryStatusSnapshot>('/v2/backup/recovery', { method: 'GET' }, {
      bundle_root: '',
      latest_bundle: null,
      validation: null,
      readiness: null,
      git: {},
      versions: {},
      backup: {},
      checklist: null
    });
  },

  async getDisasterRecoveryBundles(limit = 20): Promise<ApiResponse<DisasterRecoveryBundleRecord[]>> {
    if (useMocks) {
      await mockDelay();
      return {
        data: [
          {
            bundle_id: 'LAWIM-DRF-MOCK',
            created_at: '2026-07-11T00:00:00+00:00',
            size_bytes: 1024,
            checksum: 'mock-checksum',
            file_count: 10,
            environment: 'test',
            validation_state: 'generated',
            path: '/var/lib/lawim-backup/recovery-bundles/LAWIM-DRF-MOCK'
          }
        ],
        message: 'mock'
      };
    }
    return requestJson<DisasterRecoveryBundleRecord[]>(`/v2/backup/recovery/bundles?limit=${limit}`, { method: 'GET' }, []);
  },

  async validateDisasterRecoveryBundle(bundleId?: string): Promise<ApiResponse<DisasterRecoveryValidationSnapshot>> {
    if (useMocks) {
      await mockDelay();
      return {
        data: {
          bundle_id: bundleId || 'LAWIM-DRF-MOCK',
          manifest_present: true,
          checksum_valid: true,
          compatible: true,
          git_ok: true,
          docker_ok: true,
          postgresql_ok: true,
          restore_ready: true,
          missing_files: [],
          warnings: [],
          checks: [
            { name: 'manifest-present', passed: true, status: 'pass', detail: 'Manifest available' },
            { name: 'restore-ready', passed: true, status: 'pass', detail: 'Ready' }
          ],
          duration_seconds: 0.25,
          validated_at: '2026-07-11T00:00:00+00:00'
        },
        message: 'mock'
      };
    }
    return requestJson<DisasterRecoveryValidationSnapshot>('/v2/backup/recovery/validate', {
      method: 'POST',
      body: JSON.stringify({ bundle_id: bundleId })
    }, {
      bundle_id: bundleId || '',
      manifest_present: false,
      checksum_valid: false,
      compatible: false,
      git_ok: false,
      docker_ok: false,
      postgresql_ok: false,
      restore_ready: false,
      missing_files: [],
      warnings: [],
      checks: [],
      duration_seconds: 0,
      validated_at: ''
    });
  },

  async downloadDisasterRecoveryBundle(bundleId: string): Promise<{ blob: Blob; filename: string }> {
    return requestBlob(`/v2/backup/recovery/bundles/${encodeURIComponent(bundleId)}/download`, { method: 'GET' }, `${bundleId}.zip`);
  },

  async getReleases(): Promise<ApiResponse<Array<{ id: string; title: string; status: string }>>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ id: 'r1', title: 'Release Program O', status: 'Planned' }], message: 'mock' };
    }
    return requestJson<Array<{ id: string; title: string; status: string }>>('/v2/releases', { method: 'GET' }, []);
  },

  async getSourceIntelligence(): Promise<ApiResponse<Array<{ id: string; title: string; score: number }>>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ id: 's1', title: 'Reference code ingestion', score: 91 }], message: 'mock' };
    }
    return requestJson<Array<{ id: string; title: string; score: number }>>('/v2/source-intelligence/dashboard', { method: 'GET' }, []);
  },

  async getAssistantSuggestions(): Promise<ApiResponse<Array<{ title: string; description: string }>>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ title: 'Summarize pipeline', description: 'Review last updates' }], message: 'mock' };
    }
    const response = await requestJson<unknown[]>('/v2/assistant/agents', { method: 'GET' }, []);
    return {
      ...response,
      data: Array.isArray(response.data)
        ? response.data.map((item) => {
            const record = toRecord(item);
            return {
              title: toText(record.title ?? record.agent_key ?? 'Assistant'),
              description: toText(record.description ?? record.prompt_key ?? '')
            };
          })
        : []
    };
  },

  async askAssistant(payload: AssistantMessagePayload): Promise<ApiResponse<AssistantReply>> {
    if (useMocks) {
      await mockDelay();
      return { data: { reply: `I can help with: ${payload.message}`, suggestions: ['Review pipeline', 'Send follow-up'] }, message: 'mock' };
    }
    const projectId = Number(payload.project_id ?? 1);
    const response = await requestJson<{ chat?: Record<string, unknown> }>(
      '/v2/assistant/chat',
      {
        method: 'POST',
        body: JSON.stringify({
          message: payload.message,
          project_id: projectId,
          session_id: payload.session_id,
          agent_key: payload.agent_key
        })
      },
      { chat: {} }
    );
    const chat = toRecord(response.data.chat);
    const assistantMessage = toRecord(chat.assistant_message);
    const userMessage = toRecord(chat.user_message);
    const ragChunks = Array.isArray(chat.rag_chunks) ? chat.rag_chunks : [];
    const suggestions = [
      toText(ragChunks[0] ? toRecord(ragChunks[0]).content : ''),
      toText(ragChunks[1] ? toRecord(ragChunks[1]).content : ''),
      'Ouvrir le cockpit',
      'Relancer une question'
    ].filter((item, index, values) => Boolean(item) && values.indexOf(item) === index).slice(0, 4);
    return {
      ...response,
      data: {
        reply: toText(assistantMessage.content, 'Connected to assistant service'),
        suggestions,
        session_id: Number(chat.session_id ?? toRecord(chat.session).id ?? 0) || undefined,
        agent_key: toText(chat.agent_key ?? ''),
        mode: toText(chat.mode ?? ''),
        provider: toText(chat.provider ?? ''),
        context_snapshot_key: toText(chat.context_snapshot_key ?? ''),
        project_id: projectId,
        raw: {
          chat,
          user_message: userMessage,
          assistant_message: assistantMessage
        }
      }
    };
  },

  async createProperty(payload: CreatePropertyPayload): Promise<ApiResponse<PropertySummary>> {
    if (useMocks) {
      await mockDelay();
      return {
        data: {
          id: `local-${Date.now()}`,
          title: payload.title,
          location: joinLocation(payload.city, payload.region),
          price: toNumber(payload.price_max ?? payload.price_min ?? 0),
          type: toText(payload.property_type ?? 'Property'),
          status: toText(payload.status ?? 'draft')
        },
        message: 'mock'
      };
    }
    const response = await requestJson<unknown>('/properties', { method: 'POST', body: JSON.stringify(payload) }, {});
    return {
      ...response,
      data: mapPropertySummary(response.data)
    };
  },

  /* ── Maintenance mode methods ────────────────────────────── */

  async getServiceMaintenanceStatus(): Promise<ApiResponse<MaintenanceStatus>> {
    return requestJson<MaintenanceStatus>('/v2/maintenance/status', { method: 'GET' }, {
      maintenance_mode: true,
      message: '',
      flags: {},
      services: {},
    });
  },

  async submitMaintenanceMessage(payload: MaintenanceMessagePayload): Promise<ApiResponse<MaintenanceMessageResult>> {
    if (useMocks) {
      await mockDelay();
      return {
        data: {
          message: { id: Date.now(), channel: payload.channel, raw_message: payload.message },
          response: 'Message enregistré en mode maintenance.',
          automated_processing: 'blocked',
          handover_requested: Boolean(payload.handover_requested),
        },
        message: 'mock',
      };
    }
    return requestJson<MaintenanceMessageResult>(
      '/v2/maintenance/messages',
      { method: 'POST', body: JSON.stringify(payload) },
      { message: {}, response: '', automated_processing: 'blocked', handover_requested: false }
    );
  },

  async requestHumanHandover(payload: MaintenanceMessagePayload): Promise<ApiResponse<MaintenanceMessageResult>> {
    return this.submitMaintenanceMessage({ ...payload, handover_requested: true });
  },

  async createEstimation(payload: EstimationPayload): Promise<ApiResponse<EstimationResult>> {
    if (useMocks) {
      await mockDelay();
      return { data: { estimate: '€500k - €560k', confidence: 'High' }, message: 'mock' };
    }
    return requestJson<EstimationResult>('/v2/estimation', { method: 'POST', body: JSON.stringify(payload) }, { estimate: 'Pending', confidence: 'Low' });
  },

  async listFinancialProducts(params?: { status?: string; limit?: number }): Promise<ApiResponse<FinancialProduct[]>> {
    if (useMocks) {
      await mockDelay();
      return {
        data: [
          {
            id: 1,
            code: 'FIN-SVC-001',
            name: 'Service financier',
            description: 'Offre financière LAWIM',
            category: 'service',
            status: 'active',
            unit: 'item',
            default_price_minor: 2500,
            currency: 'XAF',
            tax_rate_bps: 0
          }
        ],
        message: 'mock'
      };
    }
    const query = buildQuery({ status: params?.status, limit: params?.limit });
    const response = await requestJson<{ products?: FinancialProduct[]; financial_products?: FinancialProduct[] }>(`/v2/financial/catalog/products${query ? `?${query}` : ''}`, { method: 'GET' }, {});
    const record = toRecord(response.data);
    return { ...response, data: (record.products ?? record.financial_products ?? []) as FinancialProduct[] };
  },

  async calculatePrice(payload: { line_items: FinancialLine[]; discount_minor?: number; fee_minor?: number; tax_rate_bps?: number; currency?: string; context?: Record<string, unknown> }): Promise<ApiResponse<PricingBreakdown>> {
    if (useMocks) {
      await mockDelay();
      const subtotal = (payload.line_items ?? []).reduce((sum, line) => sum + Math.round(Number(line.unit_price_minor) * Number(line.quantity || 1)), 0);
      return {
        data: {
          subtotal_minor: subtotal,
          discount_minor: payload.discount_minor ?? 0,
          fee_minor: payload.fee_minor ?? 0,
          tax_minor: Math.round(subtotal * ((payload.tax_rate_bps ?? 0) / 10_000)),
          total_minor: subtotal - (payload.discount_minor ?? 0) + (payload.fee_minor ?? 0) + Math.round(subtotal * ((payload.tax_rate_bps ?? 0) / 10_000)),
          currency: payload.currency ?? 'XAF',
          lines: payload.line_items ?? []
        },
        message: 'mock'
      };
    }
    return requestJson<PricingBreakdown>('/v2/financial/pricing/calculate', { method: 'POST', body: JSON.stringify(payload) }, {
      subtotal_minor: 0,
      discount_minor: 0,
      fee_minor: 0,
      tax_minor: 0,
      total_minor: 0,
      currency: payload.currency ?? 'XAF',
      lines: []
    });
  },

  async createQuote(payload: Record<string, unknown>): Promise<ApiResponse<Quote>> {
    if (useMocks) {
      await mockDelay();
      return {
        data: {
          id: 1,
          number: 'DEV-2026-000001',
          status: 'DRAFT',
          currency: String(payload.currency ?? 'XAF'),
          total_minor: Number(payload.total_minor ?? 2500),
          lines: Array.isArray(payload.lines) ? (payload.lines as FinancialLine[]) : []
        },
        message: 'mock'
      };
    }
    return requestJson<Quote>('/v2/financial/quotes', { method: 'POST', body: JSON.stringify(payload) }, {
      id: 0,
      number: '',
      status: 'DRAFT',
      currency: 'XAF',
      total_minor: 0,
      lines: []
    });
  },

  async getQuote(id: number | string): Promise<ApiResponse<Quote>> {
    if (useMocks) {
      await mockDelay();
      return {
        data: {
          id: Number(id),
          number: `DEV-2026-${String(id).padStart(6, '0')}`,
          status: 'ISSUED',
          currency: 'XAF',
          total_minor: 2500,
          lines: [{ description: 'Service financier', quantity: 1, unit_price_minor: 2500 }]
        },
        message: 'mock'
      };
    }
    return requestJson<Quote>(`/v2/financial/quotes/${encodeURIComponent(String(id))}`, { method: 'GET' }, {
      id: Number(id),
      number: '',
      status: 'DRAFT',
      currency: 'XAF',
      total_minor: 0,
      lines: []
    });
  },

  async acceptQuote(id: number | string): Promise<ApiResponse<Quote>> {
    if (useMocks) {
      await mockDelay();
      return { data: { id: Number(id), number: `DEV-2026-${String(id).padStart(6, '0')}`, status: 'ACCEPTED', currency: 'XAF', total_minor: 2500, lines: [] }, message: 'mock' };
    }
    return requestJson<Quote>(`/v2/financial/quotes/${encodeURIComponent(String(id))}/accept`, { method: 'POST' }, {
      id: Number(id),
      number: '',
      status: 'ACCEPTED',
      currency: 'XAF',
      total_minor: 0,
      lines: []
    });
  },

  async listInvoices(params?: { status?: string; customer_user_id?: number; organization_id?: number; limit?: number }): Promise<ApiResponse<Invoice[]>> {
    if (useMocks) {
      await mockDelay();
      return {
        data: [
          {
            id: 1,
            number: 'FAC-2026-000001',
            status: 'ISSUED',
            currency: 'XAF',
            total_minor: 2500,
            balance_minor: 2500,
            amount_paid_minor: 0,
            lines: [{ description: 'Service financier', quantity: 1, unit_price_minor: 2500 }]
          }
        ],
        message: 'mock'
      };
    }
    const query = buildQuery(params ?? {});
    const response = await requestJson<{ invoices?: Invoice[] }>(`/v2/financial/invoices${query ? `?${query}` : ''}`, { method: 'GET' }, {});
    const record = toRecord(response.data);
    return { ...response, data: (record.invoices ?? []) as Invoice[] };
  },

  async getInvoice(id: number | string): Promise<ApiResponse<Invoice>> {
    if (useMocks) {
      await mockDelay();
      return {
        data: {
          id: Number(id),
          number: `FAC-2026-${String(id).padStart(6, '0')}`,
          status: 'ISSUED',
          currency: 'XAF',
          total_minor: 2500,
          balance_minor: 2500,
          amount_paid_minor: 0,
          lines: [{ description: 'Service financier', quantity: 1, unit_price_minor: 2500 }]
        },
        message: 'mock'
      };
    }
    return requestJson<Invoice>(`/v2/financial/invoices/${encodeURIComponent(String(id))}`, { method: 'GET' }, {
      id: Number(id),
      number: '',
      status: 'DRAFT',
      currency: 'XAF',
      total_minor: 0,
      balance_minor: 0,
      amount_paid_minor: 0,
      lines: []
    });
  },

  async createPaymentIntent(payload: Record<string, unknown>): Promise<ApiResponse<PaymentIntent>> {
    if (useMocks) {
      await mockDelay();
      return {
        data: {
          id: 1,
          number: 'PAY-2026-000001',
          status: 'PENDING',
          amount_minor: Number(payload.amount_minor ?? 2500),
          currency: String(payload.currency ?? 'XAF'),
          provider_code: String(payload.provider_code ?? 'CAMPAY'),
          phone_number_e164: String(payload.phone_number_e164 ?? '+237677000111'),
          idempotency_key: String(payload.idempotency_key ?? 'financial-intent-mock')
        },
        message: 'mock'
      };
    }
    return requestJson<PaymentIntent>('/v2/financial/payments/intents', { method: 'POST', body: JSON.stringify(payload) }, {
      id: 0,
      number: '',
      status: 'CREATED',
      amount_minor: 0,
      currency: 'XAF',
      provider_code: 'CAMPAY'
    });
  },

  async getPaymentIntent(id: number | string): Promise<ApiResponse<PaymentIntent>> {
    if (useMocks) {
      await mockDelay();
      return { data: { id: Number(id), number: `PAY-2026-${String(id).padStart(6, '0')}`, status: 'PENDING', amount_minor: 2500, currency: 'XAF', provider_code: 'CAMPAY' }, message: 'mock' };
    }
    return requestJson<PaymentIntent>(`/v2/financial/payments/intents/${encodeURIComponent(String(id))}`, { method: 'GET' }, {
      id: Number(id),
      number: '',
      status: 'CREATED',
      amount_minor: 0,
      currency: 'XAF',
      provider_code: 'CAMPAY'
    });
  },

  async retryPayment(id: number | string, payload: Record<string, unknown> = {}): Promise<ApiResponse<PaymentAttempt>> {
    if (useMocks) {
      await mockDelay();
      return { data: { id: Number(id), status: 'PENDING', provider_code: 'CAMPAY', provider_reference: 'campay-mock', idempotency_key: String(payload.idempotency_key ?? 'retry-mock') }, message: 'mock' };
    }
    return requestJson<PaymentAttempt>(`/v2/financial/payments/intents/${encodeURIComponent(String(id))}/attempts`, { method: 'POST', body: JSON.stringify(payload) }, {
      id: Number(id),
      status: 'PENDING',
      provider_code: 'CAMPAY'
    });
  },

  async getPaymentStatus(id: number | string): Promise<ApiResponse<Record<string, unknown>>> {
    if (useMocks) {
      await mockDelay();
      return { data: { payment_intent: { id: Number(id), status: 'SUCCEEDED' }, provider_status: { status: 'SUCCESSFUL' } }, message: 'mock' };
    }
    return requestJson<Record<string, unknown>>(`/v2/financial/payments/intents/${encodeURIComponent(String(id))}/status`, { method: 'GET' }, {});
  },

  async listPaymentIntents(params?: { status?: string; invoice_id?: number; customer_user_id?: number; provider_code?: string; limit?: number }): Promise<ApiResponse<PaymentIntent[]>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ id: 1, number: 'PAY-2026-000001', status: 'PENDING', amount_minor: 2500, currency: 'XAF', provider_code: 'CAMPAY' }], message: 'mock' };
    }
    const query = buildQuery(params ?? {});
    const response = await requestJson<{ payment_intents?: PaymentIntent[] }>(`/v2/financial/payments/intents${query ? `?${query}` : ''}`, { method: 'GET' }, {});
    const record = toRecord(response.data);
    return { ...response, data: (record.payment_intents ?? []) as PaymentIntent[] };
  },

  async listPaymentTransactions(params?: { payment_intent_id?: number; payment_attempt_id?: number; invoice_id?: number; status?: string; limit?: number }): Promise<ApiResponse<PaymentTransaction[]>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ id: 1, status: 'SUCCESSFUL', type: 'collection', direction: 'inflow', amount_minor: 2500, currency: 'XAF' }], message: 'mock' };
    }
    const query = buildQuery(params ?? {});
    const response = await requestJson<{ payment_transactions?: PaymentTransaction[] }>(`/v2/financial/payments/transactions${query ? `?${query}` : ''}`, { method: 'GET' }, {});
    const record = toRecord(response.data);
    return { ...response, data: (record.payment_transactions ?? []) as PaymentTransaction[] };
  },

  async listReceipts(params?: { invoice_id?: number; status?: string; limit?: number }): Promise<ApiResponse<Receipt[]>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ id: 1, number: 'REC-2026-000001', status: 'GENERATED', currency: 'XAF', amount_minor: 2500, invoice_id: 1, payment_intent_id: 1 }], message: 'mock' };
    }
    const query = buildQuery(params ?? {});
    const response = await requestJson<{ receipts?: Receipt[] }>(`/v2/financial/receipts${query ? `?${query}` : ''}`, { method: 'GET' }, {});
    const record = toRecord(response.data);
    return { ...response, data: (record.receipts ?? []) as Receipt[] };
  },

  async getReceipt(id: number | string): Promise<ApiResponse<Receipt>> {
    if (useMocks) {
      await mockDelay();
      return { data: { id: Number(id), number: `REC-2026-${String(id).padStart(6, '0')}`, status: 'GENERATED', currency: 'XAF', amount_minor: 2500 }, message: 'mock' };
    }
    return requestJson<Receipt>(`/v2/financial/receipts/${encodeURIComponent(String(id))}`, { method: 'GET' }, {
      id: Number(id),
      number: '',
      status: 'DRAFT',
      currency: 'XAF',
      amount_minor: 0
    });
  },

  async listSubscriptions(params?: { status?: string; customer_user_id?: number; organization_id?: number; plan_id?: number; limit?: number }): Promise<ApiResponse<Subscription[]>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ id: 1, status: 'ACTIVE', customer_user_id: 1, plan_id: 1, renewal_mode: 'automatic' }], message: 'mock' };
    }
    const query = buildQuery(params ?? {});
    const response = await requestJson<{ subscriptions?: Subscription[] }>(`/v2/financial/subscriptions${query ? `?${query}` : ''}`, { method: 'GET' }, {});
    const record = toRecord(response.data);
    return { ...response, data: (record.subscriptions ?? []) as Subscription[] };
  },

  async subscribeToPlan(payload: Record<string, unknown>): Promise<ApiResponse<Subscription>> {
    if (useMocks) {
      await mockDelay();
      return { data: { id: 1, status: 'ACTIVE', customer_user_id: Number(payload.customer_user_id ?? 1), plan_id: Number(payload.plan_id ?? 1), renewal_mode: String(payload.renewal_mode ?? 'automatic') }, message: 'mock' };
    }
    return requestJson<Subscription>('/v2/financial/subscriptions', { method: 'POST', body: JSON.stringify(payload) }, { id: 0, status: 'PENDING' });
  },

  async renewSubscription(id: number | string, payload: Record<string, unknown> = {}): Promise<ApiResponse<Subscription>> {
    if (useMocks) {
      await mockDelay();
      return { data: { id: Number(id), status: 'ACTIVE', plan_id: Number(payload.plan_id ?? 1), renewal_mode: String(payload.renewal_mode ?? 'automatic') }, message: 'mock' };
    }
    return requestJson<Subscription>(`/v2/financial/subscriptions/${encodeURIComponent(String(id))}/renew`, { method: 'POST', body: JSON.stringify(payload) }, { id: Number(id), status: 'ACTIVE' });
  },

  async changeSubscriptionPlan(id: number | string, payload: Record<string, unknown>): Promise<ApiResponse<Subscription>> {
    if (useMocks) {
      await mockDelay();
      return { data: { id: Number(id), status: 'ACTIVE', plan_id: Number(payload.plan_id ?? 1), renewal_mode: String(payload.renewal_mode ?? 'automatic') }, message: 'mock' };
    }
    return requestJson<Subscription>(`/v2/financial/subscriptions/${encodeURIComponent(String(id))}/change-plan`, { method: 'POST', body: JSON.stringify(payload) }, { id: Number(id), status: 'ACTIVE' });
  },

  async cancelSubscription(id: number | string, payload: Record<string, unknown> = {}): Promise<ApiResponse<Subscription>> {
    if (useMocks) {
      await mockDelay();
      return { data: { id: Number(id), status: 'CANCELLED', renewal_mode: String(payload.renewal_mode ?? 'manual') }, message: 'mock' };
    }
    return requestJson<Subscription>(`/v2/financial/subscriptions/${encodeURIComponent(String(id))}/cancel`, { method: 'POST', body: JSON.stringify(payload) }, { id: Number(id), status: 'CANCELLED' });
  },

  async listOwnCommissions(params?: { status?: string; limit?: number }): Promise<ApiResponse<Commission[]>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ id: 1, status: 'PAYABLE', amount_minor: 300, currency: 'XAF', beneficiary_user_id: 1 }], message: 'mock' };
    }
    const query = buildQuery(params ?? {});
    const response = await requestJson<{ commissions?: Commission[] }>(`/v2/financial/commissions${query ? `?${query}` : ''}`, { method: 'GET' }, {});
    const record = toRecord(response.data);
    return { ...response, data: (record.commissions ?? []) as Commission[] };
  },

  async listOwnPayouts(params?: { status?: string; limit?: number }): Promise<ApiResponse<Payout[]>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ id: 1, status: 'APPROVED', amount_minor: 300, currency: 'XAF', beneficiary_user_id: 1 }], message: 'mock' };
    }
    const query = buildQuery(params ?? {});
    const response = await requestJson<{ payouts?: Payout[] }>(`/v2/financial/payouts${query ? `?${query}` : ''}`, { method: 'GET' }, {});
    const record = toRecord(response.data);
    return { ...response, data: (record.payouts ?? []) as Payout[] };
  },

  async requestRefund(payload: Record<string, unknown>): Promise<ApiResponse<Refund>> {
    if (useMocks) {
      await mockDelay();
      return { data: { id: 1, number: 'AVR-2026-000001', status: 'REQUESTED', amount_minor: Number(payload.amount_minor ?? 0), currency: String(payload.currency ?? 'XAF'), payment_transaction_id: Number(payload.payment_transaction_id ?? 1) }, message: 'mock' };
    }
    return requestJson<Refund>('/v2/financial/refunds', { method: 'POST', body: JSON.stringify(payload) }, { id: 0, number: '', status: 'REQUESTED', amount_minor: 0, currency: 'XAF' });
  },

  async getRefund(id: number | string): Promise<ApiResponse<Refund>> {
    if (useMocks) {
      await mockDelay();
      return { data: { id: Number(id), number: `AVR-2026-${String(id).padStart(6, '0')}`, status: 'APPROVED', amount_minor: 300, currency: 'XAF' }, message: 'mock' };
    }
    return requestJson<Refund>(`/v2/financial/refunds/${encodeURIComponent(String(id))}`, { method: 'GET' }, { id: Number(id), number: '', status: 'REQUESTED', amount_minor: 0, currency: 'XAF' });
  },

  async adminListPayments(params?: { status?: string; invoice_id?: number; customer_user_id?: number; provider_code?: string; limit?: number }): Promise<ApiResponse<PaymentIntent[]>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ id: 1, number: 'PAY-2026-000001', status: 'PENDING', amount_minor: 2500, currency: 'XAF', provider_code: 'CAMPAY' }], message: 'mock' };
    }
    const query = buildQuery(params ?? {});
    const response = await requestJson<{ payment_intents?: PaymentIntent[] }>(`/v2/financial/payments/intents${query ? `?${query}` : ''}`, { method: 'GET' }, {});
    const record = toRecord(response.data);
    return { ...response, data: (record.payment_intents ?? []) as PaymentIntent[] };
  },

  async adminVerifyPayment(id: number | string): Promise<ApiResponse<Record<string, unknown>>> {
    if (useMocks) {
      await mockDelay();
      return { data: { payment_intent: { id: Number(id), status: 'SUCCEEDED' }, provider_status: { status: 'SUCCESSFUL' } }, message: 'mock' };
    }
    return requestJson<Record<string, unknown>>(`/v2/financial/payments/intents/${encodeURIComponent(String(id))}/status`, { method: 'GET' }, {});
  },

  async adminListReconciliationConflicts(params?: { provider_code?: string; status?: string; limit?: number }): Promise<ApiResponse<ReconciliationRecord[]>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ id: 1, status: 'CONFLICT', conflict_type: 'amount_mismatch', currency: 'XAF' }], message: 'mock' };
    }
    const query = buildQuery({ ...params, status: params?.status ?? 'CONFLICT' });
    const response = await requestJson<{ reconciliation?: ReconciliationRecord[]; records?: ReconciliationRecord[] }>(`/v2/financial/reconciliation${query ? `?${query}` : ''}`, { method: 'GET' }, {});
    const record = toRecord(response.data);
    return { ...response, data: (record.reconciliation ?? record.records ?? []) as ReconciliationRecord[] };
  },

  async adminResolveReconciliation(id: number | string, payload: Record<string, unknown>): Promise<ApiResponse<ReconciliationRecord>> {
    if (useMocks) {
      await mockDelay();
      return { data: { id: Number(id), status: 'RESOLVED', conflict_type: 'amount_mismatch', currency: 'XAF' }, message: 'mock' };
    }
    return requestJson<ReconciliationRecord>(`/v2/financial/reconciliation/${encodeURIComponent(String(id))}/resolve`, { method: 'POST', body: JSON.stringify(payload) }, { id: Number(id), status: 'RESOLVED', conflict_type: 'unknown', currency: 'XAF' });
  },

  async adminListRefunds(params?: { status?: string; payment_transaction_id?: number; limit?: number }): Promise<ApiResponse<Refund[]>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ id: 1, number: 'AVR-2026-000001', status: 'REQUESTED', amount_minor: 300, currency: 'XAF' }], message: 'mock' };
    }
    const query = buildQuery(params ?? {});
    const response = await requestJson<{ refunds?: Refund[] }>(`/v2/financial/refunds${query ? `?${query}` : ''}`, { method: 'GET' }, {});
    const record = toRecord(response.data);
    return { ...response, data: (record.refunds ?? []) as Refund[] };
  },

  async adminApproveRefund(id: number | string): Promise<ApiResponse<Refund>> {
    if (useMocks) {
      await mockDelay();
      return { data: { id: Number(id), number: `AVR-2026-${String(id).padStart(6, '0')}`, status: 'APPROVED', amount_minor: 300, currency: 'XAF' }, message: 'mock' };
    }
    return requestJson<Refund>(`/v2/financial/refunds/${encodeURIComponent(String(id))}/approve`, { method: 'POST' }, { id: Number(id), number: '', status: 'APPROVED', amount_minor: 0, currency: 'XAF' });
  },

  async adminListCommissions(params?: { status?: string; beneficiary_user_id?: number; beneficiary_organization_id?: number; limit?: number }): Promise<ApiResponse<Commission[]>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ id: 1, status: 'CALCULATED', amount_minor: 300, currency: 'XAF', beneficiary_user_id: 1 }], message: 'mock' };
    }
    const query = buildQuery(params ?? {});
    const response = await requestJson<{ commissions?: Commission[] }>(`/v2/financial/commissions${query ? `?${query}` : ''}`, { method: 'GET' }, {});
    const record = toRecord(response.data);
    return { ...response, data: (record.commissions ?? []) as Commission[] };
  },

  async adminValidateCommission(id: number | string): Promise<ApiResponse<Commission>> {
    if (useMocks) {
      await mockDelay();
      return { data: { id: Number(id), status: 'VALIDATED', amount_minor: 300, currency: 'XAF' }, message: 'mock' };
    }
    return requestJson<Commission>(`/v2/financial/commissions/${encodeURIComponent(String(id))}/validate`, { method: 'POST' }, { id: Number(id), status: 'VALIDATED', amount_minor: 0, currency: 'XAF' });
  },

  async adminCreatePayout(payload: Record<string, unknown>): Promise<ApiResponse<Payout>> {
    if (useMocks) {
      await mockDelay();
      return { data: { id: 1, status: 'DRAFT', amount_minor: Number(payload.amount_minor ?? 0), currency: String(payload.currency ?? 'XAF') }, message: 'mock' };
    }
    return requestJson<Payout>('/v2/financial/payouts', { method: 'POST', body: JSON.stringify(payload) }, { id: 0, status: 'DRAFT', amount_minor: 0, currency: 'XAF' });
  },

  async adminListProviderEvents(params?: { provider_code?: string; status?: string; limit?: number }): Promise<ApiResponse<ProviderEvent[]>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ id: 1, provider_code: 'CAMPAY', event_type: 'webhook', provider_event_id: 'evt-1', status: 'RECEIVED' }], message: 'mock' };
    }
    const query = buildQuery(params ?? {});
    const response = await requestJson<{ provider_events?: ProviderEvent[] }>(`/v2/financial/provider-events${query ? `?${query}` : ''}`, { method: 'GET' }, {});
    const record = toRecord(response.data);
    return { ...response, data: (record.provider_events ?? []) as ProviderEvent[] };
  },

  async adminGetProviderHealth(): Promise<ApiResponse<ProviderHealth>> {
    if (useMocks) {
      await mockDelay();
      return {
        data: {
          code: 'CAMPAY',
          name: 'Campay',
          status: 'active',
          environment: 'sandbox',
          available: true,
          details: { supports_collection: true, supports_status_query: true, supports_webhook: true, supports_payout: true, supports_refund: false }
        },
        message: 'mock'
      };
    }
    return requestJson<ProviderHealth>('/v2/financial/providers/health', { method: 'GET' }, {
      code: 'CAMPAY',
      name: 'Campay',
      status: 'disabled',
      environment: 'sandbox',
      available: false,
      details: {}
    });
  }
};

export type ApiSdk = typeof apiSdk;
