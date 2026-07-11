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

export interface MatchResult {
  score: number;
  score_percent: number;
  grade: string;
  summary: string;
  eligible: boolean;
  breakdown: Record<string, number>;
  reasons: string[];
  distance_km: number | null;
  weights: Record<string, number>;
  target_type?: string;
  property?: PropertySummary | null;
  partner?: Record<string, unknown> | null;
}

export interface MatchQuery {
  target_type?: 'property' | 'partner';
  city?: string;
  region?: string;
  country?: string;
  budget_min?: number;
  budget_max?: number;
  budget?: number;
  latitude?: number;
  longitude?: number;
  property_type?: string;
  bedrooms_min?: number;
  availability?: string;
  need?: string;
  need_type?: string;
  partner_type?: string;
  project_type?: string;
  specialty?: string;
  language?: string;
  rating_min?: number;
  deadline_days?: number;
  subject_type?: string;
  status?: string;
  limit?: number;
  min_score?: number;
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

/* ── Brain / Advisor types ──────────────────────────────────── */

export interface BrainIntent {
  primary_intent: string;
  primary_score: number;
  is_multi_intent: boolean;
  intents: Array<{ intent: string; score: number; confidence: number }>;
  entities: {
    cities?: Array<{ city: string; match: string; region: string | null }>;
    budgets?: Array<{ raw: string; value: number; currency: string }>;
    property_types?: string[];
    surfaces_m2?: number[];
    bedrooms?: number[];
    lang?: string;
    confirmation?: boolean | null;
  };
  language: string;
  is_confirmation?: boolean | null;
  is_rejection?: boolean | null;
}

export interface BrainProgression {
  intent: string;
  progress_pct: number;
  total_steps: number;
  known_fields: string[];
  known_labels: string[];
  missing_fields: string[];
  next_question: string | null;
  next_key: string | null;
  complete: boolean;
  next_actions: string[];
}

export interface BrainSuggestion {
  type: string;
  content: string;
  action?: string;
  partner?: string;
  priority: string;
  priority_order: number;
  status?: string;
}

export interface BrainMemorySummary {
  total: number;
  by_kind: Record<string, number>;
  confirmed_facts: Array<Record<string, unknown>>;
  preferences: Array<Record<string, unknown>>;
  constraints: Array<Record<string, unknown>>;
  decisions: Array<Record<string, unknown>>;
  hypotheses: Array<Record<string, unknown>>;
  temporary: Array<Record<string, unknown>>;
}

export interface BrainResumption {
  has_history: boolean;
  short_summary: string;
  summary: string;
  objective?: string;
  city?: string;
  confirmed_count: number;
  pending_count: number;
  last_action?: string | null;
  next_step?: string | null;
  next_question?: string | null;
  language: string;
}

export interface BrainChatPayload {
  message: string;
  project_id: number;
  session_id?: number;
  language?: string;
  channel?: string;
}

export interface BrainChatResult {
  analysis: BrainIntent;
  detected_language: string;
  progression: BrainProgression;
  suggestions: BrainSuggestion[];
  memory_summary: BrainMemorySummary | null;
  intent_id?: number | null;
}

export interface BrainDossier {
  project: ProjectSummary;
  resume: BrainResumption;
}

export interface BrainConfirmResult {
  handled: boolean;
  reason?: string;
  results?: Array<{ key: string; action: string; success: boolean }>;
}

/* ── Relation / Match types ───────────────────── */

export interface BrainRelationMatch {
  relation_type: string;
  target_type: string;
  target_id: number;
  score: number;
  justification: string;
  metadata?: Record<string, unknown>;
}

export interface BrainFindMatchesPayload {
  project_id: number;
  partner_type?: string;
}

export interface BrainFindMatchesResult {
  proposals_count: number;
  properties_found: number;
  partners_found: number;
  proposals: BrainProposalResult[];
}

export interface BrainProposalResult {
  id: number;
  project_id: number;
  relation_type: string;
  target_type: string;
  target_id: number;
  score: number;
  justification: string;
  metadata_json?: string;
  status: string;
  proposed_at?: string | null;
  accepted_at?: string | null;
  rejected_at?: string | null;
  consent_requested_at?: string | null;
  consent_granted_at?: string | null;
  created_at: string;
  updated_at: string;
}

export interface BrainProposalActionPayload {
  proposal_id: number;
}

export interface BrainRelation {
  id: number;
  project_id: number;
  relation_type: string;
  source_type: string;
  source_id?: number | null;
  target_type: string;
  target_id: number;
  status: string;
  metadata_json?: string;
  established_at: string;
  created_at: string;
  updated_at: string;
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

  async getMatches(params?: MatchQuery): Promise<ApiResponse<MatchResult[]>> {
    if (useMocks) {
      await mockDelay();
      const targetType = params?.target_type ?? (params?.partner_type || params?.need ? 'partner' : 'property');
      if (targetType === 'partner') {
        return {
          data: [
            {
              score: 84,
              score_percent: 84,
              grade: 'excellent',
              summary: 'need +25; location +20; rating +10',
              eligible: true,
              breakdown: { need: 25, location: 20, rating: 10 },
              reasons: ['partner_type:photographer', 'city:Douala'],
              distance_km: null,
              weights: {},
              target_type: 'partner',
              partner: {
                id: 'partner-1',
                partner_type: 'photographer',
                display_name: 'LAWIM Studio Photo',
                description: 'Photographe immobilier et événementiel'
              }
            }
          ],
          message: 'mock'
        };
      }
      return {
        data: [
          {
            score: 76,
            score_percent: 76,
            grade: 'excellent',
            summary: 'city +20; budget +20; available +5',
            eligible: true,
            breakdown: { city: 20, budget: 20, availability: 5 },
            reasons: ['city match', 'budget ceiling compatible'],
            distance_km: 0,
            weights: {},
            target_type: 'property',
            property: mockProperties[0]
          }
        ],
        message: 'mock'
      };
    }

      const query = new URLSearchParams();
    for (const [key, value] of Object.entries(params ?? {})) {
      if (value === undefined || value === null || value === '') continue;
      query.set(key, String(value));
    }
    const response = await requestJson<unknown[]>(`/matches${query.toString() ? `?${query.toString()}` : ''}`, { method: 'GET' }, []);
    return {
      ...response,
      data: Array.isArray(response.data)
        ? response.data.map((item) => {
            const record = toRecord(item);
            return {
              ...(record as Record<string, unknown>),
              property: record.property ? mapPropertySummary(record.property) : undefined,
              partner: record.partner ? toRecord(record.partner) : undefined
            } as MatchResult;
          })
        : []
    };
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

  /* ── Brain / Advisor methods ────────────────────────────── */

  async brainChat(payload: BrainChatPayload): Promise<ApiResponse<BrainChatResult>> {
    if (useMocks) {
      await mockDelay();
      return {
        data: {
          analysis: {
            primary_intent: 'buy',
            primary_score: 80,
            is_multi_intent: false,
            intents: [{ intent: 'buy', score: 80, confidence: 1 }],
            entities: {},
            language: 'fr',
            is_confirmation: null,
            is_rejection: null
          },
          detected_language: 'fr',
          progression: {
            intent: 'buy',
            progress_pct: 20,
            total_steps: 6,
            known_fields: [],
            known_labels: [],
            missing_fields: ['city', 'budget_max', 'property_type'],
            next_question: 'Dans quelle ville souhaitez-vous acheter ?',
            next_key: 'buy_city',
            complete: false,
            next_actions: ['Vérifier le titre foncier', 'Rechercher un financement']
          },
          suggestions: [],
          memory_summary: null,
          intent_id: null
        },
        message: 'mock'
      };
    }
    const response = await requestJson<{ brain: Record<string, unknown> }>(
      '/v2/assistant/brain/chat',
      {
        method: 'POST',
        body: JSON.stringify({
          message: payload.message,
          project_id: payload.project_id,
          session_id: payload.session_id,
          language: payload.language,
          channel: payload.channel
        })
      },
      { brain: {} }
    );
    const brain = toRecord(response.data.brain);
    const analysis = toRecord(brain.analysis);
    const progression = toRecord(brain.progression);
    const suggestions = Array.isArray(brain.suggestions) ? brain.suggestions : [];
    return {
      ...response,
      data: {
        analysis: {
          primary_intent: toText(analysis.primary_intent, 'other'),
          primary_score: toNumber(analysis.primary_score, 50),
          is_multi_intent: Boolean(analysis.is_multi_intent),
          intents: Array.isArray(analysis.intents) ? analysis.intents.map((i: Record<string, unknown>) => ({
            intent: toText(i.intent),
            score: toNumber(i.score),
            confidence: toNumber(i.confidence)
          })) : [],
          entities: toRecord(analysis.entities) as BrainIntent['entities'],
          language: toText(analysis.language, 'fr'),
          is_confirmation: analysis.is_confirmation as boolean | null,
          is_rejection: analysis.is_rejection as boolean | null
        },
        detected_language: toText(brain.detected_language, 'fr'),
        progression: {
          intent: toText(progression.intent),
          progress_pct: toNumber(progression.progress_pct),
          total_steps: toNumber(progression.total_steps),
          known_fields: Array.isArray(progression.known_fields) ? progression.known_fields.map(String) : [],
          known_labels: Array.isArray(progression.known_labels) ? progression.known_labels.map(String) : [],
          missing_fields: Array.isArray(progression.missing_fields) ? progression.missing_fields.map(String) : [],
          next_question: progression.next_question ? toText(progression.next_question) : null,
          next_key: progression.next_key ? toText(progression.next_key) : null,
          complete: Boolean(progression.complete),
          next_actions: Array.isArray(progression.next_actions) ? progression.next_actions.map(String) : []
        },
        suggestions: Array.isArray(suggestions) ? suggestions.map((s: Record<string, unknown>) => ({
          type: toText(s.type),
          content: toText(s.content),
          action: s.action ? toText(s.action) : undefined,
          partner: s.partner ? toText(s.partner) : undefined,
          priority: toText(s.priority, 'medium'),
          priority_order: toNumber(s.priority_order),
          status: s.status ? toText(s.status) : undefined
        })) : [],
        memory_summary: brain.memory_summary ? (toRecord(brain.memory_summary) as unknown as BrainMemorySummary) : null,
        intent_id: brain.intent_id ? toNumber(brain.intent_id) : null
      }
    };
  },

  async brainDossiers(): Promise<ApiResponse<BrainDossier[]>> {
    if (useMocks) {
      await mockDelay();
      return {
        data: [
          {
            project: {
              id: 1, title: 'Terrain à Douala', status: 'active',
              project_type: 'buy', objective: 'Acheter un terrain',
              location_city: 'Douala', budget_min: 25000000, budget_max: 50000000
            },
            resume: {
              has_history: true,
              short_summary: 'Nous avions avancé sur votre recherche de terrain à Douala.',
              summary: 'Nous avions avancé sur votre projet Terrain à Douala.',
              objective: 'Acheter un terrain',
              city: 'Douala',
              confirmed_count: 1,
              pending_count: 0,
              next_question: 'Quel usage pour ce terrain ?',
              language: 'fr'
            }
          }
        ],
        message: 'mock'
      };
    }
    const response = await requestJson<{ dossiers: unknown[] }>(
      '/v2/assistant/brain/dossiers',
      { method: 'GET' },
      { dossiers: [] }
    );
    const dossiers = Array.isArray(response.data.dossiers) ? response.data.dossiers : [];
    return {
      ...response,
      data: (Array.isArray(response.data.dossiers) ? response.data.dossiers : []).map((item: unknown) => {
        const record = toRecord(item);
        return {
          project: record.project ? (toRecord(record.project) as unknown as ProjectSummary) : ({
            id: 0, title: 'Projet', status: 'draft', project_type: 'other', objective: ''
          } as ProjectSummary),
          resume: record.resume ? (toRecord(record.resume) as unknown as BrainResumption) : {
            has_history: false,
            short_summary: '',
            summary: '',
            confirmed_count: 0,
            pending_count: 0,
            language: 'fr'
          }
        };
      })
    };
  },

  async brainResume(projectId: number, language?: string): Promise<ApiResponse<BrainResumption>> {
    if (useMocks) {
      await mockDelay();
      return {
        data: {
          has_history: true,
          short_summary: 'Reprise de votre projet.',
          summary: 'Nous avions avancé sur votre projet.',
          objective: 'Projet immobilier',
          confirmed_count: 2,
          pending_count: 1,
          next_question: 'Quel est votre budget ?',
          language: language || 'fr'
        },
        message: 'mock'
      };
    }
    const query = language ? `?language=${language}` : '';
    const response = await requestJson<{ resumption: Record<string, unknown> }>(
      `/v2/assistant/brain/dossiers/${projectId}/resume${query}`,
      { method: 'GET' },
      { resumption: {} }
    );
    const r = toRecord(response.data.resumption);
    return {
      ...response,
      data: {
        has_history: Boolean(r.has_history),
        short_summary: toText(r.short_summary),
        summary: toText(r.summary),
        objective: r.objective ? toText(r.objective) : undefined,
        city: r.city ? toText(r.city) : undefined,
        confirmed_count: toNumber(r.confirmed_count),
        pending_count: toNumber(r.pending_count),
        last_action: r.last_action ? toText(r.last_action) : null,
        next_step: r.next_step ? toText(r.next_step) : null,
        next_question: r.next_question ? toText(r.next_question) : null,
        language: toText(r.language, 'fr')
      }
    };
  },

  async brainConfirm(projectId: number, message: string, language?: string): Promise<ApiResponse<BrainConfirmResult>> {
    if (useMocks) {
      await mockDelay();
      return {
        data: { handled: true, results: [{ key: 'budget_max', action: 'confirmed', success: true }] },
        message: 'mock'
      };
    }
    const response = await requestJson<{ confirmation: Record<string, unknown> }>(
      '/v2/assistant/brain/confirm',
      {
        method: 'POST',
        body: JSON.stringify({
          project_id: projectId,
          message,
          language: language || 'fr'
        })
      },
      { confirmation: {} }
    );
    const c = toRecord(response.data.confirmation);
    return {
      ...response,
      data: {
        handled: Boolean(c.handled),
        reason: c.reason ? toText(c.reason) : undefined,
        results: Array.isArray(c.results) ? c.results.map((r: Record<string, unknown>) => ({
          key: toText(r.key),
          action: toText(r.action),
          success: Boolean(r.success)
        })) : undefined
      }
    };
  },

  async brainFindMatches(payload: BrainFindMatchesPayload): Promise<ApiResponse<BrainFindMatchesResult>> {
    if (useMocks) {
      await mockDelay();
      return {
        data: {
          proposals_count: 2,
          properties_found: 1,
          partners_found: 1,
          proposals: [
            { id: 1, project_id: payload.project_id, relation_type: 'person_to_property', target_type: 'property', target_id: 1, score: 85, justification: 'Correspond à votre recherche', status: 'detected', proposed_at: new Date().toISOString(), created_at: new Date().toISOString(), updated_at: new Date().toISOString() },
            { id: 2, project_id: payload.project_id, relation_type: 'person_to_partner', target_type: 'partner', target_id: 1, score: 72, justification: 'Professionnel recommandé', status: 'detected', proposed_at: new Date().toISOString(), created_at: new Date().toISOString(), updated_at: new Date().toISOString() }
          ]
        },
        message: 'mock'
      };
    }
    const response = await requestJson<{ proposals_count: number; properties_found: number; partners_found: number; proposals: unknown[] }>(
      '/v2/assistant/brain/matching',
      { method: 'POST', body: JSON.stringify(payload) },
      { proposals_count: 0, properties_found: 0, partners_found: 0, proposals: [] }
    );
    return {
      ...response,
      data: {
        proposals_count: Number(response.data.proposals_count ?? 0),
        properties_found: Number(response.data.properties_found ?? 0),
        partners_found: Number(response.data.partners_found ?? 0),
        proposals: Array.isArray(response.data.proposals) ? response.data.proposals.map((p: unknown) => toRecord(p) as unknown as BrainProposalResult) : []
      }
    };
  },

  async brainProposals(projectId: number, status?: string): Promise<ApiResponse<BrainProposalResult[]>> {
    if (useMocks) {
      await mockDelay();
      return {
        data: [
          { id: 1, project_id: projectId, relation_type: 'person_to_property', target_type: 'property', target_id: 1, score: 85, justification: 'Correspond à votre recherche', status: status || 'detected', proposed_at: new Date().toISOString(), created_at: new Date().toISOString(), updated_at: new Date().toISOString() }
        ],
        message: 'mock'
      };
    }
    const query = status ? `?status=${status}` : '';
    const response = await requestJson<{ proposals: unknown[] }>(
      `/v2/assistant/brain/dossiers/${projectId}/matches${query}`,
      { method: 'GET' },
      { proposals: [] }
    );
    return {
      ...response,
      data: Array.isArray(response.data.proposals) ? response.data.proposals.map((p: unknown) => toRecord(p) as unknown as BrainProposalResult) : []
    };
  },

  async brainAcceptProposal(payload: BrainProposalActionPayload): Promise<ApiResponse<BrainProposalResult>> {
    if (useMocks) {
      await mockDelay();
      return { data: { id: payload.proposal_id, project_id: 0, relation_type: '', target_type: '', target_id: 0, score: 0, justification: '', status: 'accepted', accepted_at: new Date().toISOString(), created_at: new Date().toISOString(), updated_at: new Date().toISOString() }, message: 'mock' };
    }
    return requestJson<BrainProposalResult>(
      '/v2/assistant/brain/proposals/accept',
      { method: 'POST', body: JSON.stringify({ proposal_id: payload.proposal_id }) },
      { id: payload.proposal_id, project_id: 0, relation_type: '', target_type: '', target_id: 0, score: 0, justification: '', status: 'accepted', created_at: '', updated_at: '' }
    );
  },

  async brainRejectProposal(payload: BrainProposalActionPayload): Promise<ApiResponse<BrainProposalResult>> {
    if (useMocks) {
      await mockDelay();
      return { data: { id: payload.proposal_id, project_id: 0, relation_type: '', target_type: '', target_id: 0, score: 0, justification: '', status: 'rejected', rejected_at: new Date().toISOString(), created_at: new Date().toISOString(), updated_at: new Date().toISOString() }, message: 'mock' };
    }
    return requestJson<BrainProposalResult>(
      '/v2/assistant/brain/proposals/reject',
      { method: 'POST', body: JSON.stringify({ proposal_id: payload.proposal_id }) },
      { id: payload.proposal_id, project_id: 0, relation_type: '', target_type: '', target_id: 0, score: 0, justification: '', status: 'rejected', created_at: '', updated_at: '' }
    );
  },

  async brainGrantConsent(payload: BrainProposalActionPayload): Promise<ApiResponse<BrainProposalResult>> {
    if (useMocks) {
      await mockDelay();
      return { data: { id: payload.proposal_id, project_id: 0, relation_type: '', target_type: '', target_id: 0, score: 0, justification: '', status: 'relation_established', consent_granted_at: new Date().toISOString(), created_at: new Date().toISOString(), updated_at: new Date().toISOString() }, message: 'mock' };
    }
    return requestJson<BrainProposalResult>(
      '/v2/assistant/brain/consent/grant',
      { method: 'POST', body: JSON.stringify({ proposal_id: payload.proposal_id }) },
      { id: payload.proposal_id, project_id: 0, relation_type: '', target_type: '', target_id: 0, score: 0, justification: '', status: 'relation_established', created_at: '', updated_at: '' }
    );
  },

  async brainRelations(projectId: number): Promise<ApiResponse<BrainRelation[]>> {
    if (useMocks) {
      await mockDelay();
      return {
        data: [
          { id: 1, project_id: projectId, relation_type: 'person_to_property', source_type: 'proposal', source_id: 1, target_type: 'property', target_id: 1, status: 'relation_established', established_at: new Date().toISOString(), created_at: new Date().toISOString(), updated_at: new Date().toISOString() }
        ],
        message: 'mock'
      };
    }
    const response = await requestJson<{ relations: unknown[] }>(
      `/v2/assistant/brain/dossiers/${projectId}/relations`,
      { method: 'GET' },
      { relations: [] }
    );
    return {
      ...response,
      data: Array.isArray(response.data.relations) ? response.data.relations.map((r: unknown) => toRecord(r) as unknown as BrainRelation) : []
    };
  },

  async brainCreateDossier(payload: Record<string, unknown>): Promise<ApiResponse<ProjectSummary>> {
    if (useMocks) {
      await mockDelay();
      return {
        data: {
          id: Date.now(),
          title: toText(payload.title, 'Projet'),
          status: 'draft',
          project_type: toText(payload.project_type, 'other'),
          objective: toText(payload.objective, ''),
          location_city: payload.location_city ? toText(payload.location_city) : undefined,
          budget_min: payload.budget_min ? toNumber(payload.budget_min) : null,
          budget_max: payload.budget_max ? toNumber(payload.budget_max) : null
        },
        message: 'mock'
      };
    }
    const response = await requestJson<{ project: Record<string, unknown> }>(
      '/v2/assistant/brain/dossiers',
      {
        method: 'POST',
        body: JSON.stringify(payload)
      },
      { project: {} }
    );
    return {
      ...response,
      data: mapProjectSummary(toRecord(response.data.project))
    };
  },

  async brainSuggestions(projectId: number, status?: string): Promise<ApiResponse<BrainSuggestion[]>> {
    if (useMocks) {
      await mockDelay();
      return {
        data: [
          { type: 'action', content: 'Vérifier le titre foncier', action: 'search_land', priority: 'high', priority_order: 3 },
          { type: 'partner', content: 'Consulter un notaire', partner: 'notaire', priority: 'high', priority_order: 3 }
        ],
        message: 'mock'
      };
    }
    const query = status ? `?status=${status}` : '';
    const response = await requestJson<{ suggestions: unknown[] }>(
      `/v2/assistant/brain/dossiers/${projectId}/suggestions${query}`,
      { method: 'GET' },
      { suggestions: [] }
    );
    const suggestions = Array.isArray(response.data.suggestions) ? response.data.suggestions : [];
    return {
      ...response,
      data: suggestions.map((s: unknown) => {
        const rec = toRecord(s);
        return {
          type: toText(rec.type || rec.suggestion_type),
          content: toText(rec.content),
          action: rec.action || rec.target_action ? toText(rec.action || rec.target_action) : undefined,
          partner: rec.partner || rec.target_partner ? toText(rec.partner || rec.target_partner) : undefined,
          priority: toText(rec.priority, 'medium'),
          priority_order: toNumber(rec.priority_order),
          status: rec.status ? toText(rec.status) : undefined
        };
      })
    };
  },

  async createEstimation(payload: EstimationPayload): Promise<ApiResponse<EstimationResult>> {
    if (useMocks) {
      await mockDelay();
      return { data: { estimate: '€500k - €560k', confidence: 'High' }, message: 'mock' };
    }
    return requestJson<EstimationResult>('/v2/estimation', { method: 'POST', body: JSON.stringify(payload) }, { estimate: 'Pending', confidence: 'Low' });
  }
};

export type ApiSdk = typeof apiSdk;
